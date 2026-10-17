#!/usr/bin/env bash
# Renderiza svg/*.svg → documento/chapters/figures/<nombre>.png a 2× el viewBox.
# Uso: ./render.sh            (todos)
#      ./render.sh c4-componentes [otro ...]
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
FIGS="$DIR/../../../../documento/chapters/figures"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ESCALA=2
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

if [ $# -eq 0 ]; then set -- $(cd "$DIR" && ls *.svg | grep -v '^_' | sed 's/\.svg$//'); fi

for nombre in "$@"; do
  svg="$DIR/$nombre.svg"
  read -r _ _ w h < <(grep -o 'viewBox="[^"]*"' "$svg" | head -1 | tr -d '"' | sed 's/viewBox=//')
  # Envoltorio sin márgenes: la ventana mide exactamente el viewBox.
  printf '<!doctype html><meta charset="utf-8"><style>html,body{margin:0;background:#fff}img{display:block}</style><img src="file://%s" width="%s" height="%s">' \
    "$svg" "$w" "$h" > "$TMP/$nombre.html"
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --allow-file-access-from-files \
    --default-background-color=ffffffff --force-device-scale-factor=$ESCALA \
    --window-size="$w,$h" --screenshot="$FIGS/$nombre.png" "file://$TMP/$nombre.html" >/dev/null 2>&1
  echo "✓ $nombre.png  $(sips -g pixelWidth -g pixelHeight "$FIGS/$nombre.png" | awk '/pixel/{printf "%s ", $2}')px"
done
