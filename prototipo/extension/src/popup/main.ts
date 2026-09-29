/**
 * Ventana emergente de la extensión.
 *
 * Informa si el servicio local está en pie, abre el panel web con el
 * histórico de esta instalación (CU-05) y muestra la finalidad y la vía de
 * supresión (RF-12).
 */

import type { MensajeAbrirPanel, MensajeSalud, RespuestaMensaje } from '../compartido/mensajes';

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

document.getElementById('historico')?.addEventListener('click', () => {
  const mensaje: MensajeAbrirPanel = { tipo: 'abrir-panel' };
  void chrome.runtime.sendMessage(mensaje);
});
