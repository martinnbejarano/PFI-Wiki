"""Evaluación del sistema completo sobre el corpus argentino (RNF-05 reformulado, #36).

Manda cada uno de los 108 tuits a `POST /analizar` del servicio y compara el veredicto
con la etiqueta. Mide lo que ve el usuario: clasificador + contraste con fuentes +
combinador, no el clasificador solo.

Correspondencia fijada antes de correr (cap. 4, `sec:resultados-argentino`):

- `contradicho_por_fuentes_oficiales` e `informacion_sospechosa` → falso
- `parece_verificado` → verdadero
- `sin_contraste_externo`, sin afirmación o sin extracción → sin veredicto, que cuenta
  como error en las dos clases (el F1 macro no premia abstenerse)

Se levantan dos procesos y después se corre este *script* (todo desde `prototipo/`):

    cd clasificador && MODELO=<carpeta de beto_fakedes-chequeado_s42> .venv/bin/uvicorn space.app:app --port 7861
    cd servicio && ADAPTADOR=compuesto URL_CLASIFICADOR=http://localhost:7861 .venv/bin/uvicorn app.main:aplicacion --port 8000
    cd clasificador && .venv/bin/python evaluar_sistema.py

Las respuestas quedan en `cache_sistema/<conjunto>/` (fuera de git: llevan la afirmación
de cada tuit) y una corrida cortada retoma sin volver a pagar. El resultado va a
`resultados/sistema_<conjunto>_<version_pesos>.json`; si ya existe, el *script* se niega a
repetirlo.

`--conjunto chequeado-validacion` corre el sistema sobre las afirmaciones de validación de
Chequeado, que no intervienen en la prueba: ahí se elige el umbral del nivel desfavorable
con `--barrer`, que recalcula el veredicto binario desde la caché sin volver a llamar al LLM.

Si el corpus trae las columnas de la cuenta (`handle`, `verificada`, `creada`, `seguidores`,
`seguidos`, `respuestas`, `retuits`, `me_gusta`, `vistas`), el pedido las lleva y el Módulo 2
interviene como en la extensión; una celda vacía deja el dato ausente.
"""

import argparse
import hashlib
import json
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score

import pandas as pd

from datos import cargar_chequeado
from evaluar_argentino import CORPUS

CACHE = Path("cache_sistema")
METRICAS = ["respuestas", "retuits", "me_gusta", "vistas"]
CLASE = {
    "contradicho_por_fuentes_oficiales": "falso",
    "informacion_sospechosa": "falso",
    "parece_verificado": "verdadero",
}
ORDEN = ["verdadero", "falso", "sin_veredicto"]
MODULO_EXTRACCION = "la extracción de la afirmación verificable"  # `servicio/app/pipeline.py`


def corpus(conjunto: str) -> pd.DataFrame:
    if conjunto == "chequeado-validacion":
        filas = cargar_chequeado()
        return filas[filas["particion"] == "validacion"].reset_index(drop=True)
    filas = pd.read_csv(CORPUS, dtype=str, keep_default_na=False)
    assert filas["etiqueta_confirmada"].isin(["verdadero", "falso", "descartar"]).all(), "hay filas sin confirmar"
    filas = filas[filas["etiqueta_confirmada"] != "descartar"]
    return filas.rename(columns={"etiqueta_confirmada": "etiqueta"}).reset_index(drop=True)


def pedido(clave: str, fila: pd.Series) -> dict:
    """El cuerpo de `POST /analizar`, con la cuenta y las métricas cuando el corpus las trae."""
    dato = lambda c: fila.get(c) or None  # noqa: E731 — celda vacía o columna ausente → sin dato
    cuerpo = {"tweet_id": clave, "texto": fila["texto"], "handle": dato("handle") or "@evaluacion",
              "verificada": dato("verificada") == "si",
              "metricas": {m: int(dato(m)) if dato(m) else None for m in METRICAS}}
    if dato("creada") and dato("seguidores") and dato("seguidos"):
        cuerpo["cuenta"] = {"creada": dato("creada"), "seguidores": int(dato("seguidores")), "seguidos": int(dato("seguidos"))}
    return cuerpo


def analizar(url: str, fila: pd.Series, cache: Path) -> dict:
    clave = hashlib.sha256(fila["texto"].encode()).hexdigest()[:16]
    archivo = cache / f"{clave}.json"
    if archivo.exists():
        return json.loads(archivo.read_text(encoding="utf-8"))
    pedido_ = json.dumps(pedido(clave, fila)).encode()
    with urllib.request.urlopen(urllib.request.Request(f"{url}/analizar", pedido_, {"Content-Type": "application/json"}), timeout=180) as r:
        respuesta = json.loads(r.read())
    if MODULO_EXTRACCION in respuesta["analisis_parcial"]["modulos_ausentes"]:
        # Falla de infraestructura (credencial, red), no un resultado: no se guarda y se corta.
        raise SystemExit(f"falló la extracción: revisar OPENAI_API_KEY y el servicio ({respuesta['analisis_parcial']})")
    cache.mkdir(parents=True, exist_ok=True)
    archivo.write_text(json.dumps(respuesta, ensure_ascii=False, indent=1), encoding="utf-8")
    return respuesta


def prediccion(respuesta: dict, umbral: float | None = None) -> str:
    """Clase binaria del veredicto; con `umbral`, la recalcula desde el puntaje final.

    Los dos niveles desfavorables cuentan como falso, así que el corte severo y su rebaja
    (`_veredicto_admisible`) no cambian la clase: solo importa el umbral del nivel
    intermedio. *Sin contraste externo* no depende del puntaje y queda sin veredicto.
    """
    if not respuesta["afirmacion"]:
        return "sin_veredicto"
    clase = CLASE.get(respuesta["veredicto"], "sin_veredicto")
    if umbral is None or clase == "sin_veredicto":
        return clase
    return "falso" if respuesta["puntaje_final"] >= umbral else "verdadero"


def barrer(etiquetas: list[str], respuestas: list[dict]) -> list[dict]:
    filas = []
    for umbral in np.round(np.arange(0.30, 0.71, 0.02), 2):
        predichas = [prediccion(r, umbral) for r in respuestas]
        filas.append({
            "umbral": float(umbral),
            "f1_macro": float(f1_score(etiquetas, predichas, labels=["verdadero", "falso"], average="macro")),
        "precision_falso": float(precision_score(etiquetas, predichas, labels=["falso"], average="macro", zero_division=0)),
            "precision_falso": float(precision_score(etiquetas, predichas, labels=["falso"], average="macro", zero_division=0)),
            "recall_falso": float(recall_score(etiquetas, predichas, labels=["falso"], average="macro", zero_division=0)),
        })
    return filas


def evaluar(etiquetas: list[str], respuestas: list[dict], umbral: float | None = None) -> dict:
    predichas = [prediccion(r, umbral) for r in respuestas]
    respondidas = [i for i, p in enumerate(predichas) if p != "sin_veredicto"]
    y = [e == "falso" for e in etiquetas]
    return {
        "n": len(etiquetas),
        # Etiquetas [verdadero, falso]: una abstención nunca cuenta como acierto.
        "f1_macro": float(f1_score(etiquetas, predichas, labels=["verdadero", "falso"], average="macro")),
        "precision_falso": float(precision_score(etiquetas, predichas, labels=["falso"], average="macro", zero_division=0)),
        "cobertura": len(respondidas) / len(etiquetas),
        "f1_macro_respondidas": float(f1_score([etiquetas[i] for i in respondidas], [predichas[i] for i in respondidas], labels=["verdadero", "falso"], average="macro")) if respondidas else None,
        "auc_roc_puntaje_final": float(roc_auc_score(y, [r["puntaje_final"] for r in respuestas])),
        # Filas: real (verdadero, falso); columnas: verdadero, falso, sin veredicto.
        "matriz_confusion": confusion_matrix(etiquetas, predichas, labels=ORDEN)[:2].tolist(),
        "veredictos": dict(Counter(r["veredicto"] for r in respuestas)),
        "analisis_parciales": sum(r["analisis_parcial"]["es_parcial"] for r in respuestas),
        # El verificador del corpus de prueba también es una fuente del sistema: cuántas veces aparece.
        "con_chequeado_entre_las_fuentes": sum(any("chequeado.com" in f["url"] for f in r["fuentes"]) for r in respuestas),
    }


def intervalo(etiquetas: list[str], respuestas: list[dict], umbral: float | None = None, replicas: int = 5000) -> list[float]:
    predichas = np.array([prediccion(r, umbral) for r in respuestas])
    etiquetas = np.array(etiquetas)
    indices = np.random.default_rng(42).integers(0, len(etiquetas), (replicas, len(etiquetas)))
    f1 = [f1_score(etiquetas[i], predichas[i], labels=["verdadero", "falso"], average="macro") for i in indices]
    return np.percentile(f1, [2.5, 97.5]).round(4).tolist()


if __name__ == "__main__":
    opciones = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    opciones.add_argument("--url", default="http://localhost:8000")
    opciones.add_argument("--conjunto", choices=["argentino", "chequeado-validacion"], default="argentino")
    opciones.add_argument("--barrer", action="store_true", help="solo imprime el barrido de umbrales desde la caché")
    opciones.add_argument("--comparar-umbral", type=float, help="reporta también este umbral, recalculado desde la misma caché")
    args = opciones.parse_args()
    datos = corpus(args.conjunto)
    cache = CACHE / args.conjunto
    respuestas = []
    for i, (_, fila) in enumerate(datos.iterrows(), 1):
        respuestas.append(analizar(args.url, fila, cache))
        print(f"{i}/{len(datos)}", respuestas[-1]["veredicto"], flush=True)
    versiones = {(r["version_modelo"], r["version_configuracion_pesos"]) for r in respuestas}
    assert len(versiones) == 1, f"las respuestas mezclan versiones: {versiones}"
    version_modelo, version_pesos = versiones.pop()
    etiquetas = datos["etiqueta"].tolist()
    if args.barrer:
        print(json.dumps(barrer(etiquetas, respuestas), indent=1))
        raise SystemExit
    ruta = Path("resultados") / f"sistema_{args.conjunto}_{version_pesos.split('+')[0]}.json"
    assert not ruta.exists(), f"{ruta}: esta configuración ya se evaluó sobre ese conjunto"
    evaluacion = evaluar(etiquetas, respuestas)
    evaluacion["f1_macro_ic95"] = intervalo(etiquetas, respuestas)
    evaluaciones = {f"{args.conjunto}/prueba": evaluacion}
    if args.comparar_umbral is not None:
        comparacion = evaluar(etiquetas, respuestas, args.comparar_umbral)
        comparacion["f1_macro_ic95"] = intervalo(etiquetas, respuestas, args.comparar_umbral)
        evaluaciones[f"{args.conjunto}/umbral_{args.comparar_umbral}"] = comparacion
    resultado = {
        "id_corrida": f"sistema_{version_modelo}",
        "modelo": "sistema",
        "fecha": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "version_modelo": version_modelo,
        "version_configuracion_pesos": version_pesos,
        "correspondencia": {**CLASE, "sin_contraste_externo": "sin_veredicto"},
        "evaluaciones": evaluaciones,
    }
    ruta.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(evaluaciones, ensure_ascii=False, indent=1))
