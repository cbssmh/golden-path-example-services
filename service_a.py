#!/usr/bin/env python3
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class ServiceAHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            self.send_error(404)
            return
        payload = json.dumps(
            {"service": "service-a", "version": "0.1.0", "status": "running"}
        ).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format, *args):
        return


def main():
    port = int(os.environ.get("SERVICE_PORT", "8080"))
    ThreadingHTTPServer(("0.0.0.0", port), ServiceAHandler).serve_forever()


if __name__ == "__main__":
    main()
