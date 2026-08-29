/**
 * El movimiento de la interfaz.
 *
 * Hay **un solo gesto** y todo lo demás es acuse de recibo. El gesto es que la
 * tarjeta crece: el indicador, el detalle y el panel de evidencia son una misma
 * ficha que se abre en tres tiempos, nunca tres tarjetas apiladas. El código ya
 * afirmaba eso en prosa —la ficha suelta sus esquinas de abajo, el detalle no
 * pinta borde superior— pero lo animaba como una capa que entraba deslizándose
 * desde arriba, que es el movimiento de algo que llega de otro lado. Acá se
 * anima la altura, que es el movimiento de algo que ya estaba y se despliega.
 *
 * La altura se anima con la API de animaciones y no con una transición de CSS
 * porque el alto de destino no se conoce hasta después de insertar el nodo: se
 * mide y se anima hacia el valor medido, y al terminar se suelta para que el
 * contenido pueda volver a crecer por su cuenta —al abrir la evidencia dentro
 * del detalle, por ejemplo—.
 *
 * El repliegue existe y dura menos que el despliegue. Cerrar de golpe lo que se
 * abrió con una curva es la asimetría que delata que el movimiento se agregó
 * encima en lugar de pertenecer a la pieza.
 */

/** Entrada: asentado largo, la curva de X. */
const ENTRADA_MS = 260;
/** Salida: más corta que la entrada. Lo que se va no necesita explicarse. */
const SALIDA_MS = 160;
const CURVA = 'cubic-bezier(0.16, 1, 0.3, 1)';

/**
 * Si la persona pidió menos movimiento, o si el entorno no anima.
 *
 * `matchMedia` no existe en el entorno de pruebas y `Element.animate` tampoco:
 * en ambos casos la respuesta correcta es la misma, que es hacer el cambio de
 * estado sin animarlo. Un panel que se abre instantáneamente sigue siendo un
 * panel que se abre.
 */
function sinMovimiento(elemento: HTMLElement): boolean {
  if (typeof elemento.animate !== 'function') {
    return true;
  }
  if (typeof window.matchMedia !== 'function') {
    return false;
  }
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

/** La animación en curso de cada nodo, para poder interrumpirla. */
const enCurso = new WeakMap<HTMLElement, Animation>();

/**
 * Despliega un nodo recién insertado creciéndolo desde el alto cero.
 *
 * La opacidad resuelve antes que la altura —a un 45% del recorrido— para que el
 * contenido esté legible mientras el borde inferior todavía baja. Al revés, el
 * texto termina de aparecer después de que el panel dejó de moverse y la
 * apertura se lee en dos tiempos.
 */
export function desplegar(elemento: HTMLElement): void {
  enCurso.get(elemento)?.cancel();
  if (sinMovimiento(elemento)) {
    return;
  }

  const alto = elemento.scrollHeight;
  const animacion = elemento.animate(
    [
      { height: '0px', opacity: 0, offset: 0 },
      { opacity: 1, offset: 0.45 },
      { height: `${alto}px`, opacity: 1, offset: 1 },
    ],
    { duration: ENTRADA_MS, easing: CURVA },
  );
  enCurso.set(elemento, animacion);
}

/**
 * Repliega un nodo hasta el alto cero y avisa cuando terminó.
 *
 * `alTerminar` es donde el llamador lo quita del documento, y **solo** corre si
 * la animación llegó al final: una animación cancelada es un repliegue que la
 * persona interrumpió volviendo a abrir, y ahí el nodo tiene que quedarse.
 */
export function replegar(elemento: HTMLElement, alTerminar: () => void): void {
  enCurso.get(elemento)?.cancel();
  if (sinMovimiento(elemento)) {
    alTerminar();
    return;
  }

  const alto = elemento.getBoundingClientRect().height;
  const animacion = elemento.animate(
    [
      { height: `${alto}px`, opacity: 1, offset: 0 },
      { opacity: 0, offset: 0.7 },
      { height: '0px', opacity: 0, offset: 1 },
    ],
    { duration: SALIDA_MS, easing: 'ease-in', fill: 'forwards' },
  );
  enCurso.set(elemento, animacion);
  animacion.addEventListener('finish', () => {
    enCurso.delete(elemento);
    alTerminar();
  });
}
