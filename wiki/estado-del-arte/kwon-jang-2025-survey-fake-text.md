---
titulo: "Survey: Fake Text Detection — Misinformation y LM-Generated Texts"
tipo: fuente
tags: [survey, fake-news, misinformacion, llm-detection, deep-learning, estado-del-arte]
fuentes: ["A Comprehensive Survey of Fake Text Detection on Misinformation and LM-Generated Texts.md"]
actualizado: 2026-04-16
---

# Survey: Fake Text Detection — Misinformation y LM-Generated Texts

**Autores:** Soonchan Kwon, Beakcheol Jang  
**Publicado en:** IEEE Access (2025)  
**Fuente:** [[raw/A Comprehensive Survey of Fake Text Detection on Misinformation and LM-Generated Texts.md]]  
**Relevancia para el PFI:** Alta — ofrece el mapa completo de técnicas de detección, desde enfoques clásicos hasta LLMs. Marco de referencia directo para justificar la elección de modelo en el PFI.

---

## Contribución principal

Primer survey que unifica sistemáticamente dos grandes ramas del "fake text":
1. **Misinformación** (fake news, rumores, desinformación, hate speech, reviews falsos)
2. **Texto generado por LMs** (ChatGPT, Gemini — texto artificialmente creado)

El paper argumenta que ambos problemas comparten desafíos comunes y que los detectores de uno pueden potenciar al otro.

---

## Marco conceptual: taxonomía de fake text

```
Fake Text
├── Misinformación
│   ├── Fake news
│   ├── Rumores
│   ├── Desinformación (intencional)
│   ├── Hate speech
│   └── Reviews falsos
└── Texto generado por LM
    ├── Spam / Phishing masivo
    ├── Sesgos heredados del entrenamiento
    ├── Deshonestidad académica
    └── Alucinaciones
```

Distinción clave: **misinformación** = falso por contenido; **LM-generated** = falso por origen.

---

## Técnicas de detección de misinformación

### 1. Enfoques tradicionales

| Subtipo | Métodos | Ventaja | Limitación |
|---|---|---|---|
| Feature-based | TF-IDF, n-gramas, Bayesian classifiers | Interpretable, eficiente | No adapta a nuevos patrones, sin semántica |
| ML clásico | SVM, LR, Random Forest, Decision Tree | Simple, bien estudiado | Limitado en contextos dinámicos |

Ejemplo destacado: **CSI model** (Capture, Score, Integrate) — combina texto del artículo + reacciones de usuarios + perfil del difusor.

### 2. Deep learning

| Subtipo | Métodos representativos |
|---|---|
| Redes neuronales (CNN/RNN/LSTM) | CNN para extracción de features, RNN para secuencias, LSTM para dependencias largas |
| Attention-based | AIM (Attention-based Identification of Misinformation), ARC (attention-residual network) |
| GNN (Graph Neural Networks) | CompareNet, DDGCN (Double Dynamic Graph Convolutional Network) — modelan propagación |
| Multimodal (texto + imagen) | Event-adversarial NN, variational autoencoders multimodales |

Logro notable: ensemble de BERT + ALBERT + XLNet alcanzó **99% accuracy** en fake news de COVID-19.

### 3. Enfoques basados en información

- **Content-based**: análisis de lingüística, sentimiento, keywords del texto
- **Context-based**: patrones de posting, interacciones entre usuarios, tendencias temporales
- **Propagation-based**: estructura y velocidad de difusión en redes (PTK — Propagation Tree Kernel)

Modelo destacado: **FANG** (Factual News Graph) — grafo de contexto social de alta resolución.

### 4. Human aid-based

- Fact-checking manual + NLP de apoyo
- Crowdsourcing (usuarios que etiquetan noticias como falsas)
- LLMs como detectores (Chen & Shu: ChatGPT para cross-validación de claims)
- Sistema Detective: curación + verificadores expertos de terceros

---

## Técnicas de detección de texto generado por LM

### 1. Estadístico

- **GLTR** (Giant Language Model Test Room): analiza probabilidad de palabras, entropía, ranking
- **DetectGPT**: hipótesis de que muestras del modelo tienen curvatura log-likelihood más negativa
- **Fast-DetectGPT**: versión optimizada de DetectGPT
- **Watermarking**: SWEET (selective watermarking via entropy thresholding), métodos criptográficos

### 2. Generativo

- **Grover** (2019): generador de fake news → el mejor detector de Grover era Grover mismo (0.92 accuracy)
- **fakeRoBERTa**: RoBERTa fine-tuned en reviews falsos generados por GPT-2
- **ConDA**: contrastive domain adaptation para texto sin etiquetas

### 3. Adversarial / robustez

- **RADAR**: adversarial training paraphraser + detector
- Ataques por paraphrase reducen accuracy de detectores existentes significativamente

---

## Limitaciones identificadas

1. **Calidad de datasets**: escasos, sesgados, no representan diversidad de idiomas y culturas
2. **Naturaleza cambiante del fake text**: LLMs mejoran continuamente, detectores se desactualizan
3. **Falsos positivos**: texto humano puede ser marcado como generado por IA
4. **Aplicaciones reales**: la mayoría de la investigación es solo algoritmos, no deployments

---

## Direcciones futuras

- Investigación domain-specific (salud, legal, finanzas)
- Datasets más grandes, diversos y multilingües
- Técnicas adaptativas frente a LLMs que evolucionan
- Reducción de falsos positivos con criterios claros de error aceptable
- Sistemas reales desplegados en plataformas sociales

---

## Relevancia directa para el PFI

- Justifica usar **modelos transformer (BERT/RoBERTa)** como backbone del clasificador
- Sugiere incorporar **features de contexto** (fuente, propagación) además del texto puro
- El enfoque **content + context** es la combinación que mejores resultados da en la literatura
- El modelo **CSI (texto + usuario + fuente)** es un referente para la arquitectura del PFI
- Los **grafos de propagación** están fuera del alcance del PFI (reconocido explícitamente)

---

## Referencias cruzadas

- [[wiki/marco-teorico/tipos-fake-text]]
- [[wiki/marco-teorico/enfoques-deteccion]]
- [[wiki/modelos/modelos-overview]]
- [[wiki/estado-del-arte/albtoush-2025-arabic-fake-news]]

## Fuentes

- [[raw/A Comprehensive Survey of Fake Text Detection on Misinformation and LM-Generated Texts.md]]
