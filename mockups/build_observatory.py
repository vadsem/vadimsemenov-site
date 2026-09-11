#!/usr/bin/env python3
"""Build the Observatory site: index (About + Research), publications, visualizations.

    python3 mockups/build_observatory.py
    python3 -m http.server 8765 --bind 127.0.0.1   # from the site root
"""
import os
import re
import content as C

# Preview-only navigation bar. Set MOCKBAR=0 to build the production pages without it.
MOCKBAR = os.environ.get("MOCKBAR", "1") != "0"

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("OUT_DIR") or os.path.join(HERE, "observatory")

_P = os.environ.get("ASSET_PREFIX", "../")
IMG = _P + "assets/img/"
ICON = _P + "assets/icon/"
VID = _P + "assets/video/"
MOV = os.environ.get("MOVIE_PREFIX", "../../movies/")
OUT_DIR = os.environ.get("OUT_DIR", "")

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?'
         'family=Inter:wght@200;300;400;500&display=swap" rel="stylesheet">')

CSS = """
:root{--bg:#07090d;--fg:#e8edf4;--mut:#8c98aa;--dim:#c3ccda;--line:#1c242f;--acc:#63d3ff}
body{background:var(--bg);color:var(--fg);font:300 17px/1.75 Inter,system-ui,sans-serif;
 -webkit-font-smoothing:antialiased}
a{color:var(--acc);text-decoration:none}
a:hover{color:#9ee4ff}

/* ---- hero (index only) ---- */
.hero{position:relative;height:min(88vh,860px);display:grid;place-items:center;overflow:hidden}
.hero img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.55}
.hero::after{content:"";position:absolute;inset:0;background:
 radial-gradient(ellipse 70% 55% at 50% 46%,rgba(7,9,13,.72) 0%,rgba(7,9,13,.3) 60%,transparent 85%),
 linear-gradient(to bottom,rgba(7,9,13,.5) 0%,transparent 30%,rgba(7,9,13,.6) 78%,var(--bg) 100%)}
.hero .inner{position:relative;z-index:2;text-align:center;padding:0 24px}
.hero h1{font-size:clamp(2.6rem,7vw,5.2rem);font-weight:200;letter-spacing:-.03em;line-height:1}
.hero .sub{margin-top:1.1rem;color:#e3ebf5;font-size:clamp(.95rem,1.6vw,1.15rem)}
.hero .aff{margin-top:.35rem;color:#a8b6c8;font-size:.9rem;letter-spacing:.06em;
 text-transform:uppercase}

/* ---- compact masthead (subpages) ---- */
.mast{padding:4.5rem 24px 2.5rem;text-align:center}
.mast h1{font-size:clamp(2rem,4.5vw,3rem);font-weight:200;letter-spacing:-.03em;line-height:1}
.mast h1 a{color:inherit;text-decoration:none}
.mast .aff{margin-top:.6rem;color:var(--mut);font-size:.8rem;letter-spacing:.16em;
 text-transform:uppercase}

nav.top{position:sticky;top:0;z-index:50;display:flex;gap:2rem;justify-content:center;
 flex-wrap:wrap;padding:1rem;background:rgba(7,9,13,.72);backdrop-filter:blur(14px);
 border-bottom:1px solid var(--line);font-size:.8rem;letter-spacing:.13em;text-transform:uppercase}
nav.top a{color:var(--mut);text-decoration:none}
nav.top a:hover{color:var(--fg)}
nav.top a.on{color:var(--acc)}

.wrap{max-width:680px;margin:0 auto;padding:0 24px}
.wrap-lg{max-width:900px;margin:0 auto;padding:0 24px}
.wide{max-width:1180px;margin:0 auto;padding:0 24px}
section{padding:6rem 0}
section+section{padding-top:0}
h2{font-size:.78rem;letter-spacing:.2em;text-transform:uppercase;color:var(--acc);
 font-weight:500;margin-bottom:2.5rem}
h3{font-size:1.3rem;font-weight:400;letter-spacing:-.01em;margin-bottom:.7rem;line-height:1.3}
p{margin-bottom:1.2rem;color:var(--dim)}

/* ---- about ---- */
.about{display:grid;grid-template-columns:1fr 240px;gap:3.5rem;align-items:start}
.about .portrait{width:100%;border-radius:3px;display:block}
.about .card{position:static}
.about .card .contact{margin-top:1.1rem;font-size:.88rem;color:var(--mut);line-height:1.6}
.about .card .contact a{display:block;word-break:break-all}
.tags{display:flex;flex-wrap:wrap;gap:.5rem;list-style:none;margin-top:2rem}
.cv{display:grid;grid-template-columns:1fr 1fr;gap:3rem;margin-top:3rem;padding-top:2rem;
 border-top:1px solid var(--line)}
.cv h4{font-size:.7rem;letter-spacing:.18em;text-transform:uppercase;color:var(--acc);
 font-weight:500;margin-bottom:1.1rem}
.cv ul{list-style:none}
.cv .org{padding:.7rem 0;border-bottom:1px solid rgba(28,36,47,.55)}
.cv .org:last-child{border-bottom:0}
.cv .o{display:block;font-size:.95rem;color:var(--fg)}
.cv .org li{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:1rem;align-items:baseline;
 margin-top:.3rem}
.cv .r{font-size:.85rem;color:var(--mut)}
.cv .y{font-size:.8rem;color:#6f7a8a;white-space:nowrap}
.tags li{border:1px solid var(--line);border-radius:100px;padding:.35rem .9rem;font-size:.82rem;
 color:var(--mut)}

/* ---- research ---- */
.rs{scroll-margin-top:5.5rem;display:grid;grid-template-columns:150px minmax(0,1fr);gap:2.2rem;
 margin-bottom:3.5rem;align-items:start}
.rs>div{max-width:64ch}
.rs .mini{width:150px;height:150px;object-fit:cover;border-radius:50%;background:#0d1117;
 display:block}
.rs:last-child{margin-bottom:0}
.rs .kicker{font-size:.68rem;letter-spacing:.2em;text-transform:uppercase;color:var(--acc);
 display:block;margin-bottom:.5rem}
.rs .rsfig{margin:1.6rem 0 1.4rem}
.rs .rsfig video{width:100%;height:auto;display:block;background:#000;border-radius:10px}
.rs .rsfig.paper video{background:#fff;padding:10px;border-radius:10px}
.rs .rsfig figcaption{margin-top:.6rem;font-size:.82rem;color:var(--mut)}
.refs{list-style:none;margin-top:1.3rem;padding-top:1rem;border-top:1px solid var(--line)}
.refs li{font-size:.84rem;line-height:1.6;color:#7d879a;margin-bottom:.35rem}
.refs .ti{color:#93a0b3}
.refs a{color:#6f9db4}
.refs a:hover{color:var(--acc)}
.refs .sep{opacity:.45;margin:0 .25rem}
.refs .lnks{white-space:nowrap}
.refs li{padding-left:1.4em;text-indent:-1.4em}

/* ---- figures ---- */
.figs{display:grid;gap:4rem}
.fig video{width:100%;height:auto;display:block;background:#000;border-radius:10px}
.fig.paper video{background:#fff;padding:14px;border-radius:10px}
figcaption{margin-top:.9rem;font-size:.9rem;color:var(--mut)}
.figlinks{display:block;margin-top:.35rem;font-size:.84rem}
.figlinks a{color:#6f9db4}
.figlinks a:hover{color:var(--acc)}
.figlinks .sep{opacity:.45;margin:0 .45rem}

/* ---- publications ---- */
.stats{font-size:.9rem;color:var(--mut);margin-bottom:.9rem;line-height:1.8}
.stats b{font-weight:400;color:var(--dim)}
.stats a{color:var(--dim)}
.stats a:hover{color:var(--acc)}
.stats .sep{opacity:.4;margin:0 .5rem}
.stats .note{opacity:.75}
.links{margin-bottom:3rem;font-size:.9rem;display:flex;gap:1.6rem;flex-wrap:wrap;
 padding-top:1.2rem;border-top:1px solid var(--line)}
.pubs{list-style:none;margin-bottom:3.5rem}
.pubgroup{font-size:1.5rem;letter-spacing:-.005em;text-transform:none;color:var(--acc);
 font-weight:400;margin-bottom:1.7rem;padding-bottom:.8rem;
 border-bottom:1px solid var(--line)}
.pubs li{padding:1.1rem 0;border-bottom:1px solid var(--line)}
.pubs .meta{font-size:.8rem;color:var(--mut);margin-bottom:.25rem}
.pubs .meta .lnks{margin-left:.75rem}
.pubs .meta a{color:#7fb4cc}
.pubs .meta a:hover{color:var(--acc)}
.pubs .sep{opacity:.45;margin:0 .4rem}
.pubs .ti{font-size:1.02rem;line-height:1.45;max-width:74ch}

footer{padding:4rem 24px;text-align:center;color:var(--mut);font-size:.85rem;
 border-top:1px solid var(--line)}

@media(max-width:820px){.about{grid-template-columns:1fr}.cv{grid-template-columns:1fr;gap:2rem}
 .about .card{position:static;max-width:260px}}
@media(max-width:640px){
 .rs{grid-template-columns:1fr;gap:1.2rem}
 .rs .mini{width:96px;height:96px}
 section{padding:3rem 0}
 .mast{padding:2.75rem 24px 1.75rem}
 footer{padding:2.25rem 24px}
 .hero .aff{font-size:.62rem;letter-spacing:.02em}
 .mast .aff{font-size:.6rem;letter-spacing:.02em}
 /* nav and profile links wrap to two rows here; 2rem gap applied to rows too */
 nav.top{gap:.5rem 1.6rem;padding:.85rem 1rem}
 .links{gap:.5rem 1.6rem;padding-top:.9rem;margin-bottom:2rem}
 /* keep each metric and each journal ref whole */
 .stats .item,.pubs .meta .nb{white-space:nowrap}
 .stats .note{display:block;margin-top:.2rem;opacity:.85}
 .stats .note>.sep{display:none}
 /* research refs: link cluster drops below the title */
 .refs .lnks{display:block;margin-top:.15rem;white-space:normal}
 .refs .lnks>.sep:first-child{display:none}
 /* publications: authors / links / title on three lines, tightened */
 .pubs .meta .lnks{display:block;margin-left:0;margin-top:.15rem;white-space:normal}
 .pubgroup{line-height:1.25;margin-bottom:1rem;padding-bottom:.6rem}
 .pubs{margin-bottom:3rem}
 .pubs li{padding:.85rem 0}
 .pubs .meta{line-height:1.5}
 .pubs .meta,.pubs .ti{text-wrap:pretty}
}
"""

PAGES = [("index.html", "About"), ("publications.html", "Publications"),
         ("visualizations.html", "Visualizations")]


def _v(url):
    """Append a content version so an edited asset is never served from cache."""
    rel = url.split("?")[0]
    if rel.startswith("../../"):
        path = os.path.join(os.path.dirname(HERE), rel[6:])
    elif rel.startswith("../"):
        path = os.path.join(HERE, rel[3:])
    elif rel.startswith("movies/"):
        path = os.path.join(os.path.dirname(HERE), rel)
    else:
        path = os.path.join(HERE, rel)
    try:
        return "%s?v=%d" % (url, int(os.path.getmtime(path)))
    except OSError:
        return url


def nav(active):
    out = ""
    for label, href in C.NAV:
        cls = ' class="on"' if label == active else ""
        external = href.startswith("http") or href.endswith(".pdf")
        ext = ' target="_blank" rel="noopener"' if external else ""
        out += '<a href="%s"%s%s>%s</a>' % (href, cls, ext, label)
    return '<nav class="top">%s</nav>' % out


def mockbar(active):
    if not MOCKBAR:
        return ""
    links = "".join('<a href="%s"%s>%s</a>' % (h, ' class="on"' if n == active else "", n)
                    for h, n in PAGES)
    return ('<div class="mockbar"><span class="mocklabel">Observatory</span>%s'
            '<a class="mockhome" href="../">themes</a></div>' % links)


def page(fname, title, active, body):
    return ("""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s &mdash; %s</title>
<link rel="icon" type="image/png" sizes="32x32" href="%s">
<link rel="apple-touch-icon" sizes="180x180" href="%s">%s
<link rel="stylesheet" href="%s">
<style>%s</style></head><body>%s%s
<footer>%s &middot; <a href="mailto:%s">%s</a></footer>
<script src="%s"></script></body></html>"""
            % (C.NAME, title, _v(IMG + "favicon-32.png"),
               _v(IMG + "favicon-180.png"), FONTS, _v(_P + "assets/reset.css"), CSS,
               mockbar(active), body, C.AFFIL, C.EMAIL, C.EMAIL,
               _v(_P + "assets/mock.js")))


def masthead():
    return ('<header class="mast"><h1><a href="index.html">%s</a></h1>'
            '<div class="aff">%s</div></header>' % (C.NAME, C.AFFIL))


def video(slug, title, tone):
    w, h = C.DIMS[slug]
    meta = C.MOVIE_LINKS.get(slug, {})
    sep = '<span class="sep">&middot;</span>'
    bits = []
    for ptitle, arx in meta.get("papers", []):
        bits.append('<a href="https://arxiv.org/abs/%s" target="_blank" rel="noopener">%s</a>'
                    % (arx, ptitle))
    if meta.get("section"):
        bits.append('<a href="index.html#%s">Read more</a>' % meta["section"])
    links = ('<span class="figlinks">%s</span>' % sep.join(bits)) if bits else ""
    return ('<figure class="fig %s">'
            '<video width="%d" height="%d" preload="none" playsinline muted loop controls '
            'poster="%s"><source src="%s" type="video/mp4"></video>'
            '<figcaption>%s%s</figcaption></figure>'
            % (tone, w, h, _v("%s%s.poster.jpg" % (VID, slug)),
               _v("%s%s.mp4" % (MOV, slug)), title, links))


def cv_list(groups):
    out = ""
    for org, roles in groups:
        items = "".join('<li><span class="r">%s</span><span class="y">%s</span></li>' % (r, y)
                        for r, y in roles)
        out += '<div class="org"><span class="o">%s</span><ul>%s</ul></div>' % (org, items)
    return out


def cv_block():
    return ('<div class="cv">'
            '<div><h4>Positions</h4>%s</div>'
            '<div><h4>Education</h4>%s</div></div>'
            % (cv_list(C.POSITIONS), cv_list(C.EDUCATION)))


def refs_line(papers):
    """Faint reference list: Author et al. Year . Title . arXiv . ADS . Journal"""
    if not papers:
        return ""
    out = ""
    for authors, year, title, arx in papers:
        r = C.REFS.get(arx, {})
        bits = []
        if arx:
            bits.append('<a href="https://arxiv.org/abs/%s" target="_blank" '
                        'rel="noopener">arXiv</a>' % arx)
        if r.get("ads"):
            bits.append('<a href="https://ui.adsabs.harvard.edu/abs/%s/abstract" '
                        'target="_blank" rel="noopener">ADS</a>' % r["ads"])
        if r.get("url"):
            bits.append('<a href="%s" target="_blank" '
                        'rel="noopener">Journal</a>' % r["url"])
        sep = '<span class="sep">&middot;</span>'
        links = ('<span class="lnks">%s%s</span>' % (sep, sep.join(bits))) if bits else ""
        out += ('<li>%s %s%s<span class="ti">%s</span>%s</li>'
                % (authors, year, sep, title, links))
    return '<ul class="refs">%s</ul>' % out


def research_block(r):
    kicker = ('<span class="kicker">%s</span>' % r["kicker"]) if r.get("kicker") else ""
    fig = ""
    if r.get("video"):
        slug = r["video"]
        title = next((t for sl, t, _ in C.MOVIES if sl == slug), "")
        tone = next((tn for sl, _, tn in C.MOVIES if sl == slug), "dark")
        w, h = C.DIMS[slug]
        fig = ('<figure class="rsfig %s">'
               '<video width="%d" height="%d" preload="none" playsinline muted loop controls '
               'poster="%s"><source src="%s" type="video/mp4"></video>'
               '<figcaption>%s</figcaption></figure>'
               % (tone, w, h, _v("%s%s.poster.jpg" % (VID, slug)),
                  _v("%s%s.mp4" % (MOV, slug)), title))
    return ('<div class="rs" id="%s"><img class="mini" src="%s" alt="">'
            '<div>%s<h3>%s</h3><p>%s</p>%s%s</div></div>'
            % (r.get("id", ""), _v(ICON + r["icon"]), kicker, r["title"], r["text"], fig,
               refs_line(r["papers"])))


# ------------------------------------------------------------------- index.html

def build_index():
    bio = "".join("<p>%s</p>" % p for p in C.BIO)
    tags = "".join("<li>%s</li>" % i for i in C.INTERESTS)

    rs = "".join(research_block(r) for r in C.RESEARCH)

    body = """
<header class="hero"><img src="%(hero)s" alt="Simulation of interstellar turbulence">
 <div class="inner"><h1>%(name)s</h1><div class="sub">%(tag)s</div>
 <div class="aff">%(aff)s</div></div></header>
%(nav)s
<section id="about"><div class="wrap-lg"><h2>About</h2>
 <div class="about"><div>%(bio)s<ul class="tags">%(tags)s</ul></div>
 <div class="card"><img class="portrait" src="%(portrait)s" alt="%(name)s">
  <div class="contact"><a href="mailto:%(email)s">%(email)s</a></div></div>
 </div>%(cv)s</div></section>
<section id="research"><div class="wrap-lg"><h2>Research</h2>%(rs)s</div></section>
""" % dict(hero=_v(IMG + C.HERO), name=C.NAME, tag=C.TAGLINE, aff=C.AFFIL,
           nav=nav("About"), bio=bio, tags=tags, email=C.EMAIL,
           portrait=_v(IMG + "portrait.jpg"), cv=cv_block(), rs=rs)
    return page("index.html", "Computational astrophysicist", "About", body)


# ------------------------------------------------------------ publications.html

def build_publications():
    sep = ' <span class="sep">&middot;</span> '
    bits = []
    for n, l in C.STATS:
        url = C.STAT_LINKS.get(l)
        body = "<b>%s</b> %s" % (n, l)
        inner = ('<a href="%s" target="_blank" rel="noopener">%s</a>' % (url, body)
                 if url else body)
        bits.append('<span class="item">%s</span>' % inner)
    stats = ('<p class="stats">%s<span class="note">%s(%s)</span></p>'
             % (sep.join(bits), sep, C.STATS_NOTE % C.ADS_LIBRARY))
    links = "".join('<a href="%s" target="_blank" rel="noopener">%s</a>' % (u, t)
                    for t, u in C.LINKS)

    groups = ""
    for heading, items in C.PUBS:
        lis = ""
        for authors, journal, arx, title in items:
            r = C.REFS.get(arx, {})
            # journal, arXiv and ADS form one link cluster: on mobile it drops to its
            # own line under the authors; on desktop it stays inline beside them.
            ref_links = ['<span class="nb">%s</span>'
                         % (('<a href="%s" target="_blank" rel="noopener">%s</a>'
                             % (r["url"], journal)) if r.get("url") else journal)]
            if re.match(r"^\d{4}\.\d{4,5}$", arx or ""):
                ref_links.append('<span class="nb"><a href="https://arxiv.org/abs/%s" '
                                 'target="_blank" rel="noopener">arXiv:%s</a></span>' % (arx, arx))
            if r.get("ads"):
                ref_links.append('<span class="nb"><a href="https://ui.adsabs.harvard.edu/abs/%s'
                                 '/abstract" target="_blank" rel="noopener">ADS</a></span>' % r["ads"])
            cluster = ('<span class="lnks">%s</span>'
                       % ' <span class="sep">&middot;</span> '.join(ref_links))
            lis += ('<li><div class="meta"><span class="au">%s</span>%s</div>'
                    '<div class="ti">%s</div></li>' % (authors, cluster, title))
        groups += ('<h2 class="pubgroup">%s:</h2><ul class="pubs">%s</ul>'
                   % (heading, lis))

    body = """%(mast)s%(nav)s
<section><div class="wrap-lg">
 %(stats)s
 <div class="links">%(links)s</div>
 %(groups)s
</div></section>""" % dict(mast=masthead(), nav=nav("Publications"),
                           stats=stats, links=links, groups=groups)
    return page("publications.html", "Publications", "Publications", body)


# ---------------------------------------------------------- visualizations.html

def build_visualizations():
    figs = "".join(video(s, t, tone) for s, t, tone in C.MOVIES)
    body = """%(mast)s%(nav)s
<section><div class="wrap-lg"><h2>Visualizations</h2>
 <p>Some simulations and visualizations produced during my work. Each video can be downloaded
 in full quality from its own controls menu, and the corresponding papers are linked from the
 captions.</p>
</div><div class="wrap-lg" style="margin-top:3.5rem"><div class="figs">%(figs)s</div></div>
</section>""" % dict(mast=masthead(), nav=nav("Visualizations"), figs=figs)
    return page("visualizations.html", "Visualizations", "Visualizations", body)


def main():
    os.makedirs(OUT, exist_ok=True)
    for fname, builder in [("index.html", build_index),
                           ("publications.html", build_publications),
                           ("visualizations.html", build_visualizations)]:
        with open(os.path.join(OUT, fname), "w") as f:
            f.write(builder())
        print("built observatory/" + fname)


if __name__ == "__main__":
    main()
