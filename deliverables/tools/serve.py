#!/usr/bin/env python3
"""Serve the deliverables site (and the raw file downloads) on 0.0.0.0:8000.

Run:  /home/user/pdfenv/bin/python tools/serve.py
"""
import functools
import http.server
import os
import socketserver
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = os.path.join(ROOT, "site")
PORT = int(os.environ.get("PORT", "8000"))


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # allow the platform preview proxy/iframe and inline downloads
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


def main():
    handler = functools.partial(Handler, directory=SITE)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("0.0.0.0", PORT), handler) as httpd:
        print("serving %s at http://0.0.0.0:%d" % (SITE, PORT), flush=True)
        httpd.serve_forever()


if __name__ == "__main__":
    main()
