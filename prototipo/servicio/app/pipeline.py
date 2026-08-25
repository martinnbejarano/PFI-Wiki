"""Orquestador del análisis.

Encadena los pasos del *pipeline* y arma la `RespuestaAnalisis` del contrato.
Es el único lugar que conoce el orden de los pasos; el punto de entrada HTTP
solo lo llama, y el adaptador del proveedor no sabe que existe.

Ningún test toca este módulo directamente. Se ejercita entero por
`POST /analizar`, que es la costura que la *spec* fija para el servicio: si un
test se rompiera al reemplazar un paso, estaría probando implementación.

Qué está implementado en esta instancia y qué no:

- **Paso de veredicto (RF-06).** Real. Sale de una llamada al proveedor.
- **Paso de extracción de la afirmación (RF-04).** Pendiente del ticket #22.
  Mientras tanto la afirmación es el texto del tuit tal como se leyó del DOM y
  el tipo es `otro`, que es lo que corresponde a una afirmación sin clasificar.
- **Paso de recuperación de evidencia (RF-05).** Pendiente del ticket #23. Sin
  él, `fuentes` viene vacía y el veredicto se emite en el estado *sin contraste
  externo*, que es exactamente lo que RF-06 y RNF-06 exigen en ese caso.
- **Módulo de credibilidad de la cuenta (Módulo 2).** Pendiente del ticket #22.
  Viaja marcado con `no_implementado` para que la interfaz no lo presente como
  una medición.
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
    TipoAfirmacion,
    Veredicto,
)
from .proveedor.puerto import ProveedorDeAnalisis

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

# Valor neutro del clasificador mientras el paso de extracción no exista. No es
# una medición y no pretende serlo: el ticket #22 lo reemplaza por la salida
# real del paso de clasificación.
PUNTAJE_CLASIFICADOR_PROVISORIO = 0.5
CLASE_CLASIFICADOR_PROVISORIA = "sin_clasificar"

# Valor arbitrario del módulo de credibilidad, derivado de una semilla del
# *handle* recién en el ticket #22. Viaja marcado como no implementado.
PUNTAJE_CREDIBILIDAD_PROVISORIO = 0.55


def analizar_tuit(
    pedido: PedidoAnalisis,
    proveedor: ProveedorDeAnalisis,
    configuracion: Configuracion,
) -> RespuestaAnalisis:
    """Ejecuta el análisis completo de un tuit y arma la respuesta del contrato."""
    afirmacion = pedido.texto.strip()
    tipo_afirmacion = TipoAfirmacion.OTRO

    fuentes: list[Fuente] = _recuperar_evidencia(afirmacion, proveedor)

    emitido = proveedor.emitir_veredicto(afirmacion, fuentes)
    veredicto = _veredicto_admisible(emitido.veredicto, fuentes)
    razones = _razones_admisibles(emitido.razones, fuentes)

    puntaje_clasificador = PuntajeClasificador(
        valor=PUNTAJE_CLASIFICADOR_PROVISORIO,
        clase=CLASE_CLASIFICADOR_PROVISORIA,
    )
    # La derivación del puntaje a partir de la postura agregada de las fuentes
    # llega con el ticket #24. Sin fuentes recuperadas hay un solo valor
    # posible, y es el que se documenta arriba.
    puntaje_contraste = PuntajeContraste(valor=PUNTAJE_CONTRASTE_SIN_EVIDENCIA)

    return RespuestaAnalisis(
        tweet_id=pedido.tweet_id,
        afirmacion=afirmacion,
        tipo_afirmacion=tipo_afirmacion,
        puntajes=Puntajes(
            clasificador=puntaje_clasificador,
            credibilidad=PuntajeCredibilidad(
                valor=PUNTAJE_CREDIBILIDAD_PROVISORIO, no_implementado=True
            ),
            contraste=puntaje_contraste,
        ),
        # El combinador ponderado es del ticket #24. Hasta entonces el puntaje
        # final es el del clasificador: combinar con pesos inventados dos
        # puntajes que todavía no miden nada produciría un número con aire de
        # resultado y sin nada detrás.
        puntaje_final=puntaje_clasificador.valor,
        veredicto=veredicto,
        justificacion=emitido.justificacion,
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
