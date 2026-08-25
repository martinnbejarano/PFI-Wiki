/**
 * Detalle del veredicto (RF-09, CU-02): la segunda pantalla del *mockup*.
 *
 * El marcado y el CSS se portan de la pantalla `?pantalla=popup` de
 * `wiki/assets/mockups/mockups.html`, igual que el indicador se portó de
 * `?pantalla=badge`. Los nombres de clase son los del *mockup* —`.popup`,
 * `.p-tapa`, `.p-vered`, `.p-score`, `.p-sec`, `.mod`, `.barra`, `.razones`,
 * `.link-f`, `.sin-f`— para que la correspondencia con la figura impresa en el
 * documento se pueda verificar leyendo, y no de memoria.
 *
 * El panel se monta dentro del **mismo *shadow DOM* que el indicador**: se abre
 * desde el indicador y se despliega sobre la *timeline*. No es la ventana
 * emergente de la barra de herramientas, que solo informa si el servicio local
 * está en pie.
 *
 * Cuatro divergencias respecto de la figura, todas deliberadas:
 *
 * 1. **El bloque de la afirmación** (`.e-claim`) se toma de la tercera pantalla
 *    del *mockup*, la de evidencia, que es donde está dibujado. La segunda no
 *    lo lleva, y este ticket exige mostrar la afirmación extraída y su tipo en
 *    el detalle: se reusa el patrón visual ya publicado en lugar de inventar
 *    uno nuevo.
 * 2. **Del pie del *mockup* se porta un solo botón.** El de «Ver las 7 fuentes»
 *    abre el panel de evidencia (`evidencia.ts`), que es la tercera pantalla, y
 *    aparece únicamente cuando hay fuentes que mostrar. El de «Reportar» no se
 *    porta: el reporte de veredictos incorrectos (RF-11) está fuera del alcance
 *    de la *spec*, y un botón que no hace nada promete más de lo que la
 *    demostración entrega.
 * 3. **El ancho** es fluido con un tope de 380 px, el ancho de la tarjeta del
 *    *mockup*. En la *timeline* el panel se inserta dentro de la columna del
 *    tuit, que en pantallas angostas mide menos que eso.
 * 4. **El módulo de credibilidad** se dibuja siempre con el patrón de módulo
 *    ausente —barra rayada y etiqueta— aunque traiga un número. Ver
 *    `moduloCredibilidad`.
 * 5. **La justificación en lenguaje natural** se agrega como párrafo bajo la
 *    afirmación. La figura solo dibuja las razones, pero RF-06 pide las dos
 *    cosas y el contrato las trae separadas: las razones enumeran, la
 *    justificación explica.
 */

import type { RespuestaAnalisis, TipoAfirmacion, Veredicto } from '../compartido/contrato';
import { renderizarEvidencia } from './evidencia';

/**
 * Estilos del detalle, portados del *mockup*.
 *
 * Las variables de color se declaran sobre `.popup` y no sobre `:host` porque
 * el indicador ya reclama `:host` con `all: initial`. Los valores son los
 * mismos del `:root` del *mockup*.
 */
export const ESTILOS_DETALLE = `
.popup {
  --falso: #c0392b; --falso-bg: #fdecea;
  --sosp: #a56a00;  --sosp-bg: #fdf4e3;
  --ok: #1a7a4c;    --ok-bg: #e9f6ef;
  --wait: #5b6570;  --wait-bg: #f1f3f5;
  --tinta: #15202b; --gris: #5b6570; --linea: #e2e6ea; --fondo: #f7f9fa;
  --marca: #1b4f8f;

  width: 100%;
  max-width: 380px;
  margin: 8px 0 2px;
  background: #fff;
  color: var(--tinta);
  border: 1px solid var(--linea);
  border-radius: 12px;
  box-shadow: 0 8px 28px rgba(21, 32, 43, .13);
  overflow: hidden;
  text-align: left;
}

.p-tapa { padding: 16px 18px; border-bottom: 1px solid var(--linea); }
.p-tapa.falso { background: var(--falso-bg); }
.p-tapa.sosp { background: var(--sosp-bg); }
.p-tapa.ok { background: var(--ok-bg); }
.p-tapa.parcial { background: var(--wait-bg); }
.p-vered {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 16px;
  font-weight: 700;
  color: var(--falso);
}
.p-tapa.sosp .p-vered { color: var(--sosp); }
.p-tapa.ok .p-vered { color: var(--ok); }
.p-tapa.parcial .p-vered { color: var(--wait); }
.p-score { font-size: 34px; font-weight: 800; letter-spacing: -.02em; margin: 6px 0 2px; }
.p-sub { font-size: 12.5px; color: var(--gris); }

.e-claim {
  margin: 12px 18px;
  padding: 11px 13px;
  background: var(--fondo);
  border-left: 3px solid var(--marca);
  border-radius: 0 6px 6px 0;
  font-size: 13.5px;
}
.e-claim span {
  display: block;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: .05em;
  color: var(--gris);
  margin-bottom: 4px;
}
.e-claim.vacia { border-left-color: #d3d9df; color: var(--gris); font-style: italic; }

.p-sec { padding: 14px 18px; border-top: 1px solid var(--linea); }
.p-sec h3 {
  margin: 0 0 10px;
  font-size: 11px;
  letter-spacing: .06em;
  text-transform: uppercase;
  color: var(--gris);
}
.mod { margin-bottom: 11px; }
.mod:last-child { margin-bottom: 0; }
.mod-t { display: flex; justify-content: space-between; gap: 10px; font-size: 13px; margin-bottom: 4px; }
.mod-t span:last-child { font-variant-numeric: tabular-nums; color: var(--gris); white-space: nowrap; }
.barra { height: 6px; background: #eef1f4; border-radius: 3px; overflow: hidden; }
.barra i { display: block; height: 100%; border-radius: 3px; }
.mod-nota { margin: 5px 0 0; font-size: 11.5px; line-height: 1.45; color: var(--gris); }

.razones { margin: 0; padding-left: 17px; font-size: 13.5px; }
.razones li { margin-bottom: 6px; }
.razones li:last-child { margin-bottom: 0; }
.link-f {
  display: inline-block;
  margin: 3px 5px 0 0;
  font-size: 12px;
  color: var(--marca);
  text-decoration: none;
  background: #eaf1fa;
  border: 1px solid #c4d8f0;
  padding: 1px 7px;
  border-radius: 4px;
  white-space: nowrap;
}
.sin-f { display: inline-block; margin-top: 3px; font-size: 11.5px; color: var(--gris); font-style: italic; }

.p-just { margin: 0; padding: 14px 18px; border-top: 1px solid var(--linea); font-size: 13.5px; }

.p-pie { display: flex; gap: 8px; padding: 13px 18px; border-top: 1px solid var(--linea); }
.btn {
  flex: 1;
  padding: 9px;
  border-radius: 8px;
  font: inherit;
  font-size: 13.5px;
  font-weight: 600;
  cursor: pointer;
  border: 1px solid var(--marca);
  text-align: center;
}
.btn.pri { background: var(--marca); color: #fff; }
.btn.sec { background: #fff; color: var(--marca); }
`;

/** Tapa del panel por veredicto: clase, ícono y título, como en el *mockup*. */
const TAPA: Record<Veredicto, { clase: string; figura: string; titulo: string }> = {
  contradicho_por_fuentes_oficiales: {
    clase: 'falso',
    figura: '▲',
    titulo: 'Contradicho por fuentes oficiales',
  },
  informacion_sospechosa: { clase: 'sosp', figura: '●', titulo: 'Información sospechosa' },
  parece_verificado: { clase: 'ok', figura: '✓', titulo: 'Parece verificado' },
  sin_contraste_externo: { clase: 'parcial', figura: '◐', titulo: 'Sin contraste externo' },
};

/** Nombre legible de cada tipo de afirmación de RF-04. */
const TIPOS: Record<TipoAfirmacion, string> = {
  normativa: 'normativa',
  dato_economico: 'dato económico',
  salud: 'salud',
  educacion: 'educación',
  otro: 'otro',
};

/** Trama del *mockup* para la barra de un módulo sin dato. */
const TRAMA_SIN_DATO =
  'repeating-linear-gradient(45deg,#e2e6ea,#e2e6ea 4px,#f5f7f9 4px,#f5f7f9 8px)';

/** Formatea un puntaje con coma decimal, como en el *mockup*. */
function comaDecimal(valor: number): string {
  return valor.toFixed(2).replace('.', ',');
}

/**
 * Color de la barra de un módulo.
 *
 * Las bandas son presentacionales y nada más: los umbrales que deciden el
 * veredicto viven en la configuración del servicio (RNF-16) y llegan con el
 * ticket #24. Los cortes reproducen los de la figura, donde 0,82 y 0,89 se
 * dibujan en rojo y 0,74 en ámbar.
 */
function colorDeBarra(valor: number): string {
  if (valor >= 0.8) {
    return 'var(--falso)';
  }
  if (valor >= 0.4) {
    return 'var(--sosp)';
  }
  return 'var(--ok)';
}

/** Un módulo del desglose: rótulo, valor y barra. */
function modulo(rotulo: string, valor: number): HTMLElement {
  const nodo = document.createElement('div');
  nodo.className = 'mod';

  const encabezado = document.createElement('div');
  encabezado.className = 'mod-t';
  const nombre = document.createElement('span');
  nombre.textContent = rotulo;
  const cifra = document.createElement('span');
  cifra.textContent = comaDecimal(valor);
  encabezado.append(nombre, cifra);

  const barra = document.createElement('div');
  barra.className = 'barra';
  const relleno = document.createElement('i');
  relleno.style.width = `${Math.round(valor * 100)}%`;
  relleno.style.background = colorDeBarra(valor);
  barra.append(relleno);

  nodo.append(encabezado, barra);
  return nodo;
}

/**
 * El módulo de credibilidad de la cuenta, marcado como no implementado.
 *
 * Se dibuja con el patrón que el *mockup* reserva para un módulo sin dato
 * —barra rayada y etiqueta— **aunque el servicio devuelva un número**. Es
 * deliberado: el valor es arbitrario, derivado de una semilla del *handle*, y
 * una barra rellena a su altura lo presentaría como una medición. La cifra se
 * muestra igual, porque es lo que hace verificable que sea estable entre
 * recargas, pero acompañada de la etiqueta y de la nota que dicen qué es.
 *
 * Cuando el Módulo 2 se implemente de verdad, este caso desaparece: la bandera
 * `no_implementado` llega en falso y el módulo se dibuja como los otros dos.
 */
function moduloCredibilidad(valor: number, noImplementado: boolean): HTMLElement {
  if (!noImplementado) {
    return modulo('Señales de la cuenta autora', valor);
  }

  const nodo = document.createElement('div');
  nodo.className = 'mod';

  const encabezado = document.createElement('div');
  encabezado.className = 'mod-t';
  const nombre = document.createElement('span');
  nombre.textContent = 'Señales de la cuenta autora';
  const cifra = document.createElement('span');
  cifra.textContent = `${comaDecimal(valor)} · sin dato`;
  encabezado.append(nombre, cifra);

  const barra = document.createElement('div');
  barra.className = 'barra';
  const relleno = document.createElement('i');
  relleno.style.width = '100%';
  relleno.style.background = TRAMA_SIN_DATO;
  barra.append(relleno);

  const nota = document.createElement('p');
  nota.className = 'mod-nota';
  nota.textContent =
    'Módulo no implementado en este prototipo: el valor es arbitrario y no ' +
    'mide la credibilidad de la cuenta. No lo tomes como un dato.';

  nodo.append(encabezado, barra, nota);
  return nodo;
}

/** El bloque con la afirmación verificable extraída y su tipo (RF-04). */
function bloqueAfirmacion(analisis: RespuestaAnalisis): HTMLElement {
  const nodo = document.createElement('div');
  nodo.className = 'e-claim';
  const rotulo = document.createElement('span');
  const cuerpo = document.createTextNode('');

  if (analisis.afirmacion.trim() === '') {
    // El servicio devuelve la afirmación vacía cuando la publicación no
    // contiene ninguna verificable —una opinión, una broma, un saludo—. Se dice
    // así, en lugar de repetir el texto del tuit como si fuera la afirmación
    // analizada, que es la confusión que RF-04 existe para evitar.
    nodo.classList.add('vacia');
    rotulo.textContent = 'Sin afirmación verificable';
    cuerpo.textContent =
      'No se identificó en esta publicación ningún hecho que se pueda ' +
      'contrastar contra una fuente.';
  } else {
    rotulo.textContent = `Afirmación verificable extraída · tipo: ${TIPOS[analisis.tipo_afirmacion]}`;
    cuerpo.textContent = `«${analisis.afirmacion}»`;
  }

  nodo.append(rotulo, cuerpo);
  return nodo;
}

/** Una sección con título, como las `.p-sec` del *mockup*. */
function seccion(titulo: string, contenido: Node[]): HTMLElement {
  const nodo = document.createElement('div');
  nodo.className = 'p-sec';
  const encabezado = document.createElement('h3');
  encabezado.textContent = titulo;
  nodo.append(encabezado, ...contenido);
  return nodo;
}

/**
 * La lista de razones, cada una con el enlace a la fuente que la respalda.
 *
 * Una razón sin `fuente_url` lleva la etiqueta gris del *mockup* en lugar de un
 * enlace: separa visualmente lo que el sistema **encontró** de lo que el
 * sistema **infirió**, y solo lo primero lo puede verificar quien lee (RNF-06).
 */
function listaDeRazones(analisis: RespuestaAnalisis): HTMLElement {
  const lista = document.createElement('ul');
  lista.className = 'razones';

  for (const razon of analisis.razones) {
    const elemento = document.createElement('li');
    elemento.append(document.createTextNode(`${razon.texto} `));

    if (razon.fuente_url) {
      const fuente = analisis.fuentes.find((f) => f.url === razon.fuente_url);
      const enlace = document.createElement('a');
      enlace.className = 'link-f';
      enlace.href = razon.fuente_url;
      enlace.target = '_blank';
      enlace.rel = 'noopener noreferrer';
      enlace.textContent = `${fuente ? fuente.titulo : razon.fuente_url} ↗`;
      elemento.append(enlace);
    } else {
      const etiqueta = document.createElement('span');
      etiqueta.className = 'sin-f';
      etiqueta.textContent = 'análisis propio del sistema';
      elemento.append(etiqueta);
    }

    lista.append(elemento);
  }

  return lista;
}

/**
 * El pie del detalle, con el botón que abre el panel de evidencia (RF-09).
 *
 * Es el pie que el *mockup* dibuja bajo el detalle y que el ticket anterior
 * dejó libre a propósito para esto. El panel se despliega **dentro del mismo
 * panel de detalle**, y por lo tanto dentro del mismo *shadow DOM*: no abre
 * ninguna ventana ni saca al ciudadano de su *timeline*, que es lo que pide
 * CU-03.
 *
 * Sin fuentes no hay pie. Un botón que abriera un panel vacío prometería una
 * evidencia que no existe, y la tapa del detalle ya dijo que el análisis quedó
 * sin contraste externo.
 */
function agregarPieDeEvidencia(panel: HTMLElement, analisis: RespuestaAnalisis): void {
  const cantidad = analisis.fuentes.length;
  if (cantidad === 0) {
    return;
  }

  const pie = document.createElement('div');
  pie.className = 'p-pie';

  const boton = document.createElement('button');
  boton.type = 'button';
  boton.className = 'btn pri';
  boton.setAttribute('aria-expanded', 'false');

  const abrir = cantidad === 1 ? 'Ver la fuente' : `Ver las ${cantidad} fuentes`;
  const cerrar = cantidad === 1 ? 'Ocultar la fuente' : 'Ocultar las fuentes';
  boton.textContent = abrir;

  let evidencia: HTMLElement | null = null;

  boton.addEventListener('click', () => {
    if (evidencia) {
      evidencia.remove();
      evidencia = null;
      boton.textContent = abrir;
      boton.setAttribute('aria-expanded', 'false');
      return;
    }
    evidencia = renderizarEvidencia(analisis, TIPOS[analisis.tipo_afirmacion]);
    if (!evidencia) {
      return;
    }
    panel.append(evidencia);
    boton.textContent = cerrar;
    boton.setAttribute('aria-expanded', 'true');
  });

  pie.append(boton);
  panel.append(pie);
}

/**
 * Construye el panel de detalle a partir de un análisis.
 *
 * @param handle Cuenta autora del tuit. Aparece en la tapa como atribución de
 * la publicación analizada, tal como en la figura. El juicio que el panel
 * enuncia es siempre sobre la afirmación y nunca sobre quien la publicó
 * (RNF-07).
 */
export function renderizarDetalle(
  analisis: RespuestaAnalisis,
  handle: string,
): HTMLElement {
  const panel = document.createElement('div');
  panel.className = 'popup';

  const tapa = TAPA[analisis.veredicto];
  const nodoTapa = document.createElement('div');
  nodoTapa.className = `p-tapa ${tapa.clase}`;

  const veredicto = document.createElement('div');
  veredicto.className = 'p-vered';
  const figura = document.createElement('span');
  figura.setAttribute('aria-hidden', 'true');
  figura.textContent = tapa.figura;
  veredicto.append(figura, document.createTextNode(tapa.titulo));

  const puntaje = document.createElement('div');
  puntaje.className = 'p-score';
  const subtitulo = document.createElement('div');
  subtitulo.className = 'p-sub';

  if (analisis.veredicto === 'sin_contraste_externo') {
    // Sin contraste externo no hay porcentaje: hay un guión. Es la misma
    // decisión que la columna derecha del *mockup* y la que exige RF-08. Un
    // número calculado sobre módulos que no aportaron nada se leería igual de
    // confiable que el resto, y no lo es.
    puntaje.textContent = '—';
    subtitulo.textContent = `Sin evidencia externa con la cual contrastar · ${handle}`;
  } else {
    puntaje.textContent = `${Math.round(analisis.puntaje_final * 100)}%`;
    subtitulo.textContent = `Probabilidad estimada de desinformación · ${handle}`;
  }

  nodoTapa.append(veredicto, puntaje, subtitulo);

  const justificacion = document.createElement('p');
  justificacion.className = 'p-just';
  justificacion.textContent = analisis.justificacion;

  panel.append(
    nodoTapa,
    bloqueAfirmacion(analisis),
    justificacion,
    seccion('Qué aportó cada señal', [
      modulo('Análisis del texto', analisis.puntajes.clasificador.valor),
      moduloCredibilidad(
        analisis.puntajes.credibilidad.valor,
        analisis.puntajes.credibilidad.no_implementado,
      ),
      modulo('Contraste con fuentes', analisis.puntajes.contraste.valor),
    ]),
  );

  if (analisis.razones.length > 0) {
    panel.append(seccion('Por qué', [listaDeRazones(analisis)]));
  }

  agregarPieDeEvidencia(panel, analisis);

  return panel;
}
