#!/usr/bin/env python3
"""Replace everything below the hero on the preview home page with the redesigned sections."""
import os, re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "preview-site")
P = os.path.join(ROOT, "index.html")
h = open(P, encoding="utf-8").read()

ARROW = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
CHECK = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg>'


def link(href, text):
    return f'<a class="hx-link" href="{href}">{text}{ARROW}</a>'


services = [
    ("01", "Website design and development", "Modern websites that communicate clearly, rank better in search and turn visitors into enquiries, bookings or sales.", "/services/web-design/"),
    ("02", "Custom software", "Internal tools, client portals, web and mobile apps, APIs and integrations built around how you work.", "/services/web-development/"),
    ("03", "eCommerce and storefronts", "Shopify and custom stores with clear product journeys, solid performance and conversion-focused checkout.", "/services/ecommerce-development/"),
    ("04", "AI integration and automation", "Custom AI tools, chat agents and workflow automation that solve a real business problem.", "/services/ai-integrations/"),
]
svc = "".join(
    f'<li><a href="{u}" class="hx-row"><span class="hx-row__n">{n}</span><span class="hx-row__t"><strong>{t}</strong><span>{d}</span></span><span class="hx-row__a">{ARROW}</span></a></li>'
    for n, t, d, u in services
)

work = [
    ("originfacts", "Travel and booking", "originfacts.com", "OriginFacts", "The facts behind places worth visiting, plus news and guides on flights, hotels, airlines and airports.", "Next.js · Headless CMS", "hx-w1"),
    ("bestlooking-skin", "Beauty and skincare", "bestlooking.skin", "BestLooking.Skin", "Honest skincare reviews, formulation guides and healthy skin advice.", "Next.js · Headless CMS", "hx-w2"),
    ("nxt-deals", "Price comparison and deals", "nxt.deals", "NXT Deals", "Verified deals, coupon codes and honest price comparison, engineered for smart shopping.", "Next.js · Retailer data feeds", "hx-w3"),
    ("solostack", "Publishing · Australia", "solostack.au", "SoloStack", "Tech stacks, software reviews and AI automation guides for solo operators.", "Next.js · Payload CMS", "hx-w4"),
]
cards = "".join(
    f'<li class="hx-work {c}"><a href="/portfolio/"><span class="hx-work__img"><img src="/img/home/{img}.jpg" alt="{name} website screenshot" width="1440" height="1000" loading="lazy"></span>'
    f'<span class="hx-work__meta"><span class="hx-kicker">{cat} · {dom}</span><strong>{name}</strong><span>{desc}</span><em>{stack}</em></span></a></li>'
    for img, cat, dom, name, desc, stack, c in work
)

steps = [
    ("01", "Discover", "We start by understanding your business, audience, goals, challenges and current digital systems."),
    ("02", "Design and build", "We define scope and user journeys, design user-focused layouts, then build with clean code and integration-ready architecture."),
    ("03", "Launch and grow", "We test across devices and browsers, support deployment, and keep helping with updates, optimisation and support."),
]
steps_html = "".join(f'<li><span class="hx-step__n">{n}</span><div><strong>{t}</strong><p>{d}</p></div></li>' for n, t, d in steps)

ai_points = [
    ("Useful first", "We look for a real business problem to solve, rather than adding AI for its own sake."),
    ("Secure by design", "AI is integrated into your websites, software and workflows with care for your data and access."),
    ("Easy to manage", "Built so your team can run, review and adjust it after launch."),
]
ai_html = "".join(f'<li><span class="hx-tick">{CHECK}</span><div><strong>{t}</strong><p>{d}</p></div></li>' for t, d in ai_points)

techs = [("Next.js", "nextdotjs"), ("React", "react"), ("Astro", "astro"), ("Tailwind CSS", "tailwindcss"), ("Payload CMS", "payloadcms"), ("Strapi", "strapi"),
         ("WordPress", "wordpress"), ("WooCommerce", "woocommerce"), ("n8n", "n8n"), ("Docker", "docker"), ("Cloudflare", "cloudflare"), ("Vercel", "vercel")]
tech_html = "".join(f'<li><img src="/img/technologies/{f}.svg" alt="" width="36" height="36" loading="lazy"><span>{n}</span></li>' for n, f in techs)

facts = [("7", "service areas"), ("8", "steps from discovery to support"), ("14", "live projects in our portfolio"), ("Perth", "Australia-based, working worldwide")]
facts_html = "".join(f'<li><strong>{n}</strong><span>{l}</span></li>' for n, l in facts)

faqs = [
    ("Who do you work with?", "Businesses of all sizes, including startups, local companies, growing brands, professional service firms, e-commerce businesses, agencies and global organisations."),
    ("Do you work with clients outside Australia?", "Yes. FXN Studio is established in Australia, but our services are available to clients worldwide. We work remotely with teams across time zones using clear communication, structured milestones and flexible delivery models."),
    ("What does your process look like?", "Eight stages: discovery, strategy, design, development, integration, testing, launch, and support and improvement. Each stage has a clear purpose."),
    ("Do you build with open-source technology?", "Yes. We use modern open-source technologies and trusted platforms, which helps reduce unnecessary lock-in and gives businesses room to scale."),
    ("Can you help after launch?", "Yes. After launch we can continue helping with updates, optimisation, new features, content changes and technical support."),
]
faq_html = "".join(f'<details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(faqs))

# blog cards: reuse the existing cards' covers and text
old_blog = h[h.find('aria-labelledby="latest-title"'):]
posts = [
    ("modern-web-architecture-speed-ux", "/_astro/cover.CmeZS0NO_1j8xv7.webp", "Web Design &amp; UX", "October 2026", "Modern Web Architecture: How Speed &amp; UX Directly Impact Conversion Rates", "Analysing how sub-second page loads, Core Web Vitals and smooth interactive UI components eliminate user drop-offs and drive revenue."),
    ("reducing-checkout-friction-ecommerce-sales", "/_astro/cover.Be1RkVDJ_2arES2.webp", "eCommerce &amp; CRO", "September 2026", "Reducing Checkout Friction: 5 UX Adjustments That Immediately Boost Sales", "From one-click guest checkouts to transparent shipping calculators, explore proven UX optimisations that save abandoned shopping carts."),
    ("ai-chat-agents-internal-tooling-productivity", "/_astro/cover.B8xomNor_ZpIoLp.webp", "AI &amp; Automation", "August 2026", "AI Chat Agents &amp; Internal Tooling: How Australian Teams Reclaim 15+ Hours Weekly", "A practical engineering walkthrough of internal AI tools, automated summary dashboards and customer inquiry automation."),
]
blog_html = "".join(
    f'<li><a href="/blog/{s}/"><span class="hx-post__img"><img src="{img}" alt="" width="720" height="450" loading="lazy"></span>'
    f'<span class="hx-kicker">{cat} · {date}</span><strong>{t}</strong><span>{d}</span></a></li>'
    for s, img, cat, date, t, d in posts
)

NEW = f'''
<section class="hx-section" id="services" aria-labelledby="hx-services-title"><div class="hx-wrap hx-split">
<div class="hx-head"><p class="hx-eyebrow">What we do</p><h2 id="hx-services-title">Practical solutions, built around your business</h2><p class="hx-lead">We bring strategy, design and development together with flexible open-source technology.</p></div>
<ul class="hx-rows">{svc}</ul></div></section>

<section class="hx-section hx-tint" id="work" aria-labelledby="hx-work-title"><div class="hx-wrap">
<div class="hx-bar"><div><p class="hx-eyebrow">Selected work</p><h2 id="hx-work-title">Built for commercial impact</h2></div>{link("/portfolio/", "View all projects")}</div>
<ul class="hx-works">{cards}</ul>
<p class="hx-also">Also live: NXT Smart Home, Fur Fun Shop, OhmNook, FXN SEO and more. <a href="/portfolio/">See the full portfolio</a></p></div></section>

<section class="hx-section" id="process" aria-labelledby="hx-process-title"><div class="hx-wrap hx-media">
<figure class="hx-figure"><img src="/img/studio/process.jpg" alt="Planning a project at a desk" width="1256" height="830" loading="lazy"></figure>
<div><p class="hx-eyebrow">How we work</p><h2 id="hx-process-title">From first conversation to launch</h2><p class="hx-lead">A structured process keeps every project focused, transparent and moving in the right direction.</p><ol class="hx-steps">{steps_html}</ol>{link("/process/", "See all eight steps")}</div></div></section>

<section class="hx-section hx-tint" id="ai" aria-labelledby="hx-ai-title"><div class="hx-wrap hx-media hx-media--flip">
<div><p class="hx-eyebrow">AI integration</p><h2 id="hx-ai-title">AI that solves a real business problem</h2><p class="hx-lead">We integrate artificial intelligence into websites, software, customer experiences and internal workflows in ways that are useful, secure and easy to manage.</p><ul class="hx-ticks">{ai_html}</ul>{link("/services/ai-integrations/", "Explore AI integration")}</div>
<figure class="hx-figure"><img src="/img/studio/about.jpg" alt="Working on a laptop" width="1778" height="1142" loading="lazy"></figure></div></section>

<section class="hx-section" id="technology" aria-labelledby="hx-tech-title"><div class="hx-wrap">
<div class="hx-bar"><div><p class="hx-eyebrow">Technology</p><h2 id="hx-tech-title">Flexible, open-source technology</h2></div>{link("/technology/", "Explore technology")}</div>
<p class="hx-lead hx-narrow">We build with modern web frameworks, open-source content systems and established commerce platforms. Automation and cloud infrastructure keep the work connected.</p>
<ul class="hx-tech">{tech_html}</ul></div></section>

<section class="hx-facts" aria-label="FXN Studio at a glance"><div class="hx-wrap"><div class="hx-facts__head"><h2>Australian studio. Global delivery.</h2><p>FXN Studio helps businesses of every size build modern websites, scalable software and AI-powered digital systems.</p></div><ul>{facts_html}</ul></div></section>

<section class="hx-section" id="faq" aria-labelledby="hx-faq-title"><div class="hx-wrap hx-split">
<div class="hx-head"><p class="hx-eyebrow">FAQ</p><h2 id="hx-faq-title">Questions, answered</h2><p class="hx-lead">Can’t find what you need? <a href="/contact/">Get in touch</a>.</p></div>
<div class="hx-faq">{faq_html}</div></div></section>

<section class="hx-section hx-tint" id="insights" aria-labelledby="hx-blog-title"><div class="hx-wrap">
<div class="hx-bar"><div><p class="hx-eyebrow">Insights</p><h2 id="hx-blog-title">From the blog</h2></div>{link("/blog/", "All posts")}</div>
<ul class="hx-posts">{blog_html}</ul></div></section>
'''

m = h.find("<main")
hero_end = h.find("</section>", h.find('aria-labelledby="hero-title"')) + len("</section>")
end = h.rfind("</main>")
h = h[:hero_end] + NEW + h[end:]
open(P, "w", encoding="utf-8").write(h)
print("sections replaced")
