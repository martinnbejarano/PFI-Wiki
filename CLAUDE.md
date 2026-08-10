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

**Tema del proyecto:** Sistema de Detección Automática de Desinformación en Redes Sociales
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
├── docs/agents/           ← configuración que leen las skills de ingeniería
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

### Relación wiki ↔ documento (flujo de trabajo durante el año)

El **wiki** es el espacio de investigación y borrador: aquí se procesan fuentes, se sintetizan conceptos, se cruzan ideas. El **documento LaTeX** es la escritura final, académica y formal que va a la entrega.

**Regla general:** Primero se trabaja en el wiki, luego se vuelca al documento.

El volcado ocurre cuando:
- Una sección del wiki está suficientemente madura (no es borrador)
- El usuario pide explícitamente "pasalo al documento"
- Se acerca una entrega y hay que consolidar lo investigado

Al volcar del wiki al documento:
1. Adaptar el tono: el wiki es informal y exploratorio, el documento es académico
2. Agregar citas `\parencite{Clave}` para toda afirmación que lo requiera
3. Si la cita no existe en `biblio.bib`, agregarla antes de escribir el `\parencite{}`
4. No copiar listas de bullets directamente — convertir a prosa o `\begin{enumerate}`
5. Las advertencias (`⚠️ CONTRADICCION`) del wiki no van al documento

### Mapa wiki → documento

| Sección del wiki | Capítulo del documento |
|---|---|
| `wiki/proyecto/` (propuesta, objetivos, alcance) | `chapters/chapter01.tex` |
| `wiki/marco-teorico/` + `wiki/estado-del-arte/` | `chapters/chapter02.tex` |
| `wiki/investigacion/` + `wiki/competencia/` + `wiki/negocio/` | `chapters/chapter03.tex` |
| `wiki/solucion/` + `wiki/datasets/` + `wiki/modelos/` + `wiki/experimentos/` | `chapters/chapter04.tex` |
| `wiki/investigacion/` (entrevistas, encuestas) | `chapters/appendix/interviews.tex`, `surveys.tex` |
| `wiki/proyecto/cronograma.md` | `chapters/appendix/schedule_of_activities.tex` |

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
- `\pdfcomment{texto}` — comentario visible en el PDF pero no impreso.

### Convenciones de escritura LaTeX

- **Citas**: `\parencite{Clave}` dentro del texto. La clave tiene formato `AutorAño` (ej: `Newman2024`).
- **Clave bibliográfica**: `AutorAño` — ej: `Newman2024`, `DevlinEtAl2019`. Para múltiples autores: `ApellidoPrimerAutorEtAlAño`.
- **Autores en biblio.bib**: `Apellido, Nombre` (no al revés) — evita errores con nombres compuestos.
- **Títulos en biblio.bib**: dobles llaves `{{Título}}` para preservar mayúsculas/minúsculas exactas.
- **DOI**: campo propio, no dentro de `url`. Ej: `doi = {10.xxxx/xxxxx}`.
- **Comillas**: usar `\enquote{texto}` en lugar de comillas directas.
- **Tablas**: usar `[t]` (top). Numeradas en romano por capítulo (ya configurado).
- **Figuras**: incluir con `\input{figures/nombre.tex}` y referenciar con `\ref{fig:nombre}`.
- **Referencias internas**: `\ref{}` para figuras/tablas, `\pageref{}` para páginas.
- **No usar `\\` para saltos de párrafo** — usar línea en blanco entre párrafos.
- **Caracteres acentuados**: escribir directamente (UTF-8), no escapear (`á` no `\'a`).

### biblio.bib — fuente única de citas

`documento/biblio.bib` es la fuente autoritativa de todas las referencias del documento final.
- Toda cita usada en el documento **debe** existir en `biblio.bib` antes de compilar.
- Cuando el wiki cita un paper, la misma clave debe existir (o agregarse) en `biblio.bib`.
- El campo `note` se actualiza si la referencia es online: `Consultado: YYYY-MM-DD`.
- Compilar con `biber main` (no `bibtex`) — el template usa el backend `biber`.

### history/ — bitácora interna

`documento/history/` es un documento compilable por separado, **no va en ninguna entrega**.
Compilar con `pdflatex history` desde `documento/`.
- `considerations.tex` — convenciones LaTeX y decisiones del documento. Actualizar cuando se tome una decisión que afecte el formato o estructura.
- `01.tex`, `02.tex`, ... — entradas cronológicas de avance y decisiones importantes. Agregar entradas cuando haya cambios de enfoque, decisiones de arquitectura, o feedback del tutor.

### Qué NO hacer hasta la entrega final

- **No redactar Resumen ni Abstract** (`chapters/summary.tex`, `chapters/abstract.tex`) — solo en entrega final.
- **No generar la carátula** desde el template — generarla en la biblioteca UADE con los datos reales del proyecto.
- **No poner fecha completa** en la portada (`\today`) — solo el año (`\the\year`) hasta la entrega final.

### Checklist antes de cada entrega

- [ ] Cambiar referencias de rojo a negro: en `main.tex` comentar bloque `colorlinks`, descomentar bloque `hidelinks`
- [ ] Quitar el cronograma del anexo (`annex.tex` comenta la línea de `schedule_of_activities`)
- [ ] Verificar warnings de `biber` (referencias mal formateadas)
- [ ] Eliminar o comentar los `\Fidel{}` y `\Martin{}` resueltos
- [ ] Verificar que no queden `Completar.` sin reemplazar
- [ ] Generar carátula oficial desde la biblioteca UADE
- [ ] Si es entrega final: redactar Resumen y Abstract, poner fecha completa (`\today`)

---

## Estilo de escritura académica

### Voz y persona

- **Voz impersonal / pasiva refleja**: "se propone", "se desarrolló", "se implementó", "se analiza". No usar "nosotros proponemos" ni "yo implementé".
- **Tercera persona descriptiva**: "El sistema utiliza...", "La propuesta consiste en...", "Los resultados indican..."
- **Hedging apropiado**: "puede generar falsos positivos", "se espera que", "los resultados sugieren" — no afirmar lo incierto como certeza.

### Terminología consistente (regla de oro)

Una vez establecido un término, usarlo **siempre igual** en todo el documento. Nunca alternar entre formas distintas del mismo concepto.

- Primera aparición: nombre completo en castellano + término en inglés en cursiva + abreviatura entre paréntesis.
  Ejemplo: "modelo de lenguaje grande (*Large Language Model*, LLM)"
- Apariciones siguientes: solo la abreviatura o el término elegido. Ejemplo: "LLM" (no volver a "modelo de lenguaje grande" ni a "inteligencia artificial").
- Términos técnicos en inglés: en cursiva siempre. Ej: *fine-tuning*, *embedding*, *dashboard*, *pipeline*.
- Siglas definidas en el glosario del documento no se vuelven a expandir.

### Frases prohibidas (suenan a IA)

Nunca usar estas frases en el documento final:

- "Cabe destacar que..."
- "Es importante mencionar que..."
- "Resulta fundamental..."
- "En este sentido..."
- "Desde esta perspectiva..."
- "En el marco de..."
- "En el contexto de la presente investigación..."
- "A lo largo del presente trabajo..."
- "En pos de..."
- "Vale la pena resaltar que..."
- "Sin lugar a dudas..."
- "Como se mencionó anteriormente..." (usarlo una vez máx por capítulo)
- Iniciar demasiados párrafos consecutivos con "El" o "La" + sustantivo

### Estructura de párrafos

- Largo ideal: 4–6 oraciones. Cada párrafo desarrolla una sola idea.
- El primer párrafo de una sección contextualizará y enunciará qué se va a ver.
- Los párrafos intermedios desarrollan y citan evidencia: "De acuerdo con Apellido (año), ..."
- El último párrafo de una sección cierra y conecta con la siguiente.
- Transiciones recomendadas: "En primer lugar...", "A continuación...", "Por su parte...", "Asimismo...", "Sin embargo...", "En síntesis...", "Contrariamente a..."

### Uso de listas

- Solo cuando hay 3+ ítems que realmente son enumerables y paralelos.
- No reemplazar prosa argumentativa con listas. Las listas no argumentan, enumeran.
- En LaTeX: `\begin{enumerate}` para secuencias ordenadas, `\begin{itemize}` para atributos no ordenados.

### Citas en el texto

- La cita va al final de la afirmación que sustenta, dentro del punto: "... (Apellido, año)."
- No usar notas al pie para citas bibliográficas — solo `\parencite{}`.
- La cita no reemplaza la explicación: primero explicar la idea, luego citar la fuente.

---

## Citas y bibliografía — ISO 690-2010

El documento usa **ISO 690-2010** en su variante **autor-fecha** (equivalente al sistema Harvard). El template ya tiene `style=iso-authoryear` configurado con `biber`.

### Formato de cita en el texto

| Caso | Formato | Ejemplo |
|---|---|---|
| 1 autor | (Apellido, año) | (Bergdahl, 2022) |
| 2 autores | (Apellido1, Apellido2, año) | (Rosen, Tynan, 2025) |
| 3+ autores | (Apellido *et al.*, año) | (Harting *et al.*, 2005) |
| Cita directa | (Apellido, año, p. X) | (Fassinger, 1995, p. 84) |

En LaTeX: `\parencite{Clave}` genera el formato correcto automáticamente.
*et al.* va siempre en cursiva (`\parencite` lo hace solo con iso-authoryear).

### Sección Bibliografía

- Título de la sección: **Bibliografía** (no "Referencias", no "Fuentes").
- Ordenada **alfabéticamente** por apellido del primer autor.
- En el documento LaTeX ya está configurado en `main.tex` con `\printbibliography`.

### Formato de entradas en biblio.bib

**Artículo académico con DOI** (no se pone link ni "[en línea]"):
```bibtex
@article{ApellidoAño,
  author  = {Apellido, Nombre and Apellido2, Nombre2},
  title   = {{Título exacto del artículo}},
  journal = {Nombre de la revista},
  year    = {2022},
  volume  = {190},
  pages   = {104561},
  doi     = {10.xxxx/xxxxx},
}
```

**Artículo sin DOI pero con URL** (requiere `note` con fecha de consulta):
```bibtex
@article{ApellidoAño,
  author  = {Apellido, Nombre},
  title   = {{Título}},
  journal = {Nombre revista},
  year    = {2001},
  volume  = {15},
  number  = {7},
  url     = {https://...},
  note    = {Consulta: Noviembre de 2025},
}
```

**Libro** (con ISBN no se pone link):
```bibtex
@book{ApellidoAño,
  author    = {Apellido, Nombre},
  title     = {{Título del libro}},
  edition   = {2},
  address   = {Ciudad},
  publisher = {Editorial},
  year      = {2015},
  isbn      = {978XXXXXXXXXX},
}
```

**Recurso online sin DOI/ISBN** (requiere URL + fecha consulta):
```bibtex
@online{ApellidoAño,
  author = {Apellido, Nombre},
  title  = {{Título del recurso}},
  year   = {2025},
  url    = {https://...},
  note   = {Consulta: Mes de año},
}
```

**Capítulo en libro:**
```bibtex
@incollection{ApellidoAño,
  author    = {Apellido, Nombre},
  title     = {{Título del capítulo}},
  booktitle = {{Título del libro}},
  editor    = {Editor, Nombre},
  address   = {Ciudad},
  publisher = {Editorial},
  year      = {1995},
  pages     = {56--70},
  isbn      = {978XXXXXXXXXX},
}
```

### Reglas de citado — instrucciones del profesor

1. **Si tiene DOI, ISBN o ISSN**: no agregar link ni "[en línea]".
2. **Si no tiene DOI/ISBN**: agregar URL + "Consulta: Mes de año." al final.
3. **Fecha**: lo más completa posible (año+mes+día si está disponible; si solo hay año, solo año).
4. **Nombre de autores**: verificar que el apellido y nombre coincidan exactamente con los del artículo referenciado.
5. **Clave bibliográfica**: formato `ApellidoAño` (ej: `Newman2024`, `HartingEtAl2005`). Para un autor de organización: `NombreOrgAño`.
6. **Muchos autores en bib**: listar TODOS en el `.bib`; el estilo aplica *et al.* automáticamente en el texto.
7. **Orden en la sección Bibliografía**: alfabético por primer apellido (lo maneja biblatex automáticamente).
8. Las páginas más conocidas tienen botón "Exportar cita" en formato `.bib` — usar ese como base y completar/verificar.

### Fuentes académicas prioritarias (Ingeniería en Informática)

1. **Repositorios universitarios**: MIT DSpace, Stanford SearchWorks, Oxford ORA, Harvard DASH
2. **Bases especializadas**: IEEE Xplore, ACM Digital Library, Springer, ScienceDirect
3. **Buscadores académicos**: Google Scholar, Semantic Scholar
4. **Publicaciones indexadas**: Scopus, Web of Science

Criterios de selección: pertinencia, vigencia (idealmente últimos 5 años), calidad de la revista o evento.

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

**Plataforma objetivo (detección):** Twitter/X — única red social del prototipo.
**Medios digitales de confianza (fuentes de evidencia, no de detección):** Infobae, Clarín, La Nación, Página/12, Télam — se usan para scraping y verificación de afirmaciones, no como objetivos de detección.

**Métricas de evaluación:**
- Accuracy, Precision, Recall, F1
- AUC-ROC
- Comparación con baselines (TF-IDF + LR, etc.)

## Notas del tutor

Tutor: **Giro Uribazo, Fidel Valentin** (UADE, interno).
Email: fgirouribazo@uade.edu.ar
Ver `wiki/proyecto/reuniones.md` para notas de reuniones.

---

## Agent skills

### Issue tracker

Los *issues* viven en GitHub Issues de `martinnbejarano/PFI-Wiki`, operados con la CLI `gh`. Ver `docs/agents/issue-tracker.md`.

### Etiquetas de triage

Los cinco roles canónicos con sus nombres por defecto: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. Ver `docs/agents/triage-labels.md`.

### Documentación de dominio

Contexto único: `CONTEXT.md` en la raíz y ADR en `docs/adr/`, ambos creados de forma perezosa. El glosario del dominio vive repartido en el wiki. Ver `docs/agents/domain.md`.
