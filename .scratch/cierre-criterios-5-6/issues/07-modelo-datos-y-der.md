# 07 · `modelo-datos.md` y el DER dibujado

Type: task
Status: open
Blocked by: 06

## Question

Escribir `wiki/solucion/modelo-datos.md` y producir el diagrama entidad-relación a nivel lógico, con la definición que salga del ticket 06.

Trabajo:

1. La página, con una sección por dominio, la tabla de atributos y tipos por entidad, y un párrafo por decisión de diseño que no se lee sola en el dibujo.
2. El DER como `.drawio` en `wiki/assets/diagramas/`, coherente en paleta con los ocho existentes.
3. Validar con `python3 wiki/assets/diagramas/_tools/validar.py` —catorce entidades son muchas aristas y una huérfana se dibuja como una línea suelta sin que ningún parser la detecte—, revisar con `render.py` y exportar con `exportar.py` a `documento/chapters/figures/`.
4. La matriz de trazabilidad entidad → RF, que es lo que hace verificable la regla de corte.
5. Actualizar `index.md` y `log.md`, y quitar `modelo-datos` de la lista de pendientes de `plan-bloque-diseno.md`.

**Decisión abierta dentro del ticket.** Un DER de catorce entidades con atributos dibujado a mano en XML de draw.io es pesado y frágil. Hay que elegir entre generarlo con un guion de *layout* —como se hizo con cinco de los ocho diagramas, y que el README de `_tools/` marca como andamiaje de un solo uso— o dibujar solo las entidades y las relaciones en draw.io y dejar los atributos en las tablas de la página. La segunda opción se lee mejor impresa y es la que usan la mayoría de los PFI.

**Nota.** El README de `wiki/assets/diagramas/_tools/` advierte que el generador original no está versionado y que volver a correrlo pisaría los ajustes manuales. No reutilizarlo sobre los ocho existentes.
