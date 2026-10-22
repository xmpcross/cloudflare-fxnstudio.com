#!/usr/bin/env python3
"""Verify exported page fidelity, local links/assets, CSS URLs and sitemap."""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ('href', 'src', 'poster', 'action'):
            if attrs.get(key): self.links.append(attrs[key])
        if attrs.get('srcset') and not attrs['srcset'].startswith('data:'):
            self.links.extend(part.strip().split()[0] for part in attrs['srcset'].split(',') if part.strip())

def verify():
    domain = json.loads((ROOT / 'site.json').read_text())['domain']
    routes = json.loads((ROOT / 'routes.json').read_text())
    dist = ROOT / 'dist'
    errors = set()
    checks = 0
    def check(link, base):
        nonlocal checks
        if link.startswith(('#', '%23')): return
        url = urlsplit(urljoin(base, link))
        if url.scheme not in ('http','https') or url.netloc != domain: return
        path = unquote(url.path).lstrip('/')
        checks += 1
        if not any(f.is_file() for f in (dist / path, dist / path / 'index.html')):
            errors.add(f'{base}: missing {url.path}')
    for route in routes:
        path = route['file']
        assert (dist / path).read_bytes() == (ROOT / 'content' / path).read_bytes(), path
        html = (dist / path).read_text()
        parser = Links(); parser.feed(html)
        base = f'https://{domain}/' + path.removesuffix('index.html')
        for link in parser.links: check(link, base)
        for link in re.findall(r'url\([\s\'"]*([^\)\'"\s]+)',html): check(link,base)
    for file in dist.rglob('*.css'):
        for link in re.findall(r'url\([\s\'"]*([^\)\'"\s]+)', re.sub(r'/\*.*?\*/', '', file.read_text(), flags=re.S)):
            check(link, f'https://{domain}/'+str(file.relative_to(dist)))
    sitemap = ET.parse(dist / 'sitemap.xml')
    for loc in sitemap.findall('.//{*}loc'): check(loc.text, f'https://{domain}/')
    assert (dist / '404.html').is_file()
    if errors:
        print('\n'.join(sorted(errors)), file=sys.stderr)
        sys.exit(1)
    print(f'PASS: {len(routes)} pages identical to source; {checks} local links/assets checked; sitemap and 404 present.')

if __name__ == '__main__': verify()
