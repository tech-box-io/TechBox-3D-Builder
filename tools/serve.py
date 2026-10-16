"""Local server for a kit folder.

    python tools/serve.py "<kit folder>" [port]

Serves the folder on http://localhost:<port> with caching switched off (so an edit always shows up on
reload), and lets the part-image and thumbnail tools save what they render back into the folder:

    POST /__save/parts/R1.png      body = the file

Saving only works for requests from this computer, only inside the kit's generated-output folders,
and only for image and JSON files.
"""
import http.server
import os
import sys
from pathlib import Path

SAVE_DIRS = ('parts', 'thumbs')
SAVE_TYPES = ('.png', '.webp', '.jpg', '.json', '.csv')
MAX_BYTES = 20 * 1024 * 1024


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map, '.glb': 'model/gltf-binary', '.js': 'text/javascript', '.webp': 'image/webp'}

    def parse_request(self):
        # Answer only when addressed as localhost: a web page elsewhere cannot then read this folder by pointing its own domain name at this computer.
        ok = super().parse_request()
        port = self.server.server_port
        if ok and self.headers.get('Host') not in (f'localhost:{port}', f'127.0.0.1:{port}'):
            self.send_error(403)
            return False
        return ok

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def do_POST(self):
        root = Path(self.directory).resolve()
        if not self.path.startswith('/__save/') or self.client_address[0] not in ('127.0.0.1', '::1'):
            return self.send_error(404)
        # Only pages served by this server may save (stops any other web page open in the browser from posting here).
        origin = self.headers.get('Origin')
        if origin and origin not in (f'http://localhost:{self.server.server_port}', f'http://127.0.0.1:{self.server.server_port}'):
            return self.send_error(403, 'Cross-site save refused')
        rel = Path(self.path[len('/__save/'):].split('?')[0])
        target = (root / rel).resolve()
        length = int(self.headers.get('Content-Length', 0))
        allowed = (len(rel.parts) >= 2 and rel.parts[0] in SAVE_DIRS and target.suffix.lower() in SAVE_TYPES
                   and root / rel.parts[0] in target.parents and 0 < length <= MAX_BYTES)     # inside that save folder itself, not merely inside the kit
        if not allowed:
            return self.send_error(403, 'Not a permitted save location')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(self.rfile.read(length))
        self.send_response(204)
        self.end_headers()

    def log_message(self, fmt, *args):
        if self.command == 'POST' or (args and str(args[1]).startswith(('4', '5'))):
            super().log_message(fmt, *args)


if __name__ == '__main__':
    folder = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8790
    os.chdir(folder)
    handler = lambda *a, **k: Handler(*a, directory=str(folder), **k)
    with http.server.ThreadingHTTPServer(('127.0.0.1', port), handler) as httpd:
        print(f'Serving {folder} at http://localhost:{port}/player.html  (Ctrl+C or close this window to stop)')
        httpd.serve_forever()
