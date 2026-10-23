#!/usr/bin/env python3
"""One-off: rename Flow routes to FXN Studio routes and rewrite shared header/footer in preview-site/."""
import glob, html, os, re, shutil

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "preview-site")
os.chdir(ROOT)

MOVES = {
    "solutions/revenue-operations": "services/web-design",
    "solutions/it-and-people": "services/web-development",
    "solutions/finance": "services/ecommerce-development",
    "solutions/customer-support": "services/ai-integrations",
    "integrations": "technology",
    "customers": "portfolio",
    "careers": "process",
    "about": "about-us",
    "pricing": "pricing",
    "blog/topic/product": "blog/category/web-design",
    "blog/topic/guides": "blog/category/seo-growth",
    "blog/topic/engineering": "blog/category/ai-automation",
    "blog/topic/customers": "blog/category/ecommerce",
    "blog/introducing-flow-agents": "blog/ai-chat-agents-internal-tooling-productivity",
    "blog/lead-routing-in-an-afternoon": "blog/scaling-shopify-custom-storefront-cro",
    "blog/closing-the-books-in-three-days": "blog/reducing-checkout-friction-ecommerce-sales",
    "blog/idempotency-is-the-whole-job": "blog/modern-web-architecture-speed-ux",
    "blog/replaying-runs-at-scale": "blog/technical-seo-audit-checklist-perth-businesses",
    "blog/instructions-an-agent-can-follow": "blog/integrating-custom-ai-workflows-in-business",
    "blog/approvals-without-the-wait": "blog/high-converting-b2b-website-design-principles",
    "blog/owners-for-every-step": "blog/programmatic-seo-search-authority-foundations",
}
DELETE_DIRS = ["blog/series-b", "blog/what-2000-workflows-taught-us", "blog/2", "blog/topic/company"]

# Move through a staging dir so overlapping names cannot collide.
os.makedirs("_stage", exist_ok=True)
for i, (src, dst) in enumerate(MOVES.items()):
    if src != dst and os.path.isdir(src):
        shutil.move(src, f"_stage/{i}")
for d in DELETE_DIRS:
    shutil.rmtree(d, ignore_errors=True)
for i, (src, dst) in enumerate(MOVES.items()):
    if src != dst and os.path.isdir(f"_stage/{i}"):
        os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
        shutil.move(f"_stage/{i}", dst)
shutil.rmtree("_stage")
for d in ("solutions", "blog/topic"):
    if os.path.isdir(d):
        shutil.rmtree(d)

# Path rewrites for every internal link.
PATHS = {k: v for k, v in MOVES.items() if k != v}
PATHS["blog/topic/company"] = "blog"
PATHS["blog/series-b"] = "blog"
PATHS["blog/what-2000-workflows-taught-us"] = "blog"
PATHS["blog/2"] = "blog"
for p in glob.glob("**/*.html", recursive=True) + ["sitemap-index.xml", "rss.xml"]:
    if not os.path.exists(p):
        continue
    h = open(p, encoding="utf-8").read()
    for k, v in sorted(PATHS.items(), key=lambda kv: -len(kv[0])):
        h = re.sub(r'(["\'(])(https://flow\.xocoweb\.workers\.dev)?/' + re.escape(k) + r'/', lambda m: f"{m.group(1)}{m.group(2) or ''}/{v}/", h)
    h = h.replace("https://flow.xocoweb.workers.dev", "http://51.161.208.188:8793")
    open(p, "w", encoding="utf-8").write(h)

shutil.copy(os.path.join(ROOT, "..", "dist", "flow", "logo.svg"), "fxn-logo.svg")

# label -> (new label, new description or None, href or None)
NAV = {
    "Workflow builder": ("Website design", "Modern sites that turn visitors into enquiries", "/services/web-design/"),
    "Agents": ("Custom software", "Portals, apps and internal tools", "/services/web-development/"),
    "Approvals": ("eCommerce", "Shopify and custom storefronts that sell", "/services/ecommerce-development/"),
    "Run history": ("AI integration", "Chat agents and workflow automation", "/services/ai-integrations/"),
    "Integrations": ("Technology", "Open-source, API-first platforms", "/technology/"),
    "Triggers": ("SEO and growth", "Technical SEO and performance", "/blog/category/seo-growth/"),
    "Security": ("Open-source platforms", "Flexible technology, no lock-in", "/technology/"),
    "Pricing": ("Engagements", "Budget bands from $2.5k", "/pricing/"),
    "Revenue operations": ("OriginFacts", "Travel and booking", "/portfolio/"),
    "Finance": ("NXT Deals", "Price comparison and deals", "/portfolio/"),
    "Customer support": ("BestLooking.Skin", "Content and publishing", "/portfolio/"),
    "IT and people": ("SoloStack", "Publishing, Australia", "/portfolio/"),
    "Lead routing": ("Startups", None, "/about-us/"),
    "Invoice follow-ups": ("Growing brands", None, "/about-us/"),
    "Ticket triage": ("Professional services", None, "/about-us/"),
    "Employee onboarding": ("eCommerce businesses", None, "/about-us/"),
    "Renewal prep": ("Agencies and global organisations", None, "/about-us/"),
    "Blog": ("Insights", "Digital strategy, web and AI", "/blog/"),
    "Guides": ("SEO and growth", "Search visibility and speed", "/blog/category/seo-growth/"),
    "Engineering": ("AI and automation", "Practical AI for real workflows", "/blog/category/ai-automation/"),
    "Customer stories": ("Portfolio", "Selected projects and builds", "/portfolio/"),
    "About": ("About", "Australia-based, global delivery", "/about-us/"),
    "Careers": ("Process", "Eight steps from brief to launch", "/process/"),
    "Contact": ("Contact", "Start a project or ask a question", "/contact/"),
    "What's new": ("Latest articles", None, "/blog/"),
    "Status": ("Our process", None, "/process/"),
    "Book a demo": ("Start a project", None, "/contact/"),
    "Talk to sales": ("Start a project", None, "/contact/"),
    "Log in": ("About us", None, "/about-us/"),
    "Start free": ("Our work", None, "/portfolio/"),
    "Customers": ("Portfolio", None, "/portfolio/"),
    "Trigger": ("Discover", None, "/process/"),
    "3 min": ("Perth", None, "/about-us/"),
}
TEXT = {
    "Product": "Services", "Solutions": "Work", "Resources": "Insights", "Company": "Studio",
    "Platform": "Build", "Connect": "Platforms", "By team": "Selected work", "Popular workflows": "Who we work with", "Learn": "Learn",
    "Deal closed": "Goals agreed", "Agent": "Design", "Draft the plan": "Brand and UX", "Approval": "Build", "Lead approves": "Ship it", "Waiting": "Week 3",
    "See a workflow built from one sentence": "See how a project runs", "How Flow works": "Our process",
    "median lead response, down from 4 hours": "Australia-based, working worldwide", "Read customer stories": "About FXN Studio",
    "Search the blog": "Search the blog",
    "Get the Flow monthly": "Get FXN Studio insights",
    "New features, workflow ideas and what operations teams are automating. One email a month.": "Web, software and AI ideas from our Perth studio. One email a month.",
    "© 2026 Flow. All rights reserved.": "© 2026 FXN Studio. All rights reserved.",
    "All systems normal": "Perth, Australia",
    "Latest · Sep 29, 2026": "Latest article",
    "Introducing Flow Agents: steps that read, decide and write back": "AI Chat Agents & Internal Tooling: How Australian Teams Reclaim 15+ Hours Weekly",
    "you@company.com": "you@company.com",
}
SECTION = re.compile(r"<(header|footer)\b.*?</\1>", re.S)
A_TAG = re.compile(r"<a\b([^>]*)>(.*?)</a>", re.S)
TEXT_NODE = re.compile(r">([^<>]+)(?=<)")


def first_text(inner):
    for t in TEXT_NODE.findall(">" + inner + "<"):
        t = html.unescape(t).strip()
        if t:
            return t
    return None


def fix_section(sec):
    def fix_a(m):
        attrs, inner = m.group(1), m.group(2)
        if "data-logo-menu-trigger" in attrs:
            attrs = attrs.replace("Flow home", "FXN Studio home")
            inner = re.sub(r'aria-label="Flow"', 'aria-label="FXN Studio"', inner)
            inner = re.sub(r"<svg\b.*?</svg>", '<img src="/fxn-logo.svg" alt="FXN Studio" style="height:100%;width:auto">', inner, flags=re.S)
            return f"<a{attrs}>{inner}</a>"
        label = first_text(inner)
        if label in NAV:
            new_label, new_desc, href = NAV[label]
            attrs = re.sub(r'href="[^"]*"', f'href="{href}"', attrs, count=1)
        return f"<a{attrs}>{inner}</a>"

    sec = A_TAG.sub(fix_a, sec)
    # label and description nodes inside nav items
    def fix_desc(m):
        inner = m.group(2)
        label = first_text(inner)
        if label in NAV:
            new_label, new_desc, _ = NAV[label]
            seen = []

            def sub(t):
                raw = t.group(1)
                txt = html.unescape(raw).strip()
                if not txt:
                    return t.group(0)
                seen.append(txt)
                if len(seen) == 1:
                    return ">" + raw.replace(raw.strip(), html.escape(new_label, quote=False)) 
                if len(seen) == 2 and new_desc is not None:
                    return ">" + raw.replace(raw.strip(), html.escape(new_desc, quote=False))
                return t.group(0)

            inner = TEXT_NODE.sub(sub, inner)
        return f"<a{m.group(1)}>{inner}</a>"

    sec = A_TAG.sub(fix_desc, sec)

    def fix_text(m):
        t = html.unescape(m.group(1)).strip()
        if t in TEXT:
            return ">" + m.group(1).replace(m.group(1).strip(), html.escape(TEXT[t], quote=False))
        if t in NAV and not False:
            return ">" + m.group(1).replace(m.group(1).strip(), html.escape(NAV[t][0], quote=False))
        return m.group(0)

    sec = TEXT_NODE.sub(fix_text, sec)
    # drop third-party social links, keep RSS
    sec = re.sub(r'<li><a href="https://(?:www\.linkedin\.com|x\.com|github\.com|www\.youtube\.com)[^"]*".*?</li>', "", sec, flags=re.S)
    sec = sec.replace('href="https://status.example.com/"', 'href="/contact/"').replace('href="https://app.example.com/"', 'href="/about-us/"')
    return sec


for p in glob.glob("**/*.html", recursive=True):
    h = open(p, encoding="utf-8").read()
    h = SECTION.sub(lambda m: fix_section(m.group(0)), h)
    open(p, "w", encoding="utf-8").write(h)
print("done")
