import { defineConfig } from 'vitest/config';

/**
 * Configuración de las pruebas de la extensión.
 *
 * Va aparte de los dos archivos de construcción a propósito: `vite.config.ts` y
 * `vite.config.content.ts` describen artefactos que Chrome carga, y mezclarles
 * la configuración de pruebas obligaría a que cada `vite build` la arrastre.
 *
 * El entorno es un DOM simulado porque lo único de la extensión con riesgo
 * genuino es el lector del DOM de X: el resto es pintar y pasar mensajes, y no
 * se prueba. Ver la costura 2 de la *spec* (issue #18).
 */
export default defineConfig({
  test: {
    environment: 'jsdom',
    include: ['src/**/*.test.ts'],
  },
});
