"""Módulo 2 — credibilidad de la cuenta autora, en su forma recortada.

**Este módulo no mide nada.** Devuelve un número inventado. Está acá porque el
contrato de la respuesta reserva un lugar para el puntaje de credibilidad y la
interfaz tiene que poder dibujar el desglose de los tres puntajes parciales,
no porque haya una medición detrás. Viaja siempre con
`PuntajeCredibilidad.no_implementado` en verdadero y la interfaz lo pinta con el
patrón visual de módulo ausente.

Por qué el recorte, tal como quedó declarado en la *spec* (issue #18): el DOM del
*timeline* no expone la antigüedad de la cuenta ni su cantidad de seguidores, y
obtenerlas exigiría una petición adicional por cuenta que rompe el presupuesto
de latencia de RNF-02. El módulo real llega con el sistema completo.

**Por qué un valor derivado del *handle* y no un valor fijo.** Un número estable
entre recargas elimina el único modo de falla visible durante la exposición
—que el valor parpadee entre dos recargas del mismo tuit— sin cambiar la
naturaleza del dato. Un valor fijo para todas las cuentas, en cambio, haría
ilegible el desglose: las tres barras del detalle se verían siempre iguales.

**Por qué `hashlib` y no `hash()`.** La función `hash()` de Python aleatoriza su
semilla por proceso (`PYTHONHASHSEED`), así que el mismo *handle* daría números
distintos entre dos arranques del servicio. `hashlib.sha256` es estable entre
procesos, entre máquinas y entre versiones del intérprete, que es exactamente lo
que el criterio de estabilidad pide.
"""

from __future__ import annotations

import hashlib

# El valor se acota lejos de los extremos a propósito. Un 0,00 o un 1,00 se
# leen como certezas —«esta cuenta no es confiable en absoluto»—, y este número
# no sostiene ninguna certeza. La banda intermedia deja ver que el módulo aporta
# algo sin sugerir que ese algo esté medido.
CREDIBILIDAD_MINIMA = 0.10
CREDIBILIDAD_MAXIMA = 0.90

# Cuántos valores distintos puede tomar el puntaje. Con dos decimales visibles
# en la interfaz, la resolución fina no aporta nada.
_PASOS = 10_000


def puntaje_de_credibilidad(handle: str) -> float:
    """Devuelve el puntaje arbitrario de credibilidad de una cuenta.

    El mismo *handle* devuelve siempre el mismo valor, en este proceso y en
    cualquier otro.

    Deliberadamente **no** recibe ni consulta `PedidoAnalisis.verificada` ni
    `PedidoAnalisis.metricas`, aunque ambas estén disponibles desde que el
    lector del DOM las lee. Mezclar dos señales reales con una fórmula inventada
    produciría una medición a medias: un número que se puede defender como
    parcialmente fundado y que por eso mismo invita a leerse como una medición.
    Un dato declaradamente inventado es más honesto y más fácil de reemplazar
    cuando el módulo real exista. La regla vale para cualquiera que retome esto:
    o el módulo mide de verdad, o no mide nada.
    """
    semilla = _normalizar(handle)
    digestion = hashlib.sha256(semilla.encode("utf-8")).digest()
    entero = int.from_bytes(digestion[:8], "big")
    fraccion = (entero % _PASOS) / (_PASOS - 1)
    recorrido = CREDIBILIDAD_MAXIMA - CREDIBILIDAD_MINIMA
    return round(CREDIBILIDAD_MINIMA + fraccion * recorrido, 2)


def _normalizar(handle: str) -> str:
    """Reduce el *handle* a la forma con la que se siembra el resumen.

    X trata los identificadores sin distinguir mayúsculas, y el lector del DOM
    puede traer o no la arroba según de qué nodo lo haya leído. Sin esta
    normalización, `@Ejemplo` y `ejemplo` darían dos puntajes distintos para la
    misma cuenta, que es justo la inestabilidad que este módulo evita.
    """
    return handle.strip().lstrip("@").casefold()
