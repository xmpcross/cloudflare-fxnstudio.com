#!/usr/bin/env python3
"""Redesign the image column of the home page 'Why FXN Studio' section (idempotent; run after home-rewrite-pb.py)."""
import os, re

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "preview-site", "index.html")
h = open(P, encoding="utf-8").read()
a = h.find('id="about"'); a = h.rfind("<section", 0, a); b = h.find("</section>", a) + 10
sec = h[a:b]
svg = (
 '<svg viewBox="0 0 400 500" role="img" aria-label="A website wireframe that is designed and then built" preserveAspectRatio="xMidYMid slice">'
 '<defs><pattern id="wa-dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.1" fill="#b9c0e8" opacity=".5"/></pattern>'
 '<linearGradient id="wa-g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4f46e5"/><stop offset="1" stop-color="#14b8a6"/></linearGradient>'
 '<clipPath id="wa-clip"><rect x="40" y="86" width="320" height="300" rx="12"/></clipPath></defs>'
 '<rect width="400" height="500" fill="url(#wa-dots)"/>'
 # window
 '<g class="wa-win"><rect x="40" y="86" width="320" height="300" rx="12" class="wa-frame"/><path d="M40 118 H360" class="wa-rule"/>'
 '<circle cx="58" cy="102" r="4" class="wa-d1"/><circle cx="72" cy="102" r="4" class="wa-d2"/><circle cx="86" cy="102" r="4" class="wa-d3"/>'
 # wireframe (strategy): sketched outlines
 '<g class="wa-wire" clip-path="url(#wa-clip)">'
 '<rect x="58" y="134" width="284" height="26" rx="6" pathLength="1"/><rect x="58" y="176" width="170" height="92" rx="8" pathLength="1"/><rect x="240" y="176" width="102" height="92" rx="8" pathLength="1"/>'
 '<path d="M58 288 H300M58 304 H260M58 320 H280" pathLength="1"/><rect x="58" y="338" width="86" height="28" rx="14" pathLength="1"/></g>'
 # design: blocks fill with colour
 '<g class="wa-fill" clip-path="url(#wa-clip)">'
 '<rect x="58" y="134" width="284" height="26" rx="6" fill="#e9ebfb"/><rect x="58" y="176" width="170" height="92" rx="8" fill="url(#wa-g)"/><rect x="240" y="176" width="102" height="92" rx="8" fill="#dff4ef"/>'
 '<rect x="58" y="286" width="244" height="6" rx="3" fill="#cfd3ea"/><rect x="58" y="302" width="204" height="6" rx="3" fill="#cfd3ea"/><rect x="58" y="318" width="224" height="6" rx="3" fill="#cfd3ea"/><rect x="58" y="338" width="86" height="28" rx="14" fill="#1a1a2e"/></g></g>'
 # technology: code chip + check
 '<g class="wa-code" transform="translate(206 330)"><rect width="168" height="92" rx="12" fill="#12142b"/>'
 '<circle cx="18" cy="18" r="3.5" fill="#ff6b6b"/><circle cx="31" cy="18" r="3.5" fill="#ffd24a"/><circle cx="44" cy="18" r="3.5" fill="#3ddc97"/>'
 '<rect x="18" y="38" width="64" height="6" rx="3" fill="#8e86ff"/><rect x="90" y="38" width="40" height="6" rx="3" fill="#6ee7d4"/><rect x="30" y="54" width="86" height="6" rx="3" fill="#a3a9c2"/><rect x="30" y="70" width="52" height="6" rx="3" fill="#a3a9c2"/><rect class="wa-caret" x="86" y="68" width="3" height="10" fill="#fff"/></g>'
 '<g class="wa-ok" transform="translate(342 96)"><circle r="16" fill="#3ddc97"/><path d="M-6 0 L-1.5 5 L7 -5" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" pathLength="1"/></g>'
 # phase labels
 '<g class="wa-lb wa-l1"><rect x="40" y="418" width="120" height="30" rx="15"/><text x="56" y="437" class="wa-n">01</text><text x="78" y="437">Strategy</text></g>'
 '<g class="wa-lb wa-l2"><rect x="40" y="418" width="120" height="30" rx="15"/><text x="56" y="437" class="wa-n">02</text><text x="78" y="437">Design</text></g>'
 '<g class="wa-lb wa-l3"><rect x="40" y="418" width="132" height="30" rx="15"/><text x="56" y="437" class="wa-n">03</text><text x="78" y="437">Technology</text></g>'
 '</svg>')
style = """<style>
.why-art{position:relative;aspect-ratio:4/5;border-radius:12px;overflow:hidden;background:linear-gradient(160deg,#eef1ff 0%,#f4edff 55%,#e6f7f3 100%);box-shadow:0 24px 50px -28px rgb(40 40 120/.45)}
#about .why-art svg{display:block;width:100%;height:100%;transform:none;padding:0}
.why-art .wa-frame{fill:#fff;stroke:#d9ddf3;stroke-width:1.5}
.why-art .wa-rule{stroke:#e4e7f7;stroke-width:1.5}.why-art .wa-d1{fill:#ffb3b3}.why-art .wa-d2{fill:#ffe3a1}.why-art .wa-d3{fill:#b8ecd2}
.why-art .wa-win{animation:wa-rise 9s ease-in-out infinite}
.why-art .wa-wire rect,.why-art .wa-wire path{fill:none;stroke:#4f46e5;stroke-width:1.6;stroke-linecap:round;stroke-dasharray:1;stroke-dashoffset:1;animation:wa-sketch 9s ease-in-out infinite}
.why-art .wa-fill{opacity:0;animation:wa-fill 9s ease-in-out infinite}
.why-art .wa-code{opacity:0;transform:translate(206px,346px);animation:wa-code 9s ease-in-out infinite}
.why-art .wa-caret{animation:wa-blink 1s steps(1) infinite}
.why-art .wa-ok{opacity:0;transform-box:fill-box;transform-origin:center;animation:wa-ok 9s ease-out infinite}
.why-art .wa-ok path{stroke-dasharray:1;stroke-dashoffset:1;animation:wa-tick 9s ease-out infinite}
.why-art .wa-lb{opacity:0}.why-art .wa-lb rect{fill:#fff;stroke:#dfe3f7}
.why-art .wa-l1{animation:wa-l1 9s ease-in-out infinite}.why-art .wa-l2{animation:wa-l2 9s ease-in-out infinite}.why-art .wa-l3{animation:wa-l3 9s ease-in-out infinite}
.why-art text{font-family:inherit;font-size:13.5px;font-weight:500;fill:#1b1d2a}.why-art .wa-n{font-size:11px;font-weight:600;fill:#4f46e5;letter-spacing:.04em}
@keyframes wa-rise{0%{opacity:0;transform:translateY(14px)}6%,92%{opacity:1;transform:none}100%{opacity:0}}
@keyframes wa-sketch{0%,6%{stroke-dashoffset:1;opacity:1}28%,40%{stroke-dashoffset:0;opacity:1}52%,100%{stroke-dashoffset:0;opacity:0}}
@keyframes wa-fill{0%,32%{opacity:0}48%,92%{opacity:1}100%{opacity:0}}
@keyframes wa-code{0%,56%{opacity:0;transform:translate(206px,346px)}68%,92%{opacity:1;transform:translate(206px,330px)}100%{opacity:0}}
@keyframes wa-ok{0%,76%{opacity:0;transform:scale(.4)}84%,92%{opacity:1;transform:scale(1)}100%{opacity:0}}
@keyframes wa-tick{0%,78%{stroke-dashoffset:1}86%,100%{stroke-dashoffset:0}}
@keyframes wa-blink{50%{opacity:0}}
@keyframes wa-l1{0%,6%{opacity:0}10%,32%{opacity:1}36%,100%{opacity:0}}
@keyframes wa-l2{0%,34%{opacity:0}40%,56%{opacity:1}60%,100%{opacity:0}}
@keyframes wa-l3{0%,58%{opacity:0}64%,92%{opacity:1}100%{opacity:0}}
@media (prefers-reduced-motion:reduce){.why-art *{animation:none!important}.why-art .wa-wire rect,.why-art .wa-wire path{stroke-dashoffset:0;opacity:0}.why-art .wa-fill,.why-art .wa-code,.why-art .wa-ok,.why-art .wa-l3{opacity:1}.why-art .wa-code{transform:translate(206px,330px)}.why-art .wa-ok path{stroke-dashoffset:0}}
</style>"""
vis = style + '<div class="why-art">' + svg + '</div>'
new = re.sub(r'(<div class="col-6 col-md-4 col-lg-6 ps-5 d-none d-md-block">).*?(</div></div></div></section>)', lambda m: m.group(1) + vis + m.group(2), sec, count=1, flags=re.S)
assert new != sec or "why-vis" in sec
h = h[:a] + new + h[b:]
open(P, "w", encoding="utf-8").write(h)
print("why image redesigned")
