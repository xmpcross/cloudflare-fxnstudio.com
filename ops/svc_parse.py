"""Parse FXN Studio's existing service pages (dist/services/*) into ordered content blocks."""
import html, os, re
from html.parser import HTMLParser

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SERVICES = [  # slug, source dir, label used in nav/footer
    ("web-design", "web-design", "Website design"),
    ("custom-software", "web-development", "Custom software"),
    ("ecommerce", "ecommerce-development", "eCommerce"),
    ("open-source-platforms", "open-source-platform-solutions", "Open-source platforms"),
    ("ai-integration", "ai-integrations", "AI integration"),
    ("seo-growth", "seo-growth", "SEO and growth"),
]


class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.cur = None; self.buf = []; self.blocks = []; self.skip = 0; self.started = False
    def handle_starttag(self, t, a):
        if t in ("script", "style", "svg", "nav", "header", "footer", "button", "form"): self.skip += 1
        if t in ("h1", "h2", "h3", "h4", "p", "li", "a") and not self.skip: self.cur = t; self.buf = []
    def handle_endtag(self, t):
        if t in ("script", "style", "svg", "nav", "header", "footer", "button", "form") and self.skip: self.skip -= 1
        if t == self.cur and not self.skip:
            txt = html.unescape(re.sub(r"\s+", " ", "".join(self.buf))).strip()
            if txt: self.blocks.append((t, txt))
            self.cur = None
    def handle_data(self, d):
        if self.cur: self.buf.append(d)


def parse(src):
    h = open(os.path.join(BASE, "dist/services", src, "index.html"), encoding="utf-8").read()
    p = P(); p.feed(h)
    b = p.blocks
    i = next(k for k, (t, _) in enumerate(b) if t == "h1")
    out = b[i:]
    end = next((k for k, (t, x) in enumerate(out) if x.startswith("FXN Studio is an Australia-based")), len(out))
    return out[:end]


if __name__ == "__main__":
    for slug, src, label in SERVICES:
        print("=====", slug, label)
        for t, x in parse(src): print(f"  {t}: {x[:110]}")
