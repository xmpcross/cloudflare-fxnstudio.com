#!/usr/bin/env python3
"""Build preview-site/portfolio/index.html: Pixelbin portfolio layout with FXN Studio's live projects."""
import json, os, re, sys

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pb_shell

SRC = open(os.path.join(BASE, "ops/orig/portfolio.pixelbin.html"), encoding="utf-8").read()
HOME = open(os.path.join(BASE, "preview-site/index.html"), encoding="utf-8").read()
OUT = os.path.join(BASE, "preview-site/portfolio/index.html")
h = SRC
TITLE = "Portfolio | FXN Studio Websites, Platforms and Software"
DESC = "Live websites and platforms built by FXN Studio: publishing, price comparison, travel, e-commerce and free online tools."

h = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", h, count=1, flags=re.S)
for pat in (r'(<meta name="description" content=")[^"]*(")', r'(<meta property="og:description" content=")[^"]*(")', r'(<meta name="twitter:description" content=")[^"]*(")'):
    h = re.sub(pat, rf"\g<1>{DESC}\2", h)
for pat in (r'(<meta property="og:title" content=")[^"]*(")', r'(<meta name="twitter:title" content=")[^"]*(")'):
    h = re.sub(pat, rf"\g<1>{TITLE}\2", h)
h = re.sub(r'(<meta property="og:site_name" content=")[^"]*(")', r"\1FXN Studio\2", h)
h = h.replace('<meta property="og:locale" content="en_GB" />', '<meta property="og:locale" content="en_AU" />')
h = re.sub(r'<link rel="canonical" href="[^"]*" />', '<link rel="canonical" href="https://fxnstudio.com/portfolio/" />', h)
h = re.sub(r'<meta property="og:url" content="[^"]*" />', '<meta property="og:url" content="https://fxnstudio.com/portfolio/" />', h)
h = re.sub(r'<meta property="og:updated_time"[^>]*>', "", h)
h = re.sub(r'<meta (?:property="(?:og:image[^"]*|article:[^"]*)"|name="twitter:(?:image|label|data)[^"]*")[^>]*>', "", h)
ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "FXN Studio portfolio", "url": "https://fxnstudio.com/portfolio/",
      "publisher": {"@type": "Organization", "name": "FXN Studio", "url": "https://fxnstudio.com/"}}
h = re.sub(r'<script type="application/ld\+json"[^>]*>.*?</script>', '<script type="application/ld+json">' + json.dumps(ld) + "</script>", h, count=1, flags=re.S)
h = re.sub(r'<script[^>]*google-recaptcha[^>]*>\s*</script>', "", h)
import base64
h = re.sub(r'<script[^>]*src="data:text/javascript;base64,[^"]+"[^>]*>(?:</script>)?',
           lambda m: "" if re.search(r"UA-|gtag", base64.b64decode(re.search(r"base64,([^\"]+)", m.group(0)).group(1)).decode("utf-8", "ignore")) else m.group(0), h)
h = pb_shell.apply(h, HOME, "portfolio")

P = [  # slug, name, url, category, description
 ("originfacts", "OriginFacts", "https://originfacts.com/", "Travel and booking", "The facts behind places worth visiting, plus news and guides on flights, hotels, airlines and airports."),
 ("nxt-deals", "NXT Deals", "https://nxt.deals/", "Price comparison", "Verified deals, coupon codes and honest price comparison platform engineered for smart shopping."),
 ("nxt-discount", "NXT Discount", "https://nxtdiscount.com/", "Price comparison", "Promo codes and discounted products, read daily from retailers' own pages and priced in your currency."),
 ("nxt-bargains", "NXT Bargains", "https://nxt.bargains/", "Price comparison", "Side-by-side product comparisons, honest reviews and a smart deals marketplace."),
 ("nxt-smart-home", "NXT Smart Home", "https://nxtsmarthome.com.au/", "Publishing", "Smart home buying guides and device advice tailored for Australian homes."),
 ("nxt-smart-homes", "NXT Smart Homes", "https://nxtsmart.homes/", "Publishing", "Smart home guides, honest device reviews, comparisons and how-to walkthroughs."),
 ("bestlooking-skin", "BestLooking.Skin", "https://www.bestlooking.skin/", "Publishing", "Honest skincare reviews, formulation guides and healthy skin advice."),
 ("fur-fun-shop", "Fur Fun Shop", "https://furfunshop.com/", "eCommerce", "Toys, beds, treats and premium care products for dogs and cats."),
 ("furry-friend-facts", "Furry Friend Facts", "https://furryfriendfacts.com/", "eCommerce", "Smart gadgets for pets, from smart feeders to GPS tracking devices."),
 ("mysecure-homes", "MySecure.Homes", "https://mysecure.homes/", "eCommerce", "Smart home security products, from cameras to smart locks and alarms."),
 ("nxt-vitality", "NXT Vitality", "https://nxtvitality.com/", "eCommerce", "Supplements and health wellness products storefront."),
 ("ohmnook", "OhmNook", "https://ohmnook.com/", "Publishing", "Independent home office and work-from-home tech guides with shop listings."),
 ("solostack", "SoloStack", "https://solostack.au/", "Publishing", "Tech stacks, software reviews and AI automation guides for solo operators."),
 ("fxnseo", "FXN SEO", "https://fxnseo.com/", "Tools", "Free browser-based SEO tools for keywords, backlinks, meta tags, schema and more."),
]
cats = ["All"] + sorted({p[3] for p in P}, key=lambda c: -sum(1 for p in P if p[3] == c))
chips = "".join(f'<a href="#" class="tag{" active" if c == "All" else ""}" data-filter="{c}">{c}</a>' for c in cats)
SIZES = [6] * 14  # every card the same size
ARROW = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M8 7h9v9"/></svg>'
# slug: (headline, detail, [built with, content], [tags])
X = {
 "originfacts": ("Travel guides and the facts behind places worth visiting.", "News and guides on flights, hotels, airlines and airports, on a headless CMS.", ["Next.js", "Headless CMS"], ["Travel", "Website development"]),
 "nxt-deals": ("Verified deals and honest price comparison.", "Coupon codes and price comparison engineered for smart shopping, fed by retailer data.", ["Next.js", "Retailer feeds"], ["Price comparison", "Data feeds"]),
 "nxt-discount": ("Promo codes read daily from retailers' own pages.", "Discounted products priced in your currency, on Next.js with a headless CMS.", ["Next.js", "Headless CMS"], ["Price comparison", "Headless CMS"]),
 "nxt-bargains": ("Side-by-side comparisons and smart deals.", "Product comparisons, honest reviews and a deals marketplace built on data feeds.", ["Next.js", "Data feeds"], ["Price comparison", "Data feeds"]),
 "nxt-smart-home": ("Smart home advice for Australian homes.", "Buying guides and device advice tailored for Australian homes, with a product catalogue.", ["Next.js", "Product catalogue"], ["Publishing", "Australia"]),
 "nxt-smart-homes": ("Smart home guides, reviews and how-tos.", "Honest device reviews, comparisons and walkthroughs on a headless CMS.", ["Next.js", "Headless CMS"], ["Publishing", "Headless CMS"]),
 "bestlooking-skin": ("Honest skincare reviews and skin advice.", "Reviews, formulation guides and healthy skin advice on a fast headless CMS.", ["Next.js", "Headless CMS"], ["Publishing", "Beauty"]),
 "fur-fun-shop": ("A pet store for dogs and cats.", "Toys, beds, treats and premium care products on WooCommerce and WordPress.", ["WooCommerce", "WordPress"], ["eCommerce", "Storefront"]),
 "furry-friend-facts": ("Smart gadgets for pets.", "From smart feeders to GPS tracking devices, on a hosted store.", ["FreshStore", "Hosted store"], ["eCommerce", "Pet tech"]),
 "mysecure-homes": ("Smart home security products.", "Cameras, smart locks and alarms on a hosted store.", ["FreshStore", "Hosted store"], ["eCommerce", "Security"]),
 "nxt-vitality": ("A supplements and wellness storefront.", "Health and wellness products on a hosted store.", ["FreshStore", "Hosted store"], ["eCommerce", "Wellness"]),
 "ohmnook": ("Home office tech guides, researched.", "Independent work-from-home tech guides with shop listings, on Next.js and Payload CMS.", ["Next.js", "Payload CMS"], ["Publishing", "Shop listings"]),
 "solostack": ("Tech stacks and tools for solo operators.", "Software reviews and AI automation guides on Next.js and Payload CMS.", ["Next.js", "Payload CMS"], ["Publishing", "AI automation"]),
 "fxnseo": ("Free SEO tools that run in your browser.", "Keywords, backlinks, meta tags, schema and more, on browser tools with a headless CMS.", ["Browser tools", "Headless CMS"], ["Tools", "SEO"]),
}
KINDS = ["monitor", "laptop", "duo"]


def scene(k, s, n):
    kind = KINDS[k % 3]
    desk = f'<img src="/wp-content/uploads/fxn/desktop/{s}.jpg" alt="{n} website screenshot" width="1280" height="800" loading="lazy">'
    if kind == "monitor":
        dev = f'<span class="pf-mon"><span class="pf-mon-screen">{desk}</span><span class="pf-mon-neck"></span><span class="pf-mon-base"></span></span>'
    elif kind == "laptop":
        dev = f'<span class="pf-lap"><span class="pf-lap-lid"><span class="pf-cam"></span>{desk}</span><span class="pf-lap-base"></span></span>'
    else:
        dev = (f'<span class="pf-ipad"><span class="pf-cam"></span><img src="/wp-content/uploads/fxn/tablet/{s}.jpg" alt="{n} on an iPad screen" width="1024" height="768" loading="lazy"></span>'
               f'<span class="pf-iphone"><span class="pf-island"></span><img src="/wp-content/uploads/fxn/mobile/{s}.jpg" alt="{n} on an iPhone screen" width="520" height="1125" loading="lazy"></span>')
    return f'<span class="pf-scene">{dev}</span>'


def card(k, s, n, u, c, d):
    head, detail, built, tags = X[s]
    facts = "".join(f'<li><strong>{v}</strong><span>{l}</span></li>' for v, l in ((built[0], "Built with"), (built[1], "Content"), ("Live", "Status")))
    chips = "".join(f"<li>{t}</li>" for t in tags)
    return (f'<div class="col-md-{SIZES[k]} pf-item" data-cat="{c}"><article class="portfolio__item pf-card">'
            f'<a class="pf-media" href="{u}" target="_blank" rel="noopener" aria-label="Visit {n}">{scene(k, s, n)}</a>'
            f'<div class="pf-meta"><span class="pf-name">{n}</span><span class="pf-cat">{c}</span></div>'
            f'<h2 class="pf-head">{head}</h2><p class="pf-detail">{detail}</p>'
            f'<ul class="pf-facts">{facts}</ul>'
            f'<div class="pf-foot"><ul class="pf-tags">{chips}</ul><div class="pf-cta"><a class="pf-btn" href="{u}" target="_blank" rel="noopener">Visit site</a><a class="pf-go" href="{u}" target="_blank" rel="noopener" aria-label="Open {n}">{ARROW}</a></div></div></article></div>')


cards = "".join(card(k, *row) for k, row in enumerate(P))
style = """<style>
.pf-media{display:block;text-decoration:none}
.pf-scene{display:block;position:relative;container-type:inline-size;aspect-ratio:3/2;overflow:visible}
.pf-mon,.pf-lap,.pf-ipad,.pf-iphone{transition:transform .5s cubic-bezier(.2,.8,.2,1)}
.pf-mon{position:absolute;left:4%;top:0;width:92%;translate:0 calc(var(--p,0) * 10px)}
.pf-mon-screen{display:block;aspect-ratio:16/10;padding:1.1cqw;background:#101114;border-radius:1.6cqw;box-shadow:inset 0 0 0 .2cqw #3a3d44,0 2cqw 4cqw -1.5cqw rgb(0 0 0/.45)}
.pf-mon-screen img,.pf-lap-lid img{display:block;width:100%;height:100%;object-fit:cover;object-position:top;border-radius:.7cqw}
.pf-mon-neck{display:block;width:9%;height:6cqw;margin:0 auto;background:linear-gradient(90deg,#9aa0a8,#dde0e5 45%,#8d939b)}
.pf-mon-base{display:block;width:26%;height:1cqw;margin:0 auto;background:linear-gradient(#e3e6ea,#a7adb5);border-radius:.8cqw .8cqw .4cqw .4cqw;box-shadow:0 1.2cqw 2.2cqw -.4cqw rgb(0 0 0/.45)}
.pf-lap{position:absolute;left:7%;top:0;width:86%;translate:0 calc(var(--p,0) * 10px)}
.pf-lap-lid{display:block;position:relative;aspect-ratio:16/10;padding:1cqw;background:#0e0f12;border-radius:1.8cqw 1.8cqw 0 0;box-shadow:inset 0 0 0 .2cqw #3a3d44}
.pf-lap-base{display:block;position:relative;height:1.9cqw;width:112%;margin-left:-6%;background:linear-gradient(#eceff2,#aeb4bb);border-radius:0 0 2.2cqw 2.2cqw/0 0 1.6cqw 1.6cqw;box-shadow:0 1.6cqw 2.8cqw -.6cqw rgb(0 0 0/.5)}
.pf-lap-base:after{content:"";position:absolute;left:50%;top:0;width:12%;height:.7cqw;margin-left:-6%;background:#9298a0;border-radius:0 0 .8cqw .8cqw}
.pf-ipad{position:absolute;left:0;top:0;width:80%;aspect-ratio:4/3;padding:1.5cqw;background:#15171a;border-radius:3.2cqw;box-shadow:0 2.2cqw 5cqw -1.6cqw rgb(0 0 0/.5),inset 0 0 0 .25cqw #3b3f45;translate:0 calc(var(--p,0) * 12px)}
.pf-ipad img{display:block;width:100%;height:100%;object-fit:cover;object-position:top;border-radius:1.2cqw}
.pf-cam{position:absolute;left:50%;top:.5cqw;width:.7cqw;height:.7cqw;margin-left:-.35cqw;border-radius:50%;background:#2a2d32;z-index:2}
.pf-iphone{position:absolute;right:0;bottom:0;width:22%;aspect-ratio:9/18.6;padding:.9cqw;background:#0e0f11;border-radius:4.2cqw;box-shadow:0 2.6cqw 5.5cqw -1.4cqw rgb(0 0 0/.6),inset 0 0 0 .25cqw #3b3f45;translate:0 calc(var(--p,0) * -26px)}
.pf-iphone img{display:block;width:100%;height:100%;object-fit:cover;object-position:top;border-radius:3.4cqw}
.pf-island{position:absolute;left:50%;top:1.7cqw;width:5.6cqw;height:1.6cqw;margin-left:-2.8cqw;border-radius:1cqw;background:#050506;z-index:2}
.pf-card:hover .pf-mon,.pf-card:hover .pf-lap,.pf-card:hover .pf-ipad{transform:translateY(-.9cqw)}
.pf-card:hover .pf-iphone{transform:translateY(-1.5cqw) rotate(-1deg)}
.pf-meta{display:flex;justify-content:space-between;align-items:baseline;gap:1rem;margin-top:1.5rem;font-size:.95rem}
.pf-name{font-size:14px;font-weight:500;text-transform:uppercase;color:#0f0f0f}.pf-cat{color:#6b6b6b;font-size:.85rem;text-align:right}
.pf-head{margin:.9rem 0 0;font-size:clamp(1.25rem,1rem + 1vw,1.7rem);line-height:1.08;font-weight:600;color:#0f0f0f}
.pf-detail{margin:1rem 0 0;color:#555;line-height:1.5}
.pf-facts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1rem;list-style:none;margin:1.5rem 0 0;padding:1.25rem 0 0;border-top:1px solid #d6d6d6}
.pf-facts strong{display:block;font-size:1rem;font-weight:600;line-height:1.1;color:#0f0f0f}
.pf-facts span{display:block;margin-top:.35rem;font-size:.8rem;color:#6b6b6b;line-height:1.3}
.pf-foot{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:1rem;margin-top:1.5rem}
.pf-tags{display:flex;flex-wrap:wrap;gap:.4rem;list-style:none;margin:0;padding:0}
.pf-tags li{font-size:.78rem;color:#444;border:1px solid #cfcfcf;border-radius:6px;padding:.3rem .65rem}
.pf-cta{display:flex;gap:.25rem}
.pf-btn,.pf-go{display:inline-flex;align-items:center;justify-content:center;height:clamp(2rem,1.7rem + .6vw,2.4rem);text-decoration:none;transition:background .2s}
.pf-btn{background:#0f0f0f;color:#fff!important;padding:0 clamp(.9rem,.7rem + .6vw,1.2rem);border-radius:6px 0 0 6px;font-size:clamp(.78rem,.7rem + .25vw,.88rem)}
.pf-go{width:clamp(2rem,1.7rem + .6vw,2.4rem);background:#4f46e5;color:#fff!important;border-radius:0 6px 6px 0}.pf-go svg{width:clamp(13px,.7rem + .3vw,16px);height:auto}
.pf-btn:hover{background:#2a2a2a}.pf-go:hover{background:#3d34c9}
.pf-js .pf-item{opacity:0;transform:translateY(46px);transition:opacity .7s ease var(--d,0ms),transform .8s cubic-bezier(.2,.8,.2,1) var(--d,0ms)}
.pf-js .pf-item.is-in{opacity:1;transform:none}
/* header, after the Legency Media example */
@media (min-width:900px){.page__heading{box-sizing:border-box;height:440px;padding-top:0!important;padding-bottom:0!important}.page__heading>.container,.page__heading>.container>.row,.page__heading>.container>.row>.col{height:100%}.page__heading>.container>.row>.col{display:flex;flex-direction:column;justify-content:center}.page__heading .pf-bar{margin-top:3rem;margin-bottom:0;box-sizing:border-box;min-height:96px}}
.pf-eyebrow{margin:0 0 2rem;font-size:1rem;color:#555}
.pf-top{display:grid;grid-template-columns:minmax(0,1fr);gap:1.5rem 3rem;align-items:center}
.pf-title{margin:0;font-size:3rem;font-weight:700;line-height:.95;letter-spacing:-.04em!important;color:#0f0f0f}
.pf-sub{margin:0;max-width:30rem;color:#111;font-size:1.2rem;line-height:1.3}
.pf-bar{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:1rem;margin-top:3.5rem;padding-top:1.75rem;border-top:1px solid #d6d6d6}
.pf-bar .tags{display:flex;flex-wrap:wrap;gap:.5rem;margin:0}
.pf-bar .tag{border-radius:6px!important;padding:.85rem 1.15rem!important;border:1px solid #d9d9d9!important;background:#f7f7f7!important;color:#222!important;font-size:1rem;line-height:1;text-decoration:none}
.pf-bar .tag.active{background:#1a1a1a!important;color:#fff!important;border-color:#1a1a1a!important}
.pf-count{color:#555;font-size:.95rem}
@media (min-width:900px){.pf-top{grid-template-columns:minmax(0,1.5fr) minmax(0,1fr)}.pf-title{white-space:nowrap}.pf-sub{justify-self:start;padding-left:2rem}}
@media (prefers-reduced-motion:reduce){.pf-js .pf-item{opacity:1;transform:none;transition:none}.pf-mon,.pf-lap,.pf-ipad,.pf-iphone{translate:none;transition:none}}
</style>"""
script = ('<script>(function(){var tags=document.querySelectorAll("[data-filter]"),items=document.querySelectorAll(".pf-item");'
          'tags.forEach(function(t){t.addEventListener("click",function(e){e.preventDefault();var f=t.getAttribute("data-filter");'
          'tags.forEach(function(x){x.classList.toggle("active",x===t)});'
          'var n=0;items.forEach(function(i){var show=(f==="All"||i.getAttribute("data-cat")===f);i.style.display=show?"":"none";if(show)n++});var c=document.getElementById("pf-count");if(c)c.textContent=n+(n===1?" project":" projects")})})})();</script>')
scroll_js = ('<script>(function(){if(matchMedia("(prefers-reduced-motion: reduce)").matches)return;document.documentElement.classList.add("pf-js");'
             'var items=[].slice.call(document.querySelectorAll(".pf-item"));'
             'var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("is-in");io.unobserve(e.target)}})},{threshold:.12,rootMargin:"0px 0px -6% 0px"});'
             'items.forEach(function(it,i){it.style.setProperty("--d",(i%2)*90+"ms");io.observe(it)});'
             'var devs=[].slice.call(document.querySelectorAll(".pf-device")),tick=false;'
             'function upd(){tick=false;var vh=innerHeight;devs.forEach(function(d){var r=d.getBoundingClientRect();if(r.bottom<-120||r.top>vh+120)return;'
             'var p=((r.top+r.height/2)-vh/2)/(vh/2+r.height/2);p=Math.max(-1,Math.min(1,p));d.style.setProperty("--p",p.toFixed(3))})}'
             'addEventListener("scroll",function(){if(!tick){tick=true;requestAnimationFrame(upd)}},{passive:true});addEventListener("resize",upd);upd();})();</script>')
main = (f'<main role="main"><section class="page__heading"><div class="container"><div class="row"><div class="col"><p class="pf-eyebrow">Portfolio</p><div class="pf-top"><h1 class="pf-title">Selected work.</h1><p class="pf-sub">Live websites, platforms and tools built by FXN Studio, from publishing and price comparison to e-commerce.</p></div><div class="pf-bar"><div class="tags">{chips}</div><span class="pf-count" id="pf-count">{len(P)} projects</span></div></div></div></div></section>'
        f'{style}<section class="section section__first portfolio" style="padding-bottom:80px"><div class="container"><div class="portfolio__inner"><div class="row" style="--bs-gutter-x:5.5rem;row-gap:7rem;align-items:flex-start">{cards}</div></div></div></section>{script}{scroll_js}</main>')
h = re.sub(r"<main role=\"main\">.*?</main>", lambda m: main, h, count=1, flags=re.S)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write(h)
print("portfolio written; leftover:", [w for w in ("Pixelbin", "pixelbin", "Essex", "Trevor", "Upwork", "Magento") if w in h])
