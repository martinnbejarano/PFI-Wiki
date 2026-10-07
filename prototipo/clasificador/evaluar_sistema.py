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

Las respuestas quedan en `cache_sistema/` (fuera de git: llevan la afirmación de cada
tuit) y una corrida cortada retoma sin volver a pagar. El resultado va a
`resultados/sistema_<version_modelo>.json`; si ya existe, el *script* se niega a repetirlo.
"""

import argparse
import hashlib
import json
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from sklearn.metrics import confusion_matrix, f1_score, roc_auc_score

from evaluar_argentino import corpus

CACHE = Path("cache_sistema")
CLASE = {
    "contradicho_por_fuentes_oficiales": "falso",
    "informacion_sospechosa": "falso",
    "parece_verificado": "verdadero",
}
ORDEN = ["verdadero", "falso", "sin_veredicto"]
MODULO_EXTRACCION = "la extracción de la afirmación verificable"  # `servicio/app/pipeline.py`


def analizar(url: str, texto: str) -> dict:
    clave = hashlib.sha256(texto.encode()).hexdigest()[:16]
    archivo = CACHE / f"{clave}.json"
    if archivo.exists():
        return json.loads(archivo.read_text(encoding="utf-8"))
    pedido = json.dumps({"tweet_id": clave, "texto": texto, "handle": "@evaluacion"}).encode()
    with urllib.request.urlopen(urllib.request.Request(f"{url}/analizar", pedido, {"Content-Type": "application/json"}), timeout=180) as r:
        respuesta = json.loads(r.read())
    if MODULO_EXTRACCION in respuesta["analisis_parcial"]["modulos_ausentes"]:
        # Falla de infraestructura (credencial, red), no un resultado: no se guarda y se corta.
        raise SystemExit(f"falló la extracción: revisar OPENAI_API_KEY y el servicio ({respuesta['analisis_parcial']})")
    CACHE.mkdir(exist_ok=True)
    archivo.write_text(json.dumps(respuesta, ensure_ascii=False, indent=1), encoding="utf-8")
    return respuesta


def prediccion(respuesta: dict) -> str:
    if not respuesta["afirmacion"]:
        return "sin_veredicto"
    return CLASE.get(respuesta["veredicto"], "sin_veredicto")


def evaluar(etiquetas: list[str], respuestas: list[dict]) -> dict:
    predichas = [prediccion(r) for r in respuestas]
    respondidas = [i for i, p in enumerate(predichas) if p != "sin_veredicto"]
    y = [e == "falso" for e in etiquetas]
    return {
        "n": len(etiquetas),
        # Etiquetas [verdadero, falso]: una abstención nunca cuenta como acierto.
        "f1_macro": float(f1_score(etiquetas, predichas, labels=["verdadero", "falso"], average="macro")),
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


def intervalo(etiquetas: list[str], respuestas: list[dict], replicas: int = 5000) -> list[float]:
    predichas = np.array([prediccion(r) for r in respuestas])
    etiquetas = np.array(etiquetas)
    indices = np.random.default_rng(42).integers(0, len(etiquetas), (replicas, len(etiquetas)))
    f1 = [f1_score(etiquetas[i], predichas[i], labels=["verdadero", "falso"], average="macro") for i in indices]
    return np.percentile(f1, [2.5, 97.5]).round(4).tolist()


if __name__ == "__main__":
    opciones = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    opciones.add_argument("--url", default="http://localhost:8000")
    url = opciones.parse_args().url
    datos = corpus()
    respuestas = []
    for i, texto in enumerate(datos["texto"], 1):
        respuestas.append(analizar(url, texto))
        print(f"{i}/{len(datos)}", respuestas[-1]["veredicto"], flush=True)
    versiones = {(r["version_modelo"], r["version_configuracion_pesos"]) for r in respuestas}
    assert len(versiones) == 1, f"las respuestas mezclan versiones: {versiones}"
    version_modelo, version_pesos = versiones.pop()
    ruta = Path("resultados") / f"sistema_{version_modelo}.json"
    assert not ruta.exists(), f"{ruta}: el sistema ya se evaluó sobre el corpus argentino"
    evaluacion = evaluar(datos["etiqueta"].tolist(), respuestas)
    evaluacion["f1_macro_ic95"] = intervalo(datos["etiqueta"].tolist(), respuestas)
    resultado = {
        "id_corrida": f"sistema_{version_modelo}",
        "modelo": "sistema",
        "fecha": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "version_modelo": version_modelo,
        "version_configuracion_pesos": version_pesos,
        "correspondencia": {**CLASE, "sin_contraste_externo": "sin_veredicto"},
        "evaluaciones": {"argentino/prueba": evaluacion},
    }
    ruta.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(evaluacion, ensure_ascii=False, indent=1))
