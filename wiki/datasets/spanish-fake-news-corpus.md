---
titulo: Spanish Fake News Corpus (FakeDeS) — El Gap del Español
tipo: dataset
tags: [dataset, espanol, fakedek, posadas, iberleaf, gap-datos, latam]
fuentes: [Spanish-Fake-News-Corpus-Posadas.md]
actualizado: 2026-06-04
---

# Spanish Fake News Corpus (FakeDeS)

El Spanish Fake News Corpus, también conocido como FakeDeS en el contexto del shared task de IberLEF 2021, es el **dataset de referencia más importante del PFI**: documenta el gap crítico de datos en español para detección de desinformación.

## Descripción

| Atributo | Valor |
|---|---|
| Año original | 2019 (actualizado para IberLEF 2021) |
| Autores | Posadas-Durán et al. (UNAM, México) |
| Fuente | Sitios de noticias México + España + fact-checkers |
| Tamaño | **971 muestras totales** |
| Idioma | Español |
| Clases | Binario (real/fake) |
| Disponibilidad | GitHub libre |

## Splits

| Conjunto | Tamaño |
|---|---|
| Entrenamiento | ~700 noticias |
| Validación | ~100 noticias |
| Test | ~171 noticias |

## Temáticas (9 categorías)

Ciencia, Deporte, Economía, Educación, Entretenimiento, Política, Salud, Seguridad, Sociedad.

## Resultados en FakeDeS 2021 (mejores equipos)

Los mejores sistemas del shared task IberLEF 2021 usaron transformers:
- **MarIA (RoBERTa BNE)**: 96% accuracy (Toapanta et al., 2024)
- **BETO**: 93% accuracy
- **XLM-RoBERTa**: ~90% accuracy
- **TF-IDF + SVM (baseline)**: ~75% accuracy

## El gap crítico

Este dataset documenta la brecha fundamental del campo:

| Dataset | Idioma | Tamaño |
|---|---|---|
| LIAR | Inglés | 12.836 |
| FakeNewsNet PolitiFact | Inglés | ~1.000 |
| FakeNewsNet GossipCop | Inglés | ~27.000 |
| **Spanish Fake News** | **Español** | **971** |
| FakeDeS 2021 (extendido) | Español | ~2.000 |

**El corpus en español más grande tiene 971 muestras — 13x menor que LIAR.**

## Limitaciones

- **Tamaño muy pequeño**: 971 samples son insuficientes para fine-tuning robusto sin transfer learning
- **Contexto México + España**: diferencias culturales y léxicas significativas con Argentina
- **Sin contexto social**: no incluye datos de propagación en redes
- **Antigüedad**: 2019–2021; no cubre eventos recientes ni desinformación generada por IA

## Relevancia para el PFI — Uso dual

Este corpus tiene dos roles en el PFI:

### 1. Dataset de evaluación
Permite comparar resultados del sistema contra el estado del arte en español. Toda publicación que evalúe en FakeDeS es un comparador directo.

### 2. Evidencia del gap
La escasez de datos en español **justifica la contribución del PFI**: construir un corpus anotado con noticias argentinas es en sí mismo una contribución académica. El sistema debe incluir un módulo de recolección y anotación.

**Clave biblio**: `PosadasEtAl2019`

## Referencias cruzadas
- [[comparacion-datasets]]
- [[wiki/estado-del-arte/brechas-espanol-latam]]
- [[wiki/estado-del-arte/toapanta-2024-latam]]
- [[wiki/datasets/dataset-recomendacion]]

## Fuentes
- [[raw/datasets/Spanish-Fake-News-Corpus-Posadas.md]]
