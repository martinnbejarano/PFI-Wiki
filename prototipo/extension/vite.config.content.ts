import { defineConfig } from 'vite';

/**
 * Construcción del *content script*, en un paso aparte.
 *
 * Chrome ejecuta los guiones declarados en `content_scripts` como guiones
 * clásicos: un módulo con `import` fallaría al cargarse. Por eso este paso
 * emite un único archivo autocontenido en formato IIFE, mientras que el
 * *service worker* —que sí es un módulo— sale de la construcción principal.
 *
 * `emptyOutDir` queda en falso porque este paso corre segundo y no debe borrar
 * lo que dejó el anterior.
 *
 * Con `--mode interceptor` construye, con la misma forma, el guion que corre en
 * el mundo de la página (`src/interceptor/index.ts`).
 */
export default defineConfig(({ mode }) => {
  const nombre = mode === 'interceptor' ? 'interceptor' : 'content';
  return {
    build: {
      outDir: 'dist',
      emptyOutDir: false,
      copyPublicDir: false,
      target: 'es2022',
      minify: false,
      lib: {
        entry: `src/${nombre}/index.ts`,
        formats: ['iife'],
        name: nombre === 'content' ? 'pfiContent' : 'pfiInterceptor',
        fileName: () => `${nombre}.js`,
      },
    },
  };
});
