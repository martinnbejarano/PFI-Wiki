"""CU-07 por el contrato HTTP: el panel de tendencias de una organización
cliente (RF-14), con acceso autenticado por la clave de la organización
(RF-13) y sin la cuenta autora en claro en ninguna entrega (RF-15, RNF-10).

El último test recorre el caso de prueba 7 de la Sección 4.3 del documento.
"""

from __future__ import annotations

from datetime import datetime, timezone

from app.configuracion import Configuracion
from app.contrato import Fuente, Postura, TipoFuente
from app.historial import Historial

from .conftest import ProveedorDoble, construir_cliente

SECRETO = "secreto-de-prueba"
ADMIN = {"X-Secreto-Administrador": SECRETO}
ESCUELAS = "A partir del lunes cierran todas las escuelas de la Provincia."
INFLACION = "El INDEC informó una inflación mensual del 9 % en agosto."
HOY = datetime.now(timezone.utc).date().isoformat()


def _cliente(historial: Historial, proveedor: ProveedorDoble | None = None):
    return construir_cliente(
        proveedor or ProveedorDoble(),
        configuracion=Configuracion(secreto_administrador=SECRETO),
        historial=historial,
    )


def _clave(cliente) -> dict:
    id_organizacion = cliente.post(
        "/organizaciones", json={"nombre": "Redacción Ejemplo", "cuota_mensual": 100},
        headers=ADMIN,
    ).json()["id_organizacion"]
    clave = cliente.post(f"/organizaciones/{id_organizacion}/claves", headers=ADMIN).json()
    return {"Authorization": f"Bearer {clave['clave']}"}


def _analizar(cliente, tweet_id: str, texto: str, handle: str, instalacion: int = 1) -> None:
    respuesta = cliente.post("/analizar", json={
        "tweet_id": tweet_id, "texto": texto, "handle": handle,
        "id_instalacion": f"00000000-0000-4000-8000-{instalacion:012d}",
    })
    assert respuesta.status_code == 200


def _acumular(cliente) -> None:
    """Dos publicaciones del mismo tema de @autora_uno y una de @autora_dos."""
    _analizar(cliente, "101", ESCUELAS, "@autora_uno")
    _analizar(cliente, "102", ESCUELAS, "@autora_uno", instalacion=2)
    _analizar(cliente, "103", INFLACION, "@autora_dos")


def test_sin_clave_el_panel_y_la_exportacion_se_rechazan() -> None:
    with _cliente(Historial(":memory:")) as cliente:
        _clave(cliente)
        for ruta in ("/panel/tendencias", "/panel/tendencias.csv"):
            assert cliente.get(ruta).status_code == 401
            assert cliente.get(ruta, headers={"Authorization": "Bearer pfi_x"}).status_code == 401


def test_el_panel_presenta_temas_evolucion_y_cuentas_bajo_seudonimo() -> None:
    with _cliente(Historial(":memory:")) as cliente:
        clave = _clave(cliente)
        _acumular(cliente)
        respuesta = cliente.get("/panel/tendencias", headers=clave)

    assert respuesta.status_code == 200
    html = respuesta.text
    assert "Temas de mayor circulación" in html
    assert "cierran todas las escuelas" in html
    assert HOY in html
    assert "cuenta-1" in html and "cuenta-2" in html
    assert "autora_uno" not in html and "autora_dos" not in html


def test_el_recorte_exportado_es_agregado_y_sin_cuenta_en_claro() -> None:
    historial = Historial(":memory:")
    contradice = ProveedorDoble(fuentes=[Fuente(
        titulo="Resolución", url="https://www.boletinoficial.gob.ar/detalle/1",
        tipo=TipoFuente.FUENTE_OFICIAL, postura=Postura.CONTRADICE,
    )], puntaje_clasificador=0.9)
    with _cliente(historial) as cliente:
        clave = _clave(cliente)
        _acumular(cliente)
    with _cliente(historial, contradice) as cliente:
        _analizar(cliente, "104", INFLACION, "@autora_dos")
        respuesta = cliente.get("/panel/tendencias.csv", headers=clave)

    assert respuesta.status_code == 200
    assert respuesta.headers["content-type"].startswith("text/csv")
    filas = [linea.split(",") for linea in respuesta.text.strip().splitlines()]
    assert filas[0] == ["seccion", "clave", "publicaciones", "marcadas"]
    assert ["dia", HOY, "4", "1"] in filas
    assert ["cuenta", "cuenta-2", "2", "1"] in filas
    assert ["cuenta", "cuenta-1", "2", "0"] in filas
    assert "autora" not in respuesta.text


def test_una_publicacion_pedida_por_varias_instalaciones_cuenta_una_vez() -> None:
    with _cliente(Historial(":memory:")) as cliente:
        clave = _clave(cliente)
        _analizar(cliente, "101", ESCUELAS, "@autora_uno", instalacion=1)
        _analizar(cliente, "101", ESCUELAS, "@autora_uno", instalacion=2)
        csv = cliente.get("/panel/tendencias.csv", headers=clave).text

    assert f"dia,{HOY},1,0" in csv


def test_el_periodo_acota_lo_que_se_agrega() -> None:
    historial = Historial(":memory:")
    with _cliente(historial) as cliente:
        clave = _clave(cliente)
        _acumular(cliente)
        with historial._conexion:
            historial._conexion.execute(
                "UPDATE analisis SET fecha_analisis = '2026-01-15T12:00:00+00:00' "
                "WHERE tweet_id = '103'"
            )
        enero = cliente.get(
            "/panel/tendencias.csv?desde=2026-01-01&hasta=2026-01-31", headers=clave
        ).text

    assert "dia,2026-01-15,1,0" in enero
    assert "cuenta-2" in enero and "cuenta-1" not in enero


def test_caso_de_prueba_7() -> None:
    """Sección 4.3: analista de una organización con suscripción vigente y
    análisis acumulados en el período."""
    with _cliente(Historial(":memory:")) as cliente:
        # 1. Autenticarse (con la clave de la organización).
        clave = _clave(cliente)
        _acumular(cliente)
        # 2. Seleccionar el período.
        periodo = f"?desde={HOY}&hasta={HOY}"
        # 3. Revisar los temas, su evolución temporal y las cuentas de mayor volumen.
        panel = cliente.get("/panel/tendencias" + periodo, headers=clave)
        assert panel.status_code == 200
        assert "cierran todas las escuelas" in panel.text and HOY in panel.text
        assert "cuenta-1" in panel.text
        # 4. Exportar el recorte.
        recorte = cliente.get("/panel/tendencias.csv" + periodo, headers=clave)
        assert recorte.status_code == 200

    for entrega in (panel.text, recorte.text):
        assert "@autora" not in entrega and "autora_uno" not in entrega
