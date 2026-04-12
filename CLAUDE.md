****# CLAUDE.md — Esquema del Wiki PFI

Este archivo define cómo funciona este wiki y cómo debo (Claude) operarlo. Es el documento de configuración central. Debo leerlo al inicio de cada sesión.

---

## Contexto del proyecto

**Materia:** Proyecto Final de Ingeniería en Informática (PFI)
**Universidad:** UADE — Facultad de Ingeniería y Ciencias Exactas
**Año:** 2026
**Tutor:** Monzón, Nicolás Alberto
**Tipo de proyecto:** Desarrollo (producto y/o proceso novedoso)
**Idioma del wiki:** Español

**Tema del proyecto:** [POR DEFINIR — actualizar cuando se elija]
**Integrantes:** [POR DEFINIR]

---

## Estructura del repositorio

```
PFI-Wiki/
├── CLAUDE.md           ← este archivo (esquema y reglas)
├── index.md            ← índice de contenido (actualizar en cada ingestión)
├── log.md              ← log cronológico (append-only)
├── raw/                ← fuentes originales (NUNCA modificar)
│   ├── assets/         ← imágenes descargadas localmente
│   └── [fuentes...]    ← PDFs, artículos en markdown, notas
└── wiki/               ← páginas del wiki (yo las escribo y mantengo)
    ├── 00-resumen.md   ← visión general del PFI (página central)
    ├── proyecto/       ← gestión y seguimiento del PFI
    ├── marco-teorico/  ← conceptos teóricos del dominio
    ├── estado-del-arte/← análisis de papers y literatura
    ├── competencia/    ← análisis competitivo de soluciones existentes
    ├── solucion/       ← la solución técnica que se construye
    ├── investigacion/  ← user research, entrevistas, encuestas
    ├── negocio/        ← modelo de negocio y análisis financiero
    └── sintesis/       ← análisis cross-cutting, insights, comparaciones
```

---

## Capas del sistema

**`raw/`** — Fuentes originales. Inmutables. Nunca las modifico. Son la fuente de verdad.
Tipos: PDFs de papers, artículos clipeados en markdown, transcripciones de entrevistas, notas de clase, slides de la cátedra, datos financieros.

**`wiki/`** — Páginas generadas y mantenidas por mí. Sumarios, páginas de entidades/conceptos, análisis, síntesis. El usuario las lee; yo las escribo.

**`index.md`** — Catálogo de todo lo que hay en el wiki. Organizado por categoría. Lo actualizo en cada operación que agrega o modifica páginas.

**`log.md`** — Registro cronológico append-only. Cada entrada tiene el prefijo `## [YYYY-MM-DD] tipo | descripción` para ser parseable.

---

## Estructura de una página del wiki

Cada página debe tener:

```markdown
---
titulo: Nombre de la página
tipo: concepto | entidad | fuente | análisis | proyecto
tags: [tag1, tag2]
fuentes: [nombre-fuente-1.md, nombre-fuente-2.md]
actualizado: YYYY-MM-DD
---

# Título

Contenido...

## Referencias cruzadas
- [[página relacionada 1]]
- [[página relacionada 2]]

## Fuentes
- [[raw/nombre-fuente.pdf]]
```

---

## Operaciones

### 1. Ingestión de fuente

Cuando el usuario agrega una fuente nueva a `raw/`:

1. Leer la fuente completa
2. Discutir con el usuario los puntos clave si es pertinente
3. Crear una página de resumen en la sección correspondiente del wiki
4. Actualizar o crear páginas de conceptos/entidades afectadas (pueden ser 5-15 páginas)
5. Notar contradicciones con lo ya existente en el wiki
6. Actualizar `index.md`
7. Agregar entrada al `log.md`: `## [fecha] ingest | Título de la fuente`

Secciones donde alojar resúmenes de fuentes según tipo:
- Paper académico / artículo → `wiki/estado-del-arte/`
- Material de cátedra / slides → `wiki/proyecto/`
- Entrevista / encuesta → `wiki/investigacion/`
- Análisis de competidor → `wiki/competencia/`
- Documento técnico / arquitectura → `wiki/solucion/`

### 2. Consulta

Cuando el usuario hace una pregunta:

1. Leer `index.md` para identificar páginas relevantes
2. Leer las páginas relevantes
3. Sintetizar la respuesta con citas a las páginas del wiki
4. Si la respuesta es valiosa (un análisis, comparación, conclusión nueva), **archivarla como página nueva** en `wiki/sintesis/`
5. Agregar entrada al `log.md`: `## [fecha] query | Pregunta resumida`

### 3. Lint

Cuando el usuario pide un health-check del wiki:

1. Buscar contradicciones entre páginas
2. Identificar páginas huérfanas (sin links entrantes)
3. Identificar conceptos mencionados pero sin página propia
4. Identificar afirmaciones desactualizadas por fuentes nuevas
5. Sugerir nuevas fuentes a buscar o preguntas a investigar
6. Agregar entrada al `log.md`: `## [fecha] lint | Resumen del lint`

---

## Taxonomía del PFI

El PFI en UADE Informática sigue esta estructura en el documento final. El wiki debe cubrir todos estos módulos:

| Módulo PFI | Sección del wiki |
|---|---|
| Introducción (objetivo, alcance) | `wiki/proyecto/propuesta.md` |
| Marco Teórico | `wiki/marco-teorico/` |
| Estado del Arte | `wiki/estado-del-arte/` |
| Análisis de Competencia | `wiki/competencia/` |
| User Research | `wiki/investigacion/` |
| Requerimientos + Casos de Uso | `wiki/solucion/requerimientos.md` |
| Arquitectura | `wiki/solucion/arquitectura.md` |
| Tecnologías | `wiki/solucion/tecnologias.md` |
| Modelo de Negocio | `wiki/negocio/` |
| Análisis Financiero | `wiki/negocio/analisis-financiero.md` |
| Metodología de Desarrollo | `wiki/proyecto/metodologia.md` |
| Pruebas | `wiki/solucion/pruebas.md` |

---

## Convenciones

- **Idioma:** Todo el wiki en español. Las fuentes en inglés se resumen en español.
- **Links:** Usar sintaxis Obsidian `[[nombre-de-pagina]]` para links internos.
- **Fechas:** Formato `YYYY-MM-DD`.
- **Citas:** Citar siempre la fuente de donde viene una afirmación.
- **Contradicciones:** Marcar explícitamente con `> ⚠️ CONTRADICCION: esta afirmación contradice [[página X]]`.
- **Sin verificar:** Marcar afirmaciones no verificadas con `[sin verificar]`.
- **Borradores:** Páginas incompletas llevan tag `borrador` en el frontmatter.

---

## Entregas del PFI (cronograma tentativo UADE 2026)

Las fechas exactas se actualizan cuando el usuario las confirme.

| Entrega | Contenido aproximado |
|---|---|
| Presentación Preliminar 1 | Propuesta de tema, objetivo, alcance |
| Presentación Preliminar 2 | Marco teórico, estado del arte, competencia |
| Presentación Preliminar 3 | Solución completa, arquitectura, diseño |
| Entrega Final | Documento completo + producto funcional |

Ver `wiki/proyecto/cronograma.md` para fechas confirmadas.

---

## Notas del tutor

Tutor: **Monzón, Nicolás Alberto** (UADE + UdelaR).
Ha dirigido PFIs de tipo Desarrollo con énfasis en validación real (MVP probado con usuarios reales, no solo mocks).
Ver `wiki/proyecto/reuniones.md` para notas de reuniones.
