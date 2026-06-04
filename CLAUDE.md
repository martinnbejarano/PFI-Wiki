****# CLAUDE.md — Esquema del Wiki PFI

Este archivo define cómo funciona este wiki y cómo debo (Claude) operarlo. Es el documento de configuración central. Debo leerlo al inicio de cada sesión.

---

## Contexto del proyecto

**Materia:** Proyecto Final de Ingeniería en Informática (PFI)
**Universidad:** UADE — Facultad de Ingeniería y Ciencias Exactas
**Año:** 2026
**Tutor:** Giro Uribazo, Fidel Valentin (fgirouribazo@uade.edu.ar)
**Tipo de proyecto:** Desarrollo (producto y/o proceso novedoso)
**Idioma del wiki:** Español

**Tema del proyecto:** Sistema de Detección Automática de Desinformación en Redes Sociales y Medios Digitales
**Tema troncal:** Inteligencia Artificial
**Integrantes:** Juan Martín Bejarano Arce

---

## Estructura del repositorio

```
PFI-Wiki/
├── CLAUDE.md              ← este archivo (esquema y reglas)
├── index.md               ← índice de contenido (actualizar en cada ingestión)
├── log.md                 ← log cronológico (append-only)
│
├── raw/                   ← fuentes originales (NUNCA modificar)
│   ├── papers/            ← PDFs de papers académicos
│   ├── articulos/         ← artículos web clipeados en markdown
│   ├── implementaciones/  ← referencias de repos/código existente
│   ├── datasets/          ← fichas descriptivas de datasets
│   ├── clases/            ← material de la cátedra PFI
│   └── assets/            ← imágenes descargadas localmente
│
├── documento/             ← documento final en LaTeX (template oficial UADE)
│   ├── main.tex           ← punto de entrada; incluye todos los capítulos
│   ├── biblio.bib         ← bibliografía BibTeX (fuente única de citas del documento)
│   ├── history.tex        ← bitácora interna (compilar con `pdflatex history`)
│   ├── history/           ← entradas de bitácora y convenciones LaTeX
│   └── chapters/          ← un .tex por capítulo del documento final
│
└── wiki/                  ← páginas del wiki (yo las escribo y mantengo)
    ├── 00-resumen.md      ← visión general del PFI (página central)
    │
    │   — DOCUMENTO PFI —
    ├── proyecto/          ← gestión: propuesta, cronograma, reuniones, metodología
    ├── marco-teorico/     ← conceptos teóricos del dominio (desinformación, NLP, etc.)
    ├── estado-del-arte/   ← síntesis de papers y literatura académica
    ├── competencia/       ← análisis competitivo de soluciones existentes
    ├── investigacion/     ← user research, entrevistas, encuestas, personas
    ├── negocio/           ← modelo de negocio y análisis financiero
    │
    │   — DESARROLLO —
    ├── implementaciones/  ← análisis de sistemas similares (repos, papers con código)
    ├── datasets/          ← datasets disponibles, comparación, elección
    ├── modelos/           ← modelos de ML considerados y evaluados
    ├── experimentos/      ← resultados de experimentos, benchmarks, ablaciones
    ├── solucion/          ← la solución que se construye (req, arquitectura, tech, pruebas)
    │
    └── sintesis/          ← análisis cross-cutting, insights, comparaciones
```

---

## Capas del sistema

**`raw/`** — Fuentes originales. Inmutables. Nunca las modifico. Son la fuente de verdad.
- `raw/papers/` — PDFs de papers académicos (IEEE, arXiv, ACL, etc.)
- `raw/articulos/` — artículos web en markdown (Obsidian Web Clipper)
- `raw/implementaciones/` — notas sobre repos y código de referencia
- `raw/datasets/` — fichas de datasets (LIAR, FakeNewsNet, etc.)
- `raw/clases/` — material de la cátedra PFI (slides, cronograma, pautas)
- `raw/assets/` — imágenes descargadas localmente

**`wiki/`** — Páginas generadas y mantenidas por mí. Sumarios, páginas de entidades/conceptos, análisis, síntesis. El usuario las lee; yo las escribo.

**`index.md`** — Catálogo de todo lo que hay en el wiki. Organizado por categoría. Lo actualizo en cada operación que agrega o modifica páginas.

**`log.md`** — Registro cronológico append-only. Cada entrada tiene el prefijo `## [YYYY-MM-DD] tipo | descripción` para ser parseable.

**`documento/`** — Documento final en LaTeX. Template oficial UADE. Se compila con:
```
cd documento && pdflatex main && biber main && pdflatex main
```
La bitácora interna se compila por separado: `pdflatex history`

---

## Documento LaTeX — Estructura y flujo

### Capítulos del documento

| Archivo | Contenido |
|---|---|
| `chapters/chapter01.tex` | Introducción (objetivos, alcance) |
| `chapters/chapter02.tex` | Antecedentes (marco teórico + estado del arte) |
| `chapters/chapter03.tex` | Descripción (user research, competencia, negocio) |
| `chapters/chapter04.tex` | Metodología de desarrollo (datasets, arquitectura, tecnologías, validación) |
| `chapters/conclusion.tex` | Conclusión |
| `chapters/appendix/` | Anexos: cronograma, encuestas, entrevistas |

### Macros de anotación

- `\Fidel{texto}` — nota inline del tutor Giro Uribazo (verde). Usar cuando el tutor deja feedback.
- `\Martin{texto}` — nota inline propia (azul). Para dudas o recordatorios personales.
- `\pdfcomment{texto}` — comentario visible en el PDF.

### biblio.bib — fuente única de citas

`documento/biblio.bib` es la fuente autoritativa de todas las referencias del documento final.
Cuando el wiki cita un paper, esa misma clave debe existir (o agregarse) en `biblio.bib`.
Formato: `Apellido, Nombre` en autores; dobles llaves en títulos; DOI como campo propio.

### history/ — bitácora interna

`documento/history/` es un documento separado (no va en la entrega). Contiene:
- `considerations.tex` — convenciones LaTeX y decisiones del documento
- `01.tex`, `02.tex`, ... — entradas cronológicas de avance y decisiones importantes

Compilar con `pdflatex history` desde `documento/`.

### Antes de cada entrega final

- Cambiar referencias de rojo a negro: comentar bloque `colorlinks` en `main.tex`, descomentar `hidelinks`
- Quitar cronograma del anexo
- Redactar Resumen y Abstract
- Generar carátula oficial desde la biblioteca UADE
- Verificar warnings de biber

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
- Paper académico (teórico) → `wiki/estado-del-arte/`
- Paper académico (con implementación) → `wiki/implementaciones/`
- Artículo web → `wiki/estado-del-arte/` o `wiki/implementaciones/` según contenido
- Material de cátedra / slides → `wiki/proyecto/`
- Entrevista / encuesta → `wiki/investigacion/`
- Análisis de competidor → `wiki/competencia/`
- Dataset → `wiki/datasets/`
- Experimento / benchmark → `wiki/experimentos/`
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

## Git Workflow — Commits automáticos

**Regla de oro:** Cada vez que escribo código o contenido en el wiki, se hace commit automático.

### Cuándo commitear

✅ **SIEMPRE commitear:**
- Crear página nueva en `wiki/`
- Modificar página existente en `wiki/`
- Actualizar `index.md` (índice)
- Actualizar `log.md` (registro cronológico)
- Cambios en `wiki/solucion/` (arquitectura, implementación)
- Cambios en `wiki/datasets/` (datasets, metodología)

❌ **NO commitear:**
- `.obsidian/` (configuración local del editor)
- `.DS_Store` (archivos del sistema macOS)
- Directorios `raw/` que sean ejemplos o templates sin usar
- Archivos temporales

### Formato de commit

```
git commit -m "$(cat <<'EOF'
[Título descriptivo en imperative — máx 70 caracteres]

[Descripción del cambio en 1-3 párrafos si es necesario]

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
EOF
)"
```

**Ejemplo:**
```
Agregar restricciones legales, datasets y pipeline de preprocesamiento

- wiki/proyecto/restricciones-legales-eticas.md: análisis LPDP, ToS, compliance
- wiki/datasets/dataset-recomendacion.md: LIAR, FakeNewsNet, validación argentina
- wiki/solucion/pipeline-preprocesamiento.md: limpieza, normalización, BETO
- Actualizar propuesta.md con arquitectura de 4 módulos
- Completar análisis competitivo (tabla, océano azul, matriz ERIC)

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
```

### Branch workflow

- **Branch principal:** `main` (estable, listo para presentaciones)
- **Branches de trabajo:** `feat/*` para features, `fix/*` para correcciones
- **Merging:** Cuando el usuario da OK o una sección está completa

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

## Dominio del proyecto: Detección de Desinformación

El proyecto construye un sistema de detección automática de desinformación en redes sociales. Esto involucra:

**Conceptos clave del dominio:**
- Desinformación, misinformación, fake news — distinciones y taxonomías
- Detección de desinformación: enfoques basados en contenido, fuente, propagación, contexto
- NLP para clasificación de texto: BERT, RoBERTa, LLMs para clasificación
- Graph-based detection: propagación viral, redes de difusión
- Fact-checking automático y semi-automático

**Datasets relevantes a explorar:**
- LIAR dataset (politifact.com, 12.8k claims)
- FakeNewsNet (GossipCop + PolitiFact con contenido social)
- CREDBANK (tweets sobre eventos de noticias)
- MultiFC (multi-dominio, multi-clase)
- Otros específicos para español / contexto latinoamericano

**Tipos de modelos a explorar:**
- Clasificadores de texto (BERT, RoBERTa, XLNet)
- Modelos multimodales (texto + metadatos + grafos de propagación)
- LLMs para zero-shot y few-shot detection
- Enfoques de ensemble

**Redes sociales objetivo:** Twitter/X, Instagram, Facebook, Infobae, Clarín

**Métricas de evaluación:**
- Accuracy, Precision, Recall, F1
- AUC-ROC
- Comparación con baselines (TF-IDF + LR, etc.)

## Notas del tutor

Tutor: **Giro Uribazo, Fidel Valentin** (UADE, interno).
Email: fgirouribazo@uade.edu.ar
Ver `wiki/proyecto/reuniones.md` para notas de reuniones.
