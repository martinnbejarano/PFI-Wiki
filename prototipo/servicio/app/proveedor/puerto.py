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

Estado de implementación en esta instancia del prototipo: `extraer_afirmacion` y
`emitir_veredicto` están implementadas contra el proveedor real.
`recuperar_evidencia` llega con el ticket de búsqueda de evidencia, y hasta
entonces el adaptador la rechaza con un mensaje explícito en lugar de devolver
un valor inventado.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from pydantic import BaseModel

from ..contrato import Fuente, Razon, TipoAfirmacion, Veredicto


class AfirmacionExtraida(BaseModel):
    """Salida del paso de extracción y clasificación (RF-04).

    Es también la salida del Módulo 1: en esta instancia del prototipo el paso
    de extracción es la línea base de LLM en *zero-shot* que el protocolo de
    validación del capítulo 4 compromete, y de ella salen tanto la afirmación
    como el puntaje del clasificador. En la Entrega 4 se sustituye por el
    clasificador propio ajustado sin que esta forma cambie.

    Campos:

    - `afirmacion`: la afirmación verificable, reformulada como enunciado
      autónomo. **Cadena vacía cuando la publicación no contiene ninguna**, que
      es el caso de una opinión, una pregunta, una broma o un saludo. Ver
      `hay_afirmacion_verificable`.
    - `tipo`: uno de los cinco tipos de RF-04.
    - `puntaje`: probabilidad en [0,1] de que la publicación sea desinformación
      juzgada **solo por su texto**, sin evidencia externa. Es el `score_nlp`
      del Módulo 1.
    - `clase`: la clase asociada al puntaje, dentro del esquema de tres del
      capítulo 4: `verdadero`, `falso` o `sin_verificar`. Viaja como cadena y no
      como enumerado porque el contrato de la respuesta declara
      `PuntajeClasificador.clase` como cadena; el dominio cerrado se hace valer
      donde el valor se produce, en el adaptador.
    """

    afirmacion: str
    tipo: TipoAfirmacion
    puntaje: float
    clase: str

    @property
    def hay_afirmacion_verificable(self) -> bool:
        """Si la publicación contenía algo que se pueda contrastar.

        La ausencia se representa con `afirmacion` vacía y se lee siempre por
        esta propiedad, nunca comparando contra la cadena vacía en el llamador:
        cualquier adaptador futuro —el clasificador propio de la Entrega 4
        incluido— hereda así la misma regla sin tener que conocerla.
        """
        return bool(self.afirmacion.strip())


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
        """Extrae del texto del tuit la afirmación verificable y su tipo (RF-04).

        Cuando el texto no contiene ninguna afirmación verificable, devuelve
        `AfirmacionExtraida` con `afirmacion` vacía en lugar de fallar: no tener
        nada que verificar es un resultado legítimo del paso, no una falla.
        """
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
