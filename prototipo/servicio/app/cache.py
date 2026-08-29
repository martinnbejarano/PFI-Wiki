"""Reutilización de análisis previos (RF-07).

> RF-07: «El sistema debe reutilizar un análisis previo cuando el mismo tuit
> vuelve a solicitarse y el resultado sigue vigente.»

Una caché **en memoria del proceso**. No hay base de datos: la *spec* dejó la
persistencia fuera del alcance del prototipo, así que lo que se guarda acá se
pierde al reiniciar el servicio y eso se declara en `prototipo/README.md`.

Ningún test importa este módulo. Se ejercita entero por `POST /analizar`, igual
que el resto del servicio: dos peticiones sobre el mismo identificador nativo y
un doble del proveedor invocado una sola vez. Es lo que permite reemplazarla
mañana por la persistencia de RF-16 sin tocar una línea de la batería.


La clave, y por qué no es solo el identificador del tuit
--------------------------------------------------------

La clave es la terna **identificador nativo del tuit + versión del modelo +
versión de la configuración de pesos**.

RF-16 pide asociar cada análisis a las dos versiones que lo produjeron, y una
caché indexada solo por el identificador del tuit haría exactamente lo
contrario: alguien cambia un peso, reinicia con la configuración nueva —o
sustituye el proveedor— y el mismo tuit sigue devolviendo el análisis viejo,
producido con valores que ya no están en uso. En una demostración en vivo eso es
peor que un error, porque el mecanismo de RNF-16 —mover un peso y ver moverse el
resultado— parece roto sin estarlo.

Con las versiones en la clave, cambiar cualquier peso, cualquier umbral o el
modelo invalida por construcción todo lo guardado con los valores anteriores. No
hay que acordarse de vaciar nada. Es la misma razón por la que
`version_configuracion_pesos` es una propiedad calculada y no una cadena que
alguien escribe a mano; ver `app/configuracion.py`.


Qué **no** se guarda, y por qué
-------------------------------

**Un análisis parcial no se cachea.** Es la decisión de fondo de este módulo.

Un parcial es el resultado de una falla —el proveedor no respondió, la búsqueda
no volvió, la respuesta llegó malformada—, y esas fallas son casi siempre
transitorias. Guardarlo convertiría un corte de red de tres segundos en un
resultado permanente hasta reiniciar el proceso: el ciudadano vuelve a pedir el
análisis del mismo tuit, el proveedor ya está sano, y la extensión le sigue
devolviendo el parcial de hace un rato sin volver a intentar nada. En una
exposición es precisamente el modo de falla que no se quiere tener, porque la
única salida visible sería reiniciar el servicio delante del tribunal.

La contracara es que un proveedor caído se paga con una llamada fallida por
clic, que es barata: la llamada que falla no consume fichas y el análisis parcial
sale igual de rápido. Se elige pagar eso a cambio de que reintentar signifique
reintentar.

No es lo mismo que el caso de la publicación sin afirmación verificable: ese
análisis **sí** se guarda, porque no es una falla —todos los módulos se
ejecutaron— y volver a pedirlo daría el mismo resultado. Ver
`pipeline._respuesta_sin_afirmacion`.
"""

from __future__ import annotations

import logging
from functools import lru_cache

from .configuracion import Configuracion
from .contrato import RespuestaAnalisis

registro = logging.getLogger("app.cache")

ClaveDeAnalisis = tuple[str, str, str]
"""Identificador nativo del tuit, versión del modelo y versión de los pesos."""


def _clave(tweet_id: str, configuracion: Configuracion) -> ClaveDeAnalisis:
    """Arma la clave de un análisis a partir del tuit y de las versiones en uso."""
    return (
        tweet_id,
        configuracion.version_modelo,
        configuracion.version_configuracion_pesos,
    )


class CacheDeAnalisis:
    """Análisis ya resueltos, guardados en memoria del proceso.

    Sin tope de tamaño y sin vencimiento, a propósito: el prototipo resuelve un
    tuit por clic durante una demostración de veinte minutos, y un desalojo por
    antigüedad o por tamaño sería código que nadie puede ver funcionar ese día.
    La caché de verdad —con vencimiento, y con la vigencia que RF-07 menciona—
    llega con la persistencia de RF-16, que este prototipo declaró fuera de
    alcance.
    """

    def __init__(self) -> None:
        self._analisis: dict[ClaveDeAnalisis, RespuestaAnalisis] = {}

    def obtener(
        self, tweet_id: str, configuracion: Configuracion
    ) -> RespuestaAnalisis | None:
        """Devuelve el análisis guardado para ese tuit, o `None` si no hay."""
        guardado = self._analisis.get(_clave(tweet_id, configuracion))
        if guardado is not None:
            registro.info("cache | acierto para el tuit %s", tweet_id)
        return guardado

    def guardar(
        self, analisis: RespuestaAnalisis, configuracion: Configuracion
    ) -> None:
        """Guarda un análisis, salvo que sea parcial.

        La regla de no guardar parciales vive **acá dentro** y no en el
        orquestador: es una propiedad de la caché y no de quien la usa, así que
        ningún llamador futuro puede saltearla por olvido.
        """
        if analisis.analisis_parcial.es_parcial:
            registro.info(
                "cache | no se guarda el análisis parcial del tuit %s "
                "(módulos ausentes: %s)",
                analisis.tweet_id,
                ", ".join(analisis.analisis_parcial.modulos_ausentes) or "ninguno",
            )
            return

        self._analisis[_clave(analisis.tweet_id, configuracion)] = analisis


@lru_cache
def obtener_cache() -> CacheDeAnalisis:
    """Devuelve la caché del proceso.

    Es una dependencia de FastAPI, resuelta con `Depends` en el borde de red
    igual que el puerto del proveedor y la configuración. Los tests la
    sustituyen por el mismo mecanismo, y por eso cada cliente de pruebas
    arranca con una caché vacía en lugar de heredar la del test anterior:

        aplicacion.dependency_overrides[obtener_cache] = lambda: CacheDeAnalisis()

    Un estado global que sobreviviera entre tests haría que la batería pasara o
    fallara según el orden en que corre, que es peor que no tenerla.
    """
    return CacheDeAnalisis()
