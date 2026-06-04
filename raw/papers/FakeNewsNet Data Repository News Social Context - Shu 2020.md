---
tipo: paper
titulo: "FakeNewsNet: A Data Repository with News Content, Social Context, and Spatiotemporal Information for Studying Fake News on Social Media"
autores: [Shu, Kai, Mahudeswaran, Deepak, Wang, Suhang, Lee, Dongwon, Liu, Huan]
año: 2020
venue: "Big Data, vol. 8, no. 3. Mary Ann Liebert"
doi: "10.1089/big.2020.0062"
url: "https://www.liebertpub.com/doi/full/10.1089/big.2020.0062"
arxiv: "1809.01286"
github: "https://github.com/KaiDMML/FakeNewsNet"
relevancia: alta
temas: [dataset, fakenewsnet, fake-news, redes-sociales, propagacion, grafos, multimodal]
---

# FakeNewsNet: A Data Repository with News Content, Social Context, and Spatiotemporal Information

## Referencia completa

Shu, K., Mahudeswaran, D., Wang, S., Lee, D. y Liu, H. (2020). FakeNewsNet: A Data Repository with News Content, Social Context, and Spatiotemporal Information for Studying Fake News on Social Media. *Big Data*, vol. 8, n.º 3, pp. 171–188. DOI: 10.1089/big.2020.0062.

## Resumen

Repositorio de fake news que integra tres dimensiones: (1) contenido de noticias (texto completo, imágenes, metadata); (2) contexto social (tweets, retweets, perfiles de usuarios, reacciones); (3) información espacio-temporal. Dos subsets: PolitiFact (~314 noticias) y GossipCop (~5.464 artículos).

## Hallazgos clave

- PolitiFact subset: 314 noticias (157 fake, 157 reales) + ~41.000 nodos de difusión social
- GossipCop subset: 5.464 artículos + ~314.000 nodos; total 23.196 ítems de fake news
- ~690.732 tweets asociados con contenido del dataset
- Primer dataset que integra contenido + contexto social + datos espacio-temporales
- Arquitectura de 3 dimensiones: el contexto social captura información que el texto solo no puede
- Dataset dinámico (re-crawlable via GitHub)

## Limitaciones

- No distribuible directamente: políticas de privacidad de Twitter/X y restricciones editoriales impiden distribución de contenido completo
- Solo inglés; contexto político y entretenimiento estadounidense
- Requiere recrawling para reproducir el dataset completo

## Relevancia para el PFI

Modelo de arquitectura para el dataset argentino del PFI. La integración de contexto social (tweets de usuarios argentinos reaccionando a noticias de Infobae/Clarín) + datos de verificación de Chequeado replicaría la estructura de FakeNewsNet para el contexto local.

**Clave biblio:** `ShuEtAl2020`
