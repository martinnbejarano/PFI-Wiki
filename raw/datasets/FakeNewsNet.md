---
tipo: dataset
nombre: "FakeNewsNet"
autores: [Shu, Kai, Mahudeswaran, Deepak, Wang, Suhang, Lee, Dongwon, Liu, Huan]
año: 2020
fuente: "PolitiFact.com + GossipCop"
paper: "Shu et al. 2020 — Big Data — DOI: 10.1089/big.2020.0062"
url-github: "https://github.com/KaiDMML/FakeNewsNet"
url-paper: "https://www.liebertpub.com/doi/full/10.1089/big.2020.0062"
idioma: inglés
clases: 2
tarea: clasificacion-binaria
dominio: politica-entretenimiento
relevancia: alta
---

# FakeNewsNet

## Descripción

Repositorio de fake news que integra tres dimensiones: contenido de noticias, contexto social y datos espacio-temporales. Es el dataset más rico en información contextual y de propagación disponible públicamente.

## Subsets

### PolitiFact
- ~314 noticias (157 fake, 157 reales)
- ~41.000 nodos de difusión social (tweets, retweets)
- Fuente de veracidad: PolitiFact.com

### GossipCop
- ~5.464 artículos (fake y reales)
- ~314.000 nodos de difusión
- Fuente de veracidad: GossipCop.com (entretenimiento y celebrities)

## Estructura de datos

| Dimensión | Contenido |
|---|---|
| Contenido | Texto completo del artículo, título, imágenes, metadata, autores |
| Contexto social | Tweets sobre la noticia, perfiles de usuarios, reacciones |
| Espacio-temporal | Timestamps, geolocalización, secuencia de difusión |

**Total:** ~23.196 ítems de fake news + ~690.732 tweets asociados

## Limitaciones

- No distribuible directamente: políticas de privacidad de Twitter/X y restricciones de copyright
- Requiere recrawling desde GitHub (los datos se obtienen vía APIs de Twitter y scraping de medios)
- Solo inglés; dominios política y entretenimiento US

## Relevancia para el PFI

Modelo de arquitectura para construir un dataset argentino equivalente: noticias de Infobae/Clarín + tweets de usuarios argentinos + etiquetas de Chequeado. La estructura de tres dimensiones (contenido + contexto social + espacio-temporal) es la arquitectura ideal para el dataset del PFI.

**Clave paper biblio:** `ShuEtAl2020`
