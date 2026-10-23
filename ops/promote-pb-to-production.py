#!/usr/bin/env python3
"""Publish the Pixelbin-layout pages (home, about, services + 6 service pages, portfolio, contact) into the production source tree."""
import html, json, os, re, shutil
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
SRC = BASE / "static-flow" / "preview-site"
DST = BASE / "static"
PAGES = ["", "about-us", "services", "services/web-design", "services/custom-software", "services/ecommerce",
         "services/open-source-platforms", "services/ai-integration", "services/seo-growth", "portfolio", "contact"]
OLD = {"web-development": "custom-software", "ecommerce-development": "ecommerce", "ai-integrations": "ai-integration",
       "open-source-platform-solutions": "open-source-platforms"}

routes = json.loads((DST / "routes.json").read_text())
by_file = {r["file"]: r for r in routes}
for rel in PAGES:
    f = (rel + "/index.html").lstrip("/")
    t = (SRC / f).read_text(encoding="utf-8")
    assert "51.161.208.188" not in t and "127.0.0.1" not in t, f
    dest = DST / "content" / f
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(t, encoding="utf-8")
    title = html.unescape(re.search(r"<title>(.*?)</title>", t, flags=re.S).group(1).strip())
    if f in by_file:
        by_file[f]["title"] = title
    else:
        routes.append({"path": "/" + rel, "file": f, "title": title, "status": 200})

# retire the four renamed service URLs: remove their pages and redirect them to the new ones
retired = {f"services/{o}/index.html" for o in OLD}
routes = [r for r in routes if r["file"] not in retired]
for o in OLD:
    shutil.rmtree(DST / "content" / "services" / o, ignore_errors=True)
# repoint links inside the pages that remain
for f in (DST / "content").rglob("*.html"):
    t = f.read_text(encoding="utf-8"); o = t
    for old, new in OLD.items():
        t = t.replace(f"/services/{old}/", f"/services/{new}/").replace(f"/services/{old}\"", f"/services/{new}\"")
    if t != o: f.write_text(t, encoding="utf-8")
redir = "\n".join(f"/services/{o} /services/{n}/ 301\n/services/{o}/ /services/{n}/ 301" for o, n in OLD.items()) + "\n"
(DST / "public" / "_redirects").write_text(redir)

# assets used by the new pages
pub = DST / "public"
def cp(rel):
    s = SRC / rel.lstrip("/"); d = pub / rel.lstrip("/")
    d.parent.mkdir(parents=True, exist_ok=True); shutil.copy(s, d)
for d in ("img/fxn", "fonts/outfit", "fonts/urbanist"):
    dst = pub / d
    shutil.rmtree(dst, ignore_errors=True); shutil.copytree(SRC / d, dst)
shutil.rmtree(pub / "wp-content/uploads/fxn", ignore_errors=True)
shutil.copytree(SRC / "wp-content/uploads/fxn", pub / "wp-content/uploads/fxn", ignore=shutil.ignore_patterns("bg"))
for rel in ("/wp-content/litespeed/css/93a72da34d9e68e233e66d7b5ce06de9.css", "/wp-content/litespeed/js/5c366d9ff57e163d3e3e323f87aa3720.js",
            "/wp-includes/js/jquery/jquery.js", "/wp-content/themes/repurpose/img/favicon/favicon.png", "/wp-content/themes/repurpose/img/favicon/favicon.svg"):
    cp(rel)
css = (SRC / "wp-content/litespeed/css/93a72da34d9e68e233e66d7b5ce06de9.css").read_text(encoding="utf-8", errors="ignore")
# the stylesheet points at a theme path that was mirrored under /pixelbin/; use the real path, and strip the original site's host from scripts
cssf = pub / "wp-content/litespeed/css/93a72da34d9e68e233e66d7b5ce06de9.css"
cssf.write_text(cssf.read_text(encoding="utf-8").replace("/pixelbin/wp-content/themes/", "/wp-content/themes/"), encoding="utf-8")
shutil.copy(DST.parent / "backups/pre-publish-20261023b/public/wp-content/themes/repurpose/img/diagonal-stripes.svg", pub / "wp-content/themes/repurpose/img/diagonal-stripes.svg")
for js in ("5c366d9ff57e163d3e3e323f87aa3720.js", "f09da4fde74ed1b1be3f8b4d63a7987c.js"):
    cp("/wp-content/litespeed/js/" + js)
    jf = pub / "wp-content/litespeed/js" / js
    jf.write_text(jf.read_text(encoding="utf-8", errors="ignore").replace("https://pixelbin.com/", "/").replace("https:\\/\\/pixelbin.com\\/", "\\/"), encoding="utf-8")
for r in sorted(set(re.findall(r"url\([\"']?(/[^)\"'?#]+)", css))):
    if (SRC / r.lstrip("/")).is_file(): cp(r)
(DST / "routes.json").write_text(json.dumps(routes, indent=2) + "\n")
print("routes:", len(routes))
