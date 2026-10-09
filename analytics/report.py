#!/usr/bin/env python3
"""Print page-view statistics from the site-stats D1 database.

    python3 report.py            # last 30 days
    python3 report.py --days 7
    python3 report.py --local    # the wrangler dev database instead of production

kind: human    = page shown to a real browser (beacon fired, no webdriver)
      probable = browser-like request without a beacon (ad blocker, JS off, bounced < 3 s)
      bot      = crawler user agent, hosting network, or missing browser headers
"""
import argparse
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))


def query(sql, local):
    out = subprocess.run(
        ["npx", "wrangler", "d1", "execute", "site-stats", "--json",
         "--local" if local else "--remote", "--command", sql],
        cwd=HERE, capture_output=True, text=True, check=True).stdout
    return json.loads(out)[0]["results"]


def table(title, rows, cols):
    print(f"\n{title}")
    if not rows:
        print("  (none)")
        return
    w = {c: max(len(c), *(len(str(r[c] if r[c] is not None else "")) for r in rows)) for c in cols}
    print("  " + "  ".join(c.ljust(w[c]) for c in cols))
    for r in rows:
        print("  " + "  ".join(str(r[c] if r[c] is not None else "").ljust(w[c]) for c in cols))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--local", action="store_true")
    a = ap.parse_args()
    since = f"ts > (unixepoch() - {a.days} * 86400) * 1000"
    q = lambda sql: query(sql, a.local)

    print(f"vadimsemenov.com, last {a.days} days")
    table("Views by kind", q(
        f"SELECT kind, count(*) views, count(DISTINCT day || visitor) visitor_days "
        f"FROM classified WHERE {since} GROUP BY kind ORDER BY views DESC"),
        ["kind", "views", "visitor_days"])
    table("Daily", q(
        f"SELECT day, sum(kind='human') human, sum(kind='probable') probable, "
        f"sum(kind='bot') bot, count(DISTINCT CASE WHEN kind != 'bot' THEN visitor END) visitors "
        f"FROM classified WHERE {since} GROUP BY day ORDER BY day"),
        ["day", "human", "probable", "bot", "visitors"])
    table("Pages", q(
        f"SELECT path, sum(kind='human') human, sum(kind='probable') probable, sum(kind='bot') bot "
        f"FROM classified WHERE {since} GROUP BY path ORDER BY sum(kind != 'bot') DESC, bot DESC LIMIT 20"),
        ["path", "human", "probable", "bot"])
    table("Referrers", q(
        f"SELECT ref, sum(kind='human') human, sum(kind='probable') probable, sum(kind='bot') bot FROM classified WHERE {since} AND ref IS NOT NULL "
        f"GROUP BY ref ORDER BY sum(kind != 'bot') DESC, bot DESC LIMIT 20"),
        ["ref", "human", "probable", "bot"])
    table("Countries", q(
        f"SELECT country, sum(kind='human') human, sum(kind='probable') probable, sum(kind='bot') bot FROM classified WHERE {since} "
        f"GROUP BY country ORDER BY sum(kind != 'bot') DESC, bot DESC LIMIT 20"),
        ["country", "human", "probable", "bot"])
    table("Top bot sources (to check the rules)", q(
        f"SELECT substr(ua, 1, 70) ua, as_org, ua_bot, dc, lang IS NULL no_lang, count(*) views "
        f"FROM classified WHERE {since} AND kind = 'bot' "
        f"GROUP BY ua, as_org ORDER BY views DESC LIMIT 15"),
        ["views", "ua_bot", "dc", "no_lang", "as_org", "ua"])


if __name__ == "__main__":
    main()
