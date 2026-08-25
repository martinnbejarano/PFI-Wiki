/**
 * Mensajes que cruzan entre el *content script* y el *service worker*.
 *
 * El *content script* nunca habla con el servicio: quien tiene los permisos de
 * anfitrión y hace la petición de red es el *service worker*. Este archivo es
 * el único contrato entre ambos.
 */

import type { PedidoAnalisis } from './contrato';

/** Petición de análisis de un tuit, emitida por el *content script*. */
export interface MensajeAnalizar {
  tipo: 'analizar';
  pedido: PedidoAnalisis;
}

/** Comprobación de vida del servicio, emitida por la ventana emergente. */
export interface MensajeSalud {
  tipo: 'salud';
}

export type MensajeEntrante = MensajeAnalizar | MensajeSalud;

/** Respuesta del *service worker*, que nunca es un error opaco (RNF-11). */
export type RespuestaMensaje<T> =
  | { ok: true; datos: T }
  | { ok: false; error: string };
