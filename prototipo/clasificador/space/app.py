"""Servicio de inferencia del Módulo 1 (Hugging Face Space, ticket #32).

Un único punto: `POST /clasificar` con `{"texto": "..."}` devuelve
`{"puntaje", "clase", "version_modelo"}`. El puntaje es la probabilidad de la
clase «falso»; la clase sale del mismo umbral que los JSON de `resultados/`.

El modelo es el `.joblib` de `modelos/`: un `Pipeline` de scikit-learn que
recibe texto crudo y referencia `datos.preprocesar`, así que `datos.py` tiene
que estar al lado. Ver «Publicar el Space» en el README del clasificador.
"""

import os

import joblib
from fastapi import FastAPI
from pydantic import BaseModel

MODELO = os.environ.get("MODELO", "tfidf-lr_fakedes_s42")
UMBRAL = 0.5

modelo = joblib.load(f"{MODELO}.joblib")
app = FastAPI()


class Pedido(BaseModel):
    texto: str


@app.post("/clasificar")
def clasificar(pedido: Pedido) -> dict:
    # La columna 1 es la clase positiva del entrenamiento: `etiqueta == "falso"`.
    puntaje = float(modelo.predict_proba([pedido.texto])[0, 1])
    return {
        "puntaje": puntaje,
        "clase": "falso" if puntaje >= UMBRAL else "verdadero",
        "version_modelo": MODELO,
    }
