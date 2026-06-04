---
titulo: LIAR Dataset — Benchmark de Fake News
tipo: dataset
tags: [dataset, liar, politifact, fact-checking, benchmark, ingles]
fuentes: [LIAR A Benchmark Dataset for Fake News Detection - Wang 2017.md]
actualizado: 2026-06-04
---

# LIAR Dataset

El dataset LIAR (Wang, 2017) es el *benchmark* de referencia para detección de fake news. Es la línea de base contra la cual se comparan todos los sistemas del estado del arte.

## Descripción

| Atributo | Valor |
|---|---|
| Año | 2017 |
| Fuente | PolitiFact.com (fact-checking político) |
| Tamaño | 12.836 claims etiquetadas manualmente |
| Idioma | Inglés |
| Clases | 6 (fine-grained) |
| Split | 10.269 train / 1.284 val / 1.283 test |
| Disponibilidad | Libre descarga |

## Esquema de labels (6 clases)

| Clase | Descripción | Ejemplos |
|---|---|---|
| pants-fire | Completamente falso, ridículo | Afirmaciones sin base factual |
| false | Falso | Afirmaciones verificadamente incorrectas |
| barely-true | Casi verdad pero engañoso | Contexto parcial, malinterpretación |
| half-true | Mitad verdad | Partes verdaderas y falsas entremezcladas |
| mostly-true | Mayormente verdadero | Correcto con pequeños errores |
| true | Verdadero | Verificado completamente correcto |

## Metadatos por claim

Cada muestra incluye:
- Texto de la claim
- Hablante (político, periodista, etc.)
- Partido político
- Contexto (debate, campaña, etc.)
- Historia de veracidad del hablante (conteo de claims previas por categoría)

Los metadatos permiten modelos que combinan texto + perfil del hablante.

## Resultados del estado del arte

| Modelo | Accuracy (binary: F/T) | Accuracy (6 clases) |
|---|---|---|
| TF-IDF + LR (baseline) | ~61% | ~21% |
| BERT fine-tuned | ~67% | ~28% |
| RoBERTa | ~68% | ~29% |
| BERT + metadatos | ~70% | ~32% |

Hasan et al. (2025) reportan que incluso los mejores modelos (SVM, RoBERTa) alcanzan solo ~62% en 6 clases — evidencia de que el problema de clasificación fina es muy difícil.

## Limitaciones

- **Solo inglés**: sin datos en español
- **Solo contexto político americano**: PolitiFact cubre casi exclusivamente política de EE.UU.
- **Clase 6 difícil**: la clasificación en 6 niveles de veracidad tiene muy alta tasa de error
- **Antigüedad**: claims de 2007–2016; no cubre desinformación de IA generativa

## Relevancia para el PFI

LIAR es el **baseline de referencia** del sistema. Para comparabilidad con la literatura, el sistema del PFI debe reportar resultados en LIAR (o en LIAR traducido/filtrado al español). La granularidad de 6 clases inspira el esquema de labels propuesto para el dataset argentino.

**Clave biblio**: `Wang2017`

## Referencias cruzadas
- [[comparacion-datasets]]
- [[wiki/datasets/dataset-recomendacion]]
- [[wiki/estado-del-arte/fakebert-kaliyar-2021]]

## Fuentes
- [[raw/datasets/LIAR-dataset.md]]
- [[raw/papers/LIAR A Benchmark Dataset for Fake News Detection - Wang 2017.md]]
