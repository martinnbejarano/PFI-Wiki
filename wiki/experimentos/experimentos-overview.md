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
| EXP-03 | XLM-T (`xlm-t_fakedes_s42`) | FakeDeS, prueba oficial (572) | 0,667 | 2026-10-05 | Kaggle T4. Validación 0,776, AUC-ROC 0,737; época 5 de 5: **no convergió** (pérdida de entrenamiento alta y oscilante, F1 todavía subiendo) |
| EXP-04 | XLM-T en dos etapas (`xlm-t_liar-fakenewsnet-fakedes_s42`) | LIAR + FakeNewsNet → FakeDeS; prueba de FakeDeS | 0,704 | 2026-10-05 | Kaggle T4. Validación 0,823, AUC-ROC 0,770; época 4. La etapa en inglés suma +3,7 puntos sobre EXP-03 |
| EXP-05 | RoBERTuito (`robertuito_fakedes_s42`) | FakeDeS, prueba oficial (572) | 0,558 | 2026-10-05 | Kaggle T4. Validación 0,761, AUC-ROC 0,637. Trunca en 128 *tokens* (97 % de las noticias): pierde casi todo el cuerpo |
| EXP-06 | BETO (`beto_fakedes_s42`) | FakeDeS, prueba oficial (572) | **0,760** | 2026-10-05 | Kaggle T4. **Mejor en validación (0,876)**, AUC-ROC 0,826; época 4. Clase falso: precisión 0,861, cobertura 0,629 (106 falsos no detectados de 286) |
| EXP-07 | LLM *zero-shot* del prototipo (`llm-zero-shot_gpt-5.6-luna`) | FakeDeS, prueba oficial (572) | 0,873 | 2026-09-28 | `llm_zero_shot.py`, local. AUC-ROC 0,953; umbral 0,62 elegido en validación (F1 0,959); 0,40 USD y 2,76 s por ejemplo en 866 ejemplos. Posible contaminación: FakeDeS es público y anterior al corte del modelo [sin verificar] |

Corridas locales del notebook `prototipo/clasificador/linea_base.ipynb`; falta repetirlas en Colab [sin verificar]. Los JSON con todas las métricas (por clase, matriz de confusión, hiperparámetros) están en `prototipo/clasificador/resultados/`, y el formato está documentado en `prototipo/clasificador/README.md`.

## Mejor resultado actual

**BETO (EXP-06)**: el mejor de los modelos propios en la validación de FakeDeS (0,876), que es el criterio de selección del cap. 4. En la prueba de FakeDeS da **F1 macro 0,760**: +2,6 puntos sobre la línea base (0,734).

**RNF-05 original no se cumplía en FakeDeS** (pedía 0,80 *y* +10 puntos, o sea ≥ 0,834). El 2026-10-05 el autor lo recalibró a **F1 ≥ 0,75 y superior a la línea base**, antes de evaluar el corpus argentino, que es donde se mide (ver [[pruebas]]). Con la meta nueva, BETO cumpliría sobre FakeDeS (0,760 > 0,75 y > 0,734). Contexto: el mejor sistema publicado sobre la prueba de FakeDeS 2021 (GDUFS_DM, IberLEF 2021) logró F1 macro **0,7666**, sobre 662 noticias (la nuestra tiene 572 tras deduplicar; la comparación es aproximada). Esa prueba introduce a propósito variación temática (COVID-19) y de país, y eso explica la caída de validación a prueba que muestran todos los modelos (BETO 0,876 → 0,760). Fuente: [overview de FakeDeS 2021](https://portal.odesia.uned.es/en/node/37) (consultado 2026-10-05).

El LLM *zero-shot* (EXP-07, 0,873) supera a todos, con la reserva de contaminación ya anotada.

## Evaluación final sobre el corpus argentino (2026-10-05, #36)

Una sola evaluación, con `evaluar_argentino.py`, sobre los **108 tuits confirmados** (48 V / 60 F) y el umbral de cada JSON (0,5). Queda como `argentino/prueba` en `resultados/`.

| Modelo | F1 macro | AUC-ROC | Recall falso | Matriz [[VV, VF], [FV, FF]] |
|---|---|---|---|---|
| Línea base TF-IDF + LR | 0,496 | 0,604 | 0,900 | [[9, 39], [6, 54]] |
| **BETO** | **0,439** | 0,551 | 0,833 | [[7, 41], [10, 50]] |
| LLM *zero-shot* | pendiente | — | — | falta `OPENAI_API_KEY` en `servicio/.env` |

**Los dos modelos entrenados caen al nivel del azar** y marcan casi todo como falso (BETO, 91 de 108). **RNF-05 no se cumple en ninguna de sus dos condiciones**: 0,439 < 0,75, y BETO queda por debajo de la línea base.

Se descartó un error de inferencia: el mismo código reproduce el 0,7596 de BETO sobre la prueba de FakeDeS. La causa más probable es el **cambio de dominio**: noticias largas (titular + cuerpo, mediana ~500 *tokens*) → tuits de pocas líneas, con otro registro y otros temas. Era el riesgo que el cap. 4 anticipaba al declarar FakeDeS «no rioplatense», y el corpus argentino lo mide tal como fue diseñado.

Los otros Transformer (XLM-T, RoBERTuito) no se evaluaron sobre el corpus: evaluarlos ahora para elegir entre ellos rompería la reserva estricta.

## Baseline de referencia

**TF-IDF con regresión logística.** Ratificado el 2026-08-13.

RNF-05 exige que el clasificador supere esta línea base y alcance un F1 macro de 0,75 (hasta el 2026-10-05: +10 puntos y 0,80).

Comparación (2026-09-28): TF-IDF + LR, XLM-T con y sin etapa previa en inglés (LIAR + FakeNewsNet), RoBERTuito, BETO y un LLM *zero-shot*, todos binarios (verdadero/falso). Se elige por F1 macro en la validación de FakeDeS; el corpus argentino se evalúa una sola vez al final. Ver [[pruebas]].

El protocolo completo (partición, métricas, acuerdo inter-anotador) está en [[pruebas]].

## Referencias cruzadas

- [[wiki/modelos/modelos-overview]]
- [[wiki/datasets/datasets-overview]]
- [[wiki/solucion/pruebas]]
