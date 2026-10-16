#!/bin/bash
# Serves this kit on this computer (its content, with the one player from player/) and opens it in your browser.
# Close this window to stop.
cd "$(dirname "$0")"
KIT="$(basename "$PWD")"
PORT=8795
cd ..
if ! /usr/bin/python3 -c '' >/dev/null 2>&1; then
  echo "Could not start a local web server. Install Python 3 (python.org) and try again."
  read -r -p "Press Return to close."
  exit 1
fi
if [ ! -f tools/serve.py ] || [ ! -f player/player.html ]; then
  echo "This kit folder must stay inside the Claude_Cadasio folder (to send a guide to someone, use tools/bundle.py)."
  read -r -p "Press Return to close."
  exit 1
fi
(sleep 1; open "http://localhost:$PORT/player.html") &
/usr/bin/python3 tools/serve.py "$KIT" $PORT
