/**
 * Página del aviso de primer uso. Se abre al instalar (y desde la ventana
 * emergente); el botón «Acepto» guarda la aceptación con su versión.
 */

import { PUNTOS_DEL_AVISO, aceptarAviso, avisoAceptado } from '../compartido/aviso';

const lista = document.getElementById('puntos');
for (const punto of PUNTOS_DEL_AVISO) {
  const item = document.createElement('li');
  item.textContent = punto;
  lista?.append(item);
}

const boton = document.getElementById('acepto') as HTMLButtonElement | null;
const listo = document.getElementById('listo');

function mostrarAceptado(): void {
  if (boton) boton.disabled = true;
  if (listo) listo.hidden = false;
}

void avisoAceptado().then((aceptado) => aceptado && mostrarAceptado());
boton?.addEventListener('click', () => void aceptarAviso().then(mostrarAceptado));
