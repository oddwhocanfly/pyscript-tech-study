#!/usr/bin/env python3

from http.server import HTTPServer, SimpleHTTPRequestHandler

HOST = 'localhost'
PORT = 8000

class NoCacheHTTPRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        SimpleHTTPRequestHandler.end_headers(self)

if __name__ == '__main__':
    print(f'http://{HOST}:{PORT}')
    server = HTTPServer((HOST, PORT), NoCacheHTTPRequestHandler)
    server.serve_forever()

