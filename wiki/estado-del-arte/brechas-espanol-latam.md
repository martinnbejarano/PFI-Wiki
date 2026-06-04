---
titulo: Brechas en Español y LATAM — Estado del Arte
tipo: análisis
tags: [brecha, espanol, latam, argentina, low-resource, estado-del-arte, gaps]
fuentes: [Monolingual Multilingual Misinformation Low-Resource Languages Survey - Wang 2024.md, PolyTruth Multilingual Disinformation Detection - Gouliev 2025.md, Generalization Gaps Political Fake News Detection LIAR - Hasan 2025.md]
actualizado: 2026-06-04
---

# Brechas en Español y LATAM — Estado del Arte

Esta página consolida la evidencia empírica sobre las limitaciones del estado del arte en detección de desinformación para español y contextos latinoamericanos. Estas brechas constituyen la **justificación académica del PFI**.

## Brecha 1: 83% de la investigación es en inglés

Wang et al. (2024) — *Monolingual and Multilingual Misinformation Detection in Low-Resource Languages* — analizaron el ecosistema completo de investigación:

- **83% de los papers de detección de fake news** son en inglés
- El español tiene la segunda mayor cobertura (< 8% del total)
- Las variedades latinoamericanas del español tienen cobertura **casi inexistente**
- No existe ningún trabajo académico publicado específicamente sobre Argentina

**Consecuencia para el PFI**: el sistema propuesto no tiene competencia académica directa en el dominio argentino.

## Brecha 2: Degradación en datos reales (domain shift)

Yenikent et al. (2024) documentan el problema de **domain shift** cuantitativamente:

| Condición | Accuracy |
|---|---|
| Evaluación in-domain (mismo dataset) | 97–98% |
| Evaluación cross-domain (datos reales) | ~71% |

Una caída de **26–27 puntos porcentuales** al pasar de datos de test controlados a datos del mundo real. Este fenómeno se repite en todos los modelos evaluados.

**Causas identificadas**:
- Diferencias en vocabulario y estilo entre el dominio de entrenamiento y el real
- Los modelos aprenden señales espurias (el estilo del sitio web, no la veracidad del contenido)
- Los datasets de entrenamiento no cubren eventos ni figuras políticas actuales

**Consecuencia para el PFI**: los modelos deben evaluarse en datos frescos de Argentina, no solo en benchmarks controlados.

## Brecha 3: Generalización entre dominios políticos

Hasan et al. (2025) evaluaron la generalización en LIAR con enfoque específico en noticias políticas:

- **SVM y RoBERTa alcanzan ~62% en LIAR (6 clases)**
- El performance en política de EE.UU. no transfiere a política de otros países
- Los modelos aprenden el *bias* del fact-checker, no la veracidad intrínseca del contenido

**Hallazgo contrarresultado**: en clasificación binaria (fake/real), la diferencia entre SVM y RoBERTa es solo ~2–3%; la arquitectura compleja no garantiza mejor generalización.

## Brecha 4: Cobertura multilingüe parcial

Gouliev et al. (2025) — PolyTruth, 25 idiomas incluyendo español — encontraron que:
- **RemBERT y XLM-RoBERTa-large** son los mejores modelos multilingüe
- El español tiene mejor cobertura que otros idiomas LATAM (portugués, quechua, etc.)
- Pero la performance en español es **8–12% menor** que en inglés en el mismo sistema

**Consecuencia**: incluso los sistemas multilingüe state-of-the-art tienen un gap significativo para español.

## Brecha 5: Sin cobertura de desinformación argentina

Revisión exhaustiva de la literatura (sesión de investigación, junio 2026):

| País LATAM | Papers académicos de fake news |
|---|---|
| Brasil | ~15 papers (FakeNewsBR corpus, varios) |
| México | ~8 papers (incluye Posadas-Durán 2019) |
| Ecuador | 2–3 papers (Toapanta 2024) |
| Colombia | 1–2 papers |
| **Argentina** | **0 papers académicos específicos** |

**Argentina es el único país hispanohablante grande sin un dataset académico propio.**

## Mapa de brechas vs. solución propuesta

| Brecha | Evidencia | Solución en el PFI |
|---|---|---|
| 83% investigación en inglés | Wang et al. 2024 | Dataset argentino propio |
| Domain shift ~26pp | Yenikent et al. 2024 | Evaluación con datos frescos locales |
| Sin datos argentinos | Revisión de literatura | Corpus anotado como contribución |
| Performance multilingüe -8–12% | Gouliev et al. 2025 | RoBERTuito (nativo español social) |
| Generalización política | Hasan et al. 2025 | Fine-tuning sobre política argentina |

## Conclusión

La ausencia de investigación en Argentina y la degradación documentada en datos reales constituyen la **justificación académica primaria del PFI**. El sistema propuesto no es una reimplementación de algo existente — cubre una brecha real y documentada.

## Referencias cruzadas
- [[toapanta-2024-latam]]
- [[wiki/datasets/spanish-fake-news-corpus]]
- [[wiki/marco-teorico/difusion-desinformacion]]
- [[wiki/proyecto/propuesta]]

## Fuentes
- [[raw/papers/Monolingual Multilingual Misinformation Low-Resource Languages Survey - Wang 2024.md]]
- [[raw/papers/PolyTruth Multilingual Disinformation Detection - Gouliev 2025.md]]
- [[raw/papers/Generalization Gaps Political Fake News Detection LIAR - Hasan 2025.md]]
