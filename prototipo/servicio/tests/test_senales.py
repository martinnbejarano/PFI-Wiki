"""El flujo automático (RF-02, CU-01) por `POST /senales`.

El clasificador se sustituye por un doble a través de `obtener_clasificador`,
por el mismo mecanismo que el proveedor en el resto de la batería.
"""

from __future__ import annotations

from app.configuracion import Configuracion
from app.dependencias import obtener_clasificador
from app.main import aplicacion
from app.proveedor.clasificador import Clasificacion
from app.proveedor.puerto import ErrorDelProveedor

from .conftest import ProveedorDoble, construir_cliente


class ClasificadorPorTexto:
    """Puntúa «falso» lo que diga «falso», falla con lo que diga «falla»."""

    def __init__(self) -> None:
        self.textos_recibidos: list[str] = []

    def clasificar(self, texto: str) -> Clasificacion:
        self.textos_recibidos.append(texto)
        if "falla" in texto:
            raise ErrorDelProveedor("clasificador | tiempo límite")
        puntaje = 0.9 if "falso" in texto else 0.1
        return Clasificacion(
            puntaje=puntaje,
            clase="falso" if puntaje >= 0.5 else "verdadero",
            version_modelo="beto-doble",
        )


def pedir(publicaciones: list[dict], clasificador: ClasificadorPorTexto, llm: ProveedorDoble):
    aplicacion.dependency_overrides[obtener_clasificador] = lambda: clasificador
    try:
        with construir_cliente(llm) as cliente:
            return cliente.post("/senales", json={"publicaciones": publicaciones})
    finally:
        aplicacion.dependency_overrides.pop(obtener_clasificador, None)


def test_la_senal_es_de_prioridad_y_nunca_un_veredicto_ni_un_puntaje() -> None:
    clasificador, llm = ClasificadorPorTexto(), ProveedorDoble()
    respuesta = pedir(
        [
            {"tweet_id": "1", "texto": "un texto falso"},
            {"tweet_id": "2", "texto": "un texto cualquiera"},
            {"tweet_id": "3", "texto": "este falla"},
        ],
        clasificador,
        llm,
    )

    assert respuesta.status_code == 200
    # La publicación cuyo puntaje falló no aparece: falla en silencio.
    assert respuesta.json() == {
        "senales": [
            {"tweet_id": "1", "prioridad": "revisar", "version_modelo": "beto-doble"},
            {"tweet_id": "2", "prioridad": "neutral", "version_modelo": "beto-doble"},
        ]
    }
    # Solo el Módulo 1: el LLM no se toca, así que no cuesta ni consume tope.
    assert llm.entradas_recibidas == []
    assert sorted(clasificador.textos_recibidos) == [
        "este falla", "un texto cualquiera", "un texto falso",
    ]


def test_el_pedido_no_admite_la_cuenta_autora_ni_lotes_desmedidos() -> None:
    clasificador, llm = ClasificadorPorTexto(), ProveedorDoble()
    # Un campo de más se ignora: la cuenta autora no llega al clasificador.
    pedir([{"tweet_id": "1", "texto": "hola", "handle": "@alguien"}], clasificador, llm)
    assert clasificador.textos_recibidos == ["hola"]

    lote = [{"tweet_id": str(i), "texto": "hola"} for i in range(21)]
    assert pedir(lote, clasificador, llm).status_code == 422
    assert pedir([], clasificador, llm).status_code == 422


def test_sin_clasificador_configurado_el_lote_sale_vacio() -> None:
    # Sin `URL_CLASIFICADOR` el cliente real falla en cada texto: 200 y nada.
    with construir_cliente(ProveedorDoble(), configuracion=Configuracion(url_clasificador="")) as cliente:
        respuesta = cliente.post("/senales", json={"publicaciones": [{"tweet_id": "1", "texto": "hola"}]})
    assert respuesta.status_code == 200
    assert respuesta.json() == {"senales": []}
