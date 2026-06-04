---
tipo: paper
titulo: "GloVe: Global Vectors for Word Representation"
autores: [Pennington, Jeffrey, Socher, Richard, Manning, Christopher D.]
año: 2014
venue: "Proceedings of EMNLP 2014"
doi: "10.3115/v1/d14-1162"
url: "https://aclanthology.org/D14-1162/"
acl: "D14-1162"
relevancia: media
temas: [glove, embeddings, representacion-vectorial, nlp, co-ocurrencia]
citaciones: ~30000
---

# GloVe: Global Vectors for Word Representation

## Referencia completa

Pennington, J., Socher, R. y Manning, C. D. (2014). GloVe: Global Vectors for Word Representation. *Proceedings of EMNLP 2014*, pp. 1532–1543. DOI: 10.3115/v1/d14-1162.

## Resumen

Propone GloVe (*Global Vectors*): embeddings de palabras que combinan las ventajas del conteo de co-ocurrencias global con el aprendizaje local de Word2Vec. Entrena una descomposición matricial ponderada sobre la matriz de co-ocurrencias del corpus.

## Hallazgos clave

- Supera a Word2Vec en tareas de analogía de palabras y razonamiento semántico
- Combina eficiencia del conteo matricial global con capacidad de generalización local
- Vectores pre-entrenados en Wikipedia + Gigaword (~6B tokens) disponibles públicamente
- Dimensiones de 50, 100, 200 y 300; el de 300D es el más utilizado en NLP

## Relevancia para el PFI

Incluir en la evolución histórica de embeddings en el Marco Teórico. Puede usarse como baseline comparativo frente a embeddings contextuales (BETO). Prioridad media ya que el sistema principal usa BERT-based models, no GloVe.

**Clave biblio:** `PenningtonEtAl2014`
