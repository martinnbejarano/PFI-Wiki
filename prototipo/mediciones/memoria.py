"""Memoria semántica de evidencia (#103, PRD #100): umbral, latencia de un acierto y costo evitado.

1. Umbral (RNF-16). `memoria-pares.csv` tiene 62 pares armados sobre 31 titulares reales de
   la partición de prueba de FakeDeS (`clasificador/particiones.csv.gz`, columna `id`): por
   cada titular, una paráfrasis escrita a mano que debe acertar y un negativo difícil, del
   mismo tema con otro dato (otra cifra, otro actor, otro lugar o la negación), que debe
   fallar. El corpus argentino de RNF-05 no se usa: no está versionado y es reserva estricta.
   Se embeben con `POST /embeber` del Space, el mismo camino que usa el servicio, y se barre
   el umbral con y sin la guarda numérica de `memoria.py`. Se elige el de mayor precisión
   con la guarda, que es como corre el servicio: un falso acierto contrasta la publicación
   con evidencia ajena, una búsqueda de más solo cuesta tiempo.
2. Latencia de un acierto (RNF-02). Se siembra la memoria con los veinte tuits de `rnf02.py`
   y se analiza cada uno con un `tweet_id` nuevo por `POST /analizar`, con el servicio
   levantado con uvicorn y el proveedor compuesto real: el transporte HTTP, embeber,
   consultar sqlite-vec y recalcular clasificador, credibilidad, combinador y justificación. El LLM no tiene credencial, así que si el
   análisis lo llamara saldría parcial y el script corta. La línea base es la búsqueda web
   sobre los mismos veinte tuits, leída de `rnf02-2026-10-20.txt` (no se vuelve a pagar).
3. Costo evitado: un acierto no hace ninguna llamada al LLM, así que evita el costo entero
   del análisis profundo del modelo financiero (cap. 3, `tab:financiero-supuestos`).

Uso, desde `prototipo/` (BETO y el embebedor en local, `make clasificador`):

    servicio/.venv/bin/python mediciones/memoria.py [URL_DEL_SPACE]   # por defecto :7860
"""
import csv, json, os, statistics, subprocess, sys, tempfile, time, urllib.request, uuid
from pathlib import Path

import sqlite_vec

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "servicio"))
os.environ.pop("OPENAI_API_KEY", None)  # un acierto no debe necesitarla
from app.configuracion import Configuracion
from app.contrato import Fuente, TipoAfirmacion
from app.proveedor.memoria import ClienteEmbebedor, MemoriaDeEvidencia, _numeros, _Pendiente
from app.proveedor.openai import ProveedorOpenAI
from app.proveedor.puerto import AfirmacionExtraida
from rnf02 import TUITS

URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:7860"
PUERTO = os.environ.get("PUERTO", "8099")  # el servicio que levanta la medición de latencia
embebedor = ClienteEmbebedor(URL, tiempo_limite_s=30)

# -- 1. Umbral ------------------------------------------------------------------
pares = list(csv.DictReader(open(AQUI / "memoria-pares.csv", encoding="utf-8")))
vectores = {t: embebedor.embeber(t) for p in pares for t in (p["original"], p["variante"])}
for p in pares:
    # Los vectores vienen normalizados: el coseno es el producto escalar, igual que
    # `1 - distance` de sqlite-vec.
    p["similitud"] = sum(a * b for a, b in zip(vectores[p["original"]], vectores[p["variante"]]))
    p["cifras"] = _numeros(p["original"]) == _numeros(p["variante"])
positivos = sum(p["tipo"] == "parafrasis" for p in pares)


def medir(umbral, guarda):
    aciertos = [p for p in pares if p["similitud"] >= umbral and (p["cifras"] or not guarda)]
    vp = sum(p["tipo"] == "parafrasis" for p in aciertos)
    return (vp / len(aciertos) if aciertos else 1.0), vp / positivos, len(aciertos) - vp


# Entre los umbrales que dejan algún acierto (con ninguno la memoria no sirve y la
# precisión no está definida), el de mayor precisión con la guarda; ante empate, el
# menor, que es el de más recall.
umbrales = [u / 100 for u in range(50, 100)]
utiles = [u for u in umbrales if medir(u, True)[1] > 0]
mejor = max(medir(u, True)[0] for u in utiles)
elegido = min(u for u in utiles if medir(u, True)[0] == mejor)
print(f"# pares={len(pares)} parafrasis={positivos} negativos={len(pares) - positivos}")
print("umbral  sin guarda: precision recall FP  |  con guarda: precision recall FP")
for u in umbrales:
    if u >= 0.85 or round(u * 100) % 5 == 0:
        s, c = medir(u, False), medir(u, True)
        marca = "  <- elegido" if u == elegido else ""
        print(f"  {u:.2f}             {s[0]:.3f}  {s[1]:.3f} {s[2]:2d}  |              {c[0]:.3f}  {c[1]:.3f} {c[2]:2d}{marca}")
neg = [p for p in pares if p["tipo"] == "negativo"]
print(f"similitud negativos: max={max(p['similitud'] for p in neg):.3f} "
      f"max_que_pasa_la_guarda={max((p['similitud'] for p in neg if p['cifras']), default=0):.3f}")
print(f"similitud parafrasis: min={min(p['similitud'] for p in pares if p['tipo'] == 'parafrasis'):.3f}")
for p in pares:
    if (p["tipo"] == "parafrasis") != (p["similitud"] >= elegido and p["cifras"]):
        print(f"  error en {elegido:.2f}: {p['id']} {p['tipo']} sim={p['similitud']:.3f} "
              f"cifras_iguales={p['cifras']}  {p['variante'][:60]}")

# -- 2. Latencia de un acierto ------------------------------------------------------
configuracion = Configuracion(_env_file=None, adaptador="compuesto", url_clasificador=URL)
with tempfile.TemporaryDirectory() as carpeta:
    base = str(Path(carpeta) / "memoria.sqlite3")
    memoria = MemoriaDeEvidencia(ProveedorOpenAI(configuracion), embebedor, base, elegido,
                                 configuracion.vigencia_memoria_dias)
    fuente = Fuente(titulo="INDEC", url="https://www.indec.gob.ar/", tipo="fuente_oficial",
                    postura="corrobora", razon="Publica el dato.")
    for t in TUITS:  # la evidencia que habría dejado la búsqueda web de RNF-02
        extraida = AfirmacionExtraida(afirmacion=t, tipo=TipoAfirmacion.OTRO, puntaje=0.5, clase="sin_verificar")
        memoria._guardar(_Pendiente(t, extraida, [fuente], sqlite_vec.serialize_float32(embebedor.embeber(t)), None))

    # El servicio real por HTTP, como lo mide RNF-02 (`rnf02.py`): sin la
    # credencial del LLM, así que un análisis que lo llamara saldría parcial.
    entorno = {k: v for k, v in os.environ.items() if k != "OPENAI_API_KEY"}
    entorno.update(ADAPTADOR="compuesto", URL_CLASIFICADOR=URL, RUTA_BASE_DE_DATOS=base,
                   UMBRAL_SIMILITUD_MEMORIA=str(elegido))
    servicio = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:aplicacion", "--port", PUERTO],
        cwd=AQUI.parent / "servicio", env=entorno,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(60):
            try:
                urllib.request.urlopen(f"http://localhost:{PUERTO}/salud", timeout=1)
                break
            except OSError:
                time.sleep(0.5)

        def analizar(t):
            cuerpo = {"tweet_id": "memoria-" + uuid.uuid4().hex[:12], "texto": t, "handle": "@medicion"}
            pedido = urllib.request.Request(f"http://localhost:{PUERTO}/analizar", json.dumps(cuerpo).encode(),
                                            {"Content-Type": "application/json"})
            t0 = time.perf_counter()
            with urllib.request.urlopen(pedido, timeout=60) as r:
                respuesta = json.load(r)
            s = time.perf_counter() - t0
            assert not respuesta["analisis_parcial"]["es_parcial"], respuesta["analisis_parcial"]  # fue un acierto
            return s

        analizar(TUITS[0])  # calentamiento
        res = sorted(analizar(t) * 1000 for _ in range(5) for t in TUITS)
    finally:
        servicio.terminate()
        servicio.wait()

def p95(v):  # el mismo criterio de rnf02.py, para comparar igual con igual
    return v[min(len(v) - 1, int(round(0.95 * len(v) + 0.5)) - 1)]


web = sorted(float(l.split()[0]) for l in open(AQUI / "rnf02-2026-10-20.txt") if l.split()[1:2] == ["s"])
print(f"\n# latencia de un acierto: {len(TUITS)} tuits de rnf02.py x 5, embebedor, BETO y servicio locales, por HTTP ({URL})")
print(f"acierto      n={len(res)} mediana={statistics.median(res):.0f} ms p95={p95(res):.0f} ms max={res[-1]:.0f} ms")
print(f"busqueda web n={len(web)} mediana={statistics.median(web) * 1000:.0f} ms p95={p95(web) * 1000:.0f} ms "
      f"max={web[-1] * 1000:.0f} ms  (rnf02-2026-10-20.txt, mismos tuits, /analizar de extremo a extremo)")

# -- 3. Costo evitado ---------------------------------------------------------------
# Escenario neutral del modelo financiero (cap. 3, tab:financiero-supuestos y
# wiki/negocio/analisis-financiero.md §6.1): 2 llamadas a web_search a 0,01 USD y
# 0,0046 USD de fichas (RNF-14 midió 0,0044 sin el cargo por búsqueda).
BUSQUEDA, FICHAS = 0.0200, 0.0046
print(f"\n# costo evitado por acierto: {BUSQUEDA + FICHAS:.4f} USD = {BUSQUEDA:.4f} de búsqueda "
      f"({100 * BUSQUEDA / (BUSQUEDA + FICHAS):.0f} %) + {FICHAS:.4f} de fichas; el embebedor corre en el contenedor de BETO")
