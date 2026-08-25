/**
 * Pruebas del lector del DOM de X — costura 2 de la *spec*.
 *
 * Entra un nodo, sale el resultado: ninguna prueba conoce cómo el lector llega
 * a los datos, ni ejercita sus funciones auxiliares. El único punto de entrada
 * es `leerTuit`. Ese es el criterio que hace que estas pruebas sobrevivan a una
 * reescritura del lector y que se pongan en rojo solo cuando X cambie su
 * marcado, que es exactamente para lo que existen.
 *
 * Los fixtures viven en `__fixtures__/` y son el `outerHTML` de un único
 * `article[data-testid="tweet"]`. Los tres capturados de X real están
 * anonimizados; ver `__fixtures__/LEEME.md`.
 */

import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { describe, expect, it } from 'vitest';

import { leerTuit, type DatosTuit } from './lector-dom';

/**
 * Valores con los que se anonimizan los fixtures capturados de X real.
 *
 * Se fijan acá y no se descubren del archivo: quien coloque un fixture
 * reemplaza el *handle* y el identificador reales por estos, de modo que la
 * prueba pueda comprobar el valor exacto en lugar de conformarse con la forma.
 */
const ANONIMOS = {
  normal: { handle: '@cuenta_ejemplo', tweetId: '1900000000000000001' },
  cita: { handle: '@cuenta_citadora', tweetId: '1900000000000000002' },
  multimedia: { handle: '@cuenta_multimedia', tweetId: '1900000000000000004' },
} as const;

/** Convierte una cadena de HTML en el nodo del *timeline* que contiene. */
function nodoDeHtml(html: string): Element {
  const documento = new DOMParser().parseFromString(html, 'text/html');
  const articulo = documento.querySelector('article');
  if (!articulo) {
    throw new Error('El HTML no contiene ningún artículo');
  }
  return articulo;
}

/**
 * Directorio de los fixtures.
 *
 * Se arma con las utilidades de Node y no con `new URL`: el entorno de prueba
 * es un DOM simulado, y ahí `URL` es el del DOM, que `readFileSync` no resuelve
 * a una ruta del sistema de archivos.
 */
const DIRECTORIO_FIXTURES = join(dirname(fileURLToPath(import.meta.url)), '__fixtures__');

/** Lee un fixture del directorio `__fixtures__/` y devuelve su nodo. */
function nodoDeFixture(nombre: string): Element {
  const ruta = join(DIRECTORIO_FIXTURES, nombre);
  try {
    return nodoDeHtml(readFileSync(ruta, 'utf8'));
  } catch (error) {
    throw new Error(
      `No se pudo leer el fixture ${nombre}. Tiene que estar en ` +
        `src/content/__fixtures__/${nombre} y contener el outerHTML de un ` +
        `article[data-testid="tweet"]. Ver __fixtures__/LEEME.md. Causa: ${String(error)}`,
    );
  }
}

/** Estrecha el resultado a no nulo para poder afirmar sobre sus campos. */
function exigirDatos(datos: DatosTuit | null): DatosTuit {
  expect(datos).not.toBeNull();
  if (!datos) {
    throw new Error('El lector devolvió nada donde se esperaban datos');
  }
  return datos;
}

/** Afirma lo que vale para cualquier tuit legible, sea cual sea su contenido. */
function afirmarFormaDeLosDatos(datos: DatosTuit): void {
  expect(datos.texto.length).toBeGreaterThan(0);
  expect(datos.texto).toBe(datos.texto.trim());
  expect(typeof datos.verificada).toBe('boolean');

  for (const valor of Object.values(datos.metricas)) {
    if (valor !== null) {
      expect(Number.isInteger(valor)).toBe(true);
      expect(valor).toBeGreaterThanOrEqual(0);
    }
  }
}

/*
 * ---------------------------------------------------------------------------
 * Fixtures capturados de X real — PENDIENTES DE COLOCAR
 * ---------------------------------------------------------------------------
 *
 * Estas tres pruebas están apagadas porque los tres archivos que necesitan no
 * están en el repositorio. La captura por navegador automatizado no fue
 * posible: X responde con el aviso «Some privacy related extensions may cause
 * issues on x.com» y no llega a montar el *timeline*.
 *
 * Faltan, en `src/content/__fixtures__/`:
 *
 *   - `tuit-normal.html`      → un tuit solo de texto
 *   - `tuit-con-cita.html`    → un tuit que cita a otro
 *   - `tuit-con-multimedia.html` → un tuit con imagen o video
 *
 * Cada uno es el `outerHTML` de un único `article[data-testid="tweet"]`,
 * anonimizado con los valores de `ANONIMOS` y con la estructura del marcado
 * intacta. Al colocarlos se quita el `.skip` de este bloque.
 *
 * No se fabrican a mano: un fixture inventado presentado como captura de X
 * falsearía la evidencia del entregable, y además probaría el marcado que el
 * lector supone en lugar del que X emite, que es justo lo que hay que
 * verificar.
 */
describe.skip('un tuit capturado de X real', () => {
  it('devuelve los datos de un tuit normal', () => {
    const datos = exigirDatos(leerTuit(nodoDeFixture('tuit-normal.html')));

    expect(datos.tweetId).toBe(ANONIMOS.normal.tweetId);
    expect(datos.handle).toBe(ANONIMOS.normal.handle);
    afirmarFormaDeLosDatos(datos);

    // Un tuit del *timeline* muestra al menos un contador; si no se leyera
    // ninguno, el lector estaría mirando el lugar equivocado.
    const leidas = Object.values(datos.metricas).filter((valor) => valor !== null);
    expect(leidas.length).toBeGreaterThan(0);
  });

  it('devuelve los datos del tuit que cita, y no los del tuit citado', () => {
    const datos = exigirDatos(leerTuit(nodoDeFixture('tuit-con-cita.html')));

    expect(datos.tweetId).toBe(ANONIMOS.cita.tweetId);
    expect(datos.handle).toBe(ANONIMOS.cita.handle);
    afirmarFormaDeLosDatos(datos);

    // La publicación citada está dentro del mismo artículo: su texto y su
    // cuenta no deben filtrarse al análisis.
    expect(datos.texto).not.toContain('@cuenta_citada');
  });

  it('devuelve los datos de un tuit con multimedia', () => {
    const datos = exigirDatos(leerTuit(nodoDeFixture('tuit-con-multimedia.html')));

    expect(datos.tweetId).toBe(ANONIMOS.multimedia.tweetId);
    expect(datos.handle).toBe(ANONIMOS.multimedia.handle);
    afirmarFormaDeLosDatos(datos);
  });
});

describe('un nodo al que le faltan los campos opcionales', () => {
  it('se lee igual, con la verificación en falso y las métricas ausentes', () => {
    // Solo el texto y el identificador son obligatorios: la insignia de
    // verificación y los contadores no siempre están en el marcado, y su
    // ausencia no debe descartar el tuit entero.
    const nodo = nodoDeHtml(`
      <article data-testid="tweet">
        <div data-testid="tweetText"><span>Una afirmación cualquiera.</span></div>
        <a href="/cuenta_ejemplo/status/1900000000000000001"><time datetime="2026-08-24T12:00:00.000Z">24 ago</time></a>
      </article>
    `);

    expect(leerTuit(nodo)).toEqual({
      tweetId: '1900000000000000001',
      texto: 'Una afirmación cualquiera.',
      handle: '@cuenta_ejemplo',
      verificada: false,
      metricas: { respuestas: null, retuits: null, meGusta: null, vistas: null },
    });
  });
});

describe('un nodo sin la forma esperada', () => {
  it('se saltea en lugar de romper la extensión', () => {
    expect(leerTuit(nodoDeFixture('nodo-malformado.html'))).toBeNull();
  });

  it('se saltea cuando el artículo no tiene texto de publicación', () => {
    const nodo = nodoDeHtml(`
      <article data-testid="tweet">
        <a href="/cuenta_ejemplo/status/1900000000000000001"><time datetime="2026-08-24T12:00:00.000Z">24 ago</time></a>
      </article>
    `);
    expect(leerTuit(nodo)).toBeNull();
  });

  it('se saltea cuando el enlace permanente no tiene la forma esperada', () => {
    const nodo = nodoDeHtml(`
      <article data-testid="tweet">
        <div data-testid="tweetText"><span>Una afirmación cualquiera.</span></div>
        <a href="/i/status/no-es-un-numero"><time datetime="2026-08-24T12:00:00.000Z">24 ago</time></a>
      </article>
    `);
    expect(leerTuit(nodo)).toBeNull();
  });

  it('se saltea, sin lanzar, cuando lo que llega no es un nodo del DOM', () => {
    expect(leerTuit(undefined as unknown as Element)).toBeNull();
    expect(leerTuit({} as unknown as Element)).toBeNull();
  });
});
