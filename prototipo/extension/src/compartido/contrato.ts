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

export interface PedidoAnalisis {
  tweet_id: string;
  texto: string;
  handle: string;
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
