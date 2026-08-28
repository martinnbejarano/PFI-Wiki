"""Costura 1 de la *spec*: el contrato HTTP del punto de entrada de análisis.

Todo se prueba por `POST /analizar`. Nada acá conoce el interior del servicio.
"""

from __future__ import annotations

import pytest

from app.configuracion import Configuracion
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

from app.cache import CacheDeAnalisis

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
    """El valor depende de la cuenta: no es una constante disfrazada.

    Los dos tuits llevan identificadores distintos, como dos tuits de dos
    cuentas distintas en el mundo real: un mismo identificador nativo publicado
    por dos cuentas no existe, y pedirlo dos veces es pedir el mismo análisis
    (RF-07).
    """
    doble = ProveedorDoble()

    with construir_cliente(doble) as cliente:
        una = cliente.post(
            "/analizar",
            json=PEDIDO_DE_EJEMPLO | {"handle": "@alerta_urgente_ar"},
        ).json()
        otra = cliente.post(
            "/analizar",
            json=PEDIDO_DE_EJEMPLO
            | {"tweet_id": "9876543210987654321", "handle": "@martina_ruiz_ok"},
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


@pytest.mark.parametrize("puntaje_del_texto", [0.02, 0.5, 0.99])
def test_sin_fuentes_ningun_puntaje_alcanza_un_nivel(puntaje_del_texto: float) -> None:
    """RNF-06 es una invariante del servicio y no depende de ningún puntaje.

    Los tres puntajes barren la escala del clasificador: con evidencia, cada uno
    caería en un nivel distinto. Sin ninguna fuente enlazable, los tres terminan
    en *sin contraste externo*, porque el estado no es un escalón más bajo de la
    misma escala sino la ausencia de algo contra lo cual contrastar.
    """
    doble = ProveedorDoble(fuentes=[], puntaje_clasificador=puntaje_del_texto)

    with construir_cliente(doble) as cliente:
        cuerpo = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO).json()

    assert cuerpo["veredicto"] == Veredicto.SIN_CONTRASTE_EXTERNO.value
    assert cuerpo["veredicto"] not in NIVELES_DE_VEREDICTO


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


def fuente(
    url: str,
    titulo: str = "Una nota",
    tipo: TipoFuente | None = None,
    postura: Postura = Postura.NEUTRAL,
) -> Fuente:
    """Arma una fuente para el doble.

    `tipo` por defecto es el escalón más alto, a propósito: así, cuando el filtro
    corrige el tipo de una fuente, se ve que lo derivó del dominio y no que lo
    copió de lo que el doble había declarado.

    `postura` por defecto es `neutral`, que es la que no inclina el resultado
    para ningún lado: un test que no hable de posturas no queda dependiendo de
    una sin darse cuenta.
    """
    return Fuente(
        titulo=titulo,
        url=url,
        tipo=tipo or TipoFuente.FUENTE_OFICIAL,
        postura=postura,
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
    doble = ProveedorDoble(fuentes=[fuente(url)])

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
        fuentes=[
            fuente("https://www.indec.gob.ar/informe"),
            fuente("https://www.indec.gob.ar/informe/"),
        ],
    )

    with construir_cliente(doble) as cliente:
        cuerpo = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO).json()

    assert len(cuerpo["fuentes"]) == 1


def test_cada_fuente_llega_etiquetada_con_su_postura() -> None:
    """RF-05: cada fuente dice si corrobora, contradice o no se pronuncia.

    Es lo que le permite al ciudadano pesar la evidencia por su cuenta en lugar
    de depender del veredicto, y es lo que el panel de evidencia dibuja en la
    columna izquierda de cada fila.
    """
    doble = ProveedorDoble(
        fuentes=[
            fuente(
                "https://www.boletinoficial.gob.ar/detalle/1",
                postura=Postura.CONTRADICE,
            ),
            fuente("https://www.infobae.com/nota", postura=Postura.CORROBORA),
            fuente("https://www.telam.com.ar/notas/1.html", postura=Postura.NEUTRAL),
        ],
    )

    with construir_cliente(doble) as cliente:
        cuerpo = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO).json()

    assert [f["postura"] for f in cuerpo["fuentes"]] == [
        Postura.CONTRADICE.value,
        Postura.CORROBORA.value,
        Postura.NEUTRAL.value,
    ]
    # Y ninguna se escapa del dominio cerrado del contrato.
    assert all(f["postura"] in {p.value for p in Postura} for f in cuerpo["fuentes"])


# ---------------------------------------------------------------------------
# El combinador, los tres niveles y su configuración (RF-06, RNF-16)
#
# Nada de acá importa el módulo que combina puntajes ni sabe cómo se llama. Todo
# entra por `POST /analizar` y se mira lo que sale: el puntaje de contraste, el
# puntaje final y el nivel del veredicto. Los pesos y los umbrales se mueven
# sustituyendo la configuración por dependencia, exactamente igual que se
# sustituye el puerto del proveedor, que es lo que RNF-16 pide poder hacer sin
# volver a desplegar el servicio.
#
# Los números esperados salen de aplicar a mano la fórmula documentada con los
# valores por defecto: 0,35 al análisis del texto, 0,00 a la credibilidad de la
# cuenta y 0,65 al contraste.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("fuentes", "puntaje_del_texto", "nivel_esperado"),
    [
        # Una fuente oficial que contradice y un texto con señales de alarma:
        # el contraste queda en 1,00 y el puntaje final llega al corte severo.
        (
            [
                fuente(
                    "https://www.boletinoficial.gob.ar/detalle/1",
                    postura=Postura.CONTRADICE,
                )
            ],
            0.90,
            Veredicto.CONTRADICHO_POR_FUENTES_OFICIALES,
        ),
        # Un medio que trata el tema sin pronunciarse: el contraste queda en el
        # punto medio y el resultado depende de lo que aportó el texto.
        (
            [fuente("https://www.clarin.com/nota", postura=Postura.NEUTRAL)],
            0.62,
            Veredicto.INFORMACION_SOSPECHOSA,
        ),
        # Una fuente oficial que corrobora y un texto sobrio: nada apunta a
        # desinformación.
        (
            [
                fuente(
                    "https://www.indec.gob.ar/informe", postura=Postura.CORROBORA
                )
            ],
            0.10,
            Veredicto.PARECE_VERIFICADO,
        ),
    ],
)
def test_los_tres_niveles_de_rf06_son_alcanzables(
    fuentes: list[Fuente], puntaje_del_texto: float, nivel_esperado: Veredicto
) -> None:
    """Los tres niveles de RF-06 se alcanzan combinando evidencia.

    Sin este caso, un servicio que emitiera siempre el mismo nivel pasaría
    igual todo el resto de la batería.
    """
    doble = ProveedorDoble(fuentes=fuentes, puntaje_clasificador=puntaje_del_texto)

    with construir_cliente(doble) as cliente:
        cuerpo = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO).json()

    assert cuerpo["veredicto"] == nivel_esperado.value
    assert cuerpo["veredicto"] in NIVELES_DE_VEREDICTO


@pytest.mark.parametrize(
    ("postura", "contraste_esperado"),
    [
        (Postura.CONTRADICE, 1.0),
        (Postura.CORROBORA, 0.0),
        (Postura.NEUTRAL, 0.5),
    ],
)
def test_el_puntaje_de_contraste_sale_de_la_postura_de_las_fuentes(
    postura: Postura, contraste_esperado: float
) -> None:
    """El puntaje de contraste no es un valor fijo: lo mueve la evidencia.

    Con las tres fuentes en la misma postura el resultado es el extremo o el
    punto medio de la escala, según corresponda.
    """
    doble = ProveedorDoble(
        fuentes=[
            fuente("https://www.indec.gob.ar/informe", postura=postura),
            fuente("https://www.clarin.com/nota", postura=postura),
            fuente("https://chequeado.com/es-falso", postura=postura),
        ],
    )

    with construir_cliente(doble) as cliente:
        cuerpo = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO).json()

    assert cuerpo["puntajes"]["contraste"]["valor"] == pytest.approx(
        contraste_esperado
    )


def test_la_jerarquia_pesa_en_el_puntaje_de_contraste() -> None:
    """Una fuente oficial no vale lo mismo que una verificación previa.

    Las dos situaciones tienen la misma cantidad de fuentes y las mismas dos
    posturas; lo único que cambia es de qué escalón viene cada una. Si la
    jerarquía fuera decorativa, el puntaje de contraste sería el mismo en las
    dos y quedaría en el punto medio.
    """
    oficial_contradice = ProveedorDoble(
        fuentes=[
            fuente("https://www.indec.gob.ar/informe", postura=Postura.CONTRADICE),
            fuente("https://chequeado.com/es-falso", postura=Postura.CORROBORA),
        ],
    )
    oficial_corrobora = ProveedorDoble(
        fuentes=[
            fuente("https://www.indec.gob.ar/informe", postura=Postura.CORROBORA),
            fuente("https://chequeado.com/es-falso", postura=Postura.CONTRADICE),
        ],
    )

    with construir_cliente(oficial_contradice) as cliente:
        con_oficial_en_contra = cliente.post(
            "/analizar", json=PEDIDO_DE_EJEMPLO
        ).json()["puntajes"]["contraste"]["valor"]

    with construir_cliente(oficial_corrobora) as cliente:
        con_oficial_a_favor = cliente.post(
            "/analizar", json=PEDIDO_DE_EJEMPLO
        ).json()["puntajes"]["contraste"]["valor"]

    assert con_oficial_en_contra > 0.5 > con_oficial_a_favor


def test_cambiar_un_peso_en_la_configuracion_cambia_el_puntaje_final() -> None:
    """RNF-16: los pesos del ensamblado se ajustan sin volver a desplegar.

    La misma entrada y el mismo doble, con dos juegos de pesos distintos, dan
    dos puntajes finales distintos. Es lo que hace defendible la demostración:
    el peso se mueve en vivo y el resultado se mueve con él.
    """
    doble = ProveedorDoble(
        fuentes=[
            fuente("https://www.indec.gob.ar/informe", postura=Postura.CONTRADICE)
        ],
        puntaje_clasificador=0.20,
    )

    with construir_cliente(doble) as cliente:
        con_pesos_por_defecto = cliente.post(
            "/analizar", json=PEDIDO_DE_EJEMPLO
        ).json()["puntaje_final"]

    # El contraste deja de pesar: el puntaje final queda en lo que aportó el
    # análisis del texto y nada más.
    solo_el_texto = Configuracion(peso_clasificador=1.0, peso_contraste=0.0)
    with construir_cliente(doble, configuracion=solo_el_texto) as cliente:
        con_pesos_cambiados = cliente.post(
            "/analizar", json=PEDIDO_DE_EJEMPLO
        ).json()["puntaje_final"]

    assert con_pesos_por_defecto != con_pesos_cambiados
    assert con_pesos_por_defecto == pytest.approx(0.35 * 0.20 + 0.65 * 1.0)
    assert con_pesos_cambiados == pytest.approx(0.20)


def test_cambiar_un_umbral_en_la_configuracion_cambia_el_nivel() -> None:
    """RNF-16: los umbrales de los veredictos también son configuración.

    La misma entrada produce el mismo puntaje final y dos veredictos distintos,
    porque lo único que se movió fue dónde está el corte del nivel severo.
    """
    doble = ProveedorDoble(
        fuentes=[
            fuente(
                "https://www.boletinoficial.gob.ar/detalle/1",
                postura=Postura.CONTRADICE,
            )
        ],
        # El contraste queda en 1,00 y el puntaje final en 0,65, justo por
        # debajo del corte severo por defecto, que es 0,70.
        puntaje_clasificador=0.0,
    )

    with construir_cliente(doble) as cliente:
        con_umbrales_por_defecto = cliente.post(
            "/analizar", json=PEDIDO_DE_EJEMPLO
        ).json()

    corte_mas_bajo = Configuracion(umbral_contradicho_por_fuentes_oficiales=0.60)
    with construir_cliente(doble, configuracion=corte_mas_bajo) as cliente:
        con_corte_mas_bajo = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO).json()

    assert con_umbrales_por_defecto["puntaje_final"] == pytest.approx(
        con_corte_mas_bajo["puntaje_final"]
    )
    assert con_umbrales_por_defecto["veredicto"] == (
        Veredicto.INFORMACION_SOSPECHOSA.value
    )
    assert con_corte_mas_bajo["veredicto"] == (
        Veredicto.CONTRADICHO_POR_FUENTES_OFICIALES.value
    )


def test_el_puntaje_final_no_lo_contamina_el_modulo_no_implementado() -> None:
    """El valor inventado del Módulo 2 no entra en el resultado.

    Dos cuentas distintas producen dos puntajes de credibilidad distintos —el
    valor se deriva del *handle*— y el mismo puntaje final, porque el peso de
    ese módulo es cero mientras no mida nada. La cifra sigue viajando marcada
    para que la interfaz pueda mostrar el desglose y decir qué es.

    Los identificadores de los dos tuits son distintos, como los de dos
    publicaciones de dos cuentas distintas: repetir el identificador sería pedir
    dos veces el mismo análisis, que es lo que RF-07 resuelve reusando el
    anterior.
    """
    doble = ProveedorDoble(
        fuentes=[
            fuente("https://www.indec.gob.ar/informe", postura=Postura.CONTRADICE)
        ],
    )

    with construir_cliente(doble) as cliente:
        una = cliente.post(
            "/analizar",
            json=PEDIDO_DE_EJEMPLO | {"handle": "@alerta_urgente_ar"},
        ).json()
        otra = cliente.post(
            "/analizar",
            json=PEDIDO_DE_EJEMPLO
            | {"tweet_id": "9876543210987654321", "handle": "@martina_ruiz_ok"},
        ).json()

    assert (
        una["puntajes"]["credibilidad"]["valor"]
        != otra["puntajes"]["credibilidad"]["valor"]
    )
    assert una["puntaje_final"] == pytest.approx(otra["puntaje_final"])
    assert una["puntajes"]["credibilidad"]["no_implementado"] is True


def test_el_peso_de_la_credibilidad_es_una_decision_y_no_un_cableado() -> None:
    """Que pese cero es configuración, no una rama muerta del combinador.

    Con todo el peso puesto en la credibilidad, el puntaje final pasa a ser lo
    que ese módulo aporta. Entra **invertido** —una cuenta más creíble aporta
    menos sospecha—, que es lo que hace que el día que el Módulo 2 mida de
    verdad alcance con cambiar el peso.
    """
    doble = ProveedorDoble(
        fuentes=[
            fuente("https://www.indec.gob.ar/informe", postura=Postura.CONTRADICE)
        ],
    )
    solo_la_cuenta = Configuracion(
        peso_clasificador=0.0, peso_credibilidad=1.0, peso_contraste=0.0
    )

    with construir_cliente(doble, configuracion=solo_la_cuenta) as cliente:
        cuerpo = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO).json()

    assert cuerpo["puntaje_final"] == pytest.approx(
        1.0 - cuerpo["puntajes"]["credibilidad"]["valor"]
    )


def test_el_nivel_severo_exige_una_fuente_oficial_que_contradiga() -> None:
    """RNF-07: el nivel severo le atribuye el juicio a quien lo sostiene.

    Las dos situaciones dan el mismo puntaje final, por encima del corte severo.
    Cambia de qué escalón viene la contradicción: con un medio de referencia el
    veredicto se rebaja a *información sospechosa*, porque decir *contradicho
    por fuentes oficiales* sin ninguna fuente oficial en contra sería atribuirle
    a un organismo un juicio que no emitió.
    """
    desde_un_medio = ProveedorDoble(
        fuentes=[fuente("https://www.clarin.com/nota", postura=Postura.CONTRADICE)],
        puntaje_clasificador=0.90,
    )
    desde_un_organismo = ProveedorDoble(
        fuentes=[
            fuente("https://www.indec.gob.ar/informe", postura=Postura.CONTRADICE)
        ],
        puntaje_clasificador=0.90,
    )

    with construir_cliente(desde_un_medio) as cliente:
        con_medio = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO).json()

    with construir_cliente(desde_un_organismo) as cliente:
        con_organismo = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO).json()

    assert con_medio["puntaje_final"] == pytest.approx(con_organismo["puntaje_final"])
    assert con_medio["veredicto"] == Veredicto.INFORMACION_SOSPECHOSA.value
    assert con_organismo["veredicto"] == (
        Veredicto.CONTRADICHO_POR_FUENTES_OFICIALES.value
    )


def test_la_cuenta_autora_no_llega_a_ningun_paso_del_analisis() -> None:
    """RNF-07: el resultado se enuncia sobre la afirmación y no sobre la persona.

    La forma en que este servicio lo sostiene no es pedírselo al modelo sino
    quitarle el dato: ningún paso del análisis recibe el identificador de la
    cuenta autora, así que el texto que justifica el resultado se escribe sin
    saber quién publicó. Lo que se comprueba desde afuera es exactamente eso.
    """
    doble = ProveedorDoble(
        fuentes=[
            fuente("https://www.indec.gob.ar/informe", postura=Postura.CONTRADICE)
        ],
    )
    pedido = PEDIDO_DE_EJEMPLO | {
        "handle": "@juana_perez_1985",
        "texto": "El índice de precios de julio fue del 15 por ciento.",
        "verificada": True,
    }

    with construir_cliente(doble) as cliente:
        cuerpo = cliente.post("/analizar", json=pedido).json()

    assert cuerpo["veredicto"] in NIVELES_DE_VEREDICTO
    for entrada in doble.entradas_recibidas:
        assert "juana" not in entrada.casefold()
        assert "perez" not in entrada.casefold()
        assert "@" not in entrada


def test_la_respuesta_incluye_las_versiones_de_trazabilidad(cliente) -> None:
    """RF-16: cada análisis viaja asociado al modelo y a la configuración."""
    cuerpo = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO).json()

    assert isinstance(cuerpo["version_modelo"], str)
    assert cuerpo["version_modelo"]
    assert isinstance(cuerpo["version_configuracion_pesos"], str)
    assert cuerpo["version_configuracion_pesos"]


def test_la_version_de_los_pesos_cambia_cuando_cambian_los_pesos() -> None:
    """RF-16 pide trazabilidad, y una versión que no se mueve no la da.

    Si dos análisis producidos con pesos distintos viajaran con la misma versión
    de configuración, reproducir un resultado meses después sería imposible y
    el campo sería decorativo. La misma configuración, en cambio, tiene que dar
    siempre la misma versión.
    """
    doble = ProveedorDoble()

    with construir_cliente(doble) as cliente:
        por_defecto = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO).json()

    with construir_cliente(doble, configuracion=Configuracion()) as cliente:
        misma_configuracion = cliente.post(
            "/analizar", json=PEDIDO_DE_EJEMPLO
        ).json()

    with construir_cliente(
        doble, configuracion=Configuracion(peso_contraste=0.9)
    ) as cliente:
        otros_pesos = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO).json()

    with construir_cliente(
        doble, configuracion=Configuracion(umbral_informacion_sospechosa=0.31)
    ) as cliente:
        otro_umbral = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO).json()

    version_por_defecto = por_defecto["version_configuracion_pesos"]
    assert misma_configuracion["version_configuracion_pesos"] == version_por_defecto
    assert otros_pesos["version_configuracion_pesos"] != version_por_defecto
    assert otro_umbral["version_configuracion_pesos"] != version_por_defecto
    assert (
        otros_pesos["version_configuracion_pesos"]
        != otro_umbral["version_configuracion_pesos"]
    )


def test_un_pedido_incompleto_se_rechaza(cliente) -> None:
    """El contrato de entrada también se hace valer."""
    respuesta = cliente.post("/analizar", json={"tweet_id": "1"})

    assert respuesta.status_code == 422


# ---------------------------------------------------------------------------
# Degradación a análisis parcial (RNF-11)
#
# El doble falla en una de las tres operaciones del puerto y se mira lo que sale
# por HTTP. Nada de acá sabe en qué orden se llaman esas operaciones, cuántos
# pasos internos hay ni cómo se llama el que quedó ausente: lo que se comprueba
# es que la respuesta llegue completa, marcada como parcial y con la lista de lo
# que faltó, en lugar de un error.
# ---------------------------------------------------------------------------

CAIDA = ErrorDelProveedor("El proveedor no respondió dentro del tiempo límite.")


def test_una_falla_del_proveedor_devuelve_un_analisis_parcial_y_no_un_error() -> None:
    """RNF-11: nunca un error opaco, siempre un análisis identificado como parcial.

    Es el criterio que hace resistente la demostración: si el proveedor se cae
    en vivo, lo que llega a la extensión es una respuesta que se puede dibujar
    entera y que dice qué le falta, no un código de error del cual la interfaz
    no puede sacar nada.
    """
    doble = ProveedorDoble(error_extraccion=CAIDA)

    with construir_cliente(doble) as cliente:
        respuesta = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO)

    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    # La respuesta sigue siendo la del contrato: la interfaz la dibuja igual.
    RespuestaAnalisis.model_validate(cuerpo)
    assert cuerpo["analisis_parcial"]["es_parcial"] is True
    assert cuerpo["analisis_parcial"]["modulos_ausentes"]
    assert cuerpo["justificacion"]


@pytest.mark.parametrize(
    "doble",
    [
        pytest.param(ProveedorDoble(error_extraccion=CAIDA), id="extracción"),
        pytest.param(ProveedorDoble(error_evidencia=CAIDA), id="evidencia"),
        pytest.param(ProveedorDoble(error_veredicto=CAIDA), id="veredicto"),
    ],
)
def test_falle_donde_falle_la_respuesta_llega_marcada_como_parcial(
    doble: ProveedorDoble,
) -> None:
    """Ninguna de las tres operaciones del puerto produce un error opaco.

    Las tres se recorren desde afuera, sin decir cuál corresponde a qué módulo:
    lo que el requerimiento exige es que ninguna falla se escape, no que se
    escape solo la primera.
    """
    with construir_cliente(doble) as cliente:
        respuesta = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO)

    assert respuesta.status_code == 200
    parcial = respuesta.json()["analisis_parcial"]
    assert parcial["es_parcial"] is True
    assert len(parcial["modulos_ausentes"]) >= 1
    # Los nombres son legibles para quien lee la interfaz, no identificadores
    # internos: nada de guiones bajos ni de nombres de función.
    for nombre in parcial["modulos_ausentes"]:
        assert "_" not in nombre
        assert " " in nombre


def test_un_analisis_parcial_no_trae_un_veredicto_construido_sobre_lo_que_falta() -> None:
    """RNF-11, segunda mitad: sin el contraste no hay veredicto de tres niveles.

    La búsqueda de evidencia no responde. El análisis sigue —el texto sí se
    analizó— pero el resultado no puede ser ninguno de los tres niveles de
    RF-06, porque los tres se apoyan en evidencia que nadie recuperó. El puntaje
    del clasificador barre la escala para que ningún valor pueda alcanzar un
    nivel por su cuenta.
    """
    for puntaje_del_texto in (0.02, 0.5, 0.99):
        doble = ProveedorDoble(
            error_evidencia=CAIDA, puntaje_clasificador=puntaje_del_texto
        )

        with construir_cliente(doble) as cliente:
            cuerpo = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO).json()

        assert cuerpo["analisis_parcial"]["es_parcial"] is True
        assert cuerpo["veredicto"] == Veredicto.SIN_CONTRASTE_EXTERNO.value
        assert cuerpo["veredicto"] not in NIVELES_DE_VEREDICTO
        assert cuerpo["fuentes"] == []


def test_cuando_falla_la_busqueda_el_analisis_del_texto_sobrevive() -> None:
    """La degradación conserva lo que sí se pudo hacer.

    Sin este caso, un servicio que devolviera una respuesta vacía ante cualquier
    falla pasaría igual el resto de la batería de degradación. Lo que distingue
    un análisis parcial de una respuesta vacía es que la parte que se ejecutó
    llega intacta: la afirmación extraída, su tipo y el puntaje del texto.
    """
    doble = ProveedorDoble(
        error_evidencia=CAIDA,
        afirmacion="El índice de precios de julio fue del 1,2 por ciento.",
        tipo=TipoAfirmacion.DATO_ECONOMICO,
        puntaje_clasificador=0.83,
        clase_clasificador="falso",
    )

    with construir_cliente(doble) as cliente:
        cuerpo = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO).json()

    assert cuerpo["afirmacion"] == "El índice de precios de julio fue del 1,2 por ciento."
    assert cuerpo["tipo_afirmacion"] == TipoAfirmacion.DATO_ECONOMICO.value
    assert cuerpo["puntajes"]["clasificador"] == {"valor": 0.83, "clase": "falso"}
    assert cuerpo["analisis_parcial"]["es_parcial"] is True


def test_cuando_solo_falla_la_redaccion_el_veredicto_y_las_fuentes_sobreviven() -> None:
    """Lo que decide el veredicto es código propio y no se cae con el proveedor.

    El nivel sale del combinador a partir de los puntajes y de la postura de las
    fuentes, así que una falla en el paso que redacta la explicación no puede
    tocarlo. Lo que se pierde es el texto, y la respuesta lo dice en lugar de
    disimularlo con una justificación inventada.
    """
    doble = ProveedorDoble(
        error_veredicto=CAIDA,
        fuentes=[
            fuente(
                "https://www.boletinoficial.gob.ar/detalle/1",
                postura=Postura.CONTRADICE,
            )
        ],
        puntaje_clasificador=0.90,
    )

    with construir_cliente(doble) as cliente:
        cuerpo = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO).json()

    assert cuerpo["analisis_parcial"]["es_parcial"] is True
    assert cuerpo["veredicto"] == Veredicto.CONTRADICHO_POR_FUENTES_OFICIALES.value
    assert [f["url"] for f in cuerpo["fuentes"]] == [
        "https://www.boletinoficial.gob.ar/detalle/1"
    ]
    assert cuerpo["justificacion"]
    assert cuerpo["razones"]


def test_un_analisis_completo_no_viaja_marcado_como_parcial(cliente) -> None:
    """La contracara: sin ninguna falla, la bandera de RNF-11 viene en falso.

    Una bandera que estuviera siempre encendida no avisaría nada. Es lo que hace
    que el aviso de la interfaz signifique algo cuando aparece.
    """
    cuerpo = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO).json()

    assert cuerpo["analisis_parcial"] == {"es_parcial": False, "modulos_ausentes": []}


# ---------------------------------------------------------------------------
# Reutilización de análisis previos (RF-07)
#
# La caché no se prueba por separado y ningún test de acá la importa: se la
# ejercita por el mismo `POST /analizar` que todo lo demás, contando las veces
# que el doble fue invocado. Es lo que permite reemplazarla mañana por la
# persistencia de RF-16 sin tocar una línea de este archivo.
# ---------------------------------------------------------------------------


def test_un_tuit_ya_analizado_no_vuelve_a_invocar_al_proveedor() -> None:
    """RF-07: el mismo tuit pedido dos veces se resuelve sin volver a analizarlo.

    Es lo que le ahorra al ciudadano esperar de nuevo por algo que el sistema ya
    sabe, y lo que le ahorra al proyecto pagar dos veces la misma llamada.
    """
    doble = ProveedorDoble(
        fuentes=[
            fuente("https://www.indec.gob.ar/informe", postura=Postura.CONTRADICE)
        ],
    )

    with construir_cliente(doble) as cliente:
        primera = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO).json()
        invocaciones_tras_la_primera = len(doble.entradas_recibidas)
        segunda = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO).json()

    assert len(doble.entradas_recibidas) == invocaciones_tras_la_primera
    assert segunda == primera


def test_dos_tuits_distintos_se_analizan_cada_uno_por_su_cuenta() -> None:
    """La caché reutiliza el análisis del mismo tuit, no el del anterior.

    Sin este caso, un servicio que devolviera siempre el primer análisis que
    calculó pasaría el test de RF-07 sin cumplirlo.
    """
    doble = ProveedorDoble()

    with construir_cliente(doble) as cliente:
        primero = cliente.post(
            "/analizar",
            json=PEDIDO_DE_EJEMPLO | {"texto": "El dólar cerró a mil pesos."},
        ).json()
        segundo = cliente.post(
            "/analizar",
            json=PEDIDO_DE_EJEMPLO
            | {
                "tweet_id": "9876543210987654321",
                "texto": "Cierran cincuenta escuelas el lunes.",
            },
        ).json()

    assert len(doble.textos_recibidos) == 2
    assert primero["afirmacion"] != segundo["afirmacion"]


def test_un_analisis_parcial_no_se_reutiliza() -> None:
    """Una falla transitoria no puede volverse permanente hasta reiniciar.

    Es la decisión de fondo de la caché. El primer pedido encuentra al proveedor
    caído y devuelve un análisis parcial; el segundo, con el proveedor ya sano,
    tiene que volver a intentarlo y devolver el análisis completo. Si el parcial
    se guardara, reintentar no significaría nada: el ciudadano vería el mismo
    resultado degradado hasta que alguien reiniciara el servicio, que en una
    exposición en vivo es el peor modo de falla posible.
    """
    doble = ProveedorDoble(error_extraccion=CAIDA)

    with construir_cliente(doble) as cliente:
        primera = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO).json()
        assert primera["analisis_parcial"]["es_parcial"] is True

        # El proveedor se recupera entre un pedido y el otro.
        doble.error_extraccion = None
        segunda = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO).json()

    assert segunda["analisis_parcial"]["es_parcial"] is False
    assert segunda["afirmacion"]


def test_cambiar_los_pesos_invalida_lo_que_la_cache_tenia_guardado() -> None:
    """RF-16 y RNF-16 juntos: la caché no puede devolver análisis de otra versión.

    Un análisis guardado se produjo con un juego de pesos concreto y viaja
    asociado a él. Si la configuración cambia, ese análisis ya no responde a lo
    que el servicio está haciendo, y devolverlo haría que mover un peso en vivo
    —la demostración de RNF-16— pareciera no tener efecto.
    """
    doble = ProveedorDoble(
        fuentes=[
            fuente("https://www.indec.gob.ar/informe", postura=Postura.CONTRADICE)
        ],
        puntaje_clasificador=0.20,
    )
    otros_pesos = Configuracion(peso_clasificador=1.0, peso_contraste=0.0)
    # La misma caché para los dos clientes: es la del proceso que alguien
    # reinició con otro peso, que es el escenario que la demostración usa.
    memoria = CacheDeAnalisis()

    with construir_cliente(doble, cache=memoria) as cliente:
        con_pesos_por_defecto = cliente.post(
            "/analizar", json=PEDIDO_DE_EJEMPLO
        ).json()

    with construir_cliente(
        doble, configuracion=otros_pesos, cache=memoria
    ) as cliente:
        con_otros_pesos = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO).json()

    assert (
        con_otros_pesos["version_configuracion_pesos"]
        != con_pesos_por_defecto["version_configuracion_pesos"]
    )
    assert con_otros_pesos["puntaje_final"] != con_pesos_por_defecto["puntaje_final"]


def test_agotar_el_presupuesto_de_tiempo_degrada_a_parcial() -> None:
    """RNF-11: pasarse del presupuesto declara módulos ausentes, no cuelga.

    Con el presupuesto en cero, todo paso posterior a la extracción encuentra el
    tiempo ya consumido y se declara ausente. El cero está puesto para no hacer
    depender la prueba de un reloj; lo que se comprueba no es el número sino que
    agotar el presupuesto produzca la misma respuesta declarada que ya produce
    un proveedor que no contesta, en lugar de seguir corriendo mientras el
    ciudadano mira girar un indicador.
    """
    sin_presupuesto = Configuracion(tiempo_limite_total_s=0.0)
    doble = ProveedorDoble(
        fuentes=[fuente("https://www.boletinoficial.gob.ar/una", postura=Postura.CONTRADICE)]
    )

    with construir_cliente(doble, configuracion=sin_presupuesto) as cliente:
        cuerpo = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO).json()

    parcial = cuerpo["analisis_parcial"]
    assert parcial["es_parcial"] is True
    assert len(parcial["modulos_ausentes"]) == 2
    for nombre in parcial["modulos_ausentes"]:
        assert "_" not in nombre and " " in nombre

    # La evidencia no llegó a recuperarse, así que la invariante de RNF-06 tiene
    # que seguir valiendo: sin fuentes no se emite ninguno de los tres niveles.
    assert cuerpo["fuentes"] == []
    assert cuerpo["veredicto"] == Veredicto.SIN_CONTRASTE_EXTERNO.value
