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
## Admin dashboard (nocodesquare.com/admin)

Write, edit and delete blog posts, and change site settings, without touching code.

- Sign in with a GitHub account that has write access to this repository.
- **Blog posts** live in `content/blog/*.md` (JSON details at the top, then the article in Markdown).
- **Site settings** (cohort date, fees, social links, newsletter webhook) live in `content/settings.json`.
- Drafts: save a post as a draft, mark it ready, then publish. Publishing commits to `main` and the site rebuilds in about 2–3 minutes.
- Images uploaded in the admin go to `img/blog/`.
- Sign-in is handled by `worker.js` (`/api/auth`, `/api/callback`). It needs a GitHub OAuth App:
  `GITHUB_CLIENT_ID` in `wrangler.jsonc`, and `GITHUB_CLIENT_SECRET` as a secret in Cloudflare.

To try the admin on your own computer without GitHub: run `npx decap-server` in this folder,
then `npx wrangler dev`, and open http://localhost:8787/admin/.

## Hosting (Cloudflare Workers, static assets)

`wrangler.jsonc` tells Cloudflare to serve the `site/` folder, and to run `worker.js` only for `/api/*`.

- Build command: `python build_site.py`
- Deploy command: `npx wrangler deploy`
- Every push to `main` rebuilds and redeploys the live site.
