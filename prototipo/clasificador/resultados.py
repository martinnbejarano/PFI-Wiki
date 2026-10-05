"""Formato del JSON de resultados de una corrida (ticket #29; lo reutilizan #33, #34 y #36).

Una corrida es un modelo entrenado; puede evaluarse sobre varias particiones.
El formato está documentado en `README.md`. El puntaje es siempre la
probabilidad de la clase «falso».
"""

from __future__ import annotations

import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import pandas
import sklearn
from sklearn.metrics import confusion_matrix, f1_score, precision_recall_fscore_support, roc_auc_score

CLASES = ["verdadero", "falso"]


def metricas(etiquetas: list[str], puntajes: list[float], umbral: float = 0.5) -> dict:
    """Métricas de una evaluación. `etiquetas` son "verdadero"/"falso"."""
    reales = [CLASES.index(e) for e in etiquetas]
    predichas = [int(p >= umbral) for p in puntajes]
    precision, exhaustividad, f1, soporte = precision_recall_fscore_support(reales, predichas, labels=[0, 1], zero_division=0)
    return {
        "n": len(reales),
        "umbral": umbral,
        "f1_macro": float(f1_score(reales, predichas, average="macro")),
        "auc_roc": float(roc_auc_score(reales, puntajes)),
        "por_clase": {
            clase: {
                "precision": float(precision[i]),
                "exhaustividad": float(exhaustividad[i]),
                "f1": float(f1[i]),
                "soporte": int(soporte[i]),
            }
            for i, clase in enumerate(CLASES)
        },
        # Filas: clase real; columnas: clase predicha; en el orden de `CLASES`.
        "matriz_confusion": confusion_matrix(reales, predichas, labels=[0, 1]).tolist(),
    }


def construir_resultado(
    *,
    id_corrida: str,
    modelo: str,
    entrenado_en: str,
    hiperparametros: dict,
    evaluaciones: dict[str, dict],
    semilla: int,
    hash_particiones: str,
    epocas: list[dict] | None = None,
    consumo: dict | None = None,
) -> dict:
    """`evaluaciones` va de "dataset/particion" a la salida de `metricas`.

    `consumo` es opcional (modelos pagos por llamada, como el LLM *zero-shot*):
    p. ej. `{"costo_usd": …, "latencia_media_s": …}`. Si falta, no se escribe.
    """
    return {
        "id_corrida": id_corrida,
        "modelo": modelo,
        "fecha": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "entrenado_en": entrenado_en,
        "semilla": semilla,
        "hash_particiones": hash_particiones,
        "clases": CLASES,
        "hiperparametros": hiperparametros,
        "evaluaciones": evaluaciones,
        "epocas": epocas or [],
        **({"consumo": consumo} if consumo else {}),
        # Un `joblib` solo se garantiza con la misma versión de scikit-learn.
        "entorno": {"python": platform.python_version(), "scikit_learn": sklearn.__version__, "pandas": pandas.__version__},
    }


def guardar(resultado: dict, carpeta: str | Path) -> Path:
    ruta = Path(carpeta) / f"{resultado['id_corrida']}.json"
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return ruta
