---
tipo: paper
titulo: "PolyTruth: Multilingual Disinformation Detection using Transformer-Based Language Models"
autores: [Gouliev, Zaur, Waters, Jennifer, Wang, Chengqian]
año: 2025
venue: "ECML PKDD 2025 (Communications in Computer and Information Science, vol. 2843, Springer 2026)"
doi: "10.48550/arXiv.2509.10737"
arxiv: "2509.10737"
url: "https://arxiv.org/abs/2509.10737"
relevancia: media
temas: [multilingue, desinformacion, transformers, xlm-roberta, rembert, mbert, estado-del-arte]
---

# PolyTruth: Multilingual Disinformation Detection using Transformer-Based Language Models

## Referencia completa

Gouliev, Z., Waters, J. y Wang, C. (2025). PolyTruth: Multilingual Disinformation Detection using Transformer-Based Language Models. *ECML PKDD 2025*, Communications in Computer and Information Science, vol. 2843, pp. 353–367. Springer. arXiv: 2509.10737.

## Resumen

Comparación sistemática de 5 modelos multilingüe (mBERT, XLM, XLM-RoBERTa, RemBERT, mT5) sobre el PolyTruth Disinfo Corpus: 60.486 pares de afirmación falsa vs. corrección factual en 25+ idiomas (incluyendo español), 5 familias lingüísticas, dominios: política, salud, clima, finanzas, conspiración.

## Hallazgos clave

- **RemBERT** logra mejor accuracy general, especialmente en idiomas de bajos recursos
- XLM y mBERT tienen limitaciones importantes cuando los datos de entrenamiento son escasos
- XLM-RoBERTa es competitivo pero no el mejor en todos los idiomas
- El dataset PolyTruth cubre español como parte de los 25 idiomas
- Clasificación binaria: afirmación falsa vs. corrección factual

## Limitaciones

- Sin resultados desagregados por idioma publicados en el resumen público
- El dataset no es específico de LATAM; el español cubierto puede ser mayormente europeo
- RemBERT no está disponible en HuggingFace con el mismo soporte que XLM-RoBERTa

## Relevancia para el PFI

Introduce RemBERT como alternativa a explorar junto con XLM-RoBERTa para el clasificador. El benchmark multilingüe más completo disponible que incluye español. Confirma que el español es un idioma de recursos medios (no bajo) en este contexto.

**Clave biblio:** `GoulievEtAl2025`
