# Log del Wiki PFI

> Registro cronológico append-only. Formato de cada entrada: `## [YYYY-MM-DD] tipo | descripción`
> Tipos: `setup` | `ingest` | `query` | `lint` | `update`

## [2026-07-04] update | Correcciones del health-check (modelo, alcance, contradicciones)

Aplicadas las correcciones surgidas del lint del mismo día:

- **Modelo principal definido: RoBERTuito** (evaluando el documento LaTeX, que ya lo priorizaba de forma consistente en cap. 2). Propagado a toda la wiki: `modelos-overview.md` (antes "[POR DEFINIR]", ahora RoBERTuito principal + BETO/XLM-RoBERTa/TF-IDF como comparación; secciones 2-5 rellenadas; link roto `nlp`→`nlp-fundacional` arreglado), `transformers-bert.md` (antes "BETO como modelo principal"), `enfoques-deteccion.md` (tabla con doble "candidato principal" corregida; RoBERTuito agregado), `propuesta.md`, `metodologia-tecnica.md`, `recursos.md`. El documento LaTeX ya era coherente; no requirió cambios.
- **Dato corregido en `modelos-espanol.md`**: RoBERTuito es del grupo pysentimiento (Juan Manuel Pérez, UBA/CONICET), no de "Univ. Nac. de San Luis". Accuracy en FakeDeS alineada a Toapanta (~93%).
- **Alcance Twitter/X (#6)**: `information-tracer.md` (decisión ya tomada: MVP solo Twitter/X) y `fake-news-detector-br.md` (patrón de integración reencuadrado a Twitter/X, no Facebook). Nota: la tabla `fake-news-detector-br.md:55` no se tocó — la columna "Infobae" describe a Diggity, no al PFI.
- **Rango etario (#2)**: `propuesta.md` sección "Segmento target" pasada de "16 a 80+ años" a "18 a 40 años", coherente con la decisión del 2026-06-13.
- **Estado (#5)**: checklist de `00-resumen.md` actualizado (marco teórico, EdA y competencia marcados como hechos).

Conteo de módulos en `propuesta.md`: corregido L46 ("tres módulos" → "cuatro módulos", residuo del diseño original de 3 módulos previo al 2026-04-19) y aclarado L54 ("3 señales... que el módulo ensemble sintetiza") para no confundir las señales de análisis con el conteo de módulos.

## [2026-07-04] lint | Health-check completo del wiki (49 páginas)

Análisis del grafo de links (determinístico) + contradicciones de contenido. El grafo está sano; los problemas se concentran en (a) la decisión de alcance del 2026-06-13 (Twitter/X única plataforma de detección) no propagada a todas las páginas, (b) reincidencias del lint 2026-06-04 nunca aplicadas, y (c) páginas stub sin tocar desde abril.

**Contradicciones (prioridad alta):**
1. **Modelo principal inconsistente.** `modelos-espanol.md` concluye que **RoBERTuito** es el modelo más adecuado (entrenado sobre tweets, alineado con el alcance Twitter/X); pero `transformers-bert.md:100` dice "BETO como modelo principal" y `propuesta.md`/`00-resumen.md` dicen "BETO o XLM-RoBERTa" sin mencionar RoBERTuito. Requiere decisión del autor.
2. **`propuesta.md` rango etario.** L42/L102 dicen segmento primario "18 a 40 años"; L161 (sección "Segmento target") dice "16 a 80+ años" — resto stale del cambio del 2026-06-13.
3. **`propuesta.md` conteo de módulos.** L42/L184 dicen "cuatro módulos"; L46 dice "el prototipo funcional de los tres módulos".
4. **[REINCIDENTE] `modelos-overview.md`** sigue en "[POR DEFINIR]" y con secciones 2-5 en "[POR INVESTIGAR]" pese a que `enfoques-deteccion.md` y `modelos-espanol.md` ya lo cubren. Flagged en lint 2026-06-04, nunca aplicado.
5. **[REINCIDENTE] `00-resumen.md`** checklist "Estado actual" todo en `[ ]` (marco teórico, EdA, competencia, etc.) pese a estar hechos. Flagged en lint 2026-06-04, nunca aplicado.
6. **`fake-news-detector-br.md:55`** tabla comparativa: columna PFI "Plataforma objetivo: Sitios de noticias (Infobae, etc.)" — stale, ahora Twitter/X.

**Links:**
- [REINCIDENTE] `modelos-overview.md:75` → `[[wiki/marco-teorico/nlp]]` roto (debe ser `nlp-fundacional`).
- `implementaciones-overview.md` → `[[raw/papers/nombre.pdf]]` (template leftover) y `[[wiki/estado-del-arte/]]` (link a carpeta, no página).
- `datasets-overview.md` → `[[wiki/estado-del-arte/]]` (link a carpeta).

**Huérfanas (0 links entrantes):** `bigcn-deteccion-grafos`, `drchal-2024-pipeline-multiidioma`, `fake-news-detector-br`, `proyecto/metodologia`, `proyecto/recomendaciones-profesor`, `proyecto/recursos`.

**Stubs / placeholders (sin contenido real, casi todos de 2026-04-12):** `solucion/arquitectura`, `solucion/requerimientos`, `solucion/tecnologias`, `solucion/pruebas`, `negocio/analisis-financiero`, `proyecto/metodologia`, `investigacion/user-research`, `modelos/modelos-overview`, `datasets/datasets-overview`. Bloquean Presentaciones Preliminares 3+ (no la del 25%).

**Fuentes ingresadas sin página wiki:** MDFEND (Nan 2021), MultiFC, CREDBANK — marcadas "(pendiente)" en index.md.

**Sugerencias:** decidir RoBERTuito vs BETO como clasificador principal y unificar; evaluar página propia para Chequeado (mencionado en 8+ páginas); conectar huérfanas relevantes desde overviews.

## [2026-06-13] update | Correcciones del análisis comparativo (entrega 25%)

Revisión externa del documento (análisis comparativo contra tesis ejemplo) → correcciones de coherencia, justificación de alcance, validación de fuentes y precisión conceptual antes de la entrega del 25%:

- **Justificación Twitter/X vs WhatsApp**: se explicita por qué X es el primer objetivo de detección pese a que WhatsApp sea más masivo (espacio público donde se originan/amplifican narrativas).
- **Definición operativa**: el sistema no infiere intención; clasifica contenido "potencialmente falso, engañoso o no verificable" y usa "desinformación" como término paraguas.
- **Fuentes de evidencia**: "medios de confianza" → "fuentes periodísticas de referencia" + triangulación con fuentes oficiales y verificadores (Chequeado); ya no se tratan como única "verdad".
- **Citas**: el dato de 31,3 M usuarios y 93 % WhatsApp se reatribuye a DataReportal (no Reuters). Se suaviza el claim de "inaccesibilidad" de Cyabra/Blackbird. Raza et al. actualizado a su versión publicada (KAIS 2025); DOI corregido en Gouliev et al. (ECML PKDD).
- **Meta F1**: se adopta F1 macro como métrica principal, con justificación del umbral y atención al recall de la clase de interés.
- **Dataset**: "disponibilidad" → "factibilidad de construir/adaptar" un corpus argentino.
- **Usuarios**: segmento primario acotado (18-40, política/economía en X) + secundario (periodistas).
- **Privacidad**: cláusula de agregación/anonimización en el modelo de negocio.
- **Nueva subsección "Riesgos y desafíos del proyecto"** en cap. 1.
- **Cronograma**: pasado a página apaisada (pdflscape), filas más espaciadas, ya no se ve comprimido.

Archivos: documento/chapters/chapter01.tex, chapter02.tex; documento/biblio.bib (+DataReportal2024, Raza/Gouliev); documento/main.tex (pdflscape); documento/chapters/appendix/schedule_of_activities.tex; wiki/proyecto/propuesta.md; wiki/00-resumen.md; wiki/negocio/modelo-de-negocio.md.

## [2026-06-13] update | Acotar alcance: Twitter/X única plataforma de detección

Decisión de alcance: la extensión detecta desinformación **únicamente sobre Twitter/X**. Los medios digitales de confianza (Infobae, Clarín, La Nación, Página/12, Télam) dejan de ser objetivos de detección y pasan a usarse solo como **fuentes de evidencia** para el módulo de contraste semántico (scraping + búsqueda web). Instagram y Facebook quedan fuera del alcance del MVP (futuros releases).

Justificación: una extensión de navegador lee el DOM de la sesión del usuario, por lo que no depende de la API restringida de X; Twitter/X concentra el mayor respaldo de datasets y literatura, es texto-céntrico (alineado con RoBERTuito) y permite una arquitectura extensible por adaptadores a otras fuentes.

Archivos actualizados: documento/chapters/chapter01.tex (objetivos, alcance, limitaciones); wiki/proyecto/propuesta.md; wiki/00-resumen.md; wiki/competencia/analisis-competitivo.md; wiki/marco-teorico/modelos-espanol.md; wiki/solucion/metodologia-tecnica.md; wiki/solucion/pipeline-preprocesamiento.md; wiki/datasets/dataset-recomendacion.md; CLAUDE.md.

## [2026-06-04] update | Creación de 17 páginas wiki — Marco Teórico (5), Datasets (6), Estado del Arte (6)

Páginas creadas en wiki/marco-teorico/:
- nlp-fundacional.md — tokenización, Word2Vec, GloVe, FastText, embeddings contextuales
- transformers-bert.md — Transformer (Vaswani 2017), BERT (Devlin 2019), fine-tuning
- fact-checking-automatico.md — pipeline canónico: claim detection → evidence retrieval → verdict
- modelos-espanol.md — BETO, XLM-RoBERTa, RoBERTuito, MarIA; comparativa y recomendación
- difusion-desinformacion.md — Wardle 2017, Vosoughi 2018, Lazer 2018

Páginas creadas en wiki/datasets/:
- liar-dataset.md — 12.836 samples, 6 clases, benchmark de referencia
- fakenewsnet.md — PolitiFact + GossipCop + contexto social (grafos)
- pheme-dataset.md — ~6.500 tweets, 9 eventos, 3 clases
- fakeddit.md — 1M+ Reddit, multimodal (texto + imagen)
- spanish-fake-news-corpus.md — FakeDeS, 971 muestras; gap crítico documentado
- comparacion-datasets.md — tabla comparativa + estrategia de datos PFI (3 tiers)

Páginas creadas en wiki/estado-del-arte/:
- toapanta-2024-latam.md — MarIA 96%, BETO 93%; el comparador directo del PFI
- brechas-espanol-latam.md — 83% inglés, 0 papers Argentina, domain shift ~26pp
- fakebert-kaliyar-2021.md — BERT + CNN baseline; contexto crítico sobre evaluación in-domain
- comparativa-llms-2024-2025.md — BERT fine-tuned > LLMs; web retrieval +20pp F1
- bigcn-deteccion-grafos.md — grafos de propagación; +10pp sobre texto solo
- drchal-2024-pipeline-multiidioma.md — pipeline "any language" que excluye español

Actualizado: index.md con 17 páginas nuevas.

## [2026-06-04] ingest | Deep research Marco Teórico + Estado del Arte — 37 papers + 7 datasets a raw/

Fuentes agregadas a raw/papers/ (37 fichas):
- Vaswani 2017 (Transformer), Devlin 2019 (BERT), Conneau 2020 (XLM-RoBERTa)
- Cañete 2023 (BETO), Pérez 2022 (RoBERTuito), Yenikent 2024 (fake news español)
- Mikolov 2013 (Word2Vec), Pennington 2014 (GloVe), Bojanowski 2017 (FastText)
- Chai 2023 (preprocesamiento NLP), Guo 2022 (survey fact-checking)
- Vosoughi 2018 (difusión fake news), Lazer 2018 (ciencia fake news)
- Wardle & Derakhshan 2017 (information disorder), Srba 2025 (credibilidad)
- Wang 2017 (LIAR paper), Shu 2020 (FakeNewsNet), Kaliyar 2021 (FakeBERT)
- Hassan 2017 (ClaimBuster), Bian 2020 (BiGCN), Nan 2021 (MDFEND)
- Toapanta 2024 (LATAM Ecuador), Tian 2024 (web retrieval agents)
- Raza 2024 (BERT vs LLMs), Gouliev 2025 (PolyTruth), Hasan 2025 (generalization LIAR)
- Wang 2024 survey (low-resource), Drchal 2024 (pipeline multilingüe), Panchendrarajan 2024

Fuentes agregadas a raw/datasets/ (7 fichas):
- LIAR, FakeNewsNet, PHEME, Fakeddit, MultiFC, CREDBANK, Spanish-Fake-News-Corpus

## [2026-06-04] ingest | Slides del profesor: Marco Teórico, Estado del Arte, User Research + ejemplo PFI Sparkle

Fuentes procesadas:
- PFI_MarcoTeorico_EstadoDelArte_UserResearch-Sabados.pdf (slides de clase 2026)
- [GR_M15_Feresini_Imbriago][Entrega Final PFI 2025_V_2].pdf (ejemplo PFI aprobado)

Acciones:
- Creada wiki/proyecto/recomendaciones-profesor.md con guía completa de Marco Teórico, Estado del Arte, User Research y checklist de entrega.
- Agregadas en CLAUDE.md: sección "Estilo de escritura académica" (voz, terminología, frases prohibidas, estructura de párrafos) y sección "Citas y bibliografía — ISO 690-2010" (formato en texto, formato de entradas bib, reglas del profesor, fuentes académicas prioritarias).

## [2026-06-04] lint | Formulario de propuesta oficial — health-check y correcciones

Contradicciones encontradas y corregidas a partir del formulario de propuesta oficial (PDF, 25/04/2026):

1. **CRÍTICA — Tutor incorrecto**: Todo el repo tenía a Monzón, Nicolás Alberto como tutor. El formulario oficial indica Giro Uribazo, Fidel Valentin (fgirouribazo@uade.edu.ar, UADE interno). Corregido en CLAUDE.md, wiki/00-resumen.md, wiki/proyecto/reuniones.md, documento/chapters/title.tex, documento/main.tex.
2. **Título incompleto**: Faltaba "y Medios Digitales" al final del título oficial. Corregido en CLAUDE.md, wiki/00-resumen.md, wiki/proyecto/propuesta.md, documento/chapters/title.tex, documento/main.tex.
3. **LU del alumno**: Completado con 1150726 en documento/chapters/title.tex.
4. **Redes sociales "POR DEFINIR"** en CLAUDE.md: actualizado con las plataformas oficiales (X, Instagram, Facebook, Infobae, Clarín).

Acciones adicionales:
- Completado chapter01.tex con introducción, objetivos y alcance del formulario oficial.
- Agregada referencia Newman2024 (Reuters Institute DNR 2024) a biblio.bib.
- Renombrado macro \Nico{} → \Fidel{} en documento/main.tex y considerations.tex.

---

## [2026-06-04] lint | Health-check del wiki — contradicciones, huérfanas, faltantes

**Páginas analizadas:** 32 páginas wiki + index.md + log.md

**Contradicciones encontradas:**
1. `wiki/00-resumen.md` — checklist de estado desactualizado: marco teórico, estado del arte y análisis competitivo marcados como `[ ]` (pendiente) cuando ya están iniciados/completados con páginas reales.
2. `wiki/modelos/modelos-overview.md` — dice "Modelo elegido: [POR DEFINIR]" pero `metodologia-tecnica.md` y `enfoques-deteccion.md` ya lo definen como BETO/XLM-RoBERTa.
3. `wiki/datasets/datasets-overview.md` — dice "Dataset elegido: [POR DEFINIR]" pero `dataset-recomendacion.md` ya define LIAR + FakeNewsNet.

**Referencia rota:**
- `wiki/modelos/modelos-overview.md` línea 76: `[[wiki/marco-teorico/nlp]]` — esa página no existe.

**Páginas huérfanas (sin links entrantes desde otras páginas wiki):**
- `wiki/proyecto/recursos.md`
- `wiki/proyecto/contexto-problema.md`
- `wiki/implementaciones/fake-news-detector-br.md`
- `wiki/implementaciones/implementaciones-overview.md`

**Conceptos clave sin página propia:**
- BETO — modelo central del proyecto, sin página en `wiki/modelos/`
- XLM-RoBERTa — modelo alternativo clave, sin página en `wiki/modelos/`
- Chequeado.com — mencionado en 8+ páginas, sin análisis propio

**Placeholders críticos (importantes para el PFI, aún vacíos):**
- `wiki/solucion/arquitectura.md` — [POR DEFINIR], bloquea Presentación Preliminar 3
- `wiki/solucion/requerimientos.md` — [POR DEFINIR]
- `wiki/solucion/tecnologias.md` — [POR DEFINIR]
- `wiki/negocio/analisis-financiero.md` — [POR DEFINIR]
- `wiki/proyecto/metodologia.md` — [POR DEFINIR]
- `wiki/investigacion/user-research.md` — [POR DEFINIR]

**Fuentes a ingresar (citadas pero no formalizadas):**
- Reuters Institute Digital News Report 2024 (citado en propuesta.md)
- Paper BETO: Cañete et al. 2023
- Paper XLM-RoBERTa: Conneau et al.
- Dataset en español para fake news (pendiente de investigar)

---

## [2026-04-29] update | Modelo de negocio detallado (qué se vende, segmentos B2B, moat, BMC, FODA, pricing)

**Páginas actualizadas:** `wiki/negocio/modelo-de-negocio.md` (rewrite completo, antes era stub vacío con `[POR DEFINIR]`), `wiki/proyecto/propuesta.md` (sección "Modelo de negocio" expandida con qué se vende, segmentos B2B, moat de datos y bucle de red), `index.md`.

**Trigger:** consulta del usuario al preparar pitch para tutor — la sección original de la propuesta ("ciudadanos gratis → B2B paga") era demasiado abstracta para defender el modelo. No quedaba claro qué se vendía, a quién, ni por qué pagarían.

**Decisiones clave documentadas:**
- **Qué se vende exactamente:** no la extensión, sino información sobre qué desinformación circula en Argentina en tiempo real. Dos productos: API de detección (pricing por volumen) + reportes/dashboards de tendencias (suscripción mensual).
- **Cinco segmentos B2B:** medios de comunicación, fact-checkers (Chequeado), centros de investigación, organismos públicos / ONGs (especialmente en ciclos electorales), marcas y agencias corporativas. Cada uno con problema concreto y razón específica para pagar.
- **Moat de datos:** ventaja estructural frente a Cyabra/Blackbird.AI/Newtral FactFlow. Ellos obtienen datos por scraping de APIs (caro, limitado, ciego a WhatsApp). Nosotros, sensor distribuido en navegadores reales — registramos consumo, no solo publicación, y vemos WhatsApp cuando los usuarios abren links en el navegador.
- **Bucle de red de datos:** más usuarios → mejor dataset → producto B2B más valioso → más revenue → mejor producto ciudadano → más usuarios. Defendibilidad a largo plazo.
- **Pricing tentativo:** API Pro USD 200/mes, Enterprise USD 1.500-5.000/mes, dashboards USD 300/mes, contratos electorales USD 10k-50k.
- **Riesgos identificados:** dependencia de adopción ciudadana inicial, regulación LPDP, riesgo reputacional de sesgo percibido, riesgo de competidor enterprise pivotando.

BMC, FODA y 5 fuerzas completados con esta visión.

---

## [2026-04-22] update | Presupuesto estimado de infraestructura cloud

Creación de `wiki/proyecto/recursos.md` con el presupuesto completo del PFI. Costos fijos: $5 USD (Chrome Web Store) + dominio opcional ($15). Costos mensuales: $5/mes (Railway backend+DB), $0 Vercel, $0 HF Inference API, $0 Serper.dev. Total estimado período PFI (~12 meses): $65 USD. Incluye análisis comparativo de opciones para web search API y modelo NLP.

---

## [2026-04-19] lint | Health check del wiki — contradicciones resueltas

**Contradicciones identificadas y resueltas:**
1. **Módulos (3 vs 4):** propuesta.md línea 119 decía "3 módulos", contradice metodologia-tecnica.md. Actualizado a "4 módulos" (NLP + Credibilidad + Contraste + Ensemble).
2. **Fuente primaria para entrenamiento:** propuesta.md línea 110 mencionaba "Chequeado.com como fuente primaria", contradice metodologia-tecnica.md y dataset-recomendacion.md que describen "web search + bases de datos oficiales". Actualizado a "web search en medios confiables + bases de datos de fuentes oficiales (a determinar)".
3. **Página para Chequeado.com:** Analizado. Conclusión: Chequeado.com aparece en tabla comparativa (analisis-competitivo.md), no requiere página propia de análisis.

**Páginas analizadas:** 00-resumen.md, propuesta.md, metodologia-tecnica.md, analisis-competitivo.md, dataset-recomendacion.md, pipeline-preprocesamiento.md, restricciones-legales-eticas.md

**Estado de salud del wiki:**
- ✅ Referencias cruzadas correctas
- ✅ Index.md actualizado
- ✅ Log.md mantiene cronología
- ✅ Sin páginas huérfanas
- ✅ Nuevas páginas bien conectadas

---

## [2026-04-19] update | Restricciones legales, datasets y pipeline de preprocesamiento

**Páginas creadas:**
- `wiki/proyecto/restricciones-legales-eticas.md` — análisis de LPDP, derechos de autor, ToS, compliance
- `wiki/datasets/dataset-recomendacion.md` — estrategia de datasets (LIAR, FakeNewsNet, validación argentina)
- `wiki/solucion/pipeline-preprocesamiento.md` — pipeline de limpieza, normalización, tokenización, BETO

**Páginas actualizadas:** `index.md`, `wiki/proyecto/propuesta.md` (arquitectura 4 módulos), `wiki/competencia/analisis-competitivo.md` (tabla comparativa + ERIC)

Respuestas documentadas a preguntas sobre:
1. **Restricciones ético/legales:** Datos públicos only, LPDP compliance, copyright fair use, no ToS violations si usas APIs oficiales
2. **Selección de datasets:** LIAR (12.8k en inglés) + FakeNewsNet (11.8k) para entrenamiento; recolección manual de 200-500 posts argentinos para validación
3. **Pipeline de datos:** Limpieza (remover URLs, mentions, emojis) → Normalización (minúsculas, números → `<NUM>`) → Tokenización (spaCy) → Vectorización (BETO + pooling `[CLS]`)
4. **Manejo de español rioplatense:** Voseo OK, diminutivos/aumentativos OK, watchout spanglish

---

## [2026-04-19] update | Metodología técnica — arquitectura ML/DL de 4 módulos

**Páginas creadas:** `wiki/solucion/metodologia-tecnica.md`
**Páginas actualizadas:** `index.md`

Documento completo que especifica:
- **Módulo 1 (Deep Learning):** Fine-tune Transformer (BETO/XLM-RoBERTa) para clasificación de contenido desinformativo
- **Módulo 2 (Machine Learning):** Logistic Regression o pequeña NN para evaluación de credibilidad de fuente (metadatos de cuenta)
- **Módulo 3 (DL + Information Retrieval):** Web search en medios confiables + búsqueda en fuentes oficiales (infoleg.gob.ar, indec.gob.ar, bcra.gob.ar, minedu.gob.ar, boletin.gob.ar, etc.) — sin dependencia de Chequeado.com, expandido a múltiples fuentes de verdad
- **Módulo 4 (Ensemble):** Weighted combination o pequeña NN que sintetiza los 3 scores en decisión final

Decisión clave: reemplazo de búsqueda en Chequeado.com por **web search + fuentes oficiales**. Esto permite:
- Detectar desinformación nueva (antes de que medios la cubran)
- Acceso a "verdad de campo" (leyes, datos oficiales, decretos)
- Reducción de sesgo editorial (múltiples fuentes)
- Mayor precisión para claims sobre legislación, datos económicos, salud, educación

Incluye: casos de uso, limitaciones, ventajas, flujo end-to-end ejemplificado, tabla resumen de técnicas ML/DL usadas.

---

## [2026-04-16] update | Descripción final de la propuesta de tema

**Páginas actualizadas:** `wiki/proyecto/propuesta.md`

Sección "Descripción" finalizada y guardada. Cubre: contexto del problema (Reuters Institute 2024), crisis de confianza en medios argentinos, IA generativa como vector nuevo, gap de las soluciones existentes, modelo de negocio ciudadano+B2B, solución técnica de 3 módulos, segmento target 16-80 años, pros/contras, MVP y futuros releases.

---

## [2026-04-16] update | Modelo de negocio y diferenciador definidos

**Páginas actualizadas:** `wiki/proyecto/propuesta.md`

Decisión clave: modelo ciudadano-gratuito + B2B. La capa ciudadana no es filantropía — genera datos anonimizados de tendencias de desinformación local que se venden como API y reportes a medios, fact-checkers y centros de investigación. Diferenciador vs Cyabra/Blackbird.AI: ellos son pure enterprise sin capa ciudadana; nosotros construimos el activo diferencial (datos reales) a través de la adopción masiva.

---

## [2026-04-16] update | Propuesta — segmento target, futuros releases, limitaciones

**Páginas actualizadas:** `wiki/proyecto/propuesta.md`

Decisiones incorporadas: segmento target 16-80+ años (ciudadano común + periodista/editor como screening tool). Futuros releases: multimedia/deepfakes, WhatsApp/Telegram, grafos de propagación. Limitación principal reconocida: falsos positivos en contenido satírico/irónico.

---

## [2026-04-16] ingest | Contexto del problema — estadísticas de desinformación en Argentina

**Páginas creadas:** `wiki/proyecto/contexto-problema.md`
**Páginas actualizadas:** `index.md`

Relevamiento de estadísticas verificadas para la Propuesta de Tema. Fuente principal: Reuters Institute Digital News Report 2024 (cobertura local: La Nación). Datos clave: confianza en medios 30% (menor de LATAM), interés en noticias colapsó de 77% (2017) a 45% (2024), WhatsApp 93% de penetración. Vector nuevo documentado: IA generativa (deepfakes políticos, AI slop) como protagonista de la desinformación 2024-2025. Narrativa base definida para usar en la Descripción de la propuesta.

---

## [2026-04-16] ingest | Kwon & Jang (IEEE 2025) — Survey de detección de fake text (misinformación + LM-generated)

**Fuente:** `raw/A Comprehensive Survey of Fake Text Detection on Misinformation and LM-Generated Texts.md`  
**Páginas creadas:**
- `wiki/estado-del-arte/kwon-jang-2025-survey-fake-text.md`
- `wiki/marco-teorico/tipos-fake-text.md`
- `wiki/marco-teorico/enfoques-deteccion.md`

**Páginas actualizadas:** `index.md`

Primer survey que unifica misinformación y texto generado por LM. Cubre: TF-IDF/SVM (baseline), CNN/RNN/LSTM, GNN (propagación), Transformers (BERT/XLNet/RoBERTa), DetectGPT, watermarking. Resultado destacado: ensemble BERT+ALBERT+XLNet → 99% en COVID fake news. Justifica el uso de transformers + features de contexto de fuente para el PFI.

---

## [2026-04-16] ingest | Albtoush et al. (PeerJ 2025) — Survey fake news detection, foco árabe (análogo al español)

**Fuente:** `raw/Fake news detection state-of-the-art review and advances with attention to Arabic language aspects.md`  
**Páginas creadas:** (compartidas con ingest anterior — tipos-fake-text, enfoques-deteccion)  
**Páginas actualizadas:** `wiki/estado-del-arte/albtoush-2025-arabic-fake-news.md`, `index.md`

Survey 2020-2024 de ML/DL/Transformers para fake news. El foco en árabe es directamente análogo al desafío en español rioplatense: idioma low-resource, dialectos, datasets escasos. Resultado clave: transformers especializados en el idioma (AraBERT ≈ BETO/XLM-RoBERTa para español) superan consistentemente a modelos genéricos. Incluye tabla comparativa de 13+ estudios y datasets. Justifica BETO o XLM-RoBERTa como modelo principal del PFI.

---

## [2026-04-13] update | Objetivo general, objetivos específicos y alcance definidos

**Páginas actualizadas:** `wiki/proyecto/propuesta.md`, `wiki/00-resumen.md`

Decisiones clave tomadas:
- **Objetivo**: servicio de detección de desinformación para ciudadanos argentinos en redes sociales y medios digitales
- **Arquitectura de 3 módulos**: (1) clasificador NLP (BETO/XLM-RoBERTa), (2) score de credibilidad de fuente, (3) contraste semántico con fuentes confiables (similitud vectorial + corpus Chequeado.com)
- **Output**: score de probabilidad + evidencia (links a fuentes que corroboran/contradicen)
- **Plataformas**: Twitter/X, Instagram, Facebook, Infobae.com, Clarín.com
- **Temática**: política, economía y sociedad argentina
- **Entregables MVP**: extensión Chrome + modelo en HuggingFace + dashboard web
- **Dataset**: en español, a construir/adaptar (Chequeado.com como fuente principal)
- **Usuario objetivo**: ciudadanos comunes (primario) + periodistas/editores (secundario)
- **Fuera del alcance**: apps móviles, análisis multimedia, grafos de propagación, otros idiomas/plataformas

---

## [2026-04-13] ingest | Web search — competidores e implementaciones de referencia

**Fuentes:** búsquedas web (GitHub, G2, TechCrunch, LatAm Journalism Review, JournalismAI, etc.)
**Páginas creadas:**
- `wiki/implementaciones/gnn-fakenews-safe-graph.md`
- `wiki/implementaciones/fake-news-detector-br.md`
- `wiki/implementaciones/newtral-factflow.md`

**Páginas actualizadas:** `wiki/competencia/analisis-competitivo.md`, `index.md`

Panorama de competidores y repos de referencia relevados:
- **Competidores comerciales**: Cyabra, Blackbird.AI, Newtral FactFlow, Information Tracer
- **Implementaciones open-source**: safe-graph/GNN-FakeNews (grafos de propagación), fake-news-detector (Chrome/Firefox + crowdsourcing, LATAM)
- **Repos BERT**: múltiples implementaciones en PyTorch (LIAR dataset, BERT+GAT, DistilBERT, Siamese BERT)
- **Contexto LATAM en español**: Newtral FactFlow (70% español), Fake News Detector BR (portugués), Chequeado.com (Argentina, fact-checkers humanos)

---

## [2026-04-13] ingest | Information Tracer — plataforma de inteligencia en redes sociales

**Fuente:** `raw/Information Tracer.md` (artículo web, informationtracer.com)
**Página creada:** `wiki/implementaciones/information-tracer.md`
**Páginas actualizadas:** `wiki/competencia/analisis-competitivo.md`, `index.md`

Plataforma SaaS de detección de manipulación coordinada y bots en X, Facebook, Instagram, Reddit, YouTube, Bluesky y LinkedIn. Usado por periodistas (Tortoise Media) y académicos (CMU, Tsinghua). Modelo cerrado. Enfoque en manipulación coordinada, no en verificación de claims individuales.

---

## [2026-04-13] ingest | Diggity — MediaParty Trust API, análisis de calidad periodística

**Fuente:** `raw/timmd-9216mediaparty-trust-api Diggity a tool for checking the quality of journalistic content.md` (GitHub)
**Página creada:** `wiki/implementaciones/diggity-mediaparty.md`
**Páginas actualizadas:** `wiki/competencia/analisis-competitivo.md`, `index.md`

Herramienta open-source ganadora del MediaParty Hackathon 2025 (Buenos Aires). FastAPI + Stanford Stanza (español) + OpenRouter + DSPy + extensión Chrome. Evalúa calidad periodística (adjetivos cualitativos, extensión, complejidad, tiempos verbales). Sponsors LATAM: Fundación Avina, FUNDAR.

---

## [2026-04-13] update | Tema definido + capa de desarrollo

**Tema:** Sistema de Detección Automática de Desinformación en Redes Sociales (IA)
**Integrantes:** Juan Martín Bejarano Arce

**Nuevas carpetas raw/:** `papers/`, `articulos/`, `implementaciones/`, `datasets/`, `clases/`

**Nuevas páginas wiki:**
- `wiki/datasets/datasets-overview.md` — panorama de datasets
- `wiki/modelos/modelos-overview.md` — taxonomía de enfoques ML
- `wiki/experimentos/experimentos-overview.md` — tabla de experimentos
- `wiki/implementaciones/implementaciones-overview.md` — repos y sistemas de referencia

**Páginas actualizadas:** `CLAUDE.md`, `00-resumen.md`, `proyecto/propuesta.md`, `index.md`

---

## [2026-04-12] setup | Inicialización del wiki

Creación del esqueleto completo del wiki PFI.

**Estructura creada:**
- `CLAUDE.md` — esquema y reglas de operación
- `index.md` — índice de contenido
- `wiki/00-resumen.md` — visión general
- `wiki/proyecto/` — propuesta, cronograma, reuniones, metodología
- `wiki/solucion/` — requerimientos, arquitectura, tecnologías, pruebas
- `wiki/investigacion/user-research.md`
- `wiki/negocio/` — modelo de negocio, análisis financiero
- `wiki/competencia/analisis-competitivo.md`
- `raw/` y `raw/assets/` — directorios para fuentes

**Estado:** Tema del PFI pendiente de definición. Wiki listo para recibir la primera fuente.

**Próximo paso:** Definir el tema del proyecto y actualizar `wiki/proyecto/propuesta.md` y `wiki/00-resumen.md`.
