/**
 * Lee la trayectoria de las cuentas en las respuestas que X ya recibió.
 *
 * Corre en el mundo de la página (`"world": "MAIN"`), antes que el código de X,
 * y envuelve `fetch` y `XMLHttpRequest` para **mirar** las respuestas de la API
 * interna (`/i/api/graphql/`) con las que X arma el *timeline*. Cada tuit viene
 * con el objeto completo de su autor, y de ahí se copian la fecha de creación,
 * los seguidores y los seguidos. Se reenvían al *content script* por
 * `postMessage`.
 *
 * **No hace ningún pedido propio.** Lee datos que la plataforma ya entregó al
 * navegador de la persona, dentro de su sesión: es el mismo acto que el lector
 * del DOM, un nivel más abajo. Es lo que sostiene el argumento de la viabilidad
 * legal del cap. 3 y lo que mantiene fuera del presupuesto de RNF-02.
 *
 * Si X cambia la forma de sus respuestas, no se encuentra ninguna cuenta y el
 * Módulo 2 queda sin datos: el análisis sigue igual sin él.
 */

import { MENSAJE_CUENTAS, type CuentaLeida } from '../compartido/cuentas';

const API_DE_X = '/i/api/graphql/';

type Objeto = Record<string, unknown>;

function esObjeto(valor: unknown): valor is Objeto {
  return typeof valor === 'object' && valor !== null;
}

/** Interpreta un objeto como cuenta de X, o `null` si no lo es. */
export function leerCuenta(nodo: Objeto): CuentaLeida | null {
  const legacy = nodo.legacy;
  if (!esObjeto(legacy) || typeof legacy.followers_count !== 'number') {
    return null;
  }
  // X fue mudando el nombre y la fecha de `legacy` a `core`; se aceptan ambos.
  const core = esObjeto(nodo.core) ? nodo.core : {};
  const handle = legacy.screen_name ?? core.screen_name;
  const creada = new Date(String(legacy.created_at ?? core.created_at));
  if (typeof handle !== 'string' || Number.isNaN(creada.getTime())) {
    return null;
  }
  return {
    handle: `@${handle}`,
    creada: creada.toISOString(),
    seguidores: legacy.followers_count,
    seguidos: typeof legacy.friends_count === 'number' ? legacy.friends_count : 0,
  };
}

/** Recorre una respuesta entera y junta todas las cuentas que aparecen. */
export function buscarCuentas(raiz: unknown): CuentaLeida[] {
  const encontradas: CuentaLeida[] = [];
  const pendientes: unknown[] = [raiz];
  while (pendientes.length > 0) {
    const nodo = pendientes.pop();
    if (!esObjeto(nodo)) {
      continue;
    }
    const cuenta = leerCuenta(nodo);
    if (cuenta) {
      encontradas.push(cuenta);
    }
    pendientes.push(...Object.values(nodo));
  }
  return encontradas;
}

function publicar(texto: string): void {
  try {
    const cuentas = buscarCuentas(JSON.parse(texto));
    if (cuentas.length > 0) {
      window.postMessage({ tipo: MENSAJE_CUENTAS, cuentas }, window.location.origin);
    }
  } catch {
    // Una respuesta que no es JSON no trae cuentas.
  }
}

function instalar(): void {
  const fetchOriginal = window.fetch;
  window.fetch = async function (...argumentos: Parameters<typeof fetch>) {
    const respuesta = await fetchOriginal.apply(this, argumentos);
    if (respuesta.url.includes(API_DE_X)) {
      respuesta.clone().text().then(publicar, () => {});
    }
    return respuesta;
  };

  const abrir = XMLHttpRequest.prototype.open;
  XMLHttpRequest.prototype.open = function (
    this: XMLHttpRequest,
    ...argumentos: Parameters<XMLHttpRequest['open']>
  ) {
    if (String(argumentos[1]).includes(API_DE_X)) {
      this.addEventListener('load', () => {
        if (this.responseType === '' || this.responseType === 'text') {
          publicar(this.responseText);
        }
      });
    }
    return abrir.apply(this, argumentos);
  } as XMLHttpRequest['open'];
}

instalar();
