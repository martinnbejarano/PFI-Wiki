---
titulo: GNN-FakeNews (safe-graph) — Detección de fake news con Redes Neuronales de Grafos
tipo: entidad
tags: [implementacion, open-source, gnn, graph-neural-network, pytorch, fakenewsnet, propagacion, twitter]
fuentes: []
actualizado: 2026-04-13
---

# GNN-FakeNews — safe-graph

## Qué es

Colección de modelos de **Graph Neural Networks (GNN) para detección de fake news**, todos implementados bajo el framework UPFD (User Preference-aware Fake News Detection). Repo académico muy citado, publicado por el grupo safe-graph.

- Repo: https://github.com/safe-graph/GNN-FakeNews
- Framework: PyTorch Geometric
- Tipo: open-source, académico

## Idea central

El problema de detección de fake news se formaliza como **clasificación de grafos**: cada noticia + su red de retweets/comentarios forma un grafo. El modelo aprende a clasificar ese grafo como real o falso analizando cómo se propagó la información, quiénes la compartieron y en qué orden.

Esto contrasta con el enfoque de solo-contenido (BERT sobre el texto del artículo): acá se usa la **propagación en la red social** como señal principal.

## Modelos implementados

| Modelo | Descripción |
|---|---|
| **GCNFN** | Fake news detection con geometric deep learning (grafos de propagación en redes sociales) |
| **BiGCN** | Rumor detection con Graph Convolutional Networks bidireccionales (top-down y bottom-up) |
| **GNN-CL** | GNN con continual learning para detección de fake news en streams de social media |

## Dataset

**FakeNewsNet** (Politifact + GossipCop), extraído de Twitter:
- Noticias verificadas por fact-checkers de Politifact y GossipCop
- Grafo de retweets por noticia (quién retweeteó a quién, en qué orden)
- Metadatos de usuarios (seguidores, seguidos, historial)

Ver: [[wiki/datasets/datasets-overview]] y https://github.com/KaiDMML/FakeNewsNet

## Stack técnico

| Componente | Tecnología |
|---|---|
| Deep Learning | PyTorch |
| Graph ML | PyTorch Geometric |
| Dataset | FakeNewsNet (Twitter graphs) |
| Reproducibilidad | CodeOcean (runs sin configuración manual) |

## Por qué es relevante para el PFI

### La propagación como señal

Una noticia falsa se comporta de forma diferente en la red: se comparte entre cuentas con cierto patrón (bots que amplifican, cuentas nuevas, comunidades específicas). Este enfoque captura esa señal que el análisis de texto puro no puede ver.

Si el PFI apunta a analizar Twitter/X o Reddit, este repo es la referencia más directa para implementar la capa de grafos.

### Complementariedad con BERT

GCNFN/BiGCN y BERT no se excluyen. Un enfoque **ensemble** podría combinar:
1. BERT sobre el texto del artículo → score de veracidad por contenido
2. GNN sobre el grafo de propagación → score de veracidad por comportamiento de difusión
3. Fusión de ambos scores → predicción final

Este es el estado del arte actual en el dominio (ver [[wiki/modelos/modelos-overview]]).

### Limitaciones para el PFI

- Requiere datos de propagación (retweets, replies) — necesita API de Twitter/X u otra red social. Con las restricciones actuales de la API de X (2023+), recolectar grafos de propagación es costoso o imposible para un proyecto académico.
- El dataset está en inglés — para español/LATAM habría que construir un grafo equivalente.
- Computacionalmente más pesado que clasificadores de texto puros.

## Anti-patrones a tener en cuenta

- Los grafos de propagación son ricos en información pero difíciles de obtener en tiempo real para un MVP
- Si la API de la red social cambia o restringe el acceso, el sistema deja de funcionar

## Papers relacionados

- "Fake News Detection on Social Media using Geometric Deep Learning" (GCNFN)
- "Bi-Directional Graph Convolutional Networks for Rumor Detection" (BiGCN)
- "Fake News Detection Through Graph-based Neural Networks: A Survey" — arXiv:2307.12639

## Referencias cruzadas

- [[wiki/implementaciones/implementaciones-overview]]
- [[wiki/modelos/modelos-overview]]
- [[wiki/datasets/datasets-overview]]
- [[wiki/solucion/arquitectura]]
