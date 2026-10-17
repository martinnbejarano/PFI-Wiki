"""RNF-03: tiempo de respuesta de /analizar para tuits ya analizados (acierto de caché), bajo carga."""
import json, math, statistics, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
URL = "http://localhost:8000/analizar"
TUITS = {"rnf03-a": "El INDEC informó que la desocupación fue del 7,6 % en el segundo trimestre.",
         "rnf03-b": "Confirmaron que el aguinaldo de diciembre se paga en tres cuotas.",
         "rnf03-c": "El Gobierno anunció que el feriado del 20 de noviembre se traslada al lunes."}
def pedir(tid):
    cuerpo = {"tweet_id": tid, "texto": TUITS[tid], "handle": "@medicion", "verificada": False, "metricas": {}}
    p = urllib.request.Request(URL, json.dumps(cuerpo).encode(), {"Content-Type": "application/json"})
    t0 = time.perf_counter()
    with urllib.request.urlopen(p, timeout=120) as r: r.read()
    return time.perf_counter() - t0
for tid in TUITS: print(f"primer análisis {tid}: {pedir(tid):.1f} s", flush=True)
ids = [t for t in TUITS for _ in range(100)]
for conc in (1, 10):
    t0 = time.perf_counter()
    with ThreadPoolExecutor(conc) as ex: res = sorted(x*1000 for x in ex.map(pedir, ids))
    tot = time.perf_counter() - t0
    p95 = res[math.ceil(0.95*len(res))-1]
    print(f"concurrencia={conc} n={len(res)} mediana={statistics.median(res):.1f} ms p95={p95:.1f} ms max={res[-1]:.1f} ms  ({len(res)/tot:.0f} pedidos/s)")
