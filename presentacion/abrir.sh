#!/usr/bin/env bash
# Levanta el deck en un servidor local y lo abre en el navegador.
#
# Va por servidor y no por doble clic sobre el archivo porque es el camino que
# quedó probado: con `file://` algunos navegadores restringen la reproducción
# del video de respaldo, y el día de la defensa no es el momento de
# averiguarlo. No usa internet: todo sale de esta carpeta.
set -euo pipefail

PUERTO="${PUERTO:-8777}"
cd "$(dirname "$0")"

# El deck prueba estos dos nombres en orden: QuickTime y la captura de pantalla
# de macOS guardan .mov, no .mp4.
DEMO=""
for f in img/demo-respaldo.mp4 img/demo-respaldo.mov; do
  [ -f "$f" ] && { DEMO="$f"; break; }
done
if [ -z "$DEMO" ]; then
  echo "Aviso: no hay demo grabada de respaldo — la lámina 10 va a mostrar el marcador."
  echo "       Guardala como img/demo-respaldo.mp4 o img/demo-respaldo.mov."
else
  echo "Demo de respaldo: $DEMO"
fi

python3 -m http.server "$PUERTO" >/dev/null 2>&1 &
SERVIDOR=$!
trap 'kill $SERVIDOR 2>/dev/null || true' EXIT

sleep 1
echo "Deck en http://127.0.0.1:$PUERTO  ·  Ctrl+C para cortar"
open "http://127.0.0.1:$PUERTO/index.html" 2>/dev/null || true
wait $SERVIDOR
