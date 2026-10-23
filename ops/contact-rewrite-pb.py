#!/usr/bin/env python3
"""Rebuild preview-site/contact/index.html: Pixelbin contact layout, FXN Studio content, working mailto form."""
import base64, json, os, re

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SRC = open(os.path.join(BASE, "ops/orig/contact.pixelbin.html"), encoding="utf-8").read()
HOME = open(os.path.join(BASE, "preview-site/index.html"), encoding="utf-8").read()
OUT = os.path.join(BASE, "preview-site/contact/index.html")
h = SRC

TITLE = "Contact FXN Studio | Start a Website, Software or AI Project"
DESC = "Contact FXN Studio, a digital studio in Perth, Australia. Tell us about your website, software, e-commerce or AI project and we will get back to you with the best way forward."

# ---- head -------------------------------------------------------------------
h = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", h, count=1, flags=re.S)
for pat in (r'(<meta name="description" content=")[^"]*(")', r'(<meta property="og:description" content=")[^"]*(")', r'(<meta name="twitter:description" content=")[^"]*(")'):
    h = re.sub(pat, rf"\g<1>{DESC}\2", h)
for pat in (r'(<meta property="og:title" content=")[^"]*(")', r'(<meta name="twitter:title" content=")[^"]*(")'):
    h = re.sub(pat, rf"\g<1>{TITLE}\2", h)
h = re.sub(r'(<meta property="og:site_name" content=")[^"]*(")', r"\1FXN Studio\2", h)
h = h.replace('<meta property="og:locale" content="en_GB" />', '<meta property="og:locale" content="en_AU" />')
h = re.sub(r'<link rel="canonical" href="[^"]*" />', '<link rel="canonical" href="https://fxnstudio.com/contact/" />', h)
h = re.sub(r'<meta property="og:url" content="[^"]*" />', '<meta property="og:url" content="https://fxnstudio.com/contact/" />', h)
h = re.sub(r'<meta property="og:updated_time"[^>]*>', "", h)
h = re.sub(r'<meta (?:property="(?:og:image[^"]*|article:[^"]*)"|name="twitter:(?:image|label|data)[^"]*")[^>]*>', "", h)
ld = {"@context": "https://schema.org", "@type": "ContactPage", "name": "Contact FXN Studio", "url": "https://fxnstudio.com/contact/",
      "about": {"@type": "Organization", "name": "FXN Studio", "email": "hello@fxnstudio.com",
                "address": {"@type": "PostalAddress", "addressLocality": "Perth", "addressCountry": "AU"}}}
h = re.sub(r'<script type="application/ld\+json"[^>]*>.*?</script>', '<script type="application/ld+json">' + json.dumps(ld) + "</script>", h, count=1, flags=re.S)
h = re.sub(r'<script[^>]*google-recaptcha[^>]*>\s*</script>', "", h)
h = re.sub(r'<script[^>]*src="data:text/javascript;base64,[^"]+"[^>]*>(?:</script>)?',
           lambda m: "" if re.search(r"UA-|gtag", base64.b64decode(re.search(r"base64,([^\"]+)", m.group(0)).group(1)).decode("utf-8", "ignore")) else m.group(0), h)

# ---- header and footer taken from the rewritten home page --------------------
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pb_shell
h = pb_shell.apply(h, HOME, "contact")

# ---- main -------------------------------------------------------------------
types = ["General enquiry", "Website design and development", "eCommerce development", "Custom software", "AI integration and automation", "SEO and performance"]
radios = "".join(
    f'<span class="wpcf7-list-item{" first" if i == 0 else ""}{" last" if i == len(types) - 1 else ""}"><label class="custom-control custom-radio"><input type="radio" name="contact-type" value="{t}"{" checked" if i == 0 else ""} class="custom-control-input"><span class="wpcf7-list-item-label custom-control-label">{t}</span></label></span>'
    for i, t in enumerate(types))
budgets = ["Not sure yet", "$2.5k – $5k", "$5k – $15k", "$15k – $30k", "$30k+"]
opts = "".join(f"<option>{b}</option>" for b in budgets)


def field(label, name, typ="text", ph="", req=False, auto=""):
    star = "*" if req else ""
    return (f'<div class="form-input"><p><label>{label}</label><br /><span class="wpcf7-form-control-wrap"><input size="40" maxlength="400" class="wpcf7-form-control wpcf7-text" '
            f'{"required " if req else ""}{f"autocomplete=\"{auto}\" " if auto else ""}placeholder="{ph}{star}" value="" type="{typ}" name="{name}" /></span></p></div>')


form = (
    '<form id="fxn-enquiry" class="wpcf7-form" action="#" method="get" aria-label="Enquiry form" novalidate>'
    f'<div class="row"><div class="col-md-6">{field("First name", "first-name", ph="First name", req=True, auto="given-name")}</div><div class="col-md-6">{field("Last name", "last-name", ph="Last name", req=True, auto="family-name")}</div></div>'
    f'{field("Your email", "your-email", "email", "you@company.com", True, "email")}'
    f'<div class="row"><div class="col-md-6">{field("Company", "company", ph="Company name", auto="organization")}</div><div class="col-md-6">{field("Location", "location", ph="City, country")}</div></div>'
    f'{field("Full website URL", "your-website", "url", "https://yourwebsite.com")}'
    f'<div class="row"><div class="col-md-6"><div class="form-input"><p><label>Project budget</label><br /><span class="wpcf7-form-control-wrap"><select class="wpcf7-form-control wpcf7-text" name="budget" style="width:100%;height:74px;padding:0 20px;font-size:17px;background:transparent;border:1px solid #0f0f0f;border-radius:8px;color:inherit">{opts}</select></span></p></div></div>'
    f'<div class="col-md-6">{field("Timeline", "timeline", ph="e.g. launch by March")}</div></div>'
    '<div class="form-input"><p><label>Project overview and goals</label><br /><span class="wpcf7-form-control-wrap"><textarea cols="40" rows="8" maxlength="2000" class="wpcf7-form-control wpcf7-textarea" required placeholder="Tell us a little about your business, your goals and what you would like to build.*" name="your-message"></textarea></span></p></div>'
    f'<div class="form-input"><p><label>What do you need?</label><br /><span class="wpcf7-form-control-wrap"><span class="wpcf7-form-control wpcf7-radio">{radios}</span></span></p></div>'
    '<div class="button-bar d-flex"><p><button type="submit" class="btn__black ms-auto"><span>Send enquiry</span></button></p></div>'
    '<p id="fxn-status" role="status" aria-live="polite" style="margin-top:1rem"></p></form>'
)
script = ('<script>(function(){var f=document.getElementById("fxn-enquiry");if(!f)return;f.addEventListener("submit",function(e){e.preventDefault();'
          'var d=new FormData(f),v=function(k){return(d.get(k)||"").toString().trim()};'
          'if(!v("first-name")||!v("last-name")||!/^\\S+@\\S+\\.\\S+$/.test(v("your-email"))||!v("your-message")){document.getElementById("fxn-status").textContent="Please complete your name, a valid email and your project overview.";return}'
          'var s="Project enquiry from "+v("first-name")+" "+v("last-name");'
          'var b=["Name: "+v("first-name")+" "+v("last-name"),"Email: "+v("your-email"),"Company: "+v("company"),"Location: "+v("location"),"Website: "+v("your-website"),"Budget: "+v("budget"),"Timeline: "+v("timeline"),"Enquiry type: "+v("contact-type"),"","Project overview and goals:",v("your-message")].join("\\n");'
          'document.getElementById("fxn-status").textContent="Opening your email app with your enquiry ready to send to hello@fxnstudio.com.";'
          'window.location.href="mailto:hello@fxnstudio.com?subject="+encodeURIComponent(s)+"&body="+encodeURIComponent(b)})})();</script>')
main = ('<main role="main"><section class="page__heading"><div class="container"><div class="row"><div class="col-lg-8"><h1 class="h1">Let\'s talk</h1>'
        '<p class="subtitle h4">Whether you need a new website, a custom software platform, an e-commerce store or AI integration, FXN Studio can help you plan the right next step. Use the form below to send us a brief.</p>'
        '<p class="subtitle h4" style="margin-top:1rem"><a href="mailto:hello@fxnstudio.com">hello@fxnstudio.com</a> &middot; Perth, Australia &middot; Working with clients worldwide</p></div></div></div></section>'
        f'<section class="section section__first padded"><div class="container"><div class="row"><div class="col-lg-12">{form}</div></div></div></section>{script}</main>')
h = re.sub(r"<main role=\"main\">.*?</main>", lambda m: main, h, count=1, flags=re.S)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write(h)
left = [w for w in ("Pixelbin", "pixelbin", "Essex", "Chelmsford", "£", "UA-7211", "recaptcha") if w in h]
print("written; leftover:", left)
