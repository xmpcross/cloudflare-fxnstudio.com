#!/usr/bin/env python3
"""Build one preview page per service under preview-site/services/<slug>/ from FXN Studio's own service copy."""
import base64, html, json, os, re, sys

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pb_shell
from svc_parse import SERVICES, parse

SRC = open(os.path.join(BASE, "ops/orig/contact.pixelbin.html"), encoding="utf-8").read()
HOME = open(os.path.join(BASE, "preview-site/index.html"), encoding="utf-8").read()
esc = lambda t: html.escape(t, quote=False)

STYLE = """<style>
.svp-wrap{max-width:1366px;margin:0 auto;padding:0 21px}
.svp-crumb{margin:0 0 1.5rem;font-size:.95rem;color:#666}.svp-crumb a{color:#666;text-decoration:none}.svp-crumb a:hover{color:#111}
.svp-h1{margin:0;font-size:3rem;line-height:1.05;font-weight:700;letter-spacing:-.03em!important;color:#0f0f0f;max-width:20ch}
.svp-lead{margin:1.5rem 0 0;max-width:46rem;font-size:1.2rem;line-height:1.55;color:#333}
.svp-actions{display:flex;flex-wrap:wrap;gap:.75rem;margin-top:2rem}
.svp-tabs{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:3rem;padding-top:1.75rem;border-top:1px solid #d6d6d6}
.svp-tabs a{border:1px solid #d9d9d9;background:#f7f7f7;color:#222;border-radius:6px;padding:.75rem 1.05rem;font-size:.95rem;line-height:1;text-decoration:none}
.svp-tabs a:hover{border-color:#999}.svp-tabs a.on{background:#1a1a1a;color:#fff;border-color:#1a1a1a}
.svp-sec{display:grid;gap:1.25rem 4rem;padding:3.25rem 0;border-top:1px solid #d6d6d6}
.svp-sec h2{margin:0;font-size:1.7rem;line-height:1.15;font-weight:600;color:#0f0f0f}
.svp-num{display:block;margin-bottom:.75rem;font-size:.85rem;color:#6b6b6b;letter-spacing:.06em}
.svp-body p{margin:0 0 1rem;font-size:1.08rem;line-height:1.65;color:#444}.svp-body p:last-child{margin-bottom:0}
.svp-list{list-style:none;margin:1.25rem 0 0;padding:0;display:grid;gap:.75rem 2rem;grid-template-columns:minmax(0,1fr)}
.svp-list li{position:relative;padding:.85rem 1rem .85rem 2.6rem;background:#fff;border:1px solid #e4e4e4;border-radius:8px;color:#222;font-size:1rem;line-height:1.35}
.svp-list li:before{content:"";position:absolute;left:1rem;top:50%;width:.9rem;height:.9rem;margin-top:-.45rem;border-radius:50%;background:#e8e6ff url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%234f46e5' stroke-width='4' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m5 12.5 4.5 4.5L19 7.5'/%3E%3C/svg%3E") center/70% no-repeat}
.svp-cta{margin:3rem 0 5rem;padding:3rem;border:1px solid #d0d0d0;border-radius:12px;background:linear-gradient(135deg,#eef1ff,#f6efff 60%,#e9f8f4)}
.svp-cta h2{margin:0;font-size:2rem;line-height:1.15;font-weight:600;max-width:24ch;color:#0f0f0f}
.svp-cta p{margin:.9rem 0 0;color:#444;max-width:34rem}
.svp-cta .btn__black{margin-top:1.6rem}
@media (min-width:900px){.svp-sec{grid-template-columns:minmax(0,1fr) minmax(0,1.6fr)}.svp-list{grid-template-columns:repeat(2,minmax(0,1fr))}.svp-h1{font-size:3.4rem}}
@media (min-width:1366px){.svp-h1{font-size:3.6rem}}
</style>"""


def build(slug, src, label):
    blocks = parse(src)
    cta_i = next(k for k, (t, _) in enumerate(blocks) if t == "a")
    cta_head, cta_btn = blocks[cta_i - 1][1], blocks[cta_i][1]
    blocks = blocks[: cta_i - 1]
    title = blocks[0][1]
    k = 1
    lead = []
    while k < len(blocks) and blocks[k][0] == "p":
        lead.append(blocks[k][1]); k += 1
    secs = []
    for t, x in blocks[k:]:
        if t == "h2": secs.append([x, [], []])
        elif secs and t == "p": secs[-1][1].append(x)
        elif secs and t == "li": secs[-1][2].append(x)
    parts, n = [], 0
    for head, paras, items in secs:
        if not items: n += 1
        tag = f'<span class="svp-num">{n:02d}</span>' if (not items and n) else ""
        body = "".join(f"<p>{esc(p)}</p>" for p in paras)
        if items: body += '<ul class="svp-list">' + "".join(f"<li>{esc(i)}</li>" for i in items) + "</ul>"
        parts.append(f'<div class="svp-sec"><div>{tag}<h2>{esc(head)}</h2></div><div class="svp-body">{body}</div></div>')
    tabs = "".join(f'<a href="/services/{s}/"{" class=\"on\"" if s == slug else ""}>{l}</a>' for s, _, l in SERVICES)
    desc = lead[0] if lead else title
    main = (STYLE + '<main role="main"><section class="page__heading"><div class="svp-wrap">'
            f'<p class="svp-crumb"><a href="/services/">Services</a> / {esc(label)}</p><h1 class="svp-h1">{esc(title)}</h1>'
            + "".join(f'<p class="svp-lead">{esc(p)}</p>' for p in lead[:1])
            + '<div class="svp-actions"><a class="btn__black" href="/contact/"><span>Get in touch</span></a></div>'
            f'<nav class="svp-tabs" aria-label="Services">{tabs}</nav></div></section>'
            f'<section class="section padded" style="padding-top:0"><div class="svp-wrap">{"".join(parts)}'
            f'<div class="svp-cta"><h2>{esc(cta_head)}</h2><p>Tell us what you are planning and we will get back to you with the best way forward.</p>'
            f'<a class="btn__black" href="/contact/"><span>{esc(cta_btn)}</span></a></div></div></section></main>')
    h = SRC
    t = f"{title} | FXN Studio"
    h = re.sub(r"<title>.*?</title>", f"<title>{esc(t)}</title>", h, count=1, flags=re.S)
    for pat in (r'(<meta name="description" content=")[^"]*(")', r'(<meta property="og:description" content=")[^"]*(")', r'(<meta name="twitter:description" content=")[^"]*(")'):
        h = re.sub(pat, lambda m: m.group(1) + html.escape(desc, quote=True) + m.group(2), h)
    for pat in (r'(<meta property="og:title" content=")[^"]*(")', r'(<meta name="twitter:title" content=")[^"]*(")'):
        h = re.sub(pat, lambda m: m.group(1) + html.escape(t, quote=True) + m.group(2), h)
    h = re.sub(r'(<meta property="og:site_name" content=")[^"]*(")', r"\1FXN Studio\2", h)
    h = h.replace('<meta property="og:locale" content="en_GB" />', '<meta property="og:locale" content="en_AU" />')
    url = f"https://fxnstudio.com/services/{slug}/"
    h = re.sub(r'<link rel="canonical" href="[^"]*" />', f'<link rel="canonical" href="{url}" />', h)
    h = re.sub(r'<meta property="og:url" content="[^"]*" />', f'<meta property="og:url" content="{url}" />', h)
    h = re.sub(r'<meta property="og:updated_time"[^>]*>', "", h)
    h = re.sub(r'<meta (?:property="(?:og:image[^"]*|article:[^"]*)"|name="twitter:(?:image|label|data)[^"]*")[^>]*>', "", h)
    ld = {"@context": "https://schema.org", "@type": "Service", "name": title, "url": url, "description": desc,
          "provider": {"@type": "Organization", "name": "FXN Studio", "url": "https://fxnstudio.com/"}}
    h = re.sub(r'<script type="application/ld\+json"[^>]*>.*?</script>', lambda m: '<script type="application/ld+json">' + json.dumps(ld) + "</script>", h, count=1, flags=re.S)
    h = re.sub(r'<script[^>]*google-recaptcha[^>]*>\s*</script>', "", h)
    h = re.sub(r'<script[^>]*src="data:text/javascript;base64,[^"]+"[^>]*>(?:</script>)?',
               lambda m: "" if re.search(r"UA-|gtag", base64.b64decode(re.search(r"base64,([^\"]+)", m.group(0)).group(1)).decode("utf-8", "ignore")) else m.group(0), h)
    h = pb_shell.apply(h, HOME, "services")
    h = re.sub(r"<main role=\"main\">.*?</main>", lambda m: main, h, count=1, flags=re.S)
    out = os.path.join(BASE, "preview-site/services", slug, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(h)
    return title, len(secs)


for slug, src, label in SERVICES:
    print(slug, build(slug, src, label))
