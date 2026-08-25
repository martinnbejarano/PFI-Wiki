"""Configuración del servicio.

Un único objeto de configuración reúne lo que RNF-16 exige que viva fuera del
código —el modelo concreto, las versiones que viajan en la respuesta por RF-16—
y la credencial del proveedor, que se lee del entorno del servicio y nunca del
repositorio.

La credencial se admite ausente. El servicio arranca sin ella y responde
`GET /salud`; recién falla, con un mensaje explícito, cuando se intenta una
llamada real al proveedor. Eso permite que la batería de pruebas corra sin red
y sin credencial, que es lo que la costura 1 de la *spec* exige.

Orden de precedencia, de mayor a menor: variables de entorno del proceso,
`prototipo/servicio/.env`, valores por defecto de esta clase.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

RAIZ_DEL_SERVICIO = Path(__file__).resolve().parent.parent


class Configuracion(BaseSettings):
    """Parámetros del servicio, resueltos del entorno y del archivo `.env`."""

    model_config = SettingsConfigDict(
        env_file=RAIZ_DEL_SERVICIO / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    openai_api_key: str | None = None
    """Credencial del proveedor. Ausente por defecto, a propósito."""

    # El modelo concreto queda fijado acá y no en el código del adaptador.
    #
    # Elección: `gpt-5.6-luna`. Es el escalón de menor costo de la familia
    # vigente ($0,20 por millón de fichas de entrada y $1,20 por millón de
    # salida, según la tabla de precios consultada el 2026-08-25) y admite tanto
    # la salida estructurada como la herramienta de búsqueda web que el ticket
    # de recuperación de evidencia va a necesitar. Un prototipo que resuelve un
    # tuit por clic no justifica el escalón `sol`, cuyo costo por millón de
    # fichas es veinte veces mayor.
    modelo_llm: str = "gpt-5.6-luna"

    # Precios de la tabla oficial, en dólares por millón de fichas. Viven en
    # configuración porque son lo que convierte el consumo medido en costo
    # medido: el adaptador registra ambos por llamada. Consultados el
    # 2026-08-25 en https://developers.openai.com/api/docs/pricing
    precio_entrada_por_millon: float = 0.20
    precio_salida_por_millon: float = 1.20

    max_fichas_de_salida: int = 900
    """Tope de fichas generadas por llamada; acota costo y latencia."""

    max_fichas_de_salida_busqueda: int = 2500
    """Tope propio del paso de recuperación de evidencia.

    Es más alto que el general porque ese paso hace algo que los otros dos no
    hacen: llama a la herramienta de búsqueda web, y tanto las consultas que
    formula como el contenido que lee del resultado se facturan y se cuentan
    contra este tope. Con el tope general la llamada se corta a mitad de camino,
    la salida no se ajusta al esquema y el paso termina en `ErrorDelProveedor`
    por una razón que no tiene nada que ver con la búsqueda."""

    contexto_de_busqueda: str = "low"
    """Cuánta ventana de contexto dedica la herramienta de búsqueda: `low`,
    `medium` o `high`. Se elige `low` por el presupuesto de ocho segundos de
    RNF-02: lo que se busca de cada resultado es el título y la dirección, no un
    resumen del artículo, y la postura de cada fuente —que sí exigiría leerlo—
    es del ticket #24."""

    esfuerzo_de_razonamiento: str = "low"
    """Esfuerzo de razonamiento del modelo: `none`, `minimal`, `low`, `medium`,
    `high`, `xhigh` o `max`. Se elige `low` porque el presupuesto de latencia de
    RNF-02 es de ocho segundos y las fichas de razonamiento se facturan como
    salida: el esfuerzo alto compra un juicio más fino a costa de las dos cosas
    que este prototipo tiene contadas."""

    tiempo_limite_proveedor_s: float = 30.0
    """Corte de la llamada al proveedor, por encima del presupuesto de RNF-02."""

    version_modelo: str = "openai:gpt-5.6-luna"
    """Identificador que viaja en la respuesta por RF-16."""

    version_configuracion_pesos: str = "pesos-v1"
    """Identificador de la configuración del combinador, también por RF-16."""


@lru_cache
def obtener_configuracion() -> Configuracion:
    """Devuelve la configuración del proceso.

    Está memorizada para que el archivo `.env` se lea una sola vez. En un test
    que necesite otra configuración se sustituye por dependencia, igual que el
    puerto del proveedor.
    """
    return Configuracion()
