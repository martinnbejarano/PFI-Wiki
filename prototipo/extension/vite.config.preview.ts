import { defineConfig } from 'vite';

/**
 * Construcción del banco de pruebas visual.
 *
 * No forma parte de la extensión: no lo referencia el manifiesto y no se carga
 * en Chrome. Existe para poder inspeccionar los componentes reales sobre una
 * reproducción del *timeline* de X, que es la única superficie disponible
 * mientras x.com bloquea la sesión.
 *
 * Sale como IIFE y a `preview/`, para poder abrirlo por `file://` sin servidor.
 */
export default defineConfig({
  build: {
    outDir: 'preview',
    emptyOutDir: false,
    copyPublicDir: false,
    target: 'es2022',
    minify: false,
    lib: {
      entry: 'src/preview/main.ts',
      formats: ['iife'],
      name: 'pfiPreview',
      fileName: () => 'preview.js',
    },
  },
});
