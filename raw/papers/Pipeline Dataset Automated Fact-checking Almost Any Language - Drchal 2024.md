---
tipo: paper
titulo: "Pipeline and Dataset Generation for Automated Fact-checking in Almost Any Language"
autores: [Drchal, Jan, Ullrich, Herbert, Mlynář, Tomáš, Moravec, Václav]
año: 2024
venue: "Neural Computing and Applications (Springer)"
doi: "10.1007/s00521-024-10113-5"
url: "https://link.springer.com/article/10.1007/s00521-024-10113-5"
arxiv: "2312.10171"
relevancia: media
temas: [fact-checking, multilingue, pipeline, dataset-generation, nli, qacg, estado-del-arte]
---

# Pipeline and Dataset Generation for Automated Fact-checking in Almost Any Language

## Referencia completa

Drchal, J., Ullrich, H., Mlynář, T. y Moravec, V. (2024). Pipeline and Dataset Generation for Automated Fact-checking in Almost Any Language. *Neural Computing and Applications*. DOI: 10.1007/s00521-024-10113-5.

## Resumen

Pipeline de fact-checking automático adaptable a múltiples idiomas con bajo costo de adaptación. Usa QACG (Question Answering for Claim Generation) para generar datos de entrenamiento mediante traducción automática, reduciendo costos de anotación manual. Componentes: evidence retrieval + NLI para verificación de claims. Aplicado en checo, polaco, eslovaco e inglés.

## Hallazgos clave

- QACG: genera claims a partir de QA pairs — no requiere anotadores nativos costosos
- El pipeline es reproducible en nuevos idiomas en semanas, no meses
- La calidad del retrieval es el componente más crítico del pipeline
- NLI (Natural Language Inference) como método de verdict prediction funciona bien cross-lingual

## Limitaciones

- **No incluye español**: evaluado solo en idiomas eslavos + inglés
- La calidad de los datos generados automáticamente puede no capturar matices culturales

## Relevancia para el PFI

El método QACG de generación de datos es **directamente exportable al español/argentino**. Marca explícitamente el gap: el pipeline multilingüe no cubre español ni LATAM. Esta limitación puede mencionarse en el Estado del Arte para reforzar la justificación del PFI.

**Clave biblio:** `DrzchalEtAl2024`
