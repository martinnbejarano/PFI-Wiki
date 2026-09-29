"""CU-04 y CU-05 por el contrato HTTP: informe de un veredicto incorrecto
(`POST /reportes`, RF-11) e histórico personal en el panel web (`GET /panel`,
RF-10), con la finalidad y la vía de supresión a la vista (RF-12).

Igual que el resto de la batería, nada acá conoce la base de datos: el análisis
entra por `POST /analizar` con el identificador de la instalación y se mira lo
que sale por HTTP.
"""

from __future__ import annotations

from app.configuracion import Configuracion

from .conftest import PEDIDO_DE_EJEMPLO, ProveedorDoble, construir_cliente

INSTALACION = "0b7c3f7e-2a44-4d7e-9a57-6a3f4f1d2c10"
OTRA_INSTALACION = "5f1e9f0a-8c1b-4c55-b0a8-3a9d7e6b2f41"


def _analizar(cliente, tweet_id: str, texto: str, instalacion: str = INSTALACION):
    respuesta = cliente.post(
        "/analizar",
        json={**PEDIDO_DE_EJEMPLO, "tweet_id": tweet_id, "texto": texto,
              "id_instalacion": instalacion},
    )
    assert respuesta.status_code == 200
    return respuesta.json()


def test_el_panel_lista_los_analisis_de_la_instalacion_del_mas_reciente_al_mas_viejo(
    cliente,
) -> None:
    _analizar(cliente, "111", "Primera afirmación analizada.")
    _analizar(cliente, "222", "Segunda afirmación analizada.")

    html = cliente.get("/panel", params={"instalacion": INSTALACION}).text

    primera = html.index("Primera afirmación analizada.")
    segunda = html.index("Segunda afirmación analizada.")
    assert segunda < primera
    # Cada análisis se lista con su veredicto.
    assert html.count("Sin contraste externo") >= 2


def test_el_panel_no_muestra_los_analisis_de_otra_instalacion(cliente) -> None:
    _analizar(cliente, "111", "Afirmación de otra instalación.", OTRA_INSTALACION)

    html = cliente.get("/panel", params={"instalacion": INSTALACION}).text

    assert "Afirmación de otra instalación." not in html
    assert "Todavía no hay análisis" in html


def test_un_analisis_sin_identificador_de_instalacion_no_entra_en_ningun_historico(
    cliente,
) -> None:
    respuesta = cliente.post("/analizar", json=PEDIDO_DE_EJEMPLO)
    assert respuesta.status_code == 200

    html = cliente.get("/panel", params={"instalacion": INSTALACION}).text
    assert "Todavía no hay análisis" in html


def test_el_panel_sin_instalacion_ofrece_solo_la_informacion_institucional(
    cliente,
) -> None:
    _analizar(cliente, "111", "Algo analizado.")

    respuesta = cliente.get("/panel")

    assert respuesta.status_code == 200
    assert "Algo analizado." not in respuesta.text
    assert "desde la extensión" in respuesta.text


def test_el_panel_muestra_la_finalidad_y_la_via_de_supresion(cliente) -> None:
    """RF-12: los dos textos van en toda vista del panel."""
    for params in ({}, {"instalacion": INSTALACION}):
        html = cliente.get("/panel", params=params).text
        assert "Finalidad" in html
        assert "artículo 16 de la Ley 25.326" in html
        assert "cinco días hábiles" in html


def test_el_detalle_de_un_analisis_del_historico_muestra_su_evidencia() -> None:
    from app.contrato import Fuente, Postura, TipoFuente

    fuente = Fuente(
        titulo="Resolución del ministerio",
        url="https://www.boletinoficial.gob.ar/detalleAviso/primera/1",
        tipo=TipoFuente.FUENTE_OFICIAL,
        postura=Postura.CONTRADICE,
    )
    with construir_cliente(ProveedorDoble(fuentes=[fuente])) as cliente:
        analisis = _analizar(cliente, "111", "Cierran todas las escuelas.")

        html = cliente.get(
            "/panel", params={"instalacion": INSTALACION, "tuit": "111"}
        ).text

    assert analisis["afirmacion"] in html
    assert analisis["justificacion"] in html
    assert "Resolución del ministerio" in html
    assert 'href="https://www.boletinoficial.gob.ar/detalleAviso/primera/1"' in html


def test_el_panel_escapa_lo_que_viene_del_tuit(cliente) -> None:
    _analizar(cliente, "111", "<script>alert(1)</script>")

    html = cliente.get("/panel", params={"instalacion": INSTALACION}).text

    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;" in html


def test_un_informe_queda_registrado_con_el_analisis_la_instalacion_y_la_version() -> None:
    configuracion = Configuracion()
    with construir_cliente(ProveedorDoble(), configuracion=configuracion) as cliente:
        _analizar(cliente, "111", "Cierran todas las escuelas.")

        respuesta = cliente.post(
            "/reportes",
            json={
                "id_instalacion": INSTALACION,
                "tweet_id": "111",
                "tipo": "falso_positivo",
                "motivo": "El ministerio lo confirmó ayer.",
            },
        )

        assert respuesta.status_code == 201
        reporte = respuesta.json()
        assert reporte["tweet_id"] == "111"
        assert reporte["id_instalacion"] == INSTALACION
        assert reporte["tipo"] == "falso_positivo"
        assert reporte["motivo"] == "El ministerio lo confirmó ayer."
        assert reporte["version_modelo"] == configuracion.version_modelo

        # Y queda a la vista en el detalle del histórico.
        html = cliente.get(
            "/panel", params={"instalacion": INSTALACION, "tuit": "111"}
        ).text
        assert "falso positivo" in html
        assert "El ministerio lo confirmó ayer." in html


def test_un_informe_repetido_no_duplica_el_registro(cliente) -> None:
    _analizar(cliente, "111", "Cierran todas las escuelas.")
    cuerpo = {"id_instalacion": INSTALACION, "tweet_id": "111", "tipo": "falso_negativo"}

    primero = cliente.post("/reportes", json=cuerpo).json()
    segundo = cliente.post("/reportes", json={**cuerpo, "tipo": "falso_positivo"}).json()

    assert segundo["id_reporte"] == primero["id_reporte"]
    assert segundo["tipo"] == "falso_negativo"


def test_no_se_puede_informar_un_analisis_que_la_instalacion_no_pidio(cliente) -> None:
    _analizar(cliente, "111", "Cierran todas las escuelas.", OTRA_INSTALACION)

    respuesta = cliente.post(
        "/reportes",
        json={"id_instalacion": INSTALACION, "tweet_id": "111", "tipo": "falso_positivo"},
    )

    assert respuesta.status_code == 404


def test_un_informe_exige_un_tipo_de_error_valido(cliente) -> None:
    _analizar(cliente, "111", "Cierran todas las escuelas.")

    respuesta = cliente.post(
        "/reportes",
        json={"id_instalacion": INSTALACION, "tweet_id": "111", "tipo": "me_parece_mal"},
    )

    assert respuesta.status_code == 422
