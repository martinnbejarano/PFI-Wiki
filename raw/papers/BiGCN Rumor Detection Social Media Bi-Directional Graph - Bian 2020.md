---
tipo: paper
titulo: "Rumor Detection on Social Media with Bi-Directional Graph Convolutional Networks"
autores: [Bian, Tian, Xiao, Xi, Xu, Tingyang, Zhao, Peilin, Huang, Wenbing, Rong, Yu, Huang, Junzhou]
año: 2020
venue: "Proceedings of the 34th AAAI Conference on Artificial Intelligence (AAAI 2020)"
doi: "10.1609/aaai.v34i01.5393"
url: "https://ojs.aaai.org/index.php/AAAI/article/view/5393"
github: "https://github.com/TianBian95/BiGCN"
relevancia: media
temas: [bigcn, gnn, propagacion, rumores, grafos, deep-learning, estado-del-arte]
---

# Rumor Detection on Social Media with Bi-Directional Graph Convolutional Networks

## Referencia completa

Bian, T., Xiao, X., Xu, T., Zhao, P., Huang, W., Rong, Y. y Huang, J. (2020). Rumor Detection on Social Media with Bi-Directional Graph Convolutional Networks. *Proceedings of the 34th AAAI Conference on Artificial Intelligence*, vol. 34, n.º 01, pp. 549–556. DOI: 10.1609/aaai.v34i01.5393.

## Resumen

Modelo BiGCN con dos grafos convolucionales direccionales: top-down (modela la propagación directa de rumores) y bottom-up (modela la dispersión de respuestas). Cada grafo aplica GCN para capturar aspectos causales y estructurales de la difusión en Twitter y Weibo.

## Hallazgos clave

- Supera al estado del arte en Twitter16, Twitter15 y Weibo datasets para detección de rumores
- La bidireccionalidad (top-down + bottom-up) captura patrones complementarios de difusión
- El modelo aprovecha la estructura del árbol de conversación (replies, retweets)
- Código disponible en GitHub

## Limitaciones

- Requiere datos de propagación (árbol de conversación): no funciona sobre texto aislado
- Entrenado en inglés (Twitter) y chino (Weibo)
- No evaluado en español ni LATAM

## Relevancia para el PFI

Referencia de arquitectura para el componente de análisis de propagación, si el PFI lo incluye en iteraciones futuras. Actualmente el alcance del PFI no incluye propagación (declarado en propuesta.md), pero BiGCN es útil para contextualizar qué existe en el estado del arte en ese eje.

**Clave biblio:** `BianEtAl2020`
