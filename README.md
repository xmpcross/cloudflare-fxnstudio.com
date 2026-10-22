# fxnstudio.com — static site

Standalone HTML/CSS/JavaScript replacement for Payload, prepared and verified
locally. **Not deployed; the public domain still uses the original server.**

## Edit and build

- `content/`: 51 published HTML documents, exported from the public Payload API
  and rendered with the current title/description overrides.
- `public/`: images, fonts, CSS and browser JavaScript.
- `routes.json`: public route inventory and expected statuses.
- `scripts/build.py`: copies sources to `dist/` and generates sitemap and hosting rules.

Requirements: Python 3. Node/npm is needed only for Cloudflare development and
deployment. A plain build requires no database, CMS, running Node service or
credentials. Each project is independent of the original `app/` and backups.

```sh
python3 scripts/build.py
npm ci
npm test
npm run dev
```

Edit HTML directly and rebuild. Add the HTML file and an entry in `routes.json`
for a new page; include its canonical URL for sitemap inclusion. Generated
`dist/` is disposable; never edit it as your source. Drafts and CMS users are
not exported. Keep root `404.html` so unknown URLs do not become an SPA fallback.

## Cloudflare Pages setup

Match Holdings with a Git-connected Pages project named `fxnstudio-com`.
Use build command `npm run build`, output directory `dist`, framework None,
and this `static/` directory as the repository root (or configure its path as
Pages root if retaining a parent repository). Choose the desired production
branch. Do not create a Direct Upload project if Git integration is wanted.
No Cloudflare project, Git repository, DNS record or custom domain has been
created or changed by this migration yet.

For a deliberately chosen Direct Upload setup instead, `npm run deploy` wraps
Wrangler. `wrangler.jsonc` includes the correct project name and output directory.
Validate the preview before adding apex and www custom domains. Preserve MX,
SPF, DKIM and DMARC records; configure www to redirect to apex.

## Contacts and dynamic behavior

The existing enquiry forms simulate submission in `public/assets/main.js`.
This migration preserves their current behavior; it does not add email delivery.
Studio's separate Sandbox demo preview is still in `../worktrees/demo9-home`
and is outside this production-content migration. It still uses Payload.

## Validation and rollback

`npm test` checks every source page against the build, all local HTML/CSS links,
fonts and images, sitemap and 404. All 51 routes were also checked through the
local Cloudflare Pages runtime. Mobile and desktop browser evidence is under
`../output/playwright/` (Studio screenshots are in Europe's output directory).

Original database, public content export and nginx configuration are backed up
outside this directory in `/kspellman/sites/fxnstudio.com/backups/static-migration-20261022T175419Z`. Existing app, services, databases
and preview deployments are retained. No DNS or live nginx settings changed.

For local nginx hosting, `../config/nginx-static.conf` is the prepared complete
replacement for `/etc/nginx/sites-available/fxnstudio.com`. Build and test first,
install it, run `nginx -t`, then reload nginx. Restore the backed-up nginx
configuration to roll back. For Cloudflare rollback, retain DNS values before
cutover and restore them to the original host if necessary. Do not disable the
old app/database services until the chosen deployment is verified.
