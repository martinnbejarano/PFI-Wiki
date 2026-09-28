---
titulo: Experimentos — Panorama General
tipo: análisis
tags: [experimentos, benchmarks, resultados, evaluacion]
actualizado: 2026-09-28
---

# Experimentos y Benchmarks

## Formato de entrada para cada experimento

```
## EXP-XX — [Nombre descriptivo]

**Fecha:** YYYY-MM-DD
**Dataset:** [nombre]
**Modelo:** [nombre + versión]
**Objetivo:** ¿qué se quiere validar?

### Configuración
- Hiperparámetros: ...
- Partición: train/val/test = X/Y/Z%
- Hardware: ...

### Resultados

| Métrica | Valor |
|---|---|
| Accuracy | |
| F1 (macro) | |
| Precision | |
| Recall | |
| AUC-ROC | |

### Observaciones
...

### Próximo paso
...
```

---

## Tabla resumen de experimentos

| ID | Modelo | Dataset | F1 | Fecha | Notas |
|---|---|---|---|---|---|
| EXP-01 | TF-IDF + LR (`tfidf-lr_fakedes_s42`) | FakeDeS, prueba oficial (572) | 0,734 | 2026-09-28 | AUC-ROC 0,804; F1 macro en validación 0,806 |
| EXP-02 | TF-IDF + LR (`tfidf-lr_completo_s42`) | LIAR + FakeNewsNet + FakeDeS; prueba de FakeDeS | 0,694 | 2026-09-28 | Sobre la prueba del conjunto completo: 0,712 |

Corridas locales del notebook `prototipo/clasificador/linea_base.ipynb`; falta repetirlas en Colab [sin verificar]. Los JSON con todas las métricas (por clase, matriz de confusión, hiperparámetros) están en `prototipo/clasificador/resultados/`, y el formato está documentado en `prototipo/clasificador/README.md`.

## Mejor resultado actual

[Vacío — se llena con el avance]

## Baseline de referencia

**TF-IDF con regresión logística.** Ratificado el 2026-08-13.

RNF-05 exige que el clasificador supere esta línea base por al menos 10 puntos porcentuales de F1 macro, además de alcanzar un F1 macro de 0,80 en términos absolutos.

Comparación (2026-09-28): TF-IDF + LR, XLM-T con y sin etapa previa en inglés (LIAR + FakeNewsNet), RoBERTuito, BETO y un LLM *zero-shot*, todos binarios (verdadero/falso). Se elige por F1 macro en la validación de FakeDeS; el corpus argentino se evalúa una sola vez al final. Ver [[pruebas]].

El protocolo completo (partición, métricas, acuerdo inter-anotador) está en [[pruebas]].

## Referencias cruzadas

- [[wiki/modelos/modelos-overview]]
- [[wiki/datasets/datasets-overview]]
- [[wiki/solucion/pruebas]]
