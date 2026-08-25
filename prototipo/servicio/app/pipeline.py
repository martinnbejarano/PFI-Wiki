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
- **Paso de veredicto (RF-06).** Real. Sale de una llamada al proveedor.
- **Paso de recuperación de evidencia (RF-05).** Pendiente del ticket #23. Sin
  él, `fuentes` viene vacía y el veredicto se emite en el estado *sin contraste
  externo*, que es exactamente lo que RF-06 y RNF-06 exigen en ese caso.
- **Módulo de credibilidad de la cuenta (Módulo 2).** Recortado a propósito:
  `credibilidad.py` devuelve un valor arbitrario derivado del *handle*. Viaja
  marcado con `no_implementado` para que la interfaz no lo presente como una
  medición.
- **Combinador ponderado (Módulo 4).** Pendiente del ticket #24.
"""

from __future__ import annotations

from .configuracion import Configuracion
from .contrato import (
    AnalisisParcial,
    Fuente,
    PedidoAnalisis,
    PuntajeClasificador,
    PuntajeContraste,
    PuntajeCredibilidad,
    Puntajes,
    Razon,
    RespuestaAnalisis,
    Veredicto,
)
from .credibilidad import puntaje_de_credibilidad
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

    puntajes = _puntajes(extraida, pedido.handle, PUNTAJE_CONTRASTE_SIN_EVIDENCIA)

    if not extraida.hay_afirmacion_verificable:
        return _respuesta_sin_afirmacion(pedido, extraida, puntajes, configuracion)

    fuentes: list[Fuente] = _recuperar_evidencia(extraida.afirmacion, proveedor)

    emitido = proveedor.emitir_veredicto(extraida.afirmacion, fuentes)

    return _armar_respuesta(
        pedido=pedido,
        extraida=extraida,
        puntajes=puntajes,
        veredicto=_veredicto_admisible(emitido.veredicto, fuentes),
        justificacion=emitido.justificacion,
        razones=_razones_admisibles(emitido.razones, fuentes),
        fuentes=fuentes,
        configuracion=configuracion,
    )


def _puntajes(
    extraida: AfirmacionExtraida, handle: str, valor_contraste: float
) -> Puntajes:
    """Arma los tres puntajes parciales que el desglose de la interfaz dibuja."""
    return Puntajes(
        # El puntaje del clasificador sale del paso de extracción, que en esta
        # instancia es la línea base de LLM en *zero-shot* del Módulo 1.
        clasificador=PuntajeClasificador(valor=extraida.puntaje, clase=extraida.clase),
        # El Módulo 2 está recortado y el valor es arbitrario: por eso viaja
        # siempre marcado. Ver `credibilidad.py` para la decisión y para por qué
        # no se lo alimenta con `pedido.verificada` ni con `pedido.metricas`.
        credibilidad=PuntajeCredibilidad(
            valor=puntaje_de_credibilidad(handle), no_implementado=True
        ),
        # La derivación del puntaje a partir de la postura agregada de las
        # fuentes llega con el ticket #24. Sin fuentes recuperadas hay un solo
        # valor posible, y es el que se documenta arriba.
        contraste=PuntajeContraste(valor=valor_contraste),
    )


def _respuesta_sin_afirmacion(
    pedido: PedidoAnalisis,
    extraida: AfirmacionExtraida,
    puntajes: Puntajes,
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
    return _armar_respuesta(
        pedido=pedido,
        extraida=extraida,
        puntajes=puntajes,
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
        # El combinador ponderado es del ticket #24. Hasta entonces el puntaje
        # final es el del clasificador: combinar con pesos inventados dos
        # puntajes que todavía no miden nada produciría un número con aire de
        # resultado y sin nada detrás.
        puntaje_final=puntajes.clasificador.valor,
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
    """Recupera la evidencia externa, o nada mientras el paso no exista.

    El ticket #23 reemplaza el cuerpo de esta función por la llamada real a
    `proveedor.recuperar_evidencia`. La forma de lo que devuelve no cambia, así
    que ningún test tiene que cambiar con ella.
    """
    return []


def _veredicto_admisible(veredicto: Veredicto, fuentes: list[Fuente]) -> Veredicto:
    """Aplica la invariante de RNF-06 sobre el veredicto que emitió el proveedor.

    Sin ninguna fuente enlazable, el único resultado admisible es *sin contraste
    externo*. La instrucción que recibe el modelo ya lo dice, pero la regla es
    una invariante del sistema y no algo que dependa de que el modelo obedezca:
    se vuelve a exigir acá, del lado del servicio, donde es verificable.
    """
    if not fuentes:
        return Veredicto.SIN_CONTRASTE_EXTERNO
    return veredicto


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
