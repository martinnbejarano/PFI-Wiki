/**
 * El agrupamiento del flujo automático (CU-01): una petición por lote de
 * publicaciones visibles y no una por publicación.
 *
 * Se entra por donde entra el *content script* —un mensaje `senal` por tuit— y
 * se mira lo que sale hacia el servicio.
 */

import { expect, it, vi } from 'vitest';

it('junta las señales de la ventana en una sola petición y reparte las respuestas', async () => {
  vi.useFakeTimers();
  let escuchar: ((mensaje: unknown, emisor: unknown, responder: (r: unknown) => void) => boolean) | undefined;
  vi.stubGlobal('chrome', {
    runtime: { onMessage: { addListener: (f: typeof escuchar) => (escuchar = f) }, onInstalled: { addListener: () => {} } },
    storage: { local: { get: async () => ({ avisoAceptado: 1 }) } },
  });
  const fetch = vi.fn(async (_url: string, init: RequestInit) => {
    const { publicaciones } = JSON.parse(init.body as string) as { publicaciones: { tweet_id: string }[] };
    // El servicio omite la que no pudo puntuar.
    const senales = publicaciones
      .filter((p) => p.tweet_id !== '3')
      .map((p) => ({ tweet_id: p.tweet_id, prioridad: p.tweet_id === '1' ? 'revisar' : 'neutral', version_modelo: 'v' }));
    return new Response(JSON.stringify({ senales }));
  });
  vi.stubGlobal('fetch', fetch);
  await import('./index');

  const respuestas = ['1', '2', '3'].map(
    (id) =>
      new Promise((responder) =>
        escuchar!({ tipo: 'senal', publicacion: { tweet_id: id, texto: `texto ${id}` } }, {}, responder),
      ),
  );
  await vi.runAllTimersAsync();

  expect(fetch).toHaveBeenCalledTimes(1);
  expect(fetch.mock.calls[0][0]).toMatch(/\/senales$/);
  expect(await Promise.all(respuestas)).toEqual([
    { ok: true, datos: { tweet_id: '1', prioridad: 'revisar', version_modelo: 'v' } },
    { ok: true, datos: { tweet_id: '2', prioridad: 'neutral', version_modelo: 'v' } },
    { ok: true, datos: null },
  ]);
  vi.useRealTimers();
});
