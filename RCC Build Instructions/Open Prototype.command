#!/bin/bash
# Serves this folder locally and opens the prototype in your browser. Close this window to stop.
cd "$(dirname "$0")"
PORT=8796
(sleep 1; open "http://localhost:$PORT/player.html") &
if /usr/bin/python3 -c '' >/dev/null 2>&1; then
  # Caching is switched off so an updated guide always shows on reload.
  /usr/bin/python3 -c '
import http.server, sys
class Handler(http.server.SimpleHTTPRequestHandler):
    def parse_request(self):
        ok = super().parse_request()
        if ok and self.headers.get("Host") not in ("localhost:" + sys.argv[1], "127.0.0.1:" + sys.argv[1]):
            self.send_error(403)
            return False
        return ok
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()
http.server.ThreadingHTTPServer(("127.0.0.1", int(sys.argv[1])), Handler).serve_forever()' $PORT
elif command -v ruby >/dev/null 2>&1; then
  echo "If the guide looks out of date after an update, reload the page with Cmd+Shift+R."
  ruby -run -e httpd . -p $PORT --bind-address=127.0.0.1
else
  echo "Could not start a local web server. Install Python 3 (python.org) and try again."
  read -r -p "Press Return to close."
fi
