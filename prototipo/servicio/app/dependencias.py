"""El punto único de inyección del proveedor.

`obtener_proveedor` es la **única** función del servicio que nombra a un
proveedor concreto. Dos consecuencias buscadas:

- En la Entrega 4, sustituir el paso de clasificación por el clasificador propio
  ajustado es cambiar lo que esta función construye, en un solo lugar.
- En los tests, el proveedor se reemplaza por un doble con el mecanismo de
  sustitución de dependencias de FastAPI:

      from app.dependencias import obtener_proveedor
      from app.main import aplicacion

      aplicacion.dependency_overrides[obtener_proveedor] = lambda: doble
      ...
      aplicacion.dependency_overrides.clear()

  La clave del diccionario es esta función, no la clase del proveedor. El doble
  no hereda de nada: le alcanza con tener los tres métodos del `Protocol`.
"""

from __future__ import annotations

from functools import lru_cache

from .configuracion import Configuracion, obtener_configuracion
from .proveedor.clasificador import ClienteClasificador, ProveedorCompuesto
from .proveedor.openai import ProveedorOpenAI
from .proveedor.puerto import ProveedorDeAnalisis


@lru_cache
def obtener_proveedor() -> ProveedorDeAnalisis:
    """Devuelve el proveedor del proceso.

    Construir el adaptador no toca la red ni exige la credencial: el cliente de
    OpenAI se crea perezosamente en la primera llamada real. Por eso el servicio
    arranca sin `OPENAI_API_KEY` y la batería de pruebas corre sin ella.

    Con `ADAPTADOR=compuesto`, el puntaje del Módulo 1 sale del clasificador
    propio y el resto sigue en el LLM; ver `proveedor/clasificador.py`.
    """
    configuracion = obtener_configuracion()
    llm = ProveedorOpenAI(configuracion)
    if configuracion.adaptador == "llm":
        return llm
    return ProveedorCompuesto(llm, cliente_clasificador(configuracion))


def cliente_clasificador(configuracion: Configuracion) -> ClienteClasificador:
    return ClienteClasificador(
        configuracion.url_clasificador, configuracion.tiempo_limite_clasificador_s
    )
