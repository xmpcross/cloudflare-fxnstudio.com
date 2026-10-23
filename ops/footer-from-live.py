#!/usr/bin/env python3
"""Rebuild the footer link columns on every preview page from the live https://fxnstudio.com/ site.

Reads the live sitemap, the live footer navigation and each service page heading. Pages that
exist in the preview link locally; the rest (privacy, terms and so on) link to the live site.
"""
import glob, html, os, re, urllib.request

LIVE = "https://fxnstudio.com"
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "preview-site")


def get(path):
    req = urllib.request.Request(LIVE + path, headers={"User-Agent": "Mozilla/5.0 (footer-sync)"})
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8")


def clean(t):
    return html.unescape(re.sub(r"<[^>]+>", "", t)).strip()


home = get("/")
footer = re.search(r"<footer\b.*?</footer>", home, flags=re.S).group(0)
copyright_line = clean(re.search(r"<p>(©[^<]+)</p>", footer).group(1))
footer_nav = re.findall(r'<a href="(/[^"]*)">([^<]+)</a>', re.search(r"<nav[^>]*>.*?</nav>", footer, flags=re.S).group(0))

# live email is Cloudflare-obfuscated; decode it
cf = re.search(r"email-protection#([0-9a-f]+)", footer).group(1)
key = int(cf[:2], 16)
email = "".join(chr(int(cf[i:i + 2], 16) ^ key) for i in range(2, len(cf), 2))

sitemap = re.findall(r"<loc>https://fxnstudio\.com(/[^<]*)</loc>", get("/sitemap.xml"))
service_paths = [p for p in sitemap if p.startswith("/services/") and p != "/services/"]


def heading(path):
    page = get(path)
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", page, flags=re.S)
    title = clean(re.search(r"<title>(.*?)</title>", page, flags=re.S).group(1)).split("|")[0].strip()
    return clean(h1.group(1)) if h1 else title


SHORT = {  # long live headings shortened to a footer label
    "/services/web-design/": "Website design",
    "/services/web-development/": "Custom software",
    "/services/ecommerce-development/": "eCommerce",
    "/services/ai-integrations/": "AI integration",
    "/services/open-source-platform-solutions/": "Open-source platforms",
    "/services/seo-growth/": "SEO and growth",
}


def local_exists(path):
    f = os.path.join(ROOT, path.strip("/"), "index.html") if path != "/" else os.path.join(ROOT, "index.html")
    return os.path.exists(f)


def a(path, label):
    if local_exists(path):
        return f'<li><a href="{path}">{label}</a></li>'
    return f'<li><a href="{LIVE}{path}" rel="noopener">{label}</a></li>'


services = "".join(a(p, SHORT.get(p) or heading(p)) for p in service_paths)
nav = dict((p, l) for p, l in footer_nav)
company = "".join(a(p, nav[p]) for p in ("/about-us/", "/industries/", "/process/", "/contact/") if p in nav)
resources = a("/portfolio/", "Portfolio") + a("/blog/", "Blog")
legal = "".join(a(p, l) for p, l in footer_nav if p in ("/privacy-policy/", "/terms-of-services/", "/cookie-information/"))

cols = "".join(f'<div><p class="fx-footer__h">{t}</p><ul>{items}</ul></div>' for t, items in
               (("Services", services), ("Company", company), ("Resources", resources), ("Legal", legal)))
FOOTER = (
    '<footer class="fx-footer"><div class="fx-footer__inner">'
    '<div class="fx-footer__brand"><a href="/" aria-label="FXN Studio home"><img src="/fxn-logo.svg" alt="FXN Studio" width="173" height="32"></a>'
    "<p>Web design, custom software, e-commerce and AI integration from a Perth studio working with clients worldwide.</p>"
    f'<ul class="fx-footer__contact"><li><a href="mailto:{email}">{email}</a></li><li>Perth, Australia</li></ul></div>'
    f'<nav class="fx-footer__nav" aria-label="Footer">{cols}</nav></div>'
    f'<div class="fx-footer__bar"><div><p>{copyright_line}</p></div></div></footer>'
)

n = 0
for p in glob.glob(os.path.join(ROOT, "**/*.html"), recursive=True):
    t = open(p, encoding="utf-8").read()
    new, c = re.subn(r"<footer\b.*?</footer>", lambda m: FOOTER, t, flags=re.S)
    if c:
        open(p, "w", encoding="utf-8").write(new)
        n += 1
print("email:", email)
print("services:", [SHORT.get(p) or p for p in service_paths])
print("company:", [nav[p] for p in ("/about-us/", "/industries/", "/process/", "/contact/") if p in nav])
print("legal:", [l for p, l in footer_nav if p in ("/privacy-policy/", "/terms-of-services/", "/cookie-information/")])
print("footers updated:", n)
