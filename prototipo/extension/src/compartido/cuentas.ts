/**
 * Lo que el interceptor (mundo de la página) le pasa al *content script*.
 * Ver `src/interceptor/index.ts`.
 */

export const MENSAJE_CUENTAS = 'factum:cuentas';

export interface CuentaLeida {
  /** Con arroba, como lo devuelve el lector del DOM. */
  handle: string;
  /** Fecha de creación en ISO 8601. */
  creada: string;
  seguidores: number;
  seguidos: number;
}
