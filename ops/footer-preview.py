#!/usr/bin/env python3
"""Replace the footer on every preview-site page with the FXN Studio footer."""
import glob, os, re

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "preview-site"))

COLS = {
    "Services": [("Website design", "/services/web-design/"), ("Custom software", "/services/web-development/"),
                 ("eCommerce", "/services/ecommerce-development/"), ("AI integration", "/services/ai-integrations/"),
                 ("Technology", "/technology/")],
    "Work": [("Portfolio", "/portfolio/"), ("Engagements", "/pricing/"), ("Our process", "/process/")],
    "Insights": [("All articles", "/blog/"), ("Web design", "/blog/category/web-design/"),
                 ("SEO and growth", "/blog/category/seo-growth/"), ("AI and automation", "/blog/category/ai-automation/"),
                 ("eCommerce", "/blog/category/ecommerce/")],
    "Studio": [("About us", "/about-us/"), ("Contact", "/contact/"), ("Search", "/blog/search/"), ("RSS", "/rss.xml")],
}
cols = "".join(
    f'<div><p class="fx-footer__h">{t}</p><ul>' + "".join(f'<li><a href="{h}">{l}</a></li>' for l, h in items) + "</ul></div>"
    for t, items in COLS.items()
)
FOOTER = (
    '<footer class="fx-footer"><div class="fx-footer__inner">'
    '<div class="fx-footer__brand"><a href="/" aria-label="FXN Studio home"><img src="/fxn-logo.svg" alt="FXN Studio" width="173" height="32"></a>'
    "<p>Web design, custom software, e-commerce and AI integration from a Perth studio working with clients worldwide.</p>"
    '<ul class="fx-footer__contact"><li><a href="mailto:hello@fxnstudio.com">hello@fxnstudio.com</a></li><li>Perth, Australia</li></ul></div>'
    f'<nav class="fx-footer__nav" aria-label="Footer">{cols}</nav></div>'
    '<div class="fx-footer__bar"><div><p>© 2026 FXN Studio. All rights reserved.</p>'
    "<p>Australia-based. Working worldwide.</p></div></div></footer>"
)
n = 0
for p in glob.glob("**/*.html", recursive=True):
    h = open(p, encoding="utf-8").read()
    new, c = re.subn(r"<footer\b.*?</footer>", lambda m: FOOTER, h, flags=re.S)
    if c:
        open(p, "w", encoding="utf-8").write(new)
        n += 1
print("footers replaced:", n)
