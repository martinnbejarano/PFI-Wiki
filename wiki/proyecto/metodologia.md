---
titulo: Metodología de Desarrollo
tipo: proyecto
tags: [metodologia, kanban, gestion, herramientas, ci, definicion-de-terminado]
fuentes: []
actualizado: 2026-10-20
---

# Metodología de Desarrollo

## Enfoque: Kanban

El proyecto se organiza con **Kanban**: un flujo continuo de tareas tiradas por la demanda, con un límite de trabajo en curso, sin iteraciones de duración fija. Anderson (2010, `Anderson2010` en `biblio.bib`) lo define por un conjunto de propiedades centrales; las cuatro que se aplican acá son visualizar el flujo, limitar el trabajo en curso, gestionar el flujo y explicitar las políticas.

La elección es descriptiva y no aspiracional: es literalmente cómo se viene trabajando desde abril. Dos razones la sostienen.

1. **El equipo es de una persona.** Las ceremonias de Scrum (planificación, revisión, retrospectiva, reunión diaria) existen para sincronizar a varios integrantes. Con un solo integrante son un ritual sin interlocutor.
2. **La cadencia la imponen hitos externos.** El ritmo del año lo fijan las instancias de evaluación de la cátedra, separadas por entre seis y ocho semanas y de alcance heterogéneo. Un *sprint* de dos semanas no se alinea con ninguna de ellas.

Se evaluó declarar Scrum y se descartó. No hubo *sprints* ni ceremonias, y declararlos habría producido una sección de metodología que no describe el trabajo real. Lo que sí se toma de la práctica ágil es el principio de fondo: alcance ajustable contra fecha fija.

## Planificación y priorización

- **Requerimientos priorizados con MoSCoW** (ver [[requerimientos]]). La prioridad determina el orden de implementación y qué se sacrifica primero si el tiempo aprieta.
- **Tablero de *issues* en GitHub.** Cada unidad de trabajo es un *issue*; su estado se lee de las etiquetas de triage, la asignación y la PR asociada. Ver [[docs/agents/triage-labels]].

## Flujo de desarrollo del prototipo (flujo principal)

- **Unidad de trabajo: el *issue*.** Qué construir, criterios de aceptación verificables y «bloqueado por». Lo grande se parte en un *issue* de especificación + rebanadas verticales (ej.: #18 → #19–#26, ocho rebanadas para la demo del 50 %; #28 → #29–#36 para el clasificador).
- **Números (25/08 → 20/10/2026):** 20 *issues* de desarrollo del prototipo cerrados, 10 PR fusionadas que tocan `prototipo/` (de 15 en total) y 57 *commits* sobre `prototipo/`.
- **Rama por frente + PR a `main`.**
- **Pruebas primero:** son criterio de aceptación de cada *issue*. Servicio: 114 pruebas en pytest, 93 % de cobertura de sentencias (medido el 2026-10-20). Extensión: Vitest (23 pruebas, 3 omitidas), con la lectura del DOM de X contra *fixtures*. Ninguna batería usa red ni credencial: el puerto del proveedor se sustituye por un doble.
- **`make`:** `instalar`, `test`, `dev`, `desplegar` (Railway + `curl /salud`).
- **CI:** `.github/workflows/ci.yml` (GitHub Actions) en cada *push* y PR: job `servicio` (Python 3.13, pytest) y job `extension` (Node 24, `npm ci`, `tsc --noEmit`, `npm test`, `npm run build`). Primera corrida verde: https://github.com/martinnbejarano/PFI-Wiki/actions/runs/39430449153

| Estado | Señal en el repositorio |
|---|---|
| Por evaluar | `needs-triage` (o `needs-info` si falta información) |
| Listo | criterios de aceptación completos + etiqueta de listo para implementar |
| En curso | *issue* asignado, rama abierta (WIP = 1) |
| En revisión | PR abierta, CI corriendo |
| Terminado | PR fusionada, *issue* cerrado |
| Descartado | `wontfix` |

Cómo aparece cada propiedad de Kanban:
- **Visualizar** → el tablero se deriva de etiquetas, asignación y PR, sin registro aparte.
- **Limitar WIP** → un *issue* asignado por vez; no se abre un frente nuevo mientras haya uno que se pueda cerrar.
- **Gestionar el flujo** → rebanadas chicas y dependencias declaradas que ordenan qué pasa a «listo».
- **Políticas explícitas** → criterios de aceptación + definición de terminado, con la parte automatizable en la CI.

## Flujo de redacción del documento

Tres pasos que se repiten por tema, no por calendario:

1. **Relevamiento.** Las fuentes originales se archivan sin modificar en `raw/`.
2. **Síntesis.** Cada fuente se procesa en el wiki, que acepta borradores, contradicciones marcadas y afirmaciones sin verificar.
3. **Consolidación.** Lo maduro se vuelca al documento LaTeX con tono académico y citas verificadas.

Fuentes, wiki, documento y código viven en el mismo repositorio, así que una nota, su volcado y el cambio del prototipo que la motiva quedan en el mismo historial.

## Herramientas

| Herramienta | Función |
|---|---|
| git y GitHub | Control de versiones del código, del documento, del wiki y de las fuentes |
| GitHub Issues | Tablero Kanban: unidades de trabajo con criterios de aceptación |
| *Pull requests* de GitHub | Revisión e integración de cada cambio en `main` |
| GitHub Actions | CI: pruebas, verificación de tipos y build de la extensión |
| pytest y Vitest | Pruebas del servicio y de la extensión |
| GNU Make | Instalación, pruebas, ejecución local y despliegue |
| Asistente de programación con IA (Claude Code) | Asistencia en la implementación y en las pruebas |
| LaTeX con biber | Redacción del documento final y bibliografía |

## Definición de terminado

**Código del prototipo** (un *issue* está terminado cuando):
1. se verifican todos sus criterios de aceptación;
2. se agregaron o actualizaron las pruebas del cambio y las dos baterías pasan en la CI;
3. la extensión se construye y `tsc` no reporta fallas;
4. la PR fue revisada y aprobada por el autor antes de fusionarla;
5. si cambia el comportamiento, se actualizaron el wiki y `log.md`;
6. tras fusionar en `main`, se redesplegó (`make desplegar`) y `/salud` responde bien.

**Una página del wiki está terminada cuando:** cita sus fuentes, no tiene marcadores de pendiente, está enlazada desde [[index]] y desde al menos otra página, y marca sus contradicciones.

**Una sección del documento está terminada cuando:** cumple las convenciones de escritura, toda cita existe en `biblio.bib`, compila sin referencias ni citas sin resolver ni advertencias de biber, y no quedan `Completar.` ni notas sin resolver.

## Trabajo pendiente

| Frente | Entrega prevista |
|---|---|
| Investigación con usuarios: entrevistas, encuestas y perfiles de usuario | 4 |
| Implementación del prototipo: extensión, API y módulos de análisis | 4 |
| Construcción del corpus argentino y ajuste del clasificador | 4 y 5 |
| Experimentación, comparación contra la línea base y contra los modelos de contraste | 5 |
| Pruebas de usabilidad y validación con usuarios reales | 5 |
| Análisis financiero | 5 |

## Referencias cruzadas
- [[cronograma]]
- [[requerimientos]]
- [[pruebas]]
- [[plan-volcado-documento]]
