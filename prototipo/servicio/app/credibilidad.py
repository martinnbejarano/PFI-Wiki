"""Módulo 2 — credibilidad de la cuenta autora.

Resume la trayectoria pública de la cuenta en un número entre 0 y 1, donde 1 es
una cuenta con trayectoria establecida. Es una regla fija y declarada, no un
modelo entrenado: un promedio ponderado de cuatro subpuntajes, cada uno acotado
entre 0 y 1::

    credibilidad = p_ant · antigüedad + p_seg · seguidores
                 + p_rel · relación   + p_ver · verificada

    antigüedad = min(días desde la creación / días_antigüedad_plena, 1)
    seguidores = min(log10(seguidores + 1) / log10(seguidores_plenos), 1)
    relación   = min(seguidores / (seguidos + 1), 1)
    verificada = 1 con insignia, 0,5 sin ella

Por qué cada señal:

- **Antigüedad.** Las cuentas creadas para una campaña de desinformación suelen
  ser recientes. Satura a los dos años: pasado ese punto, más años no dicen nada.
- **Seguidores, en escala logarítmica.** Una audiencia construida es costosa de
  fabricar. El logaritmo evita que una cuenta con un millón de seguidores pese
  mil veces más que una con mil.
- **Relación seguidores/seguidos.** Seguir a miles de cuentas y que la sigan
  pocas es el patrón típico de una cuenta automatizada que busca reciprocidad.
- **Insignia de verificación.** Pesa poco y su ausencia vale 0,5 y no 0: desde
  X Premium la insignia se compra, así que tenerla dice algo y no tenerla casi
  nada.

**Por qué el módulo pesa poco en el veredicto.** Lo que se evalúa es la
afirmación y no quien la publica (RNF-07): una cuenta nueva puede decir una
verdad y una consolidada, repetir un rumor. La trayectoria de la cuenta aporta
una señal de contexto, menor que lo que dice el texto y mucho menor que lo que
dicen las fuentes. El reparto vive en `Configuracion`.

**De dónde salen los datos.** La extensión los toma del objeto de la cuenta que
X ya entregó al navegador junto con el *timeline*, sin pedidos propios. Cuando
el objeto no está, el módulo devuelve `None` y el combinador lo deja fuera de
la ponderación en lugar de inventar un valor neutro.
"""

from __future__ import annotations

import math
from datetime import UTC, datetime

from .configuracion import Configuracion
from .contrato import CuentaAutora

# Sin insignia no se sabe nada: el punto medio, no el cero. Ver el encabezado.
VERIFICADA_SIN_INSIGNIA = 0.5


def puntaje_de_credibilidad(
    cuenta: CuentaAutora | None,
    verificada: bool,
    configuracion: Configuracion,
    ahora: datetime | None = None,
) -> float | None:
    """Devuelve la credibilidad de la cuenta autora, o `None` sin datos."""
    if cuenta is None:
        return None

    ahora = ahora or datetime.now(UTC)
    creada = cuenta.creada if cuenta.creada.tzinfo else cuenta.creada.replace(tzinfo=UTC)
    dias = max((ahora - creada).days, 0)

    subpuntajes = (
        (
            configuracion.peso_credibilidad_antiguedad,
            min(dias / configuracion.dias_antiguedad_plena, 1.0),
        ),
        (
            configuracion.peso_credibilidad_seguidores,
            min(
                math.log10(cuenta.seguidores + 1)
                / math.log10(configuracion.seguidores_plenos),
                1.0,
            ),
        ),
        (
            configuracion.peso_credibilidad_relacion,
            min(cuenta.seguidores / (cuenta.seguidos + 1), 1.0),
        ),
        (
            configuracion.peso_credibilidad_verificada,
            1.0 if verificada else VERIFICADA_SIN_INSIGNIA,
        ),
    )
    peso_total = sum(peso for peso, _ in subpuntajes)
    if peso_total <= 0.0:
        return None
    return round(sum(peso * valor for peso, valor in subpuntajes) / peso_total, 4)
