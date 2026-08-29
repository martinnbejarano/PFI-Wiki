"""Orquestador del análisis.

Encadena los pasos del *pipeline* y arma la `RespuestaAnalisis` del contrato.
Es el único lugar que conoce el orden de los pasos; el punto de entrada HTTP
solo lo llama, y el adaptador del proveedor no sabe que existe.

Ningún test toca este módulo directamente. Se ejercita entero por
`POST /analizar`, que es la costura que la *spec* fija para el servicio: si un
test se rompiera al reemplazar un paso, estaría probando implementación.

Qué está implementado en esta instancia y qué no:

- **Paso de extracción de la afirmación (RF-04).** Real. Sale de una llamada al
  proveedor, que en esta instancia resuelve la clasificación del texto en
  *zero-shot*: es la línea base de LLM que el protocolo de validación del
  capítulo 4 compromete como Módulo 1. En la Entrega 4 se sustituye por el
  clasificador propio ajustado escribiendo otro adaptador del mismo puerto, sin
  que este archivo cambie.
- **Paso de recuperación de evidencia (RF-05).** Real. Sale de una búsqueda web
  restringida a la jerarquía de evidencia, y lo que vuelve pasa por el filtro
  propio de `jerarquia.py` antes de llegar al combinador. Cada fuente vuelve con
  su postura respecto de la afirmación. Cuando no vuelve ninguna fuente
  admisible, `fuentes` queda vacía y el veredicto se emite en el estado *sin
  contraste externo*, que es lo que RF-06 y RNF-06 exigen en ese caso.
- **Combinador ponderado (Módulo 4).** Real. `combinador.py` agrega la postura
  de las fuentes en el puntaje de contraste, pondera los tres puntajes parciales
  en el puntaje final y lo traduce en uno de los tres niveles de RF-06. Los
  pesos y los umbrales viven en la configuración por RNF-16.
- **Paso de veredicto (RF-06).** Real. Sale de una llamada al proveedor, que
  **recibe el nivel ya decidido** y redacta la justificación que lo explica.
- **Módulo de credibilidad de la cuenta (Módulo 2).** Recortado a propósito:
  `credibilidad.py` devuelve un valor arbitrario derivado del *handle*. Viaja
  marcado con `no_implementado` para que la interfaz no lo presente como una
  medición, y **pesa cero en el combinador** para que un número inventado no
  entre en el puntaje final.


El orden de los pasos, y por qué es este
----------------------------------------

Extraer la afirmación, recuperar la evidencia con su postura, combinar, y recién
entonces pedir la justificación. El paso que redacta va último y no primero
porque el veredicto que explica ya está decidido: es lo que evita que la
respuesta muestre un nivel y un texto que dicen cosas distintas.


Cómo se hace valer RNF-07, y hasta dónde
----------------------------------------

> RNF-07: «El resultado debe enunciarse sobre la afirmación analizada y nunca
> sobre la persona que la publicó, y el nivel severo debe atribuir el juicio a
> la fuente que lo sostiene en lugar de afirmarlo el sistema por su cuenta.»

Tres cosas lo sostienen, en orden de solidez:

1. **La identidad de la cuenta autora no llega a ningún paso que produzca
   texto.** `extraer_afirmacion` recibe el texto de la publicación y
   `emitir_veredicto` recibe la afirmación, las fuentes y el veredicto. El
   *handle* solo se usa como semilla del Módulo 2 recortado. El texto que
   justifica el resultado se escribe, literalmente, sin saber quién publicó: no
   es una instrucción que el modelo pueda desobedecer sino algo que no tiene con
   qué hacer. Es lo que se comprueba desde afuera en la batería de pruebas.
2. **El nivel severo exige una fuente oficial que contradiga.** Es la segunda
   mitad del requerimiento y es una invariante verificable. Ver
   `_veredicto_admisible`.
3. **Las instrucciones se lo exigen al modelo**, en `proveedor/openai.py`.

**Lo que no se hace, y por qué.** No hay ninguna comprobación automática de que
la justificación no hable de la persona. Un filtro por palabras clave —buscar el
*handle*, buscar «el autor», «esta cuenta»— se burla con cualquier perífrasis y
daría por limpio un texto que señala a alguien sin nombrarlo. Un chequeo que se
puede burlar es peor que ninguno, porque produce la falsa seguridad de que el
requerimiento está cubierto. Lo que cubre el caso es (1): quitarle al paso el
dato con el cual podría señalar. Para la parte que queda —una justificación que
hable de «quien publicó esto» en abstracto— este prototipo no tiene garantía
automática, y la mitigación es la revisión de las capturas de la demostración.


Degradación: qué paso admite seguir sin él y cuál no (RNF-11)
-------------------------------------------------------------

> RNF-11: «Ante la indisponibilidad del servicio de inferencia o de la API de
> búsqueda, el sistema debe devolver un análisis parcial identificado como tal,
> nunca un error opaco ni un veredicto construido sobre módulos faltantes.»

Los tres pasos hablan con el proveedor y los tres pueden fallar, pero **no son
degradables por igual**. La regla que decide es una sola: un paso es degradable
cuando lo que produce se puede reemplazar por su ausencia declarada sin que el
resto del análisis pase a apoyarse en nada.

1. **Extracción de la afirmación (RF-04) — no es degradable.** Es la entrada de
   todo lo demás: sin la afirmación no hay nada que buscar y nada sobre lo cual
   pronunciarse. Seguir sería inventar la afirmación, o buscar evidencia sobre
   el texto crudo del tuit, que es exactamente lo que RF-04 existe para separar.
   El análisis se corta acá.

   **Cortar no es devolver un error.** Lo que sale es una respuesta completa y
   válida del contrato, con código 200, con la afirmación vacía, con el estado
   *sin contraste externo*, sin puntaje calculado sobre nada y con los tres
   módulos listados como ausentes. La interfaz la puede dibujar entera; el
   ciudadano ve qué falló y puede reintentar. Ver `_respuesta_sin_extraccion`.

2. **Recuperación de evidencia (RF-05) — degradable, y es el caso interesante.**
   El análisis sigue sin contraste: `fuentes` queda vacía, el puntaje de
   contraste queda en cero y, por la invariante de RNF-06 que
   `_veredicto_admisible` ya hacía valer, el veredicto cae solo en *sin
   contraste externo* cualquiera sea el puntaje. Nada hay que agregar para que
   el veredicto no se construya sobre el módulo faltante: la invariante que ya
   existía lo impide.

3. **Redacción de la justificación (RF-06) — degradable.** Es el único de los
   tres que no aporta nada a la decisión: el nivel del veredicto ya lo produjo
   el combinador, que es código propio y no falla con el proveedor. Lo que se
   pierde es el texto que lo explica, y se reemplaza por uno fijo que dice que
   no se pudo redactar. El veredicto, los puntajes y las fuentes sobreviven
   intactos porque se calcularon antes y sin este paso.

En los tres casos la bandera de RNF-11 viaja con **los nombres legibles** de los
módulos que no se ejecutaron, no con identificadores internos: esa lista la
muestra la interfaz y va a aparecer en una captura de la demostración.

**Cuál falló se sabe por el lugar de la llamada y no leyendo el mensaje del
error.** Cada `try` envuelve un solo paso, así que el nombre del módulo ausente
sale de la rama que lo atrapó. El mensaje del `ErrorDelProveedor` trae también
la etiqueta del paso —`proveedor/openai.py` se la pone—, pero eso es para el
registro y para quien depura: hacer depender la respuesta de analizar una
cadena en castellano ataría el contrato a la redacción de un mensaje de error.
"""

from __future__ import annotations

import logging
import time

from .cache import CacheDeAnalisis
from .combinador import nivel_de_veredicto, puntaje_combinado, puntaje_de_contraste
from .configuracion import Configuracion
from .contrato import (
    AnalisisParcial,
    Fuente,
    PedidoAnalisis,
    Postura,
    PuntajeClasificador,
    PuntajeContraste,
    PuntajeCredibilidad,
    Puntajes,
    Razon,
    RespuestaAnalisis,
    TipoAfirmacion,
    TipoFuente,
    Veredicto,
)
from .credibilidad import puntaje_de_credibilidad
from .jerarquia import filtrar_por_jerarquia
from .proveedor.puerto import (
    AfirmacionExtraida,
    ErrorDelProveedor,
    ProveedorDeAnalisis,
)

registro = logging.getLogger("app.pipeline")

# El módulo de contraste no aportó nada porque no se ejecutó: no hay fuentes que
# corroboren ni que contradigan. Se emite 0,0 y no el punto medio de la escala.
#
# El razonamiento: el puntaje de contraste es lo que el módulo 3 aporta al
# combinador. Un 0,5 no significaría "no se sabe", significaría "se buscó, se
# encontró evidencia y quedó en equilibrio", que es una afirmación sobre el
# mundo que nadie hizo. Un 0,0 significa aporte nulo, que es literalmente lo que
# pasó. El riesgo de que se lea como "la evidencia lo respalda" está cubierto
# por RNF-06: con `fuentes` vacía el veredicto es `sin_contraste_externo` y la
# interfaz lo muestra sin porcentaje, así que el número nunca se presenta como
# un juicio sobre la afirmación.
PUNTAJE_CONTRASTE_SIN_EVIDENCIA = 0.0

# Qué se responde cuando la publicación no contiene ninguna afirmación
# verificable. Ver `_respuesta_sin_afirmacion` para la decisión completa.
JUSTIFICACION_SIN_AFIRMACION = (
    "La publicación no enuncia ningún hecho que pueda contrastarse contra una "
    "fuente, así que no hay nada que verificar en ella. El sistema no emite un "
    "veredicto: una opinión, una pregunta o una broma no son ni verdaderas ni "
    "falsas, y tratarlas como si lo fueran sería el error más grosero que esta "
    "herramienta puede cometer."
)
RAZON_SIN_AFIRMACION = (
    "No se identificó en el texto ninguna afirmación verificable que se pueda "
    "contrastar contra una fuente externa."
)

# Los nombres de los módulos que la respuesta lista cuando alguno no se ejecutó
# (RNF-11). Son **texto legible**, y no identificadores internos, porque la
# interfaz los muestra tal cual: aparecen en el aviso del detalle y en la nota
# del indicador, y van a quedar impresos en una captura de la demostración.
# Nombran lo que el ciudadano perdió —el contraste, la explicación— y no la
# función de Python que no llegó a correr.
MODULO_EXTRACCION = "la extracción de la afirmación verificable"
MODULO_CONTRASTE = "el contraste con evidencia externa"
MODULO_REDACCION = "la redacción de la justificación"

# Qué se responde cuando el paso de extracción falla y el análisis no puede
# empezar. Ver `_respuesta_sin_extraccion`.
JUSTIFICACION_SIN_EXTRACCION = (
    "El análisis no pudo completarse: el servicio de inferencia no respondió, "
    "así que no se llegó a identificar qué afirmación verificable contiene la "
    "publicación ni a contrastarla contra ninguna fuente. Lo que se muestra no "
    "es un veredicto sobre la publicación, es el aviso de que el sistema no "
    "pudo pronunciarse. Volvé a pedir el análisis en unos instantes."
)
RAZON_SIN_EXTRACCION = (
    "Ningún módulo del análisis llegó a ejecutarse, así que no hay ninguna "
    "señal sobre la cual apoyar un resultado."
)

# Qué se responde cuando el paso que redacta falla. El veredicto, los puntajes y
# las fuentes ya estaban decididos; lo único que falta es el texto.
JUSTIFICACION_SIN_REDACCION = (
    "El veredicto y su desglose se calcularon con normalidad, pero el servicio "
    "de inferencia no respondió cuando se le pidió redactar la explicación en "
    "lenguaje natural. El resultado y las fuentes que lo sostienen están abajo "
    "y se pueden leer por cuenta propia."
)
RAZON_SIN_REDACCION = (
    "No se pudo redactar la explicación del veredicto; las fuentes recuperadas "
    "y su postura quedan a la vista para poder juzgarlas sin ella."
)


def analizar_tuit(
    pedido: PedidoAnalisis,
    proveedor: ProveedorDeAnalisis,
    configuracion: Configuracion,
    cache: CacheDeAnalisis,
) -> RespuestaAnalisis:
    """Resuelve el análisis de un tuit, reusando el previo si lo hay (RF-07).

    La caché se consulta y se escribe **acá**, alrededor del análisis entero, y
    no dentro de ninguno de los pasos: reutilizar un análisis previo es una
    decisión sobre el resultado completo y no sobre una llamada suelta. Cuando
    hay acierto no se toca el proveedor, que es lo que RF-07 pide y lo que la
    batería comprueba contando las invocaciones del doble.

    Un análisis parcial no llega a guardarse; la regla vive en `cache.py`, junto
    con el porqué.
    """
    guardado = cache.obtener(pedido.tweet_id, configuracion)
    if guardado is not None:
        return guardado

    analisis = _analizar(pedido, proveedor, configuracion)
    cache.guardar(analisis, configuracion)
    return analisis


def _analizar(
    pedido: PedidoAnalisis,
    proveedor: ProveedorDeAnalisis,
    configuracion: Configuracion,
) -> RespuestaAnalisis:
    """Ejecuta el análisis completo de un tuit y arma la respuesta del contrato.

    Cada llamada al proveedor va envuelta por separado, de modo que una falla se
    traduzca en la ausencia declarada de **ese** módulo y no en un error opaco
    (RNF-11). El apartado «Degradación» del encabezado explica cuál de los tres
    pasos admite seguir sin él y cuál no.
    """
    comenzado = time.monotonic()

    try:
        extraida = proveedor.extraer_afirmacion(pedido.texto.strip())
    except ErrorDelProveedor as error:
        # No es degradable: sin la afirmación no hay nada que buscar ni sobre
        # qué pronunciarse. Se corta, pero se responde algo que la interfaz
        # pueda dibujar entero.
        registro.warning("degradación | falló %s: %s", MODULO_EXTRACCION, error)
        return _respuesta_sin_extraccion(pedido, configuracion)

    if not extraida.hay_afirmacion_verificable:
        return _respuesta_sin_afirmacion(pedido, extraida, configuracion)

    modulos_ausentes: list[str] = []

    try:
        _verificar_presupuesto(comenzado, configuracion, MODULO_CONTRASTE)
        fuentes: list[Fuente] = _recuperar_evidencia(extraida.afirmacion, proveedor)
    except ErrorDelProveedor as error:
        # Degradable: el análisis sigue sin contraste. La invariante de RNF-06
        # que aplica `_veredicto_admisible` hace el resto —sin fuentes el
        # veredicto cae en *sin contraste externo*, cualquiera sea el puntaje—,
        # así que el resultado no puede construirse sobre el módulo faltante.
        registro.warning("degradación | falló %s: %s", MODULO_CONTRASTE, error)
        fuentes = []
        modulos_ausentes.append(MODULO_CONTRASTE)

    # El puntaje de contraste se deriva de la postura agregada de las fuentes,
    # así que se calcula después de recuperarlas y no antes.
    puntajes = _puntajes(
        extraida,
        pedido.handle,
        puntaje_de_contraste(fuentes, configuracion) if fuentes
        else PUNTAJE_CONTRASTE_SIN_EVIDENCIA,
    )
    final = puntaje_combinado(puntajes, configuracion)
    veredicto = _veredicto_admisible(
        nivel_de_veredicto(final, configuracion), fuentes
    )

    # El paso que redacta va último y recibe el veredicto ya decidido: explica
    # el resultado en lugar de producirlo. Que vaya último es también lo que lo
    # vuelve el más barato de perder: cuando falla, ya no queda nada que
    # dependa de él.
    try:
        _verificar_presupuesto(comenzado, configuracion, MODULO_REDACCION)
        emitido = proveedor.emitir_veredicto(extraida.afirmacion, fuentes, veredicto)
        justificacion = emitido.justificacion
        razones = _razones_admisibles(emitido.razones, fuentes)
    except ErrorDelProveedor as error:
        registro.warning("degradación | falló %s: %s", MODULO_REDACCION, error)
        modulos_ausentes.append(MODULO_REDACCION)
        justificacion = JUSTIFICACION_SIN_REDACCION
        razones = [Razon(texto=RAZON_SIN_REDACCION, fuente_url=None)]

    return _armar_respuesta(
        pedido=pedido,
        extraida=extraida,
        puntajes=puntajes,
        puntaje_final=final,
        veredicto=veredicto,
        justificacion=justificacion,
        razones=razones,
        fuentes=fuentes,
        configuracion=configuracion,
        modulos_ausentes=modulos_ausentes,
    )


def _verificar_presupuesto(
    comenzado: float,
    configuracion: Configuracion,
    modulo: str,
) -> None:
    """Falla si el análisis ya gastó su presupuesto de tiempo.

    Se levanta `ErrorDelProveedor` a propósito, y no una excepción nueva: el
    paso que sigue ya sabe degradarse ante ella, así que agotar el presupuesto y
    que el proveedor no conteste se tratan igual —ambos son «este módulo no se
    pudo ejecutar»— y el ciudadano recibe la misma respuesta declarada.

    La comprobación va **entre** pasos y no dentro de uno: interrumpir una
    llamada en curso exigiría meter el plazo en la frontera del puerto, que es
    justamente la pieza que la Entrega 4 sustituye y que conviene no ensuciar.
    Cada llamada ya tiene su propio corte por `tiempo_limite_proveedor_s`.
    """
    consumido = time.monotonic() - comenzado
    if consumido >= configuracion.tiempo_limite_total_s:
        raise ErrorDelProveedor(
            f"el análisis consumió {consumido:.1f} s, por encima del "
            f"presupuesto de {configuracion.tiempo_limite_total_s:.0f} s, "
            f"así que no se ejecutó {modulo}"
        )


def _puntajes(
    extraida: AfirmacionExtraida, handle: str, valor_contraste: float
) -> Puntajes:
    """Arma los tres puntajes parciales que el combinador recibe."""
    return Puntajes(
        # El puntaje del clasificador sale del paso de extracción, que en esta
        # instancia es la línea base de LLM en *zero-shot* del Módulo 1.
        clasificador=PuntajeClasificador(valor=extraida.puntaje, clase=extraida.clase),
        # El Módulo 2 está recortado y el valor es arbitrario: por eso viaja
        # siempre marcado y por eso pesa cero en el combinador. Ver
        # `credibilidad.py` para la decisión y para por qué no se lo alimenta
        # con `pedido.verificada` ni con `pedido.metricas`.
        credibilidad=PuntajeCredibilidad(
            valor=puntaje_de_credibilidad(handle), no_implementado=True
        ),
        contraste=PuntajeContraste(valor=valor_contraste),
    )


def _respuesta_sin_afirmacion(
    pedido: PedidoAnalisis,
    extraida: AfirmacionExtraida,
    configuracion: Configuracion,
) -> RespuestaAnalisis:
    """Responde a una publicación sin ninguna afirmación verificable.

    **La decisión.** El *pipeline* se corta acá: no se busca evidencia y no se
    pide veredicto. Se devuelve una respuesta completa y válida —código 200, no
    un error— con `afirmacion` vacía, el estado *sin contraste externo* y una
    justificación que dice por qué no hay nada que verificar.

    Tres razones, en orden de peso:

    1. **Es lo honesto.** Una opinión, una broma o un saludo no son ni
       verdaderos ni falsos. Emitir un veredicto sobre ellos —aunque fuera
       *parece verificado*— es el error más caro que esta herramienta puede
       cometer: convierte una diferencia de opinión en un señalamiento con
       apariencia de medición. El apartado ético del proyecto se apoya en no
       hacer exactamente esto.
    2. **No es una falla.** No se marca como análisis parcial. `analisis_parcial`
       significa que un módulo no pudo ejecutarse (RNF-11); acá todos se
       ejecutaron y el resultado es que no había nada que contrastar. Confundir
       ambas cosas le sacaría sentido a la única bandera que avisa cuando el
       sistema está degradado.
    3. **No se gasta una llamada.** El paso de veredicto es la llamada más cara
       del análisis y no tendría entrada sobre la cual pronunciarse.

    La ausencia se representa con `afirmacion` vacía y no con el texto crudo del
    tuit. Es lo que permite a la interfaz decir «no se identificó ninguna
    afirmación verificable» en lugar de mostrar el tuit como si fuera la
    afirmación analizada, que es justamente la confusión que RF-04 existe para
    evitar.
    """
    puntajes = _puntajes(extraida, pedido.handle, PUNTAJE_CONTRASTE_SIN_EVIDENCIA)
    return _armar_respuesta(
        pedido=pedido,
        extraida=extraida,
        puntajes=puntajes,
        # El puntaje final se calcula igual, con el mismo combinador y los
        # mismos pesos que en cualquier otro análisis. No hay una fórmula
        # especial para este caso: lo que hay es un veredicto que no depende del
        # puntaje, porque no hubo nada que contrastar.
        puntaje_final=puntaje_combinado(puntajes, configuracion),
        veredicto=Veredicto.SIN_CONTRASTE_EXTERNO,
        justificacion=JUSTIFICACION_SIN_AFIRMACION,
        razones=[Razon(texto=RAZON_SIN_AFIRMACION, fuente_url=None)],
        fuentes=[],
        configuracion=configuracion,
        modulos_ausentes=[],
    )


def _respuesta_sin_extraccion(
    pedido: PedidoAnalisis, configuracion: Configuracion
) -> RespuestaAnalisis:
    """Responde cuando el paso de extracción falló y el análisis no pudo empezar.

    **Por qué este paso no se degrada como los otros dos.** La afirmación
    verificable es la entrada de todo lo que sigue. Sin ella no hay qué buscar
    ni sobre qué pronunciarse, y las dos formas de seguir igual son peores que
    detenerse: inventar una afirmación, o usar el texto crudo del tuit como si
    lo fuera —que es justamente la confusión que RF-04 existe para eliminar—.

    **Detenerse no es devolver un error.** RNF-11 prohíbe el error opaco, no el
    resultado vacío. Lo que sale de acá es una respuesta completa del contrato,
    con código 200, que la interfaz dibuja igual que cualquier otra: afirmación
    vacía, estado *sin contraste externo*, y la bandera de análisis parcial con
    los tres módulos listados, porque ninguno llegó a ejecutarse.

    **El puntaje final es cero y no sale del combinador.** Ponderar tres
    puntajes que nadie produjo daría una cifra con apariencia de medición
    calculada sobre la nada, que es lo que RNF-11 llama «un veredicto construido
    sobre módulos faltantes». Cero acompaña al estado *sin contraste externo*,
    que la interfaz muestra sin porcentaje: el número no llega a presentarse
    como un juicio. Que no pase por el combinador tiene además una consecuencia
    buscada: ningún cambio de pesos puede hacer que un análisis fallido devuelva
    una cifra distinta de cero.

    El puntaje de credibilidad se calcula igual porque no depende del proveedor
    —sale del *handle*, en el proceso— y viaja marcado como siempre. El Módulo 2
    no está entre los ausentes: no es que no se ejecutó, es que no mide, que es
    otra cosa y ya se declara con `no_implementado`.
    """
    return _armar_respuesta(
        pedido=pedido,
        extraida=AfirmacionExtraida(
            afirmacion="",
            tipo=TipoAfirmacion.OTRO,
            puntaje=0.0,
            clase="sin_verificar",
        ),
        puntajes=Puntajes(
            clasificador=PuntajeClasificador(valor=0.0, clase="sin_verificar"),
            credibilidad=PuntajeCredibilidad(
                valor=puntaje_de_credibilidad(pedido.handle), no_implementado=True
            ),
            contraste=PuntajeContraste(valor=PUNTAJE_CONTRASTE_SIN_EVIDENCIA),
        ),
        puntaje_final=0.0,
        veredicto=Veredicto.SIN_CONTRASTE_EXTERNO,
        justificacion=JUSTIFICACION_SIN_EXTRACCION,
        razones=[Razon(texto=RAZON_SIN_EXTRACCION, fuente_url=None)],
        fuentes=[],
        configuracion=configuracion,
        modulos_ausentes=[MODULO_EXTRACCION, MODULO_CONTRASTE, MODULO_REDACCION],
    )


def _armar_respuesta(
    *,
    pedido: PedidoAnalisis,
    extraida: AfirmacionExtraida,
    puntajes: Puntajes,
    puntaje_final: float,
    veredicto: Veredicto,
    justificacion: str,
    razones: list[Razon],
    fuentes: list[Fuente],
    configuracion: Configuracion,
    modulos_ausentes: list[str],
) -> RespuestaAnalisis:
    """Arma la `RespuestaAnalisis` del contrato con lo que produjeron los pasos.

    `es_parcial` **se deriva** de la lista de módulos ausentes en lugar de
    recibirse aparte. Son dos formas de decir lo mismo, y dos campos que dicen
    lo mismo terminan tarde o temprano diciendo cosas distintas: una respuesta
    marcada como parcial sin listar qué falta, o una lista de módulos ausentes
    en un análisis que se presenta como completo. Con la bandera derivada, ese
    estado no se puede representar.
    """
    return RespuestaAnalisis(
        tweet_id=pedido.tweet_id,
        afirmacion=extraida.afirmacion,
        tipo_afirmacion=extraida.tipo,
        puntajes=puntajes,
        puntaje_final=puntaje_final,
        veredicto=veredicto,
        justificacion=justificacion,
        razones=razones,
        fuentes=fuentes,
        analisis_parcial=AnalisisParcial(
            es_parcial=bool(modulos_ausentes),
            modulos_ausentes=list(modulos_ausentes),
        ),
        version_modelo=configuracion.version_modelo,
        version_configuracion_pesos=configuracion.version_configuracion_pesos,
    )


def _recuperar_evidencia(
    afirmacion: str, proveedor: ProveedorDeAnalisis
) -> list[Fuente]:
    """Recupera la evidencia externa y le hace valer la jerarquía (RF-05).

    **Por qué el filtro corre acá y no solo dentro del adaptador.** La
    restricción a los medios de referencia y a las fuentes oficiales es una
    invariante del servicio, exactamente como la regla de `_veredicto_admisible`:
    vale sea cual sea el proveedor que esté detrás. Aplicarla en el orquestador
    significa que ningún adaptador futuro —el clasificador propio de la Entrega
    4, otro proveedor de búsqueda, un índice vectorial local— puede meter en la
    respuesta una fuente de fuera de la jerarquía por olvidarse de filtrar. El
    adaptador de OpenAI además declara el filtro de dominios de su propia
    herramienta de búsqueda, que es otra capa y no la misma.

    Es también lo que vuelve verificable el filtro sin conocer el interior del
    servicio: un doble que devuelva URLs de fuera de la jerarquía produce una
    respuesta HTTP donde esas fuentes no están.
    """
    return filtrar_por_jerarquia(proveedor.recuperar_evidencia(afirmacion))


def _veredicto_admisible(veredicto: Veredicto, fuentes: list[Fuente]) -> Veredicto:
    """Aplica sobre el nivel del combinador las dos invariantes del servicio.

    **RNF-06 — sin evidencia no hay veredicto.** Sin ninguna fuente enlazable,
    el único resultado admisible es *sin contraste externo*, cualquiera sea el
    puntaje que el combinador haya producido. Es la invariante más importante
    del servicio y por eso se hace valer acá y no en la fórmula: un cambio de
    pesos o de umbrales no puede alcanzarla.

    **RNF-07 — el nivel severo atribuye el juicio a quien lo sostiene.** El
    nombre del nivel dice quién contradice la afirmación: *contradicho por
    fuentes oficiales*. Emitirlo sin que ninguna fuente oficial la contradiga
    sería atribuirle a un organismo un juicio que no emitió, que es exactamente
    lo que RNF-07 prohíbe: «el nivel severo debe atribuir el juicio a la fuente
    que lo sostiene en lugar de afirmarlo el sistema por su cuenta».

    Cuando el puntaje llega al nivel severo pero la contradicción viene de
    medios de referencia o de verificaciones previas y no de una fuente oficial,
    el veredicto se rebaja a *información sospechosa*. No se lo rebaja a *parece
    verificado*: la evidencia sí apunta contra la afirmación, lo que falta es el
    respaldo oficial que el nombre del nivel promete.
    """
    if not fuentes:
        return Veredicto.SIN_CONTRASTE_EXTERNO

    if (
        veredicto is Veredicto.CONTRADICHO_POR_FUENTES_OFICIALES
        and not _hay_fuente_oficial_que_contradice(fuentes)
    ):
        return Veredicto.INFORMACION_SOSPECHOSA

    return veredicto


def _hay_fuente_oficial_que_contradice(fuentes: list[Fuente]) -> bool:
    """Si alguna fuente del escalón oficial contradice la afirmación."""
    return any(
        fuente.tipo is TipoFuente.FUENTE_OFICIAL
        and fuente.postura is Postura.CONTRADICE
        for fuente in fuentes
    )


def _razones_admisibles(razones: list[Razon], fuentes: list[Fuente]) -> list[Razon]:
    """Deja sin enlace toda razón cuya fuente no esté entre las recuperadas.

    Es la otra mitad de RNF-06: una razón derivada de evidencia externa lleva el
    enlace a la fuente que la respalda, y una razón que no deriva de ninguna
    fuente recuperada no puede llevar un enlace inventado. Con `fuentes` vacía,
    ninguna razón conserva enlace.
    """
    urls_admisibles = {fuente.url for fuente in fuentes}
    return [
        Razon(
            texto=razon.texto,
            fuente_url=razon.fuente_url if razon.fuente_url in urls_admisibles else None,
        )
        for razon in razones
    ]
