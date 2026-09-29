"""CU-06 por el contrato HTTP: alta de una organización cliente, emisión y
revocación de claves, y la interfaz de clasificación autenticada con cuota
mensual (RF-13), sin la cuenta autora en claro en la respuesta (RF-15).

El último test recorre el caso de prueba 6 de la Sección 4.3 del documento tal
como está escrito.
"""

from __future__ import annotations

from app.configuracion import Configuracion
from app.historial import Historial

from .conftest import ProveedorDoble, construir_cliente

SECRETO = "secreto-de-prueba"
ADMIN = {"X-Secreto-Administrador": SECRETO}
TEXTO = {
    "texto": "El INDEC informó una inflación mensual del 2,1 % en agosto.",
    "handle": "@cuenta_autora_en_claro",
}


def _cliente(historial: Historial | None = None):
    return construir_cliente(
        ProveedorDoble(),
        configuracion=Configuracion(secreto_administrador=SECRETO),
        historial=historial,
    )


def _alta(cliente, cuota: int = 100) -> int:
    respuesta = cliente.post(
        "/organizaciones", json={"nombre": "Redacción Ejemplo", "cuota_mensual": cuota},
        headers=ADMIN,
    )
    assert respuesta.status_code == 201
    return respuesta.json()["id_organizacion"]


def _emitir(cliente, id_organizacion: int) -> dict:
    respuesta = cliente.post(f"/organizaciones/{id_organizacion}/claves", headers=ADMIN)
    assert respuesta.status_code == 201
    return respuesta.json()


def _con(clave: str) -> dict:
    return {"Authorization": f"Bearer {clave}"}


def test_el_alta_y_la_emision_exigen_el_secreto_administrativo() -> None:
    with _cliente() as cliente:
        sin = cliente.post("/organizaciones", json={"nombre": "X", "cuota_mensual": 1})
        mal = cliente.post(
            "/organizaciones", json={"nombre": "X", "cuota_mensual": 1},
            headers={"X-Secreto-Administrador": "otro"},
        )
        assert sin.status_code == 401
        assert mal.status_code == 401
        assert cliente.post("/organizaciones/1/claves").status_code == 401


def test_sin_secreto_configurado_el_alta_queda_deshabilitada() -> None:
    with construir_cliente(ProveedorDoble(), configuracion=Configuracion(secreto_administrador="")) as cliente:
        respuesta = cliente.post(
            "/organizaciones", json={"nombre": "X", "cuota_mensual": 1},
            headers={"X-Secreto-Administrador": ""},
        )
        assert respuesta.status_code == 401


def test_la_clave_se_muestra_una_vez_y_se_guarda_resumida() -> None:
    historial = Historial(":memory:")
    with _cliente(historial) as cliente:
        emitida = _emitir(cliente, _alta(cliente))

    assert emitida["clave"].startswith(emitida["prefijo"])
    volcado = "\n".join(historial._conexion.iterdump())
    assert emitida["clave"] not in volcado
    assert emitida["prefijo"] in volcado


def test_emitir_para_una_organizacion_inexistente_es_404() -> None:
    with _cliente() as cliente:
        assert cliente.post("/organizaciones/999/claves", headers=ADMIN).status_code == 404


def test_la_clasificacion_con_clave_valida_devuelve_el_analisis_completo() -> None:
    with _cliente() as cliente:
        clave = _emitir(cliente, _alta(cliente))["clave"]
        respuesta = cliente.post("/api/v1/clasificar", json=TEXTO, headers=_con(clave))

    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    for campo in ("puntaje_final", "veredicto", "justificacion", "fuentes"):
        assert campo in cuerpo


def test_la_respuesta_no_trae_la_cuenta_autora_en_claro() -> None:
    """RF-15 y RNF-10."""
    with _cliente() as cliente:
        clave = _emitir(cliente, _alta(cliente))["clave"]
        respuesta = cliente.post("/api/v1/clasificar", json=TEXTO, headers=_con(clave))

    assert "cuenta_autora_en_claro" not in respuesta.text


def test_sin_clave_o_con_clave_invalida_se_rechaza() -> None:
    with _cliente() as cliente:
        _emitir(cliente, _alta(cliente))
        sin = cliente.post("/api/v1/clasificar", json=TEXTO)
        invalida = cliente.post("/api/v1/clasificar", json=TEXTO, headers=_con("pfi_inventada"))

    assert sin.status_code == 401
    assert invalida.status_code == 401


def test_una_clave_revocada_se_rechaza_y_las_demas_siguen_activas() -> None:
    with _cliente() as cliente:
        id_organizacion = _alta(cliente)
        revocada = _emitir(cliente, id_organizacion)
        activa = _emitir(cliente, id_organizacion)
        baja = cliente.delete(
            f"/organizaciones/{id_organizacion}/claves/{revocada['prefijo']}", headers=ADMIN
        )
        assert baja.status_code == 204

        rechazada = cliente.post("/api/v1/clasificar", json=TEXTO, headers=_con(revocada["clave"]))
        aceptada = cliente.post("/api/v1/clasificar", json=TEXTO, headers=_con(activa["clave"]))

    assert rechazada.status_code == 401
    assert aceptada.status_code == 200


def test_revocar_una_clave_inexistente_es_404() -> None:
    with _cliente() as cliente:
        id_organizacion = _alta(cliente)
        assert cliente.delete(
            f"/organizaciones/{id_organizacion}/claves/pfi_noexiste", headers=ADMIN
        ).status_code == 404


def test_cada_clasificacion_se_registra_contra_la_cuota() -> None:
    with _cliente() as cliente:
        clave = _emitir(cliente, _alta(cliente, cuota=10))["clave"]
        cliente.post("/api/v1/clasificar", json=TEXTO, headers=_con(clave))
        cliente.post("/api/v1/clasificar", json=TEXTO, headers=_con(clave))
        consumo = cliente.get("/api/v1/consumo", headers=_con(clave))

    assert consumo.status_code == 200
    assert consumo.json()["consumo_del_mes"] == 2
    assert consumo.json()["cuota_mensual"] == 10


def test_con_la_cuota_agotada_se_rechaza_informando_el_limite_y_la_renovacion() -> None:
    with _cliente() as cliente:
        clave = _emitir(cliente, _alta(cliente, cuota=1))["clave"]
        primera = cliente.post("/api/v1/clasificar", json=TEXTO, headers=_con(clave))
        segunda = cliente.post("/api/v1/clasificar", json=TEXTO, headers=_con(clave))
        consumo = cliente.get("/api/v1/consumo", headers=_con(clave)).json()

    assert primera.status_code == 200
    assert segunda.status_code == 429
    detalle = segunda.json()["detail"]
    assert detalle["cuota_mensual"] == 1
    assert detalle["renovacion"] == consumo["renovacion"]
    # El rechazo no consume cuota.
    assert consumo["consumo_del_mes"] == 1


def test_caso_de_prueba_6() -> None:
    """Sección 4.3: clave activa, clave revocada y cuota disponible."""
    with _cliente() as cliente:
        id_organizacion = _alta(cliente)
        activa = _emitir(cliente, id_organizacion)["clave"]
        revocada = _emitir(cliente, id_organizacion)
        cliente.delete(f"/organizaciones/{id_organizacion}/claves/{revocada['prefijo']}", headers=ADMIN)

        # 1. Enviar el texto con la clave activa.
        primera = cliente.post("/api/v1/clasificar", json=TEXTO, headers=_con(activa))
        # 2. Revisar la respuesta recibida.
        assert primera.status_code == 200
        assert {"puntaje_final", "veredicto", "justificacion", "fuentes"} <= primera.json().keys()
        assert "cuenta_autora_en_claro" not in primera.text
        # 3. Consultar el consumo registrado de la organización.
        assert cliente.get("/api/v1/consumo", headers=_con(activa)).json()["consumo_del_mes"] == 1
        # 4. Enviar el mismo texto con la clave revocada.
        assert cliente.post(
            "/api/v1/clasificar", json=TEXTO, headers=_con(revocada["clave"])
        ).status_code == 401
