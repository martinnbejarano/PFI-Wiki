# Log del Wiki PFI

> Registro cronológico append-only. Formato de cada entrada: `## [YYYY-MM-DD] tipo | descripción`
> Tipos: `setup` | `ingest` | `query` | `lint` | `update`

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
