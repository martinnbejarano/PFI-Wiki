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
 */
export default defineConfig({
  build: {
    outDir: 'dist',
    emptyOutDir: false,
    copyPublicDir: false,
    target: 'es2022',
    minify: false,
    lib: {
      entry: 'src/content/index.ts',
      formats: ['iife'],
      name: 'pfiContent',
      fileName: () => 'content.js',
    },
  },
});
