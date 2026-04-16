---
titulo: Enfoques de Detección de Desinformación — Taxonomía y Comparativa
tipo: concepto
tags: [marco-teorico, deteccion, ml, deep-learning, nlp, clasificacion, estado-del-arte]
fuentes: ["A Comprehensive Survey of Fake Text Detection on Misinformation and LM-Generated Texts.md", "Fake news detection state-of-the-art review and advances with attention to Arabic language aspects.md"]
actualizado: 2026-04-16
---

# Enfoques de Detección de Desinformación — Taxonomía y Comparativa

## Mapa de enfoques

```
Detección de desinformación
├── Por METODOLOGÍA
│   ├── Tradicional (feature-based + ML clásico)
│   ├── Deep Learning (CNN, RNN, LSTM, Attention, GNN)
│   └── Transformers (BERT, RoBERTa, XLM-RoBERTa, GPT)
│
├── Por TIPO DE INFORMACIÓN ANALIZADA
│   ├── Contenido (texto, imagen, video)
│   ├── Contexto (fuente, usuario, metadata)
│   └── Propagación (estructura de difusión, temporalidad)
│
└── Por ROL HUMANO
    ├── Automático (modelo solo)
    ├── Human-aided (crowdsourcing, fact-checkers + modelo)
    └── Híbrido (LLM + human verification)
```

---

## Enfoque 1: Tradicional

### Feature-based

Extrae atributos explícitos del texto para clasificar.

| Técnica | Descripción |
|---|---|
| TF-IDF | Peso de término = frecuencia en doc × inversa de frecuencia en corpus |
| N-gramas | Secuencias de N palabras como features |
| POS tagging | Frecuencia de categorías gramaticales (sustantivos, verbos, adverbios) |
| Stylometric features | Longitud de oraciones, vocabulario único, complejidad sintáctica |

**Fortaleza:** interpretable, eficiente computacionalmente  
**Limitación:** no captura semántica, no adapta a nuevos patrones

### ML clásico

Modelos que aprenden patrones de features extraídas:

| Modelo | Uso |
|---|---|
| SVM (Support Vector Machine) | Clasificación con margen máximo — muy usado en NLP |
| Logistic Regression (LR) | Baseline estándar, sorprendentemente competitivo |
| Random Forest (RF) | Ensemble de árboles, robusto a ruido |
| Decision Tree (DT) | Interpretable, baseline simple |
| Naive Bayes (NB) | Rápido, bueno en texto |

---

## Enfoque 2: Deep Learning

### Redes neuronales estándar

| Arquitectura | Uso en detección |
|---|---|
| **CNN** (Convolutional NN) | Extracción de features locales; bueno para patrones de n-gramas |
| **RNN** (Recurrent NN) | Procesamiento secuencial; captura dependencias temporales |
| **LSTM** (Long Short-Term Memory) | Variante de RNN con memoria a largo plazo; estándar para secuencias largas |
| **GRU** (Gated Recurrent Unit) | Variante de LSTM más eficiente |
| **BiLSTM** | LSTM bidireccional; capta contexto en ambas direcciones |

### Attention-based

El mecanismo de atención permite al modelo "enfocarse" en las partes más relevantes de la entrada.

- **AIM** (Attention-based Identification of Misinformation): detecta misinformación por máxima atención en el texto
- **ARC** (Attention-Residual network): incluye dependencias de largo alcance vía atención

### GNN (Graph Neural Networks)

Especialmente útiles para **modelar propagación** en redes sociales.

| Modelo | Descripción |
|---|---|
| CompareNet | Compara noticias contra una base de conocimiento usando entidades |
| DDGCN | Double Dynamic GCN — modela propagación dinámica de noticias |
| BI-GCN | GCN top-down + bottom-up para aspectos causales y estructurales de rumores |
| FANG (Factual News Graph) | Grafo de contexto social de alta resolución |

### Multimodal (texto + imagen)

- Event-adversarial NN — funde features de texto e imagen
- Multimodal variational autoencoder + clasificador binario
- Quantum Multimodal Fusion (QMFND) — texto + imagen, 87.9% accuracy

---

## Enfoque 3: Transformers (estado del arte actual)

Los modelos transformer pre-entrenados en grandes corpus y luego fine-tuneados son el **estado del arte** desde 2019.

| Modelo | Idioma | Notas |
|---|---|---|
| **BERT** | Inglés | Bidirectional Encoder; estándar de referencia |
| **RoBERTa** | Inglés | BERT optimizado, más robusto |
| **XLNet** | Inglés | Autoregresivo + bidireccional |
| **ALBERT** | Inglés | BERT comprimido, mismo rendimiento con menos parámetros |
| **XLM-RoBERTa** | Multilingüe | RoBERTa entrenado en 100+ idiomas — candidato principal para el PFI |
| **BETO** | Español | BERT entrenado en español — candidato principal para el PFI |
| **AraBERT / CAMeLBERT** | Árabe | Equivalente a BETO para árabe |
| **GPT / ChatGPT** | Multilingüe | Generativo; también usado como detector |

### Resultados transformer para fake news

- Ensemble BERT + ALBERT + XLNet → **99% accuracy** en COVID-19 fake news (inglés)
- RoBERTa + BERT híbrido → **96.02%** en 27,780 tweets (árabe)
- Mini-BERT → **98.4%** vs DT/RF/NB/LSV (árabe)
- BERT + SVM (lingüístico) → **96.73%** en 72,000 artículos (inglés)

---

## Clasificación por información analizada

### Content-based

Analiza el texto o contenido multimedia en sí mismo.

- Características lingüísticas: sintaxis, semántica, estilo
- Análisis de sentimiento
- Reconocimiento de entidades nombradas (NER)
- Características visuales (para imágenes)

### Context-based

Va más allá del contenido — analiza el contexto en que existe.

- Patrones de posting del usuario
- Metadata: timestamp, geolocalización, plataforma
- Interacciones: likes, shares, comentarios
- Perfil de credibilidad del publicador

### Propagation-based

Analiza cómo se difunde la información.

| Modelo | Técnica |
|---|---|
| PTK (Propagation Tree Kernel) | Similitud entre árboles de propagación de rumores |
| CSI model | Integra texto + reacciones de usuarios + perfil del difusor |
| Autoencoder de red de propaganda | Embedding de red parcial para detección temprana |
| Time-series classifier | Propaga como serie temporal multivariada (RNN + CNN) |

**Para el PFI:** la propagación está fuera del alcance (declarado en `propuesta.md`), pero los features de **contexto de fuente** sí están en scope.

---

## Comparativa general de enfoques

| Enfoque | Accuracy típico | Interpretabilidad | Costo computacional | Generalización |
|---|---|---|---|---|
| TF-IDF + SVM | Buena (90-97%) | Alta | Bajo | Media |
| LSTM | Muy buena (92-98%) | Baja | Medio | Media |
| BERT fine-tuned | Excelente (95-99%) | Muy baja | Alto | Alta |
| GNN propagación | Excelente | Baja | Alto | Alta (propagación) |
| Ensemble Transformer | Estado del arte | Muy baja | Muy alto | Muy alta |

---

## Selección justificada para el PFI

Según la literatura, el mejor enfoque para el PFI es:

1. **Transformer en español** (BETO o XLM-RoBERTa) como clasificador principal de contenido
2. **Features de credibilidad de fuente** como señal de contexto adicional
3. **Contraste semántico** contra corpus confiable (Chequeado.com) como feature de información
4. Baseline de comparación: TF-IDF + LR (estándar en la literatura)

Esta combinación está respaldada por múltiples papers de este survey y representa el estado del arte para idiomas con recursos limitados.

---

## Referencias cruzadas

- [[wiki/marco-teorico/tipos-fake-text]]
- [[wiki/modelos/modelos-overview]]
- [[wiki/estado-del-arte/kwon-jang-2025-survey-fake-text]]
- [[wiki/estado-del-arte/albtoush-2025-arabic-fake-news]]
- [[wiki/solucion/arquitectura]]

## Fuentes

- [[raw/A Comprehensive Survey of Fake Text Detection on Misinformation and LM-Generated Texts.md]]
- [[raw/Fake news detection state-of-the-art review and advances with attention to Arabic language aspects.md]]
