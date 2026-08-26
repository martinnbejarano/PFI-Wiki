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
del proveedor.

El accesorio `cliente` trae el doble con valores por defecto. Para un doble
distinto —otras fuentes, otras razones, una falla— se usa `construir_cliente`,
que arma el cliente alrededor del proveedor que se le pase y deshace la
sustitución al terminar.

**Cómo se sustituye la configuración.** Por el mismo mecanismo y en la misma
función: `construir_cliente(doble, configuracion=Configuracion(peso_contraste=0.9))`.
Los pesos del combinador y los umbrales de los tres niveles viven en la
configuración por RNF-16, así que un test que quiera moverlos no toca variables
de entorno del proceso ni escribe archivos: arma la configuración que quiere y
la inyecta, igual que inyecta el proveedor.

**La caché se sustituye siempre, y sin que ningún test tenga que pedirlo.** La
reutilización de análisis previos (RF-07) es estado del proceso, así que
`construir_cliente` le da a cada cliente una caché vacía. Sin eso, dos tests que
usaran el mismo identificador de tuit —y casi todos usan `PEDIDO_DE_EJEMPLO`—
compartirían el análisis del primero que corriera, y la batería pasaría o
fallaría según el orden. Un test que pasa según el orden en que corre es peor
que ninguno.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

import pytest
from fastapi.testclient import TestClient

from app.cache import CacheDeAnalisis, obtener_cache
from app.configuracion import Configuracion, obtener_configuracion
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

    Registra todo lo que se le pasó en cada llamada, para que un test pueda
    comprobar sobre qué se hizo el análisis —y sobre qué **no** se hizo, que es
    lo que RNF-07 exige— sin tener que saber nada del interior del servicio.

    `afirmacion` en `None` significa que el doble extrae con
    `afirmacion_extraida_de`. Una cadena vacía significa que la publicación no
    contenía ninguna afirmación verificable, que es como el puerto representa
    ese caso.

    **No hay forma de fijarle el veredicto**, y no es un olvido: el proveedor no
    decide el veredicto. El nivel lo produce el servicio combinando los puntajes
    parciales, y un test que quiera un nivel concreto lo consigue por donde el
    sistema lo decide de verdad —la postura de las fuentes, el puntaje del
    clasificador y los pesos de la configuración— y no fijándolo a mano.

    **Las fallas se fijan por operación y no de a una para todas.** El puerto
    tiene tres operaciones y el servicio las usa para cosas distintas, así que
    una falla en cada una degrada de manera distinta (RNF-11). Un solo
    interruptor de falla sólo permitiría probar la primera, porque el análisis
    nunca llegaría a la segunda. Los tres nombres son los del puerto, no los de
    ningún paso interno del servicio: un test dice «la búsqueda de evidencia no
    responde» y mira qué sale por HTTP, sin saber en qué orden se llaman ni
    cuántos pasos hay.
    """

    def __init__(
        self,
        justificacion: str = (
            "No se encontró ninguna fuente que permita contrastar la afirmación, "
            "así que no puede darse por cierta ni por falsa con lo disponible."
        ),
        razones: list[Razon] | None = None,
        fuentes: list[Fuente] | None = None,
        error_extraccion: Exception | None = None,
        error_evidencia: Exception | None = None,
        error_veredicto: Exception | None = None,
        afirmacion: str | None = None,
        tipo: TipoAfirmacion = TipoAfirmacion.EDUCACION,
        puntaje_clasificador: float = 0.62,
        clase_clasificador: str = "sin_verificar",
    ) -> None:
        self.justificacion = justificacion
        self.razones = razones if razones is not None else [
            Razon(texto="La publicación no cita ninguna fuente.", fuente_url=None),
            Razon(
                texto="La afirmación es absoluta y no acota a qué distrito alcanza.",
                fuente_url=None,
            ),
        ]
        self.fuentes = fuentes if fuentes is not None else []
        self.error_extraccion = error_extraccion
        self.error_evidencia = error_evidencia
        self.error_veredicto = error_veredicto
        self.afirmacion = afirmacion
        self.tipo = tipo
        self.puntaje_clasificador = puntaje_clasificador
        self.clase_clasificador = clase_clasificador
        self.textos_recibidos: list[str] = []
        self.afirmaciones_recibidas: list[str] = []
        self.veredictos_recibidos: list[Veredicto] = []
        self.entradas_recibidas: list[str] = []
        """Todo texto que el servicio le pasó al proveedor, en cualquier paso.

        Sirve para dos cosas. Una: comprobar desde afuera que un dato **no**
        llegó a ningún paso del análisis, que es como este servicio hace valer
        la primera mitad de RNF-07. Otra: contar cuántas veces se invocó al
        proveedor, que es como se comprueba que un tuit ya analizado se resuelve
        sin volver a llamarlo (RF-07)."""

    def extraer_afirmacion(self, texto: str) -> AfirmacionExtraida:
        self.textos_recibidos.append(texto)
        self.entradas_recibidas.append(texto)
        if self.error_extraccion is not None:
            raise self.error_extraccion
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
        self.entradas_recibidas.append(afirmacion)
        if self.error_evidencia is not None:
            raise self.error_evidencia
        return list(self.fuentes)

    def emitir_veredicto(
        self, afirmacion: str, fuentes: list[Fuente], veredicto: Veredicto
    ) -> VeredictoEmitido:
        self.afirmaciones_recibidas.append(afirmacion)
        self.entradas_recibidas.append(afirmacion)
        self.veredictos_recibidos.append(veredicto)
        if self.error_veredicto is not None:
            raise self.error_veredicto
        return VeredictoEmitido(
            justificacion=self.justificacion,
            razones=list(self.razones),
        )


@contextmanager
def construir_cliente(
    proveedor: ProveedorDoble,
    configuracion: Configuracion | None = None,
    cache: CacheDeAnalisis | None = None,
) -> Iterator[TestClient]:
    """Cliente de pruebas con el proveedor —y opcionalmente la configuración— sustituidos.

    Sin `configuracion`, el servicio usa la suya, que es la que trae los pesos y
    los umbrales por defecto. Pasándole una, se ejercita el mismo servicio con
    otro juego de pesos sin tocar el entorno del proceso ni ningún archivo: es
    la forma de comprobar por el contrato HTTP lo que RNF-16 exige.

    La caché de análisis se sustituye **siempre**, sin que el test tenga que
    pedirlo, y sin `cache` cada cliente arranca con una vacía: es lo que aísla
    un test del que corrió antes. Pasarle una existente sirve para lo único que
    no se puede ejercitar con clientes aislados: que un análisis guardado con
    unos pesos no se devuelva después de cambiarlos.
    """
    # Una sola instancia para todo el cliente, y no una por petición: si cada
    # petición armara la suya, la caché nunca acertaría y el test de RF-07
    # pasaría por el motivo equivocado.
    la_cache = cache if cache is not None else CacheDeAnalisis()

    aplicacion.dependency_overrides[obtener_proveedor] = lambda: proveedor
    aplicacion.dependency_overrides[obtener_cache] = lambda: la_cache
    if configuracion is not None:
        aplicacion.dependency_overrides[obtener_configuracion] = lambda: configuracion
    try:
        with TestClient(aplicacion) as cliente:
            yield cliente
    finally:
        aplicacion.dependency_overrides.pop(obtener_proveedor, None)
        aplicacion.dependency_overrides.pop(obtener_cache, None)
        aplicacion.dependency_overrides.pop(obtener_configuracion, None)


@pytest.fixture
def proveedor_doble() -> ProveedorDoble:
    """Doble con valores por defecto: sin fuentes y sin contraste externo."""
    return ProveedorDoble()


@pytest.fixture
def cliente(proveedor_doble: ProveedorDoble) -> Iterator[TestClient]:
    """Cliente de pruebas con el doble por defecto ya sustituido."""
    with construir_cliente(proveedor_doble) as cliente_de_pruebas:
        yield cliente_de_pruebas
