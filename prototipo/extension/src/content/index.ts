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
 * acceso al servicio viven en el *service worker*.
 */

import type { RespuestaAnalisis } from '../compartido/contrato';
import type { MensajeAnalizar, RespuestaMensaje } from '../compartido/mensajes';
import { crearIndicador, ATRIBUTO_PROCESADO } from './indicador';
import { leerTuit, SELECTOR_TUIT, type DatosTuit } from './lector-dom';

/** Pide el análisis al *service worker*, que es quien habla con el servicio. */
async function pedirAnalisis(datos: DatosTuit): Promise<RespuestaAnalisis> {
  const mensaje: MensajeAnalizar = {
    tipo: 'analizar',
    pedido: { tweet_id: datos.tweetId, texto: datos.texto, handle: datos.handle },
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
  const indicador = crearIndicador(() => {
    if (enCurso) {
      return;
    }
    enCurso = true;
    indicador.mostrarAnalizando();
    pedirAnalisis(datos)
      .then((analisis) => indicador.mostrarVeredicto(analisis))
      .catch((error: unknown) => {
        const mensaje = error instanceof Error ? error.message : 'Error desconocido';
        indicador.mostrarError(mensaje);
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
