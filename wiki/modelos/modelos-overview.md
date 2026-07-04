---
titulo: Modelos — Panorama General
tipo: análisis
tags: [modelos, ml, nlp, bert, clasificacion]
actualizado: 2026-07-04
---

# Modelos para Detección de Desinformación

## Modelo elegido para el proyecto

**Modelo principal: RoBERTuito** (RoBERTa pre-entrenado sobre 500M de tweets en español). Es el candidato prioritario del clasificador de contenido porque el sistema opera exclusivamente sobre texto de Twitter/X, dominio para el que RoBERTuito fue pre-entrenado (lenguaje informal, hashtags, abreviaturas, variantes latinoamericanas). El principio de que los modelos específicos del idioma superan a los multilingües genéricos está respaldado por la literatura (Albtoush et al., 2025; Pérez et al., 2022).

**Líneas de comparación:** BETO y XLM-RoBERTa como transformers alternativos —XLM-RoBERTa habilita además transferencia cross-lingual desde datasets en inglés (LIAR, FakeNewsNet)— y **TF-IDF + Regresión Logística** como *baseline* clásico. La selección final se confirma experimentalmente con **F1 macro** como métrica principal (objetivo de referencia: 0,80, superando al *baseline* clásico en ≥10 puntos).

Detalle de la comparativa y justificación en [[wiki/marco-teorico/modelos-espanol]] y [[wiki/marco-teorico/enfoques-deteccion]].

## Taxonomía de enfoques

### 1. Basados en contenido del texto

Analizan únicamente el texto del post/artículo.

| Modelo | Tipo | Fortaleza | Limitación |
|---|---|---|---|
| TF-IDF + Logistic Regression | Baseline clásico | Simple, interpretable | No captura semántica profunda |
| BERT (base/large) | Transformer | State-of-the-art en NLP | Requiere fine-tuning, costoso |
| RoBERTa | Transformer | Mejor que BERT en benchmarks | Idem |
| XLM-RoBERTa | Transformer multilingüe | Soporte español | Idem |
| DeBERTa | Transformer | Mejor que RoBERTa en algunos tasks | Más pesado |
| LLMs (GPT-4, Claude) | LLM | Zero/few-shot sin fine-tuning | Costo de inferencia, latencia |

### 2. Basados en fuente / autor

Analizan la credibilidad de quien publica mediante metadatos (antigüedad y reputación del dominio, historial de publicaciones, concordancia dominio–cuentas citadas). En el PFI corresponde al **Módulo 2 (credibilidad de fuente)**, implementado con Regresión Logística o una red neuronal pequeña que produce un sub-*score* complementario al clasificador textual. Ver [[wiki/marco-teorico/enfoques-deteccion]].

### 3. Basados en propagación / grafos

Analizan cómo se difunde el contenido en la red (grafos de propagación, redes de difusión). El estado del arte son las GNN bidireccionales tipo BiGCN (+10pp sobre texto solo en PHEME; ver [[wiki/estado-del-arte/bigcn-deteccion-grafos]]). **Fuera del alcance del MVP**: requiere acceso a la API restringida de Twitter/X; se difiere a versiones futuras.

### 4. Multimodales

Combinan texto + imagen + metadatos (p. ej. Fakeddit, ver [[wiki/datasets/fakeddit]]). **Fuera del alcance del MVP** (solo texto); relevante para el *release* de soporte multimedia y detección de deepfakes.

### 5. Ensemble

Combinación de múltiples señales. En el PFI es el **Módulo 4**: un combinador (*weighted combination* o NN pequeña) que sintetiza los scores de contenido, credibilidad de fuente y contraste semántico en la decisión final. Ver [[wiki/solucion/metodologia-tecnica]].

## Modelo baseline

**TF-IDF + Regresión Logística**, estándar de comparación en la literatura de detección de desinformación (Wang, 2017). El objetivo es que el modelo Transformer lo supere en al menos 10 puntos porcentuales de F1 macro.

## Decisión de modelo

Se prioriza **RoBERTuito** por su ajuste al dominio (texto de Twitter/X en español rioplatense) y su origen argentino (grupo pysentimiento, UBA/CONICET), frente a BETO (Wikipedia, texto formal) y XLM-RoBERTa (multilingüe genérico). El trade-off es favorable: RoBERTuito (~125M parámetros) tiene costo de cómputo comparable a BETO, mejor alineación con el dominio, y evita la complejidad de los enfoques basados en grafos. La decisión se valida experimentalmente antes de fijarla como definitiva.

## Recursos computacionales

| Recurso | Disponibilidad |
|---|---|
| GPU local | [sí/no] |
| Google Colab | Sí |
| Hugging Face Spaces | Sí |
| AWS/GCP/Azure | [a evaluar] |

## Referencias cruzadas

- [[wiki/datasets/datasets-overview]]
- [[wiki/experimentos/experimentos-overview]]
- [[wiki/solucion/arquitectura]]
- [[wiki/marco-teorico/nlp-fundacional]]
- [[wiki/marco-teorico/modelos-espanol]]
