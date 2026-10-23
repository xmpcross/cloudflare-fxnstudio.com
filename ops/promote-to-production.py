#!/usr/bin/env python3
"""Copy the redesigned preview pages and assets into the production source tree (static/content + static/public)."""
import json, re, shutil
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
SRC = BASE / "static-flow" / "preview-site.fxn-backup"
DST = BASE / "static"
PREVIEW = "http://51.161.208.188:8793"
PROD = "https://fxnstudio.com"

pages = [p.relative_to(SRC).as_posix() for p in SRC.rglob("index.html")]
routes = json.loads((DST / "routes.json").read_text())
by_file = {r["file"]: r for r in routes}


def clean(text):
    text = text.replace(PREVIEW, PROD)
    text = re.sub(r'<link rel="sitemap"[^>]*>', "", text)
    text = text.replace("Enquiry form is off in this preview; email hello@fxnstudio.com", "Online enquiries are being set up. Please email hello@fxnstudio.com.")
    return text


for rel in sorted(pages):
    html = clean((SRC / rel).read_text(encoding="utf-8"))
    dest = DST / "content" / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html, encoding="utf-8")
    title = re.search(r"<title>(.*?)</title>", html, flags=re.S).group(1).strip()
    path = "/" + rel.removesuffix("index.html").rstrip("/")
    path = path if path != "/" else "/"
    if rel in by_file:
        by_file[rel]["title"] = title.replace("&amp;", "&")
    else:
        routes.append({"path": path, "file": rel, "title": title.replace("&amp;", "&"), "status": 200})

# assets that the new pages reference
pub = DST / "public"
for d in ("_astro", "fonts", "img"):
    if (pub / d).exists():
        shutil.rmtree(pub / d)
    shutil.copytree(SRC / d, pub / d)
for f in ("fxn-logo.svg", "og-image.png"):
    shutil.copy(SRC / f, pub / f)
for f in ("rss.xml", "search-index.json"):
    (pub / f).write_text(clean((SRC / f).read_text(encoding="utf-8")), encoding="utf-8")

(DST / "routes.json").write_text(json.dumps(routes, indent=2) + "\n")
print(len(pages), "pages ->", DST / "content", "; routes now", len(routes))
