---
tipo: paper
titulo: "RoBERTuito: a pre-trained language model for social media text in Spanish"
autores: [Pérez, Juan Manuel, Furman, Damián Ariel, Alonso Alemany, Laura, Luque, Franco]
año: 2022
venue: "Proceedings of LREC 2022"
doi: "10.48550/arXiv.2111.09453"
arxiv: "2111.09453"
url: "https://arxiv.org/abs/2111.09453"
acl: "https://aclanthology.org/2022.lrec-1.785/"
huggingface: "https://huggingface.co/pysentimiento/robertuito-base-uncased"
relevancia: alta
temas: [robertuito, roberta, espanol, redes-sociales, twitter, nlp-espanol, pre-entrenamiento]
---

# RoBERTuito: a pre-trained language model for social media text in Spanish

## Referencia completa

Pérez, J. M., Furman, D. A., Alonso Alemany, L. y Luque, F. (2022). RoBERTuito: a pre-trained language model for social media text in Spanish. *Proceedings of LREC 2022*, pp. 7235–7243. arXiv: 2111.09453.

## Resumen

Modelo RoBERTa pre-entrenado sobre 500 millones de tweets en español. Diseñado específicamente para texto de redes sociales, con preprocesamiento adaptado a lenguaje informal (emojis, abreviaciones, hashtags, menciones). Evaluado en análisis de sentimiento, detección de ironía, hate speech y análisis de emociones en español.

## Hallazgos clave

- Corpus: 500M tweets en español de 2018–2021 (Argentina, México, España, Colombia, Chile, entre otros)
- Tokenizador BPE adaptado a texto de redes sociales
- Supera a BETO y XLM-RoBERTa en tareas de texto de redes sociales en español
- Disponible en HuggingFace: `pysentimiento/robertuito-base-uncased`
- Creado por pysentimiento (grupo liderado por Juan Manuel Pérez, Universidad de Buenos Aires / CONICET)

## Relevancia para el PFI

**De los tres candidatos (BETO, XLM-RoBERTa, RoBERTuito), este es el más específico para el dominio objetivo del PFI** (Twitter/X, redes sociales en español). El hecho de que incluya tweets argentinos en su corpus de pre-entrenamiento lo hace especialmente adecuado para detectar desinformación en el contexto local. Debe ser uno de los modelos comparados en los experimentos.

**Clave biblio:** `PerezEtAl2022`
