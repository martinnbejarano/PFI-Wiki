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
 *
 * **El análisis parcial (RF-08 y RNF-11)** se dibuja con el flujo alternativo
 * *6a* que el propio *mockup* ya publica a la derecha de la misma pantalla, y
 * no con un patrón nuevo: tapa gris que dice «Análisis parcial», un guión en
 * lugar del porcentaje, el aviso que explica qué pasó, y la barra rayada con la
 * etiqueta *sin dato* en el módulo que faltó. Es el mismo patrón que el módulo
 * de credibilidad no implementado ya usaba. La decisión que sostiene la
 * pantalla es la que el *mockup* enuncia: la ausencia de un módulo se muestra
 * como ausencia y no se disimula con aritmética, porque un promedio ponderado
 * calculado con un módulo caído devuelve un número que parece igual de
 * confiable que los demás y no lo es.
 */

import {
  falta,
  MODULO_AUSENTE,
  type RespuestaAnalisis,
  type TipoAfirmacion,
  type Veredicto,
} from '../compartido/contrato';
import { renderizarEvidencia } from './evidencia';
import { ICONOS, marcaDeAtribucion } from './tema';

/**
 * Estilos del detalle, portados del *mockup*.
 *
 * Las variables de color se declaran sobre `.popup` y no sobre `:host` porque
 * el indicador ya reclama `:host` con `all: initial`. Los valores son los
 * mismos del `:root` del *mockup*.
 */
export const ESTILOS_DETALLE = `
/* -- El detalle --------------------------------------------------------- */
/*
 * Se despliega bajo el indicador y dentro del mismo ancho, como X anida una
 * cita dentro de un tuit: mismo radio, mismo borde de 1, ningun fondo propio.
 * No es una ventana flotante porque no interrumpe una tarea; es mas contenido
 * sobre el que ya se estaba leyendo.
 */
/*
 * El detalle no es una segunda tarjeta: es la misma que crece. X nunca apila dos
 * tarjetas bordeadas bajo un tuit, y apiladas el veredicto se leia dos veces,
 * como el componente renderizado por duplicado y no como jerarquia. El indicador
 * cierra sus esquinas de abajo y suelta su filete inferior mientras esto esta
 * abierto; ver la regla del indicador para aria-expanded.
 */
.popup {
  margin-top: 0;
  border: 1px solid var(--borde);
  border-top: 0;
  border-radius: 0 0 var(--radio) var(--radio);
  overflow: hidden;
  color: var(--tinta);
  font: 400 15px/20px var(--letra);
  animation: desplegar 0.28s var(--curva) both;
}

@keyframes desplegar {
  from { transform: translateY(-4px); opacity: 0; }
  to { transform: none; opacity: 1; }
}

/* -- La tapa ------------------------------------------------------------ */
.p-tapa {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: center;
  gap: 4px 16px;
  padding: 14px 16px;
  border-bottom: 1px solid var(--borde);
}
.p-tapa .atribucion { grid-column: 1; }
/*
 * La tapa no repite el titulo del veredicto —la ficha ya lo dice, doce pixeles
 * mas arriba— y se queda con lo que solo ella aporta: la cifra, su sustantivo y
 * la atribucion.
 */
.p-vered { display: none; }
.p-score {
  grid-column: 2;
  grid-row: 1 / span 3;
  align-self: center;
  font-variant-numeric: tabular-nums;
  font-weight: 700;
  font-size: 27px;
  line-height: 32px;
  letter-spacing: -0.02em;
}
.p-fig { display: grid; place-items: center; flex: 0 0 20px; }
.p-fig svg { display: block; }

/*
 * Lleva la cifra a palabras y es lo que se lee junto al numero grande, asi que
 * no puede ir en el gris que X reserva a las marcas de tiempo: sobre el carbon
 * de *Dim* ese gris no llega al contraste minimo.
 */
.p-sub {
  grid-column: 1;
  color: var(--tinta-media);
  font-size: 14px;
  line-height: 18px;
}

.p-tapa.falso .p-vered, .p-tapa.falso .p-score { color: var(--rojo); }
.p-tapa.sosp .p-vered, .p-tapa.sosp .p-score { color: var(--ambar); }
.p-tapa.ok .p-vered, .p-tapa.ok .p-score { color: var(--verde); }
.p-tapa.parcial .p-vered, .p-tapa.parcial .p-score { color: var(--tinta-apagada); }

/* -- Secciones ---------------------------------------------------------- */
.p-sec { padding: 14px 16px; border-bottom: 1px solid var(--borde); }
.p-sec h3 {
  margin: 0 0 10px;
  color: var(--tinta-apagada);
  font: 700 13px/16px var(--letra);
  letter-spacing: 0.02em;
  text-transform: uppercase;
}

/* -- La afirmacion analizada -------------------------------------------- */
/*
 * Va primero y en la tinta plena: es lo que el ciudadano necesita para juzgar
 * si el sistema analizo lo que el queria que analizara.
 */
.e-claim {
  padding: 12px 14px;
  border: 1px solid var(--borde);
  border-radius: var(--radio-chico);
  background: var(--velo);
  font-size: 15px;
  line-height: 21px;
}
.e-claim span {
  display: block;
  margin-top: 6px;
  color: var(--tinta-apagada);
  font-size: 13px;
  line-height: 16px;
}
.e-claim.vacia { color: var(--tinta-apagada); font-style: normal; }

/* -- Los tres puntajes parciales ---------------------------------------- */
.mod + .mod { margin-top: 12px; }
.mod-t {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 12px;
  margin-bottom: 6px;
  font-size: 14px;
  line-height: 18px;
}
.mod-t span {
  color: var(--tinta-apagada);
  font-variant-numeric: tabular-nums;
  font-size: 13px;
}
.barra {
  height: 4px;
  border-radius: var(--pastilla);
  background: rgba(231, 233, 234, 0.1);
  overflow: hidden;
}
.barra i { display: block; height: 100%; border-radius: inherit; }
/*
 * La nota del modulo no implementado. No es una aclaracion menor: es lo que
 * impide leer un valor inventado como si fuera una medicion.
 */
.mod-nota {
  margin: 6px 0 0;
  color: var(--tinta-apagada);
  font: 400 13px/17px var(--letra);
}

/* -- Justificacion y razones -------------------------------------------- */
.p-just { margin: 0; font-size: 15px; line-height: 21px; }
.razones { margin: 10px 0 0; padding: 0; list-style: none; }
.razones li {
  position: relative;
  padding: 0 0 0 16px;
  font-size: 14px;
  line-height: 20px;
}
.razones li + li { margin-top: 8px; }
.razones li::before {
  content: '';
  position: absolute;
  left: 2px;
  top: 8px;
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: var(--tinta-apagada);
}
/*
 * Lo que el sistema encontro se distingue de lo que infirio: la razon con
 * fuente lleva enlace en el azul de X; la que no la tiene lleva un rotulo
 * apagado, porque no hay documento que abrir.
 */
.link-f { color: var(--azul); text-decoration: none; }
.link-f:hover { text-decoration: underline; text-underline-offset: 2px; }
.sin-f {
  display: inline-block;
  margin-left: 6px;
  padding: 1px 7px;
  border: 1px solid var(--borde);
  border-radius: var(--pastilla);
  color: var(--tinta-apagada);
  font-size: 12px;
  line-height: 16px;
}

/* -- El pie ------------------------------------------------------------- */
.p-pie {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 12px 16px;
}
.btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border: 1px solid transparent;
  border-radius: var(--pastilla);
  font: 700 14px/16px var(--letra);
  cursor: pointer;
  transition: background-color 0.2s var(--curva), border-color 0.2s var(--curva);
}
.btn.pri { background: var(--tinta); color: #0f1419; }
.btn.pri:hover { background: #d7dbdc; }
.btn.sec { background: transparent; border-color: var(--borde-vivo); color: var(--tinta); }
.btn.sec:hover { background: var(--velo); }
.btn:focus-visible { outline: 2px solid var(--azul); outline-offset: 2px; }

.popup .nota-parcial { margin: 0; border: 0; border-top: 1px solid var(--borde); border-radius: 0; }

@media (prefers-reduced-motion: reduce) {
  .popup { animation: none; }
  .btn { transition: none; }
}
`;

/** Tapa del panel por veredicto: clase, ícono y título, como en el *mockup*. */
const TAPA: Record<Veredicto, { clase: string; figura: string; titulo: string }> = {
  contradicho_por_fuentes_oficiales: {
    clase: 'falso',
    figura: ICONOS.contradicho,
    titulo: 'Contradicho por fuentes oficiales',
  },
  informacion_sospechosa: { clase: 'sosp', figura: ICONOS.sospechoso, titulo: 'Información sospechosa' },
  parece_verificado: { clase: 'ok', figura: ICONOS.verificado, titulo: 'Parece verificado' },
  sin_contraste_externo: { clase: 'parcial', figura: ICONOS.sinContraste, titulo: 'Sin contraste externo' },
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
/*
 * La trama del modulo sin dato. Se dibuja con velos y no con grises fijos, para
 * que se lea igual sobre el negro de *Lights out* y sobre el carbon de *Dim*.
 */
const TRAMA_SIN_DATO =
  'repeating-linear-gradient(45deg,rgba(231,233,234,0.22),rgba(231,233,234,0.22) 4px,rgba(231,233,234,0.06) 4px,rgba(231,233,234,0.06) 8px)';

/** Formatea un puntaje con coma decimal, como en el *mockup*. */
function comaDecimal(valor: number): string {
  return valor.toFixed(2).replace('.', ',');
}

/**
 * Color de la barra de un módulo.
 *
 * Las bandas son presentacionales y nada más: los umbrales que deciden el
 * veredicto viven en la configuración del servicio (RNF-16) y no acá. Los
 * cortes reproducen los de la figura, donde 0,82 y 0,89 se dibujan en rojo y
 * 0,74 en ámbar.
 *
 * **Deliberadamente no se los sincroniza con los umbrales del servicio.** Son
 * dos cosas distintas: allá los cortes deciden el nivel del veredicto a partir
 * del puntaje final, acá el color acompaña la lectura de cada barra por
 * separado. Traerlos del servicio obligaría a exponerlos en el contrato y
 * ataría el color de una barra parcial a un umbral que no habla de ella.
 */
function colorDeBarra(valor: number): string {
  if (valor >= 0.8) {
    return 'var(--rojo)';
  }
  if (valor >= 0.4) {
    return 'var(--ambar)';
  }
  return 'var(--verde)';
}

/**
 * Un módulo del desglose: rótulo, valor y barra.
 *
 * Con `ausente` en verdadero se dibuja el patrón del *mockup* para un módulo
 * que no se pudo ejecutar: la etiqueta dice *sin dato* en lugar de una cifra y
 * la barra va rayada al ancho completo. **No se muestra el número**, y esa es
 * la diferencia con el módulo de credibilidad, que sí lo muestra: acá no hay
 * ningún valor que mostrar —el módulo no corrió— y un cero dibujado en la
 * escala se leería como «el módulo midió cero», que es una afirmación sobre la
 * afirmación analizada que nadie hizo.
 */
function modulo(rotulo: string, valor: number, ausente = false): HTMLElement {
  const nodo = document.createElement('div');
  nodo.className = 'mod';

  const encabezado = document.createElement('div');
  encabezado.className = 'mod-t';
  const nombre = document.createElement('span');
  nombre.textContent = rotulo;
  const cifra = document.createElement('span');
  cifra.textContent = ausente ? 'sin dato' : comaDecimal(valor);
  encabezado.append(nombre, cifra);

  const barra = document.createElement('div');
  barra.className = 'barra';
  const relleno = document.createElement('i');
  relleno.style.width = ausente ? '100%' : `${Math.round(valor * 100)}%`;
  relleno.style.background = ausente ? TRAMA_SIN_DATO : colorDeBarra(valor);
  barra.append(relleno);

  nodo.append(encabezado, barra);
  return nodo;
}

/** Enumera nombres separados por comas y una conjunción final. */
function enumerar(nombres: string[]): string {
  if (nombres.length <= 1) {
    return nombres.join('');
  }
  return `${nombres.slice(0, -1).join(', ')} y ${nombres[nombres.length - 1]}`;
}

/**
 * El aviso del flujo alternativo *6a*: qué módulo faltó y qué significa.
 *
 * Nombra los módulos ausentes con las palabras que el servicio devuelve, que
 * son las que una persona puede leer, y cierra diciendo lo único que importa:
 * que el resultado no es concluyente. Es la mitad de RF-08 que exige señalar
 * explícitamente el análisis parcial.
 */
function avisoParcial(analisis: RespuestaAnalisis): HTMLElement {
  const nodo = document.createElement('div');
  nodo.className = 'nota-parcial';

  const figura = document.createElement('span');
  figura.setAttribute('aria-hidden', 'true');
  figura.textContent = '◐';

  const texto = document.createElement('span');
  const ausentes = enumerar(analisis.analisis_parcial.modulos_ausentes);
  texto.textContent = ausentes
    ? `No se pudo completar ${ausentes}. Se muestra únicamente lo que el ` +
      'sistema pudo verificar por su cuenta; el resultado no es concluyente.'
    : 'Un módulo del análisis no se pudo ejecutar. Se muestra únicamente lo ' +
      'que el sistema pudo verificar por su cuenta; el resultado no es ' +
      'concluyente.';

  nodo.append(figura, texto);
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
  // Sin cifra. Impresa en la misma columna, la misma tipografía y las mismas
  // cifras tabulares que los dos puntajes que sí miden algo, se leía como una
  // medición mas —y es un valor arbitrario derivado del *handle*—. Que sea
  // estable entre recargas se sigue comprobando en la costura del contrato,
  // que es donde corresponde, y no exhibiéndolo.
  cifra.textContent = 'sin dato';
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

  if (analisis.afirmacion.trim() === '' && falta(analisis, MODULO_AUSENTE.extraccion)) {
    // La afirmación viene vacía porque el paso que la extrae no se pudo
    // ejecutar, que es otra cosa que no haber encontrado ninguna. Decir «no se
    // identificó ninguna afirmación verificable» acá sería afirmar sobre la
    // publicación algo que el sistema nunca llegó a mirar.
    nodo.classList.add('vacia');
    rotulo.textContent = 'Afirmación no analizada';
    cuerpo.textContent =
      'El sistema no llegó a leer esta publicación: el análisis no se pudo ' +
      'ejecutar. No dice nada sobre lo que la publicación afirma.';
  } else if (analisis.afirmacion.trim() === '') {
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

  const esParcial = analisis.analisis_parcial.es_parcial;
  // El *handle* sobrevive solo acá, en la etiqueta accesible, y esa es la
  // diferencia que RNF-07 marca: identifica **de qué publicación** es este
  // análisis, en lugar de acompañar al puntaje como si fuera su sujeto. No lo
  // lee nadie que pueda confundirlo con una cifra sobre la cuenta.
  panel.setAttribute('role', 'region');
  panel.setAttribute('aria-label', `Análisis de la publicación de ${handle}`);

  const tapa = TAPA[analisis.veredicto];
  const nodoTapa = document.createElement('div');
  // Un análisis parcial toma la tapa gris cualquiera sea el veredicto que
  // traiga: el color de un nivel prometería una lectura del resultado que un
  // análisis incompleto no puede sostener.
  nodoTapa.className = `p-tapa ${esParcial ? 'parcial' : tapa.clase}`;

  const veredicto = document.createElement('div');
  veredicto.className = 'p-vered';
  const figura = document.createElement('span');
  figura.setAttribute('aria-hidden', 'true');
  figura.className = 'p-fig';
  figura.innerHTML = esParcial ? ICONOS.parcial : tapa.figura;
  veredicto.append(
    figura,
    document.createTextNode(esParcial ? 'Análisis parcial' : tapa.titulo),
  );

  const puntaje = document.createElement('div');
  puntaje.className = 'p-score';
  const subtitulo = document.createElement('div');
  subtitulo.className = 'p-sub';

  if (esParcial) {
    // El *mockup* lo dibuja así y RNF-11 lo exige: un porcentaje calculado con
    // un módulo caído se leería igual de confiable que el resto y no lo es. Se
    // muestra la ausencia, no un número que la disimule.
    puntaje.textContent = '—';
    subtitulo.textContent = 'No se pudo completar el análisis';
  } else if (analisis.veredicto === 'sin_contraste_externo') {
    // Sin contraste externo tampoco hay porcentaje: no habría sobre qué
    // calcularlo. Es la misma decisión que la columna derecha del *mockup* y la
    // que exige RF-08.
    puntaje.textContent = '—';
    subtitulo.textContent = 'Sin evidencia externa con la cual contrastar';
  } else {
    puntaje.textContent = `${Math.round(analisis.puntaje_final * 100)}%`;
    // El *handle* no acompaña al puntaje. Identificaba la publicación
    // analizada, pero compartiendo renglón con «Probabilidad estimada de
    // desinformación» y con la cifra grande se leía como un puntaje **sobre la
    // cuenta**, que es exactamente lo que RNF-07 prohíbe. El detalle ya cuelga
    // del tuit que analiza, así que la publicación no necesita nombrarse.
    subtitulo.textContent = 'Probabilidad estimada de desinformación de la afirmación';
  }

  // La region mas autoritativa del analisis —el titular del veredicto y la
  // cifra grande— era la unica sin atribucion. El compromiso es que la marca
  // este siempre visible, y aca es donde mas hace falta.
  nodoTapa.append(veredicto, puntaje, subtitulo, marcaDeAtribucion());

  const justificacion = document.createElement('p');
  justificacion.className = 'p-just';
  justificacion.textContent = analisis.justificacion;

  panel.append(nodoTapa);
  if (esParcial) {
    panel.append(avisoParcial(analisis));
  }

  panel.append(
    bloqueAfirmacion(analisis),
    justificacion,
    seccion('Qué aportó cada señal', [
      modulo(
        'Análisis del texto',
        analisis.puntajes.clasificador.valor,
        falta(analisis, MODULO_AUSENTE.extraccion),
      ),
      moduloCredibilidad(
        analisis.puntajes.credibilidad.valor,
        analisis.puntajes.credibilidad.no_implementado,
      ),
      modulo(
        'Contraste con fuentes',
        analisis.puntajes.contraste.valor,
        // Sin extracción tampoco hubo búsqueda: el contraste está igual de
        // ausente aunque el servicio no lo repita.
        falta(analisis, MODULO_AUSENTE.contraste) ||
          falta(analisis, MODULO_AUSENTE.extraccion),
      ),
    ]),
  );

  if (analisis.razones.length > 0) {
    panel.append(seccion('Por qué', [listaDeRazones(analisis)]));
  }

  agregarPieDeEvidencia(panel, analisis);

  return panel;
}
