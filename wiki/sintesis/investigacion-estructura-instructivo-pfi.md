---
titulo: Estructura y formato exigidos por el instructivo PFI, contra el documento actual
tipo: análisis
tags: [entrega, e90, formato, estructura, rubrica, documento]
fuentes: [Pautas-E75-Monzon-2026.pdf, Rubrica-PFI-2026-v1.3.xlsx, GR_M15_Feresini_Imbriago-EntregaFinal2025.pdf, Cronograma-PFI-Informatica-2026.pdf, notas-chat-pfi-2026.md, documento/README.md, documento/main.tex]
actualizado: 2026-10-19
---

# Estructura y formato exigidos por el instructivo PFI, contra el documento actual

Investigación del issue #77. La rúbrica (solapa *Formalidades y compromisos*, fila 3) pide «respetar la estructura del documento propuesta por el instructivo de PFI al 100 %», y la fila 4 pide respetar el formato: carátula, fuentes, tamaño de fuente, sangría, márgenes y pie de página.

## Primero: no hay un «instructivo» como archivo

En `raw/` no hay ningún documento llamado instructivo. El cronograma lo nombra como tema de la clase 1 del 14/3 («Normativa e instructivo de PFI», `Cronograma-PFI-Informatica-2026.pdf`, p. 1), pero no está archivado. Lo que hace de instructivo son tres fuentes. Esta es su prioridad cuando chocan:

1. **Pautas del 75 % de Monzón** (`raw/clases/Pautas-E75-Monzon-2026.pdf`). Es la más reciente y la más específica: son las correcciones que la cátedra aplica en 2026. Las diapositivas se construyen de a una viñeta, así que cito la primera página del PDF donde aparece cada viñeta.
2. **README del template UADE** (`documento/README.md`, sección «Estructura sugerida para tesis de proyecto») y la configuración que trae `documento/main.tex`. «Según el template» es el criterio que las pautas usan para el formato (p. 58, 59 y 65).
3. **Tesis de referencia Feresini-Imbriago 2025** (`raw/clases/GR_M15_Feresini_Imbriago-EntregaFinal2025.pdf`, tutor Monzón). Es un ejemplo aprobado, pero anterior a las pautas de 2026; en dos puntos las contradice (ver abajo). Las páginas se citan como «PDF n (impresa m)».

`raw/pfi-ejemplo/` está vacío y `raw/propuesta-de-tema-ejemplo/` solo tiene propuestas de tema, que no sirven para el informe final.

## Respuestas

### Orden exacto de las secciones

| # | Sección | Fuente |
|---|---|---|
| 0 | Carátula de la biblioteca | Pautas p. 44; README «Antes de las entregas» |
| 0 | Portada interna (título, autor y LU, carrera, tutor, año, logo UADE) | Feresini PDF 2; `chapters/title.tex` |
| 0 | Agradecimientos | Feresini PDF 3 (en el template se incluye por defecto) |
| 0 | Resumen | Feresini PDF 4; pautas p. 19 |
| 0 | Abstract (traducción al inglés del Resumen) | Feresini PDF 5; pautas p. 19 y 128 |
| 0 | Índice | Feresini PDF 6 a 9 |
| 1 | Introducción: Objetivos (general y específicos), Alcance y Estructura del documento | README; pautas p. 31 y 32 |
| 2 | Antecedentes: Marco Teórico (con el Marco Normativo) y Estado del Arte (con la Competencia y una conclusión con título) | README; pautas p. 15, 33, 130 y 132 |
| 3 | Descripción: User Research y lo demás que describe la propuesta (negocio, financiero y legal en la tesis de referencia) | README; Feresini PDF 7 y 8 |
| 4 | Metodología de desarrollo: Metodología / Arquitectura y tecnologías utilizadas / Validación del sistema | README; pautas p. 16 y 41 |
| 5 | Conclusión general («Conclusiones generales» en las pautas) | README; pautas p. 20 y 209 |
| 6 | Bibliografía | README; Feresini PDF 9 |
| 7 | Anexos | README; pautas p. 35 y 36 |
| 8 | Lista de Figuras | README; Feresini PDF 9 |
| 9 | Lista de Tablas | README; Feresini PDF 9 |

Si los aspectos legales son extensos, van en una sección propia y no dentro de otra (pautas p. 18 y 42). Para un proyecto de desarrollo no se usa la estructura de investigación con pregunta e hipótesis (pautas p. 30).

> ⚠️ CONTRADICCION: la tesis de referencia tiene «5. Pruebas Realizadas» y «6. Discusión» como capítulos aparte (Feresini PDF 8 y 9). Las pautas de 2026 y el README ponen la validación dentro del cap. 4. Mandan las pautas.

### Listas de figuras y tablas

- Van **al final**, después de los anexos, primero figuras y después tablas (README, ítems 8 y 9; Feresini PDF 9: «Lista de Figuras 136», «Lista de Tablas 138»).
- **Sí entran al índice**: la tesis de referencia las lista en él (Feresini PDF 9).
- Son obligatorias si el documento tiene figuras o tablas (pautas p. 50).

### Glosario

**No es obligatorio.** Ninguna fuente lo pide: ni las pautas, ni el README, ni la rúbrica. La tesis de referencia no tiene glosario. Lo que sí se exige es explicar cada término del dominio la primera vez que se usa (pautas p. 103) y escribir cada término siempre de la misma forma (pautas p. 116 y 117). `CLAUDE.md` menciona «siglas definidas en el glosario del documento», pero ese glosario no existe y no hace falta crearlo.

### Marca, misión, visión y *branding*

Ninguna fuente fija el capítulo de forma normativa. Lo que hay:

- En la tesis de referencia van en el **cap. 3 (Descripción)**: «3.2.4 Producto», con 3.2.4.1 Estilo, 3.2.4.2 Logo, 3.2.4.3 Misión y 3.2.4.4 Visión, seguidos de Cruz de Porter y FODA, dentro de «3.2 Solución» (Feresini PDF 7).
- La rúbrica pone «Branding y logotipo» en la solapa **Desarrollo negocio**, al lado del modelo de negocio y la viabilidad económico-financiera (`Rubrica-PFI-2026-v1.3.xlsx`, solapa DESARROLLO NEGOCIO, fila 5). Pide desarrollar el logo, explicar sus razones y su diseño, y usar otros conceptos de *branding* o marketing.
- Las pautas del 75 % solo lo nombran entre los ítems de la rúbrica (p. 226).

Lo más defendible es que vaya en el cap. 3, con el negocio. No va en «Arquitectura y tecnologías utilizadas», porque no es ni una cosa ni la otra.

### Qué contiene «Metodología de desarrollo» y su 4.1

- **Estructura oficial** (pautas p. 41; README): 4.1 Metodología, 4.2 Arquitectura y tecnologías utilizadas, 4.3 Validación del sistema. Se cierra al final del proyecto (pautas p. 17 y 40).
- **4.1 Metodología**: según la rúbrica (DESARROLLO FUNCIONAL, fila 6), hay que nombrar la metodología, técnica o ciclo de vida y justificarla de forma válida, siguiendo sus aspectos, sea ágil o estructurada. Una justificación débil o que no coincide con la definición teórica es «cumple parcialmente». La tesis de referencia lo resuelve así (Feresini PDF 97 a 100, impresas 95 a 98): justificación del enfoque ágil, planificación y requisitos con un *Product Backlog* en tabla, dinámica de iteraciones, revisión y retrospectiva, y después diseño, implementación y pruebas contados como fases del proceso.
- **4.2**: tecnologías justificadas, arquitectura con diagramas de calidad profesional y UML con su sintaxis estándar (pautas p. 192 y 193), y modelo de datos con tipos y cardinalidades (p. 207). Si hay aprendizaje automático, el proceso de entrenamiento documentado (p. 198); si hay LLM, la mitigación de *prompt injection* (p. 201).
- **4.3**: pruebas funcionales y sus resultados, con conclusiones y decisiones (rúbrica DESARROLLO FUNCIONAL, filas 7 y 8), y cobertura de pruebas de al menos 85 % (pautas p. 197).

### Reglas de formato

Las pautas remiten al template para tamaños, encabezado y pie (p. 58, 59 y 65), así que el template es la norma. Los valores son de `documento/main.tex`, y la tesis de referencia los confirma.

| Aspecto | Regla | Fuente |
|---|---|---|
| Papel | A4, una cara | `main.tex` l. 5; Feresini (pdfinfo: A4) |
| Fuente | Times (`mathptmx`), 12 pt | `main.tex` l. 5 y 170; Feresini usa NimbusRomNo9L, el clon de Times |
| Títulos | Todos los niveles en negrita y 14 pt (capítulo, sección, subsección y subsubsección), con 12 pt antes y 6 pt después. El comentario del template dice «nos piden que el tamaño de letra de [...] sección, subsección y demás, sean del mismo tamaño» | `main.tex` l. 203 a 223; en Feresini los títulos de los tres niveles miden lo mismo (12,5 pt de caja contra 10,7 del texto) |
| Títulos de índice y listas | 14 pt, negrita | `main.tex` l. 229 a 235 |
| Interlineado | 1,5 (`\onehalfspacing`) | `main.tex` l. 201 |
| Sangría | 36 pt, también en el primer párrafo (`indentfirst`) | `main.tex` l. 162 y 163 |
| Márgenes | Izquierdo 2,7 cm y derecho 2,3 cm; el comentario del template da como ideal 4 cm arriba y 2,5 cm abajo | `main.tex` l. 100 a 109 |
| Encabezado | Logo UADE, título del PFI en mayúsculas y «Apellido, Nombre», con filete | `main.tex` l. 82 a 90; pautas p. 54 a 56 |
| Pie | «Página X de Y», con filete | `main.tex` l. 88; pautas p. 59 y 79 |
| Índice | Hasta 4 niveles | Rúbrica FORMALIDADES fila 5; pautas p. 52; `tocdepth` = 3 |
| Numeración | Sin punto final («2.1.3»); figuras en arábigo; tablas como capítulo + romano («4.I») | Pautas p. 60 y 63; `main.tex` l. 129 |
| Epígrafes | El de la tabla arriba y el de la figura abajo, con la fuente | Pautas p. 62 y 73 |
| Títulos de sección | Mayúscula solo al principio, como en una oración | Pautas p. 70 |
| Enlaces | Negros, sin color | Pautas p. 53; README; notas del chat (l. 44) |
| Portada | Solo el año en las entregas parciales; la afiliación del tutor solo si es externo | Pautas p. 45 y 49 |
| Citas | ISO 690, parentéticas, con `\parencite` (la rúbrica dice «ISO 9001», que es un error de tipeo) | Pautas p. 155 y 167; rúbrica FORMALIDADES fila 8 |

## Diferencias con el documento actual

Comparación contra `documento/main.tex`, `documento/chapters/` y el PDF compilado del 19/10 (`documento/main.pdf`, 179 páginas, y `main.toc`).

### Hay que corregir (incumple una fuente)

1. **Las listas de figuras y tablas no están en el índice.** `main.tex` (l. 304 y 306) llama a `\listoffigures` y `\listoftables` sin `\addcontentsline`, y `main.toc` no tiene esas entradas. La tesis de referencia sí las lista (Feresini PDF 9). La posición, al final, es la correcta.
2. **«Estructura del documento» está dentro de Alcance.** Hoy es la subsección 1.2.4 (`chapter01.tex` l. 67). Las pautas dicen «Estructura del documento: apartado de Introducción, no de Alcance» (p. 32): tiene que ser una sección hermana de Objetivos y Alcance. El README del template la pone dentro de Alcance, pero mandan las pautas, que son más nuevas.
3. **La Competencia es hermana del Estado del Arte.** Hoy es la sección 2.3 «Análisis de competencia» (`chapter02.tex` l. 268). Las pautas dicen «Competencia dentro del Estado del Arte» (p. 130) y piden que el Estado del Arte cierre con una conclusión con título (p. 132). Hoy la conclusión (2.2.6) queda antes de la competencia. Si la competencia entra en el Estado del Arte, la conclusión tiene que quedar última.
   > ⚠️ CONTRADICCION: la tesis de referencia tiene «2.3 Competencia» como sección hermana (Feresini PDF 6), igual que el documento actual. Las pautas de 2026 lo corrigen.
4. **Océano azul, matriz ERIC y curva de valor están al mismo nivel.** Hoy «Espacio diferencial» (el océano azul), «Matriz de eliminar, reducir, incrementar y crear», «Diccionario de variables» y «Curva de valor» son subsecciones hermanas (`chapter02.tex` l. 297, 307, 361 y 391). Las pautas piden que el océano azul contenga la matriz ERIC y la curva de valor (p. 34). Si además se aplica el punto 3, la matriz y la curva quedan en el cuarto nivel. El cuarto nivel entra en el índice. Los `\paragraph` Eliminar, Reducir, etc. quedan en el quinto, que no entra.
5. **Un solo anexo para las dos entrevistas.** `appendix/interviews.tex` abre un único `\anexo{Transcripciones de las entrevistas}` y adentro pone las dos como `\section*`. Las pautas piden un anexo por entrevista (p. 36), y así lo hace la tesis de referencia: Anexo A y Anexo B (Feresini PDF 9).
6. **La portada incluye la afiliación del tutor, que es interno.** `chapters/title.tex` pone «(UADE) Universidad Argentina de la Empresa Lima 757...» debajo de Giro Uribazo. Las pautas dicen: «Afiliación del tutor/cotutor: sólo si es externo» (p. 45).
7. **La marca está en «Arquitectura y tecnologías utilizadas».** «4.2.4 Producto», con Estilo, Logo, Misión y Visión, está en `chapter04.tex` l. 256 a 315. Ninguna regla escrita lo prohíbe, pero la tesis de referencia lo pone en el cap. 3 (Feresini PDF 7) y la rúbrica lo evalúa con el negocio. Se recomienda moverlo al cap. 3, junto al modelo de negocio.

### Menores o de nombre

8. **Título de la conclusión.** El capítulo se llama «Conclusión» (`conclusion.tex` l. 1). El README dice «Conclusión general» y las pautas, «Conclusiones generales» (p. 20 y 209). La tesis de referencia usa «Conclusión». No es obligatorio, pero cambiarlo alinea el documento con la norma de 2026.
9. **Agradecimientos desactivado.** Está comentado en `main.tex` (l. 285) y el archivo todavía dice «Completar.». La tesis de referencia lo incluye; ya figura como pendiente en [[wiki/proyecto/entrega-90-alcance]].
10. **Margen superior distinto del template original.** El commit `8c64038` (2026-06-04) cambió `\setmarginsrb{2.7cm}{2cm}{2.3cm}{1.5cm}{0cm}{2cm}...` por `{2.7cm}{0.5cm}{2.3cm}{1.5cm}{2cm}{0.5cm}...`. Midiendo el PDF, el cuerpo del texto empieza casi a la misma altura que en la tesis de referencia (113 pt contra 117 pt desde el borde) y los márgenes izquierdo y del pie coinciden. Lo que cambia es el encabezado, que queda unos 18 pt más arriba (49 pt contra 67 pt). No es necesario corregirlo, salvo que se pida el valor exacto del template.
11. **«Riesgos y desafíos del proyecto» dentro de Alcance** (1.2.3). No está en el README ni en la tesis de referencia. Ninguna regla lo prohíbe; se puede dejar.

### Ya cumple

- Los cuatro capítulos están en el orden del README. El cap. 4 tiene exactamente Metodología, Arquitectura y tecnologías utilizadas, y Validación del sistema.
- El Marco Normativo está dentro del Marco Teórico (2.1.7). La justificación de los conjuntos de datos también está en el Marco Teórico (2.1.6, pautas p. 119). La viabilidad legal es una sección propia (3.4).
- Orden de las partes: carátula, portada, Resumen, Abstract, Índice, capítulos, Bibliografía (en el índice), Anexos, listas.
- Índice con 4 niveles (`tocdepth` = 3), tablas numeradas en romano, «Página X de Y», enlaces en negro (`hidelinks`), Times 12 pt, títulos de 14 pt, interlineado 1,5 y sangría de 36 pt, todo igual al template.
- No hay glosario, y no hace falta.
- El FODA (2.3.6) no usa datos de la encuesta ni de las entrevistas, así que no choca con «FODA con datos de UR después del User Research» (pautas p. 124).

## Referencias cruzadas

- [[wiki/proyecto/entrega-90-alcance]]
- [[wiki/proyecto/calibracion-tesis-referencia]]
- [[wiki/proyecto/cronograma]]

## Fuentes

- [[raw/clases/Pautas-E75-Monzon-2026.pdf]]
- [[raw/clases/Rubrica-PFI-2026-v1.3.xlsx]]
- [[raw/clases/GR_M15_Feresini_Imbriago-EntregaFinal2025.pdf]]
- [[raw/clases/Cronograma-PFI-Informatica-2026.pdf]]
- [[raw/clases/notas-chat-pfi-2026.md]]
- `documento/README.md`, `documento/main.tex`, `documento/chapters/`
