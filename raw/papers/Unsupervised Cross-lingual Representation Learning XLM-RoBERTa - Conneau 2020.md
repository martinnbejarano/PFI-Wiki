---
tipo: paper
titulo: "Unsupervised Cross-lingual Representation Learning at Scale"
autores: [Conneau, Alexis, Khandelwal, Kartikay, Goyal, Naman, Chaudhary, Vishrav, Wenzek, Guillaume, Guzmán, Francisco, Grave, Edouard, Ott, Myle, Zettlemoyer, Luke, Stoyanov, Veselin]
año: 2020
venue: "Proceedings of ACL 2020"
doi: "10.18653/V1/2020.ACL-MAIN.747"
url: "https://aclanthology.org/2020.acl-main.747/"
arxiv: "1911.02116"
relevancia: alta
temas: [xlm-roberta, multilingue, pre-entrenamiento, cross-lingual, nlp, bert]
citaciones: ~8000
---

# Unsupervised Cross-lingual Representation Learning at Scale (XLM-RoBERTa)

## Referencia completa

Conneau, A., Khandelwal, K., Goyal, N., Chaudhary, V., Wenzek, G., Guzmán, F., Grave, E., Ott, M., Zettlemoyer, L. y Stoyanov, V. (2020). Unsupervised Cross-lingual Representation Learning at Scale. *Proceedings of ACL 2020*, pp. 8440–8451. DOI: 10.18653/V1/2020.ACL-MAIN.747.

## Resumen

Presenta XLM-RoBERTa (XLM-R): modelo multilingüe entrenado con la metodología RoBERTa sobre 2.5 TB de texto de CommonCrawl en 100 idiomas. Elimina la necesidad de datos paralelos (traducidos) para aprendizaje cross-lingual. Supera a mBERT en +14.6% promedio en XNLI.

## Hallazgos clave

- Entrenado en 2.5 TB de CommonCrawl filtrado en 100 idiomas, incluyendo español
- XLM-R base: 12 capas, 768 dim, 125M params; XLM-R large: 24 capas, 1024 dim, 355M params
- Supera a mBERT en todas las evaluaciones cross-lingual: +14.6% en XNLI promedio
- Tokens con SentencePiece (250k vocab), ventaja sobre WordPiece de BERT para idiomas morfológicamente ricos
- Disponible en HuggingFace: `xlm-roberta-base` y `xlm-roberta-large`

## Relevancia para el PFI

Candidato principal para el clasificador de desinformación, especialmente útil cuando el dataset de entrenamiento es pequeño (se puede aprovechar el pre-entrenamiento multilingüe). En el paper de Ecuador (Toapanta 2024), XLM-RoBERTa aparece indirectamente a través de sus derivados. Compararlo con BETO y RoBERTuito en los experimentos es fundamental.

**Clave biblio:** `ConneauEtAl2020`
