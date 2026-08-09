# Índice del Wiki PFI

> Actualizado: 2026-08-08. Última operación: health-check del wiki + página de decisiones pendientes y cronograma con fechas confirmadas (E3 — 50%: 28/08/2026).

---

## Proyecto

| Página | Descripción |
|---|---|
| [[wiki/00-resumen]] | Visión general del PFI — estado actual, objetivo, alcance |
| [[wiki/proyecto/propuesta]] | Propuesta de tema — idea, problema, alcance preliminar |
| [[wiki/proyecto/contexto-problema]] | Contexto del problema — estadísticas de desinformación en Argentina, IA generativa, por qué Argentina |
| [[wiki/proyecto/cronograma]] | Entregas formales con fechas confirmadas (E2 — 50%: documento 22/08/2026, exposición 29/08), plan de actividades y ruta crítica |
| [[wiki/proyecto/entrega-50-alcance]] | Alcance de la Entrega del 50% según la rúbrica oficial EP2: los ocho criterios evaluados, estado de cada uno y contradicciones entre la rúbrica y lo dicho en clase |
| [[wiki/proyecto/plan-entrega-50]] | Plan de trabajo de los 14 días hasta el 22/08: cinco bloques ordenados por dependencia, qué queda fuera de alcance y riesgos con su mitigación |
| [[wiki/proyecto/plan-bloque-diseno]] | Plan detallado del bloque de diseño (9-14/08): las ocho decisiones de producto que lo destraban, calendario día por día y especificación de requerimientos, mockups, seis diagramas y modelo de datos |
| [[wiki/proyecto/reuniones]] | Log de reuniones con el tutor Giro Uribazo |
| [[wiki/proyecto/recomendaciones-profesor]] | Guía del profesor: Marco Teórico, Estado del Arte, User Research, ISO 690-2010 |
| [[wiki/proyecto/metodologia]] | Metodología de desarrollo elegida |
| [[wiki/proyecto/restricciones-legales-eticas]] | Análisis de leyes argentinas (LPDP, derechos de autor, ToS), restricciones y compliance |
| [[wiki/proyecto/recursos]] | Presupuesto estimado: costos fijos y mensuales de infraestructura cloud (Railway, Vercel, HF Pro, Tavily) — USD 173 en el período del PFI |

## Solución

| Página | Descripción |
|---|---|
| [[wiki/solucion/metodologia-tecnica]] | Arquitectura ML/DL de 4 módulos: NLP, credibilidad, contraste + web search, ensemble |
| [[wiki/solucion/requerimientos]] | 26 requerimientos funcionales con prioridad MoSCoW y 16 no funcionales con valor comprometido; siete casos de uso desarrollados con sus flujos alternativos y matriz de trazabilidad |
| [[wiki/solucion/mockups]] | Cuatro pantallas del frontend en HTML y CSS reales: indicador sobre el tuit en sus cuatro estados, detalle del veredicto con su variante de análisis parcial, panel de evidencia y panel de tendencias B2B |
| [[wiki/solucion/arquitectura]] | Arquitectura física, lógica y modelo C4 |
| [[wiki/solucion/tecnologias]] | Stack tecnológico y servicios externos |
| [[wiki/solucion/pruebas]] | Pruebas funcionales, usabilidad y validación con usuarios |
| [[wiki/solucion/pipeline-preprocesamiento]] | Pipeline completo: limpieza, normalización, tokenización, vectorización con BETO |

## Marco Teórico

| Página | Descripción |
|---|---|
| [[wiki/marco-teorico/tipos-fake-text]] | Taxonomía de fake text: fake news, rumores, desinformación, texto generado por LM |
| [[wiki/marco-teorico/enfoques-deteccion]] | Enfoques de detección: tradicional, deep learning, transformers, content/context/propagation |
| [[wiki/marco-teorico/nlp-fundacional]] | Tokenización, embeddings (Word2Vec, GloVe, FastText) → representaciones contextuales |
| [[wiki/marco-teorico/transformers-bert]] | Arquitectura Transformer (Vaswani 2017), BERT (Devlin 2019), self-attention, fine-tuning |
| [[wiki/marco-teorico/fact-checking-automatico]] | Pipeline canónico: claim detection → evidence retrieval → verdict prediction (Guo 2022) |
| [[wiki/marco-teorico/modelos-espanol]] | BETO, XLM-RoBERTa, RoBERTuito, MarIA — comparativa y recomendación para el PFI |
| [[wiki/marco-teorico/difusion-desinformacion]] | Wardle 2017 (mis/dis/mal-información), Vosoughi 2018 (6x más rápido), Lazer 2018 |

## Estado del Arte

| Página | Descripción |
|---|---|
| [[wiki/estado-del-arte/kwon-jang-2025-survey-fake-text]] | Survey IEEE — detección de misinformación y texto generado por LM; taxonomía completa |
| [[wiki/estado-del-arte/albtoush-2025-arabic-fake-news]] | Survey PeerJ — state of the art para fake news; desafíos en idiomas low-resource |
| [[wiki/estado-del-arte/fakebert-kaliyar-2021]] | FakeBERT: BERT + CNN, 98.9% in-domain en inglés; baseline de referencia del PFI |
| [[wiki/estado-del-arte/toapanta-2024-latam]] | Mejor paper LATAM: MarIA 96%, BETO 93% en FakeDeS; el comparador directo del PFI |
| [[wiki/estado-del-arte/brechas-espanol-latam]] | 83% investigación en inglés; 0 papers sobre Argentina; degradación ~26pp cross-domain |
| [[wiki/estado-del-arte/comparativa-llms-2024-2025]] | BERT fine-tuned supera a LLMs; web retrieval +20pp F1; sistema híbrido recomendado |
| [[wiki/estado-del-arte/bigcn-deteccion-grafos]] | BiGCN: grafos bidireccionales de propagación; +10pp sobre texto solo en PHEME |
| [[wiki/estado-del-arte/drchal-2024-pipeline-multiidioma]] | Pipeline "any language" que excluye español en práctica; justifica modelos nativos |

## Análisis Competitivo

| Página | Descripción |
|---|---|
| [[wiki/competencia/analisis-competitivo]] | Competidores, tabla comparativa, océano azul, matriz ERIC |

## Investigación

| Página | Descripción |
|---|---|
| [[wiki/investigacion/user-research]] | Instrumentos diseñados: cuestionario de encuesta (15 preg., meta 120+), guía de entrevista semiestructurada, plantillas de user persona y estrategia de campo |

## Negocio

| Página | Descripción |
|---|---|
| [[wiki/negocio/modelo-de-negocio]] | Modelo freemium B2C → B2B: qué se vende (API + reportes), segmentos B2B, moat de datos vs scraping, BMC completo, FODA, 5 fuerzas, pricing y riesgos |
| [[wiki/negocio/analisis-financiero]] | VAN, TIR, payback, costos e ingresos proyectados |

## Desarrollo — Implementaciones de Referencia

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
| [[wiki/datasets/comparacion-datasets]] | Tabla comparativa completa + estrategia de datos del PFI (3 tiers) |
| [[wiki/datasets/liar-dataset]] | LIAR (Wang 2017): 12.836 samples, 6 clases, benchmark de referencia |
| [[wiki/datasets/fakenewsnet]] | FakeNewsNet (Shu 2020): PolitiFact + GossipCop + contexto social (grafos de propagación) |
| [[wiki/datasets/pheme-dataset]] | PHEME: ~6.500 tweets, 9 eventos, 3 clases (verdadero/falso/no verificado) |
| [[wiki/datasets/fakeddit]] | Fakeddit (Nakamura 2020): 1M+ Reddit, multimodal (texto + imagen) |
| [[wiki/datasets/spanish-fake-news-corpus]] | FakeDeS (Posadas 2019): 971 muestras — el gap crítico del español documentado |

## Desarrollo — Modelos

| Página | Descripción |
|---|---|
| [[wiki/modelos/modelos-overview]] | Taxonomía de enfoques (contenido, fuente, grafos, multimodal), modelo elegido |

## Desarrollo — Experimentos

| Página | Descripción |
|---|---|
| [[wiki/experimentos/experimentos-overview]] | Tabla resumen de experimentos, resultados, comparación de modelos |

## Síntesis

| Página | Descripción |
|---|---|
| [[wiki/sintesis/decisiones-pendientes-2026-08]] | Decisiones abiertas del health-check 2026-08-08 con opciones y costo: modelo principal (XLM-RoBERTa / RoBERTuito / XLM-T / comparación experimental), pipeline, tamaño del corpus argentino, número de clases |

## Fuentes ingresadas

### Papers académicos (raw/papers/)

| Fuente | Tipo | Página wiki |
|---|---|---|
| Attention Is All You Need (Vaswani et al., 2017) | Paper | [[wiki/marco-teorico/transformers-bert]] |
| BERT (Devlin et al., 2019) | Paper | [[wiki/marco-teorico/transformers-bert]] |
| BETO — Spanish BERT (Cañete et al., 2023) | Paper | [[wiki/marco-teorico/modelos-espanol]] |
| RoBERTuito (Pérez et al., 2022) | Paper | [[wiki/marco-teorico/modelos-espanol]] |
| XLM-RoBERTa (Conneau et al., 2020) | Paper | [[wiki/marco-teorico/modelos-espanol]] |
| Word2Vec (Mikolov et al., 2013) | Paper | [[wiki/marco-teorico/nlp-fundacional]] |
| GloVe (Pennington et al., 2014) | Paper | [[wiki/marco-teorico/nlp-fundacional]] |
| FastText (Bojanowski et al., 2017) | Paper | [[wiki/marco-teorico/nlp-fundacional]] |
| Text Preprocessing Survey (Chai, 2023) | Paper | [[wiki/marco-teorico/nlp-fundacional]] |
| Wardle & Derakhshan 2017 (Information Disorder) | Informe | [[wiki/marco-teorico/difusion-desinformacion]] |
| The Spread of True and False News (Vosoughi et al., 2018) | Paper | [[wiki/marco-teorico/difusion-desinformacion]] |
| The Science of Fake News (Lazer et al., 2018) | Paper | [[wiki/marco-teorico/difusion-desinformacion]] |
| Automated Fact-Checking Survey (Guo et al., 2022) | Survey | [[wiki/marco-teorico/fact-checking-automatico]] |
| Claim Detection Survey (Panchendrarajan & Zubiaga, 2024) | Survey | [[wiki/marco-teorico/fact-checking-automatico]] |
| ClaimBuster (Hassan et al., 2017) | Paper | [[wiki/marco-teorico/fact-checking-automatico]] |
| Web Retrieval for Misinformation (Tian et al., 2024) | Paper | [[wiki/estado-del-arte/comparativa-llms-2024-2025]] |
| LIAR Dataset (Wang, 2017) | Paper | [[wiki/datasets/liar-dataset]] |
| FakeNewsNet (Shu et al., 2020) | Paper | [[wiki/datasets/fakenewsnet]] |
| FakeBERT (Kaliyar et al., 2021) | Paper | [[wiki/estado-del-arte/fakebert-kaliyar-2021]] |
| BiGCN (Bian et al., 2020) | Paper | [[wiki/estado-del-arte/bigcn-deteccion-grafos]] |
| MDFEND (Nan et al., 2021) | Paper | — (pendiente) |
| Toapanta et al. 2024 — Ecuador | Paper | [[wiki/estado-del-arte/toapanta-2024-latam]] |
| BERT vs. LLMs (Raza et al., 2024) | Paper | [[wiki/estado-del-arte/comparativa-llms-2024-2025]] |
| PolyTruth (Gouliev et al., 2025) | Paper | [[wiki/estado-del-arte/brechas-espanol-latam]] |
| Low-Resource Languages Survey (Wang et al., 2024) | Survey | [[wiki/estado-del-arte/brechas-espanol-latam]] |
| Hasan et al. 2025 — LIAR generalization | Paper | [[wiki/estado-del-arte/brechas-espanol-latam]] |
| Drchal et al. 2024 — Multilingual pipeline | Paper | [[wiki/estado-del-arte/drchal-2024-pipeline-multiidioma]] |
| Yenikent et al. 2024 — Spanish BERT degradation | Paper | [[wiki/estado-del-arte/brechas-espanol-latam]] |
| Credibility Assessment + LLMs (Srba et al., 2025) | Survey | [[wiki/estado-del-arte/comparativa-llms-2024-2025]] |
| A Comprehensive Survey of Fake Text Detection (Kwon & Jang, 2025) | Survey | [[wiki/estado-del-arte/kwon-jang-2025-survey-fake-text]] |
| Fake News Detection State-of-the-Art (Albtoush et al., 2025) | Survey | [[wiki/estado-del-arte/albtoush-2025-arabic-fake-news]] |

### Datasets (raw/datasets/)

| Fuente | Tipo | Página wiki |
|---|---|---|
| LIAR Dataset | Dataset | [[wiki/datasets/liar-dataset]] |
| FakeNewsNet | Dataset | [[wiki/datasets/fakenewsnet]] |
| PHEME | Dataset | [[wiki/datasets/pheme-dataset]] |
| Fakeddit | Dataset | [[wiki/datasets/fakeddit]] |
| MultiFC | Dataset | — (pendiente) |
| CREDBANK | Dataset | — (pendiente) |
| Spanish Fake News Corpus (FakeDeS) | Dataset | [[wiki/datasets/spanish-fake-news-corpus]] |

---

*Para agregar una nueva entrada: actualizar la tabla correspondiente con el link a la página nueva y una descripción de una línea.*
