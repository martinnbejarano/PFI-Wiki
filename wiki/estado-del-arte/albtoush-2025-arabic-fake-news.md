---
titulo: "Survey: Fake News Detection — State of the Art con foco en árabe"
tipo: fuente
tags: [survey, fake-news, arabic-nlp, bert, deep-learning, datasets, estado-del-arte]
fuentes: ["Fake news detection state-of-the-art review and advances with attention to Arabic language aspects.md"]
actualizado: 2026-04-16
---

# Survey: Fake News Detection — State of the Art con foco en árabe

**Autores:** Eman Salamah Albtoush, Keng Hoon Gan, Saif A. Ahmad Alrababa  
**Publicado en:** PeerJ Computer Science (2025-03-11)  
**Fuente:** [[raw/Fake news detection state-of-the-art review and advances with attention to Arabic language aspects.md]]  
**Relevancia para el PFI:** Alta — aunque el foco es árabe, el survey cubre el estado del arte general de ML/DL/Transformers para fake news detection. Los desafíos del árabe son análogos a los del **español rioplatense** (morfología, dialectos, datasets escasos). Referente directo para la sección "Estado del Arte" del documento PFI.

---

## Contribución principal

Review comprehensivo de fake news detection con dos ejes:
1. **Estado del arte general** de técnicas ML/DL/Transformers
2. **Particularidades del árabe** como idioma de baja disponibilidad de recursos (low-resource language)

La analogía con el **español** (y en especial el español rioplatense/argentino) es directa: ambos son idiomas con datasets escasos, variaciones dialectales, y dependencia de modelos pre-entrenados en inglés que no capturan bien el contexto local.

---

## Tipología de fake news

| Tipo | Descripción |
|---|---|
| Sátira / parodia | Entretenimiento con humor, no intención de engañar (Satirewire, The Onion) |
| Clickbait | Información falsa para generar tráfico y dinero con titulares engañosos |
| Propaganda | Manipulación de creencias/emociones con fines políticos o ideológicos |
| Hoax | Contenido fabricado para entretenimiento, pero que se difunde como verdad |
| Rumores | Afirmaciones no verificadas y exageradas |

---

## Ciclo de vida del fake news

```
Creación → Diseminación → Detección temprana → Propagación
```

- **Creación**: contenido fabricado, titulares sensacionalistas
- **Diseminación**: redes sociales (WhatsApp, Facebook, X, Instagram)
- **Detección temprana**: análisis en tiempo real para cortar la propagación
- **Propagación**: alcance masivo si no se detecta a tiempo

La **detección temprana** es el foco más valioso para el PFI — evitar que la desinformación se propague antes de que sea viral.

---

## Enfoques de detección

| Enfoque | Descripción | Fortaleza | Limitación |
|---|---|---|---|
| Knowledge-based | Fact-checkers manuales (FactCheck, Politifact, Fatabyyano) | Alta precisión | No escala, lento |
| Lingüístico | Análisis gramatical, sintáctico, semántico; TF-IDF, POS tagging | Interpretable | No adapta a dialectos |
| Topic-agnostic | Credibilidad de fuente, estilo de escritura, señales emocionales | Generalizable | Confusión por tono/dialecto |
| Visual-based | Análisis de imágenes, detección de deepfakes | Cubre multimodal | Requiere algoritmos especializados |
| Social context | Propagación, comportamiento de usuario, red de difusión | Capta dinámica social | Datos ruidosos, real-time difícil |

---

## Features de detección — tres niveles

| Nivel | Features |
|---|---|
| Fuente / usuario | Credibilidad del perfil, comportamiento, emociones del publisher |
| Contenido | Estilo, positividad/negatividad, features textuales, visual features, deepfake |
| Propagación | Estructura de red, velocidad, profundidad, popularidad |

---

## Técnicas ML/DL y resultados

### Representaciones de texto

| Técnica | Tipo | Descripción |
|---|---|---|
| TF-IDF | Estadístico | Peso de término relativo al corpus |
| Bag-of-Words | Estadístico | Frecuencia de palabras sin orden |
| Word2Vec / GloVe | Embedding estático | Relaciones semánticas entre palabras |
| ELMo | Embedding contextual | Embeddings según contexto de la oración |
| FastText | Embedding + subpalabra | Incluye información morfológica (útil en español) |
| BERT | Transformer contextual | Deep contextual embeddings bidireccionales |
| AraVec | Word2Vec para árabe | Twitter + Wikipedia árabe |

### Resultados destacados (inglés)

| Método | Dataset | Accuracy / F1 |
|---|---|---|
| TF-IDF + DT/SVM/GBM | COVID-19 (10,700 artículos) | F1 = 93.32% |
| FastText + RNN | Varios | > 98% accuracy |
| BERT + Swin Transformer (multimodal) | Varios | 83.3% |
| TF-IDF + SVM (NER) | ISOT Fake News | 96.74% |
| Word2Vec + LSTM (sentiment) | Varios | 98.14% |

### Resultados para árabe (análogos al español)

| Método | Dataset árabe | Accuracy |
|---|---|---|
| SVM (features lingüísticos) | 4,079 instancias | 95.35% |
| BiLSTM | Dataset árabe actualizado | Mejor DL en corpus pequeño |
| AraGPT2 | Covid19Fakes | 88% |
| RoBERTa + BERT (híbrido) | 27,780 tweets | 96.02% |
| CAMeLBERT | 3,460 tweets | 71.3% (mejor en este set) |
| Mini-BERT | Varios | 98.4% |

> **Nota para el PFI:** Los modelos transformer especializados en el idioma (AraBERT, CAMeLBERT) superan consistentemente a los modelos genéricos en idiomas de baja disponibilidad de recursos. El equivalente en español sería **BETO** (BERT en español) o **XLM-RoBERTa**, que son los candidatos del PFI.

---

## Pre-procesamiento de texto (árabe / idiomas morfológicamente ricos)

Pasos estándar (todos aplicables también al español):
1. **Limpieza**: eliminación de valores nulos, puntuación, números, caracteres especiales, espacios duplicados
2. **Normalización**: estandarización de variantes ortográficas (en español: tildes inconsistentes, ñ, etc.)
3. **Stop word removal**: eliminación de palabras frecuentes no informativas
4. **Tokenización**: separación de texto en tokens
5. **Stemming / Lemmatización**: reducción a raíz morfológica (importante en español)
6. **Eliminación de diacríticos** (árabe) / normalización de acentuación (español)

---

## Datasets referenciados (inglés + árabe)

| Dataset | Tamaño | Dominio | Idioma | Año |
|---|---|---|---|---|
| FakeNewsNet | 23,921 | Política | Inglés | 2020 |
| FNC-1 | 75,385 | Multi-dominio | Inglés | 2020 |
| AraNews | 5,187,957 | Noticias | Árabe | 2020 |
| COVID-19 (Patwa et al.) | 10,700 | Salud | Inglés | 2021 |
| AFND | 606,912 | Noticias | Árabe | 2021 |
| MuMiN | 21M tweets | Social media | Inglés | 2022 |
| ConFake | 72,413 | Multi-dominio | Inglés | 2024 |

---

## Desafíos (directamente aplicables al PFI en español)

### 1. Escasez de datasets
- Los datasets disponibles son limitados, de un solo dominio, o no representan dialectos locales
- **Para el PFI**: construir/adaptar dataset en español argentino es un desafío central — Chequeado.com es la fuente más relevante

### 2. Detección temprana
- La detección antes de la propagación masiva requiere análisis en tiempo real
- Señales tempranas: fuentes cuestionables, titulares no profesionales, patrones de difusión anómalos

### 3. Extracción de features en idiomas complejos
- Morfología rica, dialectos, variaciones ortográficas — todo aplica al español rioplatense
- Solución: embeddings contextuales (BERT) + pre-procesamiento robusto

---

## Direcciones futuras

- Desarrollar datasets comprensivos que incluyan variantes dialectales
- Integrar GANs para augmentación de datos en idiomas con recursos escasos
- Sistemas híbridos: ML + fact-checking humano
- Aplicaciones en plataformas móviles y web para educación al usuario
- Clustering y análisis de similitud semántica entre fuentes

---

## Relevancia directa para el PFI

- **El problema del español es análogo al árabe**: idioma no-inglés, recursos escasos, dialectal, morfología rica
- **BETO / XLM-RoBERTa** son los equivalentes de AraBERT/CAMeLBERT para el PFI
- Los mejores resultados en idiomas low-resource vienen de **transformers especializados en el idioma**
- La estrategia de **feature extraction combinada** (lingüística + contextual) supera enfoques individuales
- **FastText** merece consideración por su manejo de subpalabras — útil para morfología española

---

## Referencias cruzadas

- [[wiki/marco-teorico/tipos-fake-text]]
- [[wiki/marco-teorico/enfoques-deteccion]]
- [[wiki/datasets/datasets-overview]]
- [[wiki/modelos/modelos-overview]]
- [[wiki/estado-del-arte/kwon-jang-2025-survey-fake-text]]

## Fuentes

- [[raw/Fake news detection state-of-the-art review and advances with attention to Arabic language aspects.md]]
