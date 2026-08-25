import { defineConfig } from 'vite';

/**
 * Construcción principal: el *service worker* y la ventana emergente.
 *
 * El *content script* se construye aparte, con `vite.config.content.ts`, porque
 * Chrome lo carga como guion clásico y no como módulo. Ver el README.
 *
 * Los nombres de salida no llevan huella (*hash*): el manifiesto los referencia
 * literalmente y se mantiene a mano, sin complemento de Vite para extensiones.
 */
export default defineConfig({
  base: './',
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    target: 'es2022',
    // El código de una extensión no se sirve por red: la minificación solo
    // dificulta revisar el artefacto que se carga sin empaquetar.
    minify: false,
    rollupOptions: {
      input: {
        'service-worker': 'src/service-worker/index.ts',
        popup: 'popup.html',
      },
      output: {
        format: 'es',
        entryFileNames: '[name].js',
        chunkFileNames: '[name].js',
        assetFileNames: '[name].[ext]',
      },
    },
  },
});
