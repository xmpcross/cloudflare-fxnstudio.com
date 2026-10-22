#!/usr/bin/env python3
"""Build a database-free site from editable HTML and public assets."""
import json
import shutil
from pathlib import Path
from xml.sax.saxutils import escape
from html.parser import HTMLParser
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]

class Canonical(HTMLParser):
    url = None
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.url = attrs.get('href')

def build():
    site = json.loads((ROOT / 'site.json').read_text())
    routes = json.loads((ROOT / 'routes.json').read_text())
    output = ROOT / 'dist'
    stage = ROOT / '.dist-build'
    if stage.exists():
        shutil.rmtree(stage)
    shutil.copytree(ROOT / 'public', stage)
    urls = []
    for route in routes:
        source = ROOT / 'content' / route['file']
        assert source.resolve().is_relative_to((ROOT / 'content').resolve())
        html = source.read_text()
        assert '<html' in html.lower(), f'Invalid HTML: {source}'
        dest = stage / route['file']
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html)
        if route['status'] == 200:
            parser = Canonical()
            parser.feed(html)
            if parser.url:
                urls.append(urljoin(f"https://{site['domain']}/", parser.url))
    if not (stage / '404.html').exists():
        (stage / '404.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="robots" content="noindex"><title>Page not found</title><h1>Page not found</h1><p><a href="/">Return home</a></p></html>')
    (stage / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{escape(url)}</loc></url>\n' for url in sorted(set(urls))) + '</urlset>\n')
    (stage / 'sitemap.txt').write_text('\n'.join(sorted(set(urls))) + '\n')
    (stage / '_headers').write_text('/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  X-Frame-Options: SAMEORIGIN\n')
    if site['domain'] == 'fxneurope.eu':
        (stage / '_redirects').write_text('/ /en/ 302\n/index.html /en/ 302\n')
        (stage / '_routes.json').write_text(json.dumps({'version':1,'include':['/netlify-forms.html','/__forms.html','/404','/404/','/404.html','/_not-found','/_not-found/'],'exclude':[]}))
    if output.exists():
        shutil.rmtree(output)
    stage.rename(output)
    print(f"Built {len(routes)} HTML documents for {site['domain']} in {output}")

if __name__ == '__main__':
    build()
