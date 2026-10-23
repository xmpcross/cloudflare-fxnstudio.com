#!/usr/bin/env python3
"""Home closing section: swap the silhouette figures (boy, sign, grass) for an original animated lighthouse scene (idempotent)."""
import os, re

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "preview-site", "index.html")
h = open(P, encoding="utf-8").read()
a = h.find('<svg id="web-designer-scene"'); b = h.find("</svg>", a) + 6
svg = h[a:b]
g = svg.find("<g ")
assert g > 0 or "fx-lighthouse" in svg
if g > 0:
    svg = svg[:g] + "@@SCENE@@" + "</svg>"
GLOW = 'style="fill:#ffe2a0"'
reeds = "".join(
    f'<path class="fx-reed" style="fill:none;stroke:#0e0f10;stroke-width:{w};stroke-linecap:round;animation-delay:-{d}s" d="M{x} 262 C{x + c1} {262 - hh * .45} {x + c2} {262 - hh * .8} {x + c3} {262 - hh}"/>'
    for x, c1, c2, c3, hh, w, d in [(1118, 2, 8, 14, 46, 2.2, 0), (1126, -2, -6, -12, 58, 2.4, 1.3), (1134, 3, 9, 20, 40, 2, 2.1), (1142, -1, -4, -8, 52, 2.2, .6),
                                    (868, 2, 7, 13, 44, 2.2, 1.7), (876, -3, -8, -15, 56, 2.4, .9), (884, 2, 5, 9, 36, 2, 2.6)])
scene = (
    '<style>.fx-beam{transform-origin:1000px 102px;animation:fx-sweep 9s ease-in-out infinite}.fx-beam.l{animation-delay:-4.5s}'
    '@keyframes fx-sweep{0%,100%{opacity:0;transform:rotate(-5deg)}20%,45%{opacity:1}55%{opacity:.0;transform:rotate(5deg)}}'
    '.fx-glow{animation:fx-flick 3.2s ease-in-out infinite}@keyframes fx-flick{0%,100%{opacity:1}50%{opacity:.75}}'
    '.fx-reed{transform-origin:bottom center;transform-box:fill-box;animation:fx-sway 5s ease-in-out infinite}@keyframes fx-sway{0%,100%{transform:rotate(-2deg)}50%{transform:rotate(3deg)}}'
    '@media (prefers-reduced-motion:reduce){.fx-beam,.fx-glow,.fx-reed{animation:none}.fx-beam.r{opacity:.9}}</style>'
    '<defs><linearGradient id="fxb" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#ffe9b0" stop-opacity=".42"/><stop offset="1" stop-color="#ffe9b0" stop-opacity="0"/></linearGradient>'
    '<linearGradient id="fxbl" x1="1" x2="0" y1="0" y2="0"><stop offset="0" stop-color="#ffe9b0" stop-opacity=".42"/><stop offset="1" stop-color="#ffe9b0" stop-opacity="0"/></linearGradient></defs>'
    '<g transform="translate(-175 0)"><g id="fx-lighthouse">'
    '<path class="fx-beam r" style="fill:url(#fxb)" d="M1000 102 L1560 30 L1560 175Z"/><path class="fx-beam l" style="fill:url(#fxbl)" d="M1000 102 L440 30 L440 175Z"/>'
    '<path d="M976 252 L987 124 L1013 124 L1024 252Z"/><path style="fill:#1d2128" d="M981.5 196 L1018.5 196 L1017 168 L983 168Z"/>'
    '<path d="M980 124 H1020 V117 H980Z"/><path d="M989 117 V96 H1011 V117Z"/>'
    f'<path class="fx-glow" {GLOW} d="M992 112 V100 H1008 V112Z"/><path d="M985 96 L1000 76 L1015 96Z"/><path d="M999 76 V66 H1001 V76Z"/>'
    '</g>' + reeds + '</g>')
svg = svg.replace("@@SCENE@@", scene) if "@@SCENE@@" in svg else re.sub(r'<style>\.fx-beam.*?</g>(?:<path class="fx-reed".*?/>)+</g>', scene, svg, flags=re.S)
h = h[:a] + svg + h[b:]
open(P, "w", encoding="utf-8").write(h)
print("scene swapped; old figures left:", 'id="boy"' in h, 'id="sign"' in h, 'id="greens"' in h)
