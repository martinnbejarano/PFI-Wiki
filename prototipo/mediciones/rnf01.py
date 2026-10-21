"""RNF-01: latencia de POST /senales (flujo automático) por lote de publicaciones visibles.

Mide el tramo servicio + clasificador del camino que va del ingreso del tuit en pantalla
al indicador. Lo que falta para el total —la ventana de agrupamiento del service worker
(150 ms), el cuadro del IntersectionObserver y el mensaje entre contextos— se suma aparte.
Uso: python rnf01.py [URL]   (por defecto http://localhost:8000/senales)
"""
import json, math, statistics, sys, time, urllib.request
URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000/senales"
TEXTOS = ["El INDEC informó que la desocupación fue del 7,6 % en el segundo trimestre.",
          "Confirmaron que el aguinaldo de diciembre se paga en tres cuotas.",
          "URGENTE: desde mañana se prohíbe circular sin el nuevo carnet digital. Compartí!",
          "Qué lindo día para ir a la cancha, vamos todavía.",
          "El Gobierno anunció que el feriado del 20 de noviembre se traslada al lunes.",
          "Dicen que la vacuna de la gripe trae un chip, ojo con lo que se aplican.",
          "Mañana corte de luz programado en todo el conurbano según Edenor.",
          "Se aprobó la ley que elimina el examen de ingreso en todas las universidades."]
def pedir(n, i):
    lote = [{"tweet_id": f"rnf01-{i}-{k}", "texto": TEXTOS[(i + k) % len(TEXTOS)]} for k in range(n)]
    p = urllib.request.Request(URL, json.dumps({"publicaciones": lote}).encode(), {"Content-Type": "application/json"})
    t0 = time.perf_counter()
    with urllib.request.urlopen(p, timeout=30) as r: cuerpo = json.load(r)
    assert len(cuerpo["senales"]) == n, cuerpo
    return (time.perf_counter() - t0) * 1000
pedir(1, -1)  # calentamiento
for n in (1, 5, 10, 20):
    res = sorted(pedir(n, i) for i in range(50))
    p95 = res[math.ceil(0.95 * len(res)) - 1]
    print(f"lote={n:2d} n={len(res)} mediana={statistics.median(res):.0f} ms p95={p95:.0f} ms max={res[-1]:.0f} ms")
