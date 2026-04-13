---
titulo: Modelos — Panorama General
tipo: análisis
tags: [modelos, ml, nlp, bert, clasificacion]
actualizado: 2026-04-13
---

# Modelos para Detección de Desinformación

## Modelo elegido para el proyecto

[POR DEFINIR]

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

Analizan credibilidad de quien publica.

[POR INVESTIGAR]

### 3. Basados en propagación / grafos

Analizan cómo se difunde la noticia en la red.

[POR INVESTIGAR]

### 4. Multimodales

Combinan texto + imagen + metadatos.

[POR INVESTIGAR]

### 5. Ensemble

Combinación de múltiples modelos.

[POR INVESTIGAR]

## Modelo baseline

[Definir el baseline contra el que se va a comparar]

## Decisión de modelo

[Justificar la elección: trade-off entre rendimiento, complejidad, recursos, latencia]

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
- [[wiki/marco-teorico/nlp]]
