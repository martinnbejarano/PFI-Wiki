"""Doble del proveedor y cliente de pruebas del servicio.

La batería entera se apoya en una sola costura: `POST /analizar`, ejercitado con
el cliente de pruebas de FastAPI y con el puerto del proveedor reemplazado por
un doble a través de `aplicacion.dependency_overrides`. Es el único punto de
inyección y es el mínimo inevitable: contra un proveedor real los tests no son
deterministas, cuestan dinero y necesitan conectividad.

Ningún test de este directorio sabe cuántos pasos tiene el análisis, cómo se
llama el módulo que combina los puntajes ni qué proveedor está detrás. El
criterio operativo: en la Entrega 4 se reemplaza el paso de clasificación por el
clasificador propio ajustado y ningún test debería tener que cambiar.

**Cómo se sustituye el proveedor en un test.** El doble no hereda de nada: le
alcanza con tener los tres métodos que declara `ProveedorDeAnalisis`. La clave
del diccionario de sustituciones es la función `obtener_proveedor`, no la clase
del proveedor:

    def test_algo(cliente_con, proveedor_doble):
        proveedor_doble.veredicto = Veredicto.PARECE_VERIFICADO
        respuesta = cliente_con.post("/analizar", json=...)

El accesorio `cliente` trae el doble con valores por defecto. Para un doble
distinto —otro veredicto, otras razones, una falla— se usa `construir_cliente`,
que arma el cliente alrededor del proveedor que se le pase y deshace la
sustitución al terminar.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

import pytest
from fastapi.testclient import TestClient

from app.contrato import Fuente, Razon, TipoAfirmacion, Veredicto
from app.dependencias import obtener_proveedor
from app.main import aplicacion
from app.proveedor.puerto import AfirmacionExtraida, VeredictoEmitido

PEDIDO_DE_EJEMPLO = {
    "tweet_id": "1234567890123456789",
    "texto": "A partir del lunes cierran todas las escuelas de la Provincia.",
    "handle": "@ejemplo",
}


def afirmacion_extraida_de(texto: str) -> str:
    """Extracción trivial del doble, a partir del texto que recibió.

    Devuelve algo **distinto** del texto recibido a propósito. Si el doble
    devolviera el texto tal cual, ningún test podría distinguir una respuesta
    que trae la afirmación extraída de una que se quedó con el texto crudo del
    tuit, que es justamente lo que RF-04 pide que dejen de ser la misma cosa.
    """
    return f"Afirmación extraída: {texto}"


class ProveedorDoble:
    """Doble del puerto del proveedor, con respuestas fijadas por el test.

    Registra los textos con los que se lo llamó, para que un test pueda
    comprobar que el análisis se hizo sobre el tuit que llegó en la petición sin
    tener que saber nada del interior del servicio.

    `afirmacion` en `None` significa que el doble extrae con
    `afirmacion_extraida_de`. Una cadena vacía significa que la publicación no
    contenía ninguna afirmación verificable, que es como el puerto representa
    ese caso.
    """

    def __init__(
        self,
        veredicto: Veredicto = Veredicto.SIN_CONTRASTE_EXTERNO,
        justificacion: str = (
            "No se encontró ninguna fuente que permita contrastar la afirmación, "
            "así que no puede darse por cierta ni por falsa con lo disponible."
        ),
        razones: list[Razon] | None = None,
        fuentes: list[Fuente] | None = None,
        error: Exception | None = None,
        afirmacion: str | None = None,
        tipo: TipoAfirmacion = TipoAfirmacion.EDUCACION,
        puntaje_clasificador: float = 0.62,
        clase_clasificador: str = "sin_verificar",
    ) -> None:
        self.veredicto = veredicto
        self.justificacion = justificacion
        self.razones = razones if razones is not None else [
            Razon(texto="La publicación no cita ninguna fuente.", fuente_url=None),
            Razon(
                texto="La afirmación es absoluta y no acota a qué distrito alcanza.",
                fuente_url=None,
            ),
        ]
        self.fuentes = fuentes if fuentes is not None else []
        self.error = error
        self.afirmacion = afirmacion
        self.tipo = tipo
        self.puntaje_clasificador = puntaje_clasificador
        self.clase_clasificador = clase_clasificador
        self.textos_recibidos: list[str] = []
        self.afirmaciones_recibidas: list[str] = []

    def extraer_afirmacion(self, texto: str) -> AfirmacionExtraida:
        self.textos_recibidos.append(texto)
        if self.error is not None:
            raise self.error
        afirmacion = (
            self.afirmacion if self.afirmacion is not None
            else afirmacion_extraida_de(texto)
        )
        return AfirmacionExtraida(
            afirmacion=afirmacion,
            tipo=self.tipo,
            puntaje=self.puntaje_clasificador,
            clase=self.clase_clasificador,
        )

    def recuperar_evidencia(self, afirmacion: str) -> list[Fuente]:
        return list(self.fuentes)

    def emitir_veredicto(
        self, afirmacion: str, fuentes: list[Fuente]
    ) -> VeredictoEmitido:
        self.afirmaciones_recibidas.append(afirmacion)
        if self.error is not None:
            raise self.error
        return VeredictoEmitido(
            veredicto=self.veredicto,
            justificacion=self.justificacion,
            razones=list(self.razones),
        )


@contextmanager
def construir_cliente(proveedor: ProveedorDoble) -> Iterator[TestClient]:
    """Devuelve un cliente de pruebas con el proveedor sustituido por el doble."""
    aplicacion.dependency_overrides[obtener_proveedor] = lambda: proveedor
    try:
        with TestClient(aplicacion) as cliente:
            yield cliente
    finally:
        aplicacion.dependency_overrides.pop(obtener_proveedor, None)


@pytest.fixture
def proveedor_doble() -> ProveedorDoble:
    """Doble con valores por defecto: sin fuentes y sin contraste externo."""
    return ProveedorDoble()


@pytest.fixture
def cliente(proveedor_doble: ProveedorDoble) -> Iterator[TestClient]:
    """Cliente de pruebas con el doble por defecto ya sustituido."""
    with construir_cliente(proveedor_doble) as cliente_de_pruebas:
        yield cliente_de_pruebas
