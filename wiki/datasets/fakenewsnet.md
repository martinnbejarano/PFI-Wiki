---
titulo: FakeNewsNet — Dataset con Contexto Social
tipo: dataset
tags: [dataset, fakenewsnet, politifact, gossipcop, contexto-social, grafos, ingles]
fuentes: [FakeNewsNet Data Repository News Social Context - Shu 2020.md]
actualizado: 2026-06-04
---

# FakeNewsNet

FakeNewsNet (Shu et al., 2020) es el dataset más completo en cuanto a contexto social: incluye no solo el texto de las noticias sino también la red de usuarios que las difundió en Twitter.

## Descripción

| Atributo | Valor |
|---|---|
| Año | 2020 (actualizado continuamente) |
| Fuente | PolitiFact + GossipCop + datos de Twitter |
| Idioma | Inglés |
| Clases | Binario (real/fake) |
| Disponibilidad | GitHub con scripts de descarga |

## Componentes del dataset

FakeNewsNet tiene dos sub-datasets:

### PolitiFact
- ~500 noticias falsas + ~500 noticias verdaderas
- Política americana
- Ground truth: verificación manual de periodistas

### GossipCop
- ~5.000 noticias falsas + ~22.000 noticias verdaderas
- Entretenimiento y cultura pop
- Ground truth: fact-checking del sitio GossipCop.com

## Dimensiones del dataset (únicas en el campo)

A diferencia de otros datasets que solo incluyen texto, FakeNewsNet provee:

| Dimensión | Descripción |
|---|---|
| Contenido | Título, cuerpo del artículo, imágenes |
| Fuente | Perfil de autor, metadata del sitio |
| Contexto social | Tweets que comparten la noticia |
| Red de difusión | Grafo de retweets (quién retwitteó a quién) |
| Perfil de usuarios | Descripción, seguidores, historial de tweets |
| Información espatiotemporal | Timestamps de todos los eventos |

## Habilitaciones técnicas

El contexto social de FakeNewsNet habilitó una línea completa de investigación en grafos de propagación:
- BiGCN (Bian et al., 2020): grafo bidireccional de difusión
- SAFE: análisis multimodal texto + imagen
- Information Tracer: monitoring de propagación

## Limitaciones

- Solo inglés
- PolitiFact: pocos ejemplos (~1.000 total), aunque con alta calidad de etiquetado
- GossipCop: desbalanceado (4:1 real vs. fake)
- Los datos de Twitter son de difícil acceso post-API changes de 2023
- El contexto social requiere infraestructura adicional para usar (grafos)

## Relevancia para el PFI

FakeNewsNet justifica incluir el módulo de análisis de propagación en el sistema del PFI (Módulo 3 en la arquitectura). Si el sistema monitorea Twitter/X en tiempo real, el grafo de difusión es señal adicional de detección.

El sub-dataset GossipCop, con ~22.000 noticias reales etiquetadas, es una fuente de *negative examples* (noticias verdaderas) para entrenar el modelo base.

**Clave biblio**: `ShuEtAl2020`

## Referencias cruzadas
- [[comparacion-datasets]]
- [[liar-dataset]]
- [[wiki/implementaciones/gnn-fakenews-safe-graph]]

## Fuentes
- [[raw/datasets/FakeNewsNet.md]]
- [[raw/papers/FakeNewsNet Data Repository News Social Context - Shu 2020.md]]
