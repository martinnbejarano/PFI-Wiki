---
tipo: paper
titulo: "Web Retrieval Agents for Evidence-Based Misinformation Detection"
autores: [Tian, Jacob-Junqi, Yu, Hao, Orlovskiy, Yury, Vergho, Tyler, Rivera, Mauricio, Goel, Mayank, Yang, Zachary, Godbout, Jean-Francois, Rabbany, Reihaneh, Pelrine, Kellin]
año: 2024
venue: "arXiv preprint"
doi: "10.48550/arXiv.2409.00009"
arxiv: "2409.00009"
url: "https://arxiv.org/abs/2409.00009"
relevancia: alta
temas: [rag, agentes, web-search, fact-checking, llm, evidence-retrieval, estado-del-arte]
---

# Web Retrieval Agents for Evidence-Based Misinformation Detection

## Referencia completa

Tian, J.-J., Yu, H., Orlovskiy, Y., et al. (2024). Web Retrieval Agents for Evidence-Based Misinformation Detection. arXiv: 2409.00009.

## Resumen

Sistema de fact-checking agentico que combina un LLM (sin acceso a internet) con un agente de búsqueda web. El agente recupera evidencias relevantes en tiempo real y las pasa al LLM para verificación. Evalúa múltiples estrategias de recuperación y agrupación de evidencias.

## Hallazgos clave

- Mejora de hasta **+20% en macro F1** respecto a LLMs sin búsqueda web
- El agente decide qué buscar, cuándo buscar y cómo integrar evidencias
- La calidad del retrieval es determinante: evidencias irrelevantes degradan el rendimiento
- Evaluación principalmente en inglés con datasets estándar de fact-checking

## Limitaciones

- Sesgos de fuentes web (resultados de búsqueda pueden favorecer ciertos medios)
- Sensible a decisiones de diseño del agente (qué queries generar, cómo filtrar)
- Latencia: la búsqueda web agrega tiempo de respuesta
- Evaluado solo en inglés

## Relevancia para el PFI

Arquitectura directamente relevante para el módulo de "contraste semántico con web search" del sistema propuesto. El enfoque RAG (Retrieval Augmented Generation) con búsqueda en tiempo real puede implementarse con Serper.dev + LLM. Este paper justifica ese componente arquitectural.

**Clave biblio:** `TianEtAl2024`
