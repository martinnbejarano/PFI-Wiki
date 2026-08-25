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

Estado de implementación en esta instancia del prototipo: las tres operaciones
están implementadas contra el proveedor real, determinación de la postura de
cada fuente incluida.

**El proveedor no decide el veredicto.** `emitir_veredicto` recibe el nivel ya
resuelto y devuelve la justificación que lo explica. El nivel lo produce el
combinador a partir de los tres puntajes parciales, con los pesos y los umbrales
de la configuración; ver `app/combinador.py` y `app/pipeline.py`. Es la
diferencia entre un veredicto que resulta de combinar evidencia y uno que sale
del juicio suelto de una llamada, y es lo que RF-06 describe.
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

    Trae la justificación en lenguaje natural y las razones que la sostienen, y
    **no el nivel del veredicto**: ese ya venía decidido por el combinador
    cuando este paso se llamó. Preguntárselo también al proveedor abriría la
    posibilidad de que la respuesta muestre un nivel y una justificación que
    dicen cosas distintas, que es la falla más visible que este prototipo puede
    tener en una exposición.

    `razones` respeta la regla de RNF-06: una razón lleva `fuente_url` solo
    cuando deriva de evidencia externa enlazable. Sin evidencia recuperada,
    todas las razones vienen con `fuente_url` en `None`.
    """

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

        Cada fuente vuelve con su **postura** respecto de la afirmación
        —corrobora, contradice o neutral—, que es la segunda mitad de RF-05 y lo
        que el combinador agrega para producir el puntaje de contraste.

        Devuelve la lista vacía cuando no encuentra ninguna fuente admisible;
        la lista vacía es un resultado legítimo, no una falla.

        El adaptador puede devolver lo que quiera: el orquestador vuelve a
        aplicar la jerarquía de `jerarquia.py` sobre lo que salga de acá, del
        mismo modo en que vuelve a exigir la regla de RNF-06 sobre el veredicto.
        La restricción de RF-05 es una invariante del servicio y no una promesa
        que cada adaptador tenga que acordarse de cumplir.
        """
        ...

    def emitir_veredicto(
        self, afirmacion: str, fuentes: list[Fuente], veredicto: Veredicto
    ) -> VeredictoEmitido:
        """Redacta la justificación en lenguaje natural del veredicto (RF-06).

        `veredicto` llega decidido por el combinador y **no se discute**: este
        paso explica, con las fuentes recuperadas y sus posturas, por qué el
        análisis terminó en ese nivel. Las tres entradas son coherentes entre sí
        porque el nivel se derivó de las mismas posturas que la lista de fuentes
        trae.

        Con `fuentes` vacía el veredicto que llega es
        `Veredicto.SIN_CONTRASTE_EXTERNO`, y la justificación tiene que explicar
        qué habría que verificar en lugar de afirmar nada sobre la afirmación.

        **Este paso no recibe nada sobre la cuenta autora**, y no por olvido: es
        la forma en que RNF-07 se hace valer estructuralmente. El texto que
        justifica el resultado se escribe sin saber quién publicó, así que no
        puede enunciarse sobre esa persona.
        """
        ...


__all__ = [
    "AfirmacionExtraida",
    "ErrorDelProveedor",
    "ProveedorDeAnalisis",
    "VeredictoEmitido",
    "Razon",
]
