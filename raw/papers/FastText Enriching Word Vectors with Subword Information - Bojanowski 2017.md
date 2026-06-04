---
tipo: paper
titulo: "Enriching Word Vectors with Subword Information"
autores: [Bojanowski, Piotr, Grave, Edouard, Joulin, Armand, Mikolov, Tomas]
año: 2017
venue: "Transactions of the Association for Computational Linguistics, vol. 5"
doi: "10.1162/tacl_a_00051"
url: "https://aclanthology.org/Q17-1010/"
arxiv: "1607.04606"
relevancia: media
temas: [fasttext, embeddings, subword, nlp, morfologia, espanol]
---

# Enriching Word Vectors with Subword Information (FastText)

## Referencia completa

Bojanowski, P., Grave, E., Joulin, A. y Mikolov, T. (2017). Enriching Word Vectors with Subword Information. *Transactions of the Association for Computational Linguistics*, vol. 5, pp. 135–146. DOI: 10.1162/tacl_a_00051.

## Resumen

Extiende Word2Vec incorporando información de n-gramas de caracteres. Cada palabra se representa como la suma de los vectores de sus n-gramas de caracteres. Maneja palabras fuera del vocabulario (OOV) y morfología rica — especialmente relevante para idiomas con conjugaciones y derivaciones complejas como el español.

## Hallazgos clave

- Manejo de palabras fuera del vocabulario (OOV): crítico para texto de redes sociales con errores tipográficos, argot, neologismos
- Para idiomas morfológicamente ricos (árabe, checo, alemán, español): mejora significativa sobre Word2Vec
- Meta-Learning disponible pre-entrenado en 157 idiomas incluyendo español (fastText.cc)
- Limitación: no captura contexto (como Word2Vec, es estático)

## Relevancia para el PFI

Relevante como baseline histórico en el Marco Teórico y posible componente para el modelo de fallback. FastText en español es un recurso disponible gratuitamente y podría usarse como representación de texto para el baseline TF-IDF + LR del pipeline de comparación.

**Clave biblio:** `BojanowskiEtAl2017`
