---
tipo: paper
titulo: "Claim Detection for Automated Fact-checking: A Survey on Monolingual, Multilingual and Cross-Lingual Research"
autores: [Panchendrarajan, Rrubaa, Zubiaga, Arkaitz]
año: 2024
venue: "Journal of Information and Intelligence (ScienceDirect)"
doi: "10.1016/j.jiixd.2024.01.003"
arxiv: "2401.11969"
url: "https://arxiv.org/abs/2401.11969"
sciencedirect: "https://www.sciencedirect.com/science/article/pii/S2949719124000141"
relevancia: alta
temas: [claim-detection, fact-checking, multilingue, cross-lingual, survey, nlp]
---

# Claim Detection for Automated Fact-checking: A Survey on Monolingual, Multilingual and Cross-Lingual Research

## Referencia completa

Panchendrarajan, R. y Zubiaga, A. (2024). Claim Detection for Automated Fact-checking: A Survey on Monolingual, Multilingual and Cross-Lingual Research. *Journal of Information and Intelligence*. DOI: 10.1016/j.jiixd.2024.01.003. arXiv: 2401.11969.

## Resumen

Survey sobre la primera etapa del pipeline de fact-checking: la detección de afirmaciones verificables (*claim detection*). Cubre enfoques monolingüe, multilingüe y cross-lingual. Identifica desafíos específicos para idiomas con pocos recursos (low-resource languages).

## Hallazgos clave

- La detección de claims es la etapa más crítica del pipeline: un error aquí se propaga
- Los modelos multilingüe (XLM-RoBERTa) superan a los monolingüe en escenarios cross-lingual
- Para idiomas con recursos limitados, el zero-shot cross-lingual (entrenado en inglés, aplicado en otro idioma) logra resultados razonables
- El tipo de claim importa: afirmaciones numéricas, de causa-efecto y comparativas son las más verificables
- Escasez de datasets de claim detection en español

## Relevancia para el PFI

Justifica el componente de claim detection en el pipeline del sistema. Los desafíos para idiomas con recursos limitados aplican directamente al español argentino. La recomendación de usar XLM-RoBERTa para cross-lingual es relevante para el módulo de detección.

**Clave biblio:** `PanchendrarajanZubiaga2024`
