"""Servicio HTTP del prototipo.

Expone el punto de entrada de análisis, `POST /analizar`, cuyo contrato está
definido en `contrato.py`, el informe de un veredicto incorrecto,
`POST /reportes` (CU-04), y el panel web mínimo con el histórico personal,
`GET /panel` (CU-05). Este módulo es el borde de red y nada más: no
sabe cuántos pasos tiene el análisis ni qué proveedor está detrás. Encadenar los
pasos es tarea de `pipeline.py`; hablar con el proveedor, del adaptador que
`dependencias.obtener_proveedor` construye.

Arranque:

    uvicorn app.main:aplicacion --reload --port 8000

El servicio arranca sin la credencial del proveedor. Sin ella responde
`GET /salud` con normalidad y `POST /analizar` devuelve **200 con un análisis
parcial** que lista los módulos que no pudieron ejecutarse, que es lo que exige
RNF-11. Es también la forma más simple de provocar el estado parcial a mano para
una captura: levantar el servicio sin `OPENAI_API_KEY`.

La documentación interactiva que FastAPI deriva del tipado queda en
`http://localhost:8000/docs`.
"""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from .cache import CacheDeAnalisis, obtener_cache
from .configuracion import Configuracion, obtener_configuracion
from . import panel
from .contrato import PedidoAnalisis, PedidoReporte, ReporteRegistrado, RespuestaAnalisis
from .dependencias import obtener_proveedor
from .historial import Historial, obtener_historial
from .pipeline import analizar_tuit
from .proveedor.puerto import ProveedorDeAnalisis

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


# Acá vivía un manejador que traducía `ErrorDelProveedor` en un 503. Se lo quitó
# a propósito y no por descuido: RNF-11 pide que una falla del proveedor produzca
# un análisis parcial identificado como tal, y un 503 —por más claro que sea su
# mensaje— es un error, no un análisis. La degradación ocurre ahora en
# `pipeline.py`, envolviendo cada llamada al proveedor por separado, que es el
# único lugar donde se sabe **cuál** de los módulos quedó ausente. Ninguna falla
# del proveedor llega hasta acá.


@aplicacion.get("/salud")
def salud() -> dict[str, str]:
    """Comprobación de vida, útil para verificar el arranque sin la extensión."""
    return {"estado": "vivo"}


@aplicacion.post("/analizar", response_model=RespuestaAnalisis)
def analizar(
    pedido: PedidoAnalisis,
    proveedor: Annotated[ProveedorDeAnalisis, Depends(obtener_proveedor)],
    configuracion: Annotated[Configuracion, Depends(obtener_configuracion)],
    cache: Annotated[CacheDeAnalisis, Depends(obtener_cache)],
    historial: Annotated[Historial, Depends(obtener_historial)],
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

    **Este punto de entrada no tiene camino de error para las fallas del
    proveedor.** Si un paso del análisis no se pudo ejecutar, lo que sale sigue
    siendo un 200 con la respuesta del contrato, marcada como análisis parcial y
    con la lista de los módulos ausentes (RNF-11). Un tuit ya analizado con el
    mismo modelo y la misma configuración de pesos se resuelve desde la caché en
    memoria, sin tocar el proveedor (RF-07).
    """
    analisis = analizar_tuit(pedido, proveedor, configuracion, cache)
    # Con el identificador de la instalación, el análisis entra en su
    # histórico (RF-10), también cuando sale de la caché: el usuario lo pidió.
    if pedido.id_instalacion is not None:
        historial.registrar_analisis(str(pedido.id_instalacion), analisis)
    return analisis


@aplicacion.post("/reportes", response_model=ReporteRegistrado, status_code=201)
def reportar(
    pedido: PedidoReporte,
    historial: Annotated[Historial, Depends(obtener_historial)],
) -> ReporteRegistrado:
    """Registra el informe de un veredicto incorrecto (RF-11, CU-04).

    El informe queda asociado al último análisis de ese tuit pedido desde esa
    instalación, al identificador anónimo y a la versión de modelo que produjo
    el veredicto. Reenviarlo no lo duplica: devuelve el ya registrado.
    """
    reporte = historial.registrar_reporte(
        str(pedido.id_instalacion), pedido.tweet_id, pedido.tipo.value, pedido.motivo
    )
    if reporte is None:
        raise HTTPException(404, "Esta instalación no pidió el análisis de ese tuit")
    return ReporteRegistrado(id_instalacion=reporte["uuid"], **reporte)


@aplicacion.get("/panel", response_class=HTMLResponse)
def ver_panel(
    historial: Annotated[Historial, Depends(obtener_historial)],
    instalacion: UUID | None = None,
    tuit: str | None = None,
) -> str:
    """Panel web mínimo: histórico de la instalación y detalle de cada análisis
    (RF-10, CU-05), con la finalidad y la vía de supresión (RF-12)."""
    if instalacion is None:
        return panel.renderizar_institucional()
    entradas = historial.listar(str(instalacion))
    if tuit is not None:
        entrada = next((e for e in entradas if e["tweet_id"] == tuit), None)
        if entrada is None:
            raise HTTPException(404, "Ese análisis no está en el histórico")
        return panel.renderizar_detalle(str(instalacion), entrada)
    return panel.renderizar_lista(str(instalacion), entradas)
