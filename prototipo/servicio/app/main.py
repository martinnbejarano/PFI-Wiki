"""Servicio HTTP del prototipo.

Expone un único punto de entrada de análisis, `POST /analizar`, cuyo contrato
está definido en `contrato.py`. En esta instancia la respuesta tiene valores
fijos; los tickets siguientes sustituyen el cuerpo del manejador sin tocar la
forma de la respuesta.

Arranque:

    uvicorn app.main:aplicacion --reload --port 8000

La documentación interactiva que FastAPI deriva del tipado queda en
`http://localhost:8000/docs`.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .analisis_fijo import construir_analisis
from .contrato import PedidoAnalisis, RespuestaAnalisis

aplicacion = FastAPI(
    title="Servicio de detección de desinformación — prototipo",
    description=(
        "Prototipo de la rebanada vertical para la demostración del 50 %. "
        "Un único punto de entrada de análisis con el contrato completo de la "
        "respuesta y valores fijos."
    ),
    version="0.1.0",
)

# La petición la emite el *service worker* de la extensión, cuyo origen es
# `chrome-extension://<identificador>`. El identificador cambia con cada carga
# sin empaquetar, así que se admite el esquema entero en lugar de un origen
# concreto. `localhost` queda admitido para poder probar con `curl` y desde el
# navegador durante el desarrollo.
aplicacion.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^(chrome-extension://.*|http://localhost(:\d+)?)$",
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


@aplicacion.get("/salud")
def salud() -> dict[str, str]:
    """Comprobación de vida, útil para verificar el arranque sin la extensión."""
    return {"estado": "vivo"}


@aplicacion.post("/analizar", response_model=RespuestaAnalisis)
def analizar(pedido: PedidoAnalisis) -> RespuestaAnalisis:
    """Analiza un tuit y devuelve el veredicto con su evidencia.

    En esta instancia los valores son fijos y no dependen del contenido del
    tuit, salvo el identificador nativo, que se devuelve para que quien llama
    pueda correlacionar la respuesta con el indicador que la pidió.
    """
    return construir_analisis(pedido)
