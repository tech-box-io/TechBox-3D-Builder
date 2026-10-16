"""Local server, for this computer only.

    python tools/serve.py "<kit folder>" [port]    a kit while it is being written: http://localhost:<port>/player.html
    python tools/serve.py site [port]              the published site, as Render serves it: http://localhost:<port>/<guide>/
    python tools/serve.py releases [port]          every release ever published (never uploaded): http://localhost:<port>/<guide>/r3/

A kit folder holds only its content (steps.json, model.glb, parts/, logo); the player (player.html, parts.html, js/, vendor/)
comes from the one copy in player/, as if it were in the kit folder. The site and the releases hold their own frozen copy of
the player; only the check script (js/runthrough.js, never published) is lent to them from player/.

Caching is switched off, so an edit always shows up on reload. For a kit, the part-image and thumbnail tools can save what they
render back into the folder:

    POST /__save/parts/R1.png      body = the file

Saving only works for requests from this computer, only inside the kit's generated-output folders, and only for image and JSON
files.
"""
import http.server
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLAYER = ROOT / 'player'                     # the one copy of the player
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

    def translate_path(self, path):
        local = super().translate_path(path)
        if os.path.exists(local):
            return local
        base, target = Path(self.directory).resolve(), Path(local).resolve()
        if not target.is_relative_to(base):
            return local
        rel = target.relative_to(base)
        if self.server.kind == 'kit':                                # the player, from player/
            lent = (PLAYER / rel).resolve()
        elif rel.parts[-2:] == ('js', 'runthrough.js'):              # the check script, for a published copy
            lent = PLAYER / 'js' / 'runthrough.js'
        else:
            return local
        return str(lent) if PLAYER in lent.parents and lent.exists() else local

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def do_POST(self):
        root = Path(self.directory).resolve()
        if self.server.kind != 'kit' or not self.path.startswith('/__save/') or self.client_address[0] not in ('127.0.0.1', '::1'):
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
    folder = Path(sys.argv[1] if len(sys.argv) > 1 else '.')
    folder = (folder if folder.is_absolute() or folder.exists() else ROOT / folder).resolve()
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8797
    kind = folder.name if folder.name in ('site', 'releases') else 'kit'       # (a practice publish's site/ and releases/ too)
    os.chdir(folder)
    handler = lambda *a, **k: Handler(*a, directory=str(folder), **k)
    with http.server.ThreadingHTTPServer(('127.0.0.1', port), handler) as httpd:
        httpd.kind = kind
        start = {'kit': 'player.html', 'site': '<guide>/', 'releases': '<guide>/r<N>/'}[kind]
        print(f'Serving {folder} at http://localhost:{port}/{start}  (Ctrl+C or close this window to stop)')
        httpd.serve_forever()
