#!/usr/bin/env python3
"""Insert the About FXN Studio text section directly above the closing scene on the home page (idempotent)."""
import os, re

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "preview-site", "index.html")
h = open(P, encoding="utf-8").read()
h = re.sub(r'<section class="studio-text".*?</section>', "", h, flags=re.S)
h = re.sub(r"<style>\s*\.studio-text\{.*?</style>", "", h, flags=re.S)

style = """<style>
.studio-text{background:#fff;padding:clamp(4rem,8vw,7rem) 0;color:#333}
.st-wrap{max-width:1400px;margin:0 auto;padding:0 21px;display:grid;gap:2.5rem 5rem}
.st-eyebrow{margin:0 0 1rem;font-size:.85rem;font-weight:500;letter-spacing:.08em;text-transform:uppercase;color:#6b6b6b}
.st-h{margin:0;font-size:clamp(2rem,1.3rem + 2.2vw,3rem);line-height:1.08;font-weight:600;letter-spacing:-.02em;color:#0f0f0f;max-width:14ch}
.st-body p{margin:0 0 1.25rem;font-size:1.12rem;line-height:1.7;color:#444;max-width:44rem}
.st-body p:last-child{margin-bottom:0}
.st-body strong{color:#0f0f0f;font-weight:600}
.st-body a{color:#0f0f0f;text-decoration:underline;text-underline-offset:3px}
@media (min-width:1024px){.st-wrap{grid-template-columns:minmax(0,5fr) minmax(0,7fr)}}
</style>"""
sec = (
 '<section class="studio-text" id="studio-text" aria-labelledby="st-title">' + style + '<div class="st-wrap"><div><p class="st-eyebrow">About FXN Studio</p>'
 '<h2 class="st-h" id="st-title">A digital studio built for clarity</h2></div><div class="st-body">'
 '<p><strong>FXN Studio is an Australia-based digital studio</strong> delivering web design, software development, e-commerce solutions, automation and AI integration for clients worldwide. We work with startups, local companies, growing brands, professional service firms, e-commerce businesses, agencies and global organisations.</p>'
 '<p>Every project starts with clear thinking. Before design or development begins, we look at your audience, business model, content needs, workflows, growth plans and technical requirements, so we can recommend the right solution rather than forcing every project into the same template.</p>'
 '<p>We build with modern, flexible technology: open-source frameworks, reliable platforms, API-first architecture and AI-ready workflows where they add real value. The result is a digital system that is fast, secure, maintainable and ready to grow with your business.</p>'
 '<p>Our mission is to help businesses use digital technology with clarity and confidence. See <a href="/services/">what we do</a>, browse our <a href="/portfolio/">portfolio</a> or <a href="/about-us/">learn more about the studio</a>.</p>'
 '</div></div></section>')
i = h.find("sky-scene")
assert i > 0
i = h.rfind("<section", 0, i)
h = h[:i] + sec + h[i:]
open(P, "w", encoding="utf-8").write(h)
print("text section inserted above the closing scene")
