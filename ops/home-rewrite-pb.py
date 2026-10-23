#!/usr/bin/env python3
"""Rewrite the copied Pixelbin-layout home page (preview-site/index.html) with FXN Studio content."""
import json, os, re

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "preview-site", "index.html")
h = open(P, encoding="utf-8").read()
ORIG = h


def rep(old, new, count=1):
    global h
    assert old in h, f"missing: {old[:70]}"
    h = h.replace(old, new) if count == 0 else h.replace(old, new, count)


MAIL = "mailto:hello@fxnstudio.com"
TITLE = "FXN Studio | Web Design, Software Development and AI Integration"
DESC = "FXN Studio is a digital studio in Perth, Australia building modern websites, custom software, e-commerce platforms and AI-powered automation for clients worldwide."

# ---- head -------------------------------------------------------------------
rep("<title>Essex Web Designer &amp; Full-Stack Developer | Pixelbin</title>", f"<title>{TITLE}</title>")
h = re.sub(r'(<meta name="description" content=")[^"]*(")', rf"\g<1>{DESC}\2", h, count=1)
h = re.sub(r'(<meta property="og:title" content=")[^"]*(")', rf"\g<1>{TITLE}\2", h)
h = re.sub(r'(<meta property="og:description" content=")[^"]*(")', rf"\g<1>{DESC}\2", h)
h = re.sub(r'(<meta name="twitter:title" content=")[^"]*(")', rf"\g<1>{TITLE}\2", h)
h = re.sub(r'(<meta name="twitter:description" content=")[^"]*(")', rf"\g<1>{DESC}\2", h)
h = re.sub(r'(<meta property="og:site_name" content=")[^"]*(")', r"\1FXN Studio\2", h)
h = re.sub(r'<meta property="og:locale" content="en_GB" />', '<meta property="og:locale" content="en_AU" />', h)
h = re.sub(r'<meta property="og:updated_time"[^>]*>', "", h)
h = re.sub(r'<meta (?:property="(?:og:image[^"]*|article:[^"]*)"|name="twitter:(?:image|label|data)[^"]*")[^>]*>', "", h)
ld = {"@context": "https://schema.org", "@type": "Organization", "name": "FXN Studio", "url": "https://fxnstudio.com/",
      "email": "hello@fxnstudio.com", "description": DESC,
      "address": {"@type": "PostalAddress", "addressLocality": "Perth", "addressCountry": "AU"}}
h = re.sub(r'<script type="application/ld\+json"[^>]*>.*?</script>', '<script type="application/ld+json">' + json.dumps(ld) + "</script>", h, count=1, flags=re.S)
# third-party scripts that carry the original owner's keys
h = re.sub(r'<script[^>]*google-recaptcha[^>]*>\s*</script>', "", h)

# ---- header -----------------------------------------------------------------
h = re.sub(r'(<a href="/" class="header__logo header__logo-small" title=")[^"]*(">\s*)<svg\b.*?</svg>',
           r'\1FXN Studio\2<img src="/img/fxn/logo.svg" alt="FXN Studio" style="height:2rem;width:auto;display:block">', h, count=1, flags=re.S)
rep('<li class="menu-item"><a href="/portfolio">Work</a></li>', '<li class="menu-item"><a href="#portfolio">Portfolio</a></li>')
rep('<li class="menu-item"><a href="/contact/">Contact</a></li>', '<li class="menu-item"><a href="/contact/">Contact</a></li>')
rep('<a href="mailto:hello@pixelbin.com" title="Email me"><span><i class="ph ph-envelope"></i> hello@pixelbin.com</span></a>',
    f'<a href="{MAIL}" title="Email FXN Studio"><span><i class="ph ph-envelope"></i> hello@fxnstudio.com</span></a>')
h = re.sub(r'<a class="btn__black" href="/contact" title="Contact a freelance[^"]*" aria-label="Contact a freelance[^"]*">',
           '<a class="btn__black" href="/contact/" title="Contact FXN Studio" aria-label="Contact FXN Studio">', h, count=1)

# ---- hero -------------------------------------------------------------------
rep("I build websites, eCommerce stores and apps then get them found using marketing, seo and social media.",
    "We build websites, software and AI that turn ambitious ideas into real results.")
rep("From websites and simple logos to scalable cross-platform apps and digital marketing, I do everything your business needs and I don't mess about either.",
    "Modern websites, custom software, e-commerce platforms and AI-powered automation for businesses of every size, built by an Australian studio working worldwide.")
h = re.sub(r'<a class="btn__black" href="/contact" title="Get in touch for a quote" aria-label="Get in touch for a quote"><span>Send me a project brief</span></a>',
           f'<a class="btn__black" href="{MAIL}" title="Start a project" aria-label="Start a project"><span>Start a project</span></a>', h)
h = re.sub(r'title="Get in touch for a quote" aria-label="Get in touch for a quote"><span>View my work</span>', 'title="View our work" aria-label="View our work"><span>View our work</span>', h)
rep("<span>Full-stack Developer</span>\nNode.js, React, Vue.js, WordPress, Magento, PHP, JavaScript, HTML5, CSS3",
    "<span>Websites and software</span>\nNext.js, React, Astro, Tailwind CSS, WordPress, Node.js, APIs")
rep("<span>UI/UX Designer</span>\nFigma, Adobe XD, Sketch, InVision, Prototyping, Wireframing, User Research",
    "<span>eCommerce</span>\nShopify, WooCommerce, Payload CMS, Strapi, Conversion optimisation")
rep("<span>Digital Marketer</span>\nSEO, SEM, Social Media Marketing, Content Marketing, Email Marketing, Analytics",
    "<span>AI and growth</span>\nChat agents, n8n workflows, Technical SEO, Analytics, Performance")

# ---- services ---------------------------------------------------------------
rep("Award-winning Digital Agency Services", "Digital services")
rep("Design-led, conversion-focused", "Strategy first, technology second")
rep("My services are comprehensive allowing businesses and start-ups small and large to leverage digital to reach more customers.",
    "We help businesses of every size plan, design, build and improve websites, software and AI-powered systems that make brands easier to find, trust and work with.")
blocks = [
 ("Website Design", "Create an instant connection with clean, conversion-focused ui/ux design built for real people. I offer responsive, user-friendly app and website design services in Essex.",
  "Website design", "Modern websites that communicate clearly, rank better in search and turn visitors into enquiries, bookings or sales.", "Design"),
 ("Web Development", "I build blazing-fast, secure websites that scale with your business and work flawlessly across all devices. My web development services in Essex covers everything.",
  "Custom software", "Internal tools, client portals, web applications, booking systems and APIs built around how your business works.", "Software"),
 ("Branding, Logos & Identity", "Define your brand with visuals and voice that connect emotionally and stand out clearly in a sea of the same. I deliver full branding and logo design in Essex for startups, growing brands and local businesses.",
  "eCommerce", "Shopify, WooCommerce and custom stores with clear product journeys, solid performance and conversion-focused checkout.", "eCommerce"),
 ("Full-stack Development", "From frontend polish to backend power, I handle the full stack so your platform just works. Hire a trusted full-stack developer in Essex for web apps, mobile apps, Custom CMS and APIs.",
  "Open-source platforms", "Flexible, maintainable solutions on modern open-source frameworks and trusted platforms, with room to scale and less lock-in.", "Platforms"),
 ("AI Integrations", "AI is the latest trennd. Automate smarter with AI that simplifies tasks and enhances user experience. I provide custom AI integration services in Essex for forward-thinking businesses.",
  "AI integration", "Practical AI chat agents, document processing and workflow automation that solve a real business problem and are easy to manage.", "Integrations"),
 ("Digital Marketing", "Grow your digital reach with strategic content, SEO and campaigns that drive results. I offer full-service digital marketing in Essex built to generate leads and loyalty.",
  "SEO and growth", "Technical SEO, performance optimisation and analytics so your website is easier for search engines to understand and for people to use.", "Growth"),
]
for ot, od, nt, nd, tag in blocks:
    rep(f'<h3 class="block__title">{ot.replace("&", "&amp;") if ("&amp;" in h and ot.replace("&", "&amp;") in h) else ot}</h3>', f'<h3 class="block__title">{nt}</h3>')
    rep(od, nd)
for old, new in (("Design</div></div></div><div class=\"col-md-6\"><div class=\"block b-2\">", None),):
    pass
for old_tag, new_tag in (("Programming", "Software"), ("Marketing Support", "Growth"), ("Integrations", "Integrations")):
    pass
# tags under each block (appear in order): Design, Programming, Design, Programming, Integrations, Marketing Support
tags_old = re.findall(r'(<i class="ph ph-stack"></i> )([A-Za-z ]+)(</div>)', h)
order = [b[4] for b in blocks]
it = iter(order)
h = re.sub(r'(<i class="ph ph-stack"></i> )[A-Za-z ]+(</div>)', lambda m: m.group(1) + next(it) + m.group(2), h, count=len(order))

rep("Clients trusting me", "Live projects")
rep("I work with a range of clients from small businesses to large corporations, delivering high-quality solutions.",
    "Websites and platforms we have built and run, from publishing and price comparison to e-commerce.")
h = re.sub(r'(<a href=")/contact(" class="btn__outline-white ms-auto"><span>)Chat with me', rf'\g<1>{MAIL}\2Contact us', h)
# third-party client logos -> remove the grid
h = re.sub(r'<div id="my-clients" class="raise-1">.*?</div></div></section>', "</div></section>", h, count=1, flags=re.S)

# ---- about ------------------------------------------------------------------
rep("UI/UX Design Services", "Why FXN Studio")
rep("Lets start attracing more customers together", "Clear thinking, then the right technology")
rep("Ditch the remote agency team who don't care and only deal with me. I'll take care of your business from the get go.",
    "Before design or development begins, we look at your audience, business model, content needs and growth plans, then recommend the right solution rather than forcing every project into the same template.")
rep('<ul class="list check"><li>CTO Experience</li><li>Multi-award winning</li><li>Based in Chelmsford, Essex</li><li>15+ years experience</li><li>Experience across multiple sectors</li><li>Can handle the entire process.</li></ul>',
    '<ul class="list check"><li>Established in Australia, delivering worldwide</li><li>Services for clients of any size</li><li>Strong focus on SEO, performance and user experience</li><li>Design, development, automation and AI in one studio</li><li>Flexible open-source technology</li><li>Clear milestones from start to finish</li></ul>')
rep("With a conversion-focused, ROI-driven design process, I will connect you with more loyal customers.",
    "Our mission is to help businesses use digital technology with clarity and confidence.")
rep('<a href="/contact" class="btn__black"><span>Start planning</span></a>', f'<a href="{MAIL}" class="btn__black"><span>Start planning</span></a>')
# right-hand illustration -> FXN photo
h = re.sub(r'(<div class="col-6 col-md-4 col-lg-6 ps-5 d-none d-md-block">\s*)<svg\b.*?</svg>(</div></div></div></section>)',
           r'\1<img src="/img/fxn/about.jpg" alt="Working on a laptop" style="width:100%;height:auto;border-radius:8px;display:block">\2', h, count=1, flags=re.S)

# ---- lets talk --------------------------------------------------------------
rep("The best website designer &amp; developer in Essex", "Digital strategy, design and engineering")
rep("Need someone to lead the whole thing?", "Have a project in mind?")
rep("From product strategy and team building to full-stack dev and scalable launch plans, I work with startups and founders as a freelance CTO — without the full-time cost.",
    "From website and platform builds to custom software and AI integration, FXN Studio plans, designs and delivers it, with a clear process and milestones.")
h = re.sub(r'<a class="btn__black large" href="/contact"\s*title="Book a free discovery call">\s*<span>Book a free discovery call</span>',
           f'<a class="btn__black large" href="{MAIL}"\ntitle="Start a project">\n<span>Start a project</span>', h)

# ---- process ----------------------------------------------------------------
rep("How I work", "How we work")
rep("My work doesn't just look good, it delivers results for my partners.", "A structured process keeps every project focused, transparent and moving in the right direction.")
items = [
 ("01", "Discovery", ["Goals", "Audience", "Current systems", "Scope"], "Discovery", "Share what you want to build",
  ["We start by understanding your business, audience, goals, challenges and current digital systems. This helps us identify what needs to be built and why it matters."], "Start a project"),
 ("02", "Strategy", ["Project scope", "User journeys", "Content structure", "Platforms"], "Strategy", "A practical roadmap",
  ["We define the project scope, user journeys, content structure, technical requirements and recommended platforms. This stage creates a practical roadmap for design and development."], "Send us your brief"),
 ("03", "Design", ["UX", "Interface design", "Brand"], "Design", "Layouts that make key actions easy",
  ["We create user-focused layouts and interface designs that match your brand, support your content and make key actions easy for visitors or users."], "Send us your brief"),
 ("04", "Build", ["Development", "Integration", "APIs", "Clean code"], "Development and integration", "Clean code, integration-ready architecture",
  ["We build the website, application or platform using modern technology, clean code, responsive layouts and integration-ready architecture.",
   "Where needed, we connect your digital product with third-party tools, APIs, payment systems, CRMs, analytics platforms, automation workflows or AI services."], "Request a quote"),
 ("05", "Launch", ["Testing", "Launch", "SEO", "Support"], "Testing, launch and support", "Test, launch and keep improving",
  ["We test across devices, browsers, forms, workflows and important user actions to make sure the final product works as expected.",
   "We prepare the site or system for release, support deployment and help ensure tracking, performance and essential SEO elements are in place. After launch we can keep helping with updates, optimisation, new features and technical support."], "Plan your launch"),
]
parts = []
for n, t, tags, pre, head, paras, btn in items:
    chips = "".join(f"<li>{x}</li>" for x in tags)
    body = "".join(f"<p>{p}</p>" for p in paras)
    parts.append(f'<div class="section__services-item"><div class="section__services-toggle"><div class="container"><div class="start"> {n}</div><div class="middle"><h2 class="h3">{t}</h2><ul class="tags">{chips}</ul></div><div class="end"><div class="arrow"></div></div></div></div>'
                 f'<div class="container section__services-accordion"><div class="inner"><div class="row align-items-center"><div class="col-8"><h3 class="pretitle">{pre}</h3><p class="title h3">{head}</p>{body}'
                 f'<a href="{MAIL}" class="btn__outline-white mt-4"><span>{btn}</span></a></div><div class="col-5 offset-1 hide"></div></div></div></div></div>')
a = h.find('<section class="section section__services raise-1" id="process">')
first = h.find('<div class="section__services-item">', a)
end = h.find("</section>", a)
h = h[:first] + "".join(parts) + h[end:]

# ---- portfolio --------------------------------------------------------------
rep("Freelance Web Design Company Essex", "Selected work")
rep("Strategy-led, design-driven", "Built for commercial impact")
rep("My work is user-focused, data-driven and driving new business and customers for my clients.", "Live websites and platforms from our portfolio, each built to be fast, clear and easy to manage.")
rep('<a href="/portfolio" class="btn__black ms-auto"><span>View all projects</span></a>', '<a href="https://fxnstudio.com/portfolio/" class="btn__black ms-auto" target="_blank" rel="noopener"><span>View all projects</span></a>')
work = [
 ("originfacts", "https://originfacts.com/", "OriginFacts", "Travel guides and the facts behind places worth visiting, plus news on flights, hotels, airlines and airports."),
 ("bestlooking-skin", "https://www.bestlooking.skin/", "BestLooking.Skin", "Honest skincare reviews, formulation guides and healthy skin advice on a fast headless CMS."),
 ("nxt-deals", "https://nxt.deals/", "NXT Deals", "Verified deals, coupon codes and honest price comparison, engineered for smart shopping."),
 ("solostack", "https://solostack.au/", "SoloStack", "Tech stacks, software reviews and AI automation guides for solo operators in Australia."),
 ("nxt-smart-home", "https://nxtsmarthome.com.au/", "NXT Smart Home", "Smart home buying guides and device advice tailored for Australian homes."),
 ("fxnseo", "https://fxnseo.com/", "FXN SEO", "Free browser-based SEO tools for keywords, backlinks, meta tags, schema and more."),
]
items_pat = re.compile(r'<a class="portfolio__item-link" href="[^"]*">(<div class="portfolio__item-screen">\s*<picture><img data-src=")[^"]*("[^>]*/>\s*</picture>\s*<svg\b.*?</svg></div><div class="h4 title">)[^<]*(</div><p>)[^<]*(</p>)', re.S)
it = iter(work)
def sub_item(m):
    slug, url, name, desc = next(it)
    return (f'<a class="portfolio__item-link" href="{url}" target="_blank" rel="noopener">{m.group(1)}/wp-content/uploads/fxn/{slug}-thumb-900x506.jpg{m.group(2)}{name}{m.group(3)}{desc}{m.group(4)}')
h, k = items_pat.subn(sub_item, h)
assert k == 6, f"portfolio items matched: {k}"

h = h.replace('id="portfolio" data-type="">', 'id="portfolio" data-type="" style="padding-bottom:7rem">')
# ---- testimonial and award logos (third-party people and brands) ------------
h = re.sub(r'<section class="section testimonial  padded">.*?</section>', "", h, count=1, flags=re.S)
h = re.sub(r'<section class="raise-1 relative section pt-4 pb-4" data-type="dark" id="awards">.*?</section>', "", h, count=1, flags=re.S)

# ---- sky / closing ----------------------------------------------------------
rep("Time to reach for the stars", "Let's build something that works")
rep("Reach out, lets talk about goals", "Tell us about your goals")
rep("I provide bespoke solutions crafted specifically for you.", "We provide solutions built around your business.")
rep("Whether you need a simple website, a complex eCommerce store, a mobile app or a full digital marketing package, I can help. Let's discuss your project and see how I can assist you in reaching more customers.",
    "Whether you need a new website, a custom software platform, an e-commerce store or AI integration, FXN Studio can help you plan the right next step.")
h = re.sub(r'(<a [^>]*href=")/contact("[^>]*>\s*<span>)Chat with me', rf"\g<1>{MAIL}\2Get in Touch", h)

# ---- footer -----------------------------------------------------------------
h = re.sub(r'(<div id="footer-top"><div class="container">\s*)<svg\b.*?</svg>', r'\1<img src="/img/fxn/logo-light.svg" alt="FXN Studio" style="height:2.5rem;width:auto;display:block">', h, count=1, flags=re.S)
rep("Pixelbin, providing expert level digital services since 2010", "FXN Studio, a digital studio established in Australia")
rep("Based in Chelmsford, Essex - Just outside London, I design, build and deploy brands, business websites, mobile apps and web apps then continue to support your business with digital marketing strategies.",
    "Based in Perth, Australia and serving clients globally, we design, build and launch websites, software, e-commerce platforms and AI integrations, then keep improving them with you.")
rep('<li><a href="">Home</a></li><li><a href="/portfolio">Work</a></li><li><a href="/contact">Contact</a></li>',
    '<li><a href="/">Home</a></li><li><a href="#portfolio">Portfolio</a></li><li><a href="/contact/">Contact</a></li>')
for old, new in (("Web Designer", "Website design"), ("Web Developer", "Custom software"), ("Digital Marketer", "eCommerce"), ("Social Media Manager", "AI integration"),
                 ("App Designer", "Open-source platforms"), ("UI/UX Designer", "SEO and growth"), ("Logo Designer", "Performance"), ("Branding Expert", "Strategy first")):
    rep(f"<span>{old}</span>", f"<span>{new}</span>", 0)
rep("©2026 Copyright Pixelbin Website Design, All Rights Reserved", "©2026 FXN Studio. Established in Australia. Serving clients globally.")
rep('<a href="/terms-of-services" class="terms">Terms of Service</a>', '<a href="https://fxnstudio.com/terms-of-services/" class="terms" target="_blank" rel="noopener">Terms of Service</a>')

open(P, "w", encoding="utf-8").write(h)
left = [w for w in ("Pixelbin", "pixelbin", "Essex", "Chelmsford", "Webby", "Awwwards", "Upwork", "Andy", "Cresswell", "Katrina") if w in h]
print("rewritten; leftover words:", left)
