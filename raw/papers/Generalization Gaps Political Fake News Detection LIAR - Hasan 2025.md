---
tipo: paper
titulo: "Generalization Gaps in Political Fake News Detection: An Empirical Study on the LIAR Dataset"
autores: [Hasan, S. Mahmudul, Roy, Shaily, Nafis, Akib Jawad]
año: 2025
venue: "arXiv preprint"
doi: "10.48550/arXiv.2512.18533"
arxiv: "2512.18533"
url: "https://arxiv.org/abs/2512.18533"
relevancia: media
temas: [liar, generalizacion, fake-news, politica, svm, roberta, evaluacion, estado-del-arte]
---

# Generalization Gaps in Political Fake News Detection: An Empirical Study on the LIAR Dataset

## Referencia completa

Hasan, S. M., Roy, S. y Nafis, A. J. (2025). Generalization Gaps in Political Fake News Detection: An Empirical Study on the LIAR Dataset. arXiv: 2512.18533.

## Resumen

Evaluación diagnóstica sistemática de 9 algoritmos ML sobre el dataset LIAR para investigar el problema de generalización en clasificación de desinformación política. Compara SVM, Random Forest, Decision Tree, Naive Bayes, BERT, RoBERTa y modelos ensemble.

## Hallazgos clave

- **SVM lineal (accuracy 62.4%) iguala a RoBERTa (accuracy 62.0%)** en LIAR 6 clases
- Los ensemble tree-based alcanzan >99% en training pero colapsan a ~25% en test: sobreajuste severo
- El techo de F1 ponderado para 6 clases no supera 0.32 con ningún modelo
- **Aumentar la complejidad del modelo sin conocimiento externo tiene rendimientos decrecientes**
- El cuello de botella es la calidad y cantidad de datos, no la capacidad del modelo

## Limitaciones

- Solo LIAR (inglés, político US)
- No propone solución, solo diagnóstico

## Relevancia para el PFI

Evidencia fundamental para justificar la arquitectura del sistema: el módulo de evidence retrieval (contraste con web search / Chequeado) es más valioso que escalar el modelo de clasificación. Citar al justificar por qué el sistema incluye búsqueda de evidencias externas.

**Clave biblio:** `HasanEtAl2025`
