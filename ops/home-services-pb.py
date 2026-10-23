#!/usr/bin/env python3
"""Redesign the home page 'Digital services' section: sticky intro on the left, expanding service list on the right (idempotent; run after home-rewrite-pb.py)."""
import os, re

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "preview-site", "index.html")
h = open(P, encoding="utf-8").read()

ARROW = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M8 7h9v9"/></svg>'
S = [
 ("Website design", "/services/web-design/", "Modern websites that communicate clearly, rank better in search and turn visitors into enquiries, bookings or sales.", ["UX and UI", "Responsive", "SEO-ready"]),
 ("Custom software", "/services/custom-software/", "Internal tools, client portals, web applications, booking systems and APIs built around how your business works.", ["Web apps", "Portals", "APIs"]),
 ("eCommerce", "/services/ecommerce/", "Shopify, WooCommerce and custom stores with clear product journeys, solid performance and conversion-focused checkout.", ["Shopify", "WooCommerce", "Checkout"]),
 ("Open-source platforms", "/services/open-source-platforms/", "Flexible, maintainable solutions on modern open-source frameworks and trusted platforms, with room to scale and less lock-in.", ["Next.js", "Headless CMS", "WordPress"]),
 ("AI integration", "/services/ai-integration/", "Practical AI chat agents, document processing and workflow automation that solve a real business problem and are easy to manage.", ["Chat agents", "Automation", "Documents"]),
 ("SEO and growth", "/services/seo-growth/", "Technical SEO, performance optimisation and analytics so your website is easier for search engines to understand and for people to use.", ["Technical SEO", "Speed", "Analytics"]),
]
rows = "".join(
    f'<li class="ds-row{" is-open" if i == 1 else ""}"><a href="{u}"><span class="ds-n">{i:02d}</span><span class="ds-main"><span class="ds-t">{t}</span>'
    f'<span class="ds-more"><span class="ds-d">{d}</span><span class="ds-tags">{"".join(f"<i>{x}</i>" for x in tags)}</span></span></span><span class="ds-go">{ARROW}</span></a></li>'
    for i, (t, u, d, tags) in enumerate(S, 1))

style = """<style>
.ds{position:relative;z-index:1;display:grid;gap:3rem 5rem}
.ds-intro{align-self:start}
.ds-eyebrow{margin:0 0 1.25rem;font-size:.85rem;font-weight:500;letter-spacing:.08em;text-transform:uppercase;color:#9aa0a6}
.ds-h{margin:0;color:#fff;font-size:clamp(2.2rem,1.4rem + 2.6vw,3.6rem);line-height:1.04;font-weight:600;letter-spacing:-.02em;max-width:12ch}
.ds-sub{margin:1.5rem 0 0;color:#aab0b6;font-size:1.1rem;line-height:1.55;max-width:28rem}
.ds-intro .btn__outline-white{margin-top:2rem}
.ds-list{list-style:none;margin:0;padding:0;border-top:1px solid #2c2f34}
.ds-row{border-bottom:1px solid #2c2f34}
.ds-row>a{display:grid;grid-template-columns:3rem minmax(0,1fr) auto;gap:0 1rem;align-items:start;padding:1.75rem 0;color:#fff;text-decoration:none}
.ds-n{font-size:.9rem;color:#6f757b;letter-spacing:.06em;padding-top:.55rem;transition:color .3s}
.ds-t{display:block;font-size:clamp(1.5rem,1.1rem + 1.2vw,2.1rem);font-weight:600;line-height:1.15;letter-spacing:-.01em;color:#8b9097;transition:color .3s,transform .3s}
.ds-more{display:grid;grid-template-rows:0fr;transition:grid-template-rows .45s ease}
.ds-more>*{overflow:hidden;min-height:0}
.ds-d{display:block;color:#b4bac1;line-height:1.6;font-size:1.02rem;max-width:34rem;opacity:0;transition:opacity .35s .05s}
.ds-tags{display:flex;flex-wrap:wrap;gap:.4rem;opacity:0;transition:opacity .35s .1s}
.ds-tags i{font-style:normal;font-size:.75rem;color:#c3c8cd;border:1px solid #3a3e44;border-radius:999px;padding:.25rem .65rem}
.ds-more{row-gap:0}
.ds-go{display:grid;place-items:center;width:2.75rem;height:2.75rem;border-radius:50%;border:1px solid #3a3e44;color:#8b9097;transition:background .3s,color .3s,border-color .3s,transform .3s}
.ds-row.is-open .ds-t,.ds-row>a:hover .ds-t{color:#fff}
.ds-row.is-open .ds-n{color:#a9b4ff}
.ds-row.is-open .ds-more{grid-template-rows:1fr}
.ds-row.is-open .ds-d,.ds-row.is-open .ds-tags{opacity:1}
.ds-row.is-open .ds-d{margin:1rem 0 0}.ds-row.is-open .ds-tags{margin:1rem 0 0}
.ds-row.is-open .ds-go,.ds-row>a:hover .ds-go{background:#4f46e5;border-color:#4f46e5;color:#fff;transform:rotate(0)}
@media (min-width:1024px){.ds{grid-template-columns:minmax(0,5fr) minmax(0,7fr)}.ds-intro{position:sticky;top:7rem}}
@media (prefers-reduced-motion:reduce){.ds-more,.ds-d,.ds-tags,.ds-t,.ds-go{transition:none}}
</style>"""
js = ('<script>(function(){var rows=[].slice.call(document.querySelectorAll(".ds-row"));function open(r){rows.forEach(function(x){x.classList.toggle("is-open",x===r)})}'
      'rows.forEach(function(r){r.addEventListener("mouseenter",function(){open(r)});r.addEventListener("focusin",function(){open(r)})})})();</script>')
section = (
 '<section class="section service__blocks raise-1 padded" id="services" data-type="dark">' + style + '<div class="container"><div class="ds">'
 '<div class="ds-intro"><p class="ds-eyebrow">Digital services</p><h2 class="ds-h">Strategy first, technology second</h2>'
 '<p class="ds-sub">We help businesses of every size plan, design, build and improve websites, software and AI-powered systems that make brands easier to find, trust and work with.</p>'
 '<a href="/services/" class="btn__outline-white"><span>All services</span></a></div>'
 f'<ul class="ds-list">{rows}</ul></div></div>{js}</section>')
a = h.find('<section class="section service__blocks'); b = h.find("</section>", a) + 10
assert a > 0
h = h[:a] + section + h[b:]
open(P, "w", encoding="utf-8").write(h)
print("services section redesigned")
