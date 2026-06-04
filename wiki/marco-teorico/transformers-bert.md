---
titulo: Transformers y BERT — Arquitectura y Pre-entrenamiento
tipo: concepto
tags: [transformer, bert, atencion, pre-entrenamiento, fine-tuning, nlp, deep-learning]
fuentes: [Attention Is All You Need - Vaswani 2017.md, BERT Pre-training of Deep Bidirectional Transformers - Devlin 2019.md]
actualizado: 2026-06-04
---

# Transformers y BERT — Arquitectura y Pre-entrenamiento

La arquitectura Transformer (Vaswani et al., 2017) y su aplicación en BERT (Devlin et al., 2019) constituyen la base técnica del módulo de clasificación del sistema de detección de desinformación. Estos modelos representan el estado del arte en procesamiento de lenguaje natural desde 2017–2019 en adelante.

## Arquitectura Transformer (Vaswani et al., 2017)

### Problema que resuelve

Antes del Transformer, el procesamiento de secuencias se realizaba con RNNs (LSTM, GRU), que procesan tokens secuencialmente de izquierda a derecha. Esto introduce dos problemas: gradientes que desaparecen en secuencias largas y paralelización limitada durante el entrenamiento.

### Mecanismo de atención multi-cabeza

El componente central del Transformer es el mecanismo de *self-attention*, que calcula relaciones entre todos los pares de tokens simultáneamente, sin importar la distancia posicional.

Para cada token, se generan tres vectores: Query (Q), Key (K) y Value (V). La atención se calcula como:

```
Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) * V
```

La atención *multi-cabeza* aplica este mecanismo varias veces en paralelo (8 o 16 cabezas), cada una aprendiendo diferentes tipos de relaciones (coreferencialidad, dependencias sintácticas, relaciones semánticas).

### Codificación posicional

Dado que el mecanismo de atención no tiene noción de orden, se agrega una codificación posicional (*positional encoding*) a los embeddings de entrada, usando funciones seno/coseno a distintas frecuencias.

### Estructura del Transformer original

El modelo encoder-decoder original de Vaswani et al. (2017) fue diseñado para traducción automática:
- **Encoder**: procesa la secuencia de entrada con *self-attention* y capas feed-forward
- **Decoder**: genera la secuencia de salida con *masked self-attention* + *cross-attention* sobre el encoder

Para clasificación de texto (el caso del PFI), solo se usa el **encoder**.

### Impacto

El paper "Attention Is All You Need" tuvo más de 100.000 citas en 8 años. Prácticamente toda la IA generativa moderna (GPT-4, Gemini, Claude) es una variante del Transformer.

## BERT — Bidirectional Encoder Representations from Transformers (Devlin et al., 2019)

### Innovación clave: bidireccionalidad

Los modelos previos basados en Transformer (GPT, ELMo) procesaban el texto de izquierda a derecha o combinaban dos unidireccionales. BERT entrena un encoder **bidireccional**: cada token atiende simultáneamente a todos los tokens anteriores Y posteriores en la secuencia.

Esto permite capturar contexto completo: "El banco aprobó el préstamo" vs. "Me senté en el banco del parque" — BERT produce vectores diferentes para "banco" en cada contexto.

### Pre-entrenamiento

BERT se pre-entrena sobre Wikipedia inglesa + BookCorpus (3.300M palabras) con dos objetivos no supervisados:

1. **Masked Language Model (MLM)**: el 15% de los tokens se ocultan aleatoriamente (`[MASK]`); el modelo predice los tokens enmascarados. Obliga al modelo a capturar contexto bidireccional.

2. **Next Sentence Prediction (NSP)**: dado un par de oraciones (A, B), predecir si B sigue naturalmente a A en el corpus original. Captura relaciones entre oraciones.

### Arquitectura BERT

| Variante | Capas | Cabezas | Dimensión | Parámetros |
|---|---|---|---|---|
| BERT-base | 12 | 12 | 768 | 110M |
| BERT-large | 24 | 16 | 1024 | 340M |

### Token especiales

- `[CLS]`: primer token de cada secuencia; su vector de salida se usa para clasificación
- `[SEP]`: separador entre par de oraciones
- `[MASK]`: token enmascarado durante pre-entrenamiento

### Fine-tuning para clasificación

Para adaptar BERT a una tarea específica (por ejemplo, clasificar noticias como falsas/verdaderas):

1. Agregar una capa lineal encima del vector `[CLS]`
2. Entrenar el modelo completo sobre el dataset etiquetado con tasa de aprendizaje baja (~2e-5)
3. El pre-entrenamiento masivo permite fine-tuning efectivo con datasets pequeños (~1.000–10.000 ejemplos)

Este paradigma *pre-train + fine-tune* es el estándar de la industria desde 2019.

### Limitaciones de BERT

- **Longitud máxima**: 512 tokens por secuencia (limitante para artículos largos)
- **Costo computacional**: fine-tuning requiere GPU; inferencia más lenta que modelos clásicos
- **Inglés nativo**: pre-entrenado principalmente en inglés; para español se necesitan variantes específicas (ver [[modelos-espanol]])

## RoBERTa — Optimización del pre-entrenamiento

Liu et al. (2019) demostraron que BERT estaba sub-entrenado. RoBERTa (*Robustly Optimized BERT Approach*) aplica: más datos (160GB vs. 16GB de BERT), más pasos de entrenamiento, batches más grandes, eliminación de NSP, y *dynamic masking* (diferentes máscaras por epoch). Supera a BERT en la mayoría de benchmarks.

XLM-RoBERTa extiende RoBERTa al dominio multilingüe con 100 idiomas (ver [[modelos-espanol]]).

## Relevancia para el PFI

El módulo de clasificación del sistema utiliza BETO (BERT en español, fine-tuned) como modelo principal. La arquitectura Transformer + fine-tuning es la base teórica que justifica la elección tecnológica frente a alternativas más simples (TF-IDF + LR, FastText).

Los papers de Kaliyar et al. (2021) y Yenikent et al. (2024) documentan que BERT fine-tuned alcanza 93–98% de accuracy en datasets de fake news en inglés y español respectivamente, con degradación al ~71% en datos reales (dominio shift).

## Referencias cruzadas
- [[nlp-fundacional]]
- [[modelos-espanol]]
- [[wiki/estado-del-arte/fakebert-kaliyar-2021]]
- [[wiki/solucion/pipeline-preprocesamiento]]

## Fuentes
- [[raw/papers/Attention Is All You Need - Vaswani 2017.md]]
- [[raw/papers/BERT Pre-training of Deep Bidirectional Transformers - Devlin 2019.md]]
