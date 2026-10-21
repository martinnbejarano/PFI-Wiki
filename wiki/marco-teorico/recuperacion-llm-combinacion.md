---
titulo: TF-IDF, búsqueda vectorial, LLM, RAG, postura y combinación de señales
tipo: concepto
tags: [marco-teorico, tf-idf, embeddings, hnsw, llm, prompt-injection, rag, stance, ensemble, calibracion]
fuentes: [SaltonBuckley1988, Cox1958, ReimersGurevych2019, MalkovYashunin2020, BrownEtAl2020, WeiEtAl2022, GreshakeEtAl2023, LewisEtAl2020, HanselowskiEtAl2018, ThorneEtAl2018, Dietterich2000, Wolpert1992, Platt1999, GuoEtAl2017]
actualizado: 2026-10-20
---

# TF-IDF, búsqueda vectorial, LLM, RAG, postura y combinación de señales

Teoría agregada al marco teórico del documento (cap. 2) por el issue #72. Cubre las técnicas que el sistema usa y que el marco teórico no explicaba. Las decisiones de diseño viven en el cap. 4; acá queda solo la teoría.

| Tema | Idea central | Fuente | Dónde en el cap. 2 |
|---|---|---|---|
| TF-IDF + regresión logística | Bolsa de palabras ponderada por frecuencia inversa de documento; clasificador lineal sigmoide por máxima verosimilitud. Es la línea base: eficiente e interpretable, pero no ve sinónimos ni contexto | Salton y Buckley 1988; Cox 1958 | NLP, antes de los *word embeddings* |
| *Embeddings* de oración | Sentence-BERT: red siamesa, similitud del coseno. Buscar el par más parecido entre 10.000 oraciones: ~65 h con BERT como codificador cruzado, ~5 s con SBERT | Reimers y Gurevych 2019 | `sec:busqueda-vectorial` |
| Búsqueda ANN | HNSW: grafo de proximidad de varias capas, búsqueda voraz, complejidad logarítmica | Malkov y Yashunin 2020 | `sec:busqueda-vectorial` |
| LLM y *prompting* | Aprendizaje en contexto *zero/few-shot* (GPT-3, 175.000 M de parámetros); ajuste por instrucciones (FLAN supera a GPT-3 *zero-shot* en 20 de 25 conjuntos); salida estructurada | Brown et al. 2020; Wei et al. 2022 | `sec:llm` (ahí se define la sigla LLM) |
| Inyección de instrucciones | La inyección indirecta mete órdenes en contenido de terceros (páginas, mensajes); la salida de un LLM que lee contenido no confiable tampoco es confiable | Greshake et al. 2023 | `sec:llm` |
| RAG | Memoria paramétrica + índice denso no paramétrico; salida más factual, conocimiento actualizable sin reentrenar, procedencia → *grounding* y atribución | Lewis et al. 2020 | `sec:deteccion`, 2.ª etapa |
| Detección de postura | FNC-1 (agree/disagree/discuss/unrelated): la métrica oficial premiaba a la clase mayoritaria, así que se propone F1 macro. FEVER: 185.445 afirmaciones, Supported/Refuted/NotEnoughInfo | Hanselowski et al. 2018; Thorne et al. 2018 | `sec:deteccion`, 3.ª etapa |
| *Ensembles* | Fusión temprana y tardía; por qué funciona un conjunto (errores distintos y mejores que el azar); promedio ponderado frente a *stacking* | Dietterich 2000; Wolpert 1992 | `sec:combinacion-calibracion` |
| Calibración | Salida *softmax* ≠ probabilidad; las redes modernas son sobreconfiadas; escalado de Platt y de temperatura; la transformación monótona no cambia el AUC | Platt 1999; Guo et al. 2017 | `sec:combinacion-calibracion` |

## Correcciones conceptuales del mismo issue

- **BERT**: el documento ya no dice «10–20 puntos». Usa lo que reporta Devlin et al. 2019: GLUE 80,5 (+7,7 absolutos) y MultiNLI 86,7 % (+4,6).
- **Puntaje, no probabilidad**: ni el clasificador ni el combinador están calibrados. En el documento, la extensión y el panel, el valor que se muestra se llama **«puntaje de confianza»** (en que la afirmación sea verdadera). Las preguntas de la encuesta y la entrevista conservan su redacción original («puntaje de probabilidad») porque es lo que se preguntó.
- **Error más costoso**: es el **falso positivo**, marcar como falso un contenido verídico (art. 113 CP y atribución a las fuentes). El objetivo 1 del cap. 1 prioriza la precisión de la clase *falso* e informa la cobertura. La teoría de métricas quedó neutral: cuál error importa más depende del diseño.

## Referencias cruzadas
- [[nlp-fundacional]]
- [[transformers-bert]]
- [[fact-checking-automatico]]
- [[enfoques-deteccion]]
- [[wiki/solucion/arquitectura]]

## Fuentes
- `documento/biblio.bib` (claves en el frontmatter)
