---
tipo: dataset
nombre: "Fakeddit"
autores: [Nakamura, Kai, Levy, Sharon, Wang, William Yang]
año: 2020
fuente: "Reddit (supervisión distante por subreddits)"
paper: "Nakamura et al. 2020 — LREC 2020 — arXiv:1911.03854"
url-paper: "https://aclanthology.org/2020.lrec-1.755/"
url-github: "https://github.com/entitize/fakeddit"
idioma: inglés
tamaño: 1000000
clases: "2 / 3 / 6"
tarea: clasificacion-multiclase-multimodal
dominio: reddit-multidominio
relevancia: media
---

# Fakeddit

## Descripción

Dataset multimodal de más de 1 millón de muestras extraídas de Reddit con texto + imagen + metadatos + comentarios. Etiquetado mediante supervisión distante (subreddits de noticias falsas vs. subreddits de noticias verificadas). Primer dataset de fake news a escala de millones con multimodalidad.

## Estructura

| Campo | Descripción |
|---|---|
| Título | Título del post de Reddit |
| Imagen | Imagen asociada (cuando existe) |
| Metadata | Subreddit, upvotes, timestamp, ID de autor |
| Comentarios | Comentarios del post (10 más votados) |
| Etiqueta | 2 clases (fake/real), 3 clases, o 6 clases finas |

## Tamaño

- Total: ~1.063.106 muestras
- Con imagen: ~682.000 muestras
- Solo texto: ~381.000 muestras

## Clases de etiquetado

**2 clases:** fake / real  
**3 clases:** fake (manipulado) / fake (fabricado) / real  
**6 clases:** satírico, engañoso, parcialmente falso, falso con imagen manipulada, falso con imagen irrelevante, verdadero

## Limitaciones

- Supervisión distante (no anotación humana directa): puede introducir ruido
- Fuente Reddit: no equivalente a medios de comunicación tradicionales
- Solo inglés
- Los ítems "reales" pueden contener desinformación no detectada

## Relevancia para el PFI

Justifica arquitectura multimodal (texto + imagen) si el PFI incluye análisis de imágenes. Para el contexto argentino, la supervisión distante (usar subreddits o canales de WhatsApp etiquetados como falsos/verdaderos) podría replicarse con fuentes locales.

**Clave paper biblio:** `NakamuraEtAl2020`
