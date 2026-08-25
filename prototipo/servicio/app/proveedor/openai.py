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

from openai import APIError, APITimeoutError, OpenAI, OpenAIError
from pydantic import BaseModel

from ..configuracion import Configuracion
from ..contrato import Fuente, Razon, Veredicto
from .puerto import AfirmacionExtraida, ErrorDelProveedor, VeredictoEmitido

registro = logging.getLogger(__name__)


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

    # -- las tres operaciones del puerto -----------------------------------

    def extraer_afirmacion(self, texto: str) -> AfirmacionExtraida:
        """Sin implementar todavía: llega con el ticket de la afirmación (RF-04)."""
        raise NotImplementedError(
            "La extracción de la afirmación verificable y su tipo llega con el "
            "ticket #22. Hasta entonces el orquestador usa el texto del tuit."
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
        cliente = self._cliente()
        configuracion = self._configuracion

        comenzo = time.perf_counter()
        try:
            respuesta = cliente.responses.parse(
                model=configuracion.modelo_llm,
                instructions=INSTRUCCIONES_VEREDICTO,
                input=_armar_entrada(afirmacion, fuentes),
                text_format=_SalidaVeredicto,
                max_output_tokens=configuracion.max_fichas_de_salida,
                reasoning={"effort": configuracion.esfuerzo_de_razonamiento},
            )
        except APITimeoutError as error:
            raise ErrorDelProveedor(
                "El proveedor no respondió dentro del tiempo límite de "
                f"{configuracion.tiempo_limite_proveedor_s:.0f} s."
            ) from error
        except (APIError, OpenAIError) as error:
            raise ErrorDelProveedor(
                f"El proveedor rechazó la llamada de veredicto: {error}"
            ) from error

        _registrar_consumo(respuesta, configuracion, time.perf_counter() - comenzo)

        salida = respuesta.output_parsed
        if salida is None:
            raise ErrorDelProveedor(
                "El proveedor no devolvió una salida que se ajuste al esquema "
                f"del veredicto (estado: {respuesta.status})."
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
    respuesta: object, configuracion: Configuracion, segundos: float
) -> None:
    """Deja en el registro la latencia y el costo reales de la llamada.

    Es lo que convierte el criterio de aceptación sobre latencia y costo en algo
    medido y no estimado: cada llamada real imprime sus propios números. No hay
    valores anotados de antemano en ningún lado, porque medir exige la
    credencial del usuario y una llamada verdadera.

    Prueba de humo, con la credencial ya cargada en `prototipo/servicio/.env`:

        cd prototipo/servicio
        ./.venv/bin/uvicorn app.main:aplicacion --port 8001 --log-level info
        curl -sS -X POST http://127.0.0.1:8001/analizar \\
          -H 'Content-Type: application/json' \\
          -d '{"tweet_id":"1","texto":"A partir del lunes cierran todas las escuelas de la Provincia.","handle":"@ejemplo"}'

    La línea `proveedor` del registro de uvicorn trae el modelo, los segundos,
    las fichas consumidas y el costo en dólares de esa llamada.
    """
    uso = getattr(respuesta, "usage", None)
    fichas_entrada = getattr(uso, "input_tokens", 0) or 0
    fichas_salida = getattr(uso, "output_tokens", 0) or 0
    costo = (
        fichas_entrada * configuracion.precio_entrada_por_millon
        + fichas_salida * configuracion.precio_salida_por_millon
    ) / 1_000_000

    registro.info(
        "proveedor | modelo=%s latencia=%.2fs fichas_entrada=%d "
        "fichas_salida=%d costo_usd=%.6f",
        configuracion.modelo_llm,
        segundos,
        fichas_entrada,
        fichas_salida,
        costo,
    )
