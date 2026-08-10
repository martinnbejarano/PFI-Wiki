---
titulo: Drchal et al. (2024) — Pipeline de Fact-Checking Multiidioma (Sin Español)
tipo: fuente
tags: [estado-del-arte, pipeline, multiidioma, fact-checking, drchal, gap-espanol]
fuentes: [Pipeline Dataset Automated Fact-checking Almost Any Language - Drchal 2024.md]
actualizado: 2026-06-04
---

# Drchal et al. (2024) — Pipeline de Fact-Checking "Almost Any Language"

## Referencia

> Drchal, J., et al. (2024). *A Pipeline and Dataset for Automated Fact-Checking in Almost Any Language*. [Conferencia/Workshop NLP]. Clave biblio: `DrzchalEtAl2024`

## Por qué es relevante para el PFI

Este paper es relevante por lo que **no hace**: un sistema de fact-checking que se autodefine como "casi cualquier idioma" **excluye el español** en su cobertura efectiva. Esto documenta una brecha que el PFI puede explotar.

## Descripción

Drchal et al. (2024) proponen un pipeline end-to-end para fact-checking que:
1. Recibe un claim en cualquier idioma
2. Lo traduce a inglés (o trabaja multilingüe con XLM-RoBERTa)
3. Recupera evidencia de Wikipedia multilingüe
4. Genera un veredicto usando un modelo de entailment

El pipeline es modular y puede intercambiar componentes por idioma.

## El gap con el español

A pesar del nombre "almost any language", el paper evalúa principalmente en:
- Inglés: cobertura completa
- Checo: dominio específico del grupo de investigación
- Otros europeos: alemán, francés, polaco

El español no es evaluado en ningún experimento. Las razones implícitas:
- Ausencia de un dataset de fact-checking en español con el mismo formato
- Los fact-checkers hispanohablantes no tienen APIs/feeds estructurados equivalentes a los anglófonos

## Hallazgos técnicos relevantes

| Componente | Implementación | Performance |
|---|---|---|
| Claim detection | BERT fine-tuned | F1 ~0.83 en inglés |
| Evidence retrieval | Wikipedia API | Coverage ~78% |
| Verdict prediction | XLM-RoBERTa | Accuracy ~71% en inglés |

**La traducción automática + pipeline en inglés es peor que un modelo nativo** en el idioma objetivo: ~8–10% de degradación en idiomas no-inglés.

## Implicación para el PFI

El enfoque de Drchal et al. —traducir al inglés y procesar en inglés— es subóptimo para español, porque la traducción automática destruye precisamente los rasgos de registro informal que el clasificador necesita. El PFI adopta un enfoque distinto: en lugar de traducir los datos, usa un modelo multilingüe que procesa el español de forma nativa (XLM-T) y aprovecha los conjuntos anotados en inglés por **transferencia cross-lingual**, sin traducir nada. La evaluación se hace siempre sobre texto en español.

Esto refuerza la decisión de no usar traducción automática como paso intermedio en el pipeline del PFI.

## Referencias cruzadas
- [[wiki/marco-teorico/fact-checking-automatico]]
- [[brechas-espanol-latam]]
- [[wiki/marco-teorico/modelos-espanol]]

## Fuentes
- [[raw/papers/Pipeline Dataset Automated Fact-checking Almost Any Language - Drchal 2024.md]]
