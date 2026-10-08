/**
 * *Content script*: recorre el *timeline* de X e inyecta un indicador sobre
 * cada tuit.
 *
 * El *timeline* está virtualizado —X monta y desmonta los artículos mientras
 * se desplaza—, así que no alcanza con recorrer el documento una vez: se
 * observa el árbol y cada artículo nuevo se procesa al aparecer. Los ya
 * procesados quedan marcados con un atributo propio para no duplicar el
 * indicador cuando el observador se dispara de nuevo sobre el mismo nodo.
 *
 * Este archivo no hace ninguna petición de red: los permisos de anfitrión y el
 * acceso al servicio viven en el *service worker*. La trayectoria de la cuenta
 * autora la lee el guion del mundo de la página (`src/pagina/index.ts`).
 */

import type { PedidoAnalisis, RespuestaAnalisis } from '../compartido/contrato';
import {
  ATRIBUTO_CUENTAS,
  EVENTO_LEER_CUENTAS,
  type CuentaLeida,
} from '../compartido/cuentas';
import type { MensajeAnalizar, RespuestaMensaje } from '../compartido/mensajes';
import { crearIndicador, ATRIBUTO_PROCESADO } from './indicador';
import { leerTuit, SELECTOR_TUIT, type DatosTuit } from './lector-dom';
import { conTiempoLimite } from './tiempo-limite';

/** Pide el análisis al *service worker*, que es quien habla con el servicio. */
async function pedirAnalisis(
  datos: DatosTuit,
  articulo: Element,
): Promise<RespuestaAnalisis> {
  // El pedido viaja en la nomenclatura del contrato del servicio, que es
  // separada por guiones bajos; el lector trabaja con la del propio TypeScript.
  const mensaje: MensajeAnalizar = {
    tipo: 'analizar',
    pedido: {
      tweet_id: datos.tweetId,
      texto: datos.texto,
      handle: datos.handle,
      verificada: datos.verificada,
      metricas: {
        respuestas: datos.metricas.respuestas,
        retuits: datos.metricas.retuits,
        me_gusta: datos.metricas.meGusta,
        vistas: datos.metricas.vistas,
      },
      cuenta: cuentaDe(articulo, datos.handle),
    },
  };

  const respuesta = (await chrome.runtime.sendMessage(
    mensaje,
  )) as RespuestaMensaje<RespuestaAnalisis> | undefined;

  if (!respuesta) {
    throw new Error('El *service worker* no respondió');
  }
  if (!respuesta.ok) {
    throw new Error(respuesta.error);
  }
  return respuesta.datos;
}

/**
 * La trayectoria de la cuenta autora, o nada si no se pudo leer.
 *
 * El evento se despacha en forma síncrona: cuando `dispatchEvent` vuelve, el
 * guion de la página ya dejó su respuesta en el atributo, o no la dejó porque
 * no encontró nada.
 */
function cuentaDe(articulo: Element, handle: string): PedidoAnalisis['cuenta'] {
  articulo.removeAttribute(ATRIBUTO_CUENTAS);
  articulo.dispatchEvent(new CustomEvent(EVENTO_LEER_CUENTAS));
  try {
    const cuentas = JSON.parse(articulo.getAttribute(ATRIBUTO_CUENTAS) ?? '{}') as Record<
      string,
      CuentaLeida
    >;
    return cuentas[handle.toLowerCase()];
  } catch {
    return undefined;
  }
}

/**
 * Traduce una falla a lo que el ciudadano tiene que leer y hacer.
 *
 * Dos fallas del propio Chrome llegaban acá con su texto interno en inglés y se
 * imprimían tal cual en una interfaz en castellano. La peor de las dos es
 * «Extension context invalidated»: la extensión se recargó o se actualizó, y el
 * *content script* que ya estaba en esta pestaña quedó atado a una extensión que
 * ya no existe. No hay reintento posible —el vínculo está roto hasta que la
 * pestaña se recargue— y ofrecer uno deja a la persona tocando una ficha muerta
 * en lugar de hacer lo único que lo arregla.
 */
function leerFalla(error: unknown): { texto: string; reintentable: boolean } {
  const crudo = error instanceof Error ? error.message : '';

  if (crudo.includes('Extension context invalidated')) {
    return {
      texto: 'La extensión se actualizó. Recargá la pestaña para volver a analizar',
      reintentable: false,
    };
  }
  // El *service worker* de Manifest V3 se suspende solo tras unos segundos sin
  // trabajo. Al despertarlo el primer mensaje se puede perder, y ahí el
  // reintento es exactamente lo que corresponde.
  if (crudo.includes('Receiving end does not exist')) {
    return { texto: 'El servicio de la extensión estaba dormido', reintentable: true };
  }

  return { texto: crudo || 'Error desconocido', reintentable: true };
}

/** Inserta el indicador debajo del texto del tuit, sin tocar el resto. */
function insertar(articulo: Element, anfitrion: HTMLElement): void {
  const nodoTexto = articulo.querySelector('div[data-testid="tweetText"]');
  const contenedor = nodoTexto?.parentElement;
  if (contenedor && nodoTexto) {
    contenedor.insertBefore(anfitrion, nodoTexto.nextSibling);
    return;
  }
  articulo.append(anfitrion);
}

/** Procesa un artículo del *timeline*, si es analizable y todavía no se vio. */
function procesar(articulo: Element): void {
  if (articulo.hasAttribute(ATRIBUTO_PROCESADO)) {
    return;
  }

  const datos = leerTuit(articulo);
  if (!datos) {
    // Un nodo sin los atributos esperados se saltea y se marca igual, para no
    // volver a intentarlo en cada disparo del observador.
    articulo.setAttribute(ATRIBUTO_PROCESADO, 'omitido');
    return;
  }

  articulo.setAttribute(ATRIBUTO_PROCESADO, datos.tweetId);

  let enCurso = false;
  const indicador = crearIndicador(datos.handle, () => {
    if (enCurso) {
      return;
    }
    enCurso = true;
    indicador.mostrarAnalizando();
    // El seguro que garantiza que el estado transitorio termine siempre, aunque
    // el *service worker* nunca conteste. Ver `tiempo-limite.ts`.
    conTiempoLimite(pedirAnalisis(datos, articulo))
      .then((analisis) => indicador.mostrarVeredicto(analisis))
      .catch((error: unknown) => {
        const falla = leerFalla(error);
        indicador.mostrarError(falla.texto, falla.reintentable);
      })
      .finally(() => {
        enCurso = false;
      });
  });

  insertar(articulo, indicador.anfitrion);
}

/** Recorre el subárbol recibido en busca de tuits sin procesar. */
function recorrer(raiz: ParentNode): void {
  for (const articulo of Array.from(raiz.querySelectorAll(SELECTOR_TUIT))) {
    procesar(articulo);
  }
}

function arrancar(): void {
  recorrer(document);

  const observador = new MutationObserver((mutaciones) => {
    for (const mutacion of mutaciones) {
      for (const nodo of Array.from(mutacion.addedNodes)) {
        if (!(nodo instanceof Element)) {
          continue;
        }
        if (nodo.matches(SELECTOR_TUIT)) {
          procesar(nodo);
        } else {
          recorrer(nodo);
        }
      }
    }
  });

  observador.observe(document.body, { childList: true, subtree: true });
}

arrancar();
