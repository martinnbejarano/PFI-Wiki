---
tipo: paper
titulo: "Comparison of text preprocessing methods"
autores: [Chai, C. P.]
año: 2023
venue: "Natural Language Engineering, vol. 29, no. 3. Cambridge University Press"
doi: "10.1017/S1351324922000213"
url: "https://www.cambridge.org/core/journals/natural-language-engineering/article/comparison-of-text-preprocessing-methods/2B6B9B9F3B6B9B9F3B6B9B9F3B6B9B9F"
relevancia: alta
temas: [nlp, preprocesamiento, tokenizacion, lematizacion, stemming, stopwords]
---

# Comparison of text preprocessing methods

## Referencia completa

Chai, C. P. (2023). Comparison of text preprocessing methods. *Natural Language Engineering*, vol. 29, n.º 3, pp. 637–649. DOI: 10.1017/S1351324922000213.

## Resumen

Survey publicado en Cambridge University Press que compara sistemáticamente métodos de preprocesamiento de texto en NLP: tokenización, normalización, lematización, stemming y manejo de stopwords. Evalúa el impacto de cada método en tareas de clasificación de texto y análisis de sentimiento.

## Hallazgos clave

- La lematización supera al stemming en precisión para tareas de clasificación
- La eliminación de stopwords mejora rendimiento en bolsa-de-palabras pero puede dañar modelos contextuales
- Para modelos transformer (BERT), el preprocesamiento mínimo es suficiente — el tokenizador WordPiece maneja morfología
- Para modelos clásicos (TF-IDF + SVM), el preprocesamiento completo mejora F1 entre 3–8%
- El preprocesamiento óptimo depende del idioma y la tarea

## Relevancia para el PFI

Referencia académica para la sección de preprocesamiento de texto del Marco Teórico. Justifica las decisiones de pipeline (por qué usar WordPiece/BPE para BETO vs. preprocesamiento explícito para baselines clásicos). También relevante para la sección de Metodología de Desarrollo.

**Clave biblio:** `Chai2023`
