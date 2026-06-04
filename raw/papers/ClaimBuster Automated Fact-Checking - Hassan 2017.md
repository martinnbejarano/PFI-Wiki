---
tipo: paper
titulo: "Toward Automated Fact-Checking: Detecting Check-worthy Factual Claims by ClaimBuster"
autores: [Hassan, Naeemul, Arslan, Fatma, Li, Chengkai, Tremayne, Mark]
año: 2017
venue: "KDD 2017 — Proceedings of the 23rd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining"
doi: "10.1145/3097983.3098131"
url: "https://dl.acm.org/doi/10.1145/3097983.3098131"
sistema: "https://idir.uta.edu/claimbuster/"
relevancia: media
temas: [claimbuster, claim-detection, fact-checking, nlp, sistema, estado-del-arte]
---

# Toward Automated Fact-Checking: Detecting Check-worthy Factual Claims by ClaimBuster

## Referencia completa

Hassan, N., Arslan, F., Li, C. y Tremayne, M. (2017). Toward Automated Fact-Checking: Detecting Check-worthy Factual Claims by ClaimBuster. *Proceedings of the 23rd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, pp. 1803–1812. DOI: 10.1145/3097983.3098131.

## Resumen

Primer sistema end-to-end de fact-checking automático con componentes: (1) Claim Spotter — clasifica oraciones en check-worthy factual claim / unimportant factual / non-factual; (2) Claim Matcher — compara nuevas afirmaciones contra claims ya verificadas en base de datos. Aplicado a transcripciones de debates presidenciales de EEUU.

## Hallazgos clave

- Precision de 0.96 para las top-100 oraciones más verificables
- Cobertura en vivo de debates presidenciales 2016 (primer sistema de este tipo)
- Clasificador de check-worthiness basado en SVMs con features lingüísticas
- Sistema disponible públicamente como API: idir.uta.edu/claimbuster/
- Inspiró múltiples sistemas subsiguientes (Full Fact, Chequeabot, Newtral)

## Limitaciones

- Solo inglés, solo discurso político
- No verifica hechos por sí mismo: detecta y clasifica qué verificar, pero no produce el veredicto
- Sin generalización a otros idiomas ni dominios sin reentrenamiento

## Relevancia para el PFI

El componente de claim detection es directamente aplicable al contexto argentino. El pipeline del PFI puede incorporar una etapa similar para identificar afirmaciones verificables en tweets/publicaciones antes de pasarlas al clasificador principal.

**Clave biblio:** `HassanEtAl2017`
