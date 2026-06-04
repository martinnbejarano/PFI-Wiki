---
tipo: paper
titulo: "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding"
autores: [Devlin, Jacob, Chang, Ming-Wei, Lee, Kenton, Toutanova, Kristina]
año: 2019
venue: "Proceedings of NAACL-HLT 2019"
doi: ""
acl: "N19-1423"
url: "https://aclanthology.org/N19-1423/"
arxiv: "1810.04805"
relevancia: alta
temas: [bert, transformers, pre-entrenamiento, fine-tuning, nlp, clasificacion]
citaciones: ~90000
---

# BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding

## Referencia completa

Devlin, J., Chang, M.-W., Lee, K. y Toutanova, K. (2019). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. *Proceedings of NAACL-HLT 2019*, pp. 4171–4186. ACL Anthology: N19-1423.

## Resumen

Introduce BERT (*Bidirectional Encoder Representations from Transformers*): modelo de lenguaje pre-entrenado de forma bidireccional mediante dos tareas: *Masked Language Modeling* (MLM) y *Next Sentence Prediction* (NSP). Al agregar una única capa de salida sobre el encoder pre-entrenado, logra state of the art en 11 tareas de NLP con fine-tuning mínimo.

## Hallazgos clave

- Pre-entrenamiento bidireccional: cada token ve contexto izquierdo y derecho simultáneamente (a diferencia de GPT, que es unidireccional)
- BERT-base: 12 capas encoder, 768 dimensiones, 12 cabezas de atención, 110M parámetros
- BERT-large: 24 capas, 1024 dimensiones, 16 cabezas, 340M parámetros
- Fine-tuning con una sola capa sobre la representación [CLS] para clasificación de texto
- Resultados en GLUE benchmark: supera el estado del arte en todas las tareas con margen significativo
- Base de BETO (español), AraBERT (árabe), XLM-RoBERTa y cientos de modelos de dominio específico

## Relevancia para el PFI

Paper de referencia central para justificar el uso de BETO y XLM-RoBERTa en el sistema. El Marco Teórico debe describir la arquitectura BERT antes de introducir los modelos en español. El mecanismo de fine-tuning explicado aquí es exactamente el que se aplica al clasificador de fake news.

**Clave biblio:** `DevlinEtAl2019`
