/**
 * El acuerdo entre el guion del mundo de la página y el *content script* para
 * leer la trayectoria de la cuenta autora. Ver `src/pagina/index.ts`.
 */

/** Lo dispara el *content script* sobre el artículo del tuit. */
export const EVENTO_LEER_CUENTAS = 'factum:leer-cuentas';

/** Donde el guion de la página deja las cuentas, en JSON, por *handle*. */
export const ATRIBUTO_CUENTAS = 'data-factum-cuentas';

export interface CuentaLeida {
  /** Fecha de creación en ISO 8601. */
  creada: string;
  seguidores: number;
  seguidos: number;
}
