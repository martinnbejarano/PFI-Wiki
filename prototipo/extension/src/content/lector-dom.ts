/**
 * Lector del DOM de X.
 *
 * Es una función pura de un nodo del *timeline* a los datos del tuit, o `null`
 * si el nodo no es analizable. Nadie versiona el marcado de X, así que la
 * lectura se apoya en los atributos de prueba (`data-testid`) y **es
 * defensiva**: un campo obligatorio que falta saltea el tuit en lugar de romper
 * la extensión, y un campo opcional que falta viaja como ausente en lugar de
 * invalidar la lectura entera.
 *
 * Obligatorios son solo el texto y el identificador nativo: sin ellos no hay
 * nada que analizar ni con qué correlacionar el resultado. La verificación de
 * la cuenta y las métricas de propagación son señales adicionales, y su
 * ausencia —X las oculta según el tipo de cuenta, el idioma y el ancho de la
 * ventana— no debe descartar el tuit.
 *
 * Esta es la costura 2 de la *spec*, cubierta por pruebas contra fixtures HTML
 * guardados de X real en `lector-dom.test.ts`.
 */

/** Selector de los tuits del *timeline*. */
export const SELECTOR_TUIT = 'article[data-testid="tweet"]';

/**
 * Métricas públicas de propagación visibles en el nodo del *timeline*.
 *
 * Cada campo es `null` cuando la métrica no está visible en el nodo, que no es
 * lo mismo que valer cero: X omite el número cuando el contador está en cero, y
 * las vistas solo aparecen en algunas publicaciones. Distinguir «no visible» de
 * «cero» evita que el análisis interprete una ausencia de marcado como una
 * publicación sin difusión.
 */
export interface MetricasTuit {
  respuestas: number | null;
  retuits: number | null;
  meGusta: number | null;
  vistas: number | null;
}

/** Datos que el análisis necesita de un tuit. */
export interface DatosTuit {
  /** Identificador nativo, extraído del enlace permanente. */
  tweetId: string;
  /** Texto de la publicación. */
  texto: string;
  /** Cuenta autora, con arroba. */
  handle: string;
  /** Si la cuenta autora exhibe la insignia de verificación. */
  verificada: boolean;
  /** Métricas de propagación visibles en el nodo. */
  metricas: MetricasTuit;
}

/**
 * Indica si un nodo pertenece a una publicación citada dentro del artículo.
 *
 * Un tuit con cita anida el marcado del tuit citado —su propio texto, su propio
 * enlace permanente, su propio nombre de cuenta— dentro de un contenedor con
 * `role="link"`. Sin este filtro, el lector podría devolver el texto o el
 * identificador de la publicación citada en lugar de los de la publicación que
 * se está analizando.
 */
function esDeUnaCita(nodo: Element, articulo: Element): boolean {
  let actual: Element | null = nodo.parentElement;
  while (actual && actual !== articulo) {
    if (actual.getAttribute('role') === 'link' || actual.tagName === 'ARTICLE') {
      return true;
    }
    actual = actual.parentElement;
  }
  return false;
}

/** Devuelve los nodos que coinciden con el selector y no vienen de una cita. */
function propios<T extends Element>(articulo: Element, selector: string): T[] {
  return Array.from(articulo.querySelectorAll<T>(selector)).filter(
    (nodo) => !esDeUnaCita(nodo, articulo),
  );
}

/**
 * Devuelve el enlace permanente propio del tuit.
 *
 * Un artículo puede contener más de un enlace a `/status/` —una cita anidada
 * agrega el suyo—, así que se toma el primero que envuelve un elemento `time`,
 * que es el de la publicación en sí.
 */
function enlacePermanente(articulo: Element): HTMLAnchorElement | null {
  const enlaces = propios<HTMLAnchorElement>(articulo, 'a[href*="/status/"]');
  return enlaces.find((enlace) => enlace.querySelector('time')) ?? null;
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
 * Indica si la cuenta autora exhibe la insignia de verificación.
 *
 * Se mira dentro del bloque del nombre y no en todo el artículo, porque una
 * publicación citada trae su propia insignia y no es la que interesa. X marca
 * la insignia con un atributo de prueba propio; la lectura de la etiqueta
 * accesible queda como respaldo para cuando ese atributo cambie de nombre.
 */
function leerVerificacion(articulo: Element): boolean {
  const bloqueNombre = propios(articulo, 'div[data-testid="User-Name"]')[0];
  if (!bloqueNombre) {
    return propios(articulo, 'svg[data-testid="icon-verified"]').length > 0;
  }
  if (bloqueNombre.querySelector('svg[data-testid="icon-verified"]')) {
    return true;
  }
  return Array.from(bloqueNombre.querySelectorAll('[aria-label]')).some((nodo) =>
    /verificad|verified/i.test(nodo.getAttribute('aria-label') ?? ''),
  );
}

/** Multiplicadores de las abreviaturas de magnitud, en castellano y en inglés. */
const MULTIPLICADORES: ReadonlyArray<readonly [RegExp, number]> = [
  [/^(?:mil\s*millones|b)$/i, 1_000_000_000],
  [/^(?:mill(?:ones|ón|on)?\.?|m)$/i, 1_000_000],
  [/^(?:mil|k)$/i, 1_000],
];

/**
 * Convierte el texto de un contador en un número entero.
 *
 * X abrevia los contadores grandes y usa los separadores del idioma de la
 * interfaz, de modo que el mismo valor puede aparecer como `1234`, `1.234`,
 * `1,2 mil` o `1.2K`. La ambigüedad entre separador decimal y de millar se
 * resuelve por la forma: un separador seguido de exactamente tres dígitos y sin
 * abreviatura detrás es de millar; en cualquier otro caso es decimal.
 *
 * Devuelve `null` ante cualquier texto que no encaje, que es lo que hace que un
 * cambio de formato de X degrade la métrica en lugar de descartar el tuit.
 */
function aNumero(texto: string): number | null {
  // X separa el número de su abreviatura con espacio duro; normalizarlo evita
  // que `1,2 mil` se lea como `1,2`.
  const limpio = texto.replace(/\u00a0/g, ' ');
  const coincidencia = /(\d+(?:[.,]\d+)*)\s*(mil\s*millones|millones|millón|millon|mill\.?|mil|K|M|B)?/i.exec(
    limpio,
  );
  if (!coincidencia) {
    return null;
  }

  const [, digitos, abreviatura] = coincidencia;
  if (!digitos) {
    return null;
  }

  const factor = abreviatura
    ? (MULTIPLICADORES.find(([patron]) => patron.test(abreviatura.trim()))?.[1] ?? 1)
    : 1;

  let base: number;
  if (/^\d+$/.test(digitos)) {
    base = Number(digitos);
  } else if (!abreviatura && /^\d{1,3}(?:([.,])\d{3})+$/.test(digitos)) {
    base = Number(digitos.replace(/[.,]/g, ''));
  } else if (/^\d+[.,]\d+$/.test(digitos)) {
    base = Number(digitos.replace(',', '.'));
  } else {
    return null;
  }

  const valor = Math.round(base * factor);
  return Number.isFinite(valor) ? valor : null;
}

/**
 * Lee el contador de un botón de la barra de acciones.
 *
 * Se prefiere la etiqueta accesible sobre el texto visible: X escribe ahí el
 * número exacto mientras que el texto va abreviado, y además la etiqueta existe
 * aunque el número esté oculto por el ancho de la ventana.
 */
function leerContador(nodo: Element | null): number | null {
  if (!nodo) {
    return null;
  }
  const etiqueta = nodo.getAttribute('aria-label');
  if (etiqueta) {
    const desdeEtiqueta = aNumero(etiqueta);
    if (desdeEtiqueta !== null) {
      return desdeEtiqueta;
    }
  }
  return aNumero(nodo.textContent ?? '');
}

/**
 * Atributos de prueba de cada métrica.
 *
 * Los retuits y los me gusta tienen dos nombres según si la cuenta que mira ya
 * interactuó con la publicación, y el lector acepta los dos.
 */
const ATRIBUTOS_DE_METRICA: ReadonlyArray<readonly [keyof MetricasTuit, readonly string[]]> = [
  ['respuestas', ['reply']],
  ['retuits', ['retweet', 'unretweet']],
  ['meGusta', ['like', 'unlike']],
];

/** Lee las métricas de propagación visibles en la barra de acciones. */
function leerMetricas(articulo: Element): MetricasTuit {
  const metricas: MetricasTuit = {
    respuestas: null,
    retuits: null,
    meGusta: null,
    vistas: null,
  };

  for (const [campo, atributos] of ATRIBUTOS_DE_METRICA) {
    for (const atributo of atributos) {
      const nodo = propios(articulo, `[data-testid="${atributo}"]`)[0];
      const valor = leerContador(nodo ?? null);
      if (valor !== null) {
        metricas[campo] = valor;
        break;
      }
    }
  }

  // Las vistas no son un botón: X las publica como enlace al panel de métricas
  // de la publicación, y solo en algunas.
  metricas.vistas = leerContador(propios(articulo, 'a[href*="/analytics"]')[0] ?? null);

  return metricas;
}

/**
 * Lee un nodo del *timeline* y devuelve los datos del tuit.
 *
 * Devuelve `null` cuando el nodo no tiene texto, no tiene enlace permanente o
 * el enlace no responde a la forma esperada. Nunca lanza.
 */
export function leerTuit(articulo: Element): DatosTuit | null {
  try {
    if (!articulo || typeof articulo.querySelectorAll !== 'function') {
      return null;
    }

    const nodoTexto = propios(articulo, 'div[data-testid="tweetText"]')[0];
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

    return {
      tweetId: partes.tweetId,
      texto,
      handle: partes.handle,
      verificada: leerVerificacion(articulo),
      metricas: leerMetricas(articulo),
    };
  } catch {
    return null;
  }
}
