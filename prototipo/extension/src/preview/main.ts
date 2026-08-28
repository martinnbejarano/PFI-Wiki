/**
 * Banco de pruebas visual de la extensión.
 *
 * Monta los componentes **reales** —no una copia— sobre una reproducción del
 * *timeline* de X en modo oscuro, con un tuit por estado. Existe porque la
 * interfaz no se puede inspeccionar sobre x.com: la sesión del navegador está
 * bloqueada por el aviso de extensiones de privacidad, y sin una superficie
 * donde verla no hay forma de juzgar si la integración funciona.
 *
 * No se empaqueta en la extensión: vive fuera del manifiesto y se construye
 * aparte, con `npm run preview`.
 *
 * **Todo el contenido es ficticio.** Las cuentas, los tuits y las fuentes están
 * inventados sobre temas argentinos verosímiles, por la misma razón que lo
 * están los *mockups* del documento: el apartado ético del proyecto prohíbe
 * señalar cuentas identificables como fuente de desinformación.
 */

import type { RespuestaAnalisis } from '../compartido/contrato';
import { crearIndicador } from '../content/indicador';

/** Un tuit del banco: el contenido de la tarjeta y el estado que demuestra. */
interface Caso {
  nombre: string;
  handle: string;
  hora: string;
  texto: string;
  /** Qué se le pide al indicador una vez montado. */
  montar: (indicador: ReturnType<typeof crearIndicador>) => void;
  /** Despliega el detalle, y con él el panel de evidencia si se pide. */
  desplegar?: 'detalle' | 'evidencia';
}

/** Análisis de ejemplo, completo salvo por lo que cada caso sobrescribe. */
function analisis(parcial: Partial<RespuestaAnalisis> = {}): RespuestaAnalisis {
  return {
    tweet_id: '1900000000000000001',
    afirmacion: 'A partir del lunes cierran todas las escuelas de la Provincia',
    tipo_afirmacion: 'educacion',
    puntajes: {
      clasificador: { valor: 0.82, clase: 'sin_verificar' },
      credibilidad: { valor: 0.55, no_implementado: true },
      contraste: { valor: 0.89 },
    },
    puntaje_final: 0.84,
    veredicto: 'contradicho_por_fuentes_oficiales',
    justificacion:
      'La resolución publicada en el Boletín Oficial alcanza a un conjunto acotado de establecimientos y no a la totalidad del sistema educativo provincial. Tres medios de referencia reportan el mismo alcance limitado y ninguno respalda un cierre general.',
    razones: [
      {
        texto:
          'La resolución oficial enumera los establecimientos alcanzados por la suspensión y no comprende a la totalidad.',
        fuente_url: 'https://www.boletinoficial.gob.ar/',
      },
      {
        texto: 'Tres medios de referencia contradicen el alcance afirmado.',
        fuente_url: 'https://www.lanacion.com.ar/',
      },
      {
        texto:
          'El texto combina lenguaje de urgencia con una afirmación absoluta y no cita ninguna fuente.',
        fuente_url: null,
      },
    ],
    fuentes: [
      {
        titulo: 'Resolución que dispone la suspensión de actividades en establecimientos determinados',
        url: 'https://www.boletinoficial.gob.ar/',
        tipo: 'fuente_oficial',
        postura: 'contradice',
      },
      {
        titulo: 'El Ministerio aclaró que no habrá cierre total de escuelas',
        url: 'https://www.lanacion.com.ar/',
        tipo: 'medio_de_referencia',
        postura: 'contradice',
      },
      {
        titulo: 'Qué se sabe del cierre de escuelas que circula en redes',
        url: 'https://www.infobae.com/',
        tipo: 'medio_de_referencia',
        postura: 'corrobora',
      },
      {
        titulo: 'Preocupación de las familias por el estado edilicio escolar',
        url: 'https://www.pagina12.com.ar/',
        tipo: 'medio_de_referencia',
        postura: 'neutral',
      },
      {
        titulo: 'Es falso que se cierren todas las escuelas bonaerenses',
        url: 'https://chequeado.com/',
        tipo: 'verificacion_previa',
        postura: 'contradice',
      },
    ],
    analisis_parcial: { es_parcial: false, modulos_ausentes: [] },
    version_modelo: 'openai:gpt-5.6-luna',
    version_configuracion_pesos: 'pesos-v1+9e2fd1cb',
    ...parcial,
  };
}

const CASOS: Caso[] = [
  {
    nombre: 'Rosa Delgado',
    handle: '@rosadelgado_ok',
    hora: '2 h',
    texto:
      'Cada vez más familias preguntan qué pasa con el calendario escolar de la Provincia. Alguien tiene información oficial?',
    montar: (indicador) => indicador.mostrarInicial(),
  },
  {
    nombre: 'Noticias del Sur',
    handle: '@noticiasdelsur',
    hora: '18 min',
    texto:
      '🚨 A partir del lunes cierran TODAS las escuelas de la Provincia. Pasalo antes de que lo bajen 🚨',
    montar: (indicador) => indicador.mostrarAnalizando(),
  },
  {
    nombre: 'Alerta Federal',
    handle: '@alertafederal',
    hora: '41 min',
    texto:
      'CONFIRMADO: a partir del lunes cierran todas las escuelas de la Provincia. No lo están diciendo en ningún canal.',
    montar: (indicador) => indicador.mostrarVeredicto(analisis()),
  },
  {
    nombre: 'Data Económica',
    handle: '@dataeconomica',
    hora: '1 h',
    texto:
      'La inflación de julio habría cerrado bastante por encima de lo que anticipaban las consultoras privadas.',
    montar: (indicador) =>
      indicador.mostrarVeredicto(
        analisis({
          afirmacion: 'La inflación de julio superó las estimaciones privadas',
          tipo_afirmacion: 'dato_economico',
          veredicto: 'informacion_sospechosa',
          puntaje_final: 0.58,
          fuentes: [
            {
              titulo: 'Índice de precios al consumidor, informe técnico de julio',
              url: 'https://www.indec.gob.ar/',
              tipo: 'fuente_oficial',
              postura: 'neutral',
            },
            {
              titulo: 'La inflación de julio quedó en línea con las estimaciones privadas',
              url: 'https://www.infobae.com/',
              tipo: 'medio_de_referencia',
              postura: 'contradice',
            },
          ],
          puntajes: {
            clasificador: { valor: 0.61, clase: 'sin_verificar' },
            credibilidad: { valor: 0.48, no_implementado: true },
            contraste: { valor: 0.55 },
          },
        }),
      ),
  },
  {
    nombre: 'Salud al Día',
    handle: '@saludaldia',
    hora: '3 h',
    texto:
      'El Ministerio publicó el calendario de vacunación actualizado para la campaña de invierno.',
    montar: (indicador) =>
      indicador.mostrarVeredicto(
        analisis({
          afirmacion: 'El Ministerio publicó el calendario de vacunación de invierno',
          tipo_afirmacion: 'salud',
          veredicto: 'parece_verificado',
          puntaje_final: 0.16,
          fuentes: [
            {
              titulo: 'Calendario nacional de vacunación, campaña de invierno',
              url: 'https://www.argentina.gob.ar/',
              tipo: 'fuente_oficial',
              postura: 'corrobora',
            },
            {
              titulo: 'El Ministerio publicó el calendario de vacunación de invierno',
              url: 'https://www.telam.com.ar/',
              tipo: 'medio_de_referencia',
              postura: 'corrobora',
            },
          ],
          puntajes: {
            clasificador: { valor: 0.18, clase: 'verdadero' },
            credibilidad: { valor: 0.72, no_implementado: true },
            contraste: { valor: 0.12 },
          },
        }),
      ),
  },
  {
    nombre: 'Vecinos Organizados',
    handle: '@vecinosorg',
    hora: '5 h',
    texto:
      'Dicen que el municipio va a cambiar el recorrido de la línea que pasa por el barrio. Nadie confirma nada todavía.',
    montar: (indicador) =>
      indicador.mostrarVeredicto(
        analisis({
          afirmacion: 'El municipio cambiará el recorrido de una línea de colectivo',
          tipo_afirmacion: 'otro',
          veredicto: 'sin_contraste_externo',
          fuentes: [],
          razones: [
            {
              texto:
                'No se encontró ninguna fuente dentro de la jerarquía de evidencia que se pronuncie sobre la afirmación.',
              fuente_url: null,
            },
          ],
          justificacion:
            'Ninguna fuente oficial, medio de referencia ni verificación previa se pronuncia sobre esta afirmación. El sistema no emite un veredicto cuando no hay evidencia que lo respalde.',
        }),
      ),
  },
  {
    nombre: 'Panorama Diario',
    handle: '@panoramadiario',
    hora: '6 h',
    texto:
      'Fuentes del área confirman que la medida sobre el transporte se anuncia esta semana.',
    montar: (indicador) =>
      indicador.mostrarVeredicto(
        analisis({
          afirmacion: 'La medida sobre el transporte se anuncia esta semana',
          tipo_afirmacion: 'otro',
          veredicto: 'sin_contraste_externo',
          fuentes: [],
          analisis_parcial: {
            es_parcial: true,
            modulos_ausentes: ['el contraste con evidencia externa'],
          },
        }),
      ),
  },
  {
    nombre: 'Clara Bianchi',
    handle: '@clarabianchi',
    hora: '7 h',
    texto: 'Alguien más ve que los precios de la verdulería cambian dos veces por semana?',
    montar: (indicador) => indicador.mostrarError('No se pudo contactar al servicio local'),
  },
  {
    nombre: 'Alerta Federal',
    handle: '@alertafederal',
    hora: '41 min',
    texto:
      'CONFIRMADO: a partir del lunes cierran todas las escuelas de la Provincia. No lo están diciendo en ningún canal.',
    montar: (indicador) => indicador.mostrarVeredicto(analisis()),
    desplegar: 'detalle',
  },
  {
    nombre: 'Alerta Federal',
    handle: '@alertafederal',
    hora: '41 min',
    texto:
      'CONFIRMADO: a partir del lunes cierran todas las escuelas de la Provincia. No lo están diciendo en ningún canal.',
    montar: (indicador) => indicador.mostrarVeredicto(analisis()),
    desplegar: 'evidencia',
  },
];

/** Dibuja un tuit de X con el indicador adentro, en el hueco que le corresponde. */
function tuit(caso: Caso): HTMLElement {
  const articulo = document.createElement('article');
  articulo.className = 'tuit';

  const avatar = document.createElement('div');
  avatar.className = 'avatar';

  const cuerpo = document.createElement('div');
  cuerpo.className = 'cuerpo';

  const cabecera = document.createElement('div');
  cabecera.className = 'cabecera';
  cabecera.innerHTML =
    `<span class="nombre">${caso.nombre}</span>` +
    `<span class="meta">${caso.handle} · ${caso.hora}</span>`;

  const texto = document.createElement('div');
  texto.className = 'texto';
  texto.textContent = caso.texto;

  const indicador = crearIndicador(caso.handle, () => {});
  caso.montar(indicador);

  const acciones = document.createElement('div');
  acciones.className = 'acciones';
  for (const rotulo of ['12', '48', '213', '9,4 mil']) {
    const accion = document.createElement('span');
    accion.textContent = rotulo;
    acciones.append(accion);
  }

  if (caso.desplegar) {
    const raiz = indicador.anfitrion.shadowRoot;
    raiz?.querySelector<HTMLButtonElement>('.badge')?.click();
    if (caso.desplegar === 'evidencia') {
      raiz?.querySelector<HTMLButtonElement>('.p-pie .btn.pri')?.click();
    }
  }

  cuerpo.append(cabecera, texto, indicador.anfitrion, acciones);
  articulo.append(avatar, cuerpo);
  return articulo;
}

/*
 * `?desplegado=1` deja solo los casos con el detalle abierto, para poder
 * inspeccionarlos a escala legible en lugar de dentro de una captura larga.
 */
const soloDesplegados = new URLSearchParams(location.search).has('desplegado');
const timeline = document.querySelector('#timeline');
for (const caso of CASOS) {
  if (soloDesplegados && !caso.desplegar) {
    continue;
  }
  timeline?.append(tuit(caso));
}
