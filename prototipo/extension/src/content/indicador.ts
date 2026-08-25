/**
 * Indicador que se inyecta sobre el tuit (RF-08, CU-01) y la puerta al detalle.
 *
 * El marcado y el CSS se portan de la pantalla `?pantalla=badge` de
 * `wiki/assets/mockups/mockups.html`. Todo vive dentro de un *shadow DOM*:
 * la página de X no ve estas reglas y ninguna regla de X entra acá, que es lo
 * que garantiza que la extensión no degrade la red (RNF-13 en la práctica).
 *
 * El estado se comunica por tres canales simultáneos —color, forma del ícono y
 * texto— para no depender de la percepción del color (RNF-15).
 *
 * El botón hace dos cosas distintas según el estado, que es lo que el *mockup*
 * dibuja con la leyenda «Ver análisis» a la derecha del indicador: mientras no
 * hay análisis, pide uno; una vez que lo hay, despliega y repliega el detalle
 * (`detalle.ts`) dentro de este mismo *shadow DOM*, sobre la *timeline* y sin
 * abrir ninguna otra ventana.
 */

import type { RespuestaAnalisis, Veredicto } from '../compartido/contrato';
import { ESTILOS_DETALLE, renderizarDetalle } from './detalle';
import { ESTILOS_EVIDENCIA, nombreDeFuente } from './evidencia';

/** Atributo con el que se marcan los artículos ya procesados. */
export const ATRIBUTO_PROCESADO = 'data-pfi-procesado';

const ESTILOS = `
:host {
  all: initial;
  display: block;
  margin: 8px 0 2px;
  font: 13.5px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
        Helvetica, Arial, sans-serif;
}
* { box-sizing: border-box; }

.badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  padding: 9px 12px;
  border-radius: 9px;
  font: inherit;
  font-size: 13.5px;
  cursor: pointer;
  border: 1px solid;
  text-align: left;
}
.badge .fig {
  flex: 0 0 18px;
  height: 18px;
  display: grid;
  place-items: center;
  font-size: 12px;
  font-weight: 700;
  color: #fff;
  border-radius: 3px;
}
.badge .txt { flex: 1; min-width: 0; }
.badge .txt b { display: block; font-size: 13.5px; }
.badge .txt em { font-style: normal; font-size: 12px; opacity: .85; }
.badge .mas { font-size: 12px; text-decoration: underline; white-space: nowrap; }
.badge .mas:empty { display: none; }

.b-falso { background: #fdecea; border-color: #f0b4ad; color: #c0392b; }
.b-falso .fig {
  background: #c0392b;
  clip-path: polygon(50% 0, 100% 100%, 0 100%);
  border-radius: 0;
}
.b-sosp { background: #fdf4e3; border-color: #eccf95; color: #a56a00; }
.b-sosp .fig { background: #a56a00; border-radius: 50%; }
.b-ok { background: #e9f6ef; border-color: #a8d7bf; color: #1a7a4c; }
.b-ok .fig { background: #1a7a4c; }
.b-wait { background: #f1f3f5; border-color: #d3d9df; color: #5b6570; }
.b-wait .fig {
  background: transparent;
  border: 2px solid #d3d9df;
  border-top-color: #5b6570;
  border-radius: 50%;
  animation: giro 1s linear infinite;
}
.b-parcial { background: #f1f3f5; border-color: #d3d9df; color: #5b6570; }
.b-parcial .fig { background: #5b6570; border-radius: 50%; }
.b-inicial { background: #eaf1fa; border-color: #c4d8f0; color: #1b4f8f; }
.b-inicial .fig { background: #1b4f8f; border-radius: 50%; }

@keyframes giro { to { transform: rotate(360deg); } }
@media (prefers-reduced-motion: reduce) {
  .b-wait .fig { animation: none; }
}

.nota-parcial {
  display: block;
  margin-top: 4px;
  font-size: 11.5px;
  color: #7a5b00;
  background: #fffaf0;
  border: 1px solid #e8d089;
  border-radius: 6px;
  padding: 5px 9px;
}
`;

/** Clase de estilo y forma del ícono por veredicto. */
const APARIENCIA: Record<Veredicto, { clase: string; figura: string; titulo: string }> = {
  contradicho_por_fuentes_oficiales: {
    clase: 'b-falso',
    figura: '!',
    titulo: 'Contradicho por fuentes oficiales',
  },
  informacion_sospechosa: {
    clase: 'b-sosp',
    figura: '',
    titulo: 'Información sospechosa',
  },
  parece_verificado: {
    clase: 'b-ok',
    figura: '✓',
    titulo: 'Parece verificado',
  },
  sin_contraste_externo: {
    clase: 'b-parcial',
    figura: '◐',
    titulo: 'Sin contraste externo',
  },
};

/** Enumera hasta cuatro nombres separados por comas y una conjunción final. */
function enumerar(nombres: string[]): string {
  const visibles = nombres.slice(0, 4);
  if (visibles.length <= 1) {
    return visibles.join('');
  }
  return `${visibles.slice(0, -1).join(', ')} y ${visibles[visibles.length - 1]}`;
}

/**
 * Segunda línea del indicador.
 *
 * Se enuncia sobre la afirmación y sobre quién la sostiene, nunca sobre la
 * persona que publicó el tuit (RNF-07).
 */
function detalle(analisis: RespuestaAnalisis): string {
  if (analisis.veredicto === 'sin_contraste_externo') {
    return 'No se encontró ninguna fuente admisible con la cual contrastar';
  }
  const contradicen = analisis.fuentes.filter((f) => f.postura === 'contradice');
  if (contradicen.length > 0) {
    return `Lo contradicen ${enumerar(contradicen.map((f) => nombreDeFuente(f.url)))}`;
  }
  const corroboran = analisis.fuentes.filter((f) => f.postura === 'corrobora');
  if (corroboran.length > 0) {
    return `Coincide con ${enumerar(corroboran.map((f) => nombreDeFuente(f.url)))}`;
  }
  return `${analisis.fuentes.length} fuentes consultadas, ninguna se pronuncia`;
}

/** Superficie del indicador que el *content script* maneja. */
export interface Indicador {
  /** Elemento anfitrión que se inserta en el DOM de X. */
  anfitrion: HTMLElement;
  mostrarInicial(): void;
  mostrarAnalizando(): void;
  mostrarVeredicto(analisis: RespuestaAnalisis): void;
  mostrarError(mensaje: string): void;
}

/**
 * Crea el indicador y lo devuelve sin insertarlo en el documento.
 *
 * @param handle Cuenta autora del tuit, que el detalle muestra como atribución
 * de la publicación analizada.
 * @param alHacerClic Se invoca cuando el ciudadano pide el análisis. El
 * análisis es siempre a demanda: nunca se dispara por entrar el tuit en el
 * área visible. No se invoca cuando el botón solo despliega el detalle de un
 * análisis que ya está resuelto.
 */
export function crearIndicador(handle: string, alHacerClic: () => void): Indicador {
  const anfitrion = document.createElement('div');
  anfitrion.setAttribute('data-pfi-indicador', '');

  const raiz = anfitrion.attachShadow({ mode: 'open' });

  const hoja = document.createElement('style');
  // Las tres hojas —indicador, detalle y evidencia— comparten este *shadow
  // DOM*: el detalle se despliega bajo el indicador y el panel de evidencia se
  // despliega dentro del detalle, así que nada de esto sale a la página de X ni
  // recibe una sola regla suya.
  hoja.textContent = `${ESTILOS}\n${ESTILOS_DETALLE}\n${ESTILOS_EVIDENCIA}`;

  const boton = document.createElement('button');
  boton.type = 'button';
  boton.className = 'badge b-inicial';

  const figura = document.createElement('span');
  figura.className = 'fig';
  figura.setAttribute('aria-hidden', 'true');

  const texto = document.createElement('span');
  texto.className = 'txt';
  const titulo = document.createElement('b');
  const subtitulo = document.createElement('em');
  texto.append(titulo, subtitulo);

  // La leyenda que el *mockup* pone a la derecha del indicador. Queda vacía
  // —y oculta por CSS— mientras no haya un detalle que abrir.
  const mas = document.createElement('span');
  mas.className = 'mas';

  boton.append(figura, texto, mas);
  raiz.append(hoja, boton);

  /** Análisis resuelto, o nada si todavía no hay uno que mostrar. */
  let analisisActual: RespuestaAnalisis | null = null;
  let panel: HTMLElement | null = null;

  /** Repliega el detalle y deja la leyenda acorde al estado actual. */
  function cerrarDetalle(): void {
    panel?.remove();
    panel = null;
    boton.setAttribute('aria-expanded', 'false');
    mas.textContent = analisisActual ? 'Ver análisis' : '';
  }

  /** Despliega el detalle, o lo repliega si ya estaba abierto. */
  function alternarDetalle(): void {
    if (!analisisActual) {
      return;
    }
    if (panel) {
      cerrarDetalle();
      return;
    }
    panel = renderizarDetalle(analisisActual, handle);
    raiz.append(panel);
    mas.textContent = 'Ocultar análisis';
    boton.setAttribute('aria-expanded', 'true');
  }

  // X hace clicable el artículo entero: sin frenar la propagación, tocar el
  // indicador navegaría al detalle del tuit.
  //
  // El freno va en la fase de burbujeo y **no** en la de captura. En captura el
  // recorrido baja desde el documento hasta el destino, así que un
  // `stopPropagation` sobre el anfitrión corta el evento antes de que llegue al
  // botón que vive dentro del *shadow DOM*: el indicador queda inerte y ningún
  // clic dispara el análisis. En burbujeo el botón ya atendió el evento y lo que
  // se frena es lo único que hay que frenar, que es la subida hacia los
  // manejadores de X. `preventDefault` sigue sirviendo en esta fase porque la
  // acción por defecto —seguir el enlace del artículo— se ejecuta recién al
  // terminar el envío del evento.
  const frenar = (evento: Event) => {
    evento.preventDefault();
    evento.stopPropagation();
  };
  anfitrion.addEventListener('click', frenar);
  anfitrion.addEventListener('mousedown', frenar);
  anfitrion.addEventListener('keydown', (evento) => evento.stopPropagation());
  boton.addEventListener('click', () => {
    // Con un análisis resuelto el botón abre y cierra el detalle; sin él, lo
    // pide. Un análisis que falló vuelve al segundo caso, que es lo que hace
    // que «Tocá para reintentar» signifique lo que dice.
    if (analisisActual) {
      alternarDetalle();
      return;
    }
    alHacerClic();
  });

  function pintar(
    clase: string,
    figuraTexto: string,
    tituloTexto: string,
    subtituloTexto: string,
  ): void {
    boton.className = `badge ${clase}`;
    figura.textContent = figuraTexto;
    titulo.textContent = tituloTexto;
    subtitulo.textContent = subtituloTexto;
    boton.setAttribute('aria-label', `${tituloTexto}. ${subtituloTexto}`);
    raiz.querySelector('.nota-parcial')?.remove();
    // Cualquier cambio de estado invalida el detalle que hubiera abierto: si
    // el tuit se vuelve a analizar, lo que se muestre después tiene que ser el
    // análisis nuevo y no el anterior.
    analisisActual = null;
    cerrarDetalle();
  }

  function mostrarInicial(): void {
    pintar('b-inicial', '?', 'Verificar esta publicación', 'Análisis a demanda');
  }

  function mostrarAnalizando(): void {
    pintar('b-wait', '', 'Analizando…', 'Contrastando con fuentes');
  }

  function mostrarVeredicto(analisis: RespuestaAnalisis): void {
    const apariencia = APARIENCIA[analisis.veredicto];
    const porcentaje = Math.round(analisis.puntaje_final * 100);
    // El estado de ausencia de evidencia no lleva porcentaje: no habría sobre
    // qué calcularlo (RF-08 y RNF-06).
    const encabezado =
      analisis.veredicto === 'sin_contraste_externo'
        ? apariencia.titulo
        : `${apariencia.titulo} · ${porcentaje}%`;

    pintar(apariencia.clase, apariencia.figura, encabezado, detalle(analisis));

    if (analisis.analisis_parcial.es_parcial) {
      const nota = document.createElement('p');
      nota.className = 'nota-parcial';
      const ausentes = analisis.analisis_parcial.modulos_ausentes.join(', ');
      nota.textContent = ausentes
        ? `Análisis parcial: no se ejecutó ${ausentes}. El resultado no es concluyente.`
        : 'Análisis parcial: el resultado no es concluyente.';
      raiz.append(nota);
    }

    // Recién ahora el botón deja de pedir análisis y pasa a abrir el detalle.
    analisisActual = analisis;
    cerrarDetalle();
  }

  function mostrarError(mensaje: string): void {
    pintar('b-sosp', '!', 'No se pudo analizar', `${mensaje}. Tocá para reintentar`);
  }

  mostrarInicial();

  return { anfitrion, mostrarInicial, mostrarAnalizando, mostrarVeredicto, mostrarError };
}
