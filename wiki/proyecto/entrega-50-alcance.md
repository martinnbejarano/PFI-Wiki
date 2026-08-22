---
titulo: Entrega 2 (50%) — alcance según la rúbrica oficial
tipo: proyecto
tags: [entrega, 50, rubrica, ep2, alcance]
fuentes: [Rubrica-EP2-50porciento.pdf, notas-chat-pfi-2026.md]
actualizado: 2026-08-22
---

# Entrega 2 (50%) — alcance según la rúbrica oficial

**Entrega del documento: 22/08/2026** (comisiones de sábado; los martes entregan el 18/08).
**Exposición: 29/08/2026.**

## Corrección importante del alcance

Hasta el 2026-08-08 el wiki y el anexo del documento asumían que la Entrega 2 cubría *user research, competencia y modelo de negocio*. **La rúbrica oficial de EP2 dice otra cosa**: evalúa principalmente la **solución** —requerimientos, mockups, diagramas, tecnologías, modelo de datos y una demo con avances de implementación— más las herramientas de marketing sobre la competencia y una tabla comparativa en el estado del arte. El user research entra también, por lo dicho en clase, aunque la rúbrica no lo nombra.

Consecuencia directa: las páginas `solucion/requerimientos`, `solucion/arquitectura`, `solucion/tecnologias` y el modelo de datos —que el lint del 2026-08-08 clasificó como bloqueantes de octubre— son en realidad **bloqueantes del 22 de agosto**.

## Los ocho criterios de la rúbrica

> Estado al **2026-08-22**, contra el PDF entregado (124 páginas, 21 figuras, 42 tablas). La columna de estado se releva contra el documento, no contra el wiki.

| # | Concepto | Estándar para cumplir | Estado |
|---|---|---|---|
| 1 | **Requerimientos** | Análisis funcional correcto (casos de uso o historias de usuario). Existen requerimientos funcionales y/o no funcionales | ✅ 16 RF con prioridad MoSCoW, 17 RNF con valor comprometido, 7 casos de uso con flujos alternativos y matriz de trazabilidad CU → RF |
| 2 | **Mockups** | Herramientas visuales para interpretar el trabajo: wireframes o pantallas claras y significativas del frontend | ✅ 4 pantallas: indicador sobre el tuit en sus cuatro estados, detalle del veredicto, panel de evidencia y panel de tendencias |
| 3 | **Diagramas** | Diagramas recomendables para la implementación: flujo de información, componentes, clases, objetos. Nomenclatura clara y sintaxis respetada | ✅ 9 diagramas propios: C4 en tres niveles, flujo de información, dos de secuencia, casos de uso, despliegue de red, DER y pipeline |
| 4 | **Competencias** | Herramientas de marketing y desafíos con la competencia: triple P, FODA, Cruz de Porter, Matriz Boston Consulting | ✅ 5 herramientas: matriz ERIC, curva de valor con diccionario de variables, FODA, cinco fuerzas de Porter y mix 4P. Se explicita por qué la Matriz BCG no aplica |
| 5 | **Tecnologías** | Explica y justifica la elección de lenguajes y la arquitectura de red que enmarca el trabajo | ✅ Tabla por capa con versiones fijadas, 8 decisiones con su alternativa descartada y arquitectura de red con protocolos y cruces de frontera |
| 6 | **Modelo de datos** | Diagramas para comprender el modelo de datos: diagrama de base de datos y diagrama de arquitectura | ✅ DER de 17 entidades en cinco dominios con matriz entidad → RF, más el diagrama de despliegue |
| 7 | **Demo** | Capturas que muestren avances en el desarrollo de las funcionalidades | 🔴 **No hay código.** Confirmado que corresponde a la exposición del 29/08, no al documento del 22 |
| 8 | **Tabla comparativa** | El estado del arte cuenta con una tabla comparativa respecto a las alternativas del proyecto planteado | ✅ `tab:competidores` en `chapter02.tex` |

### User research — fuera de la rúbrica pero pedido en clase

| Instrumento | Estado |
|---|---|
| Encuesta | ✅ 140 respuestas, 107 en segmento, campo 04/07 al 18/08 → [[wiki/investigacion/encuesta-resultados]] |
| Entrevistas | 🟡 2 realizadas (Maidan, fundador de empresa de IA; Soruco, periodista de Canal 10 Salta) → [[wiki/investigacion/entrevistas]]. **Falta el perfil de organización de verificación**, gestionado sin resultado dentro del plazo |
| User personas | ✅ 2 construidas sobre evidencia, con el dato de respaldo de cada atributo |

### Checklist de entrega — estado final

| Ítem | Estado |
|---|---|
| Carátula oficial de la biblioteca UADE | ✅ `cover/Caratula 2026.pdf`, incluida con `\includepdf` |
| Portada interna y encabezado alineados con la carátula | ✅ Corregidos el 22/08: el título lleva "Sistema de" y el tutor lleva la tilde en Valentín |
| Referencias en negro (`hidelinks`) | ✅ |
| Sin `\Fidel{}` ni `\Martin{}` | ✅ |
| Sin `Completar.` en el PDF | ✅ Cero. Los que quedan en archivos están en `conclusion`, `summary`, `abstract` y `acknowledgments`, todos comentados en `main.tex` |
| `biber` sin advertencias | ✅ Cero referencias sin resolver |
| Fecha: solo el año | ✅ |
| Cronograma fuera del anexo | ✅ Comentado en `annex.tex` según el checklist de `CLAUDE.md`. Los anexos quedan en A (encuesta) y B (entrevistas) |

### Lo que queda para la exposición del 29/08

1. **La demo (criterio 7).** Ver opciones en [[wiki/investigacion/entrevistas]] y el log del 22/08: rebanada vertical mínima (content script + endpoint + inferencia + badge) o, como piso, un notebook con fine-tuning y métricas.
2. **Presentación de ~20 minutos**, mitad negocio y mitad técnica.
3. **Tres preguntas previsibles del tribunal**, con la respuesta preparada: por qué no hay entrevista a una organización de verificación; cómo se tratan las afirmaciones que mezclan dato verdadero con interpretación, dado que se eliminó la categoría "engañoso"; y cómo se valida la clase `sin_verificar`, que no existe en ningún dataset público.

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
4. **Qué se sube el 22.** Sin resolver en el chat: unos entendieron que solo el documento y otros que también la presentación y la demo. **Resuelto para este proyecto: el 22 se entrega el documento y la demo va a la exposición del 29.**

## Mapeo a los capítulos del documento

| Criterio de la rúbrica | Destino |
|---|---|
| User research | `chapter03.tex` §3.1 + `appendix/surveys.tex` (Anexo A) + `appendix/interviews.tex` (Anexo B) |
| Competencias (marketing) | `chapter03.tex` |
| Requerimientos y casos de uso | `chapter04.tex` |
| Arquitectura, diagramas y modelo de datos | `chapter04.tex` |
| Tecnologías | `chapter04.tex` |
| Mockups | `chapter04.tex` (figuras) |
| Demo | Presentación + capturas en `chapter04.tex` |
| Tabla comparativa | `chapter02.tex` (estado del arte) |

Al 2026-08-22 ambos capítulos están escritos: `chapter03.tex` con user research, competencia y modelo de negocio, y `chapter04.tex` con requerimientos, casos de uso, arquitectura, modelo de datos, tecnologías, restricciones legales y validación.

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
