#!/bin/bash
# Serves the local copy of the website (the landing page, the kit pages and every guide published to it) on this computer, the
# way Render will serve models.tech-box.io, and opens it in your browser. Nothing here goes on the internet. Close this window
# to stop. The copy is share/Website preview/site, made by
#   python3 tools/publish.py <guide> --to "share/Website preview" --note "..."
# (a practice publish: it never touches site/ or releases/, which are what goes live).
cd "$(dirname "$0")"
PORT=8797
SITE="share/Website preview/site"
if ! /usr/bin/python3 -c '' >/dev/null 2>&1; then
  echo "Could not start a local web server. Install Python 3 (python.org) and try again."
  read -r -p "Press Return to close."
  exit 1
fi
if [ ! -f tools/serve.py ] || [ ! -f "$SITE/index.html" ]; then
  echo "There is no local copy of the website yet ($SITE). Ask Claude to make one:"
  echo "  python3 tools/publish.py <guide> --to \"share/Website preview\" --note \"...\""
  read -r -p "Press Return to close."
  exit 1
fi
if /usr/sbin/lsof -nP -iTCP:$PORT -sTCP:LISTEN >/dev/null 2>&1; then
  echo "Port $PORT is already in use (another window serving a copy of the website?). Opening http://localhost:$PORT/ ;"
  echo "if it shows an old copy, close that other window and double-click this again."
  open "http://localhost:$PORT/"
  read -r -p "Press Return to close."
  exit 0
fi
echo "Landing page: http://localhost:$PORT/"
(sleep 1; open "http://localhost:$PORT/") &
/usr/bin/python3 tools/serve.py "$SITE" $PORT
