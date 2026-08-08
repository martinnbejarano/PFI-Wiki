---
titulo: Entrega 2 (50%) — alcance según la rúbrica oficial
tipo: proyecto
tags: [entrega, 50, rubrica, ep2, alcance]
fuentes: [Rubrica-EP2-50porciento.pdf, notas-chat-pfi-2026.md]
actualizado: 2026-08-08
---

# Entrega 2 (50%) — alcance según la rúbrica oficial

**Entrega del documento: 22/08/2026** (comisiones de sábado; los martes entregan el 18/08).
**Exposición: 29/08/2026.**

## Corrección importante del alcance

Hasta el 2026-08-08 el wiki y el anexo del documento asumían que la Entrega 2 cubría *user research, competencia y modelo de negocio*. **La rúbrica oficial de EP2 dice otra cosa**: evalúa principalmente la **solución** —requerimientos, mockups, diagramas, tecnologías, modelo de datos y una demo con avances de implementación— más las herramientas de marketing sobre la competencia y una tabla comparativa en el estado del arte. El user research entra también, por lo dicho en clase, aunque la rúbrica no lo nombra.

Consecuencia directa: las páginas `solucion/requerimientos`, `solucion/arquitectura`, `solucion/tecnologias` y el modelo de datos —que el lint del 2026-08-08 clasificó como bloqueantes de octubre— son en realidad **bloqueantes del 22 de agosto**.

## Los ocho criterios de la rúbrica

| # | Concepto | Estándar para cumplir | Estado en el wiki |
|---|---|---|---|
| 1 | **Requerimientos** | Análisis funcional correcto (casos de uso o historias de usuario). Existen requerimientos funcionales y/o no funcionales | 🔴 `solucion/requerimientos.md` es un stub `[POR DEFINIR]` |
| 2 | **Mockups** | Herramientas visuales para interpretar el trabajo: wireframes o pantallas claras y significativas del frontend | 🔴 No existen |
| 3 | **Diagramas** | Diagramas recomendables para la implementación: flujo de información, componentes, clases, objetos. Nomenclatura clara y sintaxis respetada | 🔴 No existen (hay un diagrama de pipeline en el documento, insuficiente) |
| 4 | **Competencias** | Herramientas de marketing y desafíos con la competencia: triple P, FODA, Cruz de Porter, Matriz Boston Consulting | 🟢 FODA y 5 Fuerzas ya están en `negocio/modelo-de-negocio`; falta volcarlos al documento |
| 5 | **Tecnologías** | Explica y justifica la elección de lenguajes y la arquitectura de red que enmarca el trabajo | 🟡 `solucion/tecnologias.md` es stub, pero `proyecto/recursos.md` ya justifica casi todo el stack |
| 6 | **Modelo de datos** | Diagramas para comprender el modelo de datos: diagrama de base de datos y diagrama de arquitectura | 🔴 No existen |
| 7 | **Demo** | Capturas que muestren avances en el desarrollo de las funcionalidades | 🔴 No hay código |
| 8 | **Tabla comparativa** | El estado del arte cuenta con una tabla comparativa respecto a las alternativas del proyecto planteado | 🟢 Cumplido: `chapter02.tex:244`, tabla `tab:competidores` — "Matriz comparativa de las soluciones existentes" |

## Lo que agrega la clase, fuera de la rúbrica

De lo transcripto del 04/07 (ver [[raw/clases/notas-chat-pfi-2026.md]]):

- **User research entra en el 50%**: encuesta analizada, entrevistas transcriptas y user personas.
- **Exposición de ~20 minutos**, mitad orientada a negocio y mitad a público técnico.
- **La parte económica no entra** — el análisis financiero (VAN, TIR, payback) puede sumarse pero no se exige. Esto baja la prioridad de `negocio/analisis-financiero.md`.
- La **demo** puede ser en vivo, con capturas comentadas o en video.
- Las transcripciones de entrevistas **no deben pasarse por un LLM**: cambia el tono y lo detectan.

## Contradicciones entre fuentes

1. **FODA.** La rúbrica lo acepta explícitamente; las notas de la clase de Monzón dicen "no hacer FODA, es muy sencillo". No es un acuerdo del curso, es la preferencia de un docente de otra comisión. **Prevalece la rúbrica**: se conserva el FODA y se suma al menos una herramienta más (la Cruz de Porter ya está hecha).
2. **Cantidad de entrevistas.** Sin consenso: circulan 3, 5 y "ninguna si hacés encuesta". Lo estable es que con encuesta alcanza con menos. Con 2 entrevistas se está dentro del rango que reportan quienes también hicieron encuesta; 3 da margen.
3. **Mínimo de 120 respuestas.** Viene solo de la clase de Monzón, no de la rúbrica ni del tutor propio. Es el número más citado del curso, pero no es una regla verificada para esta comisión.
4. **Qué se sube el 22.** Sin resolver en el chat: unos entendieron que solo el documento y otros que también la presentación y la demo. **Pendiente de confirmar con el tutor.**

## Mapeo a los capítulos del documento

| Criterio de la rúbrica | Destino |
|---|---|
| User research | `chapter03.tex` + `appendix/surveys.tex` + `appendix/interviews.tex` |
| Competencias (marketing) | `chapter03.tex` |
| Requerimientos y casos de uso | `chapter04.tex` |
| Arquitectura, diagramas y modelo de datos | `chapter04.tex` |
| Tecnologías | `chapter04.tex` |
| Mockups | `chapter04.tex` (figuras) |
| Demo | Presentación + capturas en `chapter04.tex` |
| Tabla comparativa | `chapter02.tex` (estado del arte) |

Hoy `chapter03.tex` y `chapter04.tex` tienen 18 palabras cada uno, todas `Completar.`

## Referencias cruzadas

- [[wiki/proyecto/cronograma]]
- [[wiki/investigacion/user-research]]
- [[wiki/solucion/requerimientos]]
- [[wiki/solucion/arquitectura]]
- [[wiki/solucion/tecnologias]]
- [[wiki/negocio/modelo-de-negocio]]
- [[wiki/sintesis/decisiones-pendientes-2026-08]]

## Fuentes

- [[raw/clases/Rubrica-EP2-50porciento.pdf]] — rúbrica oficial de la Entrega Parcial 2
- [[raw/clases/notas-chat-pfi-2026.md]] — notas destiladas del chat del curso
