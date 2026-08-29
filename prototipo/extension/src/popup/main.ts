/**
 * Ventana emergente de la extensión.
 *
 * Solo informa si el servicio local está en pie. El detalle del veredicto y el
 * panel de evidencia son pantallas de los tickets siguientes.
 */

import type { MensajeSalud, RespuestaMensaje } from '../compartido/mensajes';

const nodo = document.getElementById('estado');

function pintar(clase: string, texto: string): void {
  if (!nodo) {
    return;
  }
  nodo.className = `estado ${clase}`;
  nodo.textContent = texto;
}

async function consultar(): Promise<void> {
  const mensaje: MensajeSalud = { tipo: 'salud' };
  const respuesta = (await chrome.runtime.sendMessage(mensaje)) as
    | RespuestaMensaje<{ estado: string }>
    | undefined;

  if (respuesta?.ok) {
    pintar('vivo', 'Servicio local en pie');
    return;
  }
  pintar('caido', respuesta?.error ?? 'No se pudo contactar al servicio local');
}

void consultar();
