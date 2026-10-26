"""Índice de fuentes oficiales del Módulo 3 (ticket #108, PRD #107), por `POST /analizar`.

El adaptador de OpenAI es el real; lo falso es el cliente de OpenAI, que
captura el mensaje y devuelve una salida fija. `sqlite-vec` es el real, sobre
una base en memoria, y el embebedor es el falso y determinista de las pruebas
de la memoria. Ningún test mira tablas: leen el mensaje que llegó al LLM, lo que
sale por HTTP y el registro.
"""

from __future__ import annotations

import json
import logging
import re

import pytest

from app.configuracion import Configuracion
from app.proveedor.indice import Fragmento, IndiceDeFuentes
from app.proveedor.memoria import DIMENSIONES, ClienteEmbebedor, MemoriaDeEvidencia
from app.proveedor.openai import ProveedorOpenAI

from .conftest import PEDIDO_DE_EJEMPLO, construir_cliente
from .test_clasificador import servicio_de_inferencia
from .test_memoria import (
    PARAFRASIS,
    UMBRAL,
    EmbebedorCaido,
    EmbebedorFalso,
    EmbebedorQueElAlmacenRechaza,
)

URL_CALENDARIO = "https://www.argentina.gob.ar/educacion/calendario-escolar-2026"

CERCANO = Fragmento(
    texto="A partir del lunes cierran todas las escuelas de la Provincia por el receso.",
    url=URL_CALENDARIO,
    titulo="Calendario escolar 2026",
    fecha_publicacion="2026-10-01",
    fuente="Ministerio de Educación",
)

LEJANO = Fragmento(
    texto="El BCRA mantuvo la tasa de política monetaria sin cambios en octubre.",
    url="https://www.bcra.gob.ar/comunicado-tasa",
    titulo="Comunicado de política monetaria",
    fecha_publicacion="2026-10-02",
    fuente="BCRA",
)

FUENTE_DEL_INDICE = {
    "titulo": "Calendario escolar 2026",
    "url": URL_CALENDARIO,
    "postura": "contradice",
    "razon": "El calendario oficial no prevé el cierre de las escuelas.",
}


class ClienteOpenAIFalso:
    """Lo mínimo del SDK que usa el adaptador: `responses.parse`. Guarda cada
    mensaje recibido y devuelve siempre la misma salida, validada con el
    esquema que pide el adaptador."""

    def __init__(self, fuentes: list[dict]) -> None:
        self.mensajes: list[str] = []
        self.salida = {
            "afirmacion": "Cierran todas las escuelas de la Provincia desde el lunes.",
            "tipo": "educacion",
            "puntaje": 0.7,
            "clase": "sin_verificar",
            "fuentes": fuentes,
        }
        self.responses = self

    def parse(self, *, input: str, text_format, **_: object) -> object:
        self.mensajes.append(input)
        return type("Respuesta", (), {
            "output_parsed": text_format.model_validate(self.salida),
            "usage": None,
            "status": "completed",
        })()


@pytest.fixture
def openai_falso(monkeypatch: pytest.MonkeyPatch):
    def armar(fuentes: list[dict] | None = None) -> ClienteOpenAIFalso:
        cliente = ClienteOpenAIFalso([FUENTE_DEL_INDICE] if fuentes is None else fuentes)
        monkeypatch.setattr("app.proveedor.openai.OpenAI", lambda **_: cliente)
        return cliente
    return armar


def configuracion(**cambios: object) -> Configuracion:
    return Configuracion(_env_file=None, openai_api_key="falsa", **cambios)


def indice_con(*fragmentos: Fragmento, embebedor=None) -> IndiceDeFuentes:
    indice = IndiceDeFuentes(":memory:", embebedor or EmbebedorFalso())
    indice.agregar(list(fragmentos))
    return indice


def analizar(proveedor, pedido: dict = PEDIDO_DE_EJEMPLO) -> dict:
    with construir_cliente(proveedor) as cliente:
        respuesta = cliente.post("/analizar", json=pedido)
    assert respuesta.status_code == 200
    return respuesta.json()


def lineas_del_indice(caplog: pytest.LogCaptureFixture) -> list[str]:
    return [
        r.getMessage() for r in caplog.records
        if r.name == "app.proveedor.openai" and r.getMessage().startswith("indice |")
    ]


def test_un_fragmento_cercano_llega_al_mensaje_y_vuelve_como_fuente_oficial(
    openai_falso, caplog: pytest.LogCaptureFixture
) -> None:
    llm = openai_falso()
    proveedor = ProveedorOpenAI(configuracion(), indice_con(CERCANO, LEJANO))

    with caplog.at_level(logging.INFO, logger="app.proveedor.openai"):
        respuesta = analizar(proveedor)

    mensaje = llm.mensajes[0]
    bloque = re.search(r"<documentos_oficiales>(.*)</documentos_oficiales>", mensaje, re.S)
    assert bloque is not None
    assert CERCANO.texto in bloque.group(1) and CERCANO.url in bloque.group(1)
    assert LEJANO.texto not in mensaje
    assert respuesta["fuentes"][0]["url"] == URL_CALENDARIO
    assert respuesta["fuentes"][0]["tipo"] == "fuente_oficial"
    assert respuesta["analisis_parcial"]["es_parcial"] is False
    assert re.match(r"indice \| fragmentos=1 \| similitud=0\.\d{3}$", lineas_del_indice(caplog)[0])


def test_se_entregan_como_mucho_k_fragmentos_sobre_el_umbral(openai_falso) -> None:
    llm = openai_falso()
    parecidos = [
        Fragmento(
            texto=f"A partir del lunes cierran todas las escuelas de la Provincia, aviso {n}.",
            url=f"{URL_CALENDARIO}/{n}", titulo="t", fecha_publicacion="2026-10-01",
            fuente="Ministerio de Educación",
        )
        for n in range(4)
    ]
    proveedor = ProveedorOpenAI(
        configuracion(fragmentos_indice=2), indice_con(*parecidos, LEJANO)
    )

    analizar(proveedor)

    assert llm.mensajes[0].count("<documento ") == 2


def test_un_fragmento_debajo_del_umbral_no_llega_y_el_mensaje_es_el_de_siempre(
    openai_falso, caplog: pytest.LogCaptureFixture
) -> None:
    sin_indice = openai_falso()
    analizar(ProveedorOpenAI(configuracion()))
    con_lejano = openai_falso()

    with caplog.at_level(logging.INFO, logger="app.proveedor.openai"):
        analizar(ProveedorOpenAI(configuracion(), indice_con(LEJANO)))

    assert con_lejano.mensajes == sin_indice.mensajes
    assert re.match(
        r"indice \| fragmentos=0 \| similitud=0\.\d{3} \| motivo=umbral$",
        lineas_del_indice(caplog)[0],
    )


def test_con_el_indice_vacio_el_mensaje_es_el_de_siempre(
    openai_falso, caplog: pytest.LogCaptureFixture
) -> None:
    sin_indice = openai_falso()
    analizar(ProveedorOpenAI(configuracion()))
    con_vacio = openai_falso()

    with caplog.at_level(logging.INFO, logger="app.proveedor.openai"):
        analizar(ProveedorOpenAI(configuracion(), indice_con()))

    assert con_vacio.mensajes == sin_indice.mensajes
    assert lineas_del_indice(caplog) == ["indice | fragmentos=0 | similitud=- | motivo=vacio"]


def test_las_instrucciones_tratan_los_fragmentos_como_datos(openai_falso) -> None:
    from app.proveedor.openai import INSTRUCCIONES_EXTRACCION_Y_EVIDENCIA as instrucciones

    assert "<documentos_oficiales>" in instrucciones
    assert "nunca una orden" in instrucciones.split("<documentos_oficiales>", 1)[1]


def test_una_url_del_indice_que_tambien_trae_la_busqueda_queda_una_sola_vez(
    openai_falso,
) -> None:
    openai_falso([FUENTE_DEL_INDICE, FUENTE_DEL_INDICE | {"url": URL_CALENDARIO + "/"}])

    respuesta = analizar(ProveedorOpenAI(configuracion(), indice_con(CERCANO)))

    assert [f["url"] for f in respuesta["fuentes"]] == [URL_CALENDARIO]


def test_un_acierto_de_la_memoria_no_consulta_el_indice(
    openai_falso, caplog: pytest.LogCaptureFixture
) -> None:
    llm = openai_falso()
    embebedor = EmbebedorFalso()
    adaptador = ProveedorOpenAI(configuracion(), indice_con(CERCANO, embebedor=embebedor))
    memoria = MemoriaDeEvidencia(
        adaptador, embebedor, ":memory:", umbral_similitud=UMBRAL, vigencia_dias=7
    )

    with caplog.at_level(logging.INFO, logger="app.proveedor.openai"):
        with construir_cliente(memoria) as cliente:
            cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO)
            cliente.post("/analizar", json=PARAFRASIS)

    assert len(llm.mensajes) == 1
    assert len(lineas_del_indice(caplog)) == 1


def test_la_memoria_y_el_indice_hacen_un_solo_pedido_a_embeber(openai_falso) -> None:
    """Con un servidor que siempre devuelve el mismo vector, todo es cercano:
    la memoria vacía falla, el índice acierta, y el texto se embebe una vez."""
    llm = openai_falso()
    recibidos: list[str] = []
    cuerpo = json.dumps({"vector": [1.0] + [0.0] * (DIMENSIONES - 1)}).encode()
    with servicio_de_inferencia(200, cuerpo, recibidos=recibidos) as url:
        embebedor = ClienteEmbebedor(url, tiempo_limite_s=2)
        adaptador = ProveedorOpenAI(configuracion(), indice_con(CERCANO, embebedor=embebedor))
        memoria = MemoriaDeEvidencia(
            adaptador, embebedor, ":memory:", umbral_similitud=UMBRAL, vigencia_dias=7
        )
        analizar(memoria)

    assert recibidos == [CERCANO.texto, PEDIDO_DE_EJEMPLO["texto"]]
    assert CERCANO.url in llm.mensajes[0]


@pytest.mark.parametrize(
    "embebedor",
    [
        pytest.param(EmbebedorCaido(), id="embebedor"),
        pytest.param(EmbebedorQueElAlmacenRechaza(), id="almacen"),
    ],
)
def test_con_el_indice_caido_el_analisis_se_completa_sin_el_bloque(
    embebedor, openai_falso, caplog: pytest.LogCaptureFixture
) -> None:
    sin_indice = openai_falso()
    analizar(ProveedorOpenAI(configuracion()))
    llm = openai_falso()
    indice = IndiceDeFuentes(":memory:", embebedor)

    with caplog.at_level(logging.INFO, logger="app.proveedor.openai"):
        respuesta = analizar(ProveedorOpenAI(configuracion(), indice))

    assert respuesta["analisis_parcial"]["es_parcial"] is False
    assert llm.mensajes == sin_indice.mensajes
    assert lineas_del_indice(caplog)[0].startswith(
        "indice | fragmentos=0 | similitud=- | motivo=no_disponible | "
    )
