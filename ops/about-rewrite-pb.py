#!/usr/bin/env python3
"""Build preview-site/about-us/index.html in the Pixelbin layout from FXN Studio's About content."""
import json, os, re, sys, base64

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pb_shell

SRC = open(os.path.join(BASE, "ops/orig/contact.pixelbin.html"), encoding="utf-8").read()  # page skeleton (head, scripts)
HOME = open(os.path.join(BASE, "preview-site/index.html"), encoding="utf-8").read()
OUT = os.path.join(BASE, "preview-site/about-us/index.html")
h = SRC
TITLE = "About FXN Studio | Australia-Based Digital Studio for Global Clients"
DESC = "FXN Studio is a modern digital studio established in Australia and built to support clients anywhere in the world, from startups to global organisations."
h = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", h, count=1, flags=re.S)
for pat in (r'(<meta name="description" content=")[^"]*(")', r'(<meta property="og:description" content=")[^"]*(")', r'(<meta name="twitter:description" content=")[^"]*(")'):
    h = re.sub(pat, rf"\g<1>{DESC}\2", h)
for pat in (r'(<meta property="og:title" content=")[^"]*(")', r'(<meta name="twitter:title" content=")[^"]*(")'):
    h = re.sub(pat, rf"\g<1>{TITLE}\2", h)
h = re.sub(r'(<meta property="og:site_name" content=")[^"]*(")', r"\1FXN Studio\2", h)
h = h.replace('<meta property="og:locale" content="en_GB" />', '<meta property="og:locale" content="en_AU" />')
h = re.sub(r'<link rel="canonical" href="[^"]*" />', '<link rel="canonical" href="https://fxnstudio.com/about-us/" />', h)
h = re.sub(r'<meta property="og:url" content="[^"]*" />', '<meta property="og:url" content="https://fxnstudio.com/about-us/" />', h)
h = re.sub(r'<meta property="og:updated_time"[^>]*>', "", h)
h = re.sub(r'<meta (?:property="(?:og:image[^"]*|article:[^"]*)"|name="twitter:(?:image|label|data)[^"]*")[^>]*>', "", h)
ld = {"@context": "https://schema.org", "@type": "AboutPage", "name": "About FXN Studio", "url": "https://fxnstudio.com/about-us/",
      "about": {"@type": "Organization", "name": "FXN Studio", "url": "https://fxnstudio.com/", "address": {"@type": "PostalAddress", "addressLocality": "Perth", "addressCountry": "AU"}}}
h = re.sub(r'<script type="application/ld\+json"[^>]*>.*?</script>', '<script type="application/ld+json">' + json.dumps(ld) + "</script>", h, count=1, flags=re.S)
h = re.sub(r'<script[^>]*google-recaptcha[^>]*>\s*</script>', "", h)
h = re.sub(r'<script[^>]*src="data:text/javascript;base64,[^"]+"[^>]*>(?:</script>)?',
           lambda m: "" if re.search(r"UA-|gtag", base64.b64decode(re.search(r"base64,([^\"]+)", m.group(0)).group(1)).decode("utf-8", "ignore")) else m.group(0), h)
h = pb_shell.apply(h, HOME, "about")

pillars = [
 ("Strategy first, technology second", "Every successful digital project starts with clear thinking. Before design or development begins, we look at your audience, business model, content needs, workflows, growth plans and technical requirements. This allows us to recommend the right solution rather than forcing every project into the same template."),
 ("Built with modern, flexible technology", "We believe businesses should have digital systems that are fast, secure, maintainable and adaptable. That is why we use modern open-source frameworks, reliable platforms, API-first architecture and AI-ready workflows where they add real value."),
 ("Clear communication from start to finish", "We keep projects organised and transparent, with clear milestones, practical recommendations and ongoing collaboration. Our goal is to make the process feel focused, productive and easy to understand."),
]
pill = "".join(f'<div class="col-md-4"><h3 class="h4 bold">{t}</h3><p>{d}</p></div>' for t, d in pillars)
checks = ["Established in Australia with a global delivery mindset", "Services available to clients of any size and location", "Strong focus on SEO, performance and user experience",
          "Expertise across design, development, automation and AI", "Flexible use of open-source technologies and modern platforms", "Practical solutions built around real business needs"]
chk = "".join(f"<li>{c}</li>" for c in checks)
main = (
 '<main role="main"><section class="page__heading"><div class="container"><div class="row"><div class="col-lg-8"><h1 class="h1">About FXN Studio</h1>'
 '<p class="subtitle h4">FXN Studio is a modern digital studio established in Australia and built to support clients anywhere in the world. We help businesses plan, design and develop digital products that are practical, scalable and ready for long-term growth.</p></div></div></div></section>'
 '<section class="section section__first padded"><div class="container"><div class="row align-items-center"><div class="col-md-7 pe-md-5"><strong class="pretitle">Perth, Australia</strong>'
 '<h2 class="mt-0 h3 bold">Australia-based digital expertise for global businesses</h2>'
 '<p>Our work combines creative thinking, technical skill and business understanding. We do not just build websites or software; we help create digital systems that make brands easier to find, easier to trust and easier to work with.</p>'
 '<h3 class="h4 bold" style="margin-top:2rem">Who we work with</h3>'
 '<p>We work with businesses of all sizes, including startups, local companies, growing brands, professional service firms, e-commerce businesses, agencies and global organisations.</p>'
 '<p>Whether you need a simple website, a complex platform, a custom internal system or AI-powered automation, our process adapts to your goals, budget and stage of growth.</p></div>'
 '<div class="col-md-5"><img src="/img/fxn/about.jpg" alt="Working on a laptop" style="width:100%;height:auto;border-radius:8px;display:block"></div></div></div></section>'
 f'<section class="section padded"><div class="container"><div class="row" style="row-gap:2rem">{pill}</div></div></section>'
 '<section class="section padded"><div class="container"><div class="row align-items-center"><div class="col-md-7 pe-md-5"><strong class="pretitle">What makes us different</strong>'
 f'<h2 class="mt-0 h3 bold">Practical solutions built around real business needs</h2><ul class="list check">{chk}</ul></div></div></div></section>'
 '<section class="section section__conversion"><div class="gradient blobs pos-2"><div class="purple"></div><div class="blue"></div></div><div class="container pt-4 pb-4"><div class="inner p-5"><div class="row"><div class="col-md-8 pe-lg-5">'
 '<strong class="pretitle">Mission</strong><h2 class="h3 title bold">Digital technology with clarity and confidence</h2>'
 '<p class="subtitle">We create websites, platforms and intelligent systems that support growth, improve operations and make digital experiences better for customers and teams.</p>'
 '<a class="btn__black large" href="/contact/" title="Get in touch"><span>Get in touch</span></a></div><div class="col-md-4 image"></div></div></div></div></section></main>')
h = re.sub(r"<main role=\"main\">.*?</main>", lambda m: main, h, count=1, flags=re.S)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write(h)
print("about written; leftover:", [w for w in ("Pixelbin", "pixelbin", "Essex", "UA-7211") if w in h])
