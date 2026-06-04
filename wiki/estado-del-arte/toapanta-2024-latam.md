---
titulo: Toapanta et al. (2024) — Detección de Fake News en Español (Ecuador)
tipo: fuente
tags: [estado-del-arte, espanol, latam, ecuador, beto, maria, fact-checking, toapanta]
fuentes: [Fake News Detection Fact Checking Ecuador Spanish Models - Toapanta 2024.md]
actualizado: 2026-06-04
---

# Toapanta et al. (2024) — El paper LATAM más relevante para el PFI

## Referencia

> Toapanta, S., et al. (2024). *Fake News Detection and Fact Checking in Spanish using NLP*. [Conferencia de computación latinoamericana]. Clave biblio: `ToapantaEtAl2024`

## Por qué es el paper más relevante para el PFI

Este es el trabajo académico existente **más directamente comparable al PFI**:
- Detección de fake news en español
- Contexto latinoamericano
- Comparación de modelos Transformer específicos para español
- Evaluación en FakeDeS (el mismo dataset que usará el PFI)

## Descripción

Toapanta et al. (2024) implementaron y compararon cuatro modelos Transformer pre-entrenados en español para detección de fake news, evaluados en el Spanish Fake News Corpus (FakeDeS 2021).

## Resultados principales

| Modelo | Accuracy | F1 |
|---|---|---|
| **MarIA (RoBERTa BNE)** | **96%** | **0.96** |
| BETO | 93% | 0.93 |
| XLM-RoBERTa | ~90% | ~0.90 |
| Baseline (TF-IDF) | ~75% | ~0.75 |

**MarIA** (pre-entrenado sobre el corpus de la Biblioteca Nacional de España, 570GB) es el mejor modelo en español para texto periodístico formal.

## Metodología

1. Preprocesamiento: limpieza estándar (stopwords, normalización)
2. Fine-tuning de cada modelo sobre el split de entrenamiento de FakeDeS
3. Evaluación en el test set oficial de FakeDeS 2021
4. Comparación de métricas: accuracy, precision, recall, F1

## Hallazgos adicionales

- **BETO supera a XLM-RoBERTa** en texto periodístico formal en español, posiblemente por mejor tokenización del vocabulario
- Los modelos Transformer superan al baseline clásico por ~18–21 puntos porcentuales
- El dataset FakeDeS (971 muestras) es suficiente para fine-tuning efectivo con modelos pre-entrenados

## Limitaciones del paper

- Evaluación solo en FakeDeS (contexto México + España, no Argentina)
- No incluye análisis de propagación en redes sociales
- Sin búsqueda web de evidencia
- Las métricas "in-domain" (~96%) no predicen performance en datos reales (ver [[wiki/estado-del-arte/comparativa-llms-2024-2025]])

## Cómo el PFI supera a Toapanta et al. (2024)

El PFI extiende este trabajo en tres dimensiones:

1. **Dominio argentino**: dataset propio con noticias argentinas (no México/España)
2. **Búsqueda web**: módulo de evidencia externa (Serper.dev + LLM), que Toapanta no implementa
3. **Redes sociales**: análisis de texto informal (RoBERTuito para tweets), no solo texto periodístico

Esta extensión justifica la contribución académica del PFI frente a trabajos previos.

## Referencias cruzadas
- [[wiki/datasets/spanish-fake-news-corpus]]
- [[wiki/marco-teorico/modelos-espanol]]
- [[brechas-espanol-latam]]

## Fuentes
- [[raw/papers/Fake News Detection Fact Checking Ecuador Spanish Models - Toapanta 2024.md]]
