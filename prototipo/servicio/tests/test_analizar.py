"""Costura 1 de la *spec*: el contrato HTTP del punto de entrada de análisis.

Todo se prueba por `POST /analizar`. Nada acá conoce el interior del servicio.
"""

from __future__ import annotations

import pytest

from app.contrato import (
    Fuente,
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


# ---------------------------------------------------------------------------
# Jerarquía de evidencia (RF-05)
#
# El filtro se prueba **solo** por el contrato HTTP: el doble devuelve fuentes y
# se mira cuáles llegan a la respuesta. Ningún test de acá importa la función
# que filtra ni sabe si el filtro corre en el orquestador, en el adaptador o en
# los dos. Es lo que permite que en la Entrega 4 el paso de búsqueda se
# reemplace por un índice vectorial local sin tocar una línea de este archivo.
# ---------------------------------------------------------------------------


def fuente(url: str, titulo: str = "Una nota", tipo: TipoFuente | None = None) -> Fuente:
    """Arma una fuente para el doble.

    `tipo` por defecto es el escalón más alto, a propósito: así, cuando el filtro
    corrige el tipo de una fuente, se ve que lo derivó del dominio y no que lo
    copió de lo que el doble había declarado.
    """
    return Fuente(
        titulo=titulo,
        url=url,
        tipo=tipo or TipoFuente.FUENTE_OFICIAL,
        postura=Postura.NEUTRAL,
    )


def test_las_fuentes_de_fuera_de_la_jerarquia_no_llegan_a_la_respuesta() -> None:
    """RF-05: el sistema no cita cualquier resultado de internet.

    El doble devuelve una mezcla de fuentes admisibles y de fuentes de fuera de
    la jerarquía —un blog, una red social, un sitio cualquiera—. Solo las
    admisibles llegan a la respuesta. La razón que enlazaba una fuente
    descartada queda sin enlace, porque una razón no puede apuntar a evidencia
    que la respuesta no muestra (RNF-06).
    """
    doble = ProveedorDoble(
        veredicto=Veredicto.CONTRADICHO_POR_FUENTES_OFICIALES,
        fuentes=[
            fuente("https://www.indec.gob.ar/informe/ipc-julio"),
            fuente("https://blog-de-alguien.test/la-verdad-sobre-la-inflacion"),
            fuente("https://www.clarin.com/economia/inflacion-julio.html"),
            fuente("https://x.com/alguien/status/1234567890"),
            fuente("https://cualquier-sitio.com.ar/nota"),
        ],
        razones=[
            Razon(
                texto="El dato oficial dice otra cosa.",
                fuente_url="https://www.indec.gob.ar/informe/ipc-julio",
            ),
            Razon(
                texto="Un blog sostiene lo contrario.",
                fuente_url="https://blog-de-alguien.test/la-verdad-sobre-la-inflacion",
            ),
        ],
    )

    with construir_cliente(doble) as cliente:
        cuerpo = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO).json()

    assert [f["url"] for f in cuerpo["fuentes"]] == [
        "https://www.indec.gob.ar/informe/ipc-julio",
        "https://www.clarin.com/economia/inflacion-julio.html",
    ]
    assert [razon["fuente_url"] for razon in cuerpo["razones"]] == [
        "https://www.indec.gob.ar/informe/ipc-julio",
        None,
    ]


@pytest.mark.parametrize(
    "url",
    [
        # Contienen el dominio admisible como subcadena, pero no son él ni un
        # subdominio suyo. Un `in` sobre el texto los dejaría pasar a los cuatro,
        # y es la forma que toma la suplantación de un medio.
        "https://no-es-clarin.com/nota",
        "https://clarin.com.desinformacion.test/nota",
        "https://fake-indec.gob.ar.otro.test/informe",
        "https://elclarin.com/nota",
    ],
)
def test_un_dominio_que_apenas_contiene_a_otro_no_pasa_el_filtro(url: str) -> None:
    """La comparación es por anfitrión, no por subcadena."""
    doble = ProveedorDoble(fuentes=[fuente(url)])

    with construir_cliente(doble) as cliente:
        cuerpo = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO).json()

    assert cuerpo["fuentes"] == []
    # Y sin ninguna fuente admisible, el resultado es el que exige RNF-06.
    assert cuerpo["veredicto"] == Veredicto.SIN_CONTRASTE_EXTERNO.value


@pytest.mark.parametrize(
    "url",
    [
        # Las formas reales que toma una URL: con y sin `www`, con un subdominio
        # de verdad, con el anfitrión en mayúsculas y con el punto final del
        # nombre absoluto.
        "https://chequeado.com/ultimas-noticias/es-falso-que/",
        "https://www.chequeado.com/ultimas-noticias/es-falso-que/",
        "https://servicios.infoleg.gob.ar/infolegInternet/anexos/1.htm",
        "HTTPS://WWW.Clarin.COM/economia/nota.html",
        "https://www.lanacion.com.ar./economia/nota",
        "https://www.argentina.gob.ar/salud/campania",
    ],
)
def test_las_formas_reales_de_una_url_admisible_no_quedan_afuera(url: str) -> None:
    """Un subdominio, una mayúscula o un punto final no sacan a una fuente."""
    doble = ProveedorDoble(
        veredicto=Veredicto.PARECE_VERIFICADO, fuentes=[fuente(url)]
    )

    with construir_cliente(doble) as cliente:
        cuerpo = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO).json()

    assert [f["url"] for f in cuerpo["fuentes"]] == [url]


def test_cada_fuente_lleva_titulo_url_y_su_tipo_en_la_jerarquia() -> None:
    """RF-05: el tipo es una propiedad del dominio, no una etiqueta que se copie.

    El doble declara las tres fuentes como oficiales. La respuesta las devuelve
    con el escalón que les corresponde de verdad, porque una fuente etiquetada
    como oficial sin serlo es exactamente lo que la jerarquía existe para
    impedir.
    """
    doble = ProveedorDoble(
        veredicto=Veredicto.INFORMACION_SOSPECHOSA,
        fuentes=[
            fuente("https://www.boletinoficial.gob.ar/detalle/1", "Resolución 1/2026"),
            fuente("https://www.pagina12.com.ar/nota", "Preocupación por las escuelas"),
            fuente("https://chequeado.com/es-falso", "Es falso que cierren todas"),
        ],
    )

    with construir_cliente(doble) as cliente:
        cuerpo = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO).json()

    assert [(f["titulo"], f["url"], f["tipo"]) for f in cuerpo["fuentes"]] == [
        (
            "Resolución 1/2026",
            "https://www.boletinoficial.gob.ar/detalle/1",
            TipoFuente.FUENTE_OFICIAL.value,
        ),
        (
            "Preocupación por las escuelas",
            "https://www.pagina12.com.ar/nota",
            TipoFuente.MEDIO_DE_REFERENCIA.value,
        ),
        (
            "Es falso que cierren todas",
            "https://chequeado.com/es-falso",
            TipoFuente.VERIFICACION_PREVIA.value,
        ),
    ]


def test_las_fuentes_llegan_ordenadas_segun_la_jerarquia() -> None:
    """El orden es la decisión de fondo del panel de evidencia (RF-09).

    Primero las fuentes oficiales, después los medios de referencia, al final
    las verificaciones previas. El doble las devuelve al revés justamente para
    que el orden de la respuesta no pueda venir del orden de entrada.
    """
    doble = ProveedorDoble(
        veredicto=Veredicto.CONTRADICHO_POR_FUENTES_OFICIALES,
        fuentes=[
            fuente("https://chequeado.com/es-falso"),
            fuente("https://www.infobae.com/nota"),
            fuente("https://www.bcra.gob.ar/estadisticas"),
            fuente("https://www.lanacion.com.ar/nota"),
            fuente("https://www.indec.gob.ar/informe"),
        ],
    )

    with construir_cliente(doble) as cliente:
        cuerpo = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO).json()

    assert [f["tipo"] for f in cuerpo["fuentes"]] == [
        TipoFuente.FUENTE_OFICIAL.value,
        TipoFuente.FUENTE_OFICIAL.value,
        TipoFuente.MEDIO_DE_REFERENCIA.value,
        TipoFuente.MEDIO_DE_REFERENCIA.value,
        TipoFuente.VERIFICACION_PREVIA.value,
    ]
    # Dentro de un mismo escalón se conserva el orden en que llegaron: la
    # jerarquía ordena entre clases de fuente, no dentro de una.
    assert [f["url"] for f in cuerpo["fuentes"]][:2] == [
        "https://www.bcra.gob.ar/estadisticas",
        "https://www.indec.gob.ar/informe",
    ]


def test_con_fuentes_admisibles_el_veredicto_de_tres_niveles_sobrevive() -> None:
    """La contracara de RNF-06: con evidencia enlazable sí hay veredicto.

    Sin este caso, la invariante que fuerza *sin contraste externo* pasaría
    igual con un servicio que nunca emitiera ninguno de los tres niveles.
    """
    doble = ProveedorDoble(
        veredicto=Veredicto.CONTRADICHO_POR_FUENTES_OFICIALES,
        fuentes=[fuente("https://www.boletinoficial.gob.ar/detalle/1")],
        razones=[
            Razon(
                texto="La resolución alcanza a 50 establecimientos.",
                fuente_url="https://www.boletinoficial.gob.ar/detalle/1",
            )
        ],
    )

    with construir_cliente(doble) as cliente:
        cuerpo = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO).json()

    assert cuerpo["veredicto"] in NIVELES_DE_VEREDICTO
    assert cuerpo["razones"][0]["fuente_url"] == (
        "https://www.boletinoficial.gob.ar/detalle/1"
    )


def test_la_misma_fuente_no_aparece_dos_veces() -> None:
    """Una nota encontrada por dos caminos se muestra una vez."""
    doble = ProveedorDoble(
        veredicto=Veredicto.PARECE_VERIFICADO,
        fuentes=[
            fuente("https://www.indec.gob.ar/informe"),
            fuente("https://www.indec.gob.ar/informe/"),
        ],
    )

    with construir_cliente(doble) as cliente:
        cuerpo = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO).json()

    assert len(cuerpo["fuentes"]) == 1


def test_la_postura_de_las_fuentes_viaja_declarada() -> None:
    """Toda fuente lleva una postura del dominio cerrado del contrato.

    En esta instancia son todas `neutral`: determinar si cada fuente corrobora o
    contradice es el ticket #24, y hasta entonces la ausencia se declara en
    lugar de inventarse.
    """
    doble = ProveedorDoble(
        veredicto=Veredicto.PARECE_VERIFICADO,
        fuentes=[fuente("https://www.telam.com.ar/notas/1.html")],
    )

    with construir_cliente(doble) as cliente:
        cuerpo = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO).json()

    assert cuerpo["fuentes"][0]["postura"] in {p.value for p in Postura}


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
