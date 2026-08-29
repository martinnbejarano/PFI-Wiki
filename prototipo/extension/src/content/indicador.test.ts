/**
 * Pruebas de lo que el ciudadano ve cuando algo falla.
 *
 * La *spec* (issue #18) fija dos costuras y esta no es ninguna de las dos: el
 * resto de la extensión «es pintar y pasar mensajes» y no se prueba. Se hace
 * una excepción acotada porque un criterio de aceptación del ticket #25 es una
 * afirmación sobre la interfaz que no se puede comprobar de otra manera —«un
 * fallo del proveedor no deja el indicador en estado transitorio permanente»—,
 * y porque es lo único de la interfaz que, si se rompe, se rompe delante del
 * tribunal y sin vuelta atrás.
 *
 * El criterio sigue siendo el mismo del resto de la batería: se entra por donde
 * entra el *content script* —`crearIndicador` y los métodos de su superficie— y
 * se mira lo que queda dibujado. Ninguna prueba conoce los nombres de las
 * clases de estado ni cómo se arma el marcado por dentro; lo que se comprueba
 * es lo que una persona leería.
 */

import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { MODULO_AUSENTE, type RespuestaAnalisis } from '../compartido/contrato';
import { crearIndicador } from './indicador';
import { conTiempoLimite } from './tiempo-limite';

/** Un análisis completo del camino feliz, sobre el cual variar lo que interese. */
function analisisDeEjemplo(): RespuestaAnalisis {
  return {
    tweet_id: '1234567890123456789',
    afirmacion: 'El índice de precios de julio fue del 1,2 por ciento.',
    tipo_afirmacion: 'dato_economico',
    puntajes: {
      clasificador: { valor: 0.83, clase: 'falso' },
      credibilidad: { valor: 0.31, no_implementado: true },
      contraste: { valor: 0.9 },
    },
    puntaje_final: 0.87,
    veredicto: 'contradicho_por_fuentes_oficiales',
    justificacion: 'El dato oficial publicado por el organismo dice otra cosa.',
    razones: [
      {
        texto: 'El informe oficial publica otro valor.',
        fuente_url: 'https://www.indec.gob.ar/informe',
      },
    ],
    fuentes: [
      {
        titulo: 'Informe de precios',
        url: 'https://www.indec.gob.ar/informe',
        tipo: 'fuente_oficial',
        postura: 'contradice',
      },
    ],
    analisis_parcial: { es_parcial: false, modulos_ausentes: [] },
    version_modelo: 'proveedor:modelo',
    version_configuracion_pesos: 'pesos-v1+00000000',
  };
}

/** Todo el texto visible del indicador y de lo que haya desplegado debajo. */
function textoVisible(anfitrion: HTMLElement): string {
  return anfitrion.shadowRoot?.textContent ?? '';
}

/** El botón del indicador, que es por donde el ciudadano interactúa. */
function boton(anfitrion: HTMLElement): HTMLButtonElement {
  const nodo = anfitrion.shadowRoot?.querySelector('button');
  if (!nodo) {
    throw new Error('El indicador no tiene botón');
  }
  return nodo as HTMLButtonElement;
}

/**
 * Si el indicador está en el estado transitorio.
 *
 * Se lo reconoce por lo que una persona vería —la leyenda «Analizando»— y no
 * por una clase de CSS, para que la prueba no se rompa al retocar los estilos.
 */
function estaAnalizando(anfitrion: HTMLElement): boolean {
  return textoVisible(anfitrion).includes('Analizando');
}


describe('el indicador nunca queda en el estado transitorio', () => {
  it('una falla del análisis lo saca del estado transitorio y ofrece reintentar', () => {
    const indicador = crearIndicador('@ejemplo', () => {});
    indicador.mostrarAnalizando();
    expect(estaAnalizando(indicador.anfitrion)).toBe(true);

    indicador.mostrarError('No se pudo contactar al servicio local');

    expect(estaAnalizando(indicador.anfitrion)).toBe(false);
    expect(textoVisible(indicador.anfitrion)).toContain('No se pudo analizar');
    expect(textoVisible(indicador.anfitrion)).toContain('reintentar');
  });

  it('el botón vuelve a pedir el análisis después de una falla', () => {
    let pedidos = 0;
    const indicador = crearIndicador('@ejemplo', () => {
      pedidos += 1;
    });

    boton(indicador.anfitrion).click();
    indicador.mostrarAnalizando();
    indicador.mostrarError('El servicio tardó demasiado');
    boton(indicador.anfitrion).click();

    expect(pedidos).toBe(2);
  });

  it('un análisis parcial también lo saca del estado transitorio', () => {
    const indicador = crearIndicador('@ejemplo', () => {});
    const analisis = analisisDeEjemplo();
    analisis.analisis_parcial = {
      es_parcial: true,
      modulos_ausentes: [MODULO_AUSENTE.contraste],
    };

    indicador.mostrarAnalizando();
    indicador.mostrarVeredicto(analisis);

    expect(estaAnalizando(indicador.anfitrion)).toBe(false);
  });
});

describe('el seguro contra el estado transitorio permanente', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('falla cuando la petición nunca contesta', async () => {
    // El modo de falla que ninguna otra defensa cubre: el *service worker* se
    // apaga entre el pedido y la respuesta, y la promesa queda pendiente para
    // siempre.
    const jamas = new Promise<string>(() => {});

    const resultado = conTiempoLimite(jamas, 20_000);
    const fallo = expect(resultado).rejects.toThrow(/no respondió a tiempo/);
    await vi.advanceTimersByTimeAsync(20_000);

    await fallo;
  });

  it('deja pasar la respuesta que llega a tiempo', async () => {
    const aTiempo = Promise.resolve('un análisis');

    await expect(conTiempoLimite(aTiempo, 20_000)).resolves.toBe('un análisis');
  });
});

describe('el análisis parcial se señala explícitamente (RF-08)', () => {
  /** Deja el indicador con un análisis parcial ya mostrado. */
  function conAnalisisParcial(modulos: string[]): HTMLElement {
    const indicador = crearIndicador('@ejemplo', () => {});
    const analisis = analisisDeEjemplo();
    analisis.analisis_parcial = { es_parcial: true, modulos_ausentes: modulos };
    indicador.mostrarVeredicto(analisis);
    return indicador.anfitrion;
  }

  it('el indicador lo nombra, dice qué faltó y no muestra porcentaje', () => {
    const anfitrion = conAnalisisParcial([MODULO_AUSENTE.contraste]);

    const texto = textoVisible(anfitrion);
    expect(texto).toContain('Análisis parcial');
    expect(texto).toContain(MODULO_AUSENTE.contraste);
    expect(texto).toContain('no es concluyente');
    // El puntaje del ejemplo es 0,87: si apareciera como porcentaje, se leería
    // igual de confiable que el de un análisis completo (RNF-11).
    expect(texto).not.toContain('87%');
  });

  it('el detalle explica qué pasó y no inventa un porcentaje', () => {
    const anfitrion = conAnalisisParcial([MODULO_AUSENTE.contraste]);

    // El detalle se abre desde el propio indicador, como en la *timeline*.
    boton(anfitrion).click();

    const texto = textoVisible(anfitrion);
    expect(texto).toContain('Se muestra únicamente lo que el sistema pudo verificar');
    expect(texto).toContain(MODULO_AUSENTE.contraste);
    // El puntaje del ejemplo es 0,87: una cifra calculada con un módulo caído se
    // leería igual de confiable que la de un análisis completo (RNF-11).
    expect(texto).not.toContain('87%');
  });

  it('cuando el análisis no llegó a empezar, nombra los tres módulos ausentes', () => {
    const anfitrion = conAnalisisParcial([
      MODULO_AUSENTE.extraccion,
      MODULO_AUSENTE.contraste,
      MODULO_AUSENTE.redaccion,
    ]);

    boton(anfitrion).click();

    const texto = textoVisible(anfitrion);
    for (const modulo of [
      MODULO_AUSENTE.extraccion,
      MODULO_AUSENTE.contraste,
      MODULO_AUSENTE.redaccion,
    ]) {
      expect(texto).toContain(modulo);
    }
    expect(texto).not.toContain('87%');
  });

  it('un análisis completo no lleva ninguna marca de parcial', () => {
    const indicador = crearIndicador('@ejemplo', () => {});
    indicador.mostrarVeredicto(analisisDeEjemplo());
    boton(indicador.anfitrion).click();

    const texto = textoVisible(indicador.anfitrion);
    expect(texto).not.toContain('Análisis parcial');
    expect(texto).not.toContain('no es concluyente');
    expect(texto).toContain('87%');
  });
});

describe('los enlaces a las fuentes abren el documento (RNF-06)', () => {
  /**
   * El indicador frena la propagación para que tocar el análisis no navegue al
   * detalle del tuit, que es lo que X hace con un clic en cualquier parte del
   * artículo. Ese freno incluía `preventDefault`, y `preventDefault` cancela
   * **cualquier** acción por defecto: aplicado sin distinguir, ningún enlace del
   * análisis abría nada.
   *
   * La prueba mira lo único que importa desde afuera: que el clic en un enlace
   * conserve su acción por defecto, y que el que no nace en un enlace la pierda.
   */
  function clicEn(nodo: Element): boolean {
    const evento = new MouseEvent('click', {
      bubbles: true,
      cancelable: true,
      composed: true,
    });
    nodo.dispatchEvent(evento);
    return evento.defaultPrevented;
  }

  it('un clic en un enlace de una fuente conserva su acción por defecto', () => {
    const indicador = crearIndicador('@ejemplo', () => {});
    indicador.mostrarVeredicto(analisisDeEjemplo());
    document.body.append(indicador.anfitrion);
    boton(indicador.anfitrion).click();

    const enlace = indicador.anfitrion.shadowRoot?.querySelector('a[href]');
    expect(enlace).toBeTruthy();
    expect(clicEn(enlace!)).toBe(false);
  });

  it('un clic fuera de un enlace sigue frenando la navegación de X', () => {
    const indicador = crearIndicador('@ejemplo', () => {});
    indicador.mostrarVeredicto(analisisDeEjemplo());
    document.body.append(indicador.anfitrion);

    expect(clicEn(boton(indicador.anfitrion))).toBe(true);
  });
});
