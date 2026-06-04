---
tipo: paper
titulo: "Attention Is All You Need"
autores: [Vaswani, Ashish, Shazeer, Noam, Parmar, Niki, Uszkoreit, Jakob, Jones, Llion, Gomez, Aidan N., Kaiser, Łukasz, Polosukhin, Illia]
año: 2017
venue: "Advances in Neural Information Processing Systems 30 (NeurIPS 2017)"
doi: ""
arxiv: "1706.03762"
url: "https://arxiv.org/abs/1706.03762"
relevancia: alta
temas: [transformer, atencion, arquitectura, nlp, deep-learning]
citaciones: ~173000
---

# Attention Is All You Need

## Referencia completa

Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł. y Polosukhin, I. (2017). Attention Is All You Need. *Advances in Neural Information Processing Systems 30 (NeurIPS 2017)*, pp. 5998–6008. arXiv: 1706.03762.

## Resumen

Propone la arquitectura Transformer, basada completamente en mecanismos de atención sin recurrencia ni convolución. Introduce el mecanismo de *multi-head self-attention* y la codificación posicional. Reemplaza las redes RNN/LSTM en tareas secuenciales de NLP, permitiendo paralelización total del entrenamiento.

## Hallazgos clave

- Arquitectura encoder-decoder compuesta únicamente por capas de atención y redes feed-forward
- *Multi-head attention*: aplica atención en paralelo desde múltiples subespacios de representación
- Escala mejor que RNNs: la distancia entre cualquier par de tokens es O(1) en capas de atención vs. O(n) en RNNs
- BLEU 28.4 en traducción inglés-alemán (state of the art en 2017)
- Base de toda la familia BERT, GPT, T5, XLM-RoBERTa y modelos subsiguientes

## Relevancia para el PFI

Paper fundacional obligatorio en el Marco Teórico. Toda la arquitectura del sistema propuesto (BETO, XLM-RoBERTa) se basa directamente en este trabajo. La sección de Marco Teórico sobre "Arquitectura Transformer" debe citar este paper como fuente primaria.

**Clave biblio:** `VaswaniEtAl2017`
