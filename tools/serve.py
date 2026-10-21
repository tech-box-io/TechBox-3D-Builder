"""Local server, for this computer only.

    python tools/serve.py "<kit folder>" [port]    a kit while it is being written: http://localhost:<port>/player.html
    python tools/serve.py site [port]              the published site, as Render serves it: http://localhost:8797/<guide>/
    python tools/serve.py releases [port]          every release ever published (never uploaded): http://localhost:8798/<guide>/r3/

A kit folder (one with a guide.py) holds only its content (steps.json, model.glb, parts/, logo); the player (player.html,
parts.html, js/, vendor/) comes from the one copy in player/, as if it were in the kit folder. Any other folder is served as a
published copy: it holds its own frozen player, and only the check script (js/runthrough.js, never published) is lent to it
from player/. A site folder is served the way Render serves one: /<guide> answers with its index.html (no redirect), a missing
file with site/404.html, folders are not listed, and render.yaml's headers are sent (Cache-Control apart), so that framing can
be tried here too.

Caching is switched off, so an edit always shows up on reload. For a kit, the part-image and thumbnail tools can save what they
render back into the folder:

    POST /__save/parts/R1.png      body = the file     (also thumbs/, cards/: the guide's picture for the website, and pages/: the PDF's)

Saving only works for requests from this computer, only inside the kit's generated-output folders, and only for image and JSON
files.
"""
import http.server
import os
import posixpath
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLAYER = ROOT / 'player'                     # the one copy of the player
PLAYER_NAMES = ('player.html', 'parts.html', 'js', 'vendor')
SAVE_DIRS = ('parts', 'thumbs', 'cards', 'pages')                # (pages: the 2D PDF's pictures, js/pages.js; not kept in git)
SAVE_TYPES = ('.png', '.webp', '.jpg', '.json', '.csv')
MAX_BYTES = 20 * 1024 * 1024
PORTS = {'site': 8797, 'releases': 8798, 'kit': 8791}


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

    def url_parts(self, path):
        """The request's path as parts below the served folder, or None if it tries to climb out."""
        rel = urllib.parse.unquote(path.split('?', 1)[0].split('#', 1)[0])
        parts = [p for p in posixpath.normpath('/' + rel).split('/') if p]
        return None if '..' in parts else parts

    def translate_path(self, path):
        local = super().translate_path(path)
        parts = self.url_parts(path)
        if os.path.exists(local) or not parts:
            return local
        if self.server.kind == 'kit':                                # the player, from player/
            lent = PLAYER.joinpath(*parts)
        elif parts[-2:] == ['js', 'runthrough.js']:                  # the check script, for a published copy
            lent = PLAYER / 'js' / 'runthrough.js'
        else:
            return local
        lent = lent.resolve()
        return str(lent) if PLAYER.resolve() in lent.parents and lent.is_file() else local

    def send_head(self):
        if self.server.kind == 'site':                               # as Render: no redirects, no listings, our own 404 page
            local = Path(self.translate_path(self.path))
            if local.is_dir():
                if (local / 'index.html').is_file():
                    self.path = self.path.split('?', 1)[0].rstrip('/') + '/index.html'
                else:
                    return self.not_found()
            elif not local.exists():
                return self.not_found()
        return super().send_head()

    def not_found(self):
        page = Path(self.directory) / '404.html'
        body = page.read_bytes() if page.is_file() else b'Not found'
        self.send_response(404)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        if self.command != 'HEAD':
            self.wfile.write(body)
        return None

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        if self.server.kind == 'site':                               # the website's headers (render.yaml), so framing can be tried here
            path = urllib.parse.unquote(self.path.split('?', 1)[0])
            for rule, name, value in self.server.headers:
                if name.lower() != 'cache-control' and (rule == '/*' or rule == path or (rule.endswith('/*') and path.startswith(rule[:-1]))):
                    self.send_header(name, value)
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
    kind = 'kit' if (folder / 'guide.py').exists() else ('releases' if folder.name == 'releases' else 'site')
    port = int(sys.argv[2]) if len(sys.argv) > 2 else PORTS[kind]
    if kind == 'kit':
        stray = [n for n in PLAYER_NAMES if (folder / n).exists()]
        if stray:
            print(f'WARNING: {folder.name} has its own {", ".join(stray)}: those are served instead of the one player in player/; '
                  'delete them from the kit folder')
    os.chdir(folder)
    handler = lambda *a, **k: Handler(*a, directory=str(folder), **k)
    with http.server.ThreadingHTTPServer(('127.0.0.1', port), handler) as httpd:
        httpd.kind = kind
        httpd.headers = []
        if kind == 'site' and (ROOT / 'render.yaml').is_file():
            sys.path.insert(0, str(Path(__file__).resolve().parent))
            from check_site import header_rules
            httpd.headers = header_rules((ROOT / 'render.yaml').read_text())
        start = {'kit': 'player.html', 'site': '<guide>/', 'releases': '<guide>/r<N>/'}[kind]
        print(f'Serving {folder} ({kind}) at http://localhost:{port}/{start}  (Ctrl+C or close this window to stop)')
        httpd.serve_forever()
