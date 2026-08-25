/**
 * Lector del DOM de X.
 *
 * Es una función pura de un nodo del *timeline* a los datos del tuit, o `null`
 * si el nodo no es analizable. Nadie versiona el marcado de X, así que la
 * lectura se apoya en los atributos de prueba (`data-testid`) y **es
 * defensiva**: un campo que falta saltea el tuit en lugar de romper la
 * extensión.
 *
 * Esta función es la costura que el ticket siguiente cubre con pruebas contra
 * fixtures HTML guardados de X real.
 */

/** Selector de los tuits del *timeline*. */
export const SELECTOR_TUIT = 'article[data-testid="tweet"]';

/** Datos mínimos que el análisis necesita de un tuit. */
export interface DatosTuit {
  /** Identificador nativo, extraído del enlace permanente. */
  tweetId: string;
  /** Texto de la publicación. */
  texto: string;
  /** Cuenta autora, con arroba. */
  handle: string;
}

/**
 * Devuelve el enlace permanente propio del tuit.
 *
 * Un artículo puede contener más de un enlace a `/status/` —una cita anidada
 * agrega el suyo—, así que se toma el primero que envuelve un elemento `time`,
 * que es el de la publicación en sí.
 */
function enlacePermanente(articulo: Element): HTMLAnchorElement | null {
  const enlaces = articulo.querySelectorAll<HTMLAnchorElement>('a[href*="/status/"]');
  for (const enlace of Array.from(enlaces)) {
    if (enlace.querySelector('time')) {
      return enlace;
    }
  }
  return null;
}

/**
 * Extrae el identificador nativo y la cuenta autora de un enlace permanente.
 *
 * El formato esperado es `/cuenta/status/1234567890123456789`, eventualmente
 * con segmentos adicionales como `/photo/1`.
 */
function partirEnlace(href: string): { tweetId: string; handle: string } | null {
  const coincidencia = /^\/([^/]+)\/status\/(\d+)/.exec(href);
  if (!coincidencia) {
    return null;
  }
  const [, cuenta, tweetId] = coincidencia;
  if (!cuenta || !tweetId) {
    return null;
  }
  return { tweetId, handle: `@${cuenta}` };
}

/**
 * Lee un nodo del *timeline* y devuelve los datos del tuit.
 *
 * Devuelve `null` cuando el nodo no tiene texto, no tiene enlace permanente o
 * el enlace no responde a la forma esperada. Nunca lanza.
 */
export function leerTuit(articulo: Element): DatosTuit | null {
  try {
    const nodoTexto = articulo.querySelector('div[data-testid="tweetText"]');
    const texto = nodoTexto?.textContent?.trim() ?? '';
    if (!texto) {
      return null;
    }

    const enlace = enlacePermanente(articulo);
    // `getAttribute` y no `.href`: interesa la ruta relativa tal como está en
    // el marcado, no la URL absoluta que el DOM resuelve.
    const href = enlace?.getAttribute('href') ?? '';
    if (!href) {
      return null;
    }

    const partes = partirEnlace(href);
    if (!partes) {
      return null;
    }

    return { tweetId: partes.tweetId, texto, handle: partes.handle };
  } catch {
    return null;
  }
}
