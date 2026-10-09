# site-stats

Cloudflare Worker in front of GitHub Pages that counts page views for
vadimsemenov.com, independently of GoatCounter.

Every request passes through unchanged. For each HTML page served with
status 200 the worker writes a row to the D1 database `site-stats` (raw
request signals: path, referrer, user agent, Accept-Language, Sec-Fetch-Mode,
country, network) and injects a small inline script that posts to `/_k` once
the page has been visible for 3 s or the visitor scrolls, clicks or types. IPs
are never stored, only a hash with a salt that is deleted after each UTC day.

Classification happens at query time in the `classified` view (`schema.sql`),
so the rules can be changed and applied retroactively:

- human: the beacon fired and `navigator.webdriver` was false
- probable: browser-like request without a beacon (ad blocker, JS off, left within 3 s)
- bot: crawler user agent, hosting network, missing browser headers, or 5+ views
  from one visitor in a day without a single beacon

Dashboard: https://vadimsemenov.com/_stats, behind Cloudflare Access (Zero Trust
team `vadimsemenov`, application "Site stats", one-time PIN by email). The worker
also verifies the Access token against `ACCESS_TEAM` / `ACCESS_AUD` in
`wrangler.toml` and returns 404 without a valid one. The page is rendered from D1
on each request (`src/dashboard.js`); nothing is stored in the git repo.

Commands (from this folder):

    python3 report.py --days 30                 # summary
    npx wrangler deploy                         # after editing src/worker.js
    npx wrangler d1 execute site-stats --remote --file schema.sql   # after editing the view
    npx wrangler dev --local-upstream vadimsemenov.com --upstream-protocol https
                                                # local test against the live site

To bypass the worker, set the DNS records in Cloudflare to "DNS only".
