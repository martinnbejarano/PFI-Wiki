/**
 * El aviso de primer uso (Ley 25.326, art. 12): hasta que se acepta, el
 * *service worker* no le manda nada al servicio, y al instalar se abre el aviso.
 */

import { afterEach, beforeEach, expect, it, vi } from 'vitest';

import { VERSION_AVISO } from '../compartido/aviso';

type Escucha = (mensaje: unknown, emisor: unknown, responder: (r: unknown) => void) => boolean;

let escuchar: Escucha | undefined;
let alInstalar: (() => void) | undefined;
let guardado: Record<string, unknown>;
const pestanas = vi.fn();
const fetch = vi.fn(async () => new Response(JSON.stringify({ senales: [] })));

beforeEach(async () => {
  vi.resetModules();
  pestanas.mockClear();
  fetch.mockClear();
  guardado = {};
  vi.stubGlobal('chrome', {
    runtime: {
      onMessage: { addListener: (f: Escucha) => (escuchar = f) },
      onInstalled: { addListener: (f: () => void) => (alInstalar = f) },
      getURL: (ruta: string) => `chrome-extension://factum/${ruta}`,
    },
    storage: {
      local: {
        get: async (clave: string) => ({ [clave]: guardado[clave] }),
        set: async (valores: Record<string, unknown>) => void Object.assign(guardado, valores),
      },
    },
    tabs: { create: pestanas },
  });
  vi.stubGlobal('fetch', fetch);
  await import('./index');
});

afterEach(() => vi.unstubAllGlobals());

function enviar(mensaje: unknown): Promise<unknown> {
  return new Promise((responder) => escuchar!(mensaje, {}, responder));
}

it('sin el aviso aceptado no envía ningún análisis ni señal al servicio', async () => {
  const analisis = await enviar({ tipo: 'analizar', pedido: { tweet_id: '1', texto: 'x', handle: '@a' } });
  vi.useFakeTimers();
  const senal = enviar({ tipo: 'senal', publicacion: { tweet_id: '1', texto: 'x' } });
  await vi.runAllTimersAsync();
  vi.useRealTimers();

  expect(analisis).toMatchObject({ ok: false, error: expect.stringContaining('aviso') });
  expect(await senal).toEqual({ ok: true, datos: null });
  expect(fetch).not.toHaveBeenCalled();
});

it('con el aviso de la versión vigente aceptado, el análisis sale', async () => {
  guardado.avisoAceptado = VERSION_AVISO;
  fetch.mockResolvedValueOnce(new Response(JSON.stringify({ tweet_id: '1' })));

  const analisis = await enviar({ tipo: 'analizar', pedido: { tweet_id: '1', texto: 'x', handle: '@a' } });

  expect(analisis).toMatchObject({ ok: true });
  expect(fetch).toHaveBeenCalledTimes(1);
});

it('una aceptación de una versión anterior no alcanza', async () => {
  guardado.avisoAceptado = VERSION_AVISO - 1;

  await enviar({ tipo: 'analizar', pedido: { tweet_id: '1', texto: 'x', handle: '@a' } });

  expect(fetch).not.toHaveBeenCalled();
});

it('al instalar abre el aviso, y no lo reabre si ya fue aceptado', async () => {
  alInstalar!();
  await vi.waitFor(() => expect(pestanas).toHaveBeenCalledWith({ url: 'chrome-extension://factum/aviso.html' }));

  pestanas.mockClear();
  guardado.avisoAceptado = VERSION_AVISO;
  alInstalar!();
  await new Promise((r) => setTimeout(r, 0));
  expect(pestanas).not.toHaveBeenCalled();
});
