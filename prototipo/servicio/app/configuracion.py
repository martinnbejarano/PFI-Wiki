"""Configuración del servicio.

Un único objeto de configuración reúne lo que RNF-16 exige que viva fuera del
código —el modelo concreto, **los pesos del combinador y los umbrales de los
tres niveles del veredicto**, y las versiones que viajan en la respuesta por
RF-16— y la credencial del proveedor, que se lee del entorno del servicio y
nunca del repositorio.

> RNF-16: «Los umbrales de los veredictos y los pesos del ensamblado deben ser
> configurables sin necesidad de volver a desplegar el servicio.»

Todo lo que el combinador usa para decidir está declarado en esta clase y en
ningún otro lugar: `app/combinador.py` recibe la configuración y no tiene un
solo número propio. Cambiar un peso es exportar una variable de entorno o
escribir una línea en `prototipo/servicio/.env` y reiniciar el proceso; no hay
que tocar código ni volver a desplegar nada. Los nombres de las variables de
entorno son los de los campos en mayúsculas: `PESO_CONTRASTE=0.9`,
`UMBRAL_INFORMACION_SOSPECHOSA=0.3`.

La credencial se admite ausente. El servicio arranca sin ella y responde
`GET /salud`; recién falla, con un mensaje explícito, cuando se intenta una
llamada real al proveedor. Eso permite que la batería de pruebas corra sin red
y sin credencial, que es lo que la costura 1 de la *spec* exige.

Orden de precedencia, de mayor a menor: argumentos del constructor —que es como
un test sustituye la configuración entera—, variables de entorno del proceso,
`prototipo/servicio/.env`, valores por defecto de esta clase.
"""

from __future__ import annotations

import hashlib
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

RAIZ_DEL_SERVICIO = Path(__file__).resolve().parent.parent

# Los campos que definen el comportamiento del combinador, en orden fijo.
#
# De acá sale la huella que identifica la configuración de pesos en uso, y por
# eso el orden importa y está escrito a mano en lugar de derivarse del recorrido
# de los campos del modelo: agregar un campo al final no cambia la huella de las
# configuraciones existentes, y renombrar uno sí la cambia, que es lo correcto.
#
# Quien agregue un peso o un umbral tiene que sumarlo a esta tupla. Si no lo
# hace, dos configuraciones que producen resultados distintos comparten versión,
# que es exactamente la falla que `version_configuracion_pesos` existe para
# evitar.
CAMPOS_DEL_COMBINADOR: tuple[str, ...] = (
    "peso_clasificador",
    "peso_credibilidad",
    "peso_contraste",
    "peso_fuente_oficial",
    "peso_medio_de_referencia",
    "peso_verificacion_previa",
    "umbral_contradicho_por_fuentes_oficiales",
    "umbral_informacion_sospechosa",
)


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

    contexto_de_busqueda: str = "medium"
    """Cuánta ventana de contexto dedica la herramienta de búsqueda: `low`,
    `medium` o `high`.

    **Subido de `low` a `medium` al implementar la postura por fuente.** El
    escalón `low` alcanzaba mientras de cada resultado solo se necesitaban el
    título y la dirección. Determinar si una fuente corrobora o contradice la
    afirmación exige otra cosa: leer lo suficiente del documento como para saber
    qué dice sobre ella. Con `low` el modelo tiene que decidir la postura
    mirando poco más que el título, y una postura decidida así es una etiqueta
    inventada con apariencia de análisis, que es peor que declararla neutral.

    **El costo de la decisión, que no se esconde.** El escalón `medium` mete más
    texto de cada resultado en la entrada de la llamada, así que sube tanto las
    fichas facturadas como la latencia del paso de recuperación de evidencia, y
    ese paso es el más caro y el más lento de los tres. El presupuesto de RNF-02
    son ocho segundos en el percentil 95 y esto lo estrecha. No se anota acá
    cuánto: medirlo exige la credencial y una llamada verdadera, y este
    repositorio no tiene ni un número de latencia ni uno de costo que no venga
    de una medición. El adaptador registra ambos por paso; la prueba manual que
    describe `prototipo/README.md` es la que los produce.

    Si la medición mostrara que `medium` rompe el presupuesto, la salida no es
    volver a `low` y seguir etiquetando posturas: es volver a `low` y volver a
    declarar todas las fuentes neutrales, que es lo honesto."""

    esfuerzo_de_razonamiento: str = "low"
    """Esfuerzo de razonamiento del modelo: `none`, `minimal`, `low`, `medium`,
    `high`, `xhigh` o `max`. Se elige `low` porque el presupuesto de latencia de
    RNF-02 es de ocho segundos y las fichas de razonamiento se facturan como
    salida: el esfuerzo alto compra un juicio más fino a costa de las dos cosas
    que este prototipo tiene contadas."""

    tiempo_limite_proveedor_s: float = 30.0
    """Corte de **una** llamada al proveedor. El análisis hace tres."""

    tiempo_limite_total_s: float = 45.0
    """Presupuesto del análisis entero, y el número que manda.

    El servicio es quien tiene que hacer cumplir el plazo, porque es el único
    que sabe cuánto lleva gastado. Entre paso y paso se comprueba lo consumido:
    si el presupuesto se agotó, los pasos que faltan se declaran ausentes y la
    respuesta sale como análisis parcial (RNF-11) en lugar de seguir corriendo
    mientras el ciudadano mira girar un indicador.

    **Los plazos de la extensión tienen que ser más holgados que este**, para
    que en toda demora normal gane la degradación declarada del servicio y no
    un corte del cliente, que no puede explicar qué pasó. Ver
    `extension/src/service-worker/index.ts`.

    Medición real del 2026-08-28 sobre una afirmación de dato económico, con
    los tres pasos y seis fuentes recuperadas: **20,2 s de extremo a extremo**.
    Está por encima de los ocho segundos que RNF-02 fija para el flujo a
    demanda; la *spec* del prototipo ya anticipaba que un modelo de lenguaje con
    búsqueda web no entra en ese presupuesto, y es el argumento de por qué el
    clasificador propio de la Entrega 4 no es opcional."""

    version_modelo: str = "openai:gpt-5.6-luna"
    """Identificador que viaja en la respuesta por RF-16."""

    # -- Módulo 4: pesos del combinador (RNF-16) ---------------------------
    #
    # Los tres puntajes parciales se combinan en un promedio ponderado. Los
    # pesos no tienen que sumar uno: el combinador normaliza por su suma, así
    # que subir un peso baja la influencia relativa de los otros dos sin que
    # nadie tenga que recalcular nada a mano. Es lo que hace que la demostración
    # pueda mover un solo número en vivo y mostrar cómo se mueve el resultado.
    #
    # La justificación de cada valor está en `app/combinador.py`, junto a la
    # fórmula que los usa.

    peso_clasificador: float = 0.35
    """Cuánto pesa el análisis del texto (Módulo 1) en el puntaje final."""

    peso_credibilidad: float = 0.0
    """Cuánto pesa el puntaje de credibilidad de la cuenta (Módulo 2).

    **Cero, a propósito.** El Módulo 2 está recortado: `app/credibilidad.py`
    devuelve un valor arbitrario derivado de un resumen del *handle* y viaja
    marcado con `no_implementado`. Ponderarlo con cualquier peso mayor que cero
    metería un número inventado dentro del puntaje final, y el puntaje final es
    lo que la interfaz muestra como probabilidad estimada de desinformación.

    El peso existe como campo —y no está borrado del combinador— porque el
    módulo real llega con el sistema completo y ese día lo único que hay que
    cambiar es este valor. Mientras tanto, cero es lo que hace que el desglose
    de la interfaz pueda seguir mostrando el valor marcado sin que contamine el
    resultado."""

    peso_contraste: float = 0.65
    """Cuánto pesa el contraste con evidencia externa (Módulo 3)."""

    # -- Módulo 4: pesos de la jerarquía de evidencia (RNF-16) -------------
    #
    # Cuánto vale la postura de una fuente según su escalón. El orden entre los
    # tres lo fija `app/jerarquia.py` y estos valores tienen que respetarlo:
    # oficial por encima de medio de referencia, y medio de referencia por
    # encima de verificación previa.

    peso_fuente_oficial: float = 1.0
    """Peso de la postura de una fuente oficial en el puntaje de contraste."""

    peso_medio_de_referencia: float = 0.6
    """Peso de la postura de un medio de referencia."""

    peso_verificacion_previa: float = 0.4
    """Peso de la postura de una verificación previa."""

    # -- Módulo 4: umbrales de los tres niveles (RNF-16) -------------------
    #
    # Los cortes que traducen el puntaje final en uno de los tres niveles de
    # RF-06. Se leen de mayor a menor: por encima del primero, el nivel severo;
    # por encima del segundo, información sospechosa; por debajo, parece
    # verificado.

    umbral_contradicho_por_fuentes_oficiales: float = 0.70
    """Desde este puntaje, el veredicto es el nivel severo de RF-06."""

    umbral_informacion_sospechosa: float = 0.40
    """Desde este puntaje, el veredicto es *información sospechosa*."""

    etiqueta_configuracion_pesos: str = "pesos-v1"
    """Nombre legible del juego de pesos y umbrales en uso.

    Es la mitad que una persona elige. La otra mitad —la que no se puede
    falsear— la calcula `version_configuracion_pesos` a partir de los valores
    reales."""

    @property
    def version_configuracion_pesos(self) -> str:
        """Identificador de la configuración del combinador en uso (RF-16).

        **Por qué es una propiedad calculada y no un campo que se escribe.**
        RF-16 pide asociar cada análisis a la configuración de pesos que lo
        produjo, para poder reproducir un resultado meses después. Una cadena
        fija cumple la letra del requerimiento y no su intención: si alguien
        cambia un peso y se olvida de subir la etiqueta —que es lo que va a
        pasar, porque son dos acciones y solo una es la que le interesa—, dos
        análisis con veredictos distintos quedan asociados a la misma versión y
        la trazabilidad que RF-16 pide deja de existir sin que nadie se entere.

        Acá la versión **se deriva de los valores**, así que no puede quedar
        desactualizada: cambiar cualquier peso o cualquier umbral cambia la
        versión en la respuesta, y no cambiar nada la deja igual. La forma es
        `etiqueta+huella`, por ejemplo `pesos-v1+3f2a1b9c`: la etiqueta es el
        nombre que una persona le puso al juego de valores y la huella son los
        primeros ocho caracteres del resumen SHA-256 de los campos que enumera
        `CAMPOS_DEL_COMBINADOR`, en ese orden.

        La huella identifica, no reconstruye: de `3f2a1b9c` no se vuelve a los
        pesos. Reconstruirlos es tarea de la persistencia que RF-16 pide y que
        este prototipo declaró fuera de alcance. Lo que sí garantiza es que dos
        análisis con la misma versión se produjeron con los mismos valores.

        Se usa SHA-256 y no `hash()` por lo mismo que `credibilidad.py`: la
        función `hash()` de Python aleatoriza su semilla por proceso, así que la
        misma configuración daría versiones distintas entre dos arranques del
        servicio.
        """
        valores = ";".join(
            f"{campo}={getattr(self, campo)!r}" for campo in CAMPOS_DEL_COMBINADOR
        )
        huella = hashlib.sha256(valores.encode("utf-8")).hexdigest()[:8]
        return f"{self.etiqueta_configuracion_pesos}+{huella}"


@lru_cache
def obtener_configuracion() -> Configuracion:
    """Devuelve la configuración del proceso.

    Está memorizada para que el archivo `.env` se lea una sola vez.

    **Cómo se sustituye en un test.** Es una dependencia de FastAPI, resuelta
    con `Depends` en el borde de red igual que el puerto del proveedor, así que
    se reemplaza por el mismo mecanismo y sin tocar variables de entorno del
    proceso:

        aplicacion.dependency_overrides[obtener_configuracion] = (
            lambda: Configuracion(peso_contraste=0.9)
        )

    Los argumentos del constructor tienen precedencia sobre el entorno y sobre
    `.env`, así que una configuración armada así es exactamente la que el test
    escribe. `tests/conftest.py` lo envuelve en `construir_cliente`.
    """
    return Configuracion()
