-- One row per HTML page served with status 200. The worker stores raw request
-- signals; whether a view counts as human or bot is decided at query time in
-- the `classified` view below, so the rules can be revised retroactively.
CREATE TABLE IF NOT EXISTS views (
  id          TEXT PRIMARY KEY,   -- random per view, embedded in the page for the beacon
  ts          INTEGER NOT NULL,   -- unix ms, server time of the page request
  host        TEXT,
  path        TEXT NOT NULL,
  ref         TEXT,               -- referrer origin + path (no query string); NULL if none
  ua          TEXT,
  lang        TEXT,               -- first Accept-Language tag; NULL if header missing
  sec_fetch   INTEGER,            -- 1 if the browser sent Sec-Fetch-Mode
  country     TEXT,
  asn         INTEGER,
  as_org      TEXT,
  ua_bot      INTEGER NOT NULL,   -- user agent matches the crawler / script pattern
  dc          INTEGER NOT NULL,   -- network is a known hosting / cloud provider
  visitor     TEXT,               -- sha256(daily salt, ip, ua); salt deleted after the day ends
  beacon_ts   INTEGER,            -- unix ms when the in-page beacon arrived; NULL if never
  beacon_why  TEXT,               -- 'v' visible for 3 s, 'i' scroll / click / key
  webdriver   INTEGER,            -- navigator.webdriver reported by the beacon
  screen_w    INTEGER
);
CREATE INDEX IF NOT EXISTS views_ts ON views (ts);

CREATE TABLE IF NOT EXISTS salts (
  day   TEXT PRIMARY KEY,         -- YYYY-MM-DD (UTC)
  salt  TEXT NOT NULL
);

DROP VIEW IF EXISTS classified;
CREATE VIEW classified AS
WITH burst AS (   -- visitors with many page loads in a day and not one beacon
  SELECT visitor, date(ts / 1000, 'unixepoch') day FROM views
  GROUP BY visitor, day HAVING count(*) >= 5 AND count(beacon_ts) = 0
)
SELECT v.*,
  CASE
    WHEN beacon_ts IS NOT NULL AND COALESCE(webdriver, 0) = 0 THEN 'human'
    -- No beacon (or a webdriver one): every modern browser sends Accept-Language and
    -- Sec-Fetch-Mode, so their absence marks a script.
    WHEN beacon_ts IS NOT NULL OR ua_bot = 1 OR dc = 1 OR lang IS NULL OR sec_fetch = 0
      OR b.visitor IS NOT NULL THEN 'bot'
    ELSE 'probable'
  END AS kind,
  date(ts / 1000, 'unixepoch') AS day
FROM views v
LEFT JOIN burst b ON b.visitor = v.visitor AND b.day = date(v.ts / 1000, 'unixepoch');
