#!/usr/bin/env python3
"""Build preview-site/about-us/index.html in the Pixelbin layout from FXN Studio's About content."""
import base64, html, json, os, re, sys

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

esc = lambda t: html.escape(t, quote=False)
pillars = [
 ("Strategy first, technology second", "Every successful digital project starts with clear thinking. Before design or development begins, we look at your audience, business model, content needs, workflows, growth plans and technical requirements. This allows us to recommend the right solution rather than forcing every project into the same template."),
 ("Built with modern, flexible technology", "We believe businesses should have digital systems that are fast, secure, maintainable and adaptable. That is why we use modern open-source frameworks, reliable platforms, API-first architecture and AI-ready workflows where they add real value."),
 ("Clear communication from start to finish", "We keep projects organised and transparent, with clear milestones, practical recommendations and ongoing collaboration. Our goal is to make the process feel focused, productive and easy to understand."),
]
checks = ["Established in Australia with a global delivery mindset", "Services available to clients of any size and location", "Strong focus on SEO, performance and user experience",
          "Expertise across design, development, automation and AI", "Flexible use of open-source technologies and modern platforms", "Practical solutions built around real business needs"]
ARROW = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
rows = "".join(f'<li class="ab-row"><span class="ab-n">{n:02d}</span><h3>{esc(t)}</h3><p>{esc(d)}</p></li>' for n, (t, d) in enumerate(pillars, 1))
chk = "".join(f"<li>{esc(c)}</li>" for c in checks)
chips = "".join(f'<a href="#{i}" class="tag{" active" if k == 0 else ""}">{l}</a>' for k, (i, l) in enumerate([("studio", "Studio"), ("approach", "How we work"), ("difference", "What makes us different"), ("mission", "Mission")]))
STYLE = """<style>
@media (min-width:900px){.page__heading{box-sizing:border-box;height:440px;padding-top:0!important;padding-bottom:0!important}.page__heading>.container,.page__heading>.container>.row,.page__heading>.container>.row>.col{height:100%}.page__heading>.container>.row>.col{display:flex;flex-direction:column;justify-content:center}.page__heading .pf-bar{margin-top:3rem;margin-bottom:0;box-sizing:border-box;min-height:96px}}
.pf-top{display:grid;grid-template-columns:minmax(0,1fr);gap:1.5rem 3rem;align-items:center}
.pf-title{margin:0;font-size:3rem;font-weight:700;line-height:.95;letter-spacing:-.04em!important;color:#0f0f0f}
.pf-sub{margin:0;max-width:30rem;color:#111;font-size:1.2rem;line-height:1.3}
.pf-bar{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:1rem;margin-top:3.5rem;padding-top:1.75rem;border-top:1px solid #d6d6d6}
.pf-bar .tags{display:flex;flex-wrap:wrap;gap:.4rem;margin:0}
.pf-bar .tag{border-radius:6px!important;padding:.8rem .95rem!important;border:1px solid #d9d9d9!important;background:#f7f7f7!important;color:#222!important;font-size:.92rem;line-height:1;text-decoration:none}
.pf-bar .tag.active{background:#1a1a1a!important;color:#fff!important;border-color:#1a1a1a!important}
.pf-count{color:#555;font-size:.95rem}
@media (min-width:900px){.pf-top{grid-template-columns:minmax(0,1.5fr) minmax(0,1fr)}.pf-title{white-space:nowrap}.pf-sub{justify-self:start;padding-left:2rem}}
.ab-wrap{max-width:1400px;margin:0 auto;padding:0 21px}
.ab-intro{display:grid;gap:2.5rem 5rem;align-items:center;padding:4rem 0}
.ab-photo{position:relative;margin:0}
.ab-photo img{display:block;width:100%;aspect-ratio:5/4;object-fit:cover;border-radius:12px}
.ab-badge{position:absolute;left:-1rem;bottom:2rem;background:#fff;border-radius:12px;padding:.9rem 1.2rem;box-shadow:0 14px 34px -14px rgb(0 0 0/.35)}
.ab-badge strong{display:block;font-size:1.35rem;line-height:1;color:#0f0f0f}.ab-badge span{display:block;margin-top:.3rem;font-size:.8rem;color:#555}
.ab-eyebrow{margin:0 0 1rem;font-size:.85rem;font-weight:500;letter-spacing:.08em;text-transform:uppercase;color:#6b6b6b}
.ab-intro h2,.ab-head h2{margin:0;font-size:2.2rem;line-height:1.1;font-weight:600;color:#0f0f0f;letter-spacing:-.02em;max-width:18ch}
.ab-intro p{margin:1.1rem 0 0;color:#444;font-size:1.08rem;line-height:1.65;max-width:36rem}
.ab-intro h3{margin:2rem 0 0;font-size:1.25rem;font-weight:600;color:#0f0f0f}
.ab-head{padding:3rem 0 2rem}
.ab-list{list-style:none;margin:0;padding:0;border-top:1px solid #d6d6d6}
.ab-row{display:grid;gap:.75rem 3rem;padding:2.25rem 0;border-bottom:1px solid #d6d6d6}
.ab-n{font-size:.9rem;color:#6b6b6b;letter-spacing:.06em}
.ab-row h3{margin:0;font-size:1.5rem;line-height:1.2;font-weight:600;color:#0f0f0f}
.ab-row p{margin:0;color:#444;line-height:1.65;font-size:1.05rem;max-width:40rem}
.ab-checks{list-style:none;margin:0;padding:0;display:grid;gap:.75rem 1.25rem;grid-template-columns:minmax(0,1fr)}
.ab-checks li{position:relative;padding:1rem 1rem 1rem 3rem;background:#fff;border:1px solid #e4e4e4;border-radius:8px;color:#222;line-height:1.35}
.ab-checks li:before{content:"";position:absolute;left:1rem;top:50%;width:1.2rem;height:1.2rem;margin-top:-.6rem;border-radius:50%;background:#e8e6ff url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%234f46e5' stroke-width='4' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m5 12.5 4.5 4.5L19 7.5'/%3E%3C/svg%3E") center/70% no-repeat}
.ab-mission{margin:4rem 0 5rem;padding:3.5rem 3rem;border-radius:12px;color:#fff;background:linear-gradient(135deg,#12142b,#2a2470 60%,#0f4c4a)}
.ab-mission .ab-eyebrow{color:#a9b0e6}
.ab-mission h2{margin:0;color:#fff;font-size:2.2rem;line-height:1.1;font-weight:600;max-width:20ch}
.ab-mission p{margin:1.2rem 0 0;color:#cfd3f2;font-size:1.1rem;line-height:1.6;max-width:38rem}
.ab-mission .btn__outline-white{margin-top:1.75rem}
@media (min-width:900px){.ab-intro{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}.ab-row{grid-template-columns:3rem minmax(0,1fr) minmax(0,1.5fr);align-items:start}.ab-checks{grid-template-columns:repeat(2,minmax(0,1fr))}.ab-mission{padding:4.5rem 4rem}}
</style>"""
main = (STYLE + '<main role="main"><section class="page__heading"><div class="container"><div class="row"><div class="col">'
        '<div class="pf-top"><h1 class="pf-title">About us.</h1><p class="pf-sub">FXN Studio is a modern digital studio established in Australia and built to support clients anywhere in the world.</p></div>'
        f'<div class="pf-bar"><div class="tags">{chips}</div><span class="pf-count">Perth, Australia</span></div></div></div></div></section>'
        '<section class="section" id="studio" style="padding-top:0;padding-bottom:0"><div class="ab-wrap"><div class="ab-intro">'
        '<figure class="ab-photo"><img src="/img/fxn/about.jpg" alt="Working on a laptop" loading="lazy"><figcaption class="ab-badge"><strong>Perth</strong><span>Australia-based, delivering worldwide</span></figcaption></figure>'
        '<div><p class="ab-eyebrow">Our studio</p><h2>Australia-based digital expertise for global businesses</h2>'
        '<p>Our work combines creative thinking, technical skill and business understanding. We do not just build websites or software; we help create digital systems that make brands easier to find, easier to trust and easier to work with.</p>'
        '<h3>Who we work with</h3>'
        '<p>We work with businesses of all sizes, including startups, local companies, growing brands, professional service firms, e-commerce businesses, agencies and global organisations.</p>'
        '<p>Whether you need a simple website, a complex platform, a custom internal system or AI-powered automation, our process adapts to your goals, budget and stage of growth.</p></div></div></div></section>'
        f'<section class="section" id="approach" style="padding-top:0;padding-bottom:0"><div class="ab-wrap"><div class="ab-head"><p class="ab-eyebrow">How we work</p><h2>Clear thinking, modern technology, open communication</h2></div><ul class="ab-list">{rows}</ul></div></section>'
        f'<section class="section" id="difference" style="padding-top:0;padding-bottom:80px"><div class="ab-wrap"><div class="ab-head"><p class="ab-eyebrow">What makes us different</p><h2>Practical solutions built around real business needs</h2></div><ul class="ab-checks">{chk}</ul></div></section>'
        '<section class="section" id="mission" style="padding-top:0;padding-bottom:0"><div class="ab-wrap"><div class="ab-mission"><p class="ab-eyebrow">Mission</p><h2>Digital technology with clarity and confidence</h2>'
        '<p>We create websites, platforms and intelligent systems that support growth, improve operations and make digital experiences better for customers and teams.</p>'
        '<a href="/contact/" class="btn__outline-white"><span>Get in touch</span></a></div></div></section></main>')
h = re.sub(r"<main role=\"main\">.*?</main>", lambda m: main, h, count=1, flags=re.S)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write(h)
print("about written; leftover:", [w for w in ("Pixelbin", "pixelbin", "Essex", "UA-7211") if w in h])
