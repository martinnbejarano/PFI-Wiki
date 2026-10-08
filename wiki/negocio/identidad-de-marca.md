---
titulo: Identidad de marca — Factum
tipo: análisis
tags: [negocio, branding, marca, logo, paleta, tipografia, tono-de-voz, extension, borrador]
fuentes: [encuesta-resultados.md, verificacion-nombre-trama.md, PRODUCT.md, DESIGN.md]
actualizado: 2026-10-08
---

# Identidad de marca — Factum

Identidad visual y verbal del producto (issue #50, spec padre #45). Sirve para la extensión, el deck, los videos y la subsección «Producto» del cap. 4. Es el borrador que se lleva a la clase de modelo de negocio del 03/10/2026, así que puede cambiar con la devolución de la cátedra.

![Logo de Factum](../assets/marca/factum-logo.svg)

**Factum. Cada afirmación, con su evidencia.**

## Nombre: Factum

*Factum* es latín: «hecho», «lo que fue hecho», participio de *facere* («hacer»). El nombre reemplaza a «Trama», que resultó tomado en el INPI (ver [[verificacion-nombre-trama]]).

El nombre funciona porque está del lado del hecho verificable. El producto lee una afirmación y la contrasta con lo que efectivamente consta en una fuente, y de eso se ocupa el sistema.

*Factum* tiene además una raíz culta y documental: es la palabra de los registros, las actas y los expedientes, y remite a un documento que se puede abrir y consultar. Eso es lo que promete el posicionamiento: el veredicto llega siempre con su evidencia enlazada (PRODUCT.md).

Es un nombre sobrio. No promete «la verdad» ni usa el vocabulario de *fake news* o de la persecución, así que no se lee como un árbitro que toma partido. Ese es el riesgo principal que marcó la encuesta: el 84,1 % pone la neutralidad política como primer atributo de confianza ([[encuesta-resultados]]). Por último, el nombre habla de lo que se afirmó y nunca de quién lo publicó, igual que el producto (principio 3 de PRODUCT.md).

Leído con los criterios de Keller para elegir elementos de marca (memorable, significativo, agradable, transferible, adaptable y protegible):

| Criterio | Cómo lo cumple Factum |
|---|---|
| Memorable | Seis letras y dos sílabas. Se lee igual en español y en inglés. |
| Significativo | Sugiere la función (el hecho) sin describirla literalmente. |
| Agradable | Tiene un registro culto sin ser críptico; suena institucional y no comercial. |
| Transferible | Sirve igual para la extensión gratuita y para los productos B2B (API, panel, reportes). |
| Adaptable | No depende de X ni de una tecnología: sobrevive a un cambio de plataforma o de modelo. |
| Protegible | Está pendiente de verificar en el INPI y en Chrome Web Store (ver [Pendientes](#pendientes)). |

## Logo

El concepto son dos mitades enfrentadas sobre un fiel: un círculo partido por un eje vertical. La mitad izquierda es la afirmación y la mitad derecha, la evidencia. El eje es el fiel de una balanza, la aguja que indica el equilibrio. Las dos mitades tienen el mismo tamaño y ninguna pesa más que la otra, para transmitir neutralidad, el atributo n.º 1 de confianza (84,1 %).

Se descartó el dibujo literal de una balanza de platillos: a 16 px se vuelve una mancha, y además es el ícono de los estudios jurídicos, que lleva a leer el producto como un tribunal que condena. El círculo partido es la abstracción de la misma idea y ya era la marca de atribución de la extensión (la mitad llena y la mitad vacía de `ICONOS.marca`, en `tema.ts`). El logo le agrega el fiel y mantiene la familia.

Principios de construcción:

- Geometría mínima: dos semicírculos y una barra, en una grilla de 64. No hay degradados, sombras ni detalles que se pierdan al achicarlo.
- Simetría izquierda-derecha, que muestra la neutralidad sin tener que explicarla.
- Dos tonos del mismo azul para las mitades, porque afirmación y evidencia son parte de la misma operación y ninguna es la «buena».
- La palabra «Factum» va en Source Serif 4 SemiBold, convertida a trazos, así que el SVG no depende de que la fuente esté instalada.

### Archivos

Fuente vectorial (SVG) en `wiki/assets/marca/`:

| Archivo | Uso |
|---|---|
| [factum-logo.svg](../assets/marca/factum-logo.svg) | Logo completo (símbolo + palabra), color, sobre fondo claro. |
| [factum-logo-mono.svg](../assets/marca/factum-logo-mono.svg) | Logo completo monocromo. La evidencia pasa a contorno para que las mitades se distingan sin color. Sirve para impresión, sellos y fondos de un solo color (se recolorea cambiando el `fill`). |
| [factum-simbolo.svg](../assets/marca/factum-simbolo.svg) | Símbolo solo, color. |
| [factum-simbolo-mono.svg](../assets/marca/factum-simbolo-mono.svg) | Símbolo solo, monocromo. |
| [factum-icono.svg](../assets/marca/factum-icono.svg) | Ícono de la extensión: símbolo en blanco sobre un cuadrado de azul tinta. Se lee igual en la barra clara y en la oscura de Chrome. Base de 48 y 128 px. |
| [factum-icono-16.svg](../assets/marca/factum-icono-16.svg) | Ícono ajustado a la grilla de 16 px: el fiel ocupa dos columnas enteras de píxeles para no desenfocarse. |

Exportaciones:

- PDF para LaTeX: `documento/images/factum-logo.pdf` y `documento/images/factum-logo-mono.pdf` (vectoriales, fondo transparente, 54,5 × 16 mm). Se incluyen con `\includegraphics{images/factum-logo}`.
- PNG de la extensión: [16](../assets/marca/factum-icono-16.png), [48](../assets/marca/factum-icono-48.png) y [128 px](../assets/marca/factum-icono-128.png). La copia que usa la extensión está en `prototipo/extension/public/icons/icono-{16,48,128}.png`.

Las exportaciones se generaron con Chrome sin interfaz (`--screenshot` para los PNG y `--print-to-pdf` para los PDF). Si se modifica un SVG, hay que volver a exportar.

### Usos

- Margen mínimo alrededor del logo: el ancho del fiel multiplicado por cuatro.
- Tamaño mínimo del logo completo: 24 px de alto en pantalla o 8 mm impreso. Por debajo de eso, usar solo el símbolo.
- Sobre fondo oscuro, usar el ícono (símbolo blanco sobre azul tinta) o el monocromo en blanco. El logo color no se pone sobre fondos oscuros, porque el azul tinta desaparece.
- No se rota, no se deforma, no se le cambia el tono a una sola mitad y no se usa en verde, ámbar ni rojo.

## Paleta

La paleta es azul tinta con neutros. El azul remite a la tinta y al papel impreso, con un registro documental e institucional y sin carga partidaria en Argentina. Se descartó el celeste de la bandera, que carga identidad nacional y se confunde con el azul de X, y también el rojo y el verde, que dentro del producto ya significan un juicio.

### Colores de marca

| Nombre | Hex | Rol |
|---|---|---|
| Azul tinta | `#1B2F52` | Color principal. Logo, palabra, títulos, fondo del ícono. Contraste 13,3:1 sobre blanco. |
| Azul evidencia | `#6F8FC0` | Mitad de la evidencia en el logo sobre fondo claro. Acentos gráficos del deck (no para texto: da 3,3:1 sobre blanco). |
| Azul evidencia claro | `#8FAEDB` | Mitad de la evidencia sobre fondo oscuro (ícono). Texto de acento sobre azul tinta (5,9:1). |
| Papel | `#F7F6F2` | Fondo de deck, videos y piezas impresas. Blanco cálido, como el del papel. |
| Grafito | `#2A2E35` | Texto de cuerpo sobre papel (12,6:1). |
| Pizarra | `#6B7280` | Texto secundario, epígrafes y fuentes de figuras (4,5:1 sobre papel, el mínimo AA). |
| Línea | `#D9DCE1` | Filetes y separadores. |
| Blanco | `#FFFFFF` | Símbolo sobre el ícono y fondo alternativo. |

### Colores de estado (no son de marca)

El verde, el ámbar y el rojo son los colores del veredicto y viven solo dentro de la interfaz de la extensión. Vienen de DESIGN.md y esta página no los cambia:

| Estado | Hex | Significado |
|---|---|---|
| Rojo de contradicción | `#f4212e` | *Contradicho por fuentes oficiales*; postura *contradice*. |
| Ámbar de sospecha | `#ffd400` | *Información sospechosa*. |
| Verde de corroboración | `#00ba7c` | *Parece verificado*; postura *corrobora*. |
| Azul de sistema (de X) | `#1d9bf0` | Trabajo en curso (análisis), foco y enlaces. Es el azul de X, no el de la marca. |

Si la marca fuera verde, el logo diría «verificado» en cada lugar donde aparece, y si fuera roja diría «falso». La marca firma el análisis y el color de estado dice el resultado: mezclarlos haría que la firma se leyera como un juicio. Por eso el logo nunca va en verde, ámbar ni rojo, y los colores de estado nunca se usan como decoración en el deck ni en los videos. Cuando una pieza de comunicación muestra un veredicto, lo muestra como captura de la interfaz.

## Tipografía

**Source Serif 4** para la palabra del logo y los títulos, y **Source Sans 3** para el texto de cuerpo del deck, los videos y las piezas de comunicación. Las dos son de Adobe, tienen licencia libre (SIL Open Font License), están en Google Fonts y cubren el español completo (tildes, eñe, comillas angulares).

La serif refuerza el registro documental de *Factum*: es la letra de los diarios, los boletines oficiales y los expedientes, las mismas fuentes contra las que el sistema contrasta. Source Serif 4 es sobria, con contraste moderado y sin rasgos caprichosos, y tiene un eje de tamaño óptico: la palabra del logo usa el corte de *display* (opsz 48, peso 600).

Para el cuerpo se usa una sans de la misma familia, que se lee mejor en pantalla y en proyección y comparte proporciones con la serif. Las dos son libres, así que el deck, los videos y una eventual web se pueden producir sin licencias, y cualquiera puede reproducirlos.

La interfaz de la extensión no usa estas fuentes: sigue con la pila tipográfica del sistema que usa X y no carga ninguna fuente web (regla «de la letra prestada» de DESIGN.md). La extensión es una invitada en casa ajena y su identidad se expresa por la marca y por el veredicto. El documento LaTeX mantiene la tipografía del template de UADE.

## Tono de voz

- Sobrio: frases cortas, sin exclamaciones, sin mayúsculas enfáticas y sin adjetivos de alarma. El sistema se limita a informar.
- En voseo: el rioplatense es el registro del usuario («tocá», «abrí», «leé»). El tuteo o el usted se leerían como una traducción.
- Sobre la afirmación: el sujeto de cada frase es la afirmación o la fuente, nunca la cuenta que publicó. El nivel más severo se atribuye a la fuente que lo sostiene.
- Con la incertidumbre a la vista: se habla de probabilidades y de fuentes, no de verdades. Cuando no hay evidencia, se dice.

| Sí | No |
|---|---|
| «Esta afirmación contradice lo publicado por el INDEC.» | «Este usuario miente.» |
| «Parece verificado: dos fuentes oficiales lo corroboran.» | «¡VERDADERO!» |
| «No hay fuentes para contrastar esta afirmación.» | «Probablemente falso.» (cuando no hay evidencia) |
| «Tocá el indicador para analizar la publicación.» | «Hacé click aquí para descubrir la verdad.» |
| «Abrí la fuente y leé el dato completo.» | «Confiá en nuestra IA.» |
| «Cada afirmación, con su evidencia.» | «Combatimos las *fake news*.» |

## *Tagline*

**«Cada afirmación, con su evidencia.»**

Resume el posicionamiento en una frase: el veredicto nunca viaja solo (principio 2 de PRODUCT.md). Nombra las dos mitades del logo, afirmación y evidencia, en el mismo orden en que se leen en el símbolo, de izquierda a derecha. Evita «verdad» y «falso», no promete nada que el sistema no haga y no apunta a nadie. «Cada» marca el alcance: cualquier afirmación, de cualquier signo político, recibe el mismo trato, y así la frase expresa la neutralidad.

## Aplicación a la extensión

- *Manifest*: `name` «Factum»; `description` con el *tagline* y sin «Prototipo del PFI»; `icons` y `action.default_icon` con 16, 48 y 128 px; `action.default_title` «Factum».
- *Popup*: título y encabezado «Factum».
- No se tocaron la lógica ni los colores de estado. El rótulo de atribución del indicador sigue diciendo *Análisis independiente*: es funcional (dice que el juicio no es de X) y no es el nombre del producto.

## Conceptos de *branding* usados

- **Identidad de marca** (Wheeler): el conjunto de nombre, símbolo, color, letra y voz que hace reconocible a la marca y que tiene que ser coherente en todos los puntos de contacto. Por eso el símbolo del logo continúa la marca de atribución que ya tenía la extensión.
- **Elementos de marca** (Keller): los seis criterios de la tabla del nombre.
- **Personalidad de marca** (Aaker): Factum es competente y sincera, no emocionante. De esa personalidad salen el tono sobrio, la serif documental y el azul tinta.
- **Posicionamiento:** la diferencia que un competidor no puede copiar de buena fe. El *tagline* la pone en palabras (ver PRODUCT.md, «Positioning»).

Estas referencias se citan en el documento con `\parencite{Wheeler2017}`, `\parencite{Keller2013}` y `\parencite{Aaker1996}` cuando se vuelque la subsección «Producto» al cap. 4.

## Pendientes

1. Verificar «Factum» en el INPI (clases 9 y 42) y en Chrome Web Store con el mismo procedimiento que [[verificacion-nombre-trama]]. [sin verificar]
2. Revisar dominio y *handle* en X.
3. ~~Volcar al cap. 4 como subsección «Producto» (Estilo, Logo, Misión, Visión), con el logo como figura.~~ Hecho el 2026-10-08 (#52), Sección 4.2.4.
4. Llevar el borrador a la clase del 03/10/2026 y ajustar con la devolución.

## Referencias cruzadas
- [[verificacion-nombre-trama]]
- [[modelo-de-negocio]]
- [[analisis-financiero]]
- [[encuesta-resultados]]
- [[user-research]]

## Fuentes
- [[encuesta-resultados]]: neutralidad política como primer atributo de confianza (84,1 %).
- PRODUCT.md y DESIGN.md (raíz del repo): posicionamiento, principios y colores de estado.
- Wheeler, A. (2017). *Designing Brand Identity*. 5.ª ed. Wiley.
- Keller, K. L. (2013). *Strategic Brand Management*. 4.ª ed. Pearson.
- Aaker, D. A. (1996). *Building Strong Brands*. Free Press.
- Source Serif 4 y Source Sans 3 en Google Fonts (OFL), consultado el 2026-09-28.
