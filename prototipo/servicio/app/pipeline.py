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
"""

from __future__ import annotations

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
    TipoFuente,
    Veredicto,
)
from .credibilidad import puntaje_de_credibilidad
from .jerarquia import filtrar_por_jerarquia
from .proveedor.puerto import AfirmacionExtraida, ProveedorDeAnalisis

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


def analizar_tuit(
    pedido: PedidoAnalisis,
    proveedor: ProveedorDeAnalisis,
    configuracion: Configuracion,
) -> RespuestaAnalisis:
    """Ejecuta el análisis completo de un tuit y arma la respuesta del contrato."""
    extraida = proveedor.extraer_afirmacion(pedido.texto.strip())

    if not extraida.hay_afirmacion_verificable:
        return _respuesta_sin_afirmacion(pedido, extraida, configuracion)

    fuentes: list[Fuente] = _recuperar_evidencia(extraida.afirmacion, proveedor)

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
    # el resultado en lugar de producirlo.
    emitido = proveedor.emitir_veredicto(extraida.afirmacion, fuentes, veredicto)

    return _armar_respuesta(
        pedido=pedido,
        extraida=extraida,
        puntajes=puntajes,
        puntaje_final=final,
        veredicto=veredicto,
        justificacion=emitido.justificacion,
        razones=_razones_admisibles(emitido.razones, fuentes),
        fuentes=fuentes,
        configuracion=configuracion,
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
) -> RespuestaAnalisis:
    """Arma la `RespuestaAnalisis` del contrato con lo que produjeron los pasos."""
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
        analisis_parcial=AnalisisParcial(es_parcial=False, modulos_ausentes=[]),
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
