/**
 * Informe de un veredicto incorrecto (RF-11, CU-04), desde el pie del detalle.
 *
 * El botón despliega un formulario con el tipo de error y el motivo; el envío
 * lo hace el *service worker*, que agrega el identificador anónimo de la
 * instalación. El servicio confirma la recepción y eso es lo que se muestra.
 *
 * No se implementa el flujo alternativo de la ficha —conservar el informe
 * localmente y reintentarlo en la sesión siguiente—: ante una falla se dice
 * que no se pudo enviar y el formulario queda para reintentar a mano.
 */

import type { PedidoReporte, TipoError } from '../compartido/contrato';
import type { MensajeReportar, RespuestaMensaje } from '../compartido/mensajes';

export const ESTILOS_REPORTE = `
.reporte { display: grid; gap: 10px; padding: 12px 14px; border-top: 1px solid var(--borde); font-size: 14px; }
.reporte[hidden] { display: none; }
.reporte fieldset { display: grid; gap: 6px; margin: 0; padding: 0; border: 0; }
.reporte legend { margin-bottom: 4px; font-weight: 700; }
.reporte textarea {
  min-height: 60px; padding: 8px; border: 1px solid var(--borde-vivo); border-radius: 8px;
  background: transparent; color: var(--tinta); font: inherit; resize: vertical;
}
.reporte-estado { margin: 0; color: var(--tinta-media); }
`;

const FORMULARIO = `
<fieldset>
  <legend>¿Qué tipo de error es?</legend>
  <label><input type="radio" name="tipo" value="falso_positivo" required>
    Falso positivo: marcó como dudosa una afirmación verdadera</label>
  <label><input type="radio" name="tipo" value="falso_negativo">
    Falso negativo: dio por buena una afirmación falsa</label>
</fieldset>
<label>Motivo<br><textarea name="motivo" maxlength="2000"
  placeholder="Por qué el veredicto es incorrecto"></textarea></label>
<div><button type="submit" class="btn pri">Enviar informe</button></div>
<p class="reporte-estado" role="status"></p>
`;

/** Agrega el botón al pie y el formulario al panel. */
export function agregarReporte(panel: HTMLElement, pie: HTMLElement, tweetId: string): void {
  const boton = document.createElement('button');
  boton.type = 'button';
  boton.className = 'btn sec';
  boton.textContent = 'Informar un error';
  boton.setAttribute('aria-expanded', 'false');

  const formulario = document.createElement('form');
  formulario.className = 'reporte';
  formulario.hidden = true;
  formulario.innerHTML = FORMULARIO;
  const estado = formulario.querySelector<HTMLElement>('.reporte-estado')!;
  const enviar = formulario.querySelector<HTMLButtonElement>('button[type="submit"]')!;

  boton.addEventListener('click', () => {
    formulario.hidden = !formulario.hidden;
    boton.setAttribute('aria-expanded', String(!formulario.hidden));
  });

  formulario.addEventListener('submit', (evento) => {
    evento.preventDefault();
    const datos = new FormData(formulario);
    const reporte: PedidoReporte = {
      tweet_id: tweetId,
      tipo: datos.get('tipo') as TipoError,
      motivo: String(datos.get('motivo') ?? '').trim(),
    };
    const mensaje: MensajeReportar = { tipo: 'reportar', reporte };
    enviar.disabled = true;
    estado.textContent = 'Enviando…';
    chrome.runtime
      .sendMessage(mensaje)
      .then((respuesta: RespuestaMensaje<unknown> | undefined) => {
        if (!respuesta?.ok) {
          throw new Error(respuesta?.error ?? 'Sin respuesta');
        }
        formulario.replaceChildren(estado);
        estado.textContent =
          'Recibimos tu informe. Queda registrado para la revisión de errores del modelo.';
        boton.remove();
      })
      .catch((error: unknown) => {
        enviar.disabled = false;
        estado.textContent = `No se pudo enviar el informe (${
          error instanceof Error ? error.message : 'error desconocido'
        }). Probá de nuevo.`;
      });
  });

  pie.append(boton);
  panel.append(formulario);
}
