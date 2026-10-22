# fxnstudio.com — Cloudflare Pages

Live at **https://fxnstudio.com**. Both apex and www custom domains are active.
Cloudflare Pages serves 51 exported HTML documents and local assets without
Payload, Next.js or a database. The original server also serves the static build
as a fallback. Production Payload is stopped and disabled.

## Edit, verify and publish

- `content/`: editable HTML documents, including metadata.
- `public/`: CSS, browser JavaScript, images and fonts.
- `routes.json`: public routes and expected HTTP statuses.
- `scripts/build.py`: builds `dist/`, sitemap and hosting rules.

Requirements: Python 3; Node 22+ and npm for development tooling.

```sh
npm ci
npm run build
npm test
npm run dev
python3 scripts/check-deployment.py https://fxnstudio.com
```

Edit sources, commit and push **`migrate/cloudflare-pages`** to
https://github.com/xmpcross/cloudflare-fxnstudio.com. Cloudflare automatically builds and deploys
that branch. Project: `fxnstudio-com`; build command: `npm run build`; output: `dist`;
repository root: `/`. Other branches produce previews. The `main` branch remains
the historical source. Generated `dist/` and credentials must not be committed.
`deploy.sh` is available for manual Wrangler uploads; prefer Git deployments.

Preview URL: https://fxnstudio-com.pages.dev

## Redirects and hosting

HTTP redirects to HTTPS. The shared `fxn-sites-www-redirect` Cloudflare Worker
redirects only `www.fxneurope.eu/*` and `www.fxnstudio.com/*` to their respective
apex domains, preserving path and query string. Certificate-validation requests
pass through. Apex content is served as static Pages assets. Its tracked source
and deployment config are in `ops/`; update the Worker explicitly with:

```sh
npx wrangler deploy --config ops/wrangler.jsonc
```

That Worker is shared by both sites; keep the source copies synchronized.
Europe also preserves the `/` to `/en/` redirect and explicit 404 routes.
Unknown pages, `/admin` and CMS API URLs return 404.

## Contact behavior and retained services

The existing enquiry forms still simulate submission in `public/assets/main.js`;
this migration does not add email delivery. They should be connected to an
email handler before relying on submissions.

The production Payload app is stopped and disabled. The separate Sandbox demo
at `preview.fxnstudio.com` is retained; its Payload service, PostgreSQL database
and backup timer remain running. It is independent of this production site.

## Verification and rollback

All 51 published routes passed status/title checks on the Pages URL and
public domain, along with 404s, headers, sitemap and robots. Source/build fidelity
and local asset/link checks pass. HTTPS and www redirects are verified. Mail and
all unrelated DNS records were preserved.

Local operational records: `../migration/cloudflare-cutover.json` and
`../migration/static-status.json`. Cutover backups (DNS, nginx, service states)
are in `../backups/cloudflare-cutover/`. Original exported content and database
backups are in the earlier `../backups/static-migration-*/` directory.

To move hosting back to the server, restore only the apex/www DNS records from
`dns-before.json`, leaving email records untouched. The origin already serves
`static/dist/` via `../config/nginx-static.conf`. To restore Payload specifically,
start its database and app services, restore `origin-nginx-before.conf`, run
`nginx -t`, and reload nginx. Europe additionally needs its backup timer enabled.
Keep backups and the old app directories until rollback is no longer needed.
