---
tipo: paper
titulo: "Fake News Detection and Fact Checking in X posts from Ecuador Chequea and Ecuador Verifica using Spanish Language Models"
autores: [Toapanta Bernabé, Mariuxi, García-Cumbreras, Miguel Ángel, Ureña-López, L. Alfonso]
año: 2024
venue: "Revista Tecnológica ESPOL (RTE), vol. 36, no. 2"
doi: "10.37815/rte.v36n2.1219"
url: "https://portal.amelica.org/ameli/journal/844/8445194010/html/"
relevancia: alta
temas: [espanol, latam, ecuador, transformers, beto, maria, roberta, twitter, fact-checking, estado-del-arte]
---

# Fake News Detection and Fact Checking in X posts from Ecuador Chequea and Ecuador Verifica using Spanish Language Models

## Referencia completa

Toapanta Bernabé, M., García-Cumbreras, M. Á. y Ureña-López, L. A. (2024). Fake News Detection and Fact Checking in X posts from Ecuador Chequea and Ecuador Verifica using Spanish Language Models. *Revista Tecnológica ESPOL*, vol. 36, n.º 2, pp. 158–173. DOI: 10.37815/rte.v36n2.1219.

## Resumen

Evaluación de 5 modelos transformer en español (MarIA, BERTin, BETO, RoBERTuito, BERTuit) sobre posts de X (Twitter) verificados por dos organizaciones ecuatorianas de fact-checking (Ecuador Chequea y Ecuador Verifica). Dataset: 1.340 ítems (expandidos a 4.640 con SMOTE), 7 categorías de veracidad. Período: enero 2020 – marzo 2024.

## Hallazgos clave

| Modelo | Accuracy | F1 |
|---|---|---|
| MarIA | 96.01% | 0.9597 |
| BERTin | 95.47% | 0.9544 |
| BETO | 93.53% | 0.9345 |
| RoBERTuito | 93.53% | 0.9335 |
| BERTuit | 93.43% | 0.9326 |

- **MarIA supera a BETO** en detección de desinformación en español para redes sociales LATAM
- Dataset con 7 categorías de veracidad (más granular que binario)
- Fuentes de datos: organizaciones de fact-checking latinoamericanas (el equivalente ecuatoriano de Chequeado)
- Período de cobertura relevante: incluye pandemia COVID-19 y períodos electorales

## Limitaciones

- Solo texto, sin análisis multimodal
- Dataset concentrado en Ecuador (no Argentina): el vocabulario político y cultural difiere
- Posible amplificación de sesgo por SMOTE (oversampling sintético)
- 1.340 muestras originales: dataset pequeño para entrenamiento robusto

## Relevancia para el PFI

**El paper más directamente comparable al PFI en el contexto LATAM.** La metodología es exportable a Argentina: reemplazar Ecuador Chequea/Verifica por Chequeado.com como fuente de etiquetas. Los resultados de MarIA como modelo superior son relevantes para la selección de modelo en el PFI. Confirma que no existe trabajo equivalente para Argentina.

**Clave biblio:** `ToapantaEtAl2024`
