/**
 * Mensajes que cruzan entre el *content script* y el *service worker*.
 *
 * El *content script* nunca habla con el servicio: quien tiene los permisos de
 * anfitrión y hace la petición de red es el *service worker*. Este archivo es
 * el único contrato entre ambos.
 */

import type { PedidoAnalisis, PedidoReporte, PublicacionVisible } from './contrato';

/** Petición de análisis de un tuit, emitida por el *content script*. */
export interface MensajeAnalizar {
  tipo: 'analizar';
  pedido: PedidoAnalisis;
}

/** Consulta del análisis previo de un tuit, sin pedir uno nuevo (RF-07). */
export interface MensajeConsultar {
  tipo: 'consultar';
  tweetId: string;
}

/**
 * Señal del texto de una publicación que entró en el área visible (CU-01).
 * El *content script* manda una por publicación; el *service worker* las
 * agrupa en lotes. La respuesta es la señal, o `null` si no la hubo.
 */
export interface MensajeSenal {
  tipo: 'senal';
  publicacion: PublicacionVisible;
}

/** Comprobación de vida del servicio, emitida por la ventana emergente. */
export interface MensajeSalud {
  tipo: 'salud';
}

/** Informe de un veredicto incorrecto, emitido desde el detalle (CU-04). */
export interface MensajeReportar {
  tipo: 'reportar';
  reporte: PedidoReporte;
}

/** Abre el panel web con el histórico de esta instalación (CU-05). */
export interface MensajeAbrirPanel {
  tipo: 'abrir-panel';
}

export type MensajeEntrante =
  | MensajeAnalizar
  | MensajeConsultar
  | MensajeSenal
  | MensajeSalud
  | MensajeReportar
  | MensajeAbrirPanel;

/** Respuesta del *service worker*, que nunca es un error opaco (RNF-11). */
export type RespuestaMensaje<T> =
  | { ok: true; datos: T }
  | { ok: false; error: string };
