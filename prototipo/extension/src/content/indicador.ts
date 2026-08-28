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
import {
  CONTRATO_DE_DIRECCION,
  ESTILOS_MARCA,
  FICHAS,
  ICONOS,
  marcaDeAtribucion,
} from './tema';
import { ESTILOS_DETALLE, renderizarDetalle } from './detalle';
import { ESTILOS_EVIDENCIA, nombreDeFuente } from './evidencia';

/** Atributo con el que se marcan los artículos ya procesados. */
export const ATRIBUTO_PROCESADO = 'data-pfi-procesado';

const ESTILOS = `
:host {
  all: initial;
  display: block;
  margin: 12px 0 4px;
  font-family: var(--letra);
  ${FICHAS}
}
* { box-sizing: border-box; }

/*
 * La seleccion, el foco y el cursor son superficies del navegador que igual
 * pertenecen al diseno. La regla de X no penetra el *shadow DOM*: sin esto,
 * seleccionar el texto de la afirmacion devolvia el azul por defecto de Chrome
 * al lado de un tuit pintado con el de X, que es lo que delata que la pieza no
 * es de la casa.
 */
::selection { background: rgba(29, 155, 240, 0.4); color: var(--tinta); }

/* -- El indicador ------------------------------------------------------- */
/*
 * Toma la forma de la tarjeta de enlace de X —ancho completo, 16 de radio,
 * borde de 1— porque es la pieza que X ya usa para adjuntar contenido bajo el
 * texto de un tuit. El fondo queda sin pintar: lo que se ve detrás es el de X.
 */
.badge {
  display: grid;
  grid-template-columns: 20px minmax(0, 1fr) auto;
  align-items: start;
  gap: 3px 12px;
  width: 100%;
  padding: 11px 14px 10px;
  border: 1px solid var(--borde);
  border-radius: var(--radio);
  background: transparent;
  color: var(--tinta);
  font: 400 15px/20px var(--letra);
  letter-spacing: 0.01em;
  text-align: left;
  cursor: pointer;
  transition: background-color 0.2s var(--curva), border-color 0.2s var(--curva);
}
.badge:hover { background: var(--velo); }
.badge:active { background: var(--velo-fuerte); }
.badge:focus-visible { outline: 2px solid var(--azul); outline-offset: 2px; }

.badge .fig {
  grid-row: 1;
  display: grid;
  place-items: center;
  width: 20px;
  height: 20px;
  color: var(--tinta-apagada);
}
.badge .fig svg { display: block; }

.badge .txt { grid-column: 2; grid-row: 1; min-width: 0; }
.badge .txt b { display: block; font-weight: 700; letter-spacing: -0.01em; }
/*
 * «84% de desinformacion · Lo contradicen …» es la linea que permite decidir sin
 * abrir nada, asi que no va en el gris que X reserva a las marcas de tiempo, que
 * ademas no alcanza el contraste minimo sobre el carbon de *Dim*. Se acota a dos
 * renglones, como X acota la descripcion de sus tarjetas de enlace.
 */
.badge .txt em {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
  margin-top: 1px;
  color: var(--tinta-media);
  font: 400 13px/17px var(--letra);
  font-style: normal;
}

/*
 * La leyenda de despliegue y su galon. Se esconde sola mientras no haya un
 * analisis que abrir, en lugar de prometer una accion que todavia no existe.
 */
.badge .mas {
  grid-column: 3;
  grid-row: 1;
  display: inline-flex;
  align-items: center;
  gap: 2px;
  align-self: center;
  justify-content: flex-end;
  min-width: 112px;
  color: var(--tinta-media);
  font-size: 13px;
  line-height: 16px;
  white-space: nowrap;
}
.badge .mas:empty { display: none; min-width: 0; }
.badge .mas svg { display: block; transition: transform 0.2s var(--curva); }
.badge[aria-expanded='true'] .mas svg { transform: rotate(180deg); }
/*
 * Con el detalle abierto la ficha suelta sus esquinas y su filete de abajo: lo
 * que sigue no es otra tarjeta, es la misma que crece.
 */
.badge[aria-expanded='true'] {
  border-radius: var(--radio) var(--radio) 0 0;
  border-bottom-color: transparent;
}
/*
 * Fusionadas en una sola tarjeta, las dos mitades tienen que compartir contorno:
 * si la ficha lo pinta con el color del estado y el detalle con el borde neutro,
 * el filete cambia de color a media altura y delata la costura.
 */
.b-falso ~ .popup { border-color: var(--rojo-borde); }
.b-sosp ~ .popup { border-color: var(--ambar-borde); }
.b-ok ~ .popup { border-color: var(--verde-borde); }

/*
 * La atribucion ocupa el renglon que X reserva, en sus tarjetas de enlace, para
 * decir de que dominio viene lo adjuntado. Es el hueco nativo de la procedencia,
 * y por eso es el lugar correcto para decir que el juicio no es de X.
 */
.badge .atribucion { grid-column: 2 / -1; grid-row: 2; margin-top: 3px; }

/* -- Estado ------------------------------------------------------------- */
/*
 * El color esta reservado para el veredicto que se apoya en evidencia. La
 * ausencia —sin contraste externo, analisis parcial— se dibuja en gris, y el
 * trabajo en curso toma el azul de X, que es su color de sistema y no un juicio
 * sobre el contenido.
 */
.b-inicial .fig { color: var(--tinta-apagada); }

.b-wait { border-color: var(--azul-borde); background: var(--azul-velo); }
.b-wait .fig { color: var(--azul); }
.b-wait .fig::after {
  content: '';
  width: 16px;
  height: 16px;
  border: 2px solid currentColor;
  border-top-color: transparent;
  border-radius: 50%;
  animation: girar 0.7s linear infinite;
}

.b-falso { border-color: var(--rojo-borde); background: var(--rojo-velo); }
.b-falso .fig { color: var(--rojo); }

.b-sosp { border-color: var(--ambar-borde); background: var(--ambar-velo); }
.b-sosp .fig { color: var(--ambar); }

.b-ok { border-color: var(--verde-borde); background: var(--verde-velo); }
.b-ok .fig { color: var(--verde); }

.b-parcial .fig { color: var(--tinta-apagada); }

/*
 * La falla no es un veredicto y no toma ningun color de veredicto: el sistema
 * no pudo pronunciarse, que es otra cosa que pronunciarse en contra.
 */
.b-falla { border-color: var(--borde-vivo); }
.b-falla .fig { color: var(--tinta-apagada); }

/*
 * El unico momento de movimiento de la interfaz: cuando el veredicto llega, el
 * indicador se asienta en lugar de aparecer de golpe. Parte de un estado ya
 * visible, asi que nada queda escondido si la animacion no corre.
 */
@keyframes asentar {
  from { transform: translateY(-2px); opacity: 0.55; }
  to { transform: none; opacity: 1; }
}
@keyframes girar { to { transform: rotate(360deg); } }

.b-falso, .b-sosp, .b-ok, .b-parcial, .b-falla { animation: asentar 0.32s var(--curva) both; }

/* -- La nota del analisis parcial --------------------------------------- */
.nota-parcial {
  margin: 8px 0 0;
  padding: 10px 14px;
  border: 1px solid var(--borde);
  border-radius: var(--radio-chico);
  color: var(--tinta-media);
  font: 400 13px/18px var(--letra);
}

@media (prefers-reduced-motion: reduce) {
  .badge, .badge .mas svg { transition: none; }
  .b-falso, .b-sosp, .b-ok, .b-parcial, .b-falla { animation: none; }
  .b-wait .fig::after { animation-duration: 2.4s; }
}
${ESTILOS_MARCA}
`;

/** Clase de estilo y forma del ícono por veredicto. */
const APARIENCIA: Record<Veredicto, { clase: string; figura: string; titulo: string }> = {
  contradicho_por_fuentes_oficiales: {
    clase: 'b-falso',
    figura: ICONOS.contradicho,
    titulo: 'Contradicho por fuentes oficiales',
  },
  informacion_sospechosa: {
    clase: 'b-sosp',
    figura: ICONOS.sospechoso,
    titulo: 'Información sospechosa',
  },
  parece_verificado: {
    clase: 'b-ok',
    figura: ICONOS.verificado,
    titulo: 'Parece verificado',
  },
  sin_contraste_externo: {
    clase: 'b-parcial',
    figura: ICONOS.sinContraste,
    titulo: 'Sin contraste externo',
  },
};

/** Enumera hasta cuatro nombres separados por comas y una conjunción final. */
function enumerar(nombres: string[]): string {
  if (nombres.length <= 1) {
    return nombres.join('');
  }
  // El recorte se hace **contando**, no dejando que el CSS corte con elipsis.
  // Recortado por elipsis, «… lanacion.com.ar y chequeado.com» terminaba en «y…»
  // —una conjunción colgando— y se perdía en silencio una de las fuentes que
  // sostienen el veredicto, que es justamente lo que el producto promete
  // mostrar. Contando, lo que se pierde queda dicho.
  const TOPE = 2;
  if (nombres.length <= TOPE) {
    return `${nombres.slice(0, -1).join(', ')} y ${nombres[nombres.length - 1]}`;
  }
  const restantes = nombres.length - TOPE;
  return `${nombres.slice(0, TOPE).join(', ')} y ${restantes} más`;
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

  // La atribucion viaja dentro del propio indicador y no en una capa aparte:
  // tiene que seguir estando cuando el ciudadano solo mira la *timeline*.
  const atribucion = marcaDeAtribucion();

  boton.append(figura, texto, mas, atribucion);
  raiz.append(document.createComment(CONTRATO_DE_DIRECCION), hoja, boton);

  /** Escribe la leyenda de despliegue, con su galón, o la deja vacía. */
  function leyenda(texto: string): void {
    mas.textContent = '';
    if (!texto) {
      return;
    }
    mas.append(texto);
    const galon = document.createElement('span');
    galon.innerHTML = ICONOS.galon;
    mas.append(galon);
  }

  /** Análisis resuelto, o nada si todavía no hay uno que mostrar. */
  let analisisActual: RespuestaAnalisis | null = null;
  let panel: HTMLElement | null = null;

  /** Repliega el detalle y deja la leyenda acorde al estado actual. */
  function cerrarDetalle(): void {
    panel?.remove();
    panel = null;
    boton.setAttribute('aria-expanded', 'false');
    leyenda(analisisActual ? 'Ver análisis' : '');
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
    leyenda('Ocultar análisis');
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
    figura.innerHTML = figuraTexto;
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
    pintar('b-inicial', ICONOS.marca, 'Verificar esta publicación', 'Análisis a demanda');
  }

  function mostrarAnalizando(): void {
    pintar('b-wait', '', 'Analizando…', 'Contrastando con fuentes');
  }

  function mostrarVeredicto(analisis: RespuestaAnalisis): void {
    const esParcial = analisis.analisis_parcial.es_parcial;
    const apariencia = APARIENCIA[analisis.veredicto];
    const porcentaje = Math.round(analisis.puntaje_final * 100);

    if (esParcial) {
      // Un análisis parcial no lleva porcentaje ni el color de un nivel, por lo
      // mismo que en el detalle: una cifra calculada con un módulo caído se lee
      // igual de confiable que las demás y no lo es (RNF-11). El indicador dice
      // qué es y la nota de abajo dice qué faltó.
      pintar('b-parcial', ICONOS.parcial, 'Análisis parcial', 'Tocá para ver qué se pudo verificar');
    } else {
      // El estado de ausencia de evidencia tampoco lleva porcentaje: no habría
      // sobre qué calcularlo (RF-08 y RNF-06).
      // El porcentaje va en el renglón de abajo y con su sustantivo, no pegado
      // al veredicto. «Parece verificado · 16%» se lee como «16% verificado»,
      // que es lo contrario de lo que el número mide: es la probabilidad
      // estimada de desinformación, como lo rotula el detalle. Un indicador que
      // hay que aprender a leer incumple RNF-15.
      const sinContraste = analisis.veredicto === 'sin_contraste_externo';
      const evidencia = detalle(analisis);
      const subtitulo = sinContraste
        ? evidencia
        : `${porcentaje}% de desinformación · ${evidencia}`;
      pintar(apariencia.clase, apariencia.figura, apariencia.titulo, subtitulo);
    }

    if (esParcial) {
      const nota = document.createElement('p');
      nota.className = 'nota-parcial';
      const ausentes = enumerar(analisis.analisis_parcial.modulos_ausentes);
      nota.textContent = ausentes
        ? `No se pudo completar ${ausentes}. El resultado no es concluyente.`
        : 'Un módulo del análisis no se pudo ejecutar. El resultado no es concluyente.';
      raiz.append(nota);
    }

    // Recién ahora el botón deja de pedir análisis y pasa a abrir el detalle.
    analisisActual = analisis;
    cerrarDetalle();
  }

  function mostrarError(mensaje: string): void {
    pintar('b-falla', ICONOS.falla, 'No se pudo analizar', `${mensaje}. Tocá para reintentar`);
  }

  mostrarInicial();

  return { anfitrion, mostrarInicial, mostrarAnalizando, mostrarVeredicto, mostrarError };
}
