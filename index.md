# Índice del Wiki PFI

> Actualizado: 2026-04-16. Última operación: contexto del problema — estadísticas Argentina (Reuters Institute 2024, IA generativa).

---

## Proyecto

| Página | Descripción |
|---|---|
| [[wiki/00-resumen]] | Visión general del PFI — estado actual, objetivo, alcance |
| [[wiki/proyecto/propuesta]] | Propuesta de tema — idea, problema, alcance preliminar |
| [[wiki/proyecto/contexto-problema]] | Contexto del problema — estadísticas de desinformación en Argentina, IA generativa, por qué Argentina |
| [[wiki/proyecto/cronograma]] | Fechas clave y entregas formales del PFI |
| [[wiki/proyecto/reuniones]] | Log de reuniones con el tutor Monzón |
| [[wiki/proyecto/metodologia]] | Metodología de desarrollo elegida |
| [[wiki/proyecto/restricciones-legales-eticas]] | Análisis de leyes argentinas (LPDP, derechos de autor, ToS), restricciones y compliance |

## Solución

| Página | Descripción |
|---|---|
| [[wiki/solucion/metodologia-tecnica]] | Arquitectura ML/DL de 4 módulos: NLP, credibilidad, contraste + web search, ensemble |
| [[wiki/solucion/requerimientos]] | Requerimientos funcionales, no funcionales y casos de uso |
| [[wiki/solucion/arquitectura]] | Arquitectura física, lógica y modelo C4 |
| [[wiki/solucion/tecnologias]] | Stack tecnológico y servicios externos |
| [[wiki/solucion/pruebas]] | Pruebas funcionales, usabilidad y validación con usuarios |
| [[wiki/solucion/pipeline-preprocesamiento]] | Pipeline completo: limpieza, normalización, tokenización, vectorización con BETO |

## Marco teórico

| Página | Descripción |
|---|---|
| [[wiki/marco-teorico/tipos-fake-text]] | Taxonomía de fake text: fake news, rumores, desinformación, texto generado por LM |
| [[wiki/marco-teorico/enfoques-deteccion]] | Enfoques de detección: tradicional, deep learning, transformers, content/context/propagation |

## Estado del arte

| Página | Descripción |
|---|---|
| [[wiki/estado-del-arte/kwon-jang-2025-survey-fake-text]] | Survey IEEE — detección de misinformación y texto generado por LM; taxonomía completa de técnicas |
| [[wiki/estado-del-arte/albtoush-2025-arabic-fake-news]] | Survey PeerJ — state of the art ML/DL/Transformers para fake news; desafíos en idiomas low-resource (análogo al español) |

## Análisis competitivo

| Página | Descripción |
|---|---|
| [[wiki/competencia/analisis-competitivo]] | Competidores, tabla comparativa, océano azul, matriz ERIC |

## Investigación

| Página | Descripción |
|---|---|
| [[wiki/investigacion/user-research]] | Entrevistas, encuestas, user personas e insights |

## Negocio

| Página | Descripción |
|---|---|
| [[wiki/negocio/modelo-de-negocio]] | Business Model Canvas, FODA, propuesta de valor |
| [[wiki/negocio/analisis-financiero]] | VAN, TIR, payback, costos e ingresos proyectados |

## Desarrollo — Implementaciones de referencia

| Página | Descripción |
|---|---|
| [[wiki/implementaciones/implementaciones-overview]] | Sistemas y repos existentes analizados, patrones y anti-patrones |
| [[wiki/implementaciones/information-tracer]] | Information Tracer — SaaS de inteligencia en redes sociales, detección de manipulación coordinada |
| [[wiki/implementaciones/diggity-mediaparty]] | Diggity — API + extensión Chrome para calidad periodística, NLP + LLM, open-source LATAM |
| [[wiki/implementaciones/gnn-fakenews-safe-graph]] | GNN-FakeNews — colección de modelos GNN para detección vía grafos de propagación (PyTorch Geometric) |
| [[wiki/implementaciones/fake-news-detector-br]] | Fake News Detector BR — extensión Chrome/Firefox con clasificación de 6 clases, crowdsourcing, portugués/LATAM |
| [[wiki/implementaciones/newtral-factflow]] | Newtral FactFlow — fact-checking automático en español con Qwen LLM, 1M+ mensajes de entrenamiento |

## Desarrollo — Datasets

| Página | Descripción |
|---|---|
| [[wiki/datasets/datasets-overview]] | Panorama de datasets disponibles, comparación y dataset elegido |
| [[wiki/datasets/dataset-recomendacion]] | Selección de datasets (LIAR, FakeNewsNet), recolección y validación con datos reales argentinos |

## Desarrollo — Modelos

| Página | Descripción |
|---|---|
| [[wiki/modelos/modelos-overview]] | Taxonomía de enfoques (contenido, fuente, grafos, multimodal), modelo elegido |

## Desarrollo — Experimentos

| Página | Descripción |
|---|---|
| [[wiki/experimentos/experimentos-overview]] | Tabla resumen de experimentos, resultados, comparación de modelos |

## Síntesis

*(vacío — se llena con análisis cross-cutting y respuestas a consultas valiosas)*

## Fuentes ingresadas

| Fuente | Tipo | Página wiki |
|---|---|---|
| A Comprehensive Survey of Fake Text Detection on Misinformation and LM-Generated Texts (Kwon & Jang, IEEE 2025) | Paper académico | [[wiki/estado-del-arte/kwon-jang-2025-survey-fake-text]] |
| Fake news detection: state-of-the-art review and advances with attention to Arabic language aspects (Albtoush et al., PeerJ 2025) | Paper académico | [[wiki/estado-del-arte/albtoush-2025-arabic-fake-news]] |

---

*Para agregar una nueva entrada: actualizar la tabla correspondiente con el link a la página nueva y una descripción de una línea.*
