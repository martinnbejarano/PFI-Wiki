/**
 * Indicador que se inyecta sobre el tuit (RF-08, CU-01).
 *
 * El marcado y el CSS se portan de la pantalla `?pantalla=badge` de
 * `wiki/assets/mockups/mockups.html`. Todo vive dentro de un *shadow DOM*:
 * la página de X no ve estas reglas y ninguna regla de X entra acá, que es lo
 * que garantiza que la extensión no degrade la red (RNF-13 en la práctica).
 *
 * El estado se comunica por tres canales simultáneos —color, forma del ícono y
 * texto— para no depender de la percepción del color (RNF-15).
 */

import type { RespuestaAnalisis, Veredicto } from '../compartido/contrato';

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

/** Nombre legible de una fuente a partir de su URL. */
function nombreDeFuente(url: string): string {
  try {
    return new URL(url).hostname.replace(/^www\./, '');
  } catch {
    return url;
  }
}

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
 * @param alHacerClic Se invoca cuando el ciudadano pide el análisis. El
 * análisis es siempre a demanda: nunca se dispara por entrar el tuit en el
 * área visible.
 */
export function crearIndicador(alHacerClic: () => void): Indicador {
  const anfitrion = document.createElement('div');
  anfitrion.setAttribute('data-pfi-indicador', '');

  const raiz = anfitrion.attachShadow({ mode: 'open' });

  const hoja = document.createElement('style');
  hoja.textContent = ESTILOS;

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

  boton.append(figura, texto);
  raiz.append(hoja, boton);

  // X hace clicable el artículo entero: sin frenar la propagación, pedir el
  // análisis navegaría al detalle del tuit.
  const frenar = (evento: Event) => {
    evento.preventDefault();
    evento.stopPropagation();
  };
  anfitrion.addEventListener('click', frenar, true);
  anfitrion.addEventListener('mousedown', frenar, true);
  anfitrion.addEventListener('keydown', (evento) => evento.stopPropagation(), true);
  boton.addEventListener('click', () => alHacerClic());

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
  }

  function mostrarError(mensaje: string): void {
    pintar('b-sosp', '!', 'No se pudo analizar', `${mensaje}. Tocá para reintentar`);
  }

  mostrarInicial();

  return { anfitrion, mostrarInicial, mostrarAnalizando, mostrarVeredicto, mostrarError };
}
