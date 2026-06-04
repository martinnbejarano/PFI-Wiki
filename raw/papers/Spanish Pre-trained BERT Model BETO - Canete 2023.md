---
tipo: paper
titulo: "Spanish Pre-trained BERT Model and Evaluation Data"
autores: [Cañete, José, Chaperon, Gabriel, Fuentes, Rodrigo, Ho, Jou-Hui, Kang, Hojun, Pérez, Jorge]
año: 2023
venue: "arXiv (versión extendida del workshop paper PML4DC @ ICLR 2020)"
doi: "10.48550/arXiv.2308.02976"
arxiv: "2308.02976"
url: "https://arxiv.org/abs/2308.02976"
github: "https://github.com/dccuchile/beto"
relevancia: alta
temas: [beto, bert, espanol, nlp-espanol, pre-entrenamiento, clasificacion]
---

# Spanish Pre-trained BERT Model and Evaluation Data (BETO)

## Referencia completa

Cañete, J., Chaperon, G., Fuentes, R., Ho, J.-H., Kang, H. y Pérez, J. (2023). Spanish Pre-trained BERT Model and Evaluation Data. arXiv: 2308.02976. [Versión workshop original en PML4DC @ ICLR 2020.]

## Resumen

Presenta BETO, un modelo BERT entrenado exclusivamente en español. Entrenado sobre ~3 mil millones de palabras del corpus Spanish Wikipedia + CCNet + OPUS. Disponible en dos versiones: cased (con distinción mayúsculas/minúsculas) y uncased. Evaluado sobre POS tagging, NER, MLDoc, XNLI y PawS-X.

## Hallazgos clave

- Arquitectura: 12 capas, 768 dimensiones, 12 cabezas de atención (mismo tamaño que BERT-base)
- Tokenizador WordPiece con vocabulario de 31.000 tokens en español
- Supera a mBERT (multilingual BERT) en todas las tareas evaluadas en español
- Disponible en HuggingFace: `dccuchile/bert-base-spanish-wwm-cased`
- Creado por el grupo NLP de la Universidad de Chile (DCC UChile)

## Relevancia para el PFI

BETO es uno de los dos modelos candidatos principales para el clasificador de fake news en español (junto con XLM-RoBERTa). El Marco Teórico debe dedicar una subsección a modelos de lenguaje en español; BETO es la referencia central. Los experimentos del PFI deben comparar BETO vs. XLM-RoBERTa vs. RoBERTuito.

**Clave biblio:** `CañeteEtAl2023`
