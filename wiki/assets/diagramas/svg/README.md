# Diagramas en SVG — kit de estilo

Los diagramas del documento se dibujan a mano en SVG con el mismo lenguaje visual que la
presentación (slide de respaldo «Arquitectura — componentes» en `presentacion/index.html`).
El `.svg` de esta carpeta es la fuente de verdad; el PNG de `documento/chapters/figures/`
se genera con `render.sh`. Los `.drawio` de la carpeta de arriba quedan como histórico.

```bash
wiki/assets/diagramas/svg/render.sh                    # todos los svg/*.svg (no los que empiezan con _)
wiki/assets/diagramas/svg/render.sh c4-componentes     # uno o varios por nombre
```

Usa Chrome *headless* (sin dependencias extra): la ventana mide exactamente el `viewBox`
y la captura sale a 2× (p. ej. 1640×916 → 3280×1832 px), sin márgenes que recortar.
Para empezar uno nuevo, copiar `_plantilla.svg`.

## Tamaño: por qué estos números

La figura se incluye a `\textwidth` (16 cm = 453 pt en A4 con los márgenes del template)
o, en `landscape`, a `0.95\linewidth` (≈ 652 pt). Se fija el ancho del `viewBox` para
que **1 px del SVG ≈ 0,39 pt impreso** en los dos casos:

| Orientación | Ancho del `viewBox` | Alto máximo | Inclusión en LaTeX |
|---|---|---|---|
| Vertical | **1160** | ~1500 | `width=\linewidth` |
| Apaisada (`landscape`) | **1640** | ~1000 | `width=0.95\linewidth` |

| Elemento | Tamaño | Impreso |
|---|---|---|
| Título de tarjeta (negrita) | 24 px | ≈ 9,4 pt |
| Descripción de tarjeta | 20 px | ≈ 7,8 pt |
| Nombre del contenedor (itálica) | 20 px | ≈ 7,8 pt |
| Etiqueta de flecha (**mínimo absoluto**) | 18 px | ≈ 7,0 pt |

Ningún texto por debajo de 18 px. Si no entra, se saca texto o se parte el diagrama;
no se achica la letra.

## Paleta (relleno / borde, por categoría)

| Categoría | Relleno | Borde | Qué representa |
|---|---|---|---|
| Actor / cliente | `#EFEAFB` | `#7B5BC4` | Personas, la extensión vista desde afuera, clientes de la API |
| Propio | `#EAF0FE` | `#2F63D8` | Componentes, contenedores y datos del sistema |
| Análisis | `#FDF3E3` | `#C08A2E` | Los cuatro módulos (M1–M4) |
| Fuente confiable | `#E9F5EE` | `#4E9B72` | Fuentes oficiales, medios ADEPA, verificadores |
| Servicio externo | `#F1F3F5` | `#98A2AE` | Inferencia, LLM, X, cualquier tercero |

Texto: título `#16181D`, descripción y etiquetas `#464F5C`. Flechas `#5A6472`.
Contenedor del sistema: sin relleno, borde `#2F63D8` punteado `10 8`, opacidad 0,5,
`rx=16`, nombre en itálica arriba a la derecha. Fondo blanco.

## Geometría

- Tarjeta: `rx=11`, borde 2 px, alto 88 (título en `y+37`, descripción en `y+68`), texto centrado.
- Ancho de tarjeta típico 340–360 px; separación mínima entre tarjetas 24 px en horizontal
  y 60 px en vertical (76 px si la arista lleva etiqueta).
- Padding del contenedor ≥ 28 px; 48 px entre el borde superior y la primera fila, para su nombre.
- Flechas: `polyline` de 2,2 px, de borde a borde de tarjeta, con el marcador de abajo.
  Discontinua (`stroke-dasharray="8 6"`) solo para lo asíncrono o fuera del pedido.

```svg
<defs><marker id="punta" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7"
  orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#5A6472"/></marker></defs>
```

Tipografía en el `<svg>` raíz: `font-family="'Avenir Next','Segoe UI',system-ui,Helvetica,Arial,sans-serif"`.

## Reglas de legibilidad

1. **Título + una línea.** Cada tarjeta lleva un título y como máximo una línea de
   descripción (≤ ~32 caracteres en 340 px, ≤ ~40 en tarjetas anchas). Sin estereotipos
   `[Componente]`.
2. **Sin notas dentro del diagrama.** Nada de notas amarillas ni párrafos: la explicación
   va en el texto del capítulo.
3. **Sin título dentro de la imagen.** El `\caption` de LaTeX es el título.
4. **Sin cruces de aristas.** Si dos se cruzan, se mueve una caja.
5. **Solo flechas ortogonales**, con el menor número de codos posible.
6. **Etiquetas de arista mínimas**: una o dos palabras (`HTTPS`, `SQL`, el nombre de un puntaje).
   No etiquetar lo obvio.
7. **≤ ~12 cajas** de contenido por diagrama. Si hay más, agrupar o partir en dos figuras.
   (`c4-componentes` llega a 15 contando los dos actores: es el techo, no la norma.)
8. **Alinear a una grilla** de columnas y filas; mucho aire.

Antes de commitear: correr `render.sh`, mirar el PNG y la página del PDF compilado a
tamaño real.
