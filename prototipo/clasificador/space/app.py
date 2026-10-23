"""Servicio de inferencia del Módulo 1 (Hugging Face Space, ticket #32).

`POST /clasificar` con `{"texto": "..."}` devuelve
`{"puntaje", "clase", "version_modelo"}`. El puntaje es la probabilidad de la
clase «falso»; la clase sale del mismo umbral que los JSON de `resultados/`.

`POST /embeber` con el mismo cuerpo devuelve `{"vector"}`, el *embedding* que la
memoria de evidencia del servicio compara (ticket #101).

El modelo es el `.joblib` de `modelos/` o, si `MODELO` es una carpeta, los pesos de un
Transformer. El `.joblib` es un `Pipeline` de scikit-learn que
recibe texto crudo y referencia `datos.preprocesar`, así que `datos.py` tiene
que estar al lado. Ver «Publicar el Space» en el README del clasificador.
"""

import os
from functools import cache

import joblib
from fastapi import FastAPI
from pydantic import BaseModel

MODELO = os.environ.get("MODELO", "tfidf-lr_fakedes_s42")
UMBRAL = 0.5

if not os.path.isdir(MODELO) and not os.path.exists(f"{MODELO}.joblib") and "/" in MODELO:
    # `<usuario>/<repo>` del Hub (privado): se baja al arrancar con el secreto HF_TOKEN.
    from huggingface_hub import snapshot_download

    MODELO = snapshot_download(MODELO, token=os.environ.get("HF_TOKEN"))

if os.path.isdir(MODELO):
    # Pesos de un Transformer (`fine_tuning.ipynb`), con el mismo preprocesamiento y truncado
    # que `evaluar_argentino.puntajes_beto`.
    # ponytail: sin lotes ni GPU; alcanza para un tuit por pedido.
    import torch
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    from datos import preprocesar

    _tokenizador = AutoTokenizer.from_pretrained(MODELO)
    _red = AutoModelForSequenceClassification.from_pretrained(MODELO).eval()

    def puntaje_falso(texto: str) -> float:
        with torch.no_grad():
            entrada = _tokenizador(preprocesar(texto), truncation=True, max_length=512, return_tensors="pt")
            return float(torch.softmax(_red(**entrada).logits, dim=-1)[0, 1])

    # La versión es el `id_corrida` del JSON de resultados que `fine_tuning.ipynb` guarda junto a los pesos.
    import json
    from pathlib import Path

    MODELO = next(
        (d["id_corrida"] for f in Path(MODELO).glob("*.json") if "id_corrida" in (d := json.loads(f.read_text()))),
        Path(MODELO).name,
    )
else:
    _modelo = joblib.load(f"{MODELO}.joblib")

    def puntaje_falso(texto: str) -> float:
        # La columna 1 es la clase positiva del entrenamiento: `etiqueta == "falso"`.
        return float(_modelo.predict_proba([texto])[0, 1])


app = FastAPI()


class Pedido(BaseModel):
    texto: str


@app.post("/clasificar")
def clasificar(pedido: Pedido) -> dict:
    puntaje = puntaje_falso(pedido.texto)
    return {
        "puntaje": puntaje,
        "clase": "falso" if puntaje >= UMBRAL else "verdadero",
        "version_modelo": MODELO,
    }


# -- Embeddings de la memoria de evidencia del servicio (ticket #101) ----------
#
# Viven acá para no sumar al despliegue otro servicio ni una dependencia de un
# proveedor externo: el contenedor ya trae torch y transformers.

MODELO_EMBEDDINGS = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


@cache
def _embebedor():
    # Perezoso: el clasificador arranca igual de rápido y el modelo (≈ 470 MB)
    # se baja recién con el primer pedido.
    from transformers import AutoModel, AutoTokenizer

    return AutoTokenizer.from_pretrained(MODELO_EMBEDDINGS), AutoModel.from_pretrained(MODELO_EMBEDDINGS).eval()


@app.post("/embeber")
def embeber(pedido: Pedido) -> dict:
    """Vector de 384 dimensiones, normalizado: el coseno es el producto escalar.
    El promedio sobre las fichas, pesado por la máscara, es el *pooling* con que
    se entrenó el modelo."""
    import torch

    tokenizador, red = _embebedor()
    with torch.no_grad():
        entrada = tokenizador(pedido.texto, truncation=True, max_length=128, return_tensors="pt")
        fichas = red(**entrada).last_hidden_state
        mascara = entrada["attention_mask"].unsqueeze(-1).float()
        vector = (fichas * mascara).sum(1) / mascara.sum(1)
    return {"vector": torch.nn.functional.normalize(vector, dim=-1)[0].tolist()}
