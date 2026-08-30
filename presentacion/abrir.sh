#!/usr/bin/env bash
# Levanta el deck en un servidor local y lo abre en el navegador.
#
# Va por servidor y no por doble clic sobre el archivo porque es el camino que
# quedó probado: con `file://` algunos navegadores restringen la reproducción
# del video de la demostración, y el día de la defensa no es el momento de
# averiguarlo. No usa internet: todo sale de esta carpeta.
set -euo pipefail

PUERTO="${PUERTO:-8777}"
cd "$(dirname "$0")"

# El deck prueba estos cuatro nombres en orden y se queda con el primero que
# exista: QuickTime y la captura de pantalla de macOS guardan .mov, no .mp4.
DEMO=""
for f in img/demo.mp4 img/demo.mov img/demo.m4v img/demo.webm; do
  [ -f "$f" ] && { DEMO="$f"; break; }
done
if [ -z "$DEMO" ]; then
  echo "Aviso: no hay video de demostración — la lámina 9 va a mostrar el marcador."
  echo "       Guardalo como img/demo.mp4, img/demo.mov, img/demo.m4v o img/demo.webm."
else
  echo "Video de la demostración: $DEMO"
fi

python3 -m http.server "$PUERTO" >/dev/null 2>&1 &
SERVIDOR=$!
trap 'kill $SERVIDOR 2>/dev/null || true' EXIT

sleep 1
echo "Deck en http://127.0.0.1:$PUERTO  ·  Ctrl+C para cortar"
open "http://127.0.0.1:$PUERTO/index.html" 2>/dev/null || true
wait $SERVIDOR
