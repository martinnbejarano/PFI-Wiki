"""CU-04 y CU-05 por el contrato HTTP: informe de un veredicto incorrecto
(`POST /reportes`, RF-11) e histórico personal en el panel web (`GET /panel`,
RF-10), con la finalidad y la vía de supresión a la vista (RF-12).

Igual que el resto de la batería, nada acá conoce la base de datos: el análisis
entra por `POST /analizar` con el identificador de la instalación y se mira lo
que sale por HTTP.
"""

from __future__ import annotations

import hashlib
import hmac
import sqlite3

from app.configuracion import Configuracion
from app.historial import Historial

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
        assert '<a href="mailto:jbejaranoarce@uade.edu.ar">jbejaranoarce@uade.edu.ar</a>' in html
        assert "pendiente de definir" not in html


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


def test_el_panel_restringe_lo_que_la_pagina_puede_cargar_y_no_filtra_la_url(cliente) -> None:
    """Sin scripts ni recursos externos, y sin referente: el identificador de
    la instalación viaja en la URL."""
    html = cliente.get("/panel", params={"instalacion": INSTALACION}).text

    assert "Content-Security-Policy" in html and "default-src 'none'" in html
    assert '<meta name="referrer" content="no-referrer">' in html


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


# --- Cuenta autora seudonimizada (Ley 25.326, art. 7) ----------------------


def test_la_cuenta_se_guarda_seudonimizada_y_nunca_en_claro() -> None:
    historial = Historial(":memory:", "secreto-de-prueba")
    with construir_cliente(ProveedorDoble(), historial=historial) as cliente:
        for handle, tweet_id in (("@Juana_Perez", "1"), ("juana_perez", "2")):
            cliente.post("/analizar", json={**PEDIDO_DE_EJEMPLO, "tweet_id": tweet_id,
                                            "handle": handle, "id_instalacion": INSTALACION})

    volcado = "\n".join(historial._conexion.iterdump()).lower()
    assert "juana" not in volcado
    esperado = hmac.new(b"secreto-de-prueba", b"juana_perez", hashlib.sha256).hexdigest()
    cuentas = historial._conexion.execute("SELECT seudonimo FROM cuenta").fetchall()
    assert [c[0] for c in cuentas] == [esperado]
    assert historial._conexion.execute("SELECT COUNT(*) FROM tuit").fetchone()[0] == 2


def test_la_migracion_reemplaza_los_handles_en_claro_y_es_idempotente(tmp_path) -> None:
    """Las bases desplegadas antes guardaban `cuenta.handle` en claro."""
    ruta = str(tmp_path / "vieja.sqlite3")
    vieja = sqlite3.connect(ruta)
    vieja.executescript(
        "CREATE TABLE cuenta (id_cuenta INTEGER PRIMARY KEY, handle TEXT NOT NULL UNIQUE);"
        "CREATE TABLE tuit (id_nativo TEXT PRIMARY KEY, id_cuenta INTEGER NOT NULL);"
        "INSERT INTO cuenta VALUES (1, '@Ana'), (2, 'ana'), (3, '@beto');"
        "INSERT INTO tuit VALUES ('10', 1), ('20', 2), ('30', 3);"
    )
    vieja.close()

    primera = Historial(ruta, "s")
    seudonimos = {f[0] for f in primera._conexion.execute("SELECT seudonimo FROM cuenta")}
    assert seudonimos == {primera.seudonimo("ana"), primera.seudonimo("beto")}
    tuits = dict(primera._conexion.execute("SELECT id_nativo, id_cuenta FROM tuit").fetchall())
    assert tuits["10"] == tuits["20"] != tuits["30"]
    primera._conexion.close()

    segunda = Historial(ruta, "s")
    assert segunda._conexion.execute("SELECT COUNT(*) FROM cuenta").fetchone()[0] == 2
    volcado = "\n".join(segunda._conexion.iterdump()).lower()
    assert "'@ana'" not in volcado and "'ana'" not in volcado and "beto" not in volcado


# -- RF-17: tope de la versión gratuita ------------------------------------


def test_el_sexto_analisis_nuevo_del_mes_se_rechaza_con_la_fecha_de_renovacion(cliente) -> None:
    for i in range(5):
        _analizar(cliente, f"cupo-{i}", f"Afirmación número {i}.")

    respuesta = cliente.post(
        "/analizar",
        json={**PEDIDO_DE_EJEMPLO, "tweet_id": "cupo-5", "texto": "La sexta.",
              "id_instalacion": INSTALACION},
    )

    assert respuesta.status_code == 429
    detalle = respuesta.json()["detail"]
    assert detalle["usados_del_mes"] == 5
    dia = detalle["renovacion"]
    assert f"{dia[8:10]}/{dia[5:7]}/{dia[:4]}" in detalle["mensaje"]


def test_lo_resuelto_desde_la_cache_no_consume_el_cupo_ni_se_corta(cliente) -> None:
    for i in range(5):
        _analizar(cliente, f"cupo-{i}", f"Afirmación número {i}.")

    # Ya analizado: se sirve desde la caché aunque el cupo esté agotado.
    _analizar(cliente, "cupo-0", "Afirmación número 0.")
    # Otra instalación tiene su propio cupo.
    _analizar(cliente, "cupo-9", "Otra afirmación.", OTRA_INSTALACION)
