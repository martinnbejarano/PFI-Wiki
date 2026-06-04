---
tipo: paper
titulo: "Fake News Detection: Comparative Evaluation of BERT-like Models and Large Language Models with Generative AI-Annotated Data"
autores: [Raza, Shaina, Paulen-Patterson, Drai, Ding, Chen]
año: 2024
venue: "Knowledge and Information Systems (Springer)"
doi: "10.48550/arXiv.2412.14276"
arxiv: "2412.14276"
url: "https://arxiv.org/abs/2412.14276"
relevancia: media
temas: [bert, llm, comparativa, fake-news, gpt4, llama, clasificacion, estado-del-arte]
---

# Fake News Detection: Comparative Evaluation of BERT-like Models and LLMs with Generative AI-Annotated Data

## Referencia completa

Raza, S., Paulen-Patterson, D. y Ding, C. (2024). Fake News Detection: Comparative Evaluation of BERT-like Models and Large Language Models with Generative AI-Annotated Data. *Knowledge and Information Systems*. arXiv: 2412.14276.

## Resumen

Evaluación comparativa de modelos encoder (BERT, RoBERTa, ALBERT) vs. modelos decoder autoregresivos (Llama2-7B, Mistral-7B) vs. LLMs con prompting (GPT-4o, GPT-4o-mini) para detección de fake news. Dataset etiquetado con GPT-4 + verificación humana, evaluado también en NELA-GT-2022.

## Hallazgos clave

- **BERT-like models superan a LLMs autoregresivos en clasificación supervisada**
- GPT-4o y GPT-4o-mini con few-shot alcanzan 98.6% de accuracy
- LLMs son más robustos ante perturbaciones de texto (ruido, errores tipográficos)
- BERT fine-tuned es más eficiente computacionalmente para inferencia en producción
- La anotación con GPT-4 produce labels de alta calidad comparable a humanos

## Limitaciones

- Dataset en inglés
- La comparación tiene limitaciones por diferencia de tamaño entre modelos (BERT-base vs. Llama2-7B)
- Resultados varían según dataset de evaluación

## Relevancia para el PFI

Justifica el enfoque principal del PFI (fine-tuning de BERT/BETO) sobre usar un LLM grande directamente. La eficiencia computacional y el rendimiento superior en clasificación hacen que BETO/MarIA fine-tuned sea la arquitectura adecuada para un sistema de producción.

**Clave biblio:** `RazaEtAl2024`
