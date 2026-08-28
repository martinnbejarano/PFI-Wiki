/**
 * *Service worker* de Manifest V3.
 *
 * Es el único componente de la extensión que hace peticiones de red, y su
 * único destino es el servicio local declarado en los permisos de anfitrión
 * del manifiesto. No conoce ninguna credencial: la clave del proveedor vive
 * solo en el entorno del servicio y nunca viaja dentro de un artefacto que
 * cualquiera puede desempaquetar.
 */

import type { RespuestaAnalisis } from '../compartido/contrato';
import type { MensajeEntrante, RespuestaMensaje } from '../compartido/mensajes';

/** Base del servicio local. El prototipo no se despliega: todo corre local. */
const BASE_DEL_SERVICIO = 'http://localhost:8000';

/**
 * Tiempo límite de la petición al servicio.
 *
 * Tiene que ser **más holgado que el presupuesto del servicio**, no más
 * ajustado. El servicio es el único que sabe cuánto lleva gastado y cuál de sus
 * pasos no llegó, así que es el que tiene que hacer cumplir el plazo: al
 * agotarlo devuelve un análisis parcial que dice qué módulo falta (RNF-11).
 * Si el cliente cortara antes, cambiaría esa respuesta explicada por un error
 * de red que no puede explicar nada.
 *
 * El presupuesto del servicio es de 45 s (`tiempo_limite_total_s`) y se
 * comprueba entre paso y paso, de modo que un paso ya empezado puede estirarlo
 * hasta unos 60 s en el peor caso. Este plazo queda por encima de ese techo.
 *
 * El valor anterior era de 15 s y cortaba análisis que el servicio completaba:
 * una medición real del 2026-08-28 dio 20,2 s de extremo a extremo.
 */
const LIMITE_MS = 75_000;

async function pedir<T>(ruta: string, cuerpo?: unknown): Promise<T> {
  const control = new AbortController();
  const temporizador = setTimeout(() => control.abort(), LIMITE_MS);
  try {
    const respuesta = await fetch(`${BASE_DEL_SERVICIO}${ruta}`, {
      method: cuerpo === undefined ? 'GET' : 'POST',
      headers: cuerpo === undefined ? undefined : { 'Content-Type': 'application/json' },
      body: cuerpo === undefined ? undefined : JSON.stringify(cuerpo),
      signal: control.signal,
    });
    if (!respuesta.ok) {
      throw new Error(`El servicio respondió ${respuesta.status}`);
    }
    return (await respuesta.json()) as T;
  } finally {
    clearTimeout(temporizador);
  }
}

/**
 * Traduce cualquier fallo a un mensaje legible.
 *
 * Nunca se propaga un error opaco hacia la interfaz: RNF-11 exige que lo que
 * llegue al ciudadano sea siempre algo que pueda interpretar.
 */
function explicar(error: unknown): string {
  if (error instanceof DOMException && error.name === 'AbortError') {
    return 'El servicio tardó demasiado';
  }
  if (error instanceof TypeError) {
    return 'No se pudo contactar al servicio local';
  }
  return error instanceof Error ? error.message : 'Error desconocido';
}

chrome.runtime.onMessage.addListener((mensaje: MensajeEntrante, _emisor, responder) => {
  if (mensaje?.tipo === 'analizar') {
    pedir<RespuestaAnalisis>('/analizar', mensaje.pedido)
      .then((datos) => responder({ ok: true, datos } satisfies RespuestaMensaje<RespuestaAnalisis>))
      .catch((error: unknown) =>
        responder({ ok: false, error: explicar(error) } satisfies RespuestaMensaje<never>),
      );
    // Devolver `true` mantiene abierto el canal hasta que llegue la respuesta.
    return true;
  }

  if (mensaje?.tipo === 'salud') {
    pedir<{ estado: string }>('/salud')
      .then((datos) => responder({ ok: true, datos }))
      .catch((error: unknown) => responder({ ok: false, error: explicar(error) }));
    return true;
  }

  return false;
});
