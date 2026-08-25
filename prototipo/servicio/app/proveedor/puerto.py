"""El puerto único del proveedor de modelo de lenguaje grande (*LLM*).

Este módulo declara la frontera entre el servicio y el proveedor. Es la pieza
de la que depende la estrategia de reemplazo de la Entrega 4: el paso de
clasificación se sustituye por el clasificador propio ajustado implementando
`extraer_afirmacion` en otro adaptador, sin que el resto del servicio ni un solo
test tengan que cambiar.

Reglas de la frontera:

1. Ningún tipo del proveedor concreto cruza este módulo. Lo que entra y sale son
   los tipos del contrato (`contrato.py`) y los tres tipos de frontera que se
   declaran acá.
2. Las tres operaciones se corresponden una a una con los requerimientos
   entregados: `extraer_afirmacion` con RF-04, `recuperar_evidencia` con RF-05 y
   `emitir_veredicto` con RF-06.
3. `ProveedorDeAnalisis` es un `Protocol`, no una clase base. Un doble de prueba
   no hereda de nada: le alcanza con tener los tres métodos.

Estado de implementación en esta instancia del prototipo: solo
`emitir_veredicto` está implementada contra el proveedor real. Las otras dos
llegan con los tickets de extracción de la afirmación y de búsqueda de
evidencia, y hasta entonces el adaptador las rechaza con un mensaje explícito
en lugar de devolver un valor inventado.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from pydantic import BaseModel

from ..contrato import Fuente, Razon, TipoAfirmacion, Veredicto


class AfirmacionExtraida(BaseModel):
    """Salida del paso de extracción y clasificación (RF-04)."""

    afirmacion: str
    tipo: TipoAfirmacion
    puntaje: float
    clase: str


class VeredictoEmitido(BaseModel):
    """Salida del paso de emisión del veredicto (RF-06).

    `razones` respeta la regla de RNF-06: una razón lleva `fuente_url` solo
    cuando deriva de evidencia externa enlazable. Sin evidencia recuperada,
    todas las razones vienen con `fuente_url` en `None`.
    """

    veredicto: Veredicto
    justificacion: str
    razones: list[Razon]


class ErrorDelProveedor(RuntimeError):
    """Falla al hablar con el proveedor.

    Incluye la credencial ausente, el corte por tiempo límite y cualquier error
    de la API. El orquestador la traduce en análisis parcial (RNF-11) en lugar
    de dejar que escape como error opaco.
    """


@runtime_checkable
class ProveedorDeAnalisis(Protocol):
    """Las tres operaciones que el servicio le pide al proveedor.

    Es el **único** punto del servicio que conoce al proveedor y el único punto
    de inyección: `main.py` lo resuelve con `Depends` en el borde de red, y los
    tests lo sustituyen por un doble con `dependency_overrides`.
    """

    def extraer_afirmacion(self, texto: str) -> AfirmacionExtraida:
        """Extrae del texto del tuit la afirmación verificable y su tipo (RF-04)."""
        ...

    def recuperar_evidencia(self, afirmacion: str) -> list[Fuente]:
        """Recupera fuentes dentro de la jerarquía de evidencia (RF-05).

        Devuelve la lista vacía cuando no encuentra ninguna fuente admisible;
        la lista vacía es un resultado legítimo, no una falla.
        """
        ...

    def emitir_veredicto(
        self, afirmacion: str, fuentes: list[Fuente]
    ) -> VeredictoEmitido:
        """Emite el veredicto y la justificación en lenguaje natural (RF-06).

        Con `fuentes` vacía, el veredicto correcto es
        `Veredicto.SIN_CONTRASTE_EXTERNO` y nunca uno de los tres niveles. El
        orquestador lo vuelve a exigir de su lado: la regla de RNF-06 es una
        invariante del sistema y no algo que se delegue al criterio del modelo.
        """
        ...


__all__ = [
    "AfirmacionExtraida",
    "ErrorDelProveedor",
    "ProveedorDeAnalisis",
    "VeredictoEmitido",
    "Razon",
]
