"""Índice de fuentes oficiales (#112, PRD #107): efecto sobre publicaciones recientes.

`indice-publicaciones.csv` tiene el texto y la URL de 10 a 20 publicaciones recientes de X
sobre datos oficiales, juntadas a mano por el autor. Cada una se analiza por `POST /analizar`
contra dos servicios levantados con uvicorn y el proveedor compuesto real, sobre una copia
de la base con el índice cargado:

- con índice: la configuración del servicio (`FRAGMENTOS_INDICE`, `UMBRAL_SIMILITUD_INDICE`);
- sin índice: `UMBRAL_SIMILITUD_INDICE=1.01`, ningún fragmento llega al LLM. Todo lo demás es igual.

La memoria se apaga en los dos (`UMBRAL_SIMILITUD_MEMORIA=1.01`): un acierto no consulta el
índice, y el segundo análisis de un mismo texto acertaría. La copia de la base evita que la
medición deje histórico o memoria en la base real. Los fragmentos entregados y la similitud
máxima salen de `IndiceDeFuentes.buscar` con el mismo embebedor y el mismo K que el adaptador;
una fuente del resultado es del índice si su URL está indexada (`indexada`). Paga dos análisis
profundos por publicación. No toca RNF-05.

Uso, desde `prototipo/` (BETO y el embebedor en local, `make clasificador`; `OPENAI_API_KEY`
en el entorno o en `servicio/.env`; la base con el índice en `RUTA_BASE_DE_DATOS`):

    servicio/.venv/bin/python mediciones/indice.py [URL_DEL_SPACE] | tee mediciones/indice-AAAA-MM-DD.txt
"""
import csv, json, os, sqlite3, statistics, subprocess, sys, tempfile, time, urllib.request, uuid
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "servicio"))
from app.configuracion import Configuracion
from app.proveedor.indice import IndiceDeFuentes
from app.proveedor.memoria import ClienteEmbebedor

URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:7860"
PUERTO = int(os.environ.get("PUERTO", "8099"))  # con índice; sin índice en el siguiente
casos = list(csv.DictReader(open(AQUI / "indice-publicaciones.csv", encoding="utf-8")))
if not casos:
    sys.exit("# casos=0: indice-publicaciones.csv no tiene publicaciones (texto,url)")
configuracion = Configuracion()
if not Path(configuracion.ruta_base_de_datos).exists():
    sys.exit(f"no existe la base con el índice: {configuracion.ruta_base_de_datos}")
if not configuracion.openai_api_key:
    sys.exit("falta OPENAI_API_KEY: sin ella cada análisis sale parcial")
K, UMBRAL = configuracion.fragmentos_indice, configuracion.umbral_similitud_indice


def p95(v):  # el mismo criterio de rnf02.py
    return v[min(len(v) - 1, int(round(0.95 * len(v) + 0.5)) - 1)]


def analizar(puerto, texto):
    cuerpo = {"tweet_id": "indice-" + uuid.uuid4().hex[:12], "texto": texto, "handle": "@medicion",
              "verificada": False, "metricas": {}}
    pedido = urllib.request.Request(f"http://localhost:{puerto}/analizar", json.dumps(cuerpo).encode(),
                                    {"Content-Type": "application/json"})
    t0 = time.perf_counter()
    with urllib.request.urlopen(pedido, timeout=180) as r:
        respuesta = json.load(r)
    return respuesta, time.perf_counter() - t0


with tempfile.TemporaryDirectory() as carpeta:
    base = str(Path(carpeta) / "medicion.sqlite3")
    with sqlite3.connect(configuracion.ruta_base_de_datos) as origen, sqlite3.connect(base) as copia:
        origen.backup(copia)
    indice = IndiceDeFuentes(base, ClienteEmbebedor(URL, tiempo_limite_s=30))
    comun = dict(os.environ, ADAPTADOR="compuesto", URL_CLASIFICADOR=URL, URL_EMBEBEDOR=URL,
                 RUTA_BASE_DE_DATOS=base, UMBRAL_SIMILITUD_MEMORIA="1.01")
    servicios = [subprocess.Popen([sys.executable, "-m", "uvicorn", "app.main:aplicacion", "--port", str(p)],
                                  cwd=AQUI.parent / "servicio", env=entorno,
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                 for p, entorno in ((PUERTO, comun), (PUERTO + 1, dict(comun, UMBRAL_SIMILITUD_INDICE="1.01")))]
    filas = []
    try:
        for p in (PUERTO, PUERTO + 1):
            for _ in range(60):
                try:
                    urllib.request.urlopen(f"http://localhost:{p}/salud", timeout=1)
                    break
                except OSError:
                    time.sleep(0.5)
        print(f"# casos={len(casos)} K={K} umbral={UMBRAL} embebedor={URL} base={configuracion.ruta_base_de_datos}")
        print("frag sim_max indice con_indice -> sin_indice  lat_con lat_sin  url")
        for c in casos:
            cercanos = indice.buscar(c["texto"], K)
            maxima = cercanos[0][1] if cercanos else 0.0
            entregados = sum(s >= UMBRAL for _, s in cercanos)
            con, s_con = analizar(PUERTO, c["texto"])
            sin, s_sin = analizar(PUERTO + 1, c["texto"])
            acierto = any(indice.indexada(f["url"]) for f in con["fuentes"])
            parcial = " PARCIAL" if con["analisis_parcial"]["es_parcial"] or sin["analisis_parcial"]["es_parcial"] else ""
            filas.append((entregados, maxima, acierto, con["veredicto"], sin["veredicto"], s_con, s_sin))
            print(f"{entregados:4d}   {maxima:.3f} {'si' if acierto else 'no':>6} {con['veredicto']} -> "
                  f"{sin['veredicto']}  {s_con:5.1f} s {s_sin:5.1f} s  {c['url']}{parcial}", flush=True)
    finally:
        for s in servicios:
            s.terminate()
            s.wait()

n = len(filas)
aciertos = sum(f[2] for f in filas)
cambian = sum(f[3] != f[4] for f in filas)
print(f"\n# totales n={n}")
print(f"aciertos del índice={aciertos} ({100 * aciertos / n:.0f} %)  con fragmentos entregados={sum(f[0] > 0 for f in filas)}"
      f"  veredictos que cambian={cambian} ({100 * cambian / n:.0f} %)")
for nombre, i in (("con índice", 5), ("sin índice", 6)):
    lat = sorted(f[i] for f in filas)
    print(f"latencia {nombre}: mediana={statistics.median(lat):.1f} s p95={p95(lat):.1f} s max={lat[-1]:.1f} s")

# Para calibrar UMBRAL_SIMILITUD_INDICE: la similitud máxima de cada caso y cuántos casos
# recibirían al menos un fragmento con cada umbral.
maximas = sorted(f[1] for f in filas)
print(f"\n# similitud máxima por caso: {' '.join(f'{m:.3f}' for m in maximas)}")
print(f"min={maximas[0]:.3f} mediana={statistics.median(maximas):.3f} max={maximas[-1]:.3f}")
for u in [x / 100 for x in range(30, 80, 5)]:
    print(f"  umbral {u:.2f}: {sum(m >= u for m in maximas):2d} de {n} casos con fragmentos" + ("  <- actual" if u == UMBRAL else ""))
