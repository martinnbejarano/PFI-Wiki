"""Servicio HTTP del prototipo.

Expone un único punto de entrada de análisis, `POST /analizar`, cuyo contrato
está definido en `contrato.py`. Este módulo es el borde de red y nada más: no
sabe cuántos pasos tiene el análisis ni qué proveedor está detrás. Encadenar los
pasos es tarea de `pipeline.py`; hablar con el proveedor, del adaptador que
`dependencias.obtener_proveedor` construye.

Arranque:

    uvicorn app.main:aplicacion --reload --port 8000

El servicio arranca sin la credencial del proveedor. Sin ella responde
`GET /salud` con normalidad y `POST /analizar` devuelve 503 con un mensaje que
dice qué falta.

La documentación interactiva que FastAPI deriva del tipado queda en
`http://localhost:8000/docs`.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .configuracion import Configuracion, obtener_configuracion
from .contrato import PedidoAnalisis, RespuestaAnalisis
from .dependencias import obtener_proveedor
from .pipeline import analizar_tuit
from .proveedor.puerto import ErrorDelProveedor, ProveedorDeAnalisis

aplicacion = FastAPI(
    title="Servicio de detección de desinformación — prototipo",
    description=(
        "Prototipo de la rebanada vertical para la demostración del 50 %. "
        "Un único punto de entrada de análisis, con el veredicto y la "
        "justificación emitidos por el proveedor de modelo de lenguaje grande."
    ),
    version="0.2.0",
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


@aplicacion.exception_handler(ErrorDelProveedor)
def manejar_error_del_proveedor(
    peticion: Request, error: ErrorDelProveedor
) -> JSONResponse:
    """Traduce una falla del proveedor en un mensaje claro y no en un 500 opaco.

    Cubre la credencial ausente, el corte por tiempo límite y los errores de la
    API. El ticket #25 reemplaza esta traducción por la degradación a análisis
    parcial que exige RNF-11.
    """
    return JSONResponse(status_code=503, content={"detalle": str(error)})


@aplicacion.get("/salud")
def salud() -> dict[str, str]:
    """Comprobación de vida, útil para verificar el arranque sin la extensión."""
    return {"estado": "vivo"}


@aplicacion.post("/analizar", response_model=RespuestaAnalisis)
def analizar(
    pedido: PedidoAnalisis,
    proveedor: Annotated[ProveedorDeAnalisis, Depends(obtener_proveedor)],
    configuracion: Annotated[Configuracion, Depends(obtener_configuracion)],
) -> RespuestaAnalisis:
    """Analiza un tuit y devuelve el veredicto con su evidencia.

    La afirmación verificable, su tipo, las fuentes, el veredicto y la
    justificación provienen de llamadas reales al proveedor. Las fuentes quedan
    restringidas a la jerarquía de evidencia de `jerarquia.py`; cuando ninguna
    resulta admisible, `fuentes` viene vacía y el veredicto se emite en el
    estado *sin contraste externo*, que es lo que RF-06 y RNF-06 exigen en ese
    caso.

    Cuando la publicación no contiene ninguna afirmación verificable, la
    respuesta llega con `afirmacion` vacía y sin veredicto de tres niveles: no
    es un error, es el resultado correcto.
    """
    return analizar_tuit(pedido, proveedor, configuracion)
