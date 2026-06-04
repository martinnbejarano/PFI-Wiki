---
titulo: NLP Fundacional — Tokenización y Embeddings
tipo: concepto
tags: [nlp, embeddings, word2vec, glove, fasttext, tokenizacion, representacion-de-texto]
fuentes: [Efficient Estimation of Word Representations Word2Vec - Mikolov 2013.md, GloVe Global Vectors for Word Representation - Pennington 2014.md, FastText Enriching Word Vectors with Subword Information - Bojanowski 2017.md, Comparison of Text Preprocessing Methods - Chai 2023.md]
actualizado: 2026-06-04
---

# NLP Fundacional — Tokenización y Embeddings

Los sistemas modernos de detección de desinformación requieren transformar texto crudo en representaciones numéricas que preserven información semántica. Este proceso comprende dos etapas consecutivas: preprocesamiento/tokenización y vectorización mediante embeddings.

## Preprocesamiento de texto

Antes de cualquier representación numérica, el texto pasa por una cadena de limpieza y normalización. Chai (2023) sistematiza los métodos de preprocesamiento más efectivos para tareas de clasificación de texto:

1. **Limpieza básica**: eliminación de ruido (HTML, caracteres especiales, URLs, menciones @usuario, hashtags)
2. **Normalización**: conversión a minúsculas, corrección ortográfica, expansión de contracciones
3. **Tokenización**: segmentación en unidades mínimas (tokens). Variantes:
   - *Word tokenization*: divide por espacios y puntuación
   - *Subword tokenization* (BPE, WordPiece): divide palabras en subunidades; robusto ante OOV (*out-of-vocabulary*)
   - *Character-level*: máxima cobertura, alta dimensionalidad
4. **Reducción**: *stemming* (raíz morfológica) o *lemmatización* (forma base canónica)
5. **Filtrado**: eliminación de *stopwords*

Para texto de redes sociales en español, la tokenización subpalabra (WordPiece, como usa BERT) es superior porque maneja slang, neologismos y variantes ortográficas sin vocabulario explícito.

## Embeddings estáticos (2013–2018)

Los *embeddings* representan palabras como vectores densos en un espacio de alta dimensión (~100–300d), donde la distancia geométrica entre vectores refleja similaridad semántica.

### Word2Vec (Mikolov et al., 2013)

Mikolov et al. (2013) propusieron dos arquitecturas de redes neuronales superficiales entrenadas sobre corpus no etiquetados:

- **CBOW** (*Continuous Bag-of-Words*): predice la palabra central a partir del contexto
- **Skip-gram**: predice el contexto a partir de la palabra central

Entrenado sobre 100B palabras de Google News, produce vectores de 300d con propiedades algebráicas notables (el vector `rey − hombre + mujer ≈ reina`). Velocidad de entrenamiento muy alta; adecuado para corpus grandes.

**Limitación clave**: cada palabra tiene un único vector fijo, sin importar el contexto. "Banco" (financiero) y "banco" (asiento) tienen el mismo vector.

### GloVe (Pennington et al., 2014)

*Global Vectors for Word Representation* entrena sobre matrices de co-ocurrencia global del corpus (no ventanas locales como Word2Vec). Captura estadísticas globales del corpus, con mejor desempeño en tareas de analogía y similaridad semántica. Disponible en vectores de 50, 100, 200, 300 dimensiones entrenados sobre Common Crawl (840B tokens).

**Diferencia con Word2Vec**: GloVe optimiza directamente la relación de co-ocurrencia; Word2Vec predice contexto local. En práctica, resultados comparables en la mayoría de tareas.

### FastText (Bojanowski et al., 2017)

Facebook AI extendió Word2Vec con *subword information*: cada palabra se representa como suma de vectores de sus n-gramas de caracteres. Por ejemplo, "correr" = sum(cor, orr, rre, rer, corr, orre, rrer, correr).

**Ventaja crítica para español y redes sociales**: maneja palabras desconocidas, errores ortográficos y morfología rica (conjugaciones, diminutivos, sufijos). "corriendo", "corriste", "correreé" comparten subvectores con "correr".

Disponible en 157 idiomas con vectores pre-entrenados sobre Wikipedia + Common Crawl.

## Embeddings contextuales (2018–presente)

La limitación fundamental de los embeddings estáticos (un vector fijo por palabra) se resuelve con modelos contextuales: el vector de cada token depende de todos los tokens circundantes en la oración.

Esta revolución fue habilitada por la arquitectura Transformer (Vaswani et al., 2017) y concretada en BERT (Devlin et al., 2019). Ver página específica: [[transformers-bert]].

## Comparativa de enfoques de vectorización

| Modelo | Tipo | Contexto | OOV | Idiomas | Tamaño modelo |
|---|---|---|---|---|---|
| Word2Vec | estático | No | No | Pocos | Pequeño |
| GloVe | estático | No | No | Pocos | Pequeño |
| FastText | estático | No | Sí (subword) | 157 | Pequeño |
| BERT | contextual | Sí | Sí (WordPiece) | Multilingüe | Grande |
| BETO | contextual | Sí | Sí (WordPiece) | Español | Grande |

## Relevancia para el PFI

El sistema de detección de desinformación utiliza BETO (BERT en español) como módulo de vectorización contextual principal. Los embeddings estáticos (FastText en español) son útiles como *baseline* rápido y para validar hipótesis antes de fine-tuning completo.

La selección de tokenización subpalabra (WordPiece en BERT/BETO) es especialmente adecuada para el dominio de redes sociales, donde abreviaturas, hashtags y errores ortográficos son frecuentes.

## Referencias cruzadas
- [[transformers-bert]]
- [[modelos-espanol]]
- [[wiki/solucion/pipeline-preprocesamiento]]
- [[wiki/marco-teorico/enfoques-deteccion]]

## Fuentes
- [[raw/papers/Efficient Estimation of Word Representations Word2Vec - Mikolov 2013.md]]
- [[raw/papers/GloVe Global Vectors for Word Representation - Pennington 2014.md]]
- [[raw/papers/FastText Enriching Word Vectors with Subword Information - Bojanowski 2017.md]]
- [[raw/papers/Comparison of Text Preprocessing Methods - Chai 2023.md]]
