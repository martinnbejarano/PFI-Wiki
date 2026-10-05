"""Servicio HTTP del prototipo.

Expone el punto de entrada de análisis, `POST /analizar`, cuyo contrato está
definido en `contrato.py`, el informe de un veredicto incorrecto,
`POST /reportes` (CU-04), y el panel web mínimo con el histórico personal,
`GET /panel` (CU-05), y la interfaz para organizaciones cliente (CU-06): la
administración de organizaciones y claves y `POST /api/v1/clasificar`, y el
panel de tendencias de esas organizaciones, `GET /panel/tendencias` (CU-07). Este módulo es el borde de red y nada más: no
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

import asyncio
import csv
import hashlib
import hmac
import io
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager, suppress
from datetime import date, datetime, timedelta, timezone
from typing import Annotated, Any
from urllib.parse import parse_qs
from uuid import UUID

from fastapi import Cookie, Depends, FastAPI, Header, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse

from .cache import CacheDeAnalisis, obtener_cache
from .configuracion import Configuracion, obtener_configuracion
from . import panel
from .contrato import (
    PedidoAnalisis,
    PedidoClasificacion,
    PedidoOrganizacion,
    PedidoReporte,
    ReporteRegistrado,
    RespuestaAnalisis,
)
from .dependencias import cliente_clasificador, obtener_proveedor
from .historial import Historial, obtener_historial
from .pipeline import analizar_tuit
from .proveedor.clasificador import mantener_despierto
from .proveedor.puerto import ProveedorDeAnalisis


@asynccontextmanager
async def ciclo_de_vida(_: FastAPI) -> AsyncIterator[None]:
    """Con el adaptador compuesto, mantiene despierto el Space mientras el
    servicio vive. Se desactiva con `INTERVALO_DESPERTAR_CLASIFICADOR_S=0`."""
    configuracion = obtener_configuracion()
    tarea = None
    if (
        configuracion.adaptador == "compuesto"
        and configuracion.url_clasificador
        and configuracion.intervalo_despertar_clasificador_s > 0
    ):
        tarea = asyncio.create_task(
            mantener_despierto(
                cliente_clasificador(configuracion),
                configuracion.intervalo_despertar_clasificador_s,
            )
        )
    yield
    if tarea is not None:
        tarea.cancel()
        with suppress(asyncio.CancelledError):
            await tarea


aplicacion = FastAPI(
    lifespan=ciclo_de_vida,
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
        historial.registrar_analisis(str(pedido.id_instalacion), analisis, pedido.handle)
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


# --- Organizaciones cliente (RF-13, CU-06) ----------------------------------


def exigir_administrador(
    configuracion: Annotated[Configuracion, Depends(obtener_configuracion)],
    x_secreto_administrador: Annotated[str, Header()] = "",
) -> None:
    """Protege la administración con el secreto de la configuración. Sin
    secreto configurado nadie administra, ni siquiera con la cabecera vacía."""
    secreto = configuracion.secreto_administrador
    if not secreto or not hmac.compare_digest(
        x_secreto_administrador.encode(), secreto.encode()
    ):
        raise HTTPException(401, "Secreto administrativo ausente o incorrecto")


def clave_autenticada(
    historial: Annotated[Historial, Depends(obtener_historial)],
    authorization: Annotated[str, Header()] = "",
) -> dict[str, Any]:
    """La clave activa del sistema cliente y su organización, o 401.

    Una clave inválida y una revocada responden igual: distinguirlas le diría
    a quien prueba claves cuáles existieron."""
    esquema, _, clave = authorization.partition(" ")
    activa = historial.clave_activa(clave) if esquema.lower() == "bearer" and clave else None
    if activa is None:
        raise HTTPException(
            401, "Clave inválida o revocada", headers={"WWW-Authenticate": "Bearer"}
        )
    return activa


@aplicacion.post(
    "/organizaciones", status_code=201, dependencies=[Depends(exigir_administrador)]
)
def alta_organizacion(
    pedido: PedidoOrganizacion,
    historial: Annotated[Historial, Depends(obtener_historial)],
) -> dict[str, Any]:
    """Alta de una organización cliente con su cuota mensual."""
    return historial.alta_organizacion(pedido.nombre, pedido.cuota_mensual)


@aplicacion.post(
    "/organizaciones/{id_organizacion}/claves",
    status_code=201,
    dependencies=[Depends(exigir_administrador)],
)
def emitir_clave(
    id_organizacion: int,
    historial: Annotated[Historial, Depends(obtener_historial)],
) -> dict[str, str]:
    """Emite una clave. **Es la única vez que se la ve**: la base guarda su
    resumen y el prefijo, que sirve para identificarla y revocarla."""
    emitida = historial.emitir_clave(id_organizacion)
    if emitida is None:
        raise HTTPException(404, "La organización no existe")
    return emitida


@aplicacion.delete(
    "/organizaciones/{id_organizacion}/claves/{prefijo}",
    status_code=204,
    dependencies=[Depends(exigir_administrador)],
)
def revocar_clave(
    id_organizacion: int,
    prefijo: str,
    historial: Annotated[Historial, Depends(obtener_historial)],
) -> Response:
    if not historial.revocar_clave(id_organizacion, prefijo):
        raise HTTPException(404, "No hay una clave activa con ese prefijo")
    return Response(status_code=204)


@aplicacion.post("/api/v1/clasificar", response_model=RespuestaAnalisis)
def clasificar(
    pedido: PedidoClasificacion,
    clave: Annotated[dict[str, Any], Depends(clave_autenticada)],
    proveedor: Annotated[ProveedorDeAnalisis, Depends(obtener_proveedor)],
    configuracion: Annotated[Configuracion, Depends(obtener_configuracion)],
    cache: Annotated[CacheDeAnalisis, Depends(obtener_cache)],
    historial: Annotated[Historial, Depends(obtener_historial)],
) -> RespuestaAnalisis:
    """Interfaz de clasificación autenticada (CU-06): el análisis completo,
    contra la cuota mensual de la organización.

    La respuesta es la del contrato, que no lleva el *handle* ni el texto de la
    publicación: la cuenta autora nunca sale en claro (RF-15). Con la cuota
    agotada responde 429 con el límite y la fecha de renovación, y el rechazo
    no consume.
    """
    consumo = historial.consumo(clave["id_organizacion"], clave["cuota_mensual"])
    if consumo["consumo_del_mes"] >= consumo["cuota_mensual"]:
        raise HTTPException(429, {"mensaje": "Cuota mensual agotada", **consumo})
    # ponytail: la verificación y el registro no son atómicos; dos llamadas
    # simultáneas con la última unidad de cuota pasan las dos.
    # La caché se indexa por el texto y nunca por el `tweet_id` del cliente:
    # si no, un texto inventado con el identificador de un tuit real quedaría
    # como su veredicto para los ciudadanos.
    clave_cache = "texto-" + hashlib.sha256(pedido.texto.encode("utf-8")).hexdigest()
    analisis = analizar_tuit(
        PedidoAnalisis(tweet_id=clave_cache, texto=pedido.texto, handle=pedido.handle),
        proveedor, configuracion, cache,
    )
    historial.registrar_consumo(clave["id_organizacion"], clave["id_api_key"])
    if pedido.tweet_id:
        analisis = analisis.model_copy(update={"tweet_id": pedido.tweet_id})
    return analisis


@aplicacion.get("/api/v1/consumo")
def consultar_consumo(
    clave: Annotated[dict[str, Any], Depends(clave_autenticada)],
    historial: Annotated[Historial, Depends(obtener_historial)],
) -> dict[str, Any]:
    """Consumo del mes de la organización contra su cuota, con la renovación."""
    return {
        "organizacion": clave["nombre"],
        **historial.consumo(clave["id_organizacion"], clave["cuota_mensual"]),
    }


# --- Panel de tendencias (RF-14, CU-07) -------------------------------------


def _periodo(desde: date | None, hasta: date | None) -> tuple[str, str]:
    """Por defecto, los últimos treinta días hasta hoy (UTC), inclusive."""
    hasta = hasta or datetime.now(timezone.utc).date()
    desde = desde or hasta - timedelta(days=29)
    if desde > hasta:
        raise HTTPException(422, "El período empieza después de terminar")
    return desde.isoformat(), hasta.isoformat()


COOKIE_DEL_PANEL = "clave_organizacion"


def organizacion_del_panel(
    historial: Annotated[Historial, Depends(obtener_historial)],
    authorization: Annotated[str, Header()] = "",
    clave_organizacion: Annotated[str, Cookie()] = "",
) -> dict[str, Any] | None:
    """La clave del analista: por cabecera, como la API, o por la cookie que
    deja el formulario de acceso para usar el panel desde el navegador."""
    esquema, _, clave = authorization.partition(" ")
    if esquema.lower() != "bearer" or not clave:
        clave = clave_organizacion
    return historial.clave_activa(clave) if clave else None


@aplicacion.post("/panel/tendencias", response_class=HTMLResponse)
async def acceder_a_tendencias(
    request: Request,
    historial: Annotated[Historial, Depends(obtener_historial)],
) -> Response:
    """El formulario de acceso: valida la clave y la deja en una cookie que el
    código de la página no puede leer ni otro sitio hacer viajar."""
    # Sin `python-multipart`: el formulario tiene un único campo.
    clave = parse_qs((await request.body()).decode()).get("clave", [""])[0].strip()
    if not clave or historial.clave_activa(clave) is None:
        return HTMLResponse(panel.renderizar_acceso(invalida=True), 401)
    respuesta = RedirectResponse("tendencias", 303)
    respuesta.set_cookie(
        COOKIE_DEL_PANEL, clave, path="/panel", httponly=True, samesite="strict",
        # ponytail: `Secure` salvo en localhost; detrás de un proxy TLS que
        # llame por otro nombre, decidirlo por configuración.
        secure=request.url.hostname not in ("localhost", "127.0.0.1"),
    )
    return respuesta


@aplicacion.get("/panel/tendencias", response_class=HTMLResponse)
def ver_tendencias(
    clave: Annotated[dict[str, Any] | None, Depends(organizacion_del_panel)],
    historial: Annotated[Historial, Depends(obtener_historial)],
    desde: date | None = None,
    hasta: date | None = None,
) -> Response:
    """Vista de tendencias para el analista de una organización cliente: temas
    de mayor circulación, evolución diaria y cuentas de mayor volumen bajo
    seudónimo (RF-14). Se entra con la clave de la organización (RF-13), en
    lugar del proveedor de identidad; sin ella, 401 con el formulario de
    acceso. No consume cuota."""
    if clave is None:
        return HTMLResponse(panel.renderizar_acceso(), 401)
    inicio, fin = _periodo(desde, hasta)
    return HTMLResponse(
        panel.renderizar_tendencias(clave["nombre"], inicio, fin, historial.tendencias(inicio, fin))
    )


@aplicacion.get("/panel/tendencias.csv", response_class=PlainTextResponse)
def exportar_tendencias(
    clave: Annotated[dict[str, Any] | None, Depends(organizacion_del_panel)],
    historial: Annotated[Historial, Depends(obtener_historial)],
    desde: date | None = None,
    hasta: date | None = None,
) -> Response:
    """El recorte del período, agregado: una fila por tema, por día y por
    cuenta seudonimizada, nunca por publicación ni con el *handle* (RF-15)."""
    if clave is None:
        raise HTTPException(401, "Clave inválida o revocada", headers={"WWW-Authenticate": "Bearer"})
    inicio, fin = _periodo(desde, hasta)
    salida = io.StringIO()
    escritor = csv.writer(salida)
    escritor.writerow(["seccion", "clave", "publicaciones", "marcadas"])
    for seccion, filas in historial.tendencias(inicio, fin).items():
        for clave_fila, publicaciones, marcadas in filas:
            # El tema sale del texto de un tuit: sin fórmulas en la planilla.
            if clave_fila[:1] in ("=", "+", "-", "@"):
                clave_fila = "'" + clave_fila
            escritor.writerow([seccion, clave_fila, publicaciones, marcadas])
    return Response(
        salida.getvalue(), media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="tendencias_{inicio}_{fin}.csv"'},
    )
