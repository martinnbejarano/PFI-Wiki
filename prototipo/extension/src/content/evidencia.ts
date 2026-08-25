/**
 * Panel de evidencia (RF-09, CU-03): la tercera pantalla del *mockup*.
 *
 * El marcado y el CSS se portan de la pantalla `?pantalla=evidencia` de
 * `wiki/assets/mockups/mockups.html`, igual que el indicador se portó de
 * `?pantalla=badge` y el detalle de `?pantalla=popup`. Los nombres de clase son
 * los del *mockup* —`.evid`, `.e-tapa`, `.e-claim`, `.e-grupo`, `.fuente`,
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
 * 3. **Todas las fuentes aparecen como neutrales** mientras la determinación de
 *    la postura sea el ticket #24. La figura muestra las tres posturas y la hoja
 *    de estilos las trae a las tres: la pantalla está lista, lo que falta es el
 *    dato.
 */

import type { Fuente, RespuestaAnalisis, TipoFuente } from '../compartido/contrato';

/**
 * Estilos del panel de evidencia, portados del *mockup*.
 *
 * Se declaran sobre `.evid` y no sobre `:host` porque el indicador ya reclama
 * `:host` con `all: initial` y las tres hojas comparten el mismo *shadow DOM*.
 * Los valores son los mismos del `:root` del *mockup*.
 */
export const ESTILOS_EVIDENCIA = `
.evid {
  --falso: #c0392b;
  --ok: #1a7a4c;
  --tinta: #15202b; --gris: #5b6570; --linea: #e2e6ea; --fondo: #f7f9fa;
  --marca: #1b4f8f;

  width: 100%;
  max-width: 620px;
  margin: 0;
  background: #fff;
  color: var(--tinta);
  border-top: 1px solid var(--linea);
  overflow: hidden;
  text-align: left;
}

.evid .e-tapa { padding: 16px 20px; border-bottom: 1px solid var(--linea); }
.evid .e-tapa h2 { margin: 0 0 4px; font-size: 16px; }
.evid .e-tapa p { margin: 0; font-size: 13px; color: var(--gris); }

/* El bloque de la afirmación ya viene definido por la hoja del detalle, que lo
   tomó de esta misma pantalla. Acá solo se corrige el margen, que en la figura
   de evidencia es el de un contenedor de 20 px y no el de uno de 18 px. */
.evid .e-claim { margin: 12px 20px 0; }

.evid .e-grupo { padding: 16px 20px; border-top: 1px solid var(--linea); margin-top: 16px; }
.evid .e-grupo:first-of-type { margin-top: 0; }
.evid .e-grupo h3 {
  margin: 0 0 12px;
  font-size: 11px;
  letter-spacing: .06em;
  text-transform: uppercase;
  color: var(--gris);
}

.evid .fuente { display: flex; gap: 11px; padding: 10px 0; border-bottom: 1px dashed var(--linea); }
.evid .fuente:last-child { border-bottom: 0; padding-bottom: 0; }
.evid .postura {
  flex: 0 0 92px;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: .03em;
  padding-top: 2px;
}
.evid .p-contra { color: var(--falso); }
.evid .p-corro { color: var(--ok); }
.evid .p-neutro { color: var(--gris); }
.evid .f-cuerpo { flex: 1; min-width: 0; }
.evid .f-org { font-size: 12px; color: var(--gris); margin-bottom: 2px; }
.evid .f-tit { font-size: 13.5px; margin: 0 0 3px; }
.evid .f-tit a { color: var(--marca); text-decoration: none; }
.evid .f-tit a:hover { text-decoration: underline; }
.evid .f-cita { font-size: 12.5px; color: var(--gris); margin: 0; }

.evid .e-nota {
  margin: 0;
  padding: 12px 20px;
  border-top: 1px solid var(--linea);
  background: var(--fondo);
  font-size: 11.5px;
  line-height: 1.45;
  color: var(--gris);
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

/** Clase y rótulo de cada postura, como en la columna izquierda del *mockup*. */
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

/** «1 fuente» / «7 fuentes», sin el `1 fuentes` que delata a una plantilla. */
function plural(cantidad: number, singular: string, muchos: string): string {
  return `${cantidad} ${cantidad === 1 ? singular : muchos}`;
}

/**
 * Resumen de la tapa: cuántas fuentes se consultaron y en qué se reparten.
 *
 * Solo se enumeran las posturas con al menos una fuente. Un «0 corroboran» en
 * la tapa es ruido, y peor: sugiere que se buscó una corroboración y no se la
 * encontró, que no es lo que ese cero dice.
 */
function resumen(fuentes: Fuente[]): string {
  const partes = [plural(fuentes.length, 'fuente consultada', 'fuentes consultadas')];

  const contradicen = fuentes.filter((f) => f.postura === 'contradice').length;
  const corroboran = fuentes.filter((f) => f.postura === 'corrobora').length;
  const neutrales = fuentes.filter((f) => f.postura === 'neutral').length;

  if (contradicen > 0) {
    partes.push(plural(contradicen, 'contradice', 'contradicen'));
  }
  if (corroboran > 0) {
    partes.push(plural(corroboran, 'corrobora', 'corroboran'));
  }
  if (neutrales > 0) {
    partes.push(plural(neutrales, 'neutral', 'neutrales'));
  }

  return partes.join(' · ');
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
  cuerpo.className = 'f-cuerpo';

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
  // poder llegar al documento aunque el título haya venido vacío.
  enlace.textContent = fuente.titulo.trim() || fuente.url;
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

/** El bloque con la afirmación verificable extraída y su tipo (RF-04). */
function bloqueAfirmacion(texto: string, tipo: string): HTMLElement {
  const nodo = document.createElement('div');
  nodo.className = 'e-claim';

  const rotulo = document.createElement('span');
  rotulo.textContent = `Afirmación verificable extraída · tipo: ${tipo}`;

  nodo.append(rotulo, document.createTextNode(`«${texto}»`));
  return nodo;
}

/**
 * Construye el panel de evidencia a partir de un análisis.
 *
 * Devuelve `null` cuando no hay ninguna fuente que mostrar. Un panel de
 * evidencia vacío no informa nada y sugiere que hubo una búsqueda que falló: el
 * detalle ya dice, en su tapa, que el análisis quedó sin contraste externo.
 *
 * @param tipoLegible Nombre en castellano del tipo de la afirmación. Lo pasa
 * quien llama para no sostener dos veces la misma tabla de nombres.
 */
export function renderizarEvidencia(
  analisis: RespuestaAnalisis,
  tipoLegible: string,
): HTMLElement | null {
  if (analisis.fuentes.length === 0) {
    return null;
  }

  const panel = document.createElement('div');
  panel.className = 'evid';

  const tapa = document.createElement('div');
  tapa.className = 'e-tapa';
  const titulo = document.createElement('h2');
  titulo.textContent = 'Evidencia del análisis';
  const subtitulo = document.createElement('p');
  subtitulo.textContent = resumen(analisis.fuentes);
  tapa.append(titulo, subtitulo);

  panel.append(tapa);

  if (analisis.afirmacion.trim() !== '') {
    panel.append(bloqueAfirmacion(analisis.afirmacion, tipoLegible));
  }

  for (const tipo of ORDEN_DE_LA_JERARQUIA) {
    const delGrupo = analisis.fuentes.filter((fuente) => fuente.tipo === tipo);
    if (delGrupo.length > 0) {
      panel.append(grupo(tipo, delGrupo));
    }
  }

  const nota = document.createElement('p');
  nota.className = 'e-nota';
  nota.textContent =
    'Las fuentes se ordenan según la jerarquía de evidencia del sistema: ' +
    'fuentes oficiales, medios de referencia y verificaciones previas. La ' +
    'búsqueda queda restringida a esos dominios, así que no se cita cualquier ' +
    'resultado de internet. Cada enlace abre el documento original.';
  panel.append(nota);

  return panel;
}
