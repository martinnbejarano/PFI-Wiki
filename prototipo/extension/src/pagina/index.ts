/**
 * Lee la trayectoria de la cuenta autora de un tuit que ya está en pantalla.
 *
 * Corre en el mundo de la página (`"world": "MAIN"`) porque es el único que ve
 * las propiedades que React cuelga de cada nodo (`__reactFiber$…`): el *content
 * script* vive en un mundo aislado y no las alcanza. X arma cada tuit con el
 * objeto completo de su autor, y de ahí se copian la fecha de creación, los
 * seguidores y los seguidos.
 *
 * **No hace ningún pedido propio.** Lee lo que la plataforma ya entregó al
 * navegador de la persona y ya está dibujado en su pantalla: el mismo acto que
 * el lector del DOM, un nivel más abajo. Es lo que sostiene el argumento de la
 * viabilidad legal del cap. 3 y lo que lo deja fuera del presupuesto de RNF-02.
 *
 * **Cómo se comunica.** El *content script* dispara `EVENTO_LEER_CUENTAS` sobre
 * el artículo al pedir el análisis. Los eventos del DOM cruzan los dos mundos y
 * se despachan en forma síncrona, así que este guion deja la respuesta en el
 * atributo `ATRIBUTO_CUENTAS` del artículo antes de que el *content script*
 * vuelva de `dispatchEvent`. Si X cambia su estructura interna, no se encuentra
 * ninguna cuenta y el Módulo 2 queda sin datos: el análisis sigue sin él.
 */

import {
  ATRIBUTO_CUENTAS,
  EVENTO_LEER_CUENTAS,
  type CuentaLeida,
} from '../compartido/cuentas';

type Objeto = Record<string, unknown>;

// Cuánto se sube por el árbol de React desde el artículo y cuánto se baja en
// las propiedades de cada nodo. El autor apareció a 14 niveles en las pruebas
// sobre x.com del 2026-10-08; el margen cubre cambios menores de X.
const NIVELES_HACIA_ARRIBA = 25;
const PROFUNDIDAD_DE_PROPIEDADES = 6;

function esObjeto(valor: unknown): valor is Objeto {
  return typeof valor === 'object' && valor !== null;
}

/** Interpreta un objeto como cuenta de X, o `null` si no lo es. */
function leerCuenta(nodo: Objeto): [string, CuentaLeida] | null {
  const { screen_name, followers_count, friends_count, created_at } = nodo;
  if (typeof screen_name !== 'string' || typeof followers_count !== 'number') {
    return null;
  }
  // X entrega la fecha en ISO o en el formato clásico de su API; `Date` lee los dos.
  const creada = new Date(String(created_at));
  if (Number.isNaN(creada.getTime())) {
    return null;
  }
  return [
    `@${screen_name.toLowerCase()}`,
    {
      creada: creada.toISOString(),
      seguidores: followers_count,
      seguidos: typeof friends_count === 'number' ? friends_count : 0,
    },
  ];
}

/**
 * Junta todas las cuentas que aparecen en las propiedades de un nodo de React
 * y de sus ancestros. Devuelve más de una cuando el tuit cita a otro: el
 * *content script* elige la del autor por su *handle*.
 */
export function cuentasDelNodo(fibra: unknown): Record<string, CuentaLeida> {
  const cuentas: Record<string, CuentaLeida> = {};
  const vistos = new WeakSet<object>();

  const juntar = (valor: unknown, profundidad: number): void => {
    if (!esObjeto(valor) || profundidad > PROFUNDIDAD_DE_PROPIEDADES || vistos.has(valor)) {
      return;
    }
    vistos.add(valor);
    const cuenta = leerCuenta(valor);
    if (cuenta) {
      cuentas[cuenta[0]] = cuenta[1];
    }
    for (const [clave, hijo] of Object.entries(valor)) {
      // `children` y los internos de React son elementos, no datos: recorrerlos
      // multiplica el costo sin encontrar nada.
      if (clave !== 'children' && !clave.startsWith('_')) {
        juntar(hijo, profundidad + 1);
      }
    }
  };

  let nodo: unknown = fibra;
  for (let nivel = 0; esObjeto(nodo) && nivel < NIVELES_HACIA_ARRIBA; nivel++) {
    juntar(nodo.memoizedProps, 0);
    nodo = nodo.return;
  }
  return cuentas;
}

function responder(evento: Event): void {
  const articulo = evento.target;
  if (!(articulo instanceof Element)) {
    return;
  }
  const clave = Object.keys(articulo).find((k) => k.startsWith('__reactFiber$'));
  if (!clave) {
    return;
  }
  try {
    const fibra = (articulo as unknown as Objeto)[clave];
    articulo.setAttribute(ATRIBUTO_CUENTAS, JSON.stringify(cuentasDelNodo(fibra)));
  } catch {
    // Una estructura inesperada deja al Módulo 2 sin datos, nada más.
  }
}

document.addEventListener(EVENTO_LEER_CUENTAS, responder, true);
