---
tipo: paper
titulo: "A Survey on Automated Fact-Checking"
autores: [Guo, Zhijiang, Schlichtkrull, Michael, Vlachos, Andreas]
año: 2022
venue: "Transactions of the Association for Computational Linguistics (TACL), vol. 10"
doi: "10.1162/tacl_a_00454"
url: "https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00454/109469/"
acl: "https://aclanthology.org/2022.tacl-1.11/"
arxiv: "2108.11896"
relevancia: alta
temas: [fact-checking, survey, claim-detection, evidence-retrieval, verdict-prediction, nlp]
---

# A Survey on Automated Fact-Checking

## Referencia completa

Guo, Z., Schlichtkrull, M. y Vlachos, A. (2022). A Survey on Automated Fact-Checking. *Transactions of the Association for Computational Linguistics*, vol. 10, pp. 178–206. DOI: 10.1162/tacl_a_00454.

## Resumen

Survey unificado del pipeline de fact-checking automático. Define y cataloga: (1) claim detection — identificar afirmaciones verificables; (2) evidence retrieval — recuperar evidencia relevante; (3) verdict prediction — clasificar la afirmación como verdadera/falsa/incierta; (4) justification production — explicar la decisión. Revisa datasets, modelos y desafíos abiertos.

## Hallazgos clave

- Pipeline canónico: claim detection → evidence retrieval → verdict prediction → justification
- Los datasets más usados son FEVER (inglés, Wikipedia) y LIAR (inglés, PolitiFact)
- Brecha crítica: la mayoría de los sistemas y datasets son monolingüe en inglés
- La recuperación de evidencia es el cuello de botella del pipeline en producción real
- Los modelos transformer (BERT, RoBERTa) son el estado del arte en verdict prediction
- La producción de justificaciones (explicabilidad) es un problema abierto

## Relevancia para el PFI

**Marco conceptual arquitectural fundamental.** Define el campo académico en el que se inscribe el proyecto. La sección "Fact-checking automático" del Marco Teórico debe describir este pipeline. La arquitectura del sistema propuesto (módulo NLP + credibilidad + contraste + ensemble) se mapea directamente sobre este pipeline.

**Clave biblio:** `GuoEtAl2022`
