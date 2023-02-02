#!/usr/bin/env python3

from http.server import HTTPServer, SimpleHTTPRequestHandler

print("http://localhost:8080")
httpd = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
httpd.serve_forever()
