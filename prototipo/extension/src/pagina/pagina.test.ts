import { expect, test } from 'vitest';
import { cuentasDelNodo } from './index';

test('junta al autor y al citado subiendo por el árbol de React', () => {
  // Forma tomada de x.com el 2026-10-08: el usuario cuelga varios niveles
  // arriba del artículo, dentro de las propiedades del tuit.
  const autor = {
    screen_name: 'Data_Economia_Arg',
    created_at: '2009-09-16T02:24:31.000Z',
    followers_count: 2796,
    friends_count: 1924,
  };
  const citado = {
    screen_name: 'otra',
    created_at: 'Wed Oct 10 20:19:24 +0000 2018',
    followers_count: 5,
  };
  const fibra = {
    memoizedProps: { className: 'css-1' },
    return: {
      memoizedProps: { tweet: { user: autor, quoted_status: { user: citado } } },
      return: null,
    },
  };

  expect(cuentasDelNodo(fibra)).toEqual({
    '@data_economia_arg': { creada: '2009-09-16T02:24:31.000Z', seguidores: 2796, seguidos: 1924 },
    '@otra': { creada: '2018-10-10T20:19:24.000Z', seguidores: 5, seguidos: 0 },
  });
});
