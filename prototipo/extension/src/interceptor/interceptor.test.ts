import { expect, test } from 'vitest';
import { buscarCuentas } from './index';

test('encuentra al autor en una respuesta del timeline, en las dos formas de X', () => {
  const respuesta = {
    data: {
      entradas: [
        {
          tweet: {
            core: {
              user_results: {
                result: {
                  legacy: {
                    screen_name: 'data_economia_arg',
                    created_at: 'Wed Oct 10 20:19:24 +0000 2018',
                    followers_count: 1200,
                    friends_count: 300,
                  },
                },
              },
            },
          },
        },
        {
          // Forma más nueva: nombre y fecha mudados a `core`.
          result: {
            core: { screen_name: 'otra', created_at: 'Mon Jan 02 10:00:00 +0000 2023' },
            legacy: { followers_count: 5, friends_count: 900 },
          },
        },
        { legacy: { full_text: 'un tuit, no una cuenta' } },
      ],
    },
  };

  const cuentas = buscarCuentas(respuesta);

  expect(cuentas).toHaveLength(2);
  expect(cuentas).toContainEqual({
    handle: '@data_economia_arg',
    creada: '2018-10-10T20:19:24.000Z',
    seguidores: 1200,
    seguidos: 300,
  });
  expect(cuentas.find((c) => c.handle === '@otra')?.seguidos).toBe(900);
});
