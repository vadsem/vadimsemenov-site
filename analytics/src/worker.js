// Page-view counter for vadimsemenov.com. Sits in front of GitHub Pages:
// every request is passed through unchanged, HTML pages are logged to D1 and
// get a small inline beacon that confirms a real browser displayed them.

const BEACON = "/_k";   // neutral name, avoids /count, /collect, /track filter rules

const BOT_UA = new RegExp([
  "bot", "crawl", "spider", "slurp", "scrap", "fetch", "preview", "monitor",
  "uptime", "check", "lighthouse", "pingdom", "headless", "phantom", "selenium",
  "puppeteer", "playwright", "curl", "wget", "python", "httpx", "aiohttp",
  "go-http", "java/", "okhttp", "libwww", "perl", "ruby", "php", "node-fetch",
  "axios", "undici", "facebookexternalhit", "whatsapp", "telegram", "discord",
  "slack", "embedly", "archive", "feed", "rss",
].join("|"), "i");

// Hosting / cloud networks: real visitors almost never browse from these.
// Cloudflare and Akamai are deliberately absent: iCloud Private Relay and WARP
// send ordinary Safari / phone traffic out through them.
const DC_ASN = new Set([
  16509, 14618, 8987,            // Amazon
  15169, 396982, 19527,          // Google
  8075, 8068,                    // Microsoft
  14061, 16276, 24940, 63949,    // DigitalOcean, OVH, Hetzner, Linode
  20473, 51167, 31898, 45102,    // Vultr, Contabo, Oracle, Alibaba
  132203, 45090,                 // Tencent
  36352, 55286, 62567, 46606,    // ColoCrossing, B2 Net, DigitalOcean, Unified Layer
  12876, 9009, 60781, 212238,    // Scaleway, M247, LeaseWeb, Datacamp
]);
const DC_ORG = /hosting|cloud(?!flare)|server|data ?cent|colo|vps|dedicated/i;

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;

export default {
  async fetch(request, env, ctx) {
    ctx.passThroughOnException();
    const url = new URL(request.url);

    if (url.pathname === BEACON) {
      // The body must be read before responding; the database write can trail.
      if (request.method === "POST") {
        const text = await request.text();
        ctx.waitUntil(beacon(text, env).catch(() => {}));
      }
      return new Response(null, { status: 204 });
    }

    if (request.method !== "GET" || !isPagePath(url.pathname)) return fetch(request);

    // Drop conditional headers so the origin returns the full page (not a 304),
    // since every view gets its own id in the body.
    const headers = new Headers(request.headers);
    headers.delete("If-None-Match");
    headers.delete("If-Modified-Since");
    const resp = await fetch(new Request(request, { headers }));

    const type = resp.headers.get("Content-Type") || "";
    if (resp.status !== 200 || !type.startsWith("text/html")) return resp;

    const id = crypto.randomUUID();
    ctx.waitUntil(logView(request, url, id, env).catch(() => {}));

    const out = new Response(resp.body, resp);
    out.headers.set("Cache-Control", "no-store");
    out.headers.delete("ETag");
    out.headers.delete("Last-Modified");
    return new HTMLRewriter()
      .on("body", { element(e) { e.append(snippet(id), { html: true }); } })
      .transform(out);
  },
};

function isPagePath(p) {
  return p.endsWith("/") || p.endsWith(".html") || !p.split("/").pop().includes(".");
}

function snippet(id) {
  // Fires once: after 3 s of visibility, or on the first scroll / click / key.
  return `<script>(function(){var s=0,t;function f(w){if(s)return;s=1;clearTimeout(t);` +
    `try{navigator.sendBeacon("${BEACON}",JSON.stringify({id:"${id}",w:w,` +
    `d:navigator.webdriver?1:0,x:screen.width}))}catch(e){}}` +
    `function v(){clearTimeout(t);if(document.visibilityState==="visible")t=setTimeout(function(){f("v")},3000)}` +
    `document.addEventListener("visibilitychange",v);v();` +
    `["scroll","pointerdown","keydown"].forEach(function(e){addEventListener(e,function(){f("i")},{once:true,passive:true})})` +
    `})();</script>`;
}

async function logView(request, url, id, env) {
  const h = request.headers;
  const cf = request.cf || {};
  const ua = h.get("User-Agent") || "";
  const ip = h.get("CF-Connecting-IP") || "";
  const now = Date.now();
  const lang = (h.get("Accept-Language") || "").split(",")[0].trim() || null;
  let ref = null;
  try {
    const r = new URL(h.get("Referer"));
    if (r.host !== url.host) ref = r.origin + r.pathname;
  } catch (e) {}

  const salt = await dailySalt(env, new Date(now).toISOString().slice(0, 10));
  const visitor = await sha256(`${salt}|${ip}|${ua}`);
  const asn = cf.asn || null;
  const dc = (asn && DC_ASN.has(asn)) || DC_ORG.test(cf.asOrganization || "") ? 1 : 0;

  await env.DB.prepare(
    `INSERT INTO views (id, ts, host, path, ref, ua, lang, sec_fetch, country, asn, as_org,
                        ua_bot, dc, visitor)
     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
  ).bind(id, now, url.host, url.pathname, ref, ua, lang, h.has("Sec-Fetch-Mode") ? 1 : 0,
         cf.country || null, asn, cf.asOrganization || null,
         !ua || BOT_UA.test(ua) ? 1 : 0, dc, visitor).run();
}

async function beacon(text, env) {
  const body = JSON.parse(text.slice(0, 500));
  if (!UUID.test(body.id || "")) return;
  // Only the first beacon per view counts, and only within an hour of the page request.
  await env.DB.prepare(
    `UPDATE views SET beacon_ts = ?, beacon_why = ?, webdriver = ?, screen_w = ?
     WHERE id = ? AND beacon_ts IS NULL AND ts > ?`
  ).bind(Date.now(), body.w === "i" ? "i" : "v", body.d ? 1 : 0,
         Number.isInteger(body.x) ? body.x : null, body.id, Date.now() - 3600e3).run();
}

async function dailySalt(env, day) {
  const row = await env.DB.prepare("SELECT salt FROM salts WHERE day = ?").bind(day).first();
  if (row) return row.salt;
  const salt = crypto.randomUUID();
  await env.DB.batch([
    env.DB.prepare("INSERT OR IGNORE INTO salts (day, salt) VALUES (?, ?)").bind(day, salt),
    env.DB.prepare("DELETE FROM salts WHERE day < ?").bind(day),
  ]);
  // Another request may have won the race; read back whichever salt was stored.
  return (await env.DB.prepare("SELECT salt FROM salts WHERE day = ?").bind(day).first()).salt;
}

async function sha256(s) {
  const d = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s));
  return [...new Uint8Array(d)].map((b) => b.toString(16).padStart(2, "0")).join("");
}
