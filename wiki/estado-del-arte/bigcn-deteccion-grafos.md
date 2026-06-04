---
titulo: BiGCN — Detección de Rumores via Grafo Bidireccional (Bian et al., 2020)
tipo: fuente
tags: [estado-del-arte, grafos, gnn, bigcn, propagacion, rumore-detection, bian]
fuentes: [BiGCN Rumor Detection Social Media Bi-Directional Graph - Bian 2020.md]
actualizado: 2026-06-04
---

# BiGCN — Detección de Rumores via Grafo Bidireccional

## Referencia

> Bian, T., Xiao, X., Xu, T., Zhao, P., Huang, W., Rong, Y., Huang, J. (2020). *Rumor Detection on Social Media with Bi-Directional Graph Convolutional Networks*. AAAI 2020. Clave biblio: `BianEtAl2020`

## Motivación

Los métodos basados en texto analizan el **contenido** de la noticia, pero ignoran **cómo se propaga**. Vosoughi et al. (2018) demostraron que las noticias falsas se difunden de manera diferente a las verdaderas (más rápido, más lejos, con patrones de cascada distintos). BiGCN explota esta señal estructural.

## Arquitectura

BiGCN modela el árbol de difusión de un post como un grafo y aplica Graph Convolutional Networks (GCN) en dos direcciones:

```
Post original
     ↓
[Árbol de propagación → Grafo]
     ↓
Top-Down GCN: modela cómo se expande el rumor
     +
Bottom-Up GCN: modela las respuestas / correcciones
     ↓
Concatenación de embeddings
     ↓
Clasificación: rumor verdadero / falso / no verificado / no-rumor
```

**Top-Down**: simula la propagación natural (un usuario comparte, sus seguidores recomparten)  
**Bottom-Up**: captura las respuestas que refutan o confirman el claim (un hilo de Twitter donde usuarios dicen "esto es falso")

## Resultados

Evaluado en PHEME (Twitter, inglés) y Weibo (chino):

| Dataset | Accuracy | F1 |
|---|---|---|
| PHEME | ~88% | ~0.87 |
| Weibo | ~96% | ~0.96 |

Supera a métodos basados solo en texto (~78% en PHEME) en ~10 puntos.

## Disponibilidad

Implementación disponible en PyTorch Geometric. Ver [[wiki/implementaciones/gnn-fakenews-safe-graph]] para repositorios de referencia.

## Limitaciones

- Requiere acceso al grafo de propagación (retweets, respuestas): solo posible con API de Twitter
- Las restricciones de API de Twitter/X post-2023 hacen muy difícil obtener estos grafos
- Los grafos de propagación son útiles para eventos con muchos reshares; para noticias de circulación baja, el grafo es escaso

## Relevancia para el PFI

**Media-Alta**: BiGCN justifica el módulo de análisis de propagación en el sistema del PFI como componente optional/futuro. Para la versión 1.0 que analiza texto directamente (sin acceso en tiempo real a los grafos de Twitter), BiGCN es una referencia arquitectural pero no implementable sin API access.

La combinación texto + grafos es la línea de investigación más prometedora según el estado del arte, pero requiere resolver el problema de acceso a datos de propagación en tiempo real.

## Referencias cruzadas
- [[wiki/marco-teorico/difusion-desinformacion]]
- [[wiki/implementaciones/gnn-fakenews-safe-graph]]
- [[wiki/datasets/fakenewsnet]]
- [[comparativa-llms-2024-2025]]

## Fuentes
- [[raw/papers/BiGCN Rumor Detection Social Media Bi-Directional Graph - Bian 2020.md]]
