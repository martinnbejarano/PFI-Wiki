---
titulo: Metodología de Desarrollo
tipo: proyecto
tags: [metodologia, kanban, gestion, herramientas]
fuentes: []
actualizado: 2026-08-19
---

# Metodología de Desarrollo

## Enfoque: Kanban

El proyecto se organiza con **Kanban**: un flujo continuo de tareas tiradas por la demanda, con un límite de trabajo en curso, sin iteraciones de duración fija.

La elección es descriptiva y no aspiracional: es literalmente cómo se viene trabajando desde abril. Dos razones la sostienen.

1. **El equipo es de una persona.** Las ceremonias de Scrum (planificación, revisión, retrospectiva, reunión diaria) existen para sincronizar a varios integrantes. Con un solo integrante son un ritual sin interlocutor.
2. **La cadencia la imponen hitos externos.** El ritmo del año lo fijan las cinco instancias de evaluación de la cátedra, que están separadas por entre seis y ocho semanas y tienen alcance heterogéneo. Un *sprint* de dos semanas no se alinea con ninguna de ellas.

Se evaluó declarar Scrum y se descartó. No hubo *sprints* de duración fija ni ceremonias, y declararlos habría producido una sección de metodología que no describe el trabajo real.

Lo que sí se toma de la práctica ágil es el principio de fondo: alcance ajustable contra fecha fija. Cada entrega parcial es un punto de revisión donde se recorta o se amplía lo que sigue según lo que se logró y según la devolución recibida.

## Planificación y priorización

- **Requerimientos priorizados con MoSCoW.** Los 16 requerimientos funcionales están clasificados en imprescindibles, importantes y deseables (ver [[requerimientos]]). La prioridad determina el orden de implementación y, sobre todo, qué se sacrifica primero si el tiempo aprieta.
- **Tablero de *issues* en GitHub.** Cada unidad de trabajo es un *issue* del repositorio. Las columnas del tablero son los estados del flujo; las etiquetas de triage (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`) marcan en qué punto está cada uno. Ver [[docs/agents/triage-labels]].
- **Límite de trabajo en curso.** Un bloque de trabajo por vez. La regla práctica es no abrir un frente nuevo mientras haya uno abierto que se pueda cerrar.

## Dinámica de trabajo

El ciclo tiene tres pasos y se repite por tema, no por calendario:

1. **Relevamiento.** Las fuentes originales (papers, artículos, material de cátedra, fichas de datasets) se archivan sin modificar en `raw/`.
2. **Síntesis.** Cada fuente se procesa en una o varias páginas del wiki, que es el espacio exploratorio: acepta borradores, marcas de contradicción y afirmaciones sin verificar.
3. **Consolidación.** Cuando una sección del wiki está madura, se vuelca al documento LaTeX con tono académico y citas verificadas.

La separación entre wiki y documento es deliberada: evita que el documento final arrastre material provisorio y permite que la investigación avance sin la fricción de la redacción formal.

## Herramientas

| Herramienta | Función |
|---|---|
| git y GitHub | Control de versiones del documento, del wiki y de las fuentes |
| GitHub Issues | Gestión de tareas sobre el tablero Kanban |
| LaTeX con biber | Redacción del documento final y gestión de la bibliografía |

El repositorio es único: fuentes, wiki y documento viven juntos y versionados. Un cambio en una página del wiki y el volcado correspondiente al documento quedan en el mismo historial, lo que hace trazable de dónde salió cada afirmación del documento final.

## Criterio de terminado

Se aplica en dos niveles, porque wiki y documento tienen estándares distintos.

**Una página del wiki está terminada cuando:**
- cita las fuentes de las que salió cada afirmación;
- no contiene marcadores de pendiente;
- está enlazada desde [[index]] y desde al menos otra página;
- las contradicciones con páginas existentes están marcadas de forma explícita.

**Una sección del documento está terminada cuando:**
- la prosa cumple las convenciones de escritura académica del proyecto;
- toda cita del texto existe en `biblio.bib`;
- compila sin referencias ni citas sin resolver y sin advertencias de biber;
- no quedan marcadores `Completar.` ni notas de trabajo sin resolver.

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
