# Nocodesquare website

The site for Nocodesquare (NCS): a community and academy for people who build with no-code, automation and AI.

## How it works

- `build_site.py` generates every page into `site/` (plain HTML, no server needed).
- `agent_md.py` writes a Markdown copy of each page plus `llms.txt` for AI agents.
- `assets/` holds the shared CSS and JavaScript; `img/` holds images.
- Python 3.11+ only, no extra packages.

## Build and preview

```bash
python build_site.py
python serve.py        # http://localhost:8080
```

## Hosting (Cloudflare Workers, static assets)

`wrangler.jsonc` tells Cloudflare to serve the `site/` folder.

- Build command: `python build_site.py`
- Deploy command: `npx wrangler deploy`
- Every push to `main` rebuilds and redeploys the live site.
