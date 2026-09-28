"""El clasificador propio del Módulo 1 (ticket #32, *spec* #28).

Dos piezas:

- `ClienteClasificador`: habla con el servicio de inferencia (el Space de
  `prototipo/clasificador/space/`). Una sola operación, texto → `Clasificacion`.
- `ProveedorCompuesto`: implementa `ProveedorDeAnalisis` sin cambiarlo. La
  afirmación y el tipo salen del LLM; el puntaje, la clase y la versión del
  modelo, del clasificador. Evidencia y veredicto se delegan en el LLM.
"""

from __future__ import annotations

import asyncio
import http.client
import json
import logging
import urllib.request
from typing import Literal, Protocol

from pydantic import BaseModel, Field

from ..contrato import Fuente, Veredicto
from .puerto import (
    AfirmacionExtraida,
    ErrorDelProveedor,
    ProveedorDeAnalisis,
    VeredictoEmitido,
)

registro = logging.getLogger("app.proveedor.clasificador")


class Clasificacion(BaseModel):
    """Lo que devuelve el servicio de inferencia."""

    puntaje: float = Field(ge=0, le=1)
    """Probabilidad de la clase «falso»."""
    clase: Literal["verdadero", "falso"]
    version_modelo: str


class Clasificador(Protocol):
    def clasificar(self, texto: str) -> Clasificacion: ...


class ClienteClasificador:
    """Cliente HTTP del Space: `POST {url}/clasificar` con `{"texto": ...}`.

    Cualquier falla —sin dirección configurada, tiempo límite, error HTTP,
    respuesta mal formada o fuera de rango— sale como `ErrorDelProveedor`, que
    el orquestador ya convierte en análisis parcial (RNF-11).
    """

    def __init__(self, url: str, tiempo_limite_s: float) -> None:
        self.url = url.rstrip("/")
        self.tiempo_limite_s = tiempo_limite_s

    def clasificar(self, texto: str) -> Clasificacion:
        if not self.url:
            raise ErrorDelProveedor("clasificador | falta URL_CLASIFICADOR")
        pedido = urllib.request.Request(
            f"{self.url}/clasificar",
            data=json.dumps({"texto": texto}).encode(),
            headers={"Content-Type": "application/json"},
        )
        try:
            # ponytail: el tiempo límite de urllib es por operación de socket, no
            # total; alcanza para una respuesta de cien bytes.
            with urllib.request.urlopen(pedido, timeout=self.tiempo_limite_s) as respuesta:
                return Clasificacion.model_validate_json(respuesta.read())
        # OSError cubre URLError, HTTPError y el tiempo límite; ValueError, la
        # validación de pydantic.
        except (OSError, ValueError, http.client.HTTPException) as error:
            raise ErrorDelProveedor(f"clasificador | {error}") from error


class ProveedorCompuesto:
    """LLM para la afirmación, clasificador propio para el puntaje."""

    def __init__(self, llm: ProveedorDeAnalisis, clasificador: Clasificador) -> None:
        self.llm = llm
        self.clasificador = clasificador

    def extraer_afirmacion(self, texto: str) -> AfirmacionExtraida:
        # El clasificador va primero: si falla, no se gasta la llamada al LLM.
        # Puntúa el texto del tuit y no la afirmación reformulada, porque se
        # entrenó sobre publicaciones originales.
        clasificacion = self.clasificador.clasificar(texto)
        extraida = self.llm.extraer_afirmacion(texto)
        return extraida.model_copy(
            update={
                "puntaje": clasificacion.puntaje,
                "clase": clasificacion.clase,
                "version_modelo": clasificacion.version_modelo,
            }
        )

    def recuperar_evidencia(self, afirmacion: str) -> list[Fuente]:
        return self.llm.recuperar_evidencia(afirmacion)

    def emitir_veredicto(
        self, afirmacion: str, fuentes: list[Fuente], veredicto: Veredicto
    ) -> VeredictoEmitido:
        return self.llm.emitir_veredicto(afirmacion, fuentes, veredicto)


async def mantener_despierto(clasificador: Clasificador, intervalo_s: float) -> None:
    """Llama al Space cada `intervalo_s` segundos mientras el servicio vive.

    La primera llamada es inmediata: si el Space estaba dormido, empieza a
    despertarse al arrancar el servicio y no con el primer tuit. Una falla solo
    se registra; la llamada siguiente vuelve a intentar.
    """
    while True:
        try:
            await asyncio.to_thread(clasificador.clasificar, "despertar")
        except ErrorDelProveedor as error:
            registro.warning("clasificador | la llamada periódica falló: %s", error)
        await asyncio.sleep(intervalo_s)
