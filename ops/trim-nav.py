#!/usr/bin/env python3
"""Remove the Work, Insights and Engagements items from the top navigation on every preview page."""
import glob, os, re

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "preview-site"))


def cut_div(h, start_pat):
    m = re.search(start_pat, h)
    if not m:
        return h
    i, depth, pos = m.start(), 0, m.start()
    for t in re.finditer(r"<div\b|</div>", h[i:]):
        depth += 1 if t.group(0) == "<div" else -1
        if depth == 0:
            return h[:i] + h[i + t.end():]
    return h


n = 0
for p in glob.glob("**/*.html", recursive=True):
    h = open(p, encoding="utf-8").read()
    o = h
    for k in ("menu-1", "menu-2"):
        h = re.sub(r'<li\b[^>]*><button[^>]*data-menu-trigger="%s".*?</button></li>' % k, "", h, flags=re.S)
        h = cut_div(h, r'<div id="%s"[^>]*data-menu-panel' % k)
    h = re.sub(r"<li\b[^>]*><details[^>]*><summary[^>]*>(?:Work|Insights)<.*?</details></li>", "", h, flags=re.S)
    h = re.sub(r'<li\b[^>]*><a href="/pricing/"[^>]*>Engagements</a></li>', "", h)
    if h != o:
        open(p, "w", encoding="utf-8").write(h)
        n += 1
print("pages updated:", n)
