---
titulo: Guion de la prueba de usabilidad
tipo: proyecto
tags: [usabilidad, sus, validacion, rnf-15]
fuentes: [documento/chapters/chapter04.tex]
actualizado: 2026-10-05
---

# Guion de la prueba de usabilidad

Material para ejecutar la prueba que describe la sección *Prueba de usabilidad* del cap. 4 (`sec:usabilidad`) y que verifica RNF-15: un usuario sin conocimiento técnico interpreta el indicador y completa el análisis **sin instrucción previa**. Los resultados se cargan en `prueba-usabilidad-registro.xlsx` (misma carpeta).

## Qué hay que mandar al terminar

1. **`prueba-usabilidad-registro.xlsx` completa**: una fila por participante en cada hoja. El puntaje SUS y el resumen se calculan solos.
2. **Fotos**: 2 o 3 en total alcanzan (el documento pide «una figura por foto»). Mejor de la pantalla y las manos que de la cara; si sale una cara, con permiso explícito.
3. **Fecha y lugar** de cada sesión (van en la hoja *Participantes*).

Con eso se completan las marcas `\Martin` de la sección: participantes, fotos, tabla del cuestionario, tabla SUS y la narración.

## Participantes

- **Cantidad:** 5. Con cinco personas aparece la mayoría de los problemas de usabilidad graves (Nielsen y Landauer, 1993) [sin verificar contra la fuente]; más de 8 no agrega mucho para un prototipo.
- **Perfil:** usan X al menos de vez en cuando, **no** son de sistemas y **no** vieron la extensión ni escucharon cómo funciona. Idealmente variar edad y ocupación.
- **Duración:** 20 a 25 minutos por persona.

## Preparación (antes de cada sesión)

- [ ] Servicio corriendo en tu Mac (`prototipo/servicio`) y respondiendo en `/salud`.
- [ ] Extensión cargada en Chrome (modo desarrollador → *Cargar descomprimida*) y con el ícono visible.
- [ ] Una ventana de Chrome **limpia** (perfil aparte), para que la persona entre a X con su cuenta o con la cuenta de prueba y cierre sesión al final.
- [ ] Probar una vez que en la línea de tiempo aparecen los indicadores y que el análisis profundo devuelve fuentes.
- [ ] Planilla abierta, cronómetro a mano, celular para las fotos.

## Guion

Leelo casi textual. La regla de oro: **no explicar qué significa el indicador ni cómo se usa**, aunque la persona pregunte. Si pregunta, respondé «¿qué te parece a vos?» y anotá la duda.

### 1. Bienvenida (2 min)

> «Gracias por venir. Estoy probando una extensión para el navegador que forma parte de mi trabajo final. **No te estoy evaluando a vos, estoy evaluando la extensión**: si algo no se entiende, es un problema de la extensión. Te voy a pedir que pienses en voz alta: que digas lo que mirás, lo que esperás que pase y lo que te confunde. No te puedo ayudar durante las tareas, pero al final charlamos. ¿Te parece bien que saque un par de fotos de la pantalla mientras la usás? No guardo nada de tu cuenta.»

### 2. Tareas (10 a 15 min)

Leé cada consigna, no agregues nada. Anotá en la hoja *Tareas*: si la completó **sin ayuda**, **con ayuda** o **no la completó**, el tiempo aproximado y lo que dijo en voz alta.

| N.º | Consigna para el participante | Se completa cuando… |
|---|---|---|
| T1 | «Entrá a tu inicio de X y mirá algunas publicaciones. ¿Qué te parece que indica la marca que aparece en algunas de ellas?» | Explica con sus palabras qué indica el indicador (que evalúa si la publicación es confiable o verdadera). |
| T2 | «Elegí una publicación que te interese y tratá de obtener más información sobre si lo que dice es cierto.» | Llega al análisis profundo de esa publicación. |
| T3 | «Ahora tratá de comprobar por tu cuenta en qué se basa ese resultado.» | Abre una de las fuentes que sostienen el veredicto. |

«Con ayuda» = le diste cualquier pista. Si pasan unos 3 minutos sin avance, das la pista mínima, la anotás y seguís.

### 3. Cuestionario cualitativo (5 min)

Preguntá en voz alta y anotá la respuesta casi textual en la hoja *Cuestionario*. Son las mismas preguntas de la tabla del cap. 4.

1. ¿Qué entendiste que indicaba la marca que apareció sobre las publicaciones?
2. ¿Te resultó claro qué hacer para obtener más información sobre una publicación?
3. ¿Las fuentes que mostró el análisis te permitieron comprobar el resultado por tu cuenta?
4. ¿Hubo algún momento en que no supieras qué estaba haciendo la extensión?
5. ¿La extensión interfirió con tu forma habitual de usar X?
6. ¿Usarías la extensión en tu navegador? ¿Por qué?

### 4. Cuestionario SUS (3 min)

Dale la hoja impresa de abajo (o leéla) y que marque **sin pensar mucho**, una opción por fila. Pasá los números a la hoja *SUS*: el puntaje sale solo.

### 5. Cierre (2 min)

Agradecé, contale ahora sí cómo funciona si quiere saber, y que **cierre sesión de X** en ese Chrome.

## Hoja para el participante — Escala SUS

*Marcá un número por fila. 1 = totalmente en desacuerdo, 5 = totalmente de acuerdo.*

| N.º | Afirmación | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| 1 | Creo que me gustaría usar este sistema con frecuencia. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 2 | Encontré el sistema innecesariamente complejo. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 3 | Pensé que el sistema era fácil de usar. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 4 | Creo que necesitaría el apoyo de una persona con conocimientos técnicos para poder usar este sistema. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 5 | Encontré que las distintas funciones del sistema estaban bien integradas. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 6 | Pensé que había demasiada inconsistencia en el sistema. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 7 | Imagino que la mayoría de las personas aprendería a usar este sistema muy rápidamente. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 8 | Encontré el sistema muy engorroso de usar. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 9 | Me sentí muy seguro usando el sistema. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 10 | Necesité aprender muchas cosas antes de poder empezar a usar este sistema. | ☐ | ☐ | ☐ | ☐ | ☐ |

Las afirmaciones son las de la tabla `tab:sus` del cap. 4 (Brooke, 1996).

## Umbral para RNF-15 (pendiente de decidir)

El cap. 4 deja abierto si RNF-15 se acepta con un umbral SUS. La referencia habitual es **68**, el promedio de cientos de estudios publicado por Sauro (2011) [sin verificar contra la fuente; si se adopta, agregar la cita a `biblio.bib`]. Conviene fijarlo **antes** de correr la prueba, por la misma razón que el protocolo del clasificador se fijó antes de ver los resultados.

## Referencias cruzadas
- [[pruebas]]
- [[requerimientos]]
- [[user-research]]
