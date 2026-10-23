#!/usr/bin/env python3
"""Home page 'Selected work': a one-row, three-up auto-sliding carousel of every portfolio card (idempotent; run after home-rewrite-pb.py and portfolio-rewrite-pb.py)."""
import os, re

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "preview-site")
home = open(os.path.join(BASE, "index.html"), encoding="utf-8").read()
pf = open(os.path.join(BASE, "portfolio/index.html"), encoding="utf-8").read()

style = re.search(r"<style>\s*\.pf-media.*?</style>", pf, flags=re.S).group(0)
body = pf[pf.find('<div class="col-md-6 pf-item"'):]
cards = re.split(r'(?=<div class="col-md-6 pf-item")', body)
cards = [c for c in cards if c.startswith('<div class="col-md-6 pf-item"')]
tail = "</div></div></div></section>"
if tail in cards[-1]:
    cards[-1] = cards[-1][: cards[-1].find(tail)]
items = []
for c in cards:
    slug = re.search(r"/wp-content/uploads/fxn/(?:desktop|tablet)/([a-z-]+)\.jpg", c).group(1)
    url = re.search(r'class="pf-media" href="([^"]+)"', c).group(1)
    name = re.search(r'aria-label="Visit ([^"]+)"', c).group(1)
    cat = re.search(r'<span class="pf-cat">([^<]*)</span>', c).group(1)
    head = re.search(r'<h2 class="pf-head">(.*?)</h2>', c, flags=re.S).group(1)
    detail = re.search(r'<p class="pf-detail">(.*?)</p>', c, flags=re.S).group(1)
    items.append((slug, url, name, cat, head, detail))
slides = items

ARROW = ('<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>')
css = """<style>
.wk-cols{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}
.wk-col{min-width:0}
.wk-col .pf-scene{display:block}
.wk-col .pf-scene{aspect-ratio:auto;padding:0 0 0}
.wk-col .pf-ipad{display:block;box-sizing:border-box;position:relative;left:auto;top:auto;width:100%;aspect-ratio:auto;margin:0;translate:none}
.wk-screen{display:block;overflow:hidden;aspect-ratio:4/3;border-radius:1.2cqw}
.wk-screen .wk-strip{height:100%}
.wk-strip{display:flex;height:100%;transition:transform .8s cubic-bezier(.22,.8,.24,1);will-change:transform}
.wk-item{position:relative;display:block;flex:0 0 100%;min-width:0;text-decoration:none}
.wk-item img{display:block;width:100%;height:100%;object-fit:cover;object-position:top}
.wk-ov{position:absolute;left:0;right:0;bottom:0;display:flex;flex-direction:column;gap:.35rem;padding:3.2rem 1.1rem 1rem;background:linear-gradient(to top,rgba(8,16,48,.94) 0%,rgba(8,16,48,.78) 45%,rgba(8,16,48,0) 100%);color:#fff;text-align:left}
.wk-ov .pf-cat{order:1;font-size:12px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:#ffd24a;text-align:left}
.wk-ov .pf-name{order:2;font-size:1.05rem;font-weight:700;line-height:1.15;letter-spacing:0;text-transform:none;color:#fff}
@media (max-width:1023px){.wk-cols{grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}.wk-col:nth-child(3){display:none}}
@media (max-width:639px){.wk-cols{grid-template-columns:minmax(0,1fr)}.wk-col:nth-child(2){display:none}}
@media (prefers-reduced-motion:reduce){.wk-strip{transition:none}}
</style>"""
js = """<script>(function(){var root=document.querySelector(".wk");if(!root)return;var cols=[].slice.call(root.querySelectorAll(".wk-col")),n=cols[0].querySelectorAll(".wk-item").length,i=0,timer=null,paused=false;
function per(){return innerWidth<640?1:innerWidth<1024?2:3}
function max(){return Math.max(0,n-per())}
function go(m,user){i=m>max()?0:m<0?max():m;cols.forEach(function(c,k){var t="translateX(-"+((i+k)*100)+"%)";c.querySelector(".wk-strip").style.transform=t});if(user)restart()}
function restart(){clearInterval(timer);if(matchMedia("(prefers-reduced-motion: reduce)").matches)return;timer=setInterval(function(){if(!paused)go(i+1)},3500)}
root.addEventListener("mouseenter",function(){paused=true});root.addEventListener("mouseleave",function(){paused=false});root.addEventListener("focusin",function(){paused=true});root.addEventListener("focusout",function(){paused=false});
var rt;addEventListener("resize",function(){clearTimeout(rt);rt=setTimeout(function(){go(Math.min(i,max()))},150)});
go(0);restart()})();</script>"""
def column(k):
    its = "".join(
        f'<a class="wk-item" href="{u}" target="_blank" rel="noopener" aria-label="Visit {nm}"><img src="/wp-content/uploads/fxn/tablet/{sl}.jpg" alt="{nm} on an iPad screen" width="1024" height="768" loading="lazy">'
        f'<span class="wk-ov"><span class="pf-cat">{ct}</span><span class="pf-name">{nm}</span></span></a>'
        for sl, u, nm, ct, hd, dt in items)
    return '<div class="wk-col"><span class="pf-scene"><span class="pf-ipad"><span class="pf-cam"></span><span class="wk-screen"><span class="wk-strip">' + its + '</span></span></span></span></div>'


car = ('<div class="portfolio__inner"><div class="wk"><div class="wk-cols">' + "".join(column(k) for k in range(3)) + "</div>"
       "</div></div></div>" + js)

home = re.sub(r"<style>(?:(?!</style>).)*\.wk-(?:dots|track)(?:(?!</style>).)*</style>", "", home, flags=re.S)
home = re.sub(r"<style>\s*\.pf-media.*?</style>", "", home, flags=re.S)
home = re.sub(r"<style>\s*\.portfolio \.pf-foot\{.*?</style>", "", home, flags=re.S)
home = re.sub(r"<script>\(function\(\)\{var root=document\.querySelector\(\"\.wk\"\).*?</script>", "", home, flags=re.S)
home = re.sub(r"<style>\s*\.wk-cols\{.*?</style>", "", home, flags=re.S)
home = re.sub(r"<style>\s*\.portfolio \.pf-foot\{.*?</style>", "", home, flags=re.S)
a = home.find('<div class="portfolio__inner">')
end = home.find("</section>", a)
assert a > 0
home = home[:a] + style + css + car + home[end:]
open(os.path.join(BASE, "index.html"), "w", encoding="utf-8").write(home)
print("selected work: carousel of", len(slides), "cards")
