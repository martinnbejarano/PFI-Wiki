---
titulo: Pipeline de Preprocesamiento y Flujo de Datos
tipo: solución
tags: [pipeline, preprocesamiento, nlp, limpieza, español]
actualizado: 2026-04-19
---

# Pipeline de Preprocesamiento y Flujo de Datos

## Resumen

El pipeline procesa texto crudo de redes sociales (tweets, posts, artículos) hasta embeddings listos para el modelo BERT. Incluye limpieza, normalización, tokenización y manejo específico de español rioplatense.

**Flujo general:**
```
Texto crudo → Limpieza → Normalización → Tokenización → Vectorización → Modelo NLP
```

---

## 1. FLUJO DE DATOS COMPLETO (end-to-end)

### Entrada
```
Fuente: Twitter/X (detección); medios de confianza (Clarín, Infobae) como evidencia
Formato: Texto libre (con mentions, URLs, emojis, caracteres especiales)

Ejemplo:
"😱 URGENTE: El dólar cierra a $5000!!! 🚨 
Ver más en https://t.co/xyz 
@MinEconomia desmiente pero ojo... #Inflación #Argentina"
```

### Salida (Módulo 1 — NLP Classifier)
```json
{
  "text": "El dólar cierra a 5000 pesos",
  "score_nlp": 0.78,
  "reasoning": "Claim extremista, números sospechosos",
  "preprocessed_text": "dólar cierra 5000 pesos",
  "tokens": ["dólar", "cierra", "5000", "pesos"],
  "embedding": [0.23, -0.45, ..., 0.67]  // 768 dimensiones (BETO)
}
```

---

## 2. ETAPA 1: LIMPIEZA (Cleaning)

### 2.1 Remover/Normalizar caracteres especiales

**Entrada:**
```
"😱 URGENTE: El dólar cierra a $5000!!! 🚨 Ver más en https://t.co/xyz"
```

**Operaciones:**

| Operación | Antes | Después | Razón |
|---|---|---|---|
| Remover emojis | "😱 URGENTE" | "URGENTE" | No aportan significado lingüístico |
| Expandir contracciones | "voy a ir" | "voy a ir" | (No aplica español, pero sí: "dólar$" → "dólar") |
| Remover URLs | "https://t.co/xyz" | "" | No son claims, solo ruido |
| Remover mentions | "@MinEconomia" | "" | Identifican personas, LPDP |
| Remover hashtags | "#Inflación" | "Inflación" | Convertir a texto (sin #) |
| Normalizar números | "$5000!!!" | "5000" | Estandarizar representación |
| Remover caracteres duplicados | "!!!!" | "." | Reducir énfasis artificial |

**Código Python recomendado:**
```python
import re
from unidecode import unidecode

def clean_text(text):
    # Remover URLs
    text = re.sub(r'https?://\S+', '', text)
    # Remover mentions
    text = re.sub(r'@\w+', '', text)
    # Remover hashtags (convertir a palabra)
    text = re.sub(r'#(\w+)', r'\1', text)
    # Remover emojis
    text = re.sub(r'[😀-🙏🌀-🗿\U0001F600-\U0001F64F]', '', text)
    # Normalizar espacios múltiples
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Ejemplo
texto = "😱 El dólar sube a $5000!!! 😱😱 @MinEconomia #Argentina"
print(clean_text(texto))
# Output: "El dólar sube a 5000 Argentina"
```

### 2.2 Manejo de caracteres especiales en español

**Casos especiales del español rioplatense:**

| Símbolo | Ejemplo | Acción |
|---|---|---|
| Tilde / acentos | "investigación" | Mantener (BERT lo maneja bien) |
| Ñ | "España, niño" | Mantener (no es ruido) |
| Diéresis | "pingüino" | Mantener |
| Signos invertidos | "¿Pregunta?" "¡Exclamación!" | Remover de inicio, mantener marcas |
| Comillas | "Dijo 'hola'" | Normalizar a comilla estándar |
| Guiones/guion bajo | "día-a-día, user_name" | Reemplazar con espacio |
| Caracteres latinos extendidos | "café, naïve" | Mantener (es español) |

**Código:**
```python
def normalize_spanish_chars(text):
    # Normalizar comillas
    text = text.replace('"', '"').replace('"', '"')
    # Reemplazar guiones por espacio
    text = re.sub(r'[-_]+', ' ', text)
    # Mantener acentos y ñ (no hacer unidecode completo)
    return text
```

---

## 3. ETAPA 2: NORMALIZACIÓN (Normalization)

### 3.1 Conversión a minúsculas

**Razón:** Reducir variantes del mismo token.

```
ANTES: "El Dólar SUBE A $5000"
DESPUÉS: "el dólar sube a 5000"
```

**Cuidado:** Algunos modelos (como BERT) prefieren **no** convertir a minúsculas completamente porque la mayúscula inicial indica nombre propio. Pero para clasificación de fake news, es generalmente seguro.

**Recomendación:** Convertir a minúsculas (simplificar).

```python
text = text.lower()
```

### 3.2 Manejo de números

**Opciones:**
1. **Mantenerlos:** "dólar 5000" (modelo aprende a detectar números extremos)
2. **Reemplazar por token especial:** "dólar <NUM>" (reducir vocabulario)
3. **Normalizar rangos:** "5000" → "<NUM_HIGH>" (valores sospechosos)

**Recomendación para PFI:** **Opción 2** (reemplazar con `<NUM>`) porque:
- Reduce vocabulario
- BERT tiene vocabulario limitado para números
- Evita sobrecarga de variantes numéricas

```python
def normalize_numbers(text):
    # Reemplazar números por token especial
    text = re.sub(r'\d+[.,]?\d*', '<NUM>', text)
    return text

# Ejemplo
print(normalize_numbers("el dólar sube a 5000 pesos"))
# Output: "el dólar sube a <NUM> pesos"
```

### 3.3 Remover stop words (opcional)

**Stop words en español:** "el", "la", "de", "y", "que", "en", etc.

**Decisión:** 
- ❌ **NO remover para BERT** — BERT está entrenado para procesar stop words, removerlos pierde contexto sintáctico
- ✅ **Remover solo si usas TF-IDF + Logistic Regression** (Módulo 2, credibilidad de fuente)

**Recomendación:** **NO remover para Módulo 1 (NLP). Sí remover para Módulo 2 (features de fuente).**

```python
# Para Módulo 2 (opcional)
from nltk.corpus import stopwords
stop_words_es = set(stopwords.words('spanish'))
tokens = [w for w in tokens if w not in stop_words_es]
```

---

## 4. ETAPA 3: TOKENIZACIÓN (Tokenization)

### 4.1 Tokenización a nivel de palabra

**Opción 1: Simple (espacios)**
```python
tokens = text.split()
# "el dólar sube" → ["el", "dólar", "sube"]
```

**Opción 2: Usando spaCy (recomendado)**
```python
import spacy
nlp = spacy.load("es_core_news_sm")  # Modelo español
doc = nlp("El dólar sube a $5000")
tokens = [token.text for token in doc]
# ["El", "dólar", "sube", "a", "$", "5000"]
```

**Opción 3: Usando NLTK**
```python
from nltk.tokenize import word_tokenize
tokens = word_tokenize("El dólar sube", language='spanish')
```

**Recomendación:** **spaCy** porque:
- Maneja puntuación correctamente
- Tiene modelo en español específico
- Mejor para procesar español rioplatense

### 4.2 Tokenización a nivel de subpalabra (Subword tokenization)

BERT no usa palabra completa, sino **subpalabras** (tokens de WordPiece). Esto lo hace BERT directamente, pero es bueno entender:

```
Palabra: "investigación"
Tokens BERT: ["invest", "##igación"]
```

**Razón:** Palabras rara vez vistas en entrenamiento se rompen en componentes conocidos.

**Para el PFI:** No necesitas implementar esto (BERT lo maneja automáticamente con `BertTokenizer`).

---

## 5. ETAPA 4: VECTORIZACIÓN (Vectorization)

### 5.1 Usando BETO (Transformers)

**BETO:** Versión española de BERT, entrenada en corpus en español.

```python
from transformers import BertTokenizer, BertModel
import torch

# Cargar modelo
model_name = "dcc-uchile/bert-base-spanish-wwm-uncased"  # BETO
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

# Procesar texto
text = "el dólar sube a <NUM> pesos"
inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
outputs = model(**inputs)
embeddings = outputs.last_hidden_state  # [batch_size, seq_len, 768]
```

**Output:**
```
Texto: "el dólar sube a <NUM> pesos"
Embedding: tensor de [1, 7, 768]  
  // 1 documento, 7 tokens, 768 dimensiones
```

### 5.2 Pooling (obtener vector de documento)

BERT produce embedding por token. Para clasificar el documento entero, necesitas un vector único:

**Opción 1: `[CLS]` token (recomendado para clasificación)**
```python
cls_embedding = embeddings[0, 0, :]  # Primer token, 768 dims
```

**Opción 2: Mean pooling**
```python
mean_embedding = embeddings[0].mean(dim=0)
```

**Opción 3: Max pooling**
```python
max_embedding = embeddings[0].max(dim=0)[0]
```

**Recomendación:** **`[CLS]` token** porque BERT está específicamente entrenado para usarlo como resumen de documento.

---

## 6. ETAPA 5: MODELO (Classification)

### 6.1 Fine-tuning BETO

Después de preprocesamiento, el flujo es:

```
Texto crudo
    ↓ [Limpieza + Normalización]
Texto limpio
    ↓ [Tokenización BERT]
IDs de tokens
    ↓ [BETO forward pass]
Embeddings [CLS]
    ↓ [Clasificador lineal (1 capa)]
Logits (raw scores)
    ↓ [Softmax]
Probabilidades: [P(verdadero), P(falso), P(mixto)]
    ↓ [Argmax]
Predicción: VERDADERO / FALSO / MIXTO
```

**Código simplificado:**
```python
from transformers import BertForSequenceClassification, BertTokenizer
import torch.nn.functional as F

model = BertForSequenceClassification.from_pretrained("dcc-uchile/bert-base-spanish-wwm-uncased", 
                                                      num_labels=3)
tokenizer = BertTokenizer.from_pretrained("dcc-uchile/bert-base-spanish-wwm-uncased")

# Inference
text = "el dólar sube a <NUM> pesos"
inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
outputs = model(**inputs)
logits = outputs.logits
probas = F.softmax(logits, dim=-1)
prediction = probas.argmax().item()

print(f"Probabilidades: {probas}")
print(f"Predicción: {['Verdadero', 'Falso', 'Mixto'][prediction]}")
```

---

## 7. PIPELINE COMPLETO (Código unificado)

```python
import re
import spacy
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import torch.nn.functional as F

class DesinformationDetectorPipeline:
    def __init__(self, model_name="dcc-uchile/bert-base-spanish-wwm-uncased"):
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertForSequenceClassification.from_pretrained(model_name, num_labels=3)
        self.nlp = spacy.load("es_core_news_sm")
        self.model.eval()
    
    def clean_text(self, text):
        # Remover URLs
        text = re.sub(r'https?://\S+', '', text)
        # Remover mentions
        text = re.sub(r'@\w+', '', text)
        # Remover hashtags (convertir a palabra)
        text = re.sub(r'#(\w+)', r'\1', text)
        # Remover emojis
        text = re.sub(r'[😀-🙏\U0001F600-\U0001F64F]', '', text)
        # Normalizar espacios
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def normalize_text(self, text):
        # Minúsculas
        text = text.lower()
        # Reemplazar números
        text = re.sub(r'\d+[.,]?\d*', '<NUM>', text)
        return text
    
    def preprocess(self, text):
        text = self.clean_text(text)
        text = self.normalize_text(text)
        return text
    
    def predict(self, text):
        text = self.preprocess(text)
        
        # Tokenizar con BERT
        inputs = self.tokenizer(text, return_tensors="pt", 
                               padding=True, truncation=True, max_length=512)
        
        # Inferencia
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        logits = outputs.logits
        probas = F.softmax(logits, dim=-1)
        prediction = probas.argmax().item()
        score = probas[0][prediction].item()
        
        labels = ['Verdadero', 'Falso', 'Mixto']
        
        return {
            'text_preprocessed': text,
            'prediction': labels[prediction],
            'score': score,
            'probabilities': {labels[i]: probas[0][i].item() for i in range(3)}
        }

# Uso
detector = DesinformationDetectorPipeline()
result = detector.predict("😱 El dólar cierra a $5000!!! @MinEconomia #Argentina")
print(result)
```

**Output:**
```python
{
    'text_preprocessed': 'dólar cierra <NUM> argentina',
    'prediction': 'Falso',
    'score': 0.78,
    'probabilities': {
        'Verdadero': 0.05,
        'Falso': 0.78,
        'Mixto': 0.17
    }
}
```

---

## 8. CASOS ESPECIALES EN ESPAÑOL RIOPLATENSE

### 8.1 Voseo (peculiaridad del español argentino)

```
Español genérico: "¿Qué haces tú?"
Español argentino: "¿Qué hacés vos?"
```

**Implicancia:** BETO está entrenado en español mayormente de España. El voseo no es problema (cubre varios dialectos) pero es bueno saberlo.

**Acción:** Mantener voseo como está (BETO lo procesa correctamente).

### 8.2 Diminutivos y aumentativos

```
"boluda", "boludo", "quilombo", "chamuyar"
```

Palabras argentinas comunes. BETO debería manejarlas, pero si no están en vocabulario:
- Se rompen en subpalabras
- O se marcan como `[UNK]` (desconocido)

**Acción:** Si hay muchos `[UNK]`, considerar fine-tuning en corpus argentino.

### 8.3 Mezcla de idiomas (Spanglish)

```
"El dólar blue está re volátil, boludo"
"Me da cringe que digan fake news sin source"
```

**Implicancia:** BETO es monolingüe (español). Palabras en inglés pueden no procesarse bien.

**Acción:** 
- Mantenerlas (el modelo las procesará como OOV/subpalabras)
- O usar XLM-RoBERTa (multilingüe) en su lugar

---

## 9. ESPECIFICACIONES TÉCNICAS

### Recursos necesarios
- **RAM:** ≥8 GB (para BETO)
- **GPU:** Recomendado (NVIDIA RTX 3060+, pero CPU funciona lentamente)
- **Espacio disco:** ≥5 GB (modelos + datasets)

### Librerías Python
```bash
pip install transformers torch spacy nltk scikit-learn pandas
python -m spacy download es_core_news_sm
```

### Modelos recomendados

| Modelo | Tamaño | Velocidad | Precisión | Recomendación |
|---|---|---|---|---|
| BETO (base) | 110M paráms | Rápido | Alta | ✅ PFI MVP |
| BETO (large) | 340M paráms | Lento | Muy Alta | ❌ Overkill para MVP |
| XLM-RoBERTa (base) | 270M paráms | Rápido | Alta (multiidioma) | ✅ Si quieres multilingual |
| DistilBERT-spanish | 66M paráms | Muy Rápido | Buena | ✅ Si RAM limitada |

---

## 10. Referencia cruzada

- [[wiki/datasets/dataset-recomendacion]]
- [[wiki/solucion/metodologia-tecnica]]
- [[wiki/proyecto/restricciones-legales-eticas]]

## Referencias

- BETO: https://huggingface.co/dcc-uchile/bert-base-spanish-wwm-uncased
- Transformers: https://huggingface.co/docs/transformers/
- spaCy: https://spacy.io/
- NLTK: https://www.nltk.org/

