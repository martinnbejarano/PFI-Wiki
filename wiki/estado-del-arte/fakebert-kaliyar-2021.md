---
titulo: FakeBERT — Detección con BERT + CNN (Kaliyar et al., 2021)
tipo: fuente
tags: [estado-del-arte, fakebert, bert, cnn, fake-news, kaliyar, 2021, ingles]
fuentes: [FakeBERT Fake News Detection BERT CNN - Kaliyar 2021.md]
actualizado: 2026-06-04
---

# FakeBERT — Detección con BERT + CNN (Kaliyar et al., 2021)

## Referencia

> Kaliyar, R. K., Goswami, A., Narang, P. (2021). *FakeBERT: Fake News Detection in Social Media with a BERT-based Deep Learning Approach*. Multimedia Tools and Applications, 80, 11765–11788. DOI: 10.1007/s11042-020-10183-2. Clave biblio: `KaliyarEtAl2021`

## Descripción

FakeBERT combina BERT con capas CNN (*Convolutional Neural Networks*) para capturar tanto representaciones contextuales profundas (BERT) como patrones locales de n-gramas (CNN). Es uno de los sistemas BERT fine-tuned con mejor performance reportado en detección de fake news en inglés.

## Arquitectura

```
Input text
    ↓
BERT encoder (BERT-base-uncased)
    ↓
[CLS] embedding (768d)
    ↓
CNN layers (1D convolutions, múltiples tamaños de kernel)
    ↓
Max pooling
    ↓
Dense + Softmax
    ↓
Fake / Real
```

La adición de capas CNN post-BERT permite capturar patrones de n-gramas específicos del dominio de fake news que el mecanismo de atención global de BERT puede no enfatizar.

## Resultados reportados

Evaluado en múltiples datasets de fake news en inglés:

| Dataset | Accuracy | F1 |
|---|---|---|
| LIAR | ~98.9% | ~0.99 |
| Fakeddit (binario) | ~97% | ~0.97 |
| Otros datasets inglés | 95–99% | 0.95–0.99 |

**Nota**: estos resultados de 98–99% son **in-domain** (entrenamiento y test del mismo dataset). Son significativamente más altos que los reportados con evaluación cross-domain.

## Contexto crítico

> ⚠️ CONTRADICCION: Los resultados de 98.9% en LIAR contrastan con los ~62–68% reportados por otros trabajos (Wang 2017, Hasan 2025) en el mismo dataset. Esta discrepancia puede deberse a (1) diferente split train/test, (2) data leakage, o (3) evaluación binaria vs. 6 clases. Ver [[wiki/estado-del-arte/brechas-espanol-latam]].

La literatura de 2024–2025 es consistente en que los resultados "too good to be true" (>95% en LIAR) suelen indicar evaluación metodológicamente cuestionable. Raza et al. (2024) y Hasan et al. (2025) obtienen resultados más conservadores con metodología más rigurosa.

## Contribución técnica

La combinación BERT + CNN es técnicamente sólida y está bien motivada:
- BERT captura contexto global (relaciones entre oraciones lejanas)
- CNN captura patrones locales (frases características de fake news: "fuentes dicen que...", "nadie te contará que...")

Esta arquitectura híbrida es una opción a considerar en la implementación del módulo de clasificación del PFI.

## Relevancia para el PFI

**Alta**: FakeBERT es el baseline comparador principal para el módulo de clasificación. El PFI debe reportar resultados al menos equivalentes a FakeBERT en los mismos datasets.

La arquitectura BERT + capas adicionales (CNN, MLP, attention) es un patrón de diseño estándar que el sistema del PFI puede adoptar.

## Referencias cruzadas
- [[wiki/marco-teorico/transformers-bert]]
- [[wiki/estado-del-arte/comparativa-llms-2024-2025]]
- [[wiki/datasets/liar-dataset]]

## Fuentes
- [[raw/papers/FakeBERT Fake News Detection BERT CNN - Kaliyar 2021.md]]
