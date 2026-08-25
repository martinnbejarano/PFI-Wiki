"""Contrato de la respuesta de análisis.

Este módulo es la definición autoritativa de lo que el servicio recibe y
devuelve en ``POST /analizar``. Los nombres de campo y los dominios cerrados
fijados acá los consume la extensión y los consumen los tickets siguientes del
prototipo: cambiarlos rompe a ambos lados.

Correspondencia con los requerimientos entregados:

- ``afirmacion`` y ``tipo_afirmacion``            → RF-04
- ``fuentes`` con tipo y postura                  → RF-05
- ``veredicto``, ``justificacion`` y ``razones``  → RF-06 y RNF-06
- ``analisis_parcial``                            → RNF-11
- ``version_modelo`` y ``version_configuracion_pesos`` → RF-16
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class TipoAfirmacion(str, Enum):
    """Tipos de afirmación verificable previstos por RF-04."""

    NORMATIVA = "normativa"
    DATO_ECONOMICO = "dato_economico"
    SALUD = "salud"
    EDUCACION = "educacion"
    OTRO = "otro"


class Veredicto(str, Enum):
    """Los tres niveles de RF-06 más el estado de ausencia de evidencia."""

    CONTRADICHO_POR_FUENTES_OFICIALES = "contradicho_por_fuentes_oficiales"
    INFORMACION_SOSPECHOSA = "informacion_sospechosa"
    PARECE_VERIFICADO = "parece_verificado"
    SIN_CONTRASTE_EXTERNO = "sin_contraste_externo"


class TipoFuente(str, Enum):
    """Jerarquía de evidencia de RF-05, en orden de precedencia."""

    FUENTE_OFICIAL = "fuente_oficial"
    MEDIO_DE_REFERENCIA = "medio_de_referencia"
    VERIFICACION_PREVIA = "verificacion_previa"


class Postura(str, Enum):
    """Postura de una fuente respecto de la afirmación analizada."""

    CORROBORA = "corrobora"
    CONTRADICE = "contradice"
    NEUTRAL = "neutral"


class MetricasTuit(BaseModel):
    """Métricas públicas de propagación visibles en el nodo del *timeline*.

    ``None`` significa que la métrica no está visible en el nodo, que no es lo
    mismo que valer cero: X omite el contador cuando está en cero y publica las
    vistas solo en algunas publicaciones. Quien consuma estos valores tiene que
    tratar la ausencia explícitamente en lugar de asumir cero.
    """

    respuestas: int | None = None
    retuits: int | None = None
    me_gusta: int | None = None
    vistas: int | None = None


class PedidoAnalisis(BaseModel):
    """Cuerpo de la petición de análisis."""

    tweet_id: str = Field(
        description="Identificador nativo del tuit; clave de caché y de correlación.",
        examples=["1234567890123456789"],
    )
    texto: str = Field(
        description="Texto del tuit leído del DOM de X.",
        examples=["A partir del lunes cierran todas las escuelas de la Provincia."],
    )
    handle: str = Field(
        description="Identificador de la cuenta autora, con arroba.",
        examples=["@ejemplo"],
    )
    verificada: bool = Field(
        default=False,
        description="Si la cuenta autora exhibe la insignia de verificación.",
        examples=[True],
    )
    metricas: MetricasTuit = Field(
        default_factory=MetricasTuit,
        description=(
            "Métricas públicas de propagación leídas del nodo del *timeline*."
        ),
    )


class PuntajeClasificador(BaseModel):
    """Salida del Módulo 1 (clasificador NLP)."""

    valor: float = Field(ge=0.0, le=1.0)
    clase: str


class PuntajeCredibilidad(BaseModel):
    """Salida del Módulo 2 (credibilidad de la cuenta autora).

    ``no_implementado`` viaja en la respuesta porque la interfaz tiene que poder
    marcar el valor como dato no medido, tal como exige el recorte declarado.
    """

    valor: float = Field(ge=0.0, le=1.0)
    no_implementado: bool = False


class PuntajeContraste(BaseModel):
    """Salida del Módulo 3 (contraste con evidencia externa)."""

    valor: float = Field(ge=0.0, le=1.0)


class Puntajes(BaseModel):
    """Los tres puntajes parciales que el combinador recibe."""

    clasificador: PuntajeClasificador
    credibilidad: PuntajeCredibilidad
    contraste: PuntajeContraste


class Razon(BaseModel):
    """Una razón de la justificación.

    ``fuente_url`` es ``None`` cuando la razón no deriva de evidencia externa
    sino del análisis del propio texto o de las señales de la cuenta.
    """

    texto: str
    fuente_url: str | None = None


class Fuente(BaseModel):
    """Una fuente consultada, dentro de la jerarquía de evidencia."""

    titulo: str
    url: str
    tipo: TipoFuente
    postura: Postura


class AnalisisParcial(BaseModel):
    """Bandera de análisis parcial exigida por RNF-11."""

    es_parcial: bool = False
    modulos_ausentes: list[str] = Field(default_factory=list)


class RespuestaAnalisis(BaseModel):
    """Respuesta completa del punto de entrada de análisis."""

    tweet_id: str
    afirmacion: str
    tipo_afirmacion: TipoAfirmacion
    puntajes: Puntajes
    puntaje_final: float = Field(ge=0.0, le=1.0)
    veredicto: Veredicto
    justificacion: str
    razones: list[Razon]
    fuentes: list[Fuente]
    analisis_parcial: AnalisisParcial
    version_modelo: str
    version_configuracion_pesos: str
