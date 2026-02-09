#!/usr/bin/env python3
"""
Simple local server for auto-saving test definitions.
Run this script, then open http://localhost:8080 in your browser.
Supports Firefox and all other browsers.
"""

import http.server
import json
import os
from urllib.parse import urlparse

PORT = 8080
DOCS_DIR = os.path.dirname(os.path.abspath(__file__))

class SaveHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DOCS_DIR, **kwargs)

    def do_POST(self):
        """Handle POST requests to save files"""
        parsed = urlparse(self.path)

        if parsed.path == '/save-definitions':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            try:
                # Validate JSON
                data = json.loads(post_data)

                # Save to file
                filepath = os.path.join(DOCS_DIR, 'test-definitions.json')
                with open(filepath, 'w') as f:
                    json.dump(data, f, indent=2)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'ok'}).encode())
                print(f"Saved test-definitions.json")

            except json.JSONDecodeError as e:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())

            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())

        elif parsed.path == '/save-data':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            try:
                data = json.loads(post_data)
                filepath = os.path.join(DOCS_DIR, 'test-data.json')
                with open(filepath, 'w') as f:
                    json.dump(data, f, indent=2)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'ok'}).encode())
                print(f"Saved test-data.json")

            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    print(f"Starting server at http://localhost:{PORT}")
    print(f"Serving files from: {DOCS_DIR}")
    print(f"Press Ctrl+C to stop")
    print()

    with http.server.HTTPServer(('', PORT), SaveHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
