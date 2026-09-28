#!/bin/sh
# Regenera las capturas PNG de mockups.html a doble resolución.
# Uso: sh capturar.sh [directorio_salida]   (por defecto, este directorio)
# Después copiar las PNG a documento/chapters/figures/ y presentacion/img/.
set -e
cd "$(dirname "$0")"
OUT="${1:-.}"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PUERTO=48731
python3 -m http.server "$PUERTO" --bind 127.0.0.1 >/dev/null 2>&1 &
SRV=$!
trap 'kill $SRV' EXIT
sleep 1
# pantalla  ancho  alto  (px CSS; la PNG sale al doble). El popup es más alto
# desde que el detalle lleva la aclaración de cómo se analiza.
for p in "badge 900 1010" "popup 900 1080" "evidencia 1000 1260" "dashboard 900 1010"; do
  set -- $p
  "$CHROME" --headless=new --force-device-scale-factor=2 --hide-scrollbars \
    --window-size="$2,$3" --screenshot="$OUT/$1.png" \
    "http://127.0.0.1:$PUERTO/mockups.html?pantalla=$1&captura=1" 2>/dev/null
done
