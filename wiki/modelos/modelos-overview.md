---
titulo: Modelos — Panorama General
tipo: análisis
tags: [modelos, ml, nlp, bert, clasificacion, xlm-t]
actualizado: 2026-08-13
---

# Modelos para Detección de Desinformación

## Modelo elegido para el proyecto

**Modelo principal: XLM-T** (`cardiffnlp/twitter-xlm-roberta-base`), ratificado el 2026-08-13. Es XLM-RoBERTa re-pre-entrenado por Cardiff NLP sobre ~198 millones de tuits en más de 30 idiomas (Barbieri et al., 2022), lo que resuelve la tensión que mantenía abierta la decisión: conserva el linaje y la arquitectura de XLM-RoBERTa —y con ellos la transferencia desde el inglés— y suma la adaptación al dominio de Twitter que hasta ahora solo ofrecía RoBERTuito.

**Por qué la transferencia importa tanto acá.** El proyecto no tiene volumen de datos anotados en español. El Tier 1 de [[wiki/datasets/comparacion-datasets]] son unos 40.000 ejemplos en inglés (LIAR y FakeNewsNet), y **existe solo si el modelo es multilingüe**. Con un modelo monolingüe el conjunto de entrenamiento se reduce a FakeDeS —971 ejemplos— más el corpus argentino que todavía hay que construir, lo que traslada todo el riesgo a la Entrega 4. El argumento decisivo no fue el prestigio del modelo sino de dónde salen los datos.

| | RoBERTuito | XLM-RoBERTa | **XLM-T** |
|---|---|---|---|
| Ajuste al dominio (tuits informales) | Alto — 500M de tuits en español | Bajo — corpus web genérico | **Alto — 198M de tuits multilingües** |
| Transferencia desde el inglés | No (monolingüe) | Sí | **Sí** |
| Tier 1 de datos (40.000 ejemplos) | Inutilizable | Disponible | **Disponible** |

**Líneas de comparación:** RoBERTuito y BETO como transformers alternativos, y **TF-IDF + Regresión Logística** como *baseline* clásico. La ratificación fija el modelo con el que se construye el prototipo, pero no cancela la comparación: la selección se confirma experimentalmente con **F1 macro** como métrica principal (objetivo de referencia: 0,80, superando al *baseline* clásico en ≥10 puntos), y esa tabla de resultados es el contenido del capítulo 4 en la Entrega 4.

El registro completo de las opciones evaluadas está en [[wiki/sintesis/decisiones-pendientes-2026-08]].

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
| XLM-T | Transformer multilingüe adaptado a Twitter | **Modelo principal del PFI** — transferencia desde el inglés y registro de redes sociales | Idem |
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

Se elige **XLM-T** frente a BETO (Wikipedia, texto formal), XLM-RoBERTa (multilingüe pero sin adaptación al dominio social) y RoBERTuito (adaptado al dominio pero monolingüe). Con ~125M de parámetros su costo de cómputo es comparable al de los otros tres, así que el *trade-off* no está en el gasto sino en qué datos habilita: es el único de los cuatro que permite entrenar sobre el Tier 1 en inglés y además entiende el registro de Twitter.

Sobre RoBERTuito conviene ser preciso, porque descartarlo como principal no es descalificarlo: se publicó en LREC 2022 y Toapanta et al. (2024) lo midieron en la tarea exacta de este PFI con 93,53 % de exactitud y F1 0,934, empatado con BETO. Que provenga de la UBA y el CONICET es además un argumento a favor en un proyecto argentino, porque implica variedad rioplatense en el corpus. Queda como la primera línea de comparación, y si gana la evaluación experimental pasa a ser el modelo del sistema.

**El costo conocido de esta decisión.** Elegir un modelo de linaje multilingüe tiene una contra documentada: Gouliev et al. (2025) reportan una caída de entre 8 y 12 puntos de rendimiento de los modelos multilingües frente a los nativos del idioma, y esa evidencia está registrada como brecha en [[wiki/estado-del-arte/brechas-espanol-latam]]. Hay dos razones para asumirla igual. La primera es que la penalización se midió sobre multilingües *genéricos*, y XLM-T está adaptado al dominio sobre 198 millones de tuits; la segunda es que el *fine-tuning* ocurre sobre datos en español. Ninguna de las dos es una demostración: son argumentos de por qué la penalización podría no materializarse. La comparación experimental contra RoBERTuito existe justamente para medirlo, y si el resultado contradice la decisión, la decisión se revierte.

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
