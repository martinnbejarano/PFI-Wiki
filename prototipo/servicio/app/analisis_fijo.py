"""Análisis de valores fijos.

Este módulo es el relleno provisorio del punto de entrada de análisis mientras
la rebanada trazadora atraviesa el manifiesto, el *shadow DOM* y el CORS. No hay
proveedor de modelo de lenguaje grande (*Large Language Model*, LLM), no hay
búsqueda web y no hay caché: la respuesta es siempre la misma y solo se
correlaciona con la petición por el identificador nativo del tuit.

Los tickets siguientes reemplazan `construir_analisis` por la cadena real de
pasos. La forma de lo que devuelve no cambia: es el contrato de `contrato.py`.

Los datos son ilustrativos y no corresponden a ninguna publicación real.
"""

from __future__ import annotations

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

VERSION_MODELO = "fijo-0"
VERSION_CONFIGURACION_PESOS = "pesos-v1"


def construir_analisis(pedido: PedidoAnalisis) -> RespuestaAnalisis:
    """Devuelve el contrato completo con valores fijos."""
    return RespuestaAnalisis(
        tweet_id=pedido.tweet_id,
        afirmacion="A partir del lunes cierran todas las escuelas de la Provincia",
        tipo_afirmacion=TipoAfirmacion.EDUCACION,
        puntajes=Puntajes(
            clasificador=PuntajeClasificador(valor=0.82, clase="sospechoso"),
            credibilidad=PuntajeCredibilidad(valor=0.55, no_implementado=True),
            contraste=PuntajeContraste(valor=0.89),
        ),
        puntaje_final=0.84,
        veredicto=Veredicto.CONTRADICHO_POR_FUENTES_OFICIALES,
        justificacion=(
            "La resolución publicada en el Boletín Oficial alcanza a un conjunto "
            "acotado de establecimientos y no a la totalidad del sistema educativo "
            "provincial. Tres medios de referencia reportan el mismo alcance "
            "limitado y ninguno respalda un cierre general."
        ),
        razones=[
            Razon(
                texto=(
                    "La resolución oficial enumera los establecimientos alcanzados "
                    "por la suspensión y no comprende a la totalidad."
                ),
                fuente_url="https://www.boletinoficial.gob.ar/",
            ),
            Razon(
                texto="Tres medios de referencia contradicen el alcance afirmado.",
                fuente_url="https://www.lanacion.com.ar/",
            ),
            Razon(
                texto=(
                    "El texto combina lenguaje de urgencia con una afirmación "
                    "absoluta y no cita ninguna fuente."
                ),
                fuente_url=None,
            ),
        ],
        fuentes=[
            Fuente(
                titulo=(
                    "Resolución que dispone la suspensión de actividades en "
                    "establecimientos determinados"
                ),
                url="https://www.boletinoficial.gob.ar/",
                tipo=TipoFuente.FUENTE_OFICIAL,
                postura=Postura.CONTRADICE,
            ),
            Fuente(
                titulo="El Ministerio aclaró que no habrá cierre total de escuelas",
                url="https://www.lanacion.com.ar/",
                tipo=TipoFuente.MEDIO_DE_REFERENCIA,
                postura=Postura.CONTRADICE,
            ),
            Fuente(
                titulo="Qué se sabe del cierre de escuelas que circula en redes",
                url="https://www.infobae.com/",
                tipo=TipoFuente.MEDIO_DE_REFERENCIA,
                postura=Postura.CORROBORA,
            ),
            Fuente(
                titulo="Preocupación de las familias por el estado edilicio escolar",
                url="https://www.pagina12.com.ar/",
                tipo=TipoFuente.MEDIO_DE_REFERENCIA,
                postura=Postura.NEUTRAL,
            ),
            Fuente(
                titulo="Es falso que se cierren todas las escuelas bonaerenses",
                url="https://chequeado.com/",
                tipo=TipoFuente.VERIFICACION_PREVIA,
                postura=Postura.CONTRADICE,
            ),
        ],
        analisis_parcial=AnalisisParcial(es_parcial=False, modulos_ausentes=[]),
        version_modelo=VERSION_MODELO,
        version_configuracion_pesos=VERSION_CONFIGURACION_PESOS,
    )
