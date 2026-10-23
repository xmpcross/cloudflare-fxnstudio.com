#!/usr/bin/env python3
"""Add a breadcrumb trail (and BreadcrumbList data) to the FXN preview pages; idempotent. Run after the page scripts."""
import html, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svc_parse import SERVICES

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "preview-site")
SITE = "https://fxnstudio.com"
PAGES = {"about-us": [("Home", "/"), ("About", None)], "services": [("Home", "/"), ("Services", None)],
         "portfolio": [("Home", "/"), ("Portfolio", None)], "contact": [("Home", "/"), ("Contact", None)]}
for slug, _, label in SERVICES:
    PAGES[f"services/{slug}"] = [("Home", "/"), ("Services", "/services/"), (label, None)]

STYLE = ('<style>main[role=main]{padding-top:96px}.bc-bar{margin:0;padding:12px 0;background:transparent;border-bottom:1px solid #ececec}.bc-bar .container{padding-left:30px;padding-right:0}'
         '.bc{margin:0;padding:0;font-size:14px;line-height:1.3;color:#555}.bc ol{display:flex;flex-wrap:wrap;gap:.35rem .6rem;list-style:none;margin:0;padding:0}'
         '.bc li{margin:0;padding:0}.bc li+li:before{content:"/";margin-right:.6rem;color:#a3a3a3}.bc a{color:#555;text-decoration:none}.bc a:hover{color:#111;text-decoration:underline}.bc [aria-current]{color:#111}'
         '@media (max-width:899px){main>.page__heading{padding-top:1.25rem!important}}.page__heading>.container,.page__heading>.svp-wrap,.page__heading>.svo-wrap,.page__heading .row{margin-top:0!important}</style>')

for page, trail in PAGES.items():
    f = os.path.join(BASE, page, "index.html")
    h = open(f, encoding="utf-8").read()
    h = re.sub(r'<style>(?:main\[role=main\]\{padding-top:96px\})?\.bc-bar\{.*?</style>', "", h, flags=re.S)
    h = re.sub(r'<style>\.bc\{.*?</style>', "", h, flags=re.S)
    h = re.sub(r'<div class="bc-bar">.*?</nav></div></div>', "", h, flags=re.S)
    h = re.sub(r'<nav class="bc"[^>]*>.*?</nav>', "", h, flags=re.S)
    h = re.sub(r'<script type="application/ld\+json" id="bc-ld">.*?</script>', "", h, flags=re.S)
    h = re.sub(r'<p class="(?:pf-eyebrow|svp-crumb)">.*?</p>', "", h, count=1, flags=re.S)
    items = "".join(
        (f'<li><a href="{u}">{html.escape(t)}</a></li>' if u else f'<li><span aria-current="page">{html.escape(t)}</span></li>') for t, u in trail)
    bar = f'{STYLE}<div class="bc-bar"><div class="container"><nav class="bc" aria-label="Breadcrumb"><ol>{items}</ol></nav></div></div>'
    h2, n = re.subn(r'(<main role="main">)', lambda m: m.group(1) + bar, h, count=1)
    assert n, page
    path = "/" + page + "/"
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": t, "item": SITE + (u or path)} for i, (t, u) in enumerate(trail)]}
    h2 = h2.replace("</head>", '<script type="application/ld+json" id="bc-ld">' + json.dumps(ld) + "</script></head>", 1)
    open(f, "w", encoding="utf-8").write(h2)
    print(page, " / ".join(t for t, _ in trail))
