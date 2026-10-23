#!/usr/bin/env python3
"""Download every pixelbin.com asset referenced by the mirrored files that is not on disk yet."""
import os, re, sys, urllib.request, urllib.parse, glob

ROOT = sys.argv[1]
os.chdir(ROOT)
pat = re.compile(r'(?:https?:)?(?:\\?/\\?/)pixelbin\.com(\\?/[^\s"\'<>()\\]*(?:\\/[^\s"\'<>()\\]*)*)')
seen, got = set(), 0
for rnd in range(4):
    new = 0
    files = [f for f in glob.glob("**/*", recursive=True) if os.path.isfile(f) and f.split(".")[-1].lower() in ("html", "css", "js", "json", "svg", "xml")]
    urls = set()
    for f in files:
        try:
            t = open(f, encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        for m in re.finditer(r'https?:(?:\\?/){2}pixelbin\.com(\\?/[^\s"\'<>()\\,;]*(?:\\/[^\s"\'<>()\\,;]*)*)', t):
            p = m.group(1).replace("\\/", "/")
            p = p.split("?")[0].split("#")[0]
            if p and p != "/" and not p.endswith("/") and "wp-json" not in p and "xmlrpc" not in p and "feed" not in p:
                urls.add(p)
    for p in sorted(urls - seen):
        seen.add(p)
        dest = urllib.parse.unquote(p.lstrip("/"))
        if os.path.exists(dest):
            continue
        try:
            req = urllib.request.Request("https://pixelbin.com" + p, headers={"User-Agent": "Mozilla/5.0"})
            data = urllib.request.urlopen(req, timeout=30).read()
            os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
            open(dest, "wb").write(data)
            got += 1; new += 1
        except Exception as e:
            print("fail", p, e)
    print("round", rnd, "new", new)
    if not new:
        break
print("downloaded", got)
