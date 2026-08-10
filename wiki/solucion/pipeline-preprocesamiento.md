---
titulo: Pipeline de Preprocesamiento y Flujo de Datos
tipo: solución
tags: [pipeline, preprocesamiento, nlp, limpieza, español, xlm-t]
actualizado: 2026-08-13
---

# Pipeline de Preprocesamiento y Flujo de Datos

## Resumen

El pipeline procesa texto crudo de Twitter/X hasta la entrada del clasificador del Módulo 1. Incluye limpieza, normalización, tokenización y manejo del español rioplatense.

**Flujo general:**
```
Texto crudo → Limpieza → Normalización → Tokenización → Modelo XLM-T → score_nlp
```

## El principio que ordena todo el pipeline

> **Preprocesar es adaptarse al pre-entrenamiento del modelo, no "limpiar" el texto.**

Esta página describía hasta el 2026-08-13 un preprocesamiento pensado para BETO —remover emojis, menciones y hashtags, y pasar todo a minúsculas—. Es correcto para un modelo entrenado sobre Wikipedia y **es lo peor posible para uno entrenado sobre tuits**.

Con la ratificación de XLM-T (ver [[wiki/modelos/modelos-overview]]) la regla se invierte. XLM-T fue pre-entrenado sobre ~198 millones de publicaciones de Twitter: los emojis, los hashtags y las menciones **estaban presentes en ese corpus** y el modelo aprendió representaciones para ellos. Borrarlos en inferencia produce una distribución de entrada que el modelo nunca vio, y anula justamente la ventaja de dominio que motivó elegirlo.

Hay una segunda razón, específica de esta tarea. El emoji 😱, la exclamación repetida y la mayúscula sostenida **son la señal**: el Módulo 1 detecta lenguaje sensacionalista y manipulador, no el contenido factual. Removerlos elimina los rasgos que el módulo tiene que clasificar.

| Operación | Correcto para BETO | Correcto para XLM-T | Por qué |
|---|---|---|---|
| Emojis | Remover | **Conservar** | Estaban en el corpus y son señal de registro emotivo |
| Hashtags | Remover el `#` | **Segmentar, conservar el texto** | `#DólarBlue` aporta contenido |
| Menciones | Remover | **Reemplazar por `@usuario`** | Token especial: conserva la estructura sin el dato personal |
| URLs | Remover | **Reemplazar por `http`** | Su presencia informa; el destino no |
| Mayúsculas | Pasar a minúsculas | **Conservar** | `URGENTE` en mayúscula es la señal |
| Signos repetidos | Colapsar | **Conservar** | `!!!` es énfasis artificial, o sea señal |
| Números | Reemplazar por `<NUM>` | **Conservar** | Ver la advertencia siguiente |

---

## 1. FLUJO DE DATOS COMPLETO (end-to-end)

### Entrada
```
Fuente: Twitter/X (detección); medios de referencia como evidencia del Módulo 3
Formato: texto libre con menciones, URLs, emojis y caracteres especiales

Ejemplo:
"😱 URGENTE: El dólar cierra a $5000!!! 🚨
Ver más en https://t.co/xyz
@MinEconomia desmiente pero ojo... #Inflación #Argentina"
```

### Salida (Módulo 1 — clasificador NLP)
```json
{
  "text_original": "😱 URGENTE: El dólar cierra a $5000!!! ...",
  "text_preprocesado": "😱 URGENTE: El dólar cierra a $5000!!! 🚨 http @usuario desmiente pero ojo... Inflación Argentina",
  "score_nlp": 0.78,
  "clase": "falso",
  "modelo_version": "xlm-t-ft-2026-08"
}
```

Obsérvese que el texto preprocesado se parece mucho al original. Eso no es falta de procesamiento: es la consecuencia del principio de arriba.

---

## 2. ETAPA 1: LIMPIEZA

### 2.1 Qué se toca y qué no

**Entrada:**
```
"😱 URGENTE: El dólar cierra a $5000!!! 🚨 Ver más en https://t.co/xyz @MinEconomia #Inflación"
```

**Operaciones:**

| Operación | Antes | Después | Razón |
|---|---|---|---|
| Normalizar URLs | `https://t.co/xyz` | `http` | Convención del pre-entrenamiento de XLM-T |
| Normalizar menciones | `@MinEconomia` | `@usuario` | Conserva la estructura sintáctica sin el dato personal |
| Segmentar hashtags | `#Inflación` | `Inflación` | El texto aporta; el `#` no |
| Colapsar espacios y saltos | `"a\n\n  b"` | `"a b"` | Ruido de formato, sin contenido |
| Recortar a 512 tokens | — | — | Límite de la arquitectura |

Todo lo demás —emojis, mayúsculas, signos repetidos, acentos, números— **se conserva**.

**Código Python:**
```python
import re

def preprocesar(texto: str) -> str:
    """Normalización mínima alineada con el pre-entrenamiento de XLM-T."""
    texto = re.sub(r'https?://\S+|www\.\S+', 'http', texto)   # URLs → token
    texto = re.sub(r'@\w+', '@usuario', texto)                # menciones → token
    texto = re.sub(r'#(\w+)', r'\1', texto)                   # hashtag → su texto
    texto = re.sub(r'\s+', ' ', texto).strip()                # espacios y saltos
    return texto

texto = "😱 El dólar sube a $5000!!! 😱😱 @MinEconomia #Argentina https://t.co/xyz"
print(preprocesar(texto))
# 😱 El dólar sube a $5000!!! 😱😱 @usuario Argentina http
```

Cinco líneas. La versión anterior tenía el doble y destruía la señal.

> **Sobre los hashtags compuestos.** `#DólarBlue` segmentado por mayúsculas da `Dólar Blue`, que es mejor entrada que la palabra pegada. Es una mejora opcional: requiere una heurística de partición por mayúsculas y no funciona con hashtags en minúscula sostenida (`#dolarblue`). Queda declarada como refinamiento, no como parte del MVP.

### 2.2 Caracteres del español rioplatense

| Símbolo | Ejemplo | Acción |
|---|---|---|
| Tildes y acentos | investigación | Conservar — el tokenizador los maneja |
| Ñ | niño | Conservar |
| Diéresis | pingüino | Conservar |
| Signos invertidos | ¿Pregunta? ¡Exclamación! | Conservar — son español correcto |
| Comillas tipográficas | "hola" | Normalizar a comilla recta |
| Guion bajo | user\_name | Conservar dentro de menciones ya normalizadas |

**No aplicar `unidecode`.** Quitar los acentos rompe palabras que el tokenizador tiene en vocabulario y no aporta nada: el modelo fue entrenado con texto acentuado.

---

## 3. ETAPA 2: NORMALIZACIÓN

### 3.1 Mayúsculas: no convertir

XLM-T es *cased*: distingue mayúsculas y minúsculas. Además, en esta tarea la mayúscula sostenida **es un rasgo predictivo**: `URGENTE`, `TODAS`, `YA`. Convertir a minúsculas borra una de las señales que el Módulo 1 busca.

Nótese que RoBERTuito, la primera línea de comparación, es *uncased*. Al evaluarlo hay que aplicarle su propio preprocesamiento —el de `pysentimiento.preprocessing`— y no este. Comparar dos modelos con el preprocesamiento del otro es una forma silenciosa de arruinar el experimento.

### 3.2 Números: conservarlos — advertencia importante

La versión anterior de esta página recomendaba reemplazar los números por un token `<NUM>` para reducir vocabulario. **En un detector de desinformación eso es un error grave**, y conviene dejarlo escrito porque parece una buena práctica.

En este dominio el número suele ser exactamente la afirmación falsificable:

```
"El gobierno cerró 500 escuelas"  →  <NUM>
"El gobierno cerró 50 escuelas"   →  <NUM>
```

Con `<NUM>` las dos entradas son idénticas para el modelo, y la diferencia entre ellas es precisamente lo que el sistema tiene que detectar: el Boletín Oficial dice 50 y el tuit dice 500. Es el ejemplo que recorre [[wiki/solucion/metodologia-tecnica]] de punta a punta.

**Regla:** los números se conservan tal cual, con su separador de miles y su símbolo de moneda.

### 3.3 Stop words: no remover

XLM-T está entrenado para procesar oraciones completas; remover artículos y preposiciones destruye la estructura sintáctica que el mecanismo de atención usa. Solo tiene sentido removerlas para el *baseline* de TF-IDF con regresión logística, que no modela orden.

---

## 4. ETAPA 3: TOKENIZACIÓN

XLM-T hereda de XLM-RoBERTa el tokenizador **SentencePiece con vocabulario Unigram de 250.000 piezas**, no WordPiece como BERT. Es relevante por dos razones: cubre los 100 idiomas del pre-entrenamiento original, lo que sostiene la transferencia desde el inglés; y maneja los emojis como piezas propias en lugar de mandarlos a `[UNK]`.

```python
from transformers import AutoTokenizer

tok = AutoTokenizer.from_pretrained("cardiffnlp/twitter-xlm-roberta-base")
print(tok.tokenize("El dólar sube 😱"))
```

La salida son piezas con el prefijo `▁`, que marca inicio de palabra; las palabras poco frecuentes se parten en varias piezas. La partición exacta de cada palabra hay que verificarla ejecutando el tokenizador — depende del vocabulario aprendido y no se puede predecir leyendo el código. No hay que implementar nada: el tokenizador se encarga.

Para el Módulo 3 —extracción y tipificación de la afirmación— sí se usa **spaCy** con `es_core_news_sm`, porque ahí hace falta reconocimiento de entidades y análisis sintáctico, no *embeddings*. Son dos tokenizaciones para dos propósitos distintos y no compiten.

---

## 5. ETAPA 4: CLASIFICACIÓN

El fine-tuning usa `AutoModelForSequenceClassification`, que agrega el cabezal de clasificación sobre el modelo base. No hace falta extraer *embeddings* ni implementar *pooling* a mano: eso solo sería necesario para usar el modelo como extractor de características congelado, que no es el caso.

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

MODELO = "cardiffnlp/twitter-xlm-roberta-base"

class ClasificadorDesinformacion:
    ETIQUETAS = ['verdadero', 'falso', 'no verificable']

    def __init__(self, modelo=MODELO):
        self.tok = AutoTokenizer.from_pretrained(modelo)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            modelo, num_labels=3)
        self.model.eval()

    def predecir(self, texto: str) -> dict:
        limpio = preprocesar(texto)
        inputs = self.tok(limpio, return_tensors="pt",
                          truncation=True, max_length=512)
        with torch.no_grad():
            logits = self.model(**inputs).logits
        probas = F.softmax(logits, dim=-1)[0]
        i = int(probas.argmax())
        return {
            'text_preprocesado': limpio,
            'clase': self.ETIQUETAS[i],
            'score_nlp': float(probas[1]),          # probabilidad de "falso"
            'probabilidades': {e: float(p) for e, p in zip(self.ETIQUETAS, probas)},
        }
```

**Sobre `score_nlp`.** Es la probabilidad de la clase *falso*, no la de la clase más probable. El Módulo 4 espera un valor en [0,1] donde 1 es máxima sospecha (ver [[wiki/solucion/metodologia-tecnica]]); devolver la confianza del argmax daría un número alto también cuando el modelo está seguro de que el contenido es verdadero, e invertiría el veredicto.

**Las tres clases** —verdadero, falso, no verificable— siguen la Decisión 5 de [[wiki/sintesis/decisiones-pendientes-2026-08]]. La clase *no verificable* es la que justifica que exista el Módulo 3: si el texto por sí solo no alcanza, hay que ir a buscar evidencia.

---

## 6. CASOS ESPECIALES EN ESPAÑOL RIOPLATENSE

### 6.1 Voseo

```
Español genérico:   "¿Qué haces tú?"
Español argentino:  "¿Qué hacés vos?"
```

El corpus de XLM-T incluye tuits de toda la hispanohablancia, así que el voseo aparece representado. **Acción:** conservarlo como está.

Es, de todos modos, el punto donde RoBERTuito tiene ventaja teórica: su corpus es exclusivamente en español con fuerte presencia rioplatense. Medir esa diferencia es parte de la comparación experimental.

### 6.2 Léxico argentino

Palabras como *quilombo*, *chamuyar* o *boludo* pueden no estar en el vocabulario. SentencePiece las parte en subpiezas en lugar de marcarlas `[UNK]`, así que degradan pero no se pierden. Si el corpus argentino anotado muestra muchas particiones patológicas, el *fine-tuning* sobre ese corpus es la corrección.

### 6.3 Mezcla de idiomas

```
"El dólar blue está re volátil"
"Me da cringe que digan fake news sin source"
```

Es el caso donde XLM-T supera con claridad a cualquier modelo monolingüe: procesa las piezas en inglés de forma nativa porque el inglés está en su pre-entrenamiento. Con BETO o RoBERTuito estas palabras se degradan a subpiezas fuera de distribución. **Acción:** conservar tal cual.

---

## 7. ESPECIFICACIONES TÉCNICAS

### Recursos

- **RAM:** ≥8 GB para *fine-tuning* local; en inferencia el modelo ocupa ~500 MB, razón por la que corre en Hugging Face y no en Railway (ver [[wiki/solucion/arquitectura]]).
- **GPU:** recomendada para el entrenamiento; la inferencia funciona en CPU.
- **Disco:** ≥5 GB entre modelos y conjuntos de datos.

### Librerías

```bash
pip install transformers torch sentencepiece spacy scikit-learn pandas
python -m spacy download es_core_news_sm
```

`sentencepiece` es obligatorio: sin él, el tokenizador de XLM-T no carga.

### Modelos

| Modelo | Identificador | Parámetros | Rol |
|---|---|---|---|
| **XLM-T** | `cardiffnlp/twitter-xlm-roberta-base` | 125M | ✅ Modelo principal |
| RoBERTuito | `pysentimiento/robertuito-base-uncased` | 125M | Línea de comparación — usar su propio preprocesamiento |
| BETO | `dccuchile/bert-base-spanish-wwm-cased` | 110M | Línea de comparación |
| TF-IDF + regresión logística | — | — | *Baseline* clásico |

> **Errata corregida el 2026-08-13.** Esta página usaba el identificador `dcc-uchile/bert-base-spanish-wwm-uncased`, que **no existe**: la organización en Hugging Face es `dccuchile`, sin guion.

---

## 8. Referencias cruzadas

- [[wiki/modelos/modelos-overview]]
- [[wiki/marco-teorico/modelos-espanol]]
- [[wiki/solucion/metodologia-tecnica]]
- [[wiki/solucion/arquitectura]]
- [[wiki/datasets/dataset-recomendacion]]
- [[wiki/sintesis/decisiones-pendientes-2026-08]]
- [[wiki/proyecto/restricciones-legales-eticas]]

## Referencias

- XLM-T: https://huggingface.co/cardiffnlp/twitter-xlm-roberta-base
- RoBERTuito: https://huggingface.co/pysentimiento/robertuito-base-uncased
- BETO: https://huggingface.co/dccuchile/bert-base-spanish-wwm-cased
- Transformers: https://huggingface.co/docs/transformers/
- spaCy: https://spacy.io/
