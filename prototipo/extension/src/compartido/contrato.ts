/**
 * Espejo en TypeScript del contrato de la respuesta de análisis.
 *
 * La definición autoritativa vive en `prototipo/servicio/app/contrato.py`.
 * Si un campo cambia allá, tiene que cambiar acá: no hay generación automática
 * y esa es una deuda declarada del prototipo.
 */

export type TipoAfirmacion =
  | 'normativa'
  | 'dato_economico'
  | 'salud'
  | 'educacion'
  | 'otro';

export type Veredicto =
  | 'contradicho_por_fuentes_oficiales'
  | 'informacion_sospechosa'
  | 'parece_verificado'
  | 'sin_contraste_externo';

export type TipoFuente =
  | 'fuente_oficial'
  | 'medio_de_referencia'
  | 'verificacion_previa';

export type Postura = 'corrobora' | 'contradice' | 'neutral';

/**
 * Métricas públicas de propagación leídas del nodo del *timeline*.
 *
 * `null` significa «no visible en el nodo», que no es lo mismo que cero: X
 * omite el contador cuando está en cero y publica las vistas solo en algunas
 * publicaciones.
 */
export interface MetricasTuit {
  respuestas: number | null;
  retuits: number | null;
  me_gusta: number | null;
  vistas: number | null;
}

export interface PedidoAnalisis {
  tweet_id: string;
  texto: string;
  handle: string;
  verificada: boolean;
  metricas: MetricasTuit;
}

export interface Puntajes {
  clasificador: { valor: number; clase: string };
  credibilidad: { valor: number; no_implementado: boolean };
  contraste: { valor: number };
}

export interface Razon {
  texto: string;
  fuente_url: string | null;
}

export interface Fuente {
  titulo: string;
  url: string;
  tipo: TipoFuente;
  postura: Postura;
}

export interface AnalisisParcial {
  es_parcial: boolean;
  modulos_ausentes: string[];
}

/**
 * Los nombres con los que el servicio lista un módulo que no pudo ejecutarse
 * (RNF-11). Espejo de las constantes de `prototipo/servicio/app/pipeline.py`.
 *
 * Son **texto legible**, no identificadores: la interfaz los muestra tal cual
 * en el aviso del análisis parcial, así que no hay una tabla de traducción que
 * mantener. Se los reconoce acá por una sola razón, que es marcar con la trama
 * de *sin dato* la barra del módulo que faltó.
 *
 * Un nombre que no esté en esta lista no rompe nada: el aviso lo enumera igual
 * y lo único que se pierde es el rayado de una barra. Es deliberado —el
 * servicio puede declarar un módulo ausente que esta versión de la extensión
 * todavía no conoce, y el ciudadano tiene que enterarse igual—.
 */
export const MODULO_AUSENTE = {
  extraccion: 'la extracción de la afirmación verificable',
  contraste: 'el contraste con evidencia externa',
  redaccion: 'la redacción de la justificación',
} as const;

/** Si el análisis declara ausente el módulo indicado. */
export function falta(
  analisis: RespuestaAnalisis,
  modulo: (typeof MODULO_AUSENTE)[keyof typeof MODULO_AUSENTE],
): boolean {
  return analisis.analisis_parcial.modulos_ausentes.includes(modulo);
}

export interface RespuestaAnalisis {
  tweet_id: string;
  afirmacion: string;
  tipo_afirmacion: TipoAfirmacion;
  puntajes: Puntajes;
  puntaje_final: number;
  veredicto: Veredicto;
  justificacion: string;
  razones: Razon[];
  fuentes: Fuente[];
  analisis_parcial: AnalisisParcial;
  version_modelo: string;
  version_configuracion_pesos: string;
}
