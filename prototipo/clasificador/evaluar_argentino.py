"""Evaluación final sobre el corpus argentino de prueba (ticket #36).

El corpus es reserva estricta (cap. 4): se evalúa una sola vez, con los modelos ya
elegidos y el umbral de su JSON. El resultado se agrega como `argentino/prueba` al
JSON de cada modelo en `resultados/`; si ya está, el script se niega a repetirlo.

    .venv/bin/python evaluar_argentino.py --beto ~/Downloads/beto_fakedes_s42

El LLM *zero-shot* se evalúa con `llm_zero_shot.py --argentino …`.
"""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import joblib
import pandas as pd

from datos import preprocesar
from resultados import metricas

CORPUS = "datos/corpus_argentino/candidatos.csv"


def corpus() -> pd.DataFrame:
    filas = pd.read_csv(CORPUS)
    assert filas["etiqueta_confirmada"].isin(["verdadero", "falso", "descartar"]).all(), "hay filas sin confirmar"
    filas = filas[filas["etiqueta_confirmada"] != "descartar"]
    return filas.rename(columns={"etiqueta_confirmada": "etiqueta"})[["texto", "etiqueta"]]


def puntajes_beto(carpeta: str, textos: list[str]) -> list[float]:
    import torch
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    tokenizador = AutoTokenizer.from_pretrained(carpeta)
    modelo = AutoModelForSequenceClassification.from_pretrained(carpeta).eval()
    # Igual que en el entrenamiento: `datos.preprocesar`, 512 fichas, truncado por la derecha.
    with torch.no_grad():
        entrada = tokenizador([preprocesar(t) for t in textos], truncation=True, max_length=512, padding=True, return_tensors="pt")
        return torch.softmax(modelo(**entrada).logits, dim=-1)[:, 1].tolist()


def agregar(id_corrida: str, datos: pd.DataFrame, puntajes: list[float]) -> dict:
    ruta = Path("resultados") / f"{id_corrida}.json"
    resultado = json.loads(ruta.read_text(encoding="utf-8"))
    assert "argentino/prueba" not in resultado["evaluaciones"], f"{id_corrida}: el corpus argentino ya se evaluó"
    umbral = resultado["evaluaciones"]["fakedes/prueba"]["umbral"]
    evaluacion = metricas(datos["etiqueta"].tolist(), puntajes, umbral)
    evaluacion["fecha"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    resultado["evaluaciones"]["argentino/prueba"] = evaluacion
    ruta.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return evaluacion


if __name__ == "__main__":
    opciones = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    opciones.add_argument("--beto", required=True, help="carpeta con los pesos de beto_fakedes_s42")
    carpeta = opciones.parse_args().beto
    datos = corpus()
    print(f"{len(datos)} tuits:", datos["etiqueta"].value_counts().to_dict())
    linea_base = joblib.load("modelos/tfidf-lr_fakedes_s42.joblib")
    for id_corrida, puntajes in (
        ("tfidf-lr_fakedes_s42", linea_base.predict_proba(datos["texto"])[:, 1].tolist()),
        ("beto_fakedes_s42", puntajes_beto(carpeta, datos["texto"].tolist())),
    ):
        m = agregar(id_corrida, datos, puntajes)
        print(id_corrida, {k: round(m[k], 4) for k in ("f1_macro", "auc_roc")}, "falso:", {k: round(v, 3) for k, v in m["por_clase"]["falso"].items()}, m["matriz_confusion"])
