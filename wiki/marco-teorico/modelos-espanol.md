---
titulo: Modelos de Lenguaje en Español — BETO, XLM-RoBERTa, RoBERTuito, MarIA, XLM-T
tipo: concepto
tags: [beto, xlm-roberta, robertuito, maria, xlm-t, bert-espanol, nlp-espanol, transformers, low-resource]
fuentes: [Spanish Pre-trained BERT Model BETO - Canete 2023.md, Unsupervised Cross-lingual Representation Learning XLM-RoBERTa - Conneau 2020.md, RoBERTuito Pre-trained Language Model for Social Media Spanish - Perez 2022.md, Fake News Detection Fact Checking Ecuador Spanish Models - Toapanta 2024.md]
actualizado: 2026-08-13
---

# Modelos de Lenguaje en Español — BETO, XLM-RoBERTa, RoBERTuito, MarIA, XLM-T

El sistema del PFI opera sobre texto en español de redes sociales (Twitter/X). Esta página compara los modelos Transformer pre-entrenados disponibles para español, evaluados en el contexto de detección de desinformación.

## Panorama de modelos Transformer en español

Cinco modelos son relevantes para el PFI. Todos son variantes de BERT o RoBERTa (ver [[transformers-bert]]):

| Modelo | Base | Corpus | Parámetros | HuggingFace |
|---|---|---|---|---|
| **BETO** | BERT | Wikipedia ES (3GB) | 110M | `dccuchile/bert-base-spanish-wwm-cased` |
| **XLM-RoBERTa** | RoBERTa | CC-100 (100 idiomas, 2.5TB) | 125M–355M | `xlm-roberta-base` |
| **RoBERTuito** | RoBERTa | 500M tweets en español | 125M | `pysentimiento/robertuito-base-uncased` |
| **MarIA** | RoBERTa | BNE corpus ES (570GB) | 125M | `PlanTL-GOB-ES/roberta-base-bne` |
| **XLM-T** ← principal | XLM-RoBERTa | ~198M de tuits en 30+ idiomas | 125M | `cardiffnlp/twitter-xlm-roberta-base` |

## BETO — BERT para Español (Cañete et al., 2023)

Desarrollado por el Departamento de Ciencias de la Computación de la Universidad de Chile (DCC-UChile). Pre-entrenado sobre la Wikipedia en español completa con *whole word masking* (WWM): en lugar de enmascarar tokens individuales, se enmascaran palabras completas, lo que mejora la comprensión morfológica.

### Características

- **Corpus**: Wikipedia en español + ~200M tokens adicionales de fuentes generales
- **Tokenización**: WordPiece con vocabulario de 32.000 tokens específico para español
- **Variantes**: cased (distingue mayúsculas) y uncased
- **Disponibilidad**: libre, HuggingFace

### Performance en detección de desinformación

Toapanta et al. (2024) reportan BETO alcanzando **93% de accuracy** en el dataset FakeDeS (español). Es consistentemente el segundo mejor modelo en español detrás de MarIA en tareas in-domain.

### Uso recomendado

Texto formal/periodístico en español. Para redes sociales, RoBERTuito supera a BETO por su corpus de entrenamiento social.

## XLM-RoBERTa — Multilingüe (Conneau et al., 2020)

Meta AI entrenó XLM-RoBERTa sobre CC-100 (Common Crawl en 100 idiomas, ~2.5TB), usando la arquitectura RoBERTa. Es el modelo multilingüe de referencia.

### Características

- **100 idiomas simultáneos**: español tiene alta representación en CC-100
- **Transfer cross-lingual**: modelos entrenados en inglés pueden transferirse a español sin datos adicionales
- **Variantes**: base (125M params) y large (355M params)

### Ventaja para el PFI

XLM-RoBERTa permite aprovechar datasets masivos en inglés (LIAR, FakeNewsNet) para pre-entrenar y luego adaptar al español con pocos datos. En escenarios *low-resource* (poco texto en español etiquetado), supera a BETO.

Gouliev et al. (2025) — PolyTruth, 25 idiomas — reportan que RemBERT y XLM-RoBERTa son los mejores en escenarios multilingüe, incluyendo español.

## RoBERTuito — Español de Redes Sociales (Pérez et al., 2022)

Desarrollado por el grupo **pysentimiento**, liderado por Juan Manuel Pérez (Universidad de Buenos Aires / CONICET, Argentina). Pre-entrenado específicamente sobre **500 millones de tweets en español** (incluyendo variantes latinoamericanas, lunfardo, abreviaturas, emojis).

### Características

- **Corpus**: 500M tweets en español (todos los dialectos latinoamericanos y español peninsular)
- **Uncased**: no distingue mayúsculas (adecuado para redes sociales)
- **Disponibilidad**: HuggingFace, libre

### Ventaja crítica para el PFI

**RoBERTuito es el modelo monolingüe más adecuado para redes sociales en español.** El PFI analiza texto de Twitter/X, donde el vocabulario informal, abreviaturas, hashtags y errores ortográficos son frecuentes; RoBERTuito fue pre-entrenado precisamente sobre tweets, lo que lo alinea con el dominio objetivo. BETO (entrenado sobre Wikipedia) no capta estos fenómenos.

Ser monolingüe es lo que lo dejó como línea de comparación y no como modelo principal: sin transferencia desde el inglés, los conjuntos anotados de LIAR y FakeNewsNet quedan fuera de uso. Ver la sección de XLM-T más abajo.

La inclusión de variantes argentinas (lunfardo, expresiones regionales) en el corpus de Twitter lo hace especialmente relevante para el dominio objetivo.

### Performance

Pérez et al. (2022) reportan mejoras de 3–8% sobre BETO en tareas de análisis de sentimiento, detección de odio y clasificación en redes sociales en español.

## XLM-T — Twitter multilingüe (Barbieri et al., 2022)

Desarrollado por **Cardiff NLP**. Es XLM-RoBERTa continuado en su pre-entrenamiento sobre aproximadamente **198 millones de tuits en más de 30 idiomas**, español incluido. Identificador: `cardiffnlp/twitter-xlm-roberta-base`. Publicado como *XLM-T: Multilingual Language Models in Twitter for Sentiment Analysis and Beyond*, LREC 2022, pp. 258–266.

### Características

- **Corpus**: ~198M de tuits multilingües sobre la base de XLM-RoBERTa (CC-100, 100 idiomas)
- **Parámetros**: ~125M, comparable a BETO y RoBERTuito
- **Disponibilidad**: HuggingFace, libre

### Por qué es el modelo principal del PFI

Resuelve la tensión que mantenía abierta la decisión de modelo. Las dos propiedades que el proyecto necesita estaban repartidas: RoBERTuito tenía la adaptación al registro de Twitter pero es monolingüe, y XLM-RoBERTa tenía la transferencia desde el inglés pero fue entrenado sobre texto web genérico. XLM-T tiene las dos, porque parte del segundo y le agrega el dominio del primero.

La consecuencia práctica no es de rendimiento sino **de datos**: los cerca de 40.000 ejemplos anotados en inglés de LIAR y FakeNewsNet solo son utilizables con un modelo multilingüe. Con uno monolingüe el conjunto de entrenamiento se reduce a FakeDeS (971 ejemplos) más el corpus argentino por construir.

**Limitación declarada**: no fue entrenado específicamente sobre español rioplatense, y Gouliev et al. (2025) documentan una caída de 8 a 12 puntos de los modelos multilingües frente a los nativos del idioma. Esa penalización se midió sobre multilingües genéricos, no adaptados al dominio, y la comparación experimental contra RoBERTuito existe para verificar si aparece.

## MarIA — Corpus BNE (Gutierrez-Fandino et al., 2022)

Desarrollado por el Plan de Tecnologías del Lenguaje del Gobierno de España. Pre-entrenado sobre el corpus de la Biblioteca Nacional de España (BNE): 570GB de texto formal en español (libros, prensa, legislación, ciencia).

### Características

- **Corpus masivo formal**: el mayor corpus monolingüe en español para pre-entrenamiento
- **Mejor en texto formal**: supera a BETO en texto periodístico y legal
- **Sin variantes latinoamericanas**: corpus principalmente español peninsular

### Performance en detección de desinformación

Toapanta et al. (2024) reportan MarIA (RoBERTa BNE) alcanzando **96% de accuracy** en FakeDeS, el mejor resultado de todos los modelos evaluados en español.

**Limitación para el PFI**: el corpus BNE es fundamentalmente español peninsular; puede no capturar bien el español argentino informal de redes sociales.

## Comparativa para el PFI

| Criterio | BETO | XLM-RoBERTa | RoBERTuito | MarIA | **XLM-T** |
|---|---|---|---|---|---|
| Texto formal/periodístico | ✓✓ | ✓✓ | ✓ | ✓✓✓ | ✓ |
| Redes sociales español | ✓ | ✓✓ | ✓✓✓ | ✓ | ✓✓✓ |
| Variantes argentinas | ✓ | ✓✓ | ✓✓✓ | ✗ | ✓✓ |
| Transfer desde inglés | ✗ | ✓✓✓ | ✗ | ✗ | ✓✓✓ |
| Datos in-domain pequeños | ✓✓ | ✓✓✓ | ✓✓ | ✓✓ | ✓✓✓ |
| Accuracy fake news ES | 93% | ~90% | ~93% | 96% | por medir |

La última fila merece una aclaración: los cuatro primeros valores provienen de Toapanta et al. (2024), que no evaluó XLM-T. Ponerle un número estimado sería inventarlo. Medirlo es parte del trabajo experimental de la Entrega 4.

### Recomendación para el PFI

**Un solo clasificador: XLM-T.** La recomendación anterior proponía un *ensemble* de dos modelos —RoBERTuito para publicaciones de redes y XLM-RoBERTa para artículos periodísticos— y quedó obsoleta el 2026-06-13, cuando el alcance dejó de incluir la clasificación de notas de medios. Hoy los medios de referencia son **fuente de evidencia** del Módulo 3, no objetos de clasificación: no hay artículos periodísticos que clasificar, así que el segundo modelo no tiene entrada.

XLM-T cubre por sí solo las dos propiedades que motivaban el *ensemble*, y hacerlo con un modelo en lugar de dos elimina un servicio de inferencia del despliegue y su costo asociado.

MarIA queda descartado para este alcance: su corpus es fundamentalmente peninsular y formal, opuesto al registro objetivo, pese a tener el mejor número de la tabla.

Ver [[wiki/modelos/modelos-overview]] para la decisión ratificada y [[wiki/solucion/metodologia-tecnica]] para la implementación.

## Referencias cruzadas
- [[transformers-bert]]
- [[nlp-fundacional]]
- [[wiki/estado-del-arte/toapanta-2024-latam]]
- [[wiki/solucion/pipeline-preprocesamiento]]

## Fuentes
- [[raw/papers/Spanish Pre-trained BERT Model BETO - Canete 2023.md]]
- [[raw/papers/Unsupervised Cross-lingual Representation Learning XLM-RoBERTa - Conneau 2020.md]]
- [[raw/papers/RoBERTuito Pre-trained Language Model for Social Media Spanish - Perez 2022.md]]
- [[raw/papers/Fake News Detection Fact Checking Ecuador Spanish Models - Toapanta 2024.md]]
