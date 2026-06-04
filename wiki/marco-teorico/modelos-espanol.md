---
titulo: Modelos de Lenguaje en Español — BETO, XLM-RoBERTa, RoBERTuito, MarIA
tipo: concepto
tags: [beto, xlm-roberta, robertuito, maria, bert-espanol, nlp-espanol, transformers, low-resource]
fuentes: [Spanish Pre-trained BERT Model BETO - Canete 2023.md, Unsupervised Cross-lingual Representation Learning XLM-RoBERTa - Conneau 2020.md, RoBERTuito Pre-trained Language Model for Social Media Spanish - Perez 2022.md, Fake News Detection Fact Checking Ecuador Spanish Models - Toapanta 2024.md]
actualizado: 2026-06-04
---

# Modelos de Lenguaje en Español — BETO, XLM-RoBERTa, RoBERTuito, MarIA

El sistema del PFI opera sobre texto en español de redes sociales y medios digitales argentinos. Esta página compara los modelos Transformer pre-entrenados disponibles para español, evaluados en el contexto de detección de desinformación.

## Panorama de modelos Transformer en español

Cuatro modelos son relevantes para el PFI. Todos son variantes de BERT o RoBERTa (ver [[transformers-bert]]):

| Modelo | Base | Corpus | Parámetros | HuggingFace |
|---|---|---|---|---|
| **BETO** | BERT | Wikipedia ES (3GB) | 110M | `dccuchile/bert-base-spanish-wwm-cased` |
| **XLM-RoBERTa** | RoBERTa | CC-100 (100 idiomas, 2.5TB) | 125M–355M | `xlm-roberta-base` |
| **RoBERTuito** | RoBERTa | 500M tweets en español | 125M | `pysentimiento/robertuito-base-uncased` |
| **MarIA** | RoBERTa | BNE corpus ES (570GB) | 125M | `PlanTL-GOB-ES/roberta-base-bne` |

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

Desarrollado por la Universidad Nacional de San Luis (Argentina) y PysentimientoAI. Pre-entrenado específicamente sobre **500 millones de tweets en español** (incluyendo variantes latinoamericanas, lunfardo, abreviaturas, emojis).

### Características

- **Corpus**: 500M tweets en español (todos los dialectos latinoamericanos y español peninsular)
- **Uncased**: no distingue mayúsculas (adecuado para redes sociales)
- **Disponibilidad**: HuggingFace, libre

### Ventaja crítica para el PFI

**RoBERTuito es el modelo más adecuado para redes sociales en español.** El PFI analiza texto de Twitter/X, Instagram y Facebook, donde el vocabulario informal, abreviaturas, hashtags y errores ortográficos son frecuentes. BETO (entrenado sobre Wikipedia) no capta estos fenómenos.

La inclusión de variantes argentinas (lunfardo, expresiones regionales) en el corpus de Twitter lo hace especialmente relevante para el dominio objetivo.

### Performance

Pérez et al. (2022) reportan mejoras de 3–8% sobre BETO en tareas de análisis de sentimiento, detección de odio y clasificación en redes sociales en español.

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

| Criterio | BETO | XLM-RoBERTa | RoBERTuito | MarIA |
|---|---|---|---|---|
| Texto formal/periodístico | ✓✓ | ✓✓ | ✓ | ✓✓✓ |
| Redes sociales español | ✓ | ✓✓ | ✓✓✓ | ✓ |
| Variantes argentinas | ✓ | ✓✓ | ✓✓✓ | ✗ |
| Transfer desde inglés | ✗ | ✓✓✓ | ✗ | ✗ |
| Datos in-domain pequeños | ✓✓ | ✓✓✓ | ✓✓ | ✓✓ |
| Accuracy fake news ES | 93% | ~90% | ~89% | 96% |

### Recomendación para el PFI

**Estrategia de ensemble**: usar dos modelos complementarios
1. **RoBERTuito** para análisis de posts de redes sociales (texto informal, hashtags, emojis)
2. **XLM-RoBERTa** para análisis de artículos periodísticos (permite aprovechar datos en inglés con transfer)

MarIA es una alternativa para texto periodístico si se dispone de suficientes datos de fine-tuning argentinos.

Ver [[wiki/solucion/metodologia-tecnica]] para la decisión final de implementación.

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
