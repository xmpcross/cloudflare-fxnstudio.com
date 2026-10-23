#!/usr/bin/env python3
"""Build preview-site/services/index.html in the Pixelbin layout from FXN Studio's services content."""
import base64, html, json, os, re, sys

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pb_shell

SRC = open(os.path.join(BASE, "ops/orig/contact.pixelbin.html"), encoding="utf-8").read()
HOME = open(os.path.join(BASE, "preview-site/index.html"), encoding="utf-8").read()
OUT = os.path.join(BASE, "preview-site/services/index.html")

# ---- services content, read from FXN Studio's own services page -------------
live = open(os.path.join(BASE, "dist/services/index.html"), encoding="utf-8").read()
live = re.sub(r"<(script|style|svg)\b.*?</\1>", "", live, flags=re.S)
toks = [html.unescape(t).strip() for t in re.findall(r">([^<>]+)<", live) if t.strip()]
a = toks.index("Digital Services for Websites, Software, Automation and AI")
intro = toks[a + 1]
services, k = [], a + 4
while k < len(toks) and toks[k] != "Need help choosing the right service?":
    title, desc = toks[k], toks[k + 1]
    assert toks[k + 2] == "Service includes:", toks[k:k + 3]
    k += 3
    items = []
    while k < len(toks) and not toks[k].startswith("Explore ") and toks[k] != "Need help choosing the right service?" and not (len(toks) > k + 2 and toks[k + 2] == "Service includes:"):
        items.append(toks[k]); k += 1
    if k < len(toks) and toks[k].startswith("Explore "):
        k += 1
    services.append((title, desc, items))
print(len(services), "services parsed:", [s[0] for s in services])

h = SRC
TITLE = "Services | Web Development, AI Integration and Custom Software | FXN Studio"
DESC = "Website design and development, custom software, AI integration, e-commerce, open-source platforms, SEO and ongoing support from FXN Studio in Perth, Australia."
h = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", h, count=1, flags=re.S)
for pat in (r'(<meta name="description" content=")[^"]*(")', r'(<meta property="og:description" content=")[^"]*(")', r'(<meta name="twitter:description" content=")[^"]*(")'):
    h = re.sub(pat, rf"\g<1>{DESC}\2", h)
for pat in (r'(<meta property="og:title" content=")[^"]*(")', r'(<meta name="twitter:title" content=")[^"]*(")'):
    h = re.sub(pat, rf"\g<1>{TITLE}\2", h)
h = re.sub(r'(<meta property="og:site_name" content=")[^"]*(")', r"\1FXN Studio\2", h)
h = h.replace('<meta property="og:locale" content="en_GB" />', '<meta property="og:locale" content="en_AU" />')
h = re.sub(r'<link rel="canonical" href="[^"]*" />', '<link rel="canonical" href="https://fxnstudio.com/services/" />', h)
h = re.sub(r'<meta property="og:url" content="[^"]*" />', '<meta property="og:url" content="https://fxnstudio.com/services/" />', h)
h = re.sub(r'<meta property="og:updated_time"[^>]*>', "", h)
h = re.sub(r'<meta (?:property="(?:og:image[^"]*|article:[^"]*)"|name="twitter:(?:image|label|data)[^"]*")[^>]*>', "", h)
ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "FXN Studio services", "url": "https://fxnstudio.com/services/",
      "publisher": {"@type": "Organization", "name": "FXN Studio", "url": "https://fxnstudio.com/"}}
h = re.sub(r'<script type="application/ld\+json"[^>]*>.*?</script>', '<script type="application/ld+json">' + json.dumps(ld) + "</script>", h, count=1, flags=re.S)
h = re.sub(r'<script[^>]*google-recaptcha[^>]*>\s*</script>', "", h)
h = re.sub(r'<script[^>]*src="data:text/javascript;base64,[^"]+"[^>]*>(?:</script>)?',
           lambda m: "" if re.search(r"UA-|gtag", base64.b64decode(re.search(r"base64,([^\"]+)", m.group(0)).group(1)).decode("utf-8", "ignore")) else m.group(0), h)
h = pb_shell.apply(h, HOME, "services")

esc = lambda t: html.escape(t, quote=False)
INTRO = intro.replace(" We help plan, design, build and optimise websites, e-commerce platforms, custom software and AI-enabled systems.", "")
from svc_parse import SERVICES, parse
STYLE = """<style>
.svo-wrap{max-width:1366px;margin:0 auto;padding:0 21px}
@media (min-width:900px){.page__heading{box-sizing:border-box;height:440px;padding-top:0!important;padding-bottom:0!important}.page__heading>.container,.page__heading>.container>.row,.page__heading>.container>.row>.col{height:100%}.page__heading>.container>.row>.col{display:flex;flex-direction:column;justify-content:center}.page__heading .pf-bar{margin-top:3rem;margin-bottom:0;box-sizing:border-box;min-height:96px}}
.pf-eyebrow{margin:0 0 2rem;font-size:1rem;color:#555}
.pf-top{display:grid;grid-template-columns:minmax(0,1fr);gap:1.5rem 3rem;align-items:center}
.pf-title{margin:0;font-size:3rem;font-weight:700;line-height:.95;letter-spacing:-.04em!important;color:#0f0f0f}
.pf-sub{margin:0;max-width:30rem;color:#111;font-size:1.2rem;line-height:1.3}
.pf-bar{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:1rem;margin-top:3.5rem;padding-top:1.75rem;border-top:1px solid #d6d6d6}
.pf-bar .tags{display:flex;flex-wrap:wrap;gap:.4rem;margin:0}
.pf-bar .tag{border-radius:6px!important;padding:.8rem .95rem!important;border:1px solid #d9d9d9!important;background:#f7f7f7!important;color:#222!important;font-size:.92rem;line-height:1;text-decoration:none}
.pf-bar .tag.active{background:#1a1a1a!important;color:#fff!important;border-color:#1a1a1a!important}
.pf-count{color:#555;font-size:.95rem}
@media (min-width:900px){.pf-top{grid-template-columns:minmax(0,1.5fr) minmax(0,1fr)}.pf-title{white-space:nowrap}.pf-sub{justify-self:start;padding-left:2rem}}
.svo-list{list-style:none;margin:3rem 0 0;padding:0;border-top:1px solid #d6d6d6}
.svo-row{border-bottom:1px solid #d6d6d6}
.svo-row>a{display:grid;gap:1rem 3rem;padding:2.25rem 0;text-decoration:none;color:#0f0f0f;transition:padding-left .3s}
.svo-row>a:hover{padding-left:.75rem}
.svo-head{display:flex;align-items:baseline;gap:1.25rem}
.svo-n{font-size:.9rem;color:#6b6b6b;letter-spacing:.06em;min-width:2rem}
.svo-t{margin:0;font-size:1.7rem;line-height:1.15;font-weight:600}
.svo-d{margin:0;color:#444;line-height:1.55;font-size:1.05rem;max-width:36rem}
.svo-tags{display:flex;flex-wrap:wrap;gap:.4rem;list-style:none;margin:.9rem 0 0;padding:0}
.svo-tags li{font-size:.78rem;color:#444;border:1px solid #cfcfcf;border-radius:6px;padding:.3rem .65rem}
.svo-go{display:none;align-self:center;color:#6b6b6b;transition:color .2s,transform .2s}
.svo-row>a:hover .svo-go{color:#4f46e5;transform:translateX(4px)}
.svo-note{margin:2rem 0 0;color:#555;max-width:40rem}
@media (min-width:900px){.svo-row>a{grid-template-columns:minmax(0,1fr) minmax(0,1.5fr) auto}.svo-go{display:block}}
</style>"""
ARROW = '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
rows = ""
for n, (slug, src, label) in enumerate(SERVICES, 1):
    b = parse(src)
    desc = next(x for t, x in b[1:] if t == "p")
    tags = [x for t, x in b if t == "li"][:4]
    chips = "".join(f"<li>{esc(x)}</li>" for x in tags)
    rows += (f'<li class="svo-row"><a href="/services/{slug}/"><div class="svo-head"><span class="svo-n">{n:02d}</span><h2 class="svo-t">{esc(label)}</h2></div>'
             f'<div><p class="svo-d">{esc(desc)}</p><ul class="svo-tags">{chips}</ul></div><span class="svo-go">{ARROW}</span></a></li>')
chips = '<a href="/services/" class="tag active">All</a>' + "".join(f'<a href="/services/{sl}/" class="tag">{lb}</a>' for sl, _, lb in SERVICES)
main = (STYLE + '<main role="main"><section class="page__heading"><div class="container"><div class="row"><div class="col"><p class="pf-eyebrow">Services</p>'
        f'<div class="pf-top"><h1 class="pf-title">What we do.</h1><p class="pf-sub">{esc(INTRO)}</p></div>'
        f'<div class="pf-bar"><div class="tags">{chips}</div><span class="pf-count">{len(SERVICES)} services</span></div></div></div></div></section>'
        f'<section class="section" style="padding-top:0;padding-bottom:80px"><div class="svo-wrap"><ul class="svo-list">{rows}</ul>'
        '<p class="svo-note">We also provide ongoing support and maintenance after launch, covering website updates, bug fixes, performance monitoring, security updates and technical consulting.</p></div></section>'
        '<section class="section section__conversion"><div class="gradient blobs pos-2"><div class="purple"></div><div class="blue"></div></div><div class="container pt-4 pb-4"><div class="inner p-5"><div class="row"><div class="col-md-8 pe-lg-5">'
        '<strong class="pretitle">Need help choosing the right service?</strong><h2 class="h3 title bold">Talk to FXN Studio</h2>'
        '<p class="subtitle">Our services are available to Australian and global clients, with flexible solutions for businesses at every stage of growth.</p>'
        '<a class="btn__black large" href="/contact/" title="Get in touch"><span>Get in touch</span></a></div><div class="col-md-4 image"></div></div></div></div></section></main>')
h = re.sub(r"<main role=\"main\">.*?</main>", lambda m: main, h, count=1, flags=re.S)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write(h)
print("services written; leftover:", [w for w in ("Pixelbin", "pixelbin", "Essex", "UA-7211") if w in h])
