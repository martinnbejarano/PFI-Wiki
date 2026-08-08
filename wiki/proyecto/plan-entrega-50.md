---
titulo: Plan de trabajo — Entrega 50% (22/08/2026)
tipo: proyecto
tags: [plan, entrega, 50, ep2, ruta-critica]
fuentes: [Rubrica-EP2-50porciento.pdf, notas-chat-pfi-2026.md]
actualizado: 2026-08-08
---

# Plan de trabajo — Entrega 50%

**Documento: sábado 22/08/2026. Exposición: sábado 29/08/2026.** Quedan 14 días.

## Diagnóstico de partida

De los ocho criterios de la rúbrica ([[wiki/proyecto/entrega-50-alcance]]), dos están cumplidos (tabla comparativa del estado del arte; FODA y Cruz de Porter para el criterio de competencias) y seis están en cero. No hay código. La encuesta lleva 7 respuestas. El análisis financiero **queda fuera**: en clase aclararon que la parte económica no entra.

La restricción real no es el tiempo de escritura sino el **orden de dependencias**: de los casos de uso salen los mockups, los diagramas y el modelo de datos. Empezar por cualquier otro lado obliga a rehacer.

## Principio de priorización

Se prioriza lo que la rúbrica puntúa. El user research no figura entre los ocho criterios —solo se pidió en clase—, así que se trabaja en paralelo y con el volumen que se consiga, sin robarle tiempo a los criterios evaluados.

---

## Bloque 0 — Hoy y mañana (8-9/08): destrabar lo que depende de terceros

Lo único que no se puede acelerar después. Tres acciones cortas:

1. **Reactivar la encuesta.** Republicar en el grupo del curso ofreciendo intercambio de respuestas —es la mecánica establecida ahí— más LinkedIn, X y red personal. Meta realista a 10 días: 50-80 respuestas. Registrar el número final y declararlo con honestidad en el documento; una muestra de 50 bien analizada y con su limitación explicitada vale más que una grande sin trazabilidad.
2. **Mandar los pedidos de entrevista.** Chequeado por su canal institucional, periodistas por LinkedIn, académicos de UBA/CONICET que trabajen desinformación. Apuntar a 3 para quedarse con 2. Es lo que más tarda en responder.
3. **Preguntar al tutor por escrito** las dos cosas que el chat dejó sin resolver: si el 22 se sube solo el documento o también la presentación y la demo, y si la demo es obligatoria para esta instancia.

## Bloque 1 — 10 al 13/08: requerimientos (criterio 1)

El núcleo del que se derivan tres criterios más.

- Requerimientos funcionales y no funcionales, con ID, descripción y prioridad. Los no funcionales salen casi solos de lo ya decidido: latencia del análisis, F1 macro objetivo, privacidad y LPDP, compatibilidad con Chrome de escritorio.
- 5 a 8 casos de uso desarrollados: analizar un tuit, ver la evidencia, consultar el histórico, reportar un falso positivo, instalar y configurar la extensión.
- Diagrama de casos de uso.
- Destino: `wiki/solucion/requerimientos.md` → `chapter04.tex`.

## Bloque 2 — 14 al 16/08: diseño (criterios 2, 3 y 6)

Los tres se apoyan en el bloque anterior y en la metodología técnica de 4 módulos, que ya está escrita.

- **Mockups**: popup de la extensión sobre un tuit con el badge de score, panel de evidencia con las fuentes que corroboran o contradicen, y el dashboard web con el histórico. Tres o cuatro pantallas alcanzan; lo que se evalúa es que sean claras y significativas.
- **Diagramas**: de componentes (los 4 módulos y sus interfaces), de flujo de información (del tuit al veredicto), y de secuencia del análisis end-to-end.
- **Modelo de datos**: diagrama entidad-relación de la base y diagrama de arquitectura del despliegue.
- Destino: `wiki/solucion/arquitectura.md` → `chapter04.tex`.

## Bloque 3 — 17 al 18/08: tecnologías y demo (criterios 5 y 7)

- **Tecnologías**: es en buena medida un traslado. `proyecto/recursos.md` ya justifica Railway, Vercel, Hugging Face y Tavily con alternativas evaluadas. Falta la justificación de los lenguajes y la **arquitectura de red**, que la rúbrica pide explícitamente y hoy no está en ninguna parte.
- **Demo**: un *vertical slice*, no el MVP. Un endpoint FastAPI que carga XLM-T desde Hugging Face y clasifica un texto, más una extensión mínima que lee el texto de un tuit del DOM y muestra el score. Es alcanzable en dos días y produce capturas reales de funcionalidad, que es lo que pide el criterio ("indicios de avance en la implementación"). Documentar con capturas comentadas.

## Bloque 4 — 19 al 21/08: escritura

- **`chapter03.tex`**: user research con los datos que haya —muestra, análisis por bloque de preguntas, gráficos propios sin capturas del formulario, entrevistas y user personas— más el análisis de competencia con las herramientas de marketing del criterio 4. FODA y Cruz de Porter ya están en `negocio/modelo-de-negocio`; conviene sumar una tercera herramienta.
- **`chapter04.tex`**: requerimientos, casos de uso, arquitectura, diagramas, modelo de datos, tecnologías y las capturas de la demo.
- **Anexos**: descomentar `surveys.tex` e `interviews.tex` en `annex.tex`. Las transcripciones van completas y **sin pasar por un LLM** — en clase avisaron que se detecta.

## 22/08 — Cierre

Compilar (`pdflatex main` → `biber main` → `pdflatex main`), correr el checklist de entrega de `CLAUDE.md`, verificar que no queden `Completar.` ni `\Fidel{}`/`\Martin{}` sin resolver, y subir.

## 23 al 28/08 — Presentación

20 minutos, mitad orientada a negocio y mitad a público técnico. La demo puede ir en vivo, como capturas comentadas o en video.

---

## Fuera de alcance de esta entrega

- Análisis financiero (VAN, TIR, payback): la parte económica no entra.
- Decisión definitiva del modelo y reescritura del pipeline de preprocesamiento: corresponden a la Entrega 4. Para la demo alcanza con usar XLM-T tal como viene, sin *fine-tuning*. Ver [[wiki/sintesis/decisiones-pendientes-2026-08]].
- Construcción del corpus argentino.

## Riesgos

| Riesgo | Mitigación |
|---|---|
| La demo no llega | Reducir el alcance a un notebook con el modelo clasificando ejemplos reales y capturas comentadas. Sigue cumpliendo "indicios de avance". |
| No se consiguen entrevistas | Plan B ya previsto en [[wiki/investigacion/user-research]]: 2 *power-users* del segmento primario con guía adaptada. |
| La encuesta queda con muestra chica | Declararla como tal y apoyar las conclusiones en las entrevistas. Una muestra chica bien analizada es defendible; una inventada es fraude académico y anula la entrega. |
| Los bloques 2 y 3 se solapan y no cierran | El criterio 7 (demo) es el más sacrificable: es el único que la cátedra dijo que estaba revisando por ser injusto entre comisiones. |

## Referencias cruzadas

- [[wiki/proyecto/entrega-50-alcance]]
- [[wiki/proyecto/cronograma]]
- [[wiki/solucion/requerimientos]]
- [[wiki/solucion/arquitectura]]
- [[wiki/solucion/tecnologias]]
- [[wiki/investigacion/user-research]]
- [[wiki/sintesis/decisiones-pendientes-2026-08]]
