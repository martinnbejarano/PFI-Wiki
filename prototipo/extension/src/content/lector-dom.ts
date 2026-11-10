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

/**
 * Selector de los tuits del *timeline*.
 *
 * X tiene dos marcados en circulación: el clásico, con `data-testid`, y el de
 * noviembre de 2026, que ya no los trae y envuelve cada `article` en un
 * `div[role="link"]` con la ruta de la publicación en `data-href`. Se aceptan los
 * dos mientras convivan.
 */
export const SELECTOR_TUIT = 'article[data-testid="tweet"], [role="link"][data-href*="/status/"] > article';

/**
 * Devuelve el nodo del texto de la publicación: `tweetText` en el marcado
 * clásico, el primer `div[dir="auto"]` propio en el nuevo.
 */
export function nodoTexto(articulo: Element): Element | null {
  return (
    propios(articulo, 'div[data-testid="tweetText"]')[0] ??
    propios(articulo, 'div[dir="auto"]')[0] ??
    null
  );
}

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
  /**
   * Si la cuenta autora es protegida: X dibuja un candado junto al nombre.
   * RNF-09 la excluye del análisis.
   */
  protegida: boolean;
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
    return (
      propios(articulo, 'svg[data-testid="icon-verified"]').length > 0 ||
      propios(articulo, '[aria-label]').some((nodo) =>
        /^(cuenta verificada|verified account)$/i.test(nodo.getAttribute('aria-label') ?? ''),
      )
    );
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

  // Marcado nuevo: sin `data-testid`, el número va en la etiqueta accesible del
  // botón («1422 reposts. Repost», «12589 Likes. Like»).
  const etiquetas: ReadonlyArray<readonly [keyof MetricasTuit, RegExp]> = [
    ['respuestas', /(repl(y|ies)|respuestas?)\b/i],
    ['retuits', /(reposts?|retweets?)\b/i],
    ['meGusta', /(likes?|me gusta)\b/i],
  ];
  const botones = propios(articulo, 'button[aria-label]');
  for (const [campo, patron] of etiquetas) {
    if (metricas[campo] !== null) continue;
    const boton = botones.find((b) => /\d/.test(b.getAttribute('aria-label') ?? '') && patron.test(b.getAttribute('aria-label') ?? ''));
    metricas[campo] = leerContador(boton ?? null);
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

    const texto = nodoTexto(articulo)?.textContent?.trim() ?? '';
    if (!texto) {
      return null;
    }

    // Una publicación citada del marcado nuevo es otro `article` anidado: la
    // procesa el artículo que la contiene, no ella misma.
    if (articulo.parentElement?.closest('article')) {
      return null;
    }

    const enlace = enlacePermanente(articulo);
    // `getAttribute` y no `.href`: interesa la ruta relativa tal como está en
    // el marcado, no la URL absoluta que el DOM resuelve. El marcado nuevo no
    // envuelve la fecha en el enlace y deja la ruta en `data-href` del contenedor.
    const href =
      enlace?.getAttribute('href') ??
      articulo.parentElement?.closest('[data-href*="/status/"]')?.getAttribute('data-href') ??
      '';
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
      // ponytail: el candado se identifica por su `data-testid`, como la
      // insignia de verificación; falta confirmarlo sobre una cuenta protegida real.
      protegida:
        propios(articulo, 'div[data-testid="User-Name"] svg[data-testid="icon-lock"]').length > 0 ||
        propios(articulo, '[aria-label]').some((nodo) =>
          /^(cuenta protegida|protected account)$/i.test(nodo.getAttribute('aria-label') ?? ''),
        ),
    };
  } catch {
    return null;
  }
}
