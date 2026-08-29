/**
 * Panel de evidencia (RF-09, CU-03): la tercera pantalla del *mockup*.
 *
 * El marcado y el CSS se portan de la pantalla `?pantalla=evidencia` de
 * `wiki/assets/mockups/mockups.html`, igual que el indicador se portó de
 * `?pantalla=badge` y el detalle de `?pantalla=popup`. Los nombres de clase son
 * los del *mockup* —`.evid`, `.e-grupo`, `.fuente`,
 * `.postura`, `.p-contra`, `.p-corro`, `.p-neutro`, `.f-cuerpo`, `.f-org`,
 * `.f-tit`— para que la correspondencia con la figura impresa en el documento
 * se pueda verificar leyendo.
 *
 * **Es el diferencial del proyecto entero.** El usuario ve, junto al veredicto,
 * las fuentes que lo respaldan, cada una enlazada al documento original. Es lo
 * que sostiene RNF-06 y lo que ningún competidor de la matriz comparativa le
 * entrega al ciudadano: no un veredicto, sino el camino para no depender del
 * veredicto.
 *
 * Dos decisiones de esa pantalla que este archivo respeta y no reinterpreta:
 *
 * 1. **Las fuentes van agrupadas y ordenadas según la jerarquía de evidencia**
 *    —primero las oficiales, después los medios de referencia, al final las
 *    verificaciones previas—. Según `wiki/solucion/mockups.md`, el orden es la
 *    decisión de fondo de la pantalla. El servicio ya devuelve `fuentes` en ese
 *    orden; acá solo se las agrupa, y el orden de los grupos sale de
 *    `ORDEN_DE_LA_JERARQUIA`, que es el mismo de `servicio/app/jerarquia.py`.
 * 2. **Arriba de todo va la afirmación verificable extraída, con su tipo.**
 *    Muestra que el sistema no compara el tuit entero contra internet sino una
 *    afirmación acotada, y explicita cuál: si la extrajo mal, el usuario lo ve
 *    en la primera línea y entiende por qué el veredicto no le cierra.
 *
 * Tres divergencias respecto de la figura, todas deliberadas:
 *
 * 1. **No se dibuja la cita textual** (`.f-cita`) ni la antigüedad de la
 *    publicación que la figura pone en `.f-org`. El contrato de la respuesta
 *    trae de cada fuente el título, la URL, el tipo y la postura, y nada más.
 *    Inventar una cita o una fecha para completar el dibujo sería fabricar
 *    justamente la evidencia que esta pantalla existe para mostrar. La clase se
 *    conserva en la hoja de estilos para cuando el dato exista.
 * 2. **El ancho** es fluido con un tope de 620 px, el de la tarjeta del
 *    *mockup*, por el mismo motivo que en el detalle: el panel se inserta dentro
 *    de la columna del tuit, que en pantallas angostas mide menos.
 * 3. **El rótulo de la postura que corrobora dice «Corrobora», y la figura dice
 *    «Corrobora parcialmente».** El patrón visual —la clase `.p-corro` y su
 *    color— se porta tal cual; lo que no se porta es el adverbio, porque el
 *    contrato tiene tres posturas y ninguna es «parcialmente». Escribir
 *    «parcialmente» sobre una fuente que el sistema etiquetó `corrobora` sería
 *    agregarle al dato un matiz que el dato no trae.
 */

import type { Fuente, RespuestaAnalisis, TipoFuente } from '../compartido/contrato';
import { escribirEnlaceSaliente } from './tema';

/**
 * Estilos del panel de evidencia, portados del *mockup*.
 *
 * Se declaran sobre `.evid` y no sobre `:host` porque el indicador ya reclama
 * `:host` con `all: initial` y las tres hojas comparten el mismo *shadow DOM*.
 * Los valores son los mismos del `:root` del *mockup*.
 */
// Fichas, iconos y marca compartidos por las tres superficies.
export const ESTILOS_EVIDENCIA = `
/* -- El panel de evidencia ---------------------------------------------- */
/*
 * Es la pantalla que sostiene la propuesta de valor: no el veredicto, sino el
 * camino para no depender del veredicto. Se despliega dentro del detalle y
 * toma la forma de lista de X —filas separadas por una linea de 1, velo al
 * pasar por encima, titulo en 15 y meta apagada en 13—, que es como X presenta
 * cualquier coleccion de items.
 */
.evid {
  border-top: 1px solid var(--borde);
  color: var(--tinta);
  font: 400 15px/20px var(--letra);
}



/* -- Los escalones de la jerarquia -------------------------------------- */
/*
 * El orden de los grupos es la decision de fondo de esta pantalla, asi que se
 * dibuja: cada escalon se anuncia con su propio encabezado y las fuentes
 * oficiales van siempre primero.
 */
.evid .e-grupo { border-top: 1px solid var(--borde); padding: 14px 14px 4px; }
/*
 * El filete que abre el panel lo pone el panel y no el primer grupo: apilados,
 * los dos trazos de 1 daban una costura de 2 que no aparece en ninguna otra
 * juntura de la tarjeta y delataba que son dos piezas y no una.
 */
.evid > .e-grupo:first-child { border-top: 0; }
.evid .e-grupo h3 {
  margin: 0 0 2px;
  color: var(--tinta-media);
  font: 700 13px/16px var(--letra);
  letter-spacing: 0.02em;
  text-transform: uppercase;
}

/* -- La fila de una fuente ---------------------------------------------- */
.evid .fuente {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: baseline;
  gap: 2px 12px;
  padding: 10px;
  margin-inline: -10px;
  border-radius: var(--radio-chico);
}
.evid .fuente + .fuente { border-top: 1px solid var(--borde); }
/* El velo al pasar por encima, que es lo que le da destino al radio de la fila. */
.evid .fuente:hover { background: var(--velo); }
/*
 * Las fuentes aterrizan una detras de otra mientras el panel crece. Es el unico
 * escalonado de la interfaz y esta donde el producto se juega: lo que el sistema
 * promete no es el veredicto sino las fuentes, y verlas llegar de a una es esa
 * promesa cumpliendose. El retardo se corta a la sexta fila: la variable de
 * indice no pasa de 6, para que una lista larga no se convierta en una espera.
 */
.evid .fuente {
  animation: aterrizar 0.34s var(--curva) both;
  animation-delay: calc(var(--i, 0) * 22ms);
}
@keyframes aterrizar {
  from { opacity: 0; transform: translateY(5px); }
  to { opacity: 1; transform: none; }
}
.evid .f-tit { grid-column: 1; margin: 0; font-size: 15px; line-height: 20px; }
.evid .f-tit a { color: var(--tinta); text-decoration: none; }
.evid .f-tit a:hover { color: var(--azul); text-decoration: underline; text-underline-offset: 2px; }
.evid .f-tit a:focus-visible { outline: 2px solid var(--azul); outline-offset: 2px; border-radius: 2px; }
/* El icono de salida es compartido: su regla vive en el modulo del tema. */
.evid .f-org {
  grid-column: 1;
  color: var(--tinta-media);
  font-size: 13px;
  line-height: 17px;
}
/*
 * El bloque que agrupa el origen y el titulo de una fuente. No reusa la clase
 * de cuerpo del *mockup*: esa rotula un parrafo —el resumen de la fuente, que
 * el contrato no trae— y usada de contenedor le imponia a la fila un margen
 * superior de 4 que descolgaba la pastilla de la postura de la linea con la que
 * esta alineada.
 */
.evid .f-datos { grid-column: 1; min-width: 0; }
.evid .f-cita {
  grid-column: 1;
  margin: 6px 0 0;
  padding-left: 10px;
  border-left: 1px solid var(--borde);
  color: var(--tinta-media);
  font-size: 14px;
  line-height: 19px;
}

/* -- La postura --------------------------------------------------------- */
/*
 * Va en pastilla y no en texto suelto porque es lo que el ciudadano usa para
 * pesar la evidencia por su cuenta. El color repite el del veredicto, de modo
 * que la lectura sea la misma arriba y abajo.
 */
.evid .postura {
  grid-column: 2;
  grid-row: 1;
  padding: 1px 9px;
  border: 1px solid currentColor;
  border-radius: var(--pastilla);
  font-size: 12px;
  line-height: 17px;
  font-weight: 700;
  white-space: nowrap;
}
.evid .p-contra { color: var(--rojo); }
.evid .p-corro { color: var(--verde); }
.evid .p-neutro { color: var(--tinta-media); }

@media (prefers-reduced-motion: reduce) {
  /*
   * Sin el escalonado las fuentes siguen apareciendo: lo que se quita es el
   * desplazamiento, no el hecho de que la lista llegue.
   */
  .evid .fuente { animation: none; }
}
`;

/**
 * El orden de los grupos, que es el de la jerarquía de evidencia.
 *
 * Es el mismo orden que `JERARQUIA_DE_EVIDENCIA` declara en
 * `servicio/app/jerarquia.py`, y la duplicación está declarada como tal: el
 * contrato viaja por HTTP y no hay generación automática entre los dos lados,
 * igual que con `compartido/contrato.ts`.
 */
const ORDEN_DE_LA_JERARQUIA: readonly TipoFuente[] = [
  'fuente_oficial',
  'medio_de_referencia',
  'verificacion_previa',
];

/** Título del grupo de cada escalón, tal como lo rotula el *mockup*. */
const TITULO_DE_GRUPO: Record<TipoFuente, string> = {
  fuente_oficial: 'Fuentes oficiales',
  medio_de_referencia: 'Medios de referencia',
  verificacion_previa: 'Verificaciones previas',
};

/**
 * Clase y rótulo de cada postura, como en la columna izquierda del *mockup*.
 *
 * La postura la determina el servicio al recuperar cada fuente y es lo que el
 * combinador agrega para producir el puntaje de contraste. Acá solo se la
 * pinta: el color de `.p-contra` y el de `.p-corro` salen del *mockup* y no se
 * eligen según el veredicto, porque lo que la columna dice es qué sostiene esa
 * fuente y no qué concluyó el sistema.
 */
const POSTURA: Record<Fuente['postura'], { clase: string; rotulo: string }> = {
  contradice: { clase: 'p-contra', rotulo: 'Contradice' },
  corrobora: { clase: 'p-corro', rotulo: 'Corrobora' },
  neutral: { clase: 'p-neutro', rotulo: 'Neutral' },
};

/** Nombre legible de una fuente a partir de su URL. */
export function nombreDeFuente(url: string): string {
  try {
    return new URL(url).hostname.replace(/^www\./, '');
  } catch {
    return url;
  }
}



/**
 * Una fila de fuente: su postura, de dónde sale y el enlace al documento.
 *
 * El enlace abre el documento original en una pestaña nueva. `noopener` y
 * `noreferrer` no son ceremonia: la extensión inyecta esto dentro de X, y sin
 * `noopener` la página que se abre queda con una referencia a la ventana de
 * origen.
 */
function filaDeFuente(fuente: Fuente): HTMLElement {
  const fila = document.createElement('div');
  fila.className = 'fuente';

  const postura = POSTURA[fuente.postura];
  const etiqueta = document.createElement('div');
  etiqueta.className = `postura ${postura.clase}`;
  etiqueta.textContent = postura.rotulo;

  const cuerpo = document.createElement('div');
  cuerpo.className = 'f-datos';

  const organismo = document.createElement('div');
  organismo.className = 'f-org';
  organismo.textContent = nombreDeFuente(fuente.url);

  const titulo = document.createElement('p');
  titulo.className = 'f-tit';
  const enlace = document.createElement('a');
  enlace.href = fuente.url;
  enlace.target = '_blank';
  enlace.rel = 'noopener noreferrer';
  // Sin título utilizable, el enlace muestra la dirección: el usuario tiene que
  // poder llegar al documento aunque el título haya venido vacío. El ícono de
  // salida dice, antes de tocar, que el enlace abre el documento original fuera
  // de X: es la promesa central del panel.
  escribirEnlaceSaliente(enlace, fuente.titulo.trim() || fuente.url);
  titulo.append(enlace);

  cuerpo.append(organismo, titulo);
  fila.append(etiqueta, cuerpo);
  return fila;
}

/** Un grupo de la jerarquía, con su rótulo y sus filas. */
function grupo(tipo: TipoFuente, fuentes: Fuente[]): HTMLElement {
  const nodo = document.createElement('div');
  nodo.className = 'e-grupo';

  const encabezado = document.createElement('h3');
  encabezado.textContent = TITULO_DE_GRUPO[tipo];
  nodo.append(encabezado, ...fuentes.map(filaDeFuente));

  return nodo;
}


/**
 * Construye el panel de evidencia a partir de un análisis.
 *
 * Devuelve `null` cuando no hay ninguna fuente que mostrar. Un panel de
 * evidencia vacío no informa nada y sugiere que hubo una búsqueda que falló: el
 * detalle ya dice, en su tapa, que el análisis quedó sin contraste externo.
 */
export function renderizarEvidencia(analisis: RespuestaAnalisis): HTMLElement | null {
  if (analisis.fuentes.length === 0) {
    return null;
  }

  const panel = document.createElement('div');
  panel.className = 'evid';

  // El panel es la lista de fuentes y nada mas. El encabezado repetia el
  // resumen que la ficha ya da, y la afirmacion extraida ya esta dibujada unos
  // centimetros mas arriba, en el detalle: verla dos veces en la misma pantalla
  // no agrega nada y hace mas larga la unica pantalla que hay que poder leer de
  // un vistazo.
  for (const tipo of ORDEN_DE_LA_JERARQUIA) {
    const delGrupo = analisis.fuentes.filter((fuente) => fuente.tipo === tipo);
    if (delGrupo.length > 0) {
      panel.append(grupo(tipo, delGrupo));
    }
  }

  // El escalonado se numera **sobre el panel entero** y no dentro de cada
  // grupo: si cada grupo reiniciara la cuenta, la primera fuente oficial y el
  // primer medio de referencia aterrizarían a la vez y el orden de la jerarquía
  // —que es la decisión de fondo de esta pantalla— dejaría de leerse en el
  // movimiento. El tope de 6 acota la espera de una lista larga.
  const filas = panel.querySelectorAll<HTMLElement>('.fuente');
  filas.forEach((fila, indice) => {
    fila.style.setProperty('--i', String(Math.min(indice, 6)));
  });

  // La nota que explicaba la jerarquia se saca: los encabezados de cada grupo
  // —FUENTES OFICIALES, MEDIOS DE REFERENCIA— ya dicen lo mismo mostrandolo.
  return panel;
}
