#!/usr/bin/env python3
"""Build the five theme mockups for vadimsemenov.com from shared content.

    python3 mockups/build.py && python3 -m http.server 8000 --directory mockups
"""
import os
import shutil
import content as C

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

THEMES = [
    ("observatory", "Observatory", "Dark &middot; cyan &middot; full-bleed hero"),
    ("journal", "Journal", "Light &middot; editorial &middot; gold accent"),
    ("grid", "Grid", "Light &middot; Swiss &middot; modular gallery"),
    ("atlas", "Atlas", "Dark &middot; gold &middot; fixed left rail"),
    ("split", "Split", "Asymmetric hero &middot; light interior"),
]

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500;600&'
         'family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;0,6..72,500;1,6..72,300&'
         'family=Fraunces:opsz,wght@9..144,300;9..144,500&'
         'family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">')

IMG = "../assets/img/"
VID = "../assets/video/"
MOV = "../../movies/"


def switcher(active):
    links = "".join(
        '<a href="../%s/"%s>%s</a>' % (s, ' class="on"' if s == active else "", n)
        for s, n, _ in THEMES)
    return ('<div class="mockbar"><span class="mocklabel">Mockup</span>%s'
            '<a class="mockhome" href="../">all five</a></div>' % links)


def nav_html():
    return "".join('<a href="%s">%s</a>' % (h, t) for t, h in C.NAV)


def bio_html():
    return "".join("<p>%s</p>" % p for p in C.BIO)


def interests_html(tag="li"):
    return "".join("<%s>%s</%s>" % (tag, i, tag) for i in C.INTERESTS)


def stats_html():
    return "".join('<div class="stat"><b>%s</b><span>%s</span></div>' % (n, l)
                   for n, l in C.STATS)


def video(slug, title, tone, cls=""):
    """A single figure. `tone` is 'paper' for white-background paper figures."""
    w, h = C.DIMS[slug]
    return ('<figure class="fig %s %s">'
            '<video width="%d" height="%d" preload="none" playsinline muted loop controls '
            'poster="%s%s.poster.jpg">'
            '<source src="%s%s.mp4" type="video/mp4"></video>'
            '<figcaption>%s</figcaption></figure>'
            % (tone, cls, w, h, VID, slug, MOV, slug, title))


def videos_html(cls="", limit=None):
    items = C.MOVIES[:limit] if limit else C.MOVIES
    return "".join(video(s, t, tone, cls) for s, t, tone in items)


def research_html(fmt):
    return "".join(fmt(i, r) for i, r in enumerate(C.RESEARCH, 1))


def pubs_html():
    return "".join(
        '<li><span class="au">%s</span><span class="jr">%s</span>'
        '<span class="ti">%s</span></li>' % (a, j, t) for a, j, t in C.PUBS)


def page(slug, title, css, body):
    return ("""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s &mdash; %s</title>%s
<link rel="stylesheet" href="../assets/reset.css">
<style>%s</style></head><body class="t-%s">%s%s
<script src="../assets/mock.js"></script></body></html>"""
            % (C.NAME, title, FONTS, css, slug, switcher(slug), body))


# ---------------------------------------------------------------- 1. OBSERVATORY

OBSERVATORY_CSS = """
:root{--bg:#07090d;--panel:#0d1117;--fg:#e8edf4;--mut:#8c98aa;--line:#1c242f;--acc:#63d3ff}
body{background:var(--bg);color:var(--fg);font:300 17px/1.75 Inter,system-ui,sans-serif;
 -webkit-font-smoothing:antialiased}
a{color:var(--acc)}
.hero{position:relative;height:min(88vh,860px);display:grid;place-items:center;overflow:hidden}
.hero img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.55}
.hero::after{content:"";position:absolute;inset:0;background:
 radial-gradient(ellipse 70% 55% at 50% 46%,rgba(7,9,13,.72) 0%,rgba(7,9,13,.3) 60%,transparent 85%),
 linear-gradient(to bottom,rgba(7,9,13,.5) 0%,transparent 30%,rgba(7,9,13,.6) 78%,var(--bg) 100%)}
.hero .inner{position:relative;z-index:2;text-align:center;padding:0 24px}
.hero h1{font-size:clamp(2.6rem,7vw,5.2rem);font-weight:200;letter-spacing:-.03em;line-height:1}
.hero .sub{margin-top:1.1rem;color:#e3ebf5;font-size:clamp(.95rem,1.6vw,1.15rem);font-weight:300}
.hero .aff{margin-top:.35rem;color:#a8b6c8;font-size:.9rem;letter-spacing:.06em;
 text-transform:uppercase}
nav.top{position:sticky;top:0;z-index:50;display:flex;gap:2rem;justify-content:center;
 padding:1rem;background:rgba(7,9,13,.72);backdrop-filter:blur(14px);
 border-bottom:1px solid var(--line);font-size:.8rem;letter-spacing:.13em;text-transform:uppercase}
nav.top a{color:var(--mut);text-decoration:none}
nav.top a:hover{color:var(--fg)}
.wrap{max-width:680px;margin:0 auto;padding:0 24px}
section{padding:6rem 0}
h2{font-size:.78rem;letter-spacing:.2em;text-transform:uppercase;color:var(--acc);
 font-weight:500;margin-bottom:2.5rem}
h3{font-size:1.35rem;font-weight:400;letter-spacing:-.01em;margin-bottom:.7rem}
p{margin-bottom:1.2rem;color:#c3ccda}
.tags{display:flex;flex-wrap:wrap;gap:.5rem;list-style:none;margin-top:2rem}
.tags li{border:1px solid var(--line);border-radius:100px;padding:.35rem .9rem;font-size:.82rem;
 color:var(--mut)}
.stats{display:flex;flex-wrap:wrap;gap:2.5rem;margin-top:3rem;padding-top:2rem;
 border-top:1px solid var(--line)}
.stat b{display:block;font-size:1.9rem;font-weight:200;letter-spacing:-.02em}
.stat span{font-size:.75rem;letter-spacing:.14em;text-transform:uppercase;color:var(--mut)}
.rs{display:grid;grid-template-columns:132px 1fr;gap:2rem;margin-bottom:3rem;align-items:start}
.rs:last-child{margin-bottom:0}
.rs img{width:132px;height:132px;object-fit:cover;border-radius:2px}
.figs{max-width:1180px;margin:0 auto;padding:0 24px;display:grid;gap:4rem}
.fig video{width:100%;height:auto;display:block;background:#000}
.fig.paper video{background:#fff;padding:14px;border-radius:3px}
figcaption{margin-top:.9rem;font-size:.9rem;color:var(--mut)}
.pubs{list-style:none}
.pubs li{padding:1.1rem 0;border-bottom:1px solid var(--line)}
.pubs .au{display:block;font-size:.8rem;color:var(--mut)}
.pubs .jr{display:block;font-size:.8rem;color:var(--acc);margin-bottom:.3rem}
.pubs .ti{font-size:1.02rem}
footer{padding:5rem 24px;text-align:center;color:var(--mut);font-size:.85rem;
 border-top:1px solid var(--line)}
@media(max-width:640px){.rs{grid-template-columns:1fr}.rs img{width:100%;height:200px}}
"""


def build_observatory():
    rs = research_html(lambda i, r: (
        '<div class="rs"><img src="%s%s" alt=""><div><h3>%s</h3><p>%s</p></div></div>'
        % (IMG, r["render"], r["title"], r["text"])))
    body = """
<header class="hero"><img src="%(img)s%(hero)s" alt="Simulation of interstellar turbulence">
 <div class="inner"><h1>%(name)s</h1>
 <div class="sub">%(tag)s</div><div class="aff">%(aff)s</div></div></header>
<nav class="top">%(nav)s</nav>
<section id="about"><div class="wrap"><h2>About</h2>%(bio)s
 <ul class="tags">%(int)s</ul><div class="stats">%(stats)s</div></div></section>
<section id="research"><div class="wrap"><h2>Research</h2>%(rs)s</div></section>
<section id="visualizations"><div class="wrap"><h2>Visualizations</h2></div>
 <div class="figs">%(vids)s</div></section>
<section id="publications"><div class="wrap"><h2>Selected publications</h2>
 <ul class="pubs">%(pubs)s</ul></div></section>
<footer>%(email)s</footer>""" % dict(
        img=IMG, hero=C.HERO, name=C.NAME, tag=C.TAGLINE, aff=C.AFFIL,
        nav=nav_html(), bio=bio_html(), int=interests_html(), stats=stats_html(),
        rs=rs, vids=videos_html(limit=5), pubs=pubs_html(), email=C.EMAIL)
    return page("observatory", "Observatory", OBSERVATORY_CSS, body)


# -------------------------------------------------------------------- 2. JOURNAL

JOURNAL_CSS = """
:root{--bg:#fbfaf7;--fg:#1b1a16;--mut:#6f6a5e;--line:#e0dcd2;--acc:#a8701a}
body{background:var(--bg);color:var(--fg);font:400 17px/1.72 Inter,system-ui,sans-serif}
a{color:var(--acc)}
.masthead{max-width:900px;margin:0 auto;padding:6rem 32px 2.5rem;text-align:center}
.masthead h1{font:300 clamp(2.8rem,6.5vw,4.6rem)/1 Newsreader,Georgia,serif;letter-spacing:-.02em}
.masthead .sub{margin-top:1rem;font:italic 300 1.25rem/1.5 Newsreader,Georgia,serif;color:var(--mut)}
.masthead .aff{margin-top:.9rem;font-size:.74rem;letter-spacing:.22em;text-transform:uppercase;
 color:var(--mut)}
.rule{max-width:900px;margin:0 auto;border-top:1px solid var(--fg);height:0}
.rule.thin{border-color:var(--line)}
nav.top{display:flex;gap:2.4rem;justify-content:center;padding:1.1rem;font-size:.72rem;
 letter-spacing:.2em;text-transform:uppercase;border-bottom:1px solid var(--line);
 position:sticky;top:0;background:rgba(251,250,247,.93);backdrop-filter:blur(10px);z-index:50}
nav.top a{color:var(--fg);text-decoration:none;opacity:.65}
nav.top a:hover{opacity:1;color:var(--acc)}
.wrap{max-width:660px;margin:0 auto;padding:0 32px}
section{padding:5.5rem 0}
h2{font:400 .72rem/1 Inter,sans-serif;letter-spacing:.24em;text-transform:uppercase;
 color:var(--acc);margin-bottom:2.4rem;padding-bottom:.9rem;border-bottom:1px solid var(--line)}
h3{font:400 1.5rem/1.3 Newsreader,Georgia,serif;margin-bottom:.6rem}
p{margin-bottom:1.25rem}
.lede p:first-child{font:300 1.22rem/1.65 Newsreader,Georgia,serif}
.tags{columns:2;list-style:none;margin-top:2.2rem;font-size:.95rem;color:var(--mut)}
.tags li{padding:.28rem 0;break-inside:avoid}
.stats{display:flex;flex-wrap:wrap;gap:2.6rem;margin-top:2.6rem;padding-top:1.6rem;
 border-top:1px solid var(--line)}
.stat b{display:block;font:300 2rem/1 Newsreader,Georgia,serif}
.stat span{font-size:.68rem;letter-spacing:.16em;text-transform:uppercase;color:var(--mut)}
.rs{margin-bottom:3.4rem}
.rs .n{font:500 .7rem/1 Inter,sans-serif;letter-spacing:.18em;color:var(--acc);
 text-transform:uppercase;display:block;margin-bottom:.5rem}
.figs{max-width:1080px;margin:0 auto;padding:0 32px;display:grid;gap:4.5rem}
.fig video{width:100%;height:auto;display:block;background:#111}
.fig.paper video{background:#fff;border:1px solid var(--line)}
figcaption{margin-top:.85rem;font-size:.88rem;color:var(--mut);
 padding-top:.7rem;border-top:1px solid var(--line)}
figcaption b{color:var(--acc);font-weight:500;letter-spacing:.1em;font-size:.7rem;
 text-transform:uppercase;margin-right:.6rem}
.pubs{list-style:none}
.pubs li{padding:1.15rem 0;border-bottom:1px solid var(--line)}
.pubs .au{font-size:.82rem;color:var(--mut)}
.pubs .jr{font-size:.82rem;color:var(--acc);margin-left:.6rem}
.pubs .ti{display:block;font:400 1.08rem/1.45 Newsreader,Georgia,serif;margin-top:.25rem}
footer{padding:5rem 32px;text-align:center;color:var(--mut);font-size:.85rem;
 border-top:1px solid var(--fg);max-width:900px;margin:0 auto}
@media(max-width:640px){.tags{columns:1}}
"""


def build_journal():
    rs = research_html(lambda i, r: (
        '<div class="rs"><span class="n">%02d</span><h3>%s</h3><p>%s</p></div>'
        % (i, r["title"], r["text"])))
    figs = "".join(
        '<figure class="fig %s"><video width="%d" height="%d" preload="none" playsinline muted '
        'loop controls poster="%s%s.poster.jpg">'
        '<source src="%s%s.mp4" type="video/mp4"></video>'
        '<figcaption><b>Fig. %d</b>%s</figcaption></figure>'
        % (tone, C.DIMS[s][0], C.DIMS[s][1], VID, s, MOV, s, i, t)
        for i, (s, t, tone) in enumerate(C.MOVIES[:5], 1))
    body = """
<header class="masthead"><h1>%(name)s</h1><div class="sub">%(tag)s</div>
 <div class="aff">%(aff)s</div></header><div class="rule"></div>
<nav class="top">%(nav)s</nav>
<section id="about"><div class="wrap lede"><h2>About</h2>%(bio)s
 <ul class="tags">%(int)s</ul><div class="stats">%(stats)s</div></div></section>
<div class="rule thin"></div>
<section id="research"><div class="wrap"><h2>Research</h2>%(rs)s</div></section>
<div class="rule thin"></div>
<section id="visualizations"><div class="wrap"><h2>Visualizations</h2></div>
 <div class="figs">%(figs)s</div></section>
<div class="rule thin"></div>
<section id="publications"><div class="wrap"><h2>Selected publications</h2>
 <ul class="pubs">%(pubs)s</ul></div></section>
<footer>%(email)s</footer>""" % dict(
        name=C.NAME, tag=C.TAGLINE, aff=C.AFFIL, nav=nav_html(), bio=bio_html(),
        int=interests_html(), stats=stats_html(), rs=rs, figs=figs,
        pubs=pubs_html(), email=C.EMAIL)
    return page("journal", "Journal", JOURNAL_CSS, body)


# ----------------------------------------------------------------------- 3. GRID

GRID_CSS = """
:root{--bg:#f2f2f0;--fg:#0e0e0e;--mut:#6b6b6b;--line:#d6d6d2;--acc:#0a72a0}
body{background:var(--bg);color:var(--fg);font:400 16px/1.6 Inter,system-ui,sans-serif;
 -webkit-font-smoothing:antialiased}
a{color:var(--acc)}
.g{max-width:1280px;margin:0 auto;padding:0 28px;
 display:grid;grid-template-columns:repeat(12,1fr);gap:24px}
.masthead{padding:5rem 0 2rem}
.masthead h1{grid-column:1/9;font-size:clamp(2.4rem,7.2vw,5.8rem);font-weight:500;
 letter-spacing:-.04em;line-height:.94}
.masthead .meta{grid-column:9/13;align-self:end;font-size:.82rem;color:var(--mut)}
.masthead .meta b{display:block;color:var(--fg);font-weight:500;letter-spacing:-.01em;
 font-size:.95rem;margin-bottom:.3rem}
nav.top{position:sticky;top:0;z-index:50;background:var(--bg);
 border-top:1px solid var(--fg);border-bottom:1px solid var(--line)}
nav.top .g{padding-top:.85rem;padding-bottom:.85rem}
nav.top a{grid-column:span 2;font-size:.74rem;letter-spacing:.14em;text-transform:uppercase;
 color:var(--fg);text-decoration:none;opacity:.6}
nav.top a:hover{opacity:1;color:var(--acc)}
section{padding:5rem 0}
h2{grid-column:1/3;font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;
 color:var(--acc);font-weight:500}
.col{grid-column:3/10}
.col p{margin-bottom:1.1rem;font-size:1.06rem;line-height:1.7}
.side{grid-column:10/13;font-size:.85rem;color:var(--mut)}
.tags{list-style:none}
.tags li{padding:.3rem 0;border-bottom:1px solid var(--line)}
.stats{grid-column:3/13;display:grid;grid-template-columns:repeat(5,1fr);gap:24px;
 margin-top:2.5rem;padding-top:1.5rem;border-top:1px solid var(--fg)}
.stat b{display:block;font-size:2.1rem;font-weight:500;letter-spacing:-.04em;line-height:1}
.stat span{font-size:.68rem;letter-spacing:.12em;text-transform:uppercase;color:var(--mut)}
.rs{grid-column:3/13;display:grid;grid-template-columns:repeat(10,1fr);gap:24px;
 padding:2rem 0;border-top:1px solid var(--line)}
.rs img{grid-column:span 2;width:100%;aspect-ratio:1;object-fit:cover}
.rs div{grid-column:span 8}
.rs h3{font-size:1.2rem;font-weight:500;letter-spacing:-.015em;margin-bottom:.4rem}
.rs p{font-size:.95rem;color:#3c3c3c}
.gal{grid-column:1/13;display:grid;grid-template-columns:repeat(12,1fr);gap:24px}
.fig{grid-column:span 6}
.fig.wide{grid-column:span 12}
.fig video{width:100%;height:auto;display:block;background:#111}
.fig.paper video{background:#fff;border:1px solid var(--line)}
figcaption{margin-top:.7rem;font-size:.82rem;color:var(--mut)}
.sq{grid-column:1/13;display:grid;grid-template-columns:repeat(5,1fr);gap:24px;margin-bottom:3rem}
.sq img{width:100%;aspect-ratio:1;object-fit:cover;display:block}
.pubs{grid-column:3/13;list-style:none}
.pubs li{display:grid;grid-template-columns:1fr 3fr;gap:24px;padding:1rem 0;
 border-top:1px solid var(--line)}
.pubs .au{font-size:.8rem;color:var(--mut)}
.pubs .jr{display:block;font-size:.8rem;color:var(--acc)}
.pubs .ti{font-size:1rem;letter-spacing:-.01em}
footer{border-top:1px solid var(--fg);margin-top:3rem}
footer .g{padding-top:3rem;padding-bottom:3rem}
footer a{grid-column:1/6;font-size:.9rem}
@media(max-width:860px){.masthead h1,.masthead .meta,.col,.side,.stats,.rs,.pubs,.gal,.sq,
 .fig,.fig.wide,h2,footer a{grid-column:1/13}.stats,.sq{grid-template-columns:repeat(2,1fr)}
 .rs{grid-template-columns:1fr}.rs img,.rs div{grid-column:1/-1}.rs img{aspect-ratio:16/9}
 nav.top a{grid-column:span 4}.pubs li{grid-template-columns:1fr}}
"""


def build_grid():
    rs = research_html(lambda i, r: (
        '<div class="rs"><img src="%s%s" alt=""><div><h3>%s</h3><p>%s</p></div></div>'
        % (IMG, r["render"], r["title"], r["text"])))
    sq = "".join('<img src="%s%s" alt="%s">' % (IMG, f.replace(".jpg", ".thumb.jpg"), a)
                 for f, _, a in C.RENDERS)
    figs = "".join(video(s, t, tone, "wide" if i % 3 == 0 else "")
                   for i, (s, t, tone) in enumerate(C.MOVIES[:5]))
    body = """
<header class="masthead g"><h1>%(name)s</h1>
 <div class="meta"><b>%(tag)s</b>%(aff)s<br>%(email)s</div></header>
<nav class="top"><div class="g">%(nav)s</div></nav>
<section id="about"><div class="g"><h2>About</h2><div class="col">%(bio)s</div>
 <div class="side"><ul class="tags">%(int)s</ul></div>
 <div class="stats">%(stats)s</div></div></section>
<section id="research"><div class="g"><h2>Research</h2>%(rs)s</div></section>
<section id="visualizations"><div class="g"><div class="sq">%(sq)s</div>
 <h2>Visualizations</h2><div class="gal">%(figs)s</div></div></section>
<section id="publications"><div class="g"><h2>Publications</h2>
 <ul class="pubs">%(pubs)s</ul></div></section>
<footer><div class="g"><a href="mailto:%(email)s">%(email)s</a></div></footer>""" % dict(
        name=C.NAME, tag=C.TAGLINE, aff=C.AFFIL, email=C.EMAIL, nav=nav_html(),
        bio=bio_html(), int=interests_html(), stats=stats_html(), rs=rs, sq=sq,
        figs=figs, pubs=pubs_html())
    return page("grid", "Grid", GRID_CSS, body)


# ---------------------------------------------------------------------- 4. ATLAS

ATLAS_CSS = """
:root{--bg:#0c0a07;--panel:#141009;--fg:#f2ece0;--mut:#968d7c;--line:#262016;--acc:#e9a83c}
body{background:var(--bg);color:var(--fg);font:300 17px/1.75 Inter,system-ui,sans-serif;
 -webkit-font-smoothing:antialiased}
a{color:var(--acc)}
.rail{position:fixed;left:0;top:0;bottom:0;width:290px;padding:3rem 2.2rem;
 border-right:1px solid var(--line);display:flex;flex-direction:column;
 background:var(--bg);z-index:40}
.rail h1{font-size:1.9rem;font-weight:300;letter-spacing:-.025em;line-height:1.1}
.rail .tag{margin-top:.6rem;color:var(--acc);font-size:.9rem}
.rail .aff{margin-top:.3rem;color:var(--mut);font-size:.85rem;line-height:1.5}
.rail nav{margin-top:3rem;display:flex;flex-direction:column;gap:.1rem}
.rail nav a{color:var(--mut);text-decoration:none;font-size:.9rem;padding:.5rem 0;
 border-bottom:1px solid var(--line)}
.rail nav a:hover{color:var(--fg);padding-left:.4rem;transition:padding .15s}
.rail .foot{margin-top:auto;font:400 .78rem/1.6 JetBrains Mono,monospace;color:var(--mut)}
.rail .thumb{margin-top:2rem;width:100%;aspect-ratio:1;object-fit:cover;opacity:.8}
main{margin-left:290px}
section{padding:5.5rem 4rem;border-bottom:1px solid var(--line);max-width:1100px}
h2{font:400 .74rem/1 JetBrains Mono,monospace;letter-spacing:.2em;text-transform:uppercase;
 color:var(--acc);margin-bottom:2.4rem}
h3{font-size:1.3rem;font-weight:400;letter-spacing:-.01em;margin-bottom:.6rem}
p{margin-bottom:1.2rem;color:#cdc4b6;max-width:62ch}
.tags{display:flex;flex-wrap:wrap;gap:.45rem;list-style:none;margin-top:2rem}
.tags li{border:1px solid var(--line);padding:.3rem .8rem;font-size:.8rem;color:var(--mut)}
.stats{display:flex;flex-wrap:wrap;gap:3rem;margin-top:2.8rem;padding-top:1.8rem;
 border-top:1px solid var(--line)}
.stat b{display:block;font-size:2rem;font-weight:200;letter-spacing:-.03em;color:var(--acc)}
.stat span{font:400 .68rem/1 JetBrains Mono,monospace;letter-spacing:.12em;
 text-transform:uppercase;color:var(--mut)}
.rs{padding:1.8rem 0;border-top:1px solid var(--line);display:grid;
 grid-template-columns:1fr 96px;gap:2rem;align-items:start}
.rs img{width:96px;height:96px;object-fit:cover;grid-column:2}
.rs>div{grid-column:1;grid-row:1}
.figs{display:grid;gap:3.5rem}
.fig video{width:100%;height:auto;display:block;background:#000}
.fig.paper video{background:#fff;padding:12px}
figcaption{margin-top:.8rem;font-size:.88rem;color:var(--mut)}
.pubs{list-style:none}
.pubs li{padding:1rem 0;border-top:1px solid var(--line)}
.pubs .au{font:400 .78rem/1.5 JetBrains Mono,monospace;color:var(--mut)}
.pubs .jr{font:400 .78rem/1.5 JetBrains Mono,monospace;color:var(--acc);margin-left:.6rem}
.pubs .ti{display:block;margin-top:.2rem}
@media(max-width:900px){.rail{position:static;width:auto;border-right:0;
 border-bottom:1px solid var(--line)}.rail .thumb{display:none}main{margin-left:0}
 section{padding:3.5rem 1.5rem}}
"""


def build_atlas():
    rs = research_html(lambda i, r: (
        '<div class="rs"><div><h3>%s</h3><p>%s</p></div><img src="%s%s" alt=""></div>'
        % (r["title"], r["text"], IMG, r["render"])))
    body = """
<aside class="rail"><h1>%(name)s</h1><div class="tag">%(tag)s</div>
 <div class="aff">%(aff)s</div><nav>%(nav)s</nav>
 <img class="thumb" src="%(img)s%(hero)s" alt="">
 <div class="foot">%(email)s</div></aside>
<main>
<section id="about"><h2>About</h2>%(bio)s<ul class="tags">%(int)s</ul>
 <div class="stats">%(stats)s</div></section>
<section id="research"><h2>Research</h2>%(rs)s</section>
<section id="visualizations"><h2>Visualizations</h2><div class="figs">%(vids)s</div></section>
<section id="publications"><h2>Selected publications</h2>
 <ul class="pubs">%(pubs)s</ul></section>
</main>""" % dict(
        name=C.NAME, tag=C.TAGLINE, aff=C.AFFIL, nav=nav_html(), img=IMG,
        hero=C.HERO_WARM, email=C.EMAIL, bio=bio_html(), int=interests_html(),
        stats=stats_html(), rs=rs, vids=videos_html(limit=5), pubs=pubs_html())
    return page("atlas", "Atlas", ATLAS_CSS, body)


# ---------------------------------------------------------------------- 5. SPLIT

SPLIT_CSS = """
:root{--bg:#ffffff;--fg:#141414;--mut:#6e6e6e;--line:#e6e6e6;--dark:#0a0d12;--acc:#1d7fa8}
body{background:var(--bg);color:var(--fg);font:400 17px/1.7 Inter,system-ui,sans-serif;
 -webkit-font-smoothing:antialiased}
a{color:var(--acc)}
.split{display:grid;grid-template-columns:1fr 1fr;min-height:100vh}
.split .art{position:relative;background:var(--dark);overflow:hidden}
.split .art img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.split .art::after{content:"";position:absolute;left:0;right:0;bottom:0;height:40%;
 background:linear-gradient(to top,rgba(6,10,16,.75),transparent);z-index:1}
.split .art figcaption{position:absolute;left:24px;bottom:22px;color:rgba(255,255,255,.9);
 font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;z-index:2}
.split .say{display:flex;flex-direction:column;justify-content:center;padding:4rem 3.5rem}
.split h1{font:300 clamp(2.6rem,5.2vw,4.4rem)/1 Fraunces,Georgia,serif;letter-spacing:-.03em}
.split .tag{margin-top:1.2rem;font-size:1.15rem;color:var(--mut)}
.split .aff{margin-top:.5rem;font-size:.75rem;letter-spacing:.2em;text-transform:uppercase;
 color:var(--mut)}
.split .lede{margin-top:2.2rem;max-width:46ch;color:#3a3a3a}
.split .cta{margin-top:2.4rem;display:flex;gap:1.6rem;font-size:.8rem;letter-spacing:.14em;
 text-transform:uppercase}
nav.top{position:sticky;top:0;z-index:50;display:flex;gap:2.2rem;justify-content:center;
 padding:1.1rem;background:rgba(255,255,255,.93);backdrop-filter:blur(10px);
 border-bottom:1px solid var(--line);font-size:.74rem;letter-spacing:.16em;
 text-transform:uppercase}
nav.top a{color:var(--fg);text-decoration:none;opacity:.6}
nav.top a:hover{opacity:1;color:var(--acc)}
.wrap{max-width:700px;margin:0 auto;padding:0 32px}
section{padding:6rem 0}
h2{font-size:.72rem;letter-spacing:.22em;text-transform:uppercase;color:var(--acc);
 font-weight:500;margin-bottom:2.4rem}
h3{font:400 1.45rem/1.3 Fraunces,Georgia,serif;margin-bottom:.55rem}
p{margin-bottom:1.15rem}
.tags{display:flex;flex-wrap:wrap;gap:.5rem;list-style:none;margin-top:2rem}
.tags li{background:#f4f4f4;border-radius:3px;padding:.32rem .8rem;font-size:.83rem;
 color:var(--mut)}
.stats{display:flex;flex-wrap:wrap;gap:2.8rem;margin-top:2.8rem;padding-top:1.8rem;
 border-top:1px solid var(--line)}
.stat b{display:block;font:300 2rem/1 Fraunces,Georgia,serif}
.stat span{font-size:.68rem;letter-spacing:.14em;text-transform:uppercase;color:var(--mut)}
.rs{padding:2rem 0;border-top:1px solid var(--line)}
.band{background:var(--dark);padding:6rem 0;margin:0}
.band h2{color:#7fd0ee}
.band .wrap{color:#d6dde6}
.figs{max-width:1120px;margin:0 auto;padding:0 32px;display:grid;gap:4rem}
.fig video{width:100%;height:auto;display:block;background:#000}
.fig.paper video{background:#fff;padding:12px;border-radius:2px}
.band figcaption{margin-top:.8rem;font-size:.88rem;color:#93a0b0}
.pubs{list-style:none}
.pubs li{padding:1.1rem 0;border-top:1px solid var(--line)}
.pubs .au{font-size:.8rem;color:var(--mut)}
.pubs .jr{font-size:.8rem;color:var(--acc);margin-left:.55rem}
.pubs .ti{display:block;font:400 1.05rem/1.4 Fraunces,Georgia,serif;margin-top:.25rem}
footer{padding:5rem 32px;text-align:center;color:var(--mut);font-size:.85rem;
 border-top:1px solid var(--line)}
@media(max-width:820px){.split{grid-template-columns:1fr}
 .split .art{min-height:48vh}.split .say{padding:3rem 1.8rem 4rem}}
"""


def build_split():
    rs = research_html(lambda i, r: (
        '<div class="rs"><h3>%s</h3><p>%s</p></div>' % (r["title"], r["text"])))
    body = """
<header class="split">
 <figure class="art"><img src="%(img)s%(hero)s" alt="Simulation of interstellar turbulence">
  <figcaption>Supersonic turbulence in the interstellar medium</figcaption></figure>
 <div class="say"><h1>%(name)s</h1><div class="tag">%(tag)s</div>
  <div class="aff">%(aff)s</div>
  <div class="lede"><p>Simulating how galaxies form, from individual star-forming regions to
  cosmological volumes.</p></div>
  <div class="cta"><a href="#research">Research</a><a href="#visualizations">Visualizations</a>
  <a href="#cv">CV</a></div></div></header>
<nav class="top">%(nav)s</nav>
<section id="about"><div class="wrap"><h2>About</h2>%(bio)s
 <ul class="tags">%(int)s</ul><div class="stats">%(stats)s</div></div></section>
<section id="research"><div class="wrap"><h2>Research</h2>%(rs)s</div></section>
<section id="visualizations" class="band"><div class="wrap"><h2>Visualizations</h2></div>
 <div class="figs">%(vids)s</div></section>
<section id="publications"><div class="wrap"><h2>Selected publications</h2>
 <ul class="pubs">%(pubs)s</ul></div></section>
<footer>%(email)s</footer>""" % dict(
        img=IMG, hero=C.HERO, name=C.NAME, tag=C.TAGLINE, aff=C.AFFIL,
        nav=nav_html(), bio=bio_html(), int=interests_html(), stats=stats_html(),
        rs=rs, vids=videos_html(limit=5), pubs=pubs_html(), email=C.EMAIL)
    return page("split", "Split", SPLIT_CSS, body)


# ------------------------------------------------------------------------ GALLERY

GALLERY_CSS = """
body{background:#101216;color:#e8edf4;font:300 17px/1.7 Inter,system-ui,sans-serif;
 -webkit-font-smoothing:antialiased}
.hd{max-width:1100px;margin:0 auto;padding:5rem 32px 2.5rem}
.hd h1{font-size:2.4rem;font-weight:200;letter-spacing:-.03em}
.hd p{margin-top:.9rem;color:#8c98aa;max-width:62ch}
.cards{max-width:1100px;margin:0 auto;padding:0 32px 6rem;display:grid;
 grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:28px}
.card{border:1px solid #232a34;border-radius:4px;overflow:hidden;text-decoration:none;
 color:inherit;display:block;background:#161a20;transition:border-color .15s,transform .15s}
.card:hover{border-color:#63d3ff;transform:translateY(-2px)}
.card .sw{height:96px;display:flex}
.card .sw i{flex:1}
.card .bd{padding:1.4rem 1.5rem 1.6rem}
.card h2{font-size:1.25rem;font-weight:400;letter-spacing:-.01em}
.card .d{margin-top:.4rem;font-size:.86rem;color:#8c98aa}
.note{max-width:1100px;margin:0 auto;padding:0 32px 6rem;color:#8c98aa;font-size:.92rem}
.note h3{color:#e8edf4;font-weight:400;font-size:1.05rem;margin-bottom:.7rem}
.note li{margin-left:1.2rem;padding:.2rem 0}
"""

SWATCHES = {
    "observatory": ["#07090d", "#0d1117", "#63d3ff", "#e8edf4"],
    "journal": ["#fbfaf7", "#e0dcd2", "#a8701a", "#1b1a16"],
    "grid": ["#f2f2f0", "#d6d6d2", "#0a72a0", "#0e0e0e"],
    "atlas": ["#0c0a07", "#262016", "#e9a83c", "#f2ece0"],
    "split": ["#ffffff", "#0a0d12", "#1d7fa8", "#141414"],
}


def build_gallery():
    cards = ""
    for slug, name, desc in THEMES:
        sw = "".join('<i style="background:%s"></i>' % c for c in SWATCHES[slug])
        cards += ('<a class="card" href="%s/"><div class="sw">%s</div>'
                  '<div class="bd"><h2>%s</h2><div class="d">%s</div></div></a>'
                  % (slug, sw, name, desc))
    body = """<div class="hd"><h1>Five directions for vadimsemenov.com</h1>
<p>Each is a full working page &mdash; homepage, research, visualizations, publications &mdash;
built with your real content, the five new turbulence renders, and the actual simulation movies.
Resize the window to check mobile.</p></div>
<div class="cards">%s</div>
<div class="note"><h3>What the movies force</h3><ul>
<li><b>3 of 10 are white-background paper figures</b> (gas-cycling, art-disk, art-tng) with axes and
colorbars. On the dark designs they sit on a white plate rather than bleeding &mdash; otherwise they
glare.</li>
<li><b>3 are pure black full-bleed</b> (the three cosmic-ray runs) and bleed edge to edge cleanly.</li>
<li><b>4 are mixed</b> dark montages with bright panels inside.</li>
<li>The five new square renders are the only text-free, uniformly dark assets, so they carry the
heroes and thumbnails.</li></ul>
<h3>Note on copy</h3><p>Bio and tagline are draft text previewing the agreed framing &mdash; Harvard
front and centre, Anthropic added. Publication counts are from the current live site and still need
checking against ADS.</p></div>""" % cards
    return ("""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Theme directions &mdash; vadimsemenov.com</title>%s
<link rel="stylesheet" href="assets/reset.css">
<style>%s</style></head><body>%s</body></html>""" % (FONTS, GALLERY_CSS, body))


# --------------------------------------------------------------------------- RUN

RESET = """*{margin:0;padding:0;box-sizing:border-box}
img,video{max-width:100%}
ul{list-style:none}
.mockbar{position:fixed;right:14px;bottom:14px;z-index:900;display:flex;gap:2px;
 align-items:center;background:rgba(16,18,22,.93);backdrop-filter:blur(10px);
 border:1px solid #2c343f;border-radius:100px;padding:5px 6px;
 font:400 11px/1 Inter,system-ui,sans-serif;letter-spacing:.06em;box-shadow:0 6px 24px rgba(0,0,0,.3)}
.mockbar .mocklabel{color:#6d7887;padding:0 8px;text-transform:uppercase;letter-spacing:.14em}
.mockbar a{color:#aeb9c7;text-decoration:none;padding:6px 10px;border-radius:100px}
.mockbar a:hover{background:#232b35;color:#fff}
.mockbar a.on{background:#63d3ff;color:#07090d}
.mockbar .mockhome{color:#63d3ff}
@media(max-width:640px){.mockbar .mocklabel{display:none}.mockbar a{padding:6px 7px}}
/* Full-page capture: a very tall viewport must not stretch vh-based heroes. */
@media(min-height:1400px){.hero{height:860px!important}.split{min-height:860px!important}}
"""

MOCKJS = """// Videos are preload="none" and never start on their own -- the viewer presses play.
// Nothing is fetched until then. A video that scrolls fully out of view is paused so
// it stops using bandwidth in the background.
var io = new IntersectionObserver(function(es){
  es.forEach(function(e){ if (!e.isIntersecting && !e.target.paused) e.target.pause(); });
}, {threshold: 0});
document.querySelectorAll("video").forEach(function(v){ io.observe(v); });

// The index page holds both About and Research, so the nav highlight has to follow
// the scroll position rather than the page. Subpages have no such anchors and skip this.
(function () {
  var about = document.getElementById("about");
  var research = document.getElementById("research");
  if (!about || !research) return;

  var links = {};
  document.querySelectorAll("nav.top a").forEach(function (a) {
    var m = (a.getAttribute("href") || "").match(/#(about|research)$/);
    if (m) links[m[1]] = a;
  });
  if (!links.about || !links.research) return;

  function update() {
    // whichever section has crossed just under the sticky nav is the current one
    var line = window.scrollY + 140;
    var current = research.offsetTop <= line ? "research" : "about";
    links.about.classList.toggle("on", current === "about");
    links.research.classList.toggle("on", current === "research");
  }

  update();
  window.addEventListener("scroll", update, { passive: true });
  window.addEventListener("resize", update);
})();
"""

BUILDERS = {
    "observatory": build_observatory,
    "journal": build_journal,
    "grid": build_grid,
    "atlas": build_atlas,
    "split": build_split,
}


def main():
    os.makedirs(os.path.join(HERE, "assets"), exist_ok=True)
    with open(os.path.join(HERE, "assets", "reset.css"), "w") as f:
        f.write(RESET)
    with open(os.path.join(HERE, "assets", "mock.js"), "w") as f:
        f.write(MOCKJS)
    for slug, _, _ in THEMES:
        d = os.path.join(HERE, slug)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w") as f:
            f.write(BUILDERS[slug]())
        print("built", slug)
    with open(os.path.join(HERE, "index.html"), "w") as f:
        f.write(build_gallery())
    print("built gallery")


if __name__ == "__main__":
    main()
