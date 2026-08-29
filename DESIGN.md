---
name: Detector de desinformación en X
description: Interfaz inyectada en el timeline de x.com que emite un veredicto sobre una afirmación y muestra la evidencia que lo sostiene.
colors:
  velo: "rgba(255, 255, 255, 0.03)"
  velo-fuerte: "rgba(255, 255, 255, 0.07)"
  borde: "#2f3336"
  borde-vivo: "#3e4144"
  tinta: "#e7e9ea"
  tinta-media: "#a8aeb2"
  tinta-apagada: "#71767b"
  tinta-invertida: "#0f1419"
  tinta-hover: "#d7dbdc"
  azul: "#1d9bf0"
  rojo: "#f4212e"
  ambar: "#ffd400"
  verde: "#00ba7c"
  azul-velo: "rgba(29, 155, 240, 0.12)"
  azul-borde: "rgba(29, 155, 240, 0.4)"
  rojo-velo: "rgba(244, 33, 46, 0.12)"
  rojo-borde: "rgba(244, 33, 46, 0.4)"
  ambar-velo: "rgba(255, 212, 0, 0.1)"
  ambar-borde: "rgba(255, 212, 0, 0.35)"
  verde-velo: "rgba(0, 186, 124, 0.12)"
  verde-borde: "rgba(0, 186, 124, 0.4)"
typography:
  display:
    fontFamily: "-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif"
    fontSize: "27px"
    fontWeight: 700
    lineHeight: "32px"
    letterSpacing: "-0.02em"
    fontFeature: "tabular-nums"
  headline:
    fontFamily: "-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif"
    fontSize: "15px"
    fontWeight: 700
    lineHeight: "20px"
    letterSpacing: "-0.01em"
  body:
    fontFamily: "-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: "20px"
    letterSpacing: "0.01em"
  body-small:
    fontFamily: "-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: "18px"
  meta:
    fontFamily: "-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif"
    fontSize: "13px"
    fontWeight: 400
    lineHeight: "17px"
  label:
    fontFamily: "-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif"
    fontSize: "13px"
    fontWeight: 700
    lineHeight: "16px"
    letterSpacing: "0.02em"
    textTransform: "uppercase"
  action:
    fontFamily: "-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif"
    fontSize: "14px"
    fontWeight: 700
    lineHeight: "16px"
  pill:
    fontFamily: "-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif"
    fontSize: "12px"
    fontWeight: 700
    lineHeight: "17px"
rounded:
  radio: "16px"
  radio-chico: "8px"
  pastilla: "9999px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "12px"
  lg: "14px"
  xl: "16px"
components:
  indicador:
    backgroundColor: "transparent"
    textColor: "{colors.tinta}"
    typography: "{typography.body}"
    rounded: "{rounded.radio}"
    padding: "11px 14px 10px"
    width: "100%"
  indicador-hover:
    backgroundColor: "{colors.velo}"
  indicador-activo:
    backgroundColor: "{colors.velo-fuerte}"
  indicador-analizando:
    backgroundColor: "{colors.azul-velo}"
    textColor: "{colors.azul}"
  indicador-contradicho:
    backgroundColor: "{colors.rojo-velo}"
    textColor: "{colors.rojo}"
  indicador-sospechoso:
    backgroundColor: "{colors.ambar-velo}"
    textColor: "{colors.ambar}"
  indicador-verificado:
    backgroundColor: "{colors.verde-velo}"
    textColor: "{colors.verde}"
  indicador-sin-evidencia:
    backgroundColor: "transparent"
    iconColor: "{colors.tinta-apagada}"
    textColor: "{colors.tinta}"
  indicador-abierto:
    rounded: "16px 16px 0 0"
    borderBottomColor: "transparent"
    note: "el detalle hereda el borde de estado de la ficha"
  detalle:
    backgroundColor: "transparent"
    textColor: "{colors.tinta}"
    typography: "{typography.body}"
    rounded: "0 0 16px 16px"
  detalle-tapa:
    padding: "13px 14px"
    typography: "{typography.display}"
  detalle-seccion:
    padding: "14px"
  bloque-afirmacion:
    backgroundColor: "{colors.velo}"
    textColor: "{colors.tinta}"
    rounded: "{rounded.radio-chico}"
    padding: "12px 14px"
  nota-ausencia:
    backgroundColor: "transparent"
    textColor: "{colors.tinta-media}"
    typography: "{typography.meta}"
    rounded: "{rounded.radio-chico}"
    padding: "10px 14px"
  boton-primario:
    backgroundColor: "{colors.tinta}"
    textColor: "{colors.tinta-invertida}"
    typography: "{typography.action}"
    rounded: "{rounded.pastilla}"
    padding: "8px 16px"
  boton-primario-hover:
    backgroundColor: "{colors.tinta-hover}"
  pastilla-contradice:
    backgroundColor: "transparent"
    textColor: "{colors.rojo}"
    typography: "{typography.pill}"
    rounded: "{rounded.pastilla}"
    padding: "1px 9px"
  pastilla-corrobora:
    backgroundColor: "transparent"
    textColor: "{colors.verde}"
    typography: "{typography.pill}"
    rounded: "{rounded.pastilla}"
    padding: "1px 9px"
  pastilla-neutral:
    backgroundColor: "transparent"
    textColor: "{colors.tinta-media}"
    typography: "{typography.pill}"
    rounded: "{rounded.pastilla}"
    padding: "1px 9px"
  fila-fuente:
    backgroundColor: "transparent"
    textColor: "{colors.tinta}"
    rounded: "{rounded.radio-chico}"
    padding: "10px 0"
  fila-fuente-hover:
    backgroundColor: "{colors.velo}"
  atribucion:
    backgroundColor: "transparent"
    textColor: "{colors.tinta-media}"
    typography: "{typography.meta}"
  barra-puntaje:
    backgroundColor: "rgba(231, 233, 234, 0.1)"
    rounded: "{rounded.pastilla}"
    height: "4px"
---

# Design System: Detector de desinformación en X

## Overview

**Creative North Star: "La invitada que firma"**

La interfaz no tiene lienzo propio. Vive dentro de una raíz de sombra inyectada en la columna del *timeline* de x.com, entre el texto de una publicación y su barra de acciones, y todo lo que dibuja convive con la interfaz de X sin poder ocultarla ni reemplazarla. La consecuencia es que el sistema toma prestada la materia de la casa —el borde de un píxel, el radio de 16, la pila tipográfica, los cuatro acentos— y se reserva para sí una sola cosa: el juicio. Esa tensión, integrarse sin suplantar, es lo que organiza cada decisión que sigue.

El modo oscuro es exclusivo y no hay conmutador. X publica ese modo en dos variantes —*Lights out* sobre negro y *Dim* sobre un azul carbón— y la extensión no sabe en cuál está corriendo, así que **no pinta ningún fondo**: se apoya en velos blancos translúcidos que dejan pasar lo que haya debajo. Un fondo opaco incrustado se recortaría como un parche sobre la segunda variante, que es el aspecto de artefacto externo que la pieza existe para evitar.

La densidad es la de X: tipografía de 15 sobre interlineado de 20, filas separadas por una línea de un píxel, superficies con 14 y 16 de acolchado, y ninguna sombra en ninguna parte. Lo único que se aparta del sustrato es la firma. La marca de atribución, con su círculo partido, aparece **una vez por región visible** —en el pie del indicador, y otra vez en la tapa del panel de evidencia, que queda a mil píxeles de distancia— para que nadie pueda concluir que el veredicto lo emite la plataforma. Nunca dos veces dentro de la misma banda: repetida a noventa píxeles se lee como el componente renderizado por duplicado y no como firma.

**Key Characteristics:**
- Fondo heredado por velos translúcidos, nunca pintado.
- Modo oscuro exclusivo, sin variante clara y sin conmutador.
- Color reservado al veredicto que se apoya en evidencia; la ausencia va en gris.
- Una sola familia de íconos, construida sobre un círculo, con la ausencia dibujada como trazo faltante.
- Marca de atribución presente en toda región visible que emita un juicio, y una sola vez en cada una.
- Sin sombras: la profundidad la dan el borde de un píxel y el velo.

## Colors

La paleta no se elige: se hereda. Los cuatro acentos, el gris de las marcas de tiempo y el color de la tinta son los de la interfaz de X, y el único valor que el sistema introduce por su cuenta es un escalón intermedio de tinta que existe por una razón de contraste.

### Primary
- **Azul de sistema** (`{colors.azul}`): el azul de X. Marca el trabajo en curso —el indicador mientras analiza, con su velo y su borde— y las superficies del navegador que igual pertenecen al diseño: el anillo de foco, la selección de texto, el enlace a una fuente dentro de la lista de razones. Nunca expresa un juicio sobre el contenido.

### Secondary
Los tres colores del veredicto. Aparecen en el ícono, en el borde y en el velo del indicador, en la cifra grande del detalle y en la pastilla de postura de cada fuente. Cada uno tiene su par en velo (fondo, al 10–12 %) y en borde (al 35–40 %).

- **Rojo de contradicción** (`{colors.rojo}`): veredicto *contradicho por fuentes oficiales*, y postura *contradice* de una fuente.
- **Ámbar de sospecha** (`{colors.ambar}`): veredicto *información sospechosa*. Su velo va al 10 % y su borde al 35 %, más bajos que los de sus pares, porque el ámbar puro pesa más sobre negro.
- **Verde de corroboración** (`{colors.verde}`): veredicto *parece verificado*, y postura *corrobora*.

### Neutral
- **Tinta** (`{colors.tinta}`): el texto de X. Titulares de veredicto, afirmación extraída, justificación, título de cada fuente. Es también el fondo del botón primario, invertido sobre `{colors.tinta-invertida}`.
- **Tinta media** (`{colors.tinta-media}`): el escalón que el sistema agrega. El gris de X da 4,6:1 sobre el negro de *Lights out* pero 3,6:1 sobre el carbón de *Dim*, por debajo del mínimo. Todo lo que hay que poder leer y no es titular —la segunda línea del indicador, el sustantivo que acompaña a la cifra, el dominio de cada fuente— usa esta tinta.
- **Tinta apagada** (`{colors.tinta-apagada}`): el gris de X. **Es para dibujo, no para palabras.** Queda reservado al aro de un ícono en reposo y a las superficies sin texto. Sobre el velo ámbar en *Dim* da 2,9:1, muy por debajo del mínimo, así que ninguna línea que haya que leer lo usa —ni siquiera la atribución, que el encargo exige siempre visible.
- **Borde** (`{colors.borde}`): la línea de un píxel con la que X separa todo. Contorno de las tres superficies, separador entre secciones y entre filas de fuentes.
- **Borde vivo** (`{colors.borde-vivo}`): un escalón más claro, para el contorno del estado de falla y el del botón secundario.
- **Velo** y **velo fuerte** (`{colors.velo}`, `{colors.velo-fuerte}`): blanco al 3 % y al 7 %. Fondo del bloque de la afirmación, realce al pasar por encima del indicador y de cada fila de fuente, y estado presionado del indicador.

### Named Rules

**La regla del fondo heredado.** Ninguna superficie pinta un fondo opaco. Todo relleno es un velo translúcido, blanco o del acento correspondiente, de modo que la variante oscura de X que haya debajo se vea a través. Prueba: si un valor de fondo se lee como hexadecimal de seis dígitos, está mal.

**La regla del color reservado.** El color solo aparece cuando hay un veredicto sostenido por evidencia. La ausencia —*sin contraste externo*, *análisis parcial*— se dibuja en gris con el borde neutro y sin velo de estado. El trabajo en curso toma el azul de sistema, que no es un juicio. La falla toma el borde vivo y ningún color de veredicto: no haber podido pronunciarse es otra cosa que pronunciarse en contra.

**La regla de los tres escalones.** Hay exactamente tres niveles de tinta y el del medio no es decorativo. Texto que el ciudadano necesita leer para decidir: tinta o tinta media. Texto que solo acompaña: tinta apagada. Nunca poner en el gris de X una línea que haya que leer para entender el veredicto.

## Typography

**Familia única:** la pila de respaldo de X (`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`).

**Character:** no hay elección tipográfica propia. X compone su interfaz sobre una tipografía que no se puede redistribuir, y esta es exactamente la pila que X usa cuando la suya no carga; adoptarla hace que la métrica coincida en lugar de aproximarse. El sistema no carga ninguna fuente ni declara ninguna familia adicional.

### Hierarchy
- **Display** (700, 27px/32px, `-0.02em`, cifras tabulares): la única cifra grande del sistema, el porcentaje en la tapa del detalle. Toma el color del veredicto. Cuando no hay porcentaje que mostrar, ocupa su lugar un guión largo en el mismo tamaño.
- **Headline** (700, 15px/20px, `-0.01em`): el titular del veredicto en el indicador y el título del panel de evidencia. Es el mismo peso y tamaño con que X dibuja el nombre de una cuenta.
- **Body** (400, 15px/20px, `+0.01em`): la afirmación extraída, la justificación en lenguaje natural, el título de cada fuente. El interlineado sube a 21px en los bloques de prosa larga.
- **Body-small** (400, 14px/18px): el sustantivo que acompaña a la cifra, el rótulo y el valor de cada puntaje parcial, las razones (a 20px de interlineado) y el cuerpo de una fila de fuente.
- **Meta** (400, 13px/16–18px): la segunda línea del indicador, la atribución, la leyenda de despliegue, las notas al pie y la nota del módulo no implementado. Todas en tinta media, nunca en el gris de X.
- **Label** (700, 13px/16px, `+0.02em`, versalitas altas): los rótulos de sección del detalle y los encabezados de cada escalón de la jerarquía en el panel de evidencia. Es el único uso de mayúsculas del sistema.
- **Action** (700, 14px/16px): el texto del botón.
- **Pill** (700, 12px/17px): la pastilla de postura de una fuente.

### Named Rules

**La regla de la letra prestada.** La pila tipográfica no es una decisión de identidad, es la de X. No se agrega ninguna familia, no se carga ninguna fuente web y no se declara ninguna variante *display*. La identidad propia se expresa por la marca de atribución y por el veredicto, nunca por la letra.

**La regla de las tres líneas.** La segunda línea del indicador se recorta a tres renglones con puntos suspensivos, como X recorta la descripción de una tarjeta adjunta. Es la línea que permite decidir sin abrir nada, así que va en tinta media y nunca en el gris accesorio. Tres y no dos porque el peor caso —el veredicto contradicho, que es el que más fuentes nombra— pedía un renglón más, y lo que quedaba cortado era la cuenta de las fuentes que no entraron.

**La regla del número con su sustantivo.** Un porcentaje nunca viaja pegado al titular del veredicto. Va en el renglón de abajo, acompañado de lo que mide (*probabilidad estimada de que la afirmación sea verdadera*). Un indicador que hay que aprender a leer no cumple su función.

**La regla de la cifra al derecho.** El servicio estima una probabilidad de desinformación, donde más alto es peor; la interfaz muestra su complemento. Enunciado como desinformación, el número y el color de la tarjeta apuntaban en direcciones opuestas: un 30 % en verde, un 84 % en rojo, de modo que el veredicto favorable se anunciaba con la cifra más chica. Al derecho, grande y verde es buena noticia y chica y roja la contraria, y no hay nada que aprender. La inversión ocurre en un solo módulo porque la usan las dos superficies de la misma tarjeta.

## Layout

La interfaz ocupa una fila de ancho completo dentro de la columna de la publicación, entre el texto y la barra de acciones, con 12px de aire arriba y 4px abajo. No hay ancho propio: el ancho lo fija la columna del *timeline*. La raíz de sombra se abre con `all: initial` sobre el anfitrión, de modo que ninguna regla de X entra y ninguna regla propia sale.

El indicador es una grilla de tres columnas —20px para el ícono, el resto para el texto, y una columna automática para la leyenda de despliegue— con 12px de separación horizontal y 3px vertical. La atribución vive en una segunda fila que abarca de la segunda columna al final. La tapa del detalle es una grilla de dos columnas: a la izquierda el sustantivo y la atribución, a la derecha la cifra, centrada verticalmente sobre las tres filas.

El ritmo de acolchado es corto y regular. **El riel izquierdo es único**: 14px de acolchado horizontal en todo el interior de la tarjeta —ficha, tapa, secciones, pie y panel de evidencia—, porque ficha y detalle son una sola superficie y dos rieles a dos píxeles uno del otro delatan la costura. 12px para separar bloques hermanos, 8px para los pares ícono-texto y 4–6px para lo fino. El único acolchado de 16px que queda es el horizontal del botón, que es una pastilla y no una superficie. Las secciones del detalle se apilan separadas por una línea de un píxel, sin margen entre ellas.

No hay puntos de corte. La única consulta de medios del sistema es `prefers-reduced-motion`. La superficie soportada es Chrome de escritorio, así que el diseño responde al ancho de la columna de X y no a un catálogo de anchos de pantalla.

## Elevation & Depth

**Este sistema no usa sombras.** No hay una sola declaración de `box-shadow`, `filter` ni `backdrop-filter` en toda la interfaz. La profundidad se construye con dos materiales y nada más: la línea de un píxel en `{colors.borde}`, que delimita y separa, y el velo blanco translúcido, que realza sin despegar.

La jerarquía es tonal, no espacial. Un elemento se adelanta subiendo su velo (3 % al pasar por encima, 7 % al presionar) o encendiendo el velo de su acento, nunca levantándose del plano. El bloque de la afirmación se distingue de la prosa que lo rodea por un velo al 3 % más un borde, no por una sombra.

El único realce que se dibuja fuera del plano es el anillo de foco: `outline: 2px solid` en el azul de sistema, con 2px de separación, en el indicador, el botón y cada enlace a una fuente.

### Named Rules

**La regla del plano único.** Todo vive en el mismo plano que el *timeline*. Si una pieza necesita destacarse, sube su velo o enciende su borde; no se levanta. Una sombra sobre el *timeline* de X delata inmediatamente que la pieza no es de la casa.

**La regla de la ficha que crece.** El detalle no es una segunda tarjeta: es la misma que crece. Cuando se despliega, el indicador cierra sus esquinas inferiores y suelta su filete de abajo, y el panel abre con esquinas superiores rectas y sin borde superior. X nunca apila dos tarjetas bordeadas bajo una publicación.

## Shapes

El sistema tiene tres radios y una geometría de firma. Las superficies exteriores llevan 16px (`{rounded.radio}`), el mismo radio con que X adjunta contenido bajo una publicación. Los bloques interiores —la afirmación extraída, la nota de ausencia, la fila de una fuente— llevan 8px (`{rounded.radio-chico}`). Todo lo que es acción o etiqueta va en pastilla completa: el botón, la pastilla de postura, la etiqueta de razón sin fuente y la barra de puntaje.

Los bordes son siempre de un píxel y siempre rectos; no hay biseles, degradados de borde ni contornos dobles. La barra de puntaje es un riel de 4px de alto en pastilla, con el relleno heredando el radio.

La geometría de firma es el círculo. **Los íconos son una sola familia**, todos dibujados en una caja de 20 sobre un círculo de radio 7,5 con trazo de 2 y extremos redondeados, heredando el color por `currentColor`. Lo que cambia entre estados es lo que pasa dentro del círculo —una barra horizontal, una exclamación, una comprobación, una barra oblicua— o el círculo mismo cuando lo que falta es la evidencia. La marca es ese mismo círculo con una mitad rellena y la otra vacía.

### Named Rules

**La regla del círculo.** Todo ícono del sistema se construye sobre la misma circunferencia de radio 7,5 con trazo 2. Un ícono nuevo cambia el interior del círculo, nunca la silueta. No se admiten glifos tipográficos ni íconos importados de otra biblioteca.

**La regla del trazo faltante.** La ausencia de evidencia se dibuja como ausencia de trazo. *Sin contraste externo* es el mismo círculo, discontinuo; *análisis parcial* es media circunferencia firme y media discontinua. La forma dice lo que dice el color, para quien no distingue el color.

## Components

### Indicador (componente de firma)

La puerta de entrada y la única pieza que el ciudadano ve sin pedir nada. Es un botón de ancho completo con la forma de una tarjeta adjunta.

- **Forma:** esquinas de 16px, borde de un píxel, fondo transparente, acolchado `11px 14px 10px`.
- **Contenido:** ícono de 20 a la izquierda, titular del veredicto en *headline*, segunda línea en *meta* sobre tinta media recortada a dos renglones, leyenda de despliegue con galón a la derecha, y la marca de atribución en la fila de abajo.
- **Estados:** *inicial* (ícono de marca, gris, sin velo) · *analizando* (velo y borde azules, anillo giratorio de 16px en lugar de ícono) · *contradicho / sospechoso / verificado* (velo y borde del acento) · *sin contraste externo* y *análisis parcial* (gris, borde neutro, sin velo) · *falla* (borde vivo, gris).
- **Interacción:** al pasar por encima toma el velo, al presionar el velo fuerte, al enfocar el anillo azul. Con el detalle abierto, `aria-expanded="true"` rota el galón 180°, recorta las esquinas inferiores y transparenta el filete de abajo.
- **Comportamiento distintivo:** el mismo botón hace dos cosas según el estado. Sin análisis resuelto lo pide; con un análisis resuelto despliega y repliega el detalle. La leyenda de despliegue se oculta sola mientras no haya nada que abrir, en lugar de prometer una acción inexistente.

### Marca de atribución (componente de firma)

Un círculo partido de 15px y un rótulo funcional (*Análisis independiente*) en tinta apagada a 13px, con 6px de separación y sin corte de línea.

- **Dónde:** en el indicador, en el renglón que X reserva al dominio de origen de una tarjeta adjunta; en la tapa del detalle, junto a la cifra; y en la tapa del panel de evidencia.
- **Por qué ahí:** ese renglón es el hueco nativo de la procedencia. Es el lugar correcto para decir que el juicio no es de X.

### Detalle del veredicto

La continuación del indicador. Borde de un píxel sin filete superior, esquinas inferiores de 16px, sin fondo propio, con una entrada de 0,28s que sube 4px.

- **Tapa:** acolchado `13px 14px`, separada por una línea. Lleva la cifra en *display* con el color del veredicto, el sustantivo que la explica en tinta media y la atribución. No repite el titular del veredicto, que la ficha ya dice doce píxeles más arriba.
- **Secciones:** acolchado `14px`, separadas por una línea, con rótulo en *label*.
- **Bloque de la afirmación:** velo al 3 %, borde, esquinas de 8px, la afirmación entre comillas angulares y su tipo en un rótulo apagado arriba.
- **Desglose de puntajes:** rótulo y valor con coma decimal en cifras tabulares, y un riel de 4px en pastilla sobre blanco al 10 %. El relleno va rojo desde 0,80, ámbar desde 0,40 y verde por debajo; esos cortes son presentacionales y no son los umbrales que deciden el veredicto.
- **Razones:** lista sin viñeta nativa, con un punto de 4px en tinta apagada dibujado a la izquierda. La razón que se apoya en un documento lleva el enlace en azul con su flecha de salida; la que no, una pastilla apagada que dice *análisis propio del sistema*.

### Botón

- **Primario:** fondo en tinta plena, texto en `{colors.tinta-invertida}`, pastilla completa, acolchado `8px 16px`, texto en *action*. Al pasar por encima aclara a `{colors.tinta-hover}`. Es el único botón que el detalle instancia, y solo aparece cuando hay fuentes que mostrar; su rótulo se ajusta a la cantidad (*Ver la fuente* / *Ver las N fuentes*) y alterna a *Ocultar*.
- **Foco:** anillo azul de 2px con 2px de separación, igual que el indicador.

### Panel de evidencia

La lista de fuentes, desplegada dentro del detalle. Toma la forma con que X presenta cualquier colección.

- **Tapa:** título en *headline*, resumen de posturas en tinta media y la atribución.
- **Escalones:** cada nivel de la jerarquía —fuentes oficiales, medios de referencia, verificaciones previas— se anuncia con su propio encabezado en *label* sobre una línea separadora. El orden de los grupos se dibuja porque es la decisión de fondo de la pantalla.
- **Fila de fuente:** grilla de dos columnas, el dominio en tinta media a 13px sobre el título en tinta plena a 15px, y la pastilla de postura a la derecha. Las filas se separan entre sí por una línea y toman el velo al pasar por encima, que es lo que le da destino a su radio de 8px.
- **Pastilla de postura:** borde y texto en `currentColor` —rojo para *Contradice*, verde para *Corrobora*, gris para *Neutral*—, pastilla completa, acolchado `1px 9px`.
- **Enlace:** el título entero es el enlace, en tinta plena; al pasar por encima vira al azul y se subraya con 2px de separación. Lleva siempre el ícono de salida, que dice antes de tocar que el documento se abre fuera de X.
- **Pie:** una nota en tinta apagada que explica el orden de la jerarquía y la restricción de dominios.

### Patrón de ausencia

No es un componente sino un patrón que atraviesa tres superficies, y es la traducción visual del principio del producto.

- **En la cifra:** un guión largo en lugar del porcentaje, con el sustantivo cambiado por lo que efectivamente pasó.
- **En una barra:** relleno al ancho completo con una trama diagonal a 45° construida con velos (no con grises fijos, para que se lea igual sobre las dos variantes oscuras de X) y la etiqueta *sin dato* en lugar de la cifra.
- **En el ícono:** el círculo discontinuo, o medio discontinuo.
- **En la nota:** un recuadro de esquinas de 8px, borde y tinta apagada que nombra qué faltó y dice que el resultado no es concluyente.

### Movimiento

Tres animaciones, todas cortas y todas sobre la misma curva `cubic-bezier(0.16, 1, 0.3, 1)`, de salida rápida y asentado largo.

- **Asentar** (0,32s): el indicador baja 2px y sube de 0,55 a 1 de opacidad cuando llega el veredicto. Parte de un estado ya visible, así que nada queda escondido si la animación no corre.
- **Desplegar** (0,28s): el detalle entra desde 4px arriba.
- **Girar** (0,7s, lineal, infinita): el anillo del estado de análisis.
- **Con `prefers-reduced-motion`:** las transiciones y las dos entradas se apagan por completo, y el giro del anillo se estira a 2,4s en lugar de detenerse, porque es lo único que comunica que algo está pasando.

## Do's and Don'ts

### Do:
- **Do** apoyar todo fondo en un velo translúcido (`{colors.velo}`, `{colors.velo-fuerte}` o el velo del acento) para que la variante oscura de X se vea a través.
- **Do** comunicar cada estado por tres canales a la vez: color, forma del ícono y texto. La forma tiene que bastar para quien no distingue el color.
- **Do** construir todo ícono nuevo sobre la circunferencia de radio 7,5 con trazo 2, cambiando el interior y no la silueta.
- **Do** poner en tinta media (`{colors.tinta-media}`) cualquier línea que haya que leer para entender el veredicto, y dejar `{colors.tinta-apagada}` solo para dibujo —el aro de un ícono en reposo—, nunca para palabras.
- **Do** dibujar la ausencia como ausencia: guión en lugar de cifra, trama en lugar de relleno, trazo discontinuo en lugar de continuo.
- **Do** distinguir lo que el sistema encontró de lo que infirió: enlace azul con flecha de salida para lo primero, pastilla apagada para lo segundo.
- **Do** llevar la marca de atribución en cada región visible que emita un juicio, y **una sola vez** en cada una. La copia que se conserva es la que sobrevive al plegado.
- **Do** separar y agrupar con la línea de un píxel en `{colors.borde}`, que es como X separa todo.

### Don't:
- **Don't** pintar un fondo opaco en ninguna superficie de la extensión.
- **Don't** usar sombras, desenfoques de fondo ni ningún recurso que despegue una pieza del plano del *timeline*.
- **Don't** dar color de veredicto a un estado sin evidencia. *Sin contraste externo*, *análisis parcial* y la falla van en gris.
- **Don't** mostrar un porcentaje cuando el análisis está incompleto o no tuvo con qué contrastarse: una cifra calculada con un módulo caído se lee tan confiable como las demás y no lo es.
- **Don't** pegar el porcentaje al titular del veredicto. *Parece verificado · 16 %* se lee como «16 % verificado», que es lo contrario de lo que el número mide.
- **Don't** poner en el gris de X (`{colors.tinta-apagada}`) una línea que decida la lectura: sobre el carbón de *Dim* no llega al contraste mínimo.
- **Do** recortar toda enumeración **contando** —«y 1 más»— y nunca con elipsis de CSS. Cortada por elipsis, la lista de fuentes termina en una conjunción colgando y pierde en silencio una de las fuentes que sostienen el veredicto, que es justamente lo que el producto promete mostrar. El `line-clamp` queda solo como red de seguridad.
- **Do** reservar ancho fijo para la leyenda de despliegue. Sin eso, «Ocultar análisis» es más ancha que «Ver análisis» y desplegar el panel reacomoda el resumen de la cabecera.
- **Do** compartir el color de estado entre las dos mitades de la tarjeta fusionada. Si la ficha pinta su contorno con el acento del veredicto y el detalle con el borde neutro, el filete cambia de color a media altura.
- **Don't** apilar una segunda tarjeta bordeada bajo el indicador. Lo que se despliega es la misma ficha creciendo.
- **Don't** introducir una familia tipográfica, cargar una fuente web ni declarar una variante *display*.
- **Don't** dibujar un botón, una pestaña o un menú que prometa una acción que la demostración no ejecuta; la leyenda de despliegue y el pie de evidencia se ocultan solos cuando no hay nada que abrir.
- **Don't** enunciar nada sobre la cuenta que publicó. Toda superficie habla de la afirmación.
