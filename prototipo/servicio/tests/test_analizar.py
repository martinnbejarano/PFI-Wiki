"""Costura 1 de la *spec*: el contrato HTTP del punto de entrada de análisis.

Todo se prueba por `POST /analizar`. Nada acá conoce el interior del servicio.
"""

from __future__ import annotations

import pytest

from app.contrato import (
    Postura,
    Razon,
    RespuestaAnalisis,
    TipoAfirmacion,
    TipoFuente,
    Veredicto,
)
from app.proveedor.puerto import ErrorDelProveedor

from .conftest import (
    PEDIDO_DE_EJEMPLO,
    ProveedorDoble,
    afirmacion_extraida_de,
    construir_cliente,
)

NIVELES_DE_VEREDICTO = {
    Veredicto.CONTRADICHO_POR_FUENTES_OFICIALES.value,
    Veredicto.INFORMACION_SOSPECHOSA.value,
    Veredicto.PARECE_VERIFICADO.value,
}


def test_el_servicio_esta_vivo_sin_credencial(cliente) -> None:
    """El servicio arranca y responde aunque no haya credencial del proveedor."""
    respuesta = cliente.get("/salud")

    assert respuesta.status_code == 200
    assert respuesta.json() == {"estado": "vivo"}


def test_camino_feliz(cliente, proveedor_doble) -> None:
    """Entra un tuit y sale un análisis con veredicto y justificación."""
    respuesta = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO)

    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert cuerpo["tweet_id"] == PEDIDO_DE_EJEMPLO["tweet_id"]
    assert cuerpo["veredicto"] == Veredicto.SIN_CONTRASTE_EXTERNO.value
    assert cuerpo["justificacion"] == proveedor_doble.justificacion
    assert len(cuerpo["razones"]) == len(proveedor_doble.razones)


def test_el_analisis_se_hace_sobre_el_texto_del_tuit(cliente, proveedor_doble) -> None:
    """El análisis parte del tuit que llegó, no de un texto fijo."""
    pedido = PEDIDO_DE_EJEMPLO | {
        "texto": "El índice de precios de julio fue del 1,2 por ciento.",
    }

    respuesta = cliente.post("/analizar", json=pedido)

    assert respuesta.status_code == 200
    afirmacion = respuesta.json()["afirmacion"]
    assert proveedor_doble.textos_recibidos == [pedido["texto"]]
    assert afirmacion == afirmacion_extraida_de(pedido["texto"])
    # El juicio se emitió sobre la afirmación que salió del análisis y no sobre
    # otra cosa: es lo que vuelve interpretable el resultado para quien lee.
    assert proveedor_doble.afirmaciones_recibidas == [afirmacion]


def test_la_respuesta_trae_la_afirmacion_verificable_y_su_tipo() -> None:
    """RF-04: la afirmación es la extraída del tuit, no el texto crudo.

    Es lo que le permite al ciudadano juzgar si el sistema analizó lo que él
    quería que analizara.
    """
    doble = ProveedorDoble(
        afirmacion="El índice de precios de julio fue del 1,2 por ciento.",
        tipo=TipoAfirmacion.DATO_ECONOMICO,
    )
    pedido = PEDIDO_DE_EJEMPLO | {
        "texto": "🚨 MIREN ESTO: la inflación de julio dio 1,2%!!! COMPARTAN 🚨",
    }

    with construir_cliente(doble) as cliente:
        cuerpo = cliente.post("/analizar", json=pedido).json()

    assert cuerpo["afirmacion"] == "El índice de precios de julio fue del 1,2 por ciento."
    assert cuerpo["afirmacion"] != pedido["texto"]
    assert cuerpo["tipo_afirmacion"] == TipoAfirmacion.DATO_ECONOMICO.value


def test_el_puntaje_del_clasificador_sale_del_analisis_del_texto() -> None:
    """El desglose expone lo que aportó el análisis del texto, no un valor fijo."""
    doble = ProveedorDoble(puntaje_clasificador=0.83, clase_clasificador="falso")

    with construir_cliente(doble) as cliente:
        cuerpo = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO).json()

    assert cuerpo["puntajes"]["clasificador"] == {"valor": 0.83, "clase": "falso"}


def test_un_tuit_sin_afirmacion_verificable_no_recibe_veredicto() -> None:
    """Una opinión o una broma no son ni verdaderas ni falsas.

    La respuesta llega completa y con código 200 —no es un error—, con la
    afirmación vacía, sin veredicto de tres niveles y con una justificación que
    explica que no hay nada que verificar.
    """
    doble = ProveedorDoble(afirmacion="", tipo=TipoAfirmacion.OTRO)
    pedido = PEDIDO_DE_EJEMPLO | {"texto": "Qué lindo día para tomar mate ☀️"}

    with construir_cliente(doble) as cliente:
        respuesta = cliente.post("/analizar", json=pedido)

    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert cuerpo["afirmacion"] == ""
    assert cuerpo["veredicto"] == Veredicto.SIN_CONTRASTE_EXTERNO.value
    assert cuerpo["veredicto"] not in NIVELES_DE_VEREDICTO
    assert cuerpo["justificacion"]
    assert cuerpo["razones"]
    # No es una degradación: todos los módulos se ejecutaron y el resultado es
    # que no había nada que contrastar.
    assert cuerpo["analisis_parcial"]["es_parcial"] is False


def test_el_puntaje_de_credibilidad_es_estable_para_el_mismo_handle() -> None:
    """El mismo *handle* devuelve siempre el mismo valor.

    Es lo que evita el único modo de falla visible en vivo: que el número
    parpadee entre dos recargas del mismo tuit durante la exposición. Se
    comprueba con dos tuits distintos de la misma cuenta para que ninguna caché
    por identificador de tuit pueda hacer pasar el test por el motivo
    equivocado.
    """
    doble = ProveedorDoble()

    with construir_cliente(doble) as cliente:
        primero = cliente.post(
            "/analizar", json=PEDIDO_DE_EJEMPLO | {"handle": "@data_economia_arg"}
        ).json()
        segundo = cliente.post(
            "/analizar",
            json=PEDIDO_DE_EJEMPLO
            | {"tweet_id": "9876543210987654321", "handle": "@data_economia_arg"},
        ).json()

    assert (
        primero["puntajes"]["credibilidad"]["valor"]
        == segundo["puntajes"]["credibilidad"]["valor"]
    )


def test_dos_cuentas_distintas_no_comparten_el_puntaje_de_credibilidad() -> None:
    """El valor depende de la cuenta: no es una constante disfrazada."""
    doble = ProveedorDoble()

    with construir_cliente(doble) as cliente:
        una = cliente.post(
            "/analizar", json=PEDIDO_DE_EJEMPLO | {"handle": "@alerta_urgente_ar"}
        ).json()
        otra = cliente.post(
            "/analizar", json=PEDIDO_DE_EJEMPLO | {"handle": "@martina_ruiz_ok"}
        ).json()

    assert (
        una["puntajes"]["credibilidad"]["valor"]
        != otra["puntajes"]["credibilidad"]["valor"]
    )


def test_forma_completa_de_la_respuesta(cliente) -> None:
    """Todos los campos del contrato están presentes y bien tipados."""
    respuesta = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO)

    assert respuesta.status_code == 200
    cuerpo = respuesta.json()

    # Validar contra el contrato es lo que comprueba el tipado de cada campo:
    # los enumerados cerrados, los rangos de los puntajes y los campos que no
    # admiten ausencia.
    analisis = RespuestaAnalisis.model_validate(cuerpo)

    assert set(cuerpo) == set(RespuestaAnalisis.model_fields)
    assert isinstance(analisis.afirmacion, str) and analisis.afirmacion
    assert isinstance(analisis.tipo_afirmacion, TipoAfirmacion)
    assert isinstance(analisis.veredicto, Veredicto)
    assert isinstance(analisis.justificacion, str) and analisis.justificacion
    assert 0.0 <= analisis.puntajes.clasificador.valor <= 1.0
    assert 0.0 <= analisis.puntajes.credibilidad.valor <= 1.0
    assert 0.0 <= analisis.puntajes.contraste.valor <= 1.0
    assert 0.0 <= analisis.puntaje_final <= 1.0
    assert isinstance(analisis.razones, list) and analisis.razones
    assert isinstance(analisis.fuentes, list)
    assert isinstance(analisis.analisis_parcial.es_parcial, bool)
    assert isinstance(analisis.analisis_parcial.modulos_ausentes, list)
    for fuente in analisis.fuentes:
        assert isinstance(fuente.tipo, TipoFuente)
        assert isinstance(fuente.postura, Postura)


def test_el_modulo_de_credibilidad_viaja_marcado(cliente) -> None:
    """El puntaje de credibilidad se declara no implementado, no se disfraza."""
    respuesta = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO)

    assert respuesta.json()["puntajes"]["credibilidad"]["no_implementado"] is True


def test_sin_fuentes_no_hay_veredicto_de_tres_niveles(cliente) -> None:
    """Sin fuentes recuperadas, el estado es *sin contraste externo*."""
    cuerpo = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO).json()

    assert cuerpo["fuentes"] == []
    assert cuerpo["veredicto"] == Veredicto.SIN_CONTRASTE_EXTERNO.value
    assert cuerpo["veredicto"] not in NIVELES_DE_VEREDICTO


@pytest.mark.parametrize(
    "nivel",
    [
        Veredicto.CONTRADICHO_POR_FUENTES_OFICIALES,
        Veredicto.INFORMACION_SOSPECHOSA,
        Veredicto.PARECE_VERIFICADO,
    ],
)
def test_un_nivel_emitido_sin_fuentes_no_llega_a_la_respuesta(nivel: Veredicto) -> None:
    """RNF-06 es una invariante del servicio, no una sugerencia al proveedor.

    Aunque el proveedor devuelva uno de los tres niveles, sin ninguna fuente
    enlazable la respuesta lo emite como *sin contraste externo*.
    """
    doble = ProveedorDoble(veredicto=nivel, fuentes=[])

    with construir_cliente(doble) as cliente:
        cuerpo = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO).json()

    assert cuerpo["veredicto"] == Veredicto.SIN_CONTRASTE_EXTERNO.value


def test_sin_fuentes_ninguna_razon_lleva_enlace() -> None:
    """Una razón no puede enlazar evidencia que nadie recuperó (RNF-06)."""
    doble = ProveedorDoble(
        razones=[
            Razon(texto="Un medio lo desmiente.", fuente_url="https://inventado.test/"),
            Razon(texto="La publicación no cita ninguna fuente.", fuente_url=None),
        ],
        fuentes=[],
    )

    with construir_cliente(doble) as cliente:
        cuerpo = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO).json()

    assert [razon["fuente_url"] for razon in cuerpo["razones"]] == [None, None]


def test_la_respuesta_incluye_las_versiones_de_trazabilidad(cliente) -> None:
    """RF-16: cada análisis viaja asociado al modelo y a la configuración."""
    cuerpo = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO).json()

    assert isinstance(cuerpo["version_modelo"], str)
    assert cuerpo["version_modelo"]
    assert isinstance(cuerpo["version_configuracion_pesos"], str)
    assert cuerpo["version_configuracion_pesos"]


def test_una_falla_del_proveedor_devuelve_un_mensaje_claro() -> None:
    """Una falla del proveedor no se filtra como error opaco."""
    doble = ProveedorDoble(
        error=ErrorDelProveedor("Falta la credencial del proveedor.")
    )

    with construir_cliente(doble) as cliente:
        respuesta = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO)

    assert respuesta.status_code == 503
    assert "credencial" in respuesta.json()["detalle"]


def test_un_pedido_incompleto_se_rechaza(cliente) -> None:
    """El contrato de entrada también se hace valer."""
    respuesta = cliente.post("/analizar", json={"tweet_id": "1"})

    assert respuesta.status_code == 422
