#!/usr/bin/env python3
"""Make self-hosted Outfit the default font on every page in preview-site/ (run after the page scripts)."""
import glob, os, re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "preview-site")
LINK = '<link rel="preload" href="/fonts/outfit/outfit-latin.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="/fonts/outfit/outfit.css"><link rel="preload" href="/fonts/urbanist/urbanist-latin.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="/fonts/urbanist/urbanist.css">'
n = 0
for p in glob.glob(os.path.join(ROOT, "**/*.html"), recursive=True):
    h = open(p, encoding="utf-8", errors="ignore").read()
    o = h
    h = re.sub(r'<link[^>]*(?:fonts\.googleapis\.com|fonts\.gstatic\.com)[^>]*>', "", h)
    h = h.replace(LINK, "")
    h = h.replace("</head>", LINK + "</head>", 1)
    if h != o:
        open(p, "w", encoding="utf-8").write(h); n += 1
print("pages updated:", n)
