---
titulo: Toapanta et al. (2024) — Detección de Fake News en Español (Ecuador)
tipo: fuente
tags: [estado-del-arte, espanol, latam, ecuador, beto, maria, roberta, fact-checking, toapanta]
fuentes: [Fake News Detection Fact Checking Ecuador Spanish Models - Toapanta 2024.md]
actualizado: 2026-06-04
---

# Toapanta et al. (2024) — El paper LATAM más relevante para el PFI

## Referencia

> Toapanta Bernabé, M., García-Cumbreras, M. Á. y Ureña-López, L. A. (2024). Fake News Detection and Fact Checking in X posts from Ecuador Chequea and Ecuador Verifica using Spanish Language Models. *Revista Tecnológica ESPOL*, vol. 36, n.º 2, pp. 158–173. DOI: 10.37815/rte.v36n2.1219. Clave biblio: `ToapantaEtAl2024`

## Por qué es el paper más relevante para el PFI

Este es el trabajo académico existente **más directamente comparable al PFI**:
- Detección de fake news en español latinoamericano
- Datos de organizaciones de fact-checking latinoamericanas (Ecuador Chequea y Ecuador Verifica)
- Comparación de modelos Transformer específicos para español
- Metodología exportable al contexto argentino (reemplazar Ecuador Chequea por Chequeado.com)

## Descripción

Toapanta et al. (2024) implementaron y compararon cinco modelos Transformer pre-entrenados en español para detección de fake news sobre un corpus de publicaciones en X (ex Twitter) verificadas por organizaciones ecuatorianas de fact-checking. Dataset: **1.340 ítems** en 7 categorías de veracidad (período enero 2020 – marzo 2024), expandidos a 4.640 mediante SMOTE para equilibrar clases.

## Resultados principales

| Modelo | Accuracy | F1 |
|---|---|---|
| **MarIA (RoBERTa BNE)** | **96.01%** | **0.9597** |
| BERTin | 95.47% | 0.9544 |
| BETO | 93.53% | 0.9345 |
| RoBERTuito | 93.53% | 0.9335 |
| BERTuit | 93.43% | 0.9326 |

**MarIA** (pre-entrenado sobre el corpus de la Biblioteca Nacional de España, 570GB) es el mejor modelo en español para este tipo de tarea.

## Metodología

1. Recolección de posts verificados por fact-checkers ecuatorianos
2. Etiquetado en 7 categorías de veracidad (más granular que binario)
3. Preprocesamiento estándar + balanceo con SMOTE
4. Fine-tuning de cada modelo
5. Evaluación con accuracy, precision, recall, F1

## Cómo el PFI extiende este trabajo

| Dimensión | Toapanta 2024 | PFI (propuesto) |
|---|---|---|
| País | Ecuador | Argentina |
| Fuente de verdad | Ecuador Chequea/Verifica | Chequeado.com + AFP Factual |
| Búsqueda de evidencia | No | Módulo Serper.dev |
| Texto informal redes | Sí (Twitter) | Sí (Twitter + Instagram) |
| Contribución de datos | No (sin dataset público) | Dataset argentino como contribución |

## Limitaciones del paper

- Dataset concentrado en Ecuador: diferencias culturales y léxicas con Argentina
- 1.340 muestras originales antes de SMOTE: pequeño para entrenamiento robusto sin oversampling
- Solo texto, sin análisis multimodal ni evidencia externa
- 7 categorías de veracidad (no estándar con respecto al resto de la literatura)

## Referencias cruzadas
- [[wiki/datasets/spanish-fake-news-corpus]]
- [[wiki/marco-teorico/modelos-espanol]]
- [[brechas-espanol-latam]]
- [[comparativa-llms-2024-2025]]

## Fuentes
- [[raw/papers/Fake News Detection Fact Checking Ecuador Spanish Models - Toapanta 2024.md]]
