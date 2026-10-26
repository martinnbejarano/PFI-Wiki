#!/usr/bin/env bash
# Corre chequeo.js sobre un deck servido en local con Chrome sin ventana y
# exporta su PDF. Sale con error si el chequeo falla.
#   ./chequear.sh              → index.html  → PRESENTACION.pdf
#   ./chequear.sh factum.html  → factum.html → factum.pdf
set -euo pipefail
cd "$(dirname "$0")"
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
PUERTO="${PUERTO:-8778}"
DECK="${1:-index.html}"
if [ "$DECK" = index.html ]; then PDF=PRESENTACION.pdf; else PDF="${DECK%.html}.pdf"; fi

python3 -m http.server "$PUERTO" >/dev/null 2>&1 &
SERVIDOR=$!
trap 'kill $SERVIDOR 2>/dev/null || true' EXIT
sleep 1

SALIDA=$("$CHROME" --headless=new --disable-gpu --window-size=1600,900 \
  --virtual-time-budget=6000 --dump-dom "http://127.0.0.1:$PUERTO/$DECK?chequeo" 2>/dev/null \
  | sed -n '/<pre id="chequeo">/,/<\/pre>/p' | sed 's/<[^>]*>//g')
echo "${SALIDA:-CHEQUEO FALLA: el deck no escribió resultado}"

"$CHROME" --headless=new --disable-gpu --no-pdf-header-footer \
  --virtual-time-budget=4000 --print-to-pdf="$PDF" \
  "http://127.0.0.1:$PUERTO/$DECK" 2>/dev/null
echo "PDF: presentacion/$PDF"

[[ "$SALIDA" == "CHEQUEO OK"* ]]
