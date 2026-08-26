# vadimsemenov.com

Static site for Vadim Semenov, computational astrophysicist at the Center for
Astrophysics | Harvard & Smithsonian.

Served by GitHub Pages from `docs/` on `main`, at the custom domain in `docs/CNAME`.

## Layout

- `docs/` — the published site: three pages, assets, and the simulation movies
- `src/content.py` — all site copy, publication list, reference links, YouTube ids
- `src/build_observatory.py` — generates the three pages from that content

## Rebuilding

Edit `src/content.py`, then from `mockups/`:

    MOCKBAR=0 ASSET_PREFIX="" MOVIE_PREFIX="movies/" OUT_DIR="$PWD/../docs" \
      python3 build_observatory.py

Videos are native `<video preload="none">` with poster frames: nothing downloads
until the viewer presses play, so the page costs ~1 MB to open rather than ~117 MB.
