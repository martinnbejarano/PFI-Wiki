---
titulo: Entrega del 90 % — alcance, estado y plan de acción
tipo: proyecto
tags: [entrega, e75, e90, rubrica, plan]
fuentes: [Pautas-E75-Monzon-2026.pdf, Rubrica-PFI-2026-v1.3.xlsx, Cronograma-PFI-Informatica-2026.pdf, GR_M15_Feresini_Imbriago-EntregaFinal2025.pdf]
actualizado: 2026-09-28
---

# Entrega del 90 % — alcance, estado y plan de acción

La cátedra la llama Entrega Preliminar 3 (75 %). **Para defender en diciembre, el avance tiene que ser del 90 %**, y ese es el camino elegido. En la práctica, se entrega el informe final: el evaluador externo lo corrige con la rúbrica del 100 %, y la fecha de defensa se fija después de su devolución.

## Fechas (cronograma oficial 2026)

| Hito | Fecha |
|---|---|
| **Entrega del documento al 90 %** | **sábado 24/10/2026, 23:59** |
| Exposición de avance (10 a 15 min, con demo) | 24/10, 31/10 o 7/11. La presentación se sube el día anterior |
| Feedback y consultas | 14/11 |
| Recuperatorio del 75 % / 90 % | 28/11 |
| Defensas, llamado regular | 9/12 al 14/12 |

La entrega la envía el tutor, así que la fecha real de corte es **antes del 24/10**, la que acuerde Fidel.

## Qué acompaña al documento

1. **Tres videos de 5 minutos** que explican la tesis.
2. Un **informe de avance**.
3. La **rúbrica del 75 % como autoevaluación**, que completa y avala el tutor.
4. Una **demo productiva**: el proyecto aplicado a un escenario real, y documentado.

## Qué exige el documento (novedades del 75 %)

- Marco normativo dentro del Marco Teórico.
- Metodología de desarrollo con su estructura oficial: *Metodología* / *Arquitectura y tecnologías utilizadas* / *Validación del sistema*. Se cierra al final.
- Los aspectos legales, si son extensos, van en una sección propia.
- Resumen, Abstract (traducción del Resumen) y capítulo de Conclusiones generales.
- Siguen vigentes todas las exigencias del 25 % y del 50 %, más la lista de formato y redacción de las pautas (unas 90 viñetas; ver la fuente).

## Estado frente a la rúbrica del 100 %

Leyenda: ✅ se cumple · 🟡 parcial · 🔴 falta.

| Solapa (pts) | Criterio | Estado | Qué falta |
|---|---|---|---|
| Calidad técnica (25) | Modelo de datos y arquitectura | ✅ | Pasar la arquitectura a calidad «nivel AWS» si no lo es |
| | Justificación tecnológica | ✅ | — |
| | Tendencias en informática | 🟡 | Hoy toda la inferencia es un LLM de terceros. La pauta dice que **no puede ser solo un *wrapper* de un LLM**: hace falta el clasificador propio entrenado |
| | Producto entregado | 🟡 | Los objetivos específicos prometen un módulo de credibilidad (pesa 0) y un clasificador propio. Implementarlos o recortar los objetivos |
| | Uso de datasets | 🟡 | Documentado, pero sin usar: se usa recién cuando haya entrenamiento. Declarar el corpus propio como fuente primaria |
| Formalidades (20) | Estructura | 🔴 | Reordenar el cap. 4 en tres secciones, sacar lo legal a una sección propia, agregar el marco normativo, Conclusiones, Resumen y Abstract |
| | Formato, índice, redacción, idioma | 🟡 | Pasada completa contra la lista de las pautas: *Title Case* en títulos, «no debe» en requerimientos, lenguaje de trabajo en progreso («Trabajo previsto», «Alcance diferido», «Decisiones diferidas»), menciones a entregas |
| | Citas y bibliografía | 🟡 | Las pautas prohíben citar páginas web y documentación de *vendors*; hay 14 entradas `@online` que revisar. Pasar los *preprints* de arXiv a su versión publicada |
| | Hilo conductor | ✅ | Revisar después de reestructurar |
| Desarrollo funcional (15) | Requerimientos, diagramas, mockups, metodología | ✅ | Diagramas UML con sintaxis estándar completa |
| | **Pruebas funcionales** | 🔴 | Hay 61 tests del servicio (cobertura 88 %) y 16 de la extensión (cobertura sin medir). **Faltan las pruebas con usuarios** (usabilidad) |
| | **Resultados de las pruebas** | 🔴 | No hay resultados ni decisiones tomadas a partir de ellos. La validación del sistema está escrita como protocolo, sin números |
| Investigación (30) | Marco teórico | 🟡 | Falta el marco normativo |
| | Estado del arte y conclusión | ✅ | La pauta pide la competencia *dentro* del Estado del Arte; hoy está en el cap. 3 (ver contradicción) |
| | **User research** | 🔴 | **Encuesta: 140 respuestas; el mínimo nuevo es 160.** **Entrevistas: 2; se esperan 5**, 3 como mínimo si se combina con encuesta. **Personas: 2; se piden 3**, y en formato gráfico |
| | Viabilidad legal | ✅ | Hay un análisis extenso; pasarlo a sección propia |
| | Viabilidad técnica | ✅ | No aplica (no hay hardware) |
| | Dominio conceptual | ✅ | — |
| | **Conclusiones generales** | 🔴 | El capítulo no existe (`conclusion.tex` tiene «Completar.») |
| Negocio (10) | Modelo de negocio | ✅ | — |
| | **Viabilidad económico-financiera** | 🔴 | `analisis-financiero.md` es una plantilla vacía. Se piden dos escenarios (optimista y pesimista) y VAN, TIR o *payback* |
| | **Branding y logotipo** | 🔴 | No hay nombre ni logo: la extensión se llama «Detector de desinformación — prototipo» |

Además, fuera de la rúbrica pero en las pautas:

- **Mitigación de *prompt injection*** (se le pasa el texto del tuit a un LLM): no está documentada.
- **Proceso de entrenamiento documentado** (variables y métricas), si se usa ML.
- **Escenario real:** hoy el servicio corre en local. Hay que desplegarlo y publicar la extensión, aunque sea sin listar.

> ⚠️ CONTRADICCION: las pautas del 75 % dicen «Competencia dentro del Estado del Arte», pero el template y el mapa de `CLAUDE.md` ponen el análisis competitivo en el cap. 3 (Descripción), y así se aprobó el 50 %. Consultar a Fidel antes de mover algo.

## Riesgos

1. **El clasificador propio es la ruta crítica.** Sin él, el producto es un *wrapper* de un LLM (criterio eliminatorio de las pautas), la validación no tiene números y las conclusiones no tienen de qué concluir. Salida mínima viable: *fine-tuning* de XLM-T o BETO sobre FakeDeS, que ya está en español y etiquetado, con la línea base TF-IDF + regresión logística. Es trabajo de días en Colab, no de semanas. El corpus argentino anotado a mano (300 a 500 casos) va solo como test real, y si no llega se recorta.
2. **El trabajo de campo depende de terceros**: 20 respuestas más a la encuesta, 3 entrevistas y usuarios para la prueba de usabilidad. Hay que arrancarlo esta semana.
3. **El tutor envía la entrega**: su fecha de corte y la autoevaluación restan días al plan.

## Plan de acción (28/09 → 24/10)

### Semana 1 · 28/09 a 04/10 — arrancar lo que depende de otros

- [ ] Preguntar a Fidel su fecha de corte, cómo quiere la autoevaluación y lo de la competencia dentro del Estado del Arte.
- [ ] Reabrir la encuesta hasta pasar las 160 respuestas.
- [ ] Coordinar 3 entrevistas nuevas. Prioridad: una organización de verificación (pendiente desde el 50 %), un usuario del segmento y alguien de un medio socio de ADEPA.
- [ ] Clasificador: preparar FakeDeS, entrenar la línea base TF-IDF + LR y lanzar el primer *fine-tuning*.
- [ ] Nombre del producto y logo (hay clase de modelo de negocio el 03/10).

### Semana 2 · 05/10 a 11/10 — cerrar el producto

- [ ] Integrar el clasificador al servicio en reemplazo del puntaje del LLM, con métricas contra la línea base.
- [ ] Decidir el módulo 2 (credibilidad): implementar las señales públicas mínimas o recortarlo de los objetivos.
- [ ] Mitigación de *prompt injection*, implementada y documentada.
- [ ] Desplegar el servicio y publicar la extensión (escenario real).
- [ ] Análisis financiero: supuestos, costos, dos escenarios, VAN, TIR y *payback*.

### Semana 3 · 12/10 a 18/10 — validar y escribir

- [ ] Prueba de usabilidad con 5 a 8 usuarios (tareas + cuestionario SUS) y registro de los resultados.
- [ ] Validación del sistema con números: métricas del clasificador y del sistema completo sobre el test real.
- [ ] Reestructurar el documento: el cap. 4 en tres secciones, lo legal en sección propia y el marco normativo en el Marco Teórico.
- [ ] Volcar las entrevistas nuevas (un anexo por entrevista), la tercera persona y la encuesta actualizada.
- [ ] Conclusiones generales atadas a cada objetivo específico, y después Resumen y Abstract.

### Semana 4 · 19/10 a 24/10 — pulir y entregar

- [ ] Pasada de formato y redacción contra la lista completa de las pautas.
- [ ] Bibliografía: sacar las citas web y de *vendors*, pasar los *preprints* a su versión publicada y cargar las claves del trabajo futuro (FActScore, ProgramFC y ClaimDecomp).
- [ ] Grabar los 3 videos de 5 minutos.
- [ ] Informe de avance y autoevaluación con la rúbrica.
- [ ] Deck y guion de 10 a 15 minutos con demo, aplicando lo pendiente del feedback del 50 %.
- [ ] Compilar, checklist de entrega y enviar al tutor.

## Referencias cruzadas

- [[wiki/proyecto/cronograma]]
- [[wiki/proyecto/entrega-50-alcance]]
- [[wiki/proyecto/calibracion-tesis-referencia]]
- [[wiki/presentacion/e50/analisis-feedback]]
- [[wiki/negocio/analisis-financiero]]
- [[wiki/solucion/pruebas]]

## Fuentes

- [[raw/clases/Pautas-E75-Monzon-2026.pdf]]
- [[raw/clases/Rubrica-PFI-2026-v1.3.xlsx]]
- [[raw/clases/Cronograma-PFI-Informatica-2026.pdf]]
