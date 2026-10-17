"""Objetivo 3: proporción de análisis profundos con al menos tres fuentes admitidas.

Reusa los veinte tuits redactados para RNF-02 (ajenos al conjunto de prueba real),
cada uno con un identificador nuevo para que no salga de la caché.
"""
import collections, json, urllib.request, uuid
from rnf02 import TUITS

conteos = []
for t in TUITS:
    cuerpo = {"tweet_id": "fuentes-" + uuid.uuid4().hex[:12], "texto": t, "handle": "@medicion",
              "verificada": False, "metricas": {}}
    p = urllib.request.Request("http://localhost:8000/analizar", json.dumps(cuerpo).encode(),
                               {"Content-Type": "application/json"})
    with urllib.request.urlopen(p, timeout=180) as r:
        d = json.load(r)
    fuentes = d.get("fuentes", [])
    conteos.append(len(fuentes))
    tipos = collections.Counter(f.get("tipo") for f in fuentes)
    print(f"{len(fuentes):2d} fuentes {dict(tipos)}  {d.get('veredicto')}  {t[:45]}", flush=True)
con3 = sum(c >= 3 for c in conteos)
print(f"n={len(conteos)} con_3_o_mas={con3} ({100*con3/len(conteos):.0f} %) mediana={sorted(conteos)[len(conteos)//2]} sin_fuentes={conteos.count(0)}")
