// Stats page at /_stats. Cloudflare Access sits in front of the path; the
// worker additionally verifies the Access token itself, so a missing or
// misconfigured Access policy fails closed (404) instead of exposing the page.

const PERIODS = [7, 30, 90, 365];

export async function stats(request, env) {
  if (!(await accessOk(request, env))) return new Response("Not found", { status: 404 });
  const d = +new URL(request.url).searchParams.get("days");
  return new Response(await render(env, PERIODS.includes(d) ? d : 30), {
    headers: { "Content-Type": "text/html; charset=utf-8", "Cache-Control": "no-store",
               "X-Robots-Tag": "noindex" },
  });
}

export async function render(env, days) {
  const since = Date.now() - days * 86400e3;
  const people = "ts > ?1 AND kind != 'bot'";

  const [kinds, daily, pages, refs, countries, bots] = (await env.DB.batch([
    `SELECT kind, count(*) n, count(DISTINCT day || visitor) vd FROM classified WHERE ts > ?1 GROUP BY kind`,
    `SELECT day, sum(kind='human') human, sum(kind='probable') probable, sum(kind='bot') bot,
            count(DISTINCT CASE WHEN kind != 'bot' THEN visitor END) visitors
       FROM classified WHERE ts > ?1 GROUP BY day`,
    `SELECT path, sum(kind='human') human, sum(kind='probable') probable FROM classified
      WHERE ${people} GROUP BY path ORDER BY count(*) DESC LIMIT 20`,
    `SELECT ref, sum(kind='human') human, sum(kind='probable') probable, sum(kind='bot') bot FROM classified WHERE ts > ?1 AND ref IS NOT NULL
      GROUP BY ref ORDER BY sum(kind != 'bot') DESC, bot DESC LIMIT 20`,
    `SELECT country, sum(kind='human') human, sum(kind='probable') probable, sum(kind='bot') bot FROM classified WHERE ts > ?1
      GROUP BY country ORDER BY sum(kind != 'bot') DESC, bot DESC LIMIT 20`,
    `SELECT ua, as_org, ua_bot, dc, lang IS NULL no_lang, count(*) n FROM classified
      WHERE ts > ?1 AND kind = 'bot' GROUP BY ua, as_org ORDER BY n DESC LIMIT 15`,
  ].map((q) => env.DB.prepare(q).bind(since)))).map((r) => r.results);

  const k = Object.fromEntries(kinds.map((r) => [r.kind, r]));
  const byDay = Object.fromEntries(daily.map((r) => [r.day, r]));
  const series = [];
  for (let i = days - 1; i >= 0; i--) {
    const day = new Date(Date.now() - i * 86400e3).toISOString().slice(0, 10);
    series.push(byDay[day] || { day, human: 0, probable: 0, bot: 0, visitors: 0 });
  }
  const visitorDays = series.reduce((s, r) => s + r.visitors, 0);

  return `<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<title>Site stats</title><style>${CSS}</style></head><body><main>
<header><h1>vadimsemenov.com</h1><nav>${PERIODS.map((d) =>
    `<a href="?days=${d}"${d === days ? ' aria-current="page"' : ""}>${d} days</a>`).join("")}</nav></header>
<section class="tiles">
  ${tile("Human views", k.human?.n || 0, "beacon confirmed")}
  ${tile("Probable views", k.probable?.n || 0, "browser, no beacon")}
  ${tile("Visitors", visitorDays, "unique per day, summed")}
  ${tile("Bot views", k.bot?.n || 0, "filtered out")}
</section>
<section class="card"><h2>Daily views</h2>
  <div class="legend"><span><i style="background:var(--s1)"></i>Human</span><span><i style="background:var(--s2)"></i>Probable</span></div>
  ${chart(series)}
  <details><summary>Table</summary>${table(series.slice().reverse(),
    [["day", "Day"], ["human", "Human"], ["probable", "Probable"], ["visitors", "Visitors"], ["bot", "Bots"]])}</details>
</section>
<div class="grid">
<section class="card"><h2>Pages</h2>${table(pages, [["path", "Path"], ["human", "Human"], ["probable", "Probable"]])}</section>
<section class="card"><h2>Referrers</h2>${table(refs, [["ref", "Referrer"], ...[["human", "Human"], ["probable", "Probable"], ["bot", "Bot"]]])}</section>
<section class="card"><h2>Countries</h2>${table(countries, [["country", "Country"], ...[["human", "Human"], ["probable", "Probable"], ["bot", "Bot"]]])}</section>
<section class="card wide"><h2>Top bot sources</h2>${table(bots.map((b) => ({ ...b,
    why: [b.ua_bot && "user agent", b.dc && "hosting network", b.no_lang && "no language"].filter(Boolean).join(", ") || "no beacon / headers" })),
    [["ua", "User agent"], ["as_org", "Network"], ["why", "Flagged by"], ["n", "Views"]])}</section>
</div>
<p class="note">Human: page shown in a real browser (visible 3 s or scrolled). Probable: browser-like request
with no beacon, e.g. ad blocker, JavaScript off, or left within 3 s. Visitors are counted per day from a
daily-salted hash and summed over the period.</p>
</main><div id="tip" role="status" hidden></div><script>${TIP_JS}</script></body></html>`;
}

function tile(label, value, sub) {
  return `<div class="tile"><div class="label">${label}</div><div class="value">${value.toLocaleString("en-US")}</div><div class="sub">${sub}</div></div>`;
}

function table(rows, cols) {
  if (!rows.length) return `<p class="empty">No data yet.</p>`;
  return `<div class="scroll"><table><thead><tr>${cols.map(([, h], i) =>
    `<th${i ? ' class="num"' : ""}>${h}</th>`).join("")}</tr></thead><tbody>${rows.map((r) =>
    `<tr>${cols.map(([c], i) => `<td${i ? ' class="num"' : ""}>${esc(r[c] ?? "")}</td>`).join("")}</tr>`).join("")}
  </tbody></table></div>`;
}

function chart(series) {
  const W = 720, H = 220, L = 36, B = 22, T = 8;
  const pw = W - L - 4, ph = H - B - T;
  const max = Math.max(1, ...series.map((r) => r.human + r.probable));
  const step = niceStep(max);
  const top = Math.ceil(max / step) * step;
  const y = (v) => T + ph - (v / top) * ph;
  const slot = pw / series.length, bw = Math.max(2, Math.min(28, slot * 0.7));
  let g = "";
  for (let v = 0; v <= top; v += step) {
    g += `<line x1="${L}" x2="${W - 4}" y1="${y(v)}" y2="${y(v)}" class="gl"/>` +
         `<text x="${L - 6}" y="${y(v) + 4}" class="axis" text-anchor="end">${v}</text>`;
  }
  const labelEvery = Math.ceil(series.length / 6);
  series.forEach((r, i) => {
    const x = L + i * slot + (slot - bw) / 2;
    const hTop = y(r.human), pTop = y(r.human + r.probable);
    if (r.human) g += bar(x, hTop, bw, y(0) - hTop, !r.probable);
    if (r.probable) g += bar(x, pTop, bw, Math.max(0, hTop - pTop - (r.human ? 2 : 0)), true, "s2");
    if ((series.length - 1 - i) % labelEvery === 0)
      g += `<text x="${x + bw / 2}" y="${H - 6}" class="axis" text-anchor="middle">${r.day.slice(5)}</text>`;
    g += `<rect x="${L + i * slot}" y="${T}" width="${slot}" height="${ph}" class="hit" tabindex="0"
           data-tip="${r.day}|${r.human}|${r.probable}|${r.visitors}|${r.bot}"/>`;
  });
  return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Daily human and probable views">${g}
    <line x1="${L}" x2="${W - 4}" y1="${y(0)}" y2="${y(0)}" class="base"/></svg>`;
}

function bar(x, top, w, h, rounded, cls = "s1") {
  if (h <= 0) return "";
  const r = rounded ? Math.min(4, w / 2, h) : 0;
  return `<path class="${cls}" d="M${x},${top + h}V${top + r}q0,-${r} ${r},-${r}h${w - 2 * r}q${r},0 ${r},${r}V${top + h}Z"/>`;
}

function niceStep(max) {
  const raw = max / 4, p = 10 ** Math.floor(Math.log10(raw));
  return [1, 2, 5, 10].map((m) => m * p).find((s) => s >= raw) || p * 10;
}

function esc(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
}

async function accessOk(request, env) {
  if (!env.ACCESS_TEAM || !env.ACCESS_AUD) return false;
  try {
    const jwt = request.headers.get("Cf-Access-Jwt-Assertion") || "";
    const [h, p, s] = jwt.split(".");
    const header = JSON.parse(atob(b64(h))), payload = JSON.parse(atob(b64(p)));
    const iss = `https://${env.ACCESS_TEAM}.cloudflareaccess.com`;
    const aud = [].concat(payload.aud);
    if (payload.iss !== iss || !aud.includes(env.ACCESS_AUD) || payload.exp * 1000 < Date.now()) return false;
    const { keys } = await (await fetch(`${iss}/cdn-cgi/access/certs`)).json();
    const jwk = keys.find((k) => k.kid === header.kid);
    if (!jwk) return false;
    const alg = { name: "RSASSA-PKCS1-v1_5", hash: "SHA-256" };
    const key = await crypto.subtle.importKey("jwk", jwk, alg, false, ["verify"]);
    const sig = Uint8Array.from(atob(b64(s)), (c) => c.charCodeAt(0));
    return await crypto.subtle.verify(alg, key, sig, new TextEncoder().encode(`${h}.${p}`));
  } catch (e) {
    return false;
  }
}

function b64(s) {
  s = s.replace(/-/g, "+").replace(/_/g, "/");
  return s + "=".repeat((4 - (s.length % 4)) % 4);
}

const CSS = `
:root{color-scheme:light;--bg:#f4f4f2;--surface:#fcfcfb;--line:#e4e3df;--text:#0b0b0b;--text2:#52514e;--muted:#7a7974;--s1:#2a78d6;--s2:#eb6834}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){color-scheme:dark;--bg:#111110;--surface:#1a1a19;--line:#2e2e2b;--text:#fff;--text2:#c3c2b7;--muted:#8f8e86;--s1:#3987e5;--s2:#d95926}}
:root[data-theme="dark"]{color-scheme:dark;--bg:#111110;--surface:#1a1a19;--line:#2e2e2b;--text:#fff;--text2:#c3c2b7;--muted:#8f8e86;--s1:#3987e5;--s2:#d95926}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:1040px;margin:0 auto;padding:24px 16px 48px}
header{display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:space-between;margin-bottom:20px}
h1{font-size:20px;font-weight:600;margin:0}h2{font-size:14px;font-weight:600;margin:0 0 12px;color:var(--text2)}
nav{display:flex;gap:4px}nav a{white-space:nowrap;padding:5px 10px;border-radius:6px;color:var(--text2);text-decoration:none;font-size:13px;border:1px solid var(--line)}
nav a[aria-current]{background:var(--text);color:var(--bg);border-color:var(--text)}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(150px,45%),1fr));gap:12px;margin-bottom:12px}
.tile,.card{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:16px}
.label{font-size:13px;color:var(--text2)}.value{font-size:28px;font-weight:600;font-variant-numeric:tabular-nums;margin:2px 0}.sub{font-size:12px;color:var(--muted)}
.card{margin-bottom:12px;min-width:0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(320px,100%),1fr));gap:12px}.grid .card{margin:0}.wide{grid-column:1/-1}
.legend{display:flex;gap:16px;font-size:13px;color:var(--text2);margin-bottom:6px}.legend i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:6px;vertical-align:-1px}
svg{width:100%;height:auto;display:block}.gl{stroke:var(--line);stroke-width:1}.base{stroke:var(--muted);stroke-width:1}
.axis{fill:var(--muted);font-size:11px;font-variant-numeric:tabular-nums}.s1{fill:var(--s1)}.s2{fill:var(--s2)}
.hit{fill:transparent;outline:none}.hit:hover,.hit:focus{fill:var(--text);fill-opacity:.06}
details{margin-top:8px;font-size:13px;color:var(--text2)}summary{cursor:pointer}
.scroll{overflow-x:auto}table{width:100%;border-collapse:collapse;font-size:13px}
th{text-align:left;font-weight:500;color:var(--muted);border-bottom:1px solid var(--line);padding:4px 8px 6px 0}
td{padding:5px 8px 5px 0;border-bottom:1px solid var(--line);color:var(--text);max-width:340px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.num{text-align:right;font-variant-numeric:tabular-nums}.empty{color:var(--muted);font-size:13px;margin:0}
.note{font-size:12px;color:var(--muted);max-width:720px}
#tip{position:fixed;pointer-events:none;background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:8px 10px;font-size:12px;box-shadow:0 4px 16px rgba(0,0,0,.15);z-index:9}
#tip b{display:block;margin-bottom:2px}#tip i{display:inline-block;width:8px;height:8px;border-radius:2px;margin-right:6px}
`;

const TIP_JS = `
var tip=document.getElementById("tip");
function show(el,x,y){var d=el.dataset.tip.split("|");
tip.innerHTML="<b>"+d[0]+"</b><i style='background:var(--s1)'></i>Human "+d[1]+"<br><i style='background:var(--s2)'></i>Probable "+d[2]+"<br>Visitors "+d[3]+" &middot; Bots "+d[4];
tip.hidden=false;var w=tip.offsetWidth;tip.style.left=Math.min(x+12,innerWidth-w-8)+"px";tip.style.top=(y-tip.offsetHeight-12)+"px"}
document.querySelectorAll(".hit").forEach(function(el){
el.addEventListener("mousemove",function(e){show(el,e.clientX,e.clientY)});
el.addEventListener("focus",function(){var r=el.getBoundingClientRect();show(el,r.left+r.width/2,r.top+40)});
el.addEventListener("mouseleave",function(){tip.hidden=true});el.addEventListener("blur",function(){tip.hidden=true})});
`;
