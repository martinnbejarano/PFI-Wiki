"""El Módulo 1 con el clasificador propio (ticket #32), por `POST /analizar`.

El adaptador compuesto se arma con un doble del LLM (`ProveedorDoble`) y un
doble del cliente del servicio de inferencia, y se inyecta por el mismo punto
que el resto de la batería.
"""

from __future__ import annotations

import asyncio
import json
import threading
import time
from collections.abc import Iterator
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest
from fastapi.testclient import TestClient

from app.configuracion import obtener_configuracion
from app.dependencias import obtener_proveedor
from app.main import aplicacion
from app.proveedor.clasificador import (
    Clasificacion,
    ClienteClasificador,
    ProveedorCompuesto,
    mantener_despierto,
)
from app.proveedor.puerto import ErrorDelProveedor

from .conftest import PEDIDO_DE_EJEMPLO, ProveedorDoble, construir_cliente


class ClasificadorDoble:
    """Doble del cliente del servicio de inferencia. No hereda de nada."""

    def __init__(self, error: Exception | None = None) -> None:
        self.error = error
        self.textos_recibidos: list[str] = []

    def clasificar(self, texto: str) -> Clasificacion:
        self.textos_recibidos.append(texto)
        if self.error is not None:
            raise self.error
        return Clasificacion(puntaje=0.91, clase="falso", version_modelo="tfidf-lr_fakedes_s42")


def analizar(llm: ProveedorDoble, clasificador: ClasificadorDoble) -> dict:
    with construir_cliente(ProveedorCompuesto(llm, clasificador)) as cliente:
        respuesta = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO)
    assert respuesta.status_code == 200
    return respuesta.json()


def test_el_puntaje_y_la_clase_del_modulo_1_son_los_del_clasificador() -> None:
    llm = ProveedorDoble(puntaje_clasificador=0.10, clase_clasificador="verdadero")
    clasificador = ClasificadorDoble()

    cuerpo = analizar(llm, clasificador)

    assert cuerpo["puntajes"]["clasificador"] == {"valor": 0.91, "clase": "falso"}
    # La afirmación y el tipo siguen saliendo del LLM.
    assert cuerpo["afirmacion"].startswith("Afirmación extraída: ")
    assert cuerpo["tipo_afirmacion"] == "educacion"
    # El clasificador puntúa el texto del tuit, no la afirmación reformulada.
    assert clasificador.textos_recibidos == [PEDIDO_DE_EJEMPLO["texto"]]


def test_version_modelo_es_la_del_clasificador() -> None:
    cuerpo = analizar(ProveedorDoble(), ClasificadorDoble())

    assert cuerpo["version_modelo"] == "tfidf-lr_fakedes_s42"


def test_si_el_clasificador_falla_el_analisis_sale_parcial_y_no_un_500() -> None:
    llm = ProveedorDoble()

    cuerpo = analizar(llm, ClasificadorDoble(error=ErrorDelProveedor("no respondió")))

    assert cuerpo["analisis_parcial"]["es_parcial"] is True
    assert cuerpo["veredicto"] == "sin_contraste_externo"
    assert llm.textos_recibidos == []  # no se gasta la llamada al LLM


def test_sin_afirmacion_verificable_el_comportamiento_es_el_de_siempre() -> None:
    llm = ProveedorDoble(afirmacion="")

    cuerpo = analizar(llm, ClasificadorDoble())

    assert cuerpo["afirmacion"] == ""
    assert cuerpo["veredicto"] == "sin_contraste_externo"
    assert cuerpo["analisis_parcial"]["es_parcial"] is False
    assert cuerpo["fuentes"] == []
    assert llm.afirmaciones_recibidas == []  # no se pidió veredicto


# -- El cliente HTTP real, contra un servidor local de mentira ---------------

@contextmanager
def servicio_de_inferencia(
    estado: int, cuerpo: bytes, demora_s: float = 0, recibidos: list[str] | None = None
) -> Iterator[str]:
    class Manejador(BaseHTTPRequestHandler):
        def do_POST(self) -> None:
            pedido = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            if recibidos is not None:
                recibidos.append(pedido["texto"])
            time.sleep(demora_s)
            self.send_response(estado)
            self.end_headers()
            self.wfile.write(cuerpo)

        def log_message(self, *args: object) -> None:
            pass

    servidor = ThreadingHTTPServer(("127.0.0.1", 0), Manejador)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    try:
        yield f"http://127.0.0.1:{servidor.server_port}"
    finally:
        servidor.shutdown()


RESPUESTA_DEL_SPACE = json.dumps(
    {"puntaje": 0.8, "clase": "falso", "version_modelo": "tfidf-lr_fakedes_s42"}
).encode()


def test_el_cliente_http_trae_puntaje_clase_y_version_del_space() -> None:
    with servicio_de_inferencia(200, RESPUESTA_DEL_SPACE) as url:
        cuerpo = analizar(ProveedorDoble(), ClienteClasificador(url, tiempo_limite_s=2))

    assert cuerpo["puntajes"]["clasificador"] == {"valor": 0.8, "clase": "falso"}
    assert cuerpo["version_modelo"] == "tfidf-lr_fakedes_s42"


@pytest.mark.parametrize(
    ("estado", "cuerpo", "demora_s"),
    [
        (200, RESPUESTA_DEL_SPACE, 1.0),  # vence el tiempo límite
        (503, b"dormido", 0),  # error HTTP
        (200, b"<html>no es JSON</html>", 0),  # respuesta mal formada
        (200, b'{"puntaje": 7, "clase": "falso", "version_modelo": "x"}', 0),
    ],
    ids=["tiempo-limite", "error-http", "mal-formada", "fuera-de-rango"],
)
def test_cualquier_falla_del_cliente_http_deja_el_analisis_parcial(
    estado: int, cuerpo: bytes, demora_s: float
) -> None:
    with servicio_de_inferencia(estado, cuerpo, demora_s) as url:
        respuesta = analizar(ProveedorDoble(), ClienteClasificador(url, tiempo_limite_s=0.3))

    assert respuesta["analisis_parcial"]["es_parcial"] is True


def test_sin_direccion_del_clasificador_el_analisis_sale_parcial() -> None:
    respuesta = analizar(ProveedorDoble(), ClienteClasificador("", tiempo_limite_s=1))

    assert respuesta["analisis_parcial"]["es_parcial"] is True


# -- Llamada periódica para que el Space no se duerma -------------------------
#
# No se ve por `POST /analizar`, así que se prueba la rutina directamente.

def test_la_llamada_periodica_sigue_aunque_el_space_falle() -> None:
    clasificador = ClasificadorDoble(error=ErrorDelProveedor("dormido"))

    async def correr_un_rato() -> None:
        tarea = asyncio.create_task(mantener_despierto(clasificador, intervalo_s=0.01))
        await asyncio.sleep(0.1)
        tarea.cancel()

    asyncio.run(correr_un_rato())

    assert len(clasificador.textos_recibidos) >= 2


def test_con_adaptador_compuesto_el_servicio_despierta_al_space_al_arrancar(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """La configuración por entorno arma el adaptador compuesto de verdad."""
    recibidos: list[str] = []
    with servicio_de_inferencia(200, RESPUESTA_DEL_SPACE, recibidos=recibidos) as url:
        monkeypatch.setenv("ADAPTADOR", "compuesto")
        monkeypatch.setenv("URL_CLASIFICADOR", url)
        obtener_configuracion.cache_clear()
        obtener_proveedor.cache_clear()
        try:
            with TestClient(aplicacion):
                for _ in range(50):
                    if recibidos:
                        break
                    time.sleep(0.02)
            proveedor = obtener_proveedor()
        finally:
            obtener_configuracion.cache_clear()
            obtener_proveedor.cache_clear()

    assert recibidos[0] == "despertar"
    assert isinstance(proveedor, ProveedorCompuesto)
