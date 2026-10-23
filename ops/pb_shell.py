"""Shared header and footer for the Pixelbin-layout pages, taken from the home page and given one nav."""
import re

NAV = [("Home", "/", "home"), ("About", "/about-us/", "about"), ("Services", "/services/", "services"), ("Portfolio", "/portfolio/", "portfolio")]
FOOT = NAV + [("Contact", "/contact/", "contact")]


def shell(home_html, current):
    hdr = re.search(r'<header class="header">.*?</header>', home_html, flags=re.S).group(0)
    ftr = re.search(r'<footer class="footer" id="footer">.*?</footer>', home_html, flags=re.S).group(0)
    items = "".join(
        f'<li class="menu-item{" current-menu-item current_page_item" if key == current else ""}"><a href="{href}">{label}</a></li>' for label, href, key in NAV)
    hdr = re.sub(r'(<nav class="nav">)<ul>.*?</ul>', lambda m: m.group(1) + "<ul>" + items + "</ul>", hdr, count=1, flags=re.S)
    hdr = re.sub(r'(<a class="btn__black" href=")[^"]*(" title="Contact FXN Studio")', r"\1/contact/\2", hdr)
    foot = "".join(f'<li><a href="{href}">{label}</a></li>' for label, href, key in FOOT)
    ftr = re.sub(r'(<div class="col-2 offset-4 text-right">)<ul>.*?</ul>', lambda m: m.group(1) + "<ul>" + foot + "</ul>", ftr, count=1, flags=re.S)
    return hdr, ftr


def apply(page_html, home_html, current):
    hdr, ftr = shell(home_html, current)
    page_html = re.sub(r'<header class="header">.*?</header>', lambda m: hdr, page_html, count=1, flags=re.S)
    page_html = re.sub(r'<footer class="footer" id="footer">.*?</footer>', lambda m: ftr, page_html, count=1, flags=re.S)
    return page_html
