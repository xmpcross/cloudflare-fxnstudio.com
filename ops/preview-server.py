#!/usr/bin/env python3
"""Serve preview-site/ for preview on 0.0.0.0:8793 with a noindex header."""
import functools, http.server, os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "preview-site")
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8793


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("X-Robots-Tag", "noindex, nofollow")
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


handler = functools.partial(Handler, directory=ROOT)
http.server.ThreadingHTTPServer(("0.0.0.0", PORT), handler).serve_forever()
