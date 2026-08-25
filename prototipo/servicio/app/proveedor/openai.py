"""Adaptador de OpenAI para el puerto del proveedor.

Este es el **único** archivo del servicio que nombra a OpenAI. Cambiar de
proveedor, o sustituir el paso de clasificación por el clasificador propio
ajustado en la Entrega 4, es escribir otro adaptador de `ProveedorDeAnalisis` y
cambiar la línea de `dependencias.py` que lo construye.

Documentación consultada el **2026-08-25**:

- Referencia de la API de respuestas (*Responses API*), que es la interfaz
  vigente y la que admite la herramienta de búsqueda web que el paso de
  recuperación de evidencia va a necesitar:
  https://developers.openai.com/api/reference/python/resources/responses
- Guía de salida estructurada (*structured outputs*), de donde sale el uso de
  `responses.parse(..., text_format=<modelo de Pydantic>)` y la lectura del
  resultado en `output_parsed`:
  https://developers.openai.com/api/docs/guides/structured-outputs
- Catálogo de modelos y tabla de precios, de donde salen el identificador
  `gpt-5.6-luna` y los precios anotados en `configuracion.py`:
  https://developers.openai.com/api/docs/models
  https://developers.openai.com/api/docs/pricing

La credencial no se lee en el momento de importar este módulo ni al construir
el adaptador: el cliente se crea perezosamente en la primera llamada real. Así
el servicio arranca sin credencial y la batería de pruebas corre sin red.
"""

from __future__ import annotations

import logging
import time
from enum import Enum
from typing import TypeVar

from openai import APIError, APITimeoutError, OpenAI, OpenAIError
from pydantic import BaseModel

from ..configuracion import Configuracion
from ..contrato import Fuente, Razon, TipoAfirmacion, Veredicto
from .puerto import AfirmacionExtraida, ErrorDelProveedor, VeredictoEmitido

registro = logging.getLogger(__name__)

_Salida = TypeVar("_Salida", bound=BaseModel)


INSTRUCCIONES_EXTRACCION = """\
Sos el módulo de extracción y clasificación de un sistema de detección de \
desinformación en publicaciones de la red social X, orientado al contexto \
argentino.

Recibís el texto de una publicación. Tenés que devolver cuatro cosas: la \
afirmación verificable que contiene, su tipo, un puntaje y una clase.

1. **La afirmación.** Es el hecho contrastable que la publicación sostiene, \
reescrito como un enunciado autónomo, en una sola oración, entendible sin \
haber leído el tuit. Sacá los emojis, los hashtags, las mayúsculas de grito y \
las apelaciones a compartir. No agregues ningún dato que el texto no diga: si \
la publicación no aclara la fecha, el lugar ni el organismo, la afirmación \
tampoco los aclara. Si la publicación sostiene varias, quedate con la más \
verificable y la más central.

2. **Cuando no hay ninguna afirmación verificable**, devolvé `afirmacion` como \
cadena vacía, `tipo` en `otro`, `clase` en `sin_verificar` y `puntaje` en 0. \
Es el caso de una opinión, una valoración, una pregunta, una broma, un saludo, \
una consigna o un mensaje personal: nada de eso enuncia un hecho que se pueda \
contrastar contra una fuente. No fuerces una afirmación donde no la hay; \
inventarla es peor que decir que no hay.

3. **El tipo.** Uno de estos cinco, exactamente: `normativa` para leyes, \
decretos, resoluciones y medidas de gobierno; `dato_economico` para \
inflación, precios, tipo de cambio, empleo, salarios y estadísticas \
oficiales; `salud` para enfermedades, vacunas, tratamientos y sistema \
sanitario; `educacion` para escuelas, universidades, docentes y calendario \
escolar; `otro` para todo lo demás.

4. **El puntaje.** Un número entre 0 y 1 que estima qué tan probable es que la \
publicación sea desinformación, juzgada **únicamente por su texto** y sin \
ninguna evidencia externa. Suben el puntaje el lenguaje de urgencia y de \
alarma, las mayúsculas de grito, las afirmaciones absolutas sin fuente citada, \
la apelación a compartir antes de que \"lo bajen\", la atribución a fuentes \
anónimas y la incoherencia interna. Lo bajan el tono descriptivo, la mención \
de la fuente y el enunciado acotado. No uses lo que sepas del mundo para \
decidir si el hecho ocurrió: eso lo resuelve el módulo de contraste con \
fuentes, no vos.

5. **La clase.** `falso` si el texto solo tiene señales de desinformación, \
`verdadero` si se lee como una descripción sobria de un hecho, y \
`sin_verificar` cuando el texto no alcanza para inclinarse por ninguna de las \
dos. `sin_verificar` no es un punto intermedio de una escala: es la ausencia \
de respaldo suficiente para pronunciarse, y es la respuesta correcta para casi \
todo el contenido de circulación reciente.

Escribí la afirmación en castellano rioplatense, sin tecnicismos.
"""


INSTRUCCIONES_VEREDICTO = """\
Sos el módulo de emisión de veredictos de un sistema de detección de \
desinformación en publicaciones de la red social X, orientado al contexto \
argentino.

Recibís una afirmación y la lista de fuentes que el módulo de contraste \
recuperó. Tenés que emitir un veredicto, una justificación en lenguaje natural \
y las razones que la sostienen.

Reglas que no se negocian:

1. Si la lista de fuentes viene vacía, el veredicto es exactamente \
`sin_contraste_externo`. Nunca uno de los tres niveles. Sin evidencia externa \
no hay veredicto que sostener: decirlo es el resultado correcto, no una falla.
2. Una razón lleva `fuente_url` solamente si esa URL está en la lista de \
fuentes recibida. Si la lista viene vacía, todas las razones llevan \
`fuente_url` en null. No inventes enlaces, títulos ni medios bajo ninguna \
circunstancia.
3. El resultado se enuncia siempre sobre la afirmación y nunca sobre la \
persona que la publicó.
4. Sin fuentes, la justificación explica qué habría que verificar y por qué la \
afirmación no puede darse por cierta ni por falsa con lo disponible. No afirma \
que la publicación sea falsa ni que sea verdadera.
5. Escribí en castellano rioplatense, claro y sin tecnicismos, para alguien sin \
formación técnica. Entre dos y cuatro oraciones de justificación, y entre dos y \
cuatro razones.
"""


class _ClaseDelTexto(str, Enum):
    """Las tres clases del Módulo 1, tal como las fija el capítulo 4.

    `sin_verificar` no expresa un grado intermedio de veracidad sino la
    ausencia de evidencia suficiente para pronunciarse, y es la situación
    habitual del contenido de circulación reciente, que es el que al sistema le
    interesa detectar.

    El dominio se cierra acá, donde el valor se produce: la salida estructurada
    obliga al modelo a elegir uno de los tres y no admite una etiqueta
    inventada. El contrato de la respuesta lo transporta como cadena.
    """

    VERDADERO = "verdadero"
    FALSO = "falso"
    SIN_VERIFICAR = "sin_verificar"


class _SalidaExtraccion(BaseModel):
    """Esquema de la salida estructurada del paso de extracción."""

    afirmacion: str
    tipo: TipoAfirmacion
    puntaje: float
    clase: _ClaseDelTexto


class _RazonDelModelo(BaseModel):
    """Una razón tal como la devuelve el modelo.

    Se declara aparte de `contrato.Razon` a propósito: los campos del esquema
    estricto de salida estructurada no llevan valores por defecto, mientras que
    `contrato.Razon` sí los lleva por comodidad de quien construye la respuesta.
    """

    texto: str
    fuente_url: str | None


class _SalidaVeredicto(BaseModel):
    """Esquema de la salida estructurada del paso de veredicto."""

    veredicto: Veredicto
    justificacion: str
    razones: list[_RazonDelModelo]


class ProveedorOpenAI:
    """Implementación de `ProveedorDeAnalisis` contra la API de OpenAI."""

    def __init__(self, configuracion: Configuracion) -> None:
        self._configuracion = configuracion
        self._cliente_memorizado: OpenAI | None = None

    # -- construcción perezosa del cliente --------------------------------

    def _cliente(self) -> OpenAI:
        """Construye el cliente en la primera llamada real.

        La credencial ausente falla acá y no al importar el módulo ni al
        arrancar el servicio, con un mensaje que dice qué hacer.
        """
        if self._cliente_memorizado is not None:
            return self._cliente_memorizado

        clave = self._configuracion.openai_api_key
        if not clave:
            raise ErrorDelProveedor(
                "Falta la credencial del proveedor. Definí OPENAI_API_KEY en el "
                "entorno del servicio o en prototipo/servicio/.env (ese archivo "
                "está fuera del control de versiones). El servicio arranca sin "
                "la credencial a propósito: sin ella solo falla la llamada real."
            )

        self._cliente_memorizado = OpenAI(
            api_key=clave,
            timeout=self._configuracion.tiempo_limite_proveedor_s,
        )
        return self._cliente_memorizado

    # -- una llamada con salida estructurada -------------------------------

    def _parsear(
        self,
        instrucciones: str,
        entrada: str,
        formato: type[_Salida],
        paso: str,
    ) -> _Salida:
        """Hace una llamada con salida estructurada y devuelve el objeto tipado.

        Vive acá y no repetida en cada operación porque las tres comparten
        exactamente lo mismo: el modelo y sus topes salen de la configuración,
        cualquier falla se traduce a `ErrorDelProveedor` con un mensaje que dice
        en qué paso ocurrió, y la latencia y el costo de la llamada quedan
        registrados. `paso` es solo la etiqueta que hace legibles ambas cosas.
        """
        cliente = self._cliente()
        configuracion = self._configuracion

        comenzo = time.perf_counter()
        try:
            respuesta = cliente.responses.parse(
                model=configuracion.modelo_llm,
                instructions=instrucciones,
                input=entrada,
                text_format=formato,
                max_output_tokens=configuracion.max_fichas_de_salida,
                reasoning={"effort": configuracion.esfuerzo_de_razonamiento},
            )
        except APITimeoutError as error:
            raise ErrorDelProveedor(
                f"El proveedor no respondió dentro del tiempo límite de "
                f"{configuracion.tiempo_limite_proveedor_s:.0f} s en el paso de "
                f"{paso}."
            ) from error
        except (APIError, OpenAIError) as error:
            raise ErrorDelProveedor(
                f"El proveedor rechazó la llamada de {paso}: {error}"
            ) from error

        _registrar_consumo(
            respuesta, configuracion, time.perf_counter() - comenzo, paso
        )

        salida = respuesta.output_parsed
        if salida is None:
            raise ErrorDelProveedor(
                "El proveedor no devolvió una salida que se ajuste al esquema "
                f"de {paso} (estado: {respuesta.status})."
            )
        return salida

    # -- las tres operaciones del puerto -----------------------------------

    def extraer_afirmacion(self, texto: str) -> AfirmacionExtraida:
        """Extrae la afirmación verificable, su tipo y el puntaje del texto (RF-04).

        Es a la vez el Módulo 1 en su forma de línea base: la clasificación del
        texto se resuelve en *zero-shot* con el mismo modelo, que es lo que la
        *spec* compromete para esta instancia del prototipo. Sustituirlo por el
        clasificador propio ajustado en la Entrega 4 es escribir otro adaptador
        del puerto; nada fuera de este archivo cambia.
        """
        salida = self._parsear(
            INSTRUCCIONES_EXTRACCION,
            f"Publicación analizada:\n{texto}",
            _SalidaExtraccion,
            "extracción",
        )

        return AfirmacionExtraida(
            afirmacion=salida.afirmacion.strip(),
            tipo=salida.tipo,
            # El esquema estructurado fija el tipo del campo, no su rango: nada
            # impide que el modelo devuelva 1,4. Acotarlo acá evita que un valor
            # fuera de escala se convierta en un error de validación del
            # contrato —y en un 500— a tres capas de distancia de su causa.
            puntaje=min(max(salida.puntaje, 0.0), 1.0),
            clase=salida.clase.value,
        )

    def recuperar_evidencia(self, afirmacion: str) -> list[Fuente]:
        """Sin implementar todavía: llega con el ticket de evidencia (RF-05)."""
        raise NotImplementedError(
            "La búsqueda de evidencia con la jerarquía de fuentes llega con el "
            "ticket #23. Hasta entonces el análisis se emite sin contraste "
            "externo, que es lo que RNF-06 exige cuando no hay fuente."
        )

    def emitir_veredicto(
        self, afirmacion: str, fuentes: list[Fuente]
    ) -> VeredictoEmitido:
        """Emite el veredicto y la justificación con una llamada real (RF-06)."""
        salida = self._parsear(
            INSTRUCCIONES_VEREDICTO,
            _armar_entrada(afirmacion, fuentes),
            _SalidaVeredicto,
            "veredicto",
        )

        return VeredictoEmitido(
            veredicto=salida.veredicto,
            justificacion=salida.justificacion,
            razones=[
                Razon(texto=razon.texto, fuente_url=razon.fuente_url)
                for razon in salida.razones
            ],
        )


def _armar_entrada(afirmacion: str, fuentes: list[Fuente]) -> str:
    """Arma el mensaje de entrada con la afirmación y las fuentes recuperadas."""
    if not fuentes:
        listado = (
            "(ninguna: el módulo de contraste no recuperó ninguna fuente "
            "admisible)"
        )
    else:
        listado = "\n".join(
            f"- [{fuente.tipo.value} · {fuente.postura.value}] "
            f"{fuente.titulo} — {fuente.url}"
            for fuente in fuentes
        )

    return f"Afirmación analizada:\n{afirmacion}\n\nFuentes recuperadas:\n{listado}"


def _registrar_consumo(
    respuesta: object, configuracion: Configuracion, segundos: float, paso: str
) -> None:
    """Deja en el registro la latencia y el costo reales de la llamada.

    Es lo que convierte el criterio de aceptación sobre latencia y costo en algo
    medido y no estimado: cada llamada real imprime sus propios números. No hay
    valores anotados de antemano en ningún lado, porque medir exige la
    credencial del usuario y una llamada verdadera.

    El análisis de un tuit hace más de una llamada —una por paso del
    *pipeline*—, así que cada línea del registro dice a qué paso corresponde y
    la latencia del análisis completo es la suma de las suyas.

    Prueba de humo, con la credencial ya cargada en `prototipo/servicio/.env`:

        cd prototipo/servicio
        ./.venv/bin/uvicorn app.main:aplicacion --port 8001 --log-level info
        curl -sS -X POST http://127.0.0.1:8001/analizar \\
          -H 'Content-Type: application/json' \\
          -d '{"tweet_id":"1","texto":"A partir del lunes cierran todas las escuelas de la Provincia.","handle":"@ejemplo"}'

    Las líneas `proveedor` del registro de uvicorn traen el paso, el modelo, los
    segundos, las fichas consumidas y el costo en dólares de cada llamada.
    """
    uso = getattr(respuesta, "usage", None)
    fichas_entrada = getattr(uso, "input_tokens", 0) or 0
    fichas_salida = getattr(uso, "output_tokens", 0) or 0
    costo = (
        fichas_entrada * configuracion.precio_entrada_por_millon
        + fichas_salida * configuracion.precio_salida_por_millon
    ) / 1_000_000

    registro.info(
        "proveedor | paso=%s modelo=%s latencia=%.2fs fichas_entrada=%d "
        "fichas_salida=%d costo_usd=%.6f",
        paso,
        configuracion.modelo_llm,
        segundos,
        fichas_entrada,
        fichas_salida,
        costo,
    )
