/**
 * El mundo visual de la extensión: fichas de diseño, íconos y marca.
 *
 * Las tres superficies —indicador, detalle y panel de evidencia— comparten este
 * módulo. Cambiar una ficha acá las cambia a las tres.
 *
 * **La decisión de fondo es que el fondo no se pinta.** Las superficies se
 * apoyan en velos translúcidos sobre lo que haya debajo, así que la extensión
 * hereda el negro de *Lights out* o el azul carbón de *Dim* sin saber en cuál
 * está. Un `#000000` incrustado se vería como un parche recortado sobre el
 * segundo, que es exactamente el aspecto de artefacto externo que hay que
 * evitar.
 */

/**
 * Contrato de dirección de esta interfaz.
 *
 * Se inyecta como comentario en la raíz de sombra de cada indicador, de modo
 * que sobreviva al empaquetado y se pueda auditar en `dist/content.js` y en el
 * DOM andando.
 */
export const CONTRATO_DE_DIRECCION = `
TESIS: se adopta el sustrato de X y se rechaza su voz. La categoría resuelve esto
con una tarjeta de extensión que se anuncia como ajena; acá la estructura es de X
y lo propio es el veredicto y la marca.
MUNDO PROPIO: fondo heredado por velos translúcidos, nunca pintado. Bordes
#2F3336, texto #E7E9EA, apagado #71767B, azul #1D9BF0. Color reservado para el
veredicto con evidencia: rojo #F4212E, ámbar #FFD400, verde #00BA7C. La ausencia
es gris. Íconos propios sobre un círculo de 20 con trazo 2.
RELATO: el ciudadano ve una señal que parece de X, entiende que el juicio no es
de X, y llega a la fuente en dos toques.
PRIMER CUADRO: fila de ancho completo entre el texto del tuit y la barra de
acciones, 16 de radio y borde de 1, con la marca a la izquierda, el veredicto en
15 y el galón a la derecha.
FORMA: lenguaje visual de X en modo oscuro, fijado por el encargo; sin torneo de
mundos.
FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
`.trim();

/**
 * Fichas del modo oscuro de X.
 *
 * Los valores son los de la interfaz de X, no una aproximación: el propósito de
 * la extensión es no distinguirse del sustrato en el que vive.
 */
export const FICHAS = `
  /* -- Sustrato heredado ------------------------------------------------- */
  --velo: rgba(255, 255, 255, 0.03);
  --velo-fuerte: rgba(255, 255, 255, 0.07);
  --borde: #2f3336;
  --borde-vivo: #3e4144;

  /* -- Tinta ------------------------------------------------------------- */
  --tinta: #e7e9ea;
  /*
   * Escalon intermedio, y la ficha que usa **todo texto que haya que leer**.
   *
   * El gris de X (#71767b) da 4,6:1 sobre el negro de *Lights out*, pero 3,6:1
   * sobre el carbon de *Dim* y apenas 2,9:1 sobre el velo ambar en *Dim*: por
   * debajo del minimo de 4,5:1 en las dos superficies que esta extension usa
   * mas. Sirve para dibujo —el aro de un icono en reposo— y no para palabras.
   *
   * Medido: 9,4:1 sobre negro puro, 7,4:1 sobre *Dim*, y entre 5,9:1 y 8,7:1
   * sobre los velos de color de ambos fondos.
   */
  --tinta-media: #a8aeb2;
  --tinta-apagada: #71767b;

  /* -- Acentos de X ------------------------------------------------------ */
  --azul: #1d9bf0;
  --rojo: #f4212e;
  --ambar: #ffd400;
  --verde: #00ba7c;

  /* Los mismos acentos en velo, para fondos y bordes de estado. */
  --rojo-velo: rgba(244, 33, 46, 0.12);
  --rojo-borde: rgba(244, 33, 46, 0.4);
  --ambar-velo: rgba(255, 212, 0, 0.1);
  --ambar-borde: rgba(255, 212, 0, 0.35);
  --verde-velo: rgba(0, 186, 124, 0.12);
  --verde-borde: rgba(0, 186, 124, 0.4);
  --azul-velo: rgba(29, 155, 240, 0.12);
  --azul-borde: rgba(29, 155, 240, 0.4);

  /* -- Métrica ----------------------------------------------------------- */
  --radio: 16px;
  --radio-chico: 8px;
  --pastilla: 9999px;

  /* X compone su interfaz sobre una tipografía propia que no se puede
     redistribuir. La pila de respaldo es la misma que X usa cuando la suya no
     carga, así que la métrica coincide en lugar de aproximarse. */
  --letra: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica,
    Arial, sans-serif;

  /* La curva de X: salida rápida y asentado largo. */
  --curva: cubic-bezier(0.16, 1, 0.3, 1);
`;

/**
 * Íconos de estado, dibujados en una sola gramática.
 *
 * Todos viven en una caja de 20 sobre un círculo de radio 7,5 con trazo de 2 y
 * extremos redondeados. Que compartan el círculo es lo que los hace leerse como
 * una familia y no como una colección: el estado cambia lo que pasa **dentro**
 * del círculo, o el círculo mismo cuando lo que falta es la evidencia.
 *
 * Heredan el color por `currentColor`, así que el estado lo fija el CSS.
 */
const CAJA = 'viewBox="0 0 20 20" width="20" height="20" aria-hidden="true"';
const TRAZO =
  'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"';

/** Círculo continuo, base de casi todos los íconos. */
const ARO = `<circle cx="10" cy="10" r="7.5" ${TRAZO} />`;

export const ICONOS = {
  /**
   * La marca. Un círculo partido: una mitad afirmada, la otra por verificar.
   *
   * Es a la vez el ícono del estado inicial y la marca de atribución, y esa
   * doble función es deliberada: lo primero que el ciudadano ve del sistema es
   * la marca del sistema, no un signo de pregunta genérico.
   */
  marca: `<svg ${CAJA}>${ARO}<path d="M10 2.5a7.5 7.5 0 0 0 0 15z" fill="currentColor" /></svg>`,

  /** Contradicho: el círculo tachado por una barra. */
  contradicho: `<svg ${CAJA}>${ARO}<path d="M6.2 10h7.6" ${TRAZO} /></svg>`,

  /** Sospechoso: la advertencia clásica, dibujada y no tipografiada. */
  sospechoso: `<svg ${CAJA}>${ARO}<path d="M10 5.9v4.4" ${TRAZO} /><circle cx="10" cy="13.7" r="1.15" fill="currentColor" /></svg>`,

  /** Verificado: el círculo con la marca de comprobación. */
  verificado: `<svg ${CAJA}>${ARO}<path d="M6.5 10.1l2.5 2.5 4.5-5" ${TRAZO} /></svg>`,

  /**
   * Sin contraste externo: el mismo círculo, discontinuo.
   *
   * La ausencia de evidencia se dibuja como ausencia de trazo. Es la traducción
   * visual más directa del principio que el producto sostiene: un vacío no se
   * rellena.
   */
  sinContraste: `<svg ${CAJA}><circle cx="10" cy="10" r="7.5" ${TRAZO} stroke-dasharray="2.4 3.4" /></svg>`,

  /** Análisis parcial: media circunferencia firme, media discontinua. */
  parcial: `<svg ${CAJA}><path d="M10 2.5a7.5 7.5 0 0 0 0 15" ${TRAZO} /><path d="M10 2.5a7.5 7.5 0 0 1 0 15" ${TRAZO} stroke-dasharray="2.4 3.4" /></svg>`,

  /** Falla: el círculo con la barra oblicua de lo que no se pudo hacer. */
  falla: `<svg ${CAJA}>${ARO}<path d="M5.6 14.4l8.8-8.8" ${TRAZO} /></svg>`,

  /** Galón de despliegue. */
  galon: `<svg viewBox="0 0 20 20" width="18" height="18" aria-hidden="true"><path d="M5.5 8l4.5 4.5L14.5 8" ${TRAZO} /></svg>`,

  /** Enlace saliente, en la fila de cada fuente. */
  saliente: `<svg viewBox="0 0 20 20" width="15" height="15" aria-hidden="true"><path d="M8.5 4.5H5.2A1.2 1.2 0 0 0 4 5.7v9.1a1.2 1.2 0 0 0 1.2 1.2h9.1a1.2 1.2 0 0 0 1.2-1.2v-3.3" ${TRAZO} /><path d="M11.6 3.6H16.4V8.4" ${TRAZO} /><path d="M16.4 3.6L9.7 10.3" ${TRAZO} /></svg>`,
} as const;

/**
 * La marca de atribución, siempre visible.
 *
 * Existe para que la integración no se vuelva suplantación. La extensión toma
 * prestado el lenguaje visual de X, así que sin esta marca el ciudadano podría
 * concluir que el veredicto lo emite la plataforma —y el sistema no juzga en
 * nombre de nadie más que de las fuentes que enlaza—.
 *
 * El rótulo es funcional y no un nombre de producto: el proyecto todavía no
 * tiene uno, e inventarlo acá sería inventar un hecho.
 */
export function marcaDeAtribucion(): HTMLElement {
  const marca = document.createElement('span');
  marca.className = 'atribucion';
  marca.innerHTML = ICONOS.marca;

  const rotulo = document.createElement('span');
  rotulo.textContent = 'Análisis independiente';
  marca.append(rotulo);

  return marca;
}

/**
 * Escribe en un enlace su texto y el ícono que dice que abre fuera de X.
 *
 * El ícono queda unido a la última palabra por una cola sin corte de línea. Un
 * título que llena su última línea empujaría al ícono al renglón siguiente, y
 * ahí queda solo bajo el bloque de texto sin decir a qué enlace pertenece.
 *
 * La cola se arma únicamente si hay dónde cortar y si la última palabra es
 * corta: pegarle el ícono a una palabra larga —una dirección web sin espacios,
 * por ejemplo— dejaría un bloque irrompible que se sale de la columna del tuit,
 * que es peor que el ícono colgado.
 */
export function escribirEnlaceSaliente(enlace: HTMLAnchorElement, texto: string): void {
  const limpio = texto.trim();
  const corte = limpio.lastIndexOf(' ');
  const ultima = corte === -1 ? limpio : limpio.slice(corte + 1);

  const salida = document.createElement('span');
  salida.className = 'f-salida';
  salida.setAttribute('aria-hidden', 'true');
  salida.innerHTML = ICONOS.saliente;

  if (corte === -1 || ultima.length > 20) {
    enlace.append(limpio, salida);
    return;
  }

  enlace.append(`${limpio.slice(0, corte)} `);
  const cola = document.createElement('span');
  cola.className = 'f-cola';
  cola.append(ultima, salida);
  enlace.append(cola);
}

/**
 * Estilos compartidos por las tres superficies: la marca y el icono de salida.
 *
 * El icono de salida aparece en dos lugares —el enlace de cada razón, en el
 * detalle, y el de cada fuente, en la evidencia— y por eso su regla es una sola.
 * Antes el detalle usaba una flecha ↗ de la fuente tipográfica y la evidencia el
 * trazo dibujado: la misma promesa, «esto abre el documento fuera de X»,
 * anunciada con dos marcas distintas dentro de la misma tarjeta.
 *
 * Va **dentro del renglón** y no como segundo ítem de una caja flexible: como
 * ítem flexible quedaba centrado contra el alto de todo el bloque, así que en un
 * título de dos líneas flotaba a media altura y lejos de la última palabra, sin
 * pertenecer a ninguna de las dos.
 */
export const ESTILOS_MARCA = `
.f-salida {
  display: inline-block;
  margin-left: 5px;
  vertical-align: -2px;
  opacity: 0.55;
}
.f-salida svg { display: block; }
/*
 * La última palabra y el ícono viajan juntos. Suelto en el flujo, el ícono era
 * una caja más que buscaba renglón por su cuenta: en un título que llenaba su
 * última línea caía solo al renglón siguiente, y un ícono huérfano bajo un
 * bloque de texto no dice de qué enlace habla.
 */
.f-cola { white-space: nowrap; }

.atribucion {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: var(--tinta-media);
  font-size: 13px;
  line-height: 16px;
  letter-spacing: 0.01em;
  white-space: nowrap;
}
.atribucion svg { width: 15px; height: 15px; flex: 0 0 15px; }
`;
