#!/usr/bin/env python3
"""Read-only smoke check of every published route on a deployed site."""
import concurrent.futures
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
base = sys.argv[1].rstrip('/')
routes = json.loads((ROOT / 'routes.json').read_text())
def fetch(path):
    request = urllib.request.Request(base + path, headers={'User-Agent':'FXN migration verification'})
    try:
        response = urllib.request.urlopen(request, timeout=30)
    except urllib.error.HTTPError as error:
        response = error
    return response.status, response.read(), response.headers

def check(route):
    path = route['path']
    if path != '/' and '.' not in path.rsplit('/',1)[-1]: path += '/'
    status, body, headers = fetch(path)
    assert status == route['status'], f'{path}: HTTP {status}, expected {route["status"]}'
    if route['status'] == 200:
        assert headers.get('X-Content-Type-Options') == 'nosniff', f'{path}: missing security header'
        if path != '/':
            original = (ROOT / 'content' / route['file']).read_text()
            title = re.search(r'<title[^>]*>(.*?)</title>', original, re.S|re.I).group(1)
            assert title in body.decode(), f'{path}: title mismatch'
    return path
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    checked = list(pool.map(check, routes))
for path in ['/migration-missing-page-check/', '/admin', '/api/users']:
    status, _, _ = fetch(path)
    assert status == 404, f'{path}: expected 404, got {status}'
assert fetch('/sitemap.xml')[0] == 200
assert fetch('/robots.txt')[0] == 200
print(json.dumps({'base':base,'pages':len(checked),'all_passed':True,'checked':['page status and titles','security headers','404','admin/API disabled','sitemap','robots']}))
