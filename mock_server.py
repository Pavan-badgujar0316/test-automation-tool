"""A tiny local web server used as the system under test.
Run:  python mock_server.py   (serves on http://localhost:8000)
"""
import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

ITEMS = [
    {"id": 1, "name": "Sword", "price": 120},
    {"id": 2, "name": "Shield", "price": 90},
]


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, payload):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self._send(200, {"status": "ok"})
        elif self.path == "/items":
            self._send(200, ITEMS)
        elif self.path == "/items/1":
            self._send(200, ITEMS[0])
        elif self.path == "/slow":
            time.sleep(1.5)  # simulates a slow endpoint
            self._send(200, {"status": "slow but ok"})
        else:
            self._send(404, {"error": "not found"})

    def log_message(self, *args):  # keep the console quiet
        pass


if __name__ == "__main__":
    print("Mock server running on http://localhost:8000 (Ctrl+C to stop)")
    HTTPServer(("localhost", 8000), Handler).serve_forever()
