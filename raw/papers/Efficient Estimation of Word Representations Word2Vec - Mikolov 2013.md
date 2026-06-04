---
tipo: paper
titulo: "Efficient Estimation of Word Representations in Vector Space"
autores: [Mikolov, Tomas, Chen, Kai, Corrado, Greg, Dean, Jeffrey]
año: 2013
venue: "Workshop at ICLR 2013"
doi: "10.48550/arXiv.1301.3781"
arxiv: "1301.3781"
url: "https://arxiv.org/abs/1301.3781"
relevancia: alta
temas: [word2vec, embeddings, representacion-vectorial, nlp, skip-gram, cbow]
citaciones: ~85000
---

# Efficient Estimation of Word Representations in Vector Space (Word2Vec)

## Referencia completa

Mikolov, T., Chen, K., Corrado, G. y Dean, J. (2013). Efficient Estimation of Word Representations in Vector Space. *Workshop at ICLR 2013*. arXiv: 1301.3781.

## Resumen

Introduce Word2Vec: dos arquitecturas para aprender representaciones vectoriales densas de palabras a partir de corpus de texto sin supervisión. Skip-gram: predice palabras del contexto dado el término central. CBOW (Continuous Bag of Words): predice el término central dadas las palabras del contexto.

## Hallazgos clave

- Vectores de palabras capturan relaciones semánticas y sintácticas: rey - hombre + mujer ≈ reina
- Skip-gram funciona mejor con datos escasos; CBOW es más eficiente computacionalmente
- Entrenado en 100 mil millones de palabras de Google News
- 300 dimensiones típicas; vectores pre-entrenados disponibles públicamente
- Antecedente directo de GloVe, FastText y embeddings contextuales (BERT)

## Relevancia para el PFI

Paper seminal obligatorio para la evolución histórica de representaciones de texto en el Marco Teórico: bag-of-words → Word2Vec → GloVe/FastText → BERT. No se usa directamente en el sistema propuesto (que usa BERT/BETO), pero su presentación es necesaria para justificar por qué los transformers son superiores.

**Clave biblio:** `MikolovEtAl2013`
