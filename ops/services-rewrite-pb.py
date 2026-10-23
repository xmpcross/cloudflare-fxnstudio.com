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
rows = ""
for n, (title, desc, items) in enumerate(services, 1):
    chips = "".join(f"<li>{esc(i)}</li>" for i in items[:4])
    rows += (f'<div class="section__services-item"><div class="section__services-toggle"><div class="container"><div class="start"> {n:02d}</div><div class="middle"><h2 class="h3">{esc(title)}</h2><ul class="tags">{chips}</ul></div><div class="end"><div class="arrow"></div></div></div></div>'
             f'<div class="container section__services-accordion"><div class="inner"><div class="row align-items-center"><div class="col-8"><h3 class="pretitle">{esc(title)}</h3><p class="title h3">Service includes</p>'
             f'<p>{esc(desc)}</p><p>{" &middot; ".join(esc(i) for i in items)}</p><a href="/contact/" class="btn__outline-white mt-4"><span>Discuss this service</span></a></div><div class="col-5 offset-1 hide"></div></div></div></div></div>')
main = ('<main role="main"><section class="page__heading"><div class="container"><div class="row"><div class="col-lg-8"><h1 class="h1">Services</h1>'
        f'<p class="subtitle h4">{esc(intro)}</p></div></div></div></section>'
        f'<section class="section section__services raise-1" id="services-list" style="padding-top:2rem">{rows}</section>'
        '<section class="section section__conversion"><div class="gradient blobs pos-2"><div class="purple"></div><div class="blue"></div></div><div class="container pt-4 pb-4"><div class="inner p-5"><div class="row"><div class="col-md-8 pe-lg-5">'
        '<strong class="pretitle">Need help choosing the right service?</strong><h2 class="h3 title bold">Talk to FXN Studio</h2>'
        '<p class="subtitle">Our services are available to Australian and global clients, with flexible solutions for businesses at every stage of growth.</p>'
        '<a class="btn__black large" href="/contact/" title="Get in touch"><span>Get in touch</span></a></div><div class="col-md-4 image"></div></div></div></div></section></main>')
h = re.sub(r"<main role=\"main\">.*?</main>", lambda m: main, h, count=1, flags=re.S)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write(h)
print("services written; leftover:", [w for w in ("Pixelbin", "pixelbin", "Essex", "UA-7211") if w in h])
