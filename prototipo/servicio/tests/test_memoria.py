"""Memoria semántica de evidencia del Módulo 3 (ticket #101, PRD #100), por `POST /analizar`.

La memoria envuelve al doble del LLM y va dentro del proveedor compuesto, igual
que en `dependencias.py`. El embebedor es falso y determinista; `sqlite-vec` es
el real, sobre una base en memoria. Ningún test mira tablas ni vectores: cuentan
llamadas al LLM y leen lo que sale por HTTP.
"""

from __future__ import annotations

import hashlib
import json
import logging
import math
import re
from datetime import datetime, timedelta, timezone

import pytest

from app.contrato import Fuente, Postura, TipoFuente
from app.proveedor.clasificador import Clasificacion, ProveedorCompuesto
from app.proveedor.memoria import DIMENSIONES, ClienteEmbebedor, MemoriaDeEvidencia
from app.proveedor.puerto import ErrorDelProveedor

from .conftest import PEDIDO_DE_EJEMPLO, ProveedorDoble, construir_cliente
from .test_clasificador import servicio_de_inferencia

UMBRAL = 0.7

PARAFRASIS = {
    "tweet_id": "1111111111111111111",
    "texto": "Desde el lunes cierran todas las escuelas de la Provincia.",
    "handle": "@otra_cuenta",
}

NO_RELACIONADA = {
    "tweet_id": "2222222222222222222",
    "texto": "Hoy el dólar blue cerró en alza en la City porteña.",
    "handle": "@otra_cuenta",
}

FUENTES = [
    Fuente(
        titulo="Calendario escolar",
        url="https://www.argentina.gob.ar/educacion/calendario",
        tipo=TipoFuente.FUENTE_OFICIAL,
        postura=Postura.CONTRADICE,
    ),
    Fuente(
        titulo="No cierran las escuelas",
        url="https://www.clarin.com/sociedad/escuelas.html",
        tipo=TipoFuente.MEDIO_DE_REFERENCIA,
        postura=Postura.CONTRADICE,
    ),
]


class EmbebedorFalso:
    """Bolsa de palabras en 384 casillas, normalizada. Dos textos que comparten
    casi todas las palabras quedan cerca; dos que no comparten ninguna, lejos.
    Usa SHA-256 y no `hash()`, que cambia de semilla en cada proceso."""

    def __init__(self) -> None:
        self.textos_recibidos: list[str] = []

    def embeber(self, texto: str) -> list[float]:
        self.textos_recibidos.append(texto)
        vector = [0.0] * DIMENSIONES
        for palabra in re.findall(r"\w+", texto.lower()):
            vector[int(hashlib.sha256(palabra.encode()).hexdigest(), 16) % DIMENSIONES] += 1
        norma = math.sqrt(sum(x * x for x in vector))
        return [x / norma for x in vector]


class ClasificadorPorTexto:
    """Puntúa cada texto distinto con un valor distinto: así se ve que, en un
    acierto, el puntaje del Módulo 1 es el de la publicación nueva."""

    def clasificar(self, texto: str) -> Clasificacion:
        puntaje = 0.9 if texto == PEDIDO_DE_EJEMPLO["texto"] else 0.2
        return Clasificacion(
            puntaje=puntaje, clase="falso" if puntaje >= 0.5 else "verdadero", version_modelo="beto"
        )


def proveedor(llm: ProveedorDoble, ruta: str = ":memory:") -> ProveedorCompuesto:
    memoria = MemoriaDeEvidencia(llm, EmbebedorFalso(), ruta, umbral_similitud=UMBRAL)
    return ProveedorCompuesto(memoria, ClasificadorPorTexto())


def analizar_dos(primero: dict, segundo: dict, llm: ProveedorDoble) -> tuple[dict, dict]:
    with construir_cliente(proveedor(llm)) as cliente:
        uno = cliente.post("/analizar", json=primero)
        dos = cliente.post("/analizar", json=segundo)
    assert uno.status_code == dos.status_code == 200
    return uno.json(), dos.json()


def test_una_publicacion_equivalente_reutiliza_la_evidencia_sin_llamar_al_llm() -> None:
    llm = ProveedorDoble(fuentes=FUENTES)

    original, equivalente = analizar_dos(PEDIDO_DE_EJEMPLO, PARAFRASIS, llm)

    assert llm.textos_recibidos == [PEDIDO_DE_EJEMPLO["texto"]]
    assert equivalente["fuentes"] == original["fuentes"]
    assert equivalente["afirmacion"] == original["afirmacion"]
    assert equivalente["tweet_id"] == PARAFRASIS["tweet_id"]


def test_en_un_acierto_el_texto_y_la_cuenta_se_puntuan_de_nuevo() -> None:
    llm = ProveedorDoble(fuentes=FUENTES)
    establecida = {"creada": "2012-03-01T00:00:00Z", "seguidores": 250_000, "seguidos": 400}

    original, equivalente = analizar_dos(
        PEDIDO_DE_EJEMPLO, PARAFRASIS | {"cuenta": establecida, "verificada": True}, llm
    )

    assert original["puntajes"]["clasificador"]["valor"] == pytest.approx(0.9)
    assert equivalente["puntajes"]["clasificador"]["valor"] == pytest.approx(0.2)
    assert original["puntajes"]["credibilidad"]["valor"] is None
    assert equivalente["puntajes"]["credibilidad"]["valor"] == pytest.approx(1.0)


def test_una_publicacion_no_relacionada_vuelve_a_buscar() -> None:
    llm = ProveedorDoble(fuentes=FUENTES)

    analizar_dos(PEDIDO_DE_EJEMPLO, NO_RELACIONADA, llm)

    assert llm.textos_recibidos == [PEDIDO_DE_EJEMPLO["texto"], NO_RELACIONADA["texto"]]


def test_la_memoria_sobrevive_a_un_reinicio(tmp_path) -> None:
    ruta = str(tmp_path / "prototipo.sqlite3")
    with construir_cliente(proveedor(ProveedorDoble(fuentes=FUENTES), ruta)) as cliente:
        original = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO).json()

    llm_tras_reinicio = ProveedorDoble(fuentes=FUENTES)
    with construir_cliente(proveedor(llm_tras_reinicio, ruta)) as cliente:
        equivalente = cliente.post("/analizar", json=PARAFRASIS).json()

    assert llm_tras_reinicio.textos_recibidos == []
    assert equivalente["fuentes"] == original["fuentes"]


def test_el_registro_dice_acierto_o_fallo_y_la_similitud(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.INFO, logger="app.proveedor.memoria"):
        with construir_cliente(proveedor(ProveedorDoble(fuentes=FUENTES))) as cliente:
            for pedido in (PEDIDO_DE_EJEMPLO, PARAFRASIS, NO_RELACIONADA):
                cliente.post("/analizar", json=pedido)

    lineas = [r.getMessage() for r in caplog.records if r.name == "app.proveedor.memoria"]
    assert len(lineas) == 3
    assert lineas[0].startswith("memoria | fallo | similitud=- ")
    assert re.match(r"memoria \| acierto \| similitud=0\.\d{3}$", lineas[1])
    assert re.match(r"memoria \| fallo \| similitud=0\.\d{3} \| motivo=umbral$", lineas[2])


def test_el_cliente_http_del_embebedor_alimenta_la_memoria() -> None:
    """El cliente real contra un servidor local que siempre devuelve el mismo
    vector: la segunda publicación, cualquiera sea, es un acierto."""
    vector = [1.0] + [0.0] * (DIMENSIONES - 1)
    recibidos: list[str] = []
    llm = ProveedorDoble(fuentes=FUENTES)
    cuerpo = json.dumps({"vector": vector}).encode()
    with servicio_de_inferencia(200, cuerpo, recibidos=recibidos) as url:
        memoria = MemoriaDeEvidencia(
            llm, ClienteEmbebedor(url, tiempo_limite_s=2), ":memory:", umbral_similitud=UMBRAL
        )
        with construir_cliente(ProveedorCompuesto(memoria, ClasificadorPorTexto())) as cliente:
            cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO)
            cliente.post("/analizar", json=NO_RELACIONADA)

    assert recibidos == [PEDIDO_DE_EJEMPLO["texto"], NO_RELACIONADA["texto"]]
    assert len(llm.textos_recibidos) == 1


INFLACION = {
    "tweet_id": "3333333333333333333",
    "texto": "Según el INDEC la inflación de septiembre fue de 1,9 % en todo el país.",
    "handle": "@ejemplo",
}

OTRA_INFLACION = {
    "tweet_id": "4444444444444444444",
    "texto": "Según el INDEC la inflación de septiembre fue de 2,3 % en todo el país.",
    "handle": "@otra_cuenta",
}


def lineas_de_la_memoria(caplog: pytest.LogCaptureFixture) -> list[str]:
    return [r.getMessage() for r in caplog.records if r.name == "app.proveedor.memoria"]


def test_dos_textos_similares_con_otros_numeros_no_comparten_evidencia(
    caplog: pytest.LogCaptureFixture,
) -> None:
    llm = ProveedorDoble(fuentes=FUENTES)

    with caplog.at_level(logging.INFO, logger="app.proveedor.memoria"):
        analizar_dos(INFLACION, OTRA_INFLACION, llm)

    assert llm.textos_recibidos == [INFLACION["texto"], OTRA_INFLACION["texto"]]
    assert re.match(
        r"memoria \| fallo \| similitud=0\.\d{3} \| motivo=numeros$",
        lineas_de_la_memoria(caplog)[-1],
    )


class Reloj:
    """Hora que el test adelanta a mano, para vencer evidencia sin esperar días."""

    def __init__(self) -> None:
        self.ahora = datetime(2026, 10, 1, tzinfo=timezone.utc)

    def __call__(self) -> datetime:
        return self.ahora


def test_la_evidencia_vencida_se_vuelve_a_buscar_y_actualiza_la_memoria(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """La tercera publicación tiene el texto de la primera: si la búsqueda nueva
    hubiera agregado una fila en lugar de renovar la vencida, la más cercana
    seguiría siendo la vieja y habría una tercera búsqueda."""
    llm = ProveedorDoble(fuentes=FUENTES)
    reloj = Reloj()
    memoria = MemoriaDeEvidencia(
        llm, EmbebedorFalso(), ":memory:", umbral_similitud=UMBRAL, vigencia_dias=7, reloj=reloj
    )
    misma_que_la_primera = PEDIDO_DE_EJEMPLO | {"tweet_id": "5555555555555555555"}

    with caplog.at_level(logging.INFO, logger="app.proveedor.memoria"):
        with construir_cliente(ProveedorCompuesto(memoria, ClasificadorPorTexto())) as cliente:
            cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO)
            reloj.ahora += timedelta(days=8)
            cliente.post("/analizar", json=PARAFRASIS)
            reloj.ahora += timedelta(hours=1)
            cliente.post("/analizar", json=misma_que_la_primera)

    assert llm.textos_recibidos == [PEDIDO_DE_EJEMPLO["texto"], PARAFRASIS["texto"]]
    lineas = lineas_de_la_memoria(caplog)
    assert re.match(r"memoria \| fallo \| similitud=0\.\d{3} \| motivo=vencida$", lineas[1])
    assert lineas[2].startswith("memoria | acierto")


@pytest.mark.parametrize(
    "llm",
    [
        pytest.param(ProveedorDoble(fuentes=[]), id="sin_fuentes"),
        pytest.param(ProveedorDoble(fuentes=FUENTES, afirmacion=""), id="sin_afirmacion"),
        pytest.param(
            ProveedorDoble(fuentes=FUENTES, error_veredicto=ErrorDelProveedor("caído")),
            id="parcial",
        ),
    ],
)
def test_un_analisis_sin_fuentes_sin_afirmacion_o_parcial_no_alimenta_la_memoria(
    llm: ProveedorDoble,
) -> None:
    analizar_dos(PEDIDO_DE_EJEMPLO, PARAFRASIS, llm)

    assert llm.textos_recibidos == [PEDIDO_DE_EJEMPLO["texto"], PARAFRASIS["texto"]]


class EmbebedorCaido:
    def embeber(self, texto: str) -> list[float]:
        raise ErrorDelProveedor("embebedor | Connection refused")


class EmbebedorQueElAlmacenRechaza:
    """Un vector de otra dimensión: `sqlite-vec` rechaza la consulta, que es
    la forma de hacer fallar al almacén real sin tocar sus tablas."""

    def embeber(self, texto: str) -> list[float]:
        return [1.0, 0.0]


@pytest.mark.parametrize(
    "embebedor",
    [
        pytest.param(EmbebedorCaido(), id="embebedor"),
        pytest.param(EmbebedorQueElAlmacenRechaza(), id="almacen"),
    ],
)
def test_con_la_memoria_caida_el_analisis_sigue_por_la_busqueda_web(
    embebedor, caplog: pytest.LogCaptureFixture
) -> None:
    llm = ProveedorDoble(fuentes=FUENTES)
    memoria = MemoriaDeEvidencia(llm, embebedor, ":memory:", umbral_similitud=UMBRAL)

    with caplog.at_level(logging.INFO, logger="app.proveedor.memoria"):
        with construir_cliente(ProveedorCompuesto(memoria, ClasificadorPorTexto())) as cliente:
            respuestas = [cliente.post("/analizar", json=p) for p in (PEDIDO_DE_EJEMPLO, PARAFRASIS)]

    assert [r.status_code for r in respuestas] == [200, 200]
    assert all(r.json()["analisis_parcial"]["es_parcial"] is False for r in respuestas)
    assert all(r.json()["fuentes"] for r in respuestas)
    assert llm.textos_recibidos == [PEDIDO_DE_EJEMPLO["texto"], PARAFRASIS["texto"]]
    lineas = lineas_de_la_memoria(caplog)
    assert len(lineas) == 2
    assert all(
        linea.startswith("memoria | fallo | similitud=- | motivo=no_disponible")
        for linea in lineas
    )
