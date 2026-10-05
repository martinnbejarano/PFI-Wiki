---
titulo: Guía de etiquetado del corpus argentino de prueba
tipo: proyecto
tags: [corpus-argentino, etiquetas, chequeado, indec, bcra, conjunto-de-prueba]
fuentes: [https://chequeado.com/metodo/]
actualizado: 2026-09-28
---

# Guía de etiquetado del corpus argentino de prueba

Criterio único para pasar cada candidato de la planilla (`prototipo/clasificador/datos/corpus_argentino/candidatos.csv`) a una de las dos clases del clasificador, `verdadero` o `falso`. La etiqueta **no sale de un juicio propio**: sale de la calificación que Chequeado publicó sobre ese tuit o del dato oficial (INDEC, BCRA) que el tuit cita. El autor confirma o corrige cada fila en la columna `etiqueta_confirmada` aplicando esta guía.

## 1. Calificaciones de Chequeado → clase

Chequeado usa dos escalas ([método](https://chequeado.com/metodo/), consultado el 2026-09-28): una para el discurso público de dirigentes y otra, más corta, para desinformación viral (Falso, Engañoso, Verdadero, Insostenible).

| Calificación | Definición de Chequeado (resumida) | Clase |
|---|---|---|
| **Verdadero** | Demostrada verdadera contra las fuentes más confiables | `verdadero` |
| **Verdadero, pero…** | Consistente con los datos, pero omite algún elemento o el contexto | `verdadero` |
| **Falso** | Demostrada falsa contra las fuentes más confiables | `falso` |
| **Engañoso** | Coincide en parte con datos ciertos, pero fue manipulada para dar un mensaje | `falso` |
| **Exagerado** | No es estrictamente cierta, aunque sí la tendencia a la que alude | descartar |
| **Discutible** | No es claro si es cierta; depende de las variables del análisis | descartar |
| **Apresurado** | Podría ser cierta, pero es una proyección y no un dato | descartar |
| **Insostenible** | Sale de investigaciones sin sustento o es imposible de chequear | descartar |
| **Inchequeable** | Corpus sin ninguna afirmación contrastable | descartar |

Cada extremo de la escala absorbe su grado vecino y el centro se descarta. Es el mismo corte que la tabla de mapeo de LIAR (`barely-true` → `falso`, `mostly-true` → `verdadero`), pero más estricto: como el corpus es solo de prueba, se prefiere perder filas antes que medir contra una etiqueta dudosa.

## 2. Tuits con un dato oficial (INDEC, BCRA)

Un tuit que cita una cifra del INDEC o del BCRA es `verdadero` **solo si la cifra coincide con la publicación oficial**: mismo indicador, mismo período, mismo ámbito y el valor publicado (se admite el redondeo al decimal que usa el organismo). El enlace de la fila tiene que llevar al informe, cuadro o comunicado oficial que muestra ese número.

- Si la cifra no coincide, el tuit **se descarta**: no pasa a `falso`, porque el desvío puede ser un error de tipeo o una desactualización y nadie lo calificó.
- Si el tuit mezcla el dato con una interpretación («la pobreza bajó gracias a…»), se evalúa solo si la interpretación no es una afirmación fáctica distinta; si lo es, se descarta.

## 3. Qué se descarta siempre

1. **El tuit no es el contenido verificado.** Una nota que califica un video de Instagram y cita un tuit de un economista como fuente no aporta ese tuit: su texto no fue calificado.
2. **Sin afirmación en el texto.** Tuits cuyo contenido chequeado es solo la imagen o el video («mirá esto» + video) y el texto no enuncia el hecho calificado.
3. **Fuera de idioma u origen.** Solo tuits en español de cuentas argentinas, o de cuentas anónimas cuyo contenido circuló en la Argentina sobre un tema argentino. Ante la duda, se descarta.
4. **No verificable por método.** Opiniones, promesas, sátira declarada o pronósticos, que Chequeado no califica.
5. **Duplicados.** Mismo identificador de tuit, o mismo texto tras normalizar (minúsculas, sin tildes, sin URL ni menciones, espacios colapsados). Se conserva la primera aparición.
6. **Calificación ambigua para ese tuit.** Si la nota califica varias afirmaciones y no queda claro cuál corresponde al tuit, se descarta.

## 4. Columnas de la planilla

| Columna | Contenido |
|---|---|
| `enlace_tuit` | URL del tuit tal como figura en la nota o la fuente |
| `texto` | Texto del tuit tal como lo reproduce la fuente (embebido o cita textual) |
| `calificacion_original_o_dato_oficial` | Calificación de Chequeado, o el dato oficial citado |
| `enlace_nota_o_fuente` | Nota de Chequeado o publicación oficial que sustenta la etiqueta |
| `etiqueta_propuesta` | Clase según esta guía |
| `etiqueta_confirmada` | Vacía; la completa el autor |

La planilla es solo conjunto de prueba (*holdout* estricto, ver [[datasets-overview]]) y no se distribuye durante el PFI.

## Referencias cruzadas
- [[datasets-overview]]
- [[pruebas]]
- [[restricciones-legales-eticas]]

## Fuentes
- Chequeado, «Método de verificación»: https://chequeado.com/metodo/
