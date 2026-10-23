"""Shared header and footer for the Pixelbin-layout pages, taken from the home page and given one nav."""
import os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svc_parse import SERVICES

NAV = [("Home", "/", "home"), ("About", "/about-us/", "about"), ("Services", "/services/", "services"), ("Portfolio", "/portfolio/", "portfolio")]
FOOT = NAV + [("Contact", "/contact/", "contact")]


SUBMENU_STYLE = """<style>
.header{overflow:visible!important}.menu-item.has-sub{position:relative}
.menu-item.has-sub>a:after{content:"";display:inline-block;width:.38em;height:.38em;margin-left:.45em;border-right:1.5px solid currentColor;border-bottom:1.5px solid currentColor;transform:translateY(-.15em) rotate(45deg);transition:transform .2s}
.sub-menu{position:absolute;left:-1rem;top:100%;min-width:15.5rem;margin:0;padding:.6rem;list-style:none;background:#fff;border:1px solid #e4e6eb;border-radius:10px;box-shadow:0 18px 40px -18px rgb(15 18 32/.35);opacity:0;visibility:hidden;transform:translateY(6px);transition:opacity .18s,transform .18s,visibility .18s;z-index:120}
.menu-item.has-sub:hover>.sub-menu,.menu-item.has-sub:focus-within>.sub-menu{opacity:1;visibility:visible;transform:none}
.menu-item.has-sub:hover>a:after{transform:translateY(-.05em) rotate(225deg)}
.nav .sub-menu{display:block!important;flex-direction:column!important;width:max-content}.nav .sub-menu li{margin:0!important;padding:0!important;display:block!important;float:none!important;width:auto!important}
.nav .sub-menu a{display:block!important;padding:.65rem .85rem!important;line-height:1.2!important;height:auto!important;border-radius:7px;font-size:14px;font-weight:500;letter-spacing:0;text-transform:none;color:#1c2030!important;white-space:nowrap;text-decoration:none}
.sub-menu a:hover,.sub-menu a:focus{background:#f1f2f6;color:#4f46e5!important}
.sub-menu a.on{color:#4f46e5!important}
@media (max-width:991px){.sub-menu{position:static;opacity:1;visibility:visible;transform:none;box-shadow:none;border:0;background:transparent;padding:.25rem 0 .25rem 1rem;min-width:0}.menu-item.has-sub>a:after{display:none}.sub-menu a{padding:.4rem 0;color:inherit!important}}
</style>"""


def submenu(current_path=""):
    items = "".join(f'<li><a href="/services/{sl}/"{" class=\"on\"" if current_path == sl else ""}>{lb}</a></li>' for sl, _, lb in SERVICES)
    return f'<ul class="sub-menu">{items}</ul>'


def with_submenu(hdr, current_path=""):
    """Turn the Services nav item into a dropdown listing every service page."""
    hdr = re.sub(r'<ul class="sub-menu">.*?</ul>', "", hdr, flags=re.S)
    hdr = re.sub(r'<li class="menu-item( current-menu-item current_page_item)?( has-sub)?"><a href="/services/">Services</a></li>',
                 lambda m: f'<li class="menu-item{m.group(1) or ""} has-sub"><a href="/services/">Services</a>{submenu(current_path)}</li>', hdr)
    return hdr


def shell(home_html, current):
    hdr = re.search(r'<header class="header">.*?</header>', home_html, flags=re.S).group(0)
    items = "".join(
        f'<li class="menu-item{" current-menu-item current_page_item" if key == current else ""}"><a href="{href}">{label}</a></li>' for label, href, key in NAV)
    hdr = re.sub(r'(<nav class="nav">)<ul>.*?</ul>', lambda m: m.group(1) + "<ul>" + items + "</ul>", hdr, count=1, flags=re.S)
    hdr = re.sub(r'(<a class="btn__black" href=")[^"]*(" title="Contact FXN Studio")', r"\1/contact/\2", hdr)
    hdr = with_submenu(hdr)
    return hdr, new_footer()


def apply(page_html, home_html, current):
    hdr, ftr = shell(home_html, current)
    page_html = page_html.replace(SUBMENU_STYLE, "")
    hdr = SUBMENU_STYLE + hdr
    page_html = re.sub(r'<header class="header">.*?</header>', lambda m: hdr, page_html, count=1, flags=re.S)
    page_html = re.sub(r'(?:<style>\s*\.fx2\{.*?</style>)?<footer class="footer[^"]*" id="footer">.*?</footer>', lambda m: ftr, page_html, count=1, flags=re.S)
    return page_html


FOOTER_STYLE = """<style>
.fx2{position:relative;background:#0a0c14;color:#c9ced8;font-weight:300;overflow:hidden;padding:0}
.fx2-in{max-width:1366px;margin:0 auto;padding:4.5rem 2rem 2.5rem}
.fx2-grid{display:grid;gap:3rem 2rem;grid-template-columns:minmax(0,1fr)}
.fx2-brand img{display:block;height:2.4rem;width:auto}
.fx2-brand p{margin:1.4rem 0 0;max-width:24rem;line-height:1.6;color:#a2a9b6}
.fx2-mail{display:inline-block;margin-top:1.4rem;color:#fff!important;font-weight:500;border-bottom:1px solid #4a5062;text-decoration:none;padding-bottom:.15rem}
.fx2-mail:hover{border-color:#fff}
.fx2 h2.fx2-h{margin:0 0 1.1rem;font-size:.8rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:#7d8596}
.fx2 ul{list-style:none;margin:0;padding:0;display:grid;gap:.7rem}
.fx2 ul a{color:#e4e7ee;text-decoration:none;font-size:16px;transition:color .2s}
.fx2 ul a:hover{color:#8e86ff}
.fx2-bar{margin-top:3.5rem;padding-top:1.5rem;border-top:1px solid #1e2230;display:flex;flex-wrap:wrap;gap:.75rem 2rem;justify-content:space-between;font-size:.85rem;color:#7d8596}
.fx2-bar a{color:#a2a9b6;text-decoration:underline}
@media (min-width:768px){.fx2-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (min-width:1024px){.fx2-grid{grid-template-columns:minmax(0,2fr) repeat(3,minmax(0,1fr))}}
</style>"""


def new_footer():
    pages = [("Home", "/"), ("About", "/about-us/"), ("Services", "/services/"), ("Portfolio", "/portfolio/"), ("Contact", "/contact/")]
    svc = [("Website design", "/services/web-design/"), ("Custom software", "/services/custom-software/"), ("eCommerce", "/services/ecommerce/"), ("Open-source platforms", "/services/open-source-platforms/"), ("AI integration", "/services/ai-integration/"), ("SEO and growth", "/services/seo-growth/")]
    li = lambda items: "".join(f'<li><a href="{h}">{t}</a></li>' for t, h in items)
    return (FOOTER_STYLE + '<footer class="footer fx2" id="footer"><div class="fx2-in"><div class="fx2-grid">'
            '<div class="fx2-brand"><img src="/img/fxn/logo-light.svg" alt="FXN Studio"><p>FXN Studio is a digital studio established in Australia. We design, build and launch websites, software, e-commerce platforms and AI integrations for clients worldwide.</p>'
            '<a class="fx2-mail" href="mailto:hello@fxnstudio.com">hello@fxnstudio.com</a></div>'
            f'<div><h2 class="fx2-h">Pages</h2><ul>{li(pages)}</ul></div>'
            f'<div><h2 class="fx2-h">Services</h2><ul>{li(svc)}</ul></div>'
            '<div><h2 class="fx2-h">Studio</h2><ul><li><span style="color:#e4e7ee">Perth, Australia</span></li><li><span style="color:#a2a9b6">Working with clients worldwide</span></li>'
            '<li><a href="https://fxnstudio.com/privacy-policy/" target="_blank" rel="noopener">Privacy policy</a></li><li><a href="https://fxnstudio.com/terms-of-services/" target="_blank" rel="noopener">Terms of service</a></li></ul></div></div>'
            '<div class="fx2-bar"><span>&copy;2026 FXN Studio. Established in Australia. Serving clients globally.</span><span>Perth, Western Australia</span></div></div></footer>')
