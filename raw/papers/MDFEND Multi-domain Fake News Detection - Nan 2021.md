---
tipo: paper
titulo: "MDFEND: Multi-domain Fake News Detection"
autores: [Nan, Qiong, Cao, Juan, Zhu, Yanyan, Wang, Ya-Nan, Li, Jintao]
año: 2021
venue: "Proceedings of the 30th ACM International Conference on Information and Knowledge Management (CIKM 2021)"
doi: "10.1145/3459637.3482139"
url: "https://dl.acm.org/doi/10.1145/3459637.3482139"
arxiv: "2201.00987"
relevancia: media
temas: [mdfend, multi-dominio, domain-gate, fake-news, clasificacion, estado-del-arte]
---

# MDFEND: Multi-domain Fake News Detection

## Referencia completa

Nan, Q., Cao, J., Zhu, Y., Wang, Y.-N. y Li, J. (2021). MDFEND: Multi-domain Fake News Detection. *Proceedings of CIKM 2021*, pp. 3343–3347. DOI: 10.1145/3459637.3482139.

## Resumen

Primer modelo diseñado específicamente para detección de fake news en múltiples dominios simultáneamente. Usa un *domain gate* para seleccionar combinaciones de expertos (*mixture of experts*) específicos de cada dominio. Introduce el dataset Weibo21 (4.488 fake + 4.640 real, 9 dominios, en chino).

## Hallazgos clave

- Los modelos entrenados en un dominio generaliza mal a otros dominios: pérdida de 15-30% en F1
- El domain gate permite que el mismo modelo capture patrones específicos de política, salud, deportes, etc.
- Mejora significativa sobre baselines (EANN, BERT, RoBERTa) en detección multi-dominio
- Weibo21 es el dataset de referencia para multi-dominio en chino

## Limitaciones

- Solo en chino (Weibo)
- La transferencia a otros idiomas requiere adaptación significativa
- El domain gate requiere conocer el dominio en inferencia

## Relevancia para el PFI

El sistema del PFI debe detectar desinformación en múltiples dominios (política, economía, salud). MDFEND evidencia que un modelo único sin distinción de dominio tiene rendimiento subóptimo. Justifica considerar estrategias multi-dominio en el diseño del clasificador.

**Clave biblio:** `NanEtAl2021`
