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

if [ ! -f img/demo.mp4 ]; then
  echo "Aviso: falta img/demo.mp4 — la lámina 8 va a mostrar el marcador."
fi

python3 -m http.server "$PUERTO" >/dev/null 2>&1 &
SERVIDOR=$!
trap 'kill $SERVIDOR 2>/dev/null || true' EXIT

sleep 1
echo "Deck en http://127.0.0.1:$PUERTO  ·  Ctrl+C para cortar"
open "http://127.0.0.1:$PUERTO/index.html" 2>/dev/null || true
wait $SERVIDOR
