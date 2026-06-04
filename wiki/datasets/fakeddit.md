---
titulo: Fakeddit — Dataset Multimodal de Reddit
tipo: dataset
tags: [dataset, fakeddit, reddit, multimodal, imagen-texto, supervision-distante, ingles]
fuentes: [Fakeddit-dataset.md]
actualizado: 2026-06-04
---

# Fakeddit

Fakeddit (Nakamura et al., 2020) es el dataset de fake news a escala de millones con cobertura multimodal (texto + imagen). Es el referente para sistemas que analizan tanto el contenido textual como visual.

## Descripción

| Atributo | Valor |
|---|---|
| Año | 2020 |
| Fuente | Reddit (supervisión distante por subreddits) |
| Tamaño | ~1.063.106 muestras |
| Idioma | Inglés |
| Clases | 2 / 3 / 6 según configuración |
| Disponibilidad | GitHub libre |

## Estructura de los datos

| Campo | Descripción |
|---|---|
| Título | Título del post de Reddit |
| Imagen | Imagen asociada (cuando existe) |
| Metadata | Subreddit, upvotes, timestamp, ID de autor |
| Comentarios | 10 comentarios más votados |
| Etiqueta | Fake/real según subreddit fuente |

### Con/sin imagen

- Con imagen: ~682.000 muestras
- Solo texto: ~381.000 muestras

## Esquema de labels

**2 clases**: fake / real  
**3 clases**: fake manipulado / fake fabricado / real  
**6 clases**: satírico / engañoso / parcialmente falso / falso con imagen manipulada / falso con imagen irrelevante / verdadero

## Supervisión distante

El etiquetado usa **supervisión distante**: los posts en subreddits como r/satire, r/TheOnion, r/fakefacts se clasifican como fake; los posts en r/worldnews, r/news como real. Esto permite escala masiva sin anotación humana, pero introduce ruido.

## Limitaciones

- Inglés exclusivamente
- Fuente Reddit ≠ medios de comunicación (sesgo de plataforma)
- Supervisión distante genera ruido en las etiquetas
- Acceso a imágenes puede requerir re-descarga (los links expiran)

## Relevancia para el PFI

**Relevancia media**. Fakeddit es útil para dos propósitos:

1. **Arquitectura multimodal**: si el PFI incluye análisis de imágenes (el sistema detecta deepfakes o imágenes con texto falso), Fakeddit es el baseline de referencia
2. **Metodología de supervisión distante**: la técnica de usar comunidades/subreddits como proxy de veracidad puede replicarse en español (canales de WhatsApp "antifake" vs. canales que circulan desinformación)

Para la versión 1.0 del sistema (solo análisis de texto), Fakeddit no es prioritario.

**Clave biblio**: `NakamuraEtAl2020`

## Referencias cruzadas
- [[comparacion-datasets]]
- [[wiki/solucion/arquitectura]]

## Fuentes
- [[raw/datasets/Fakeddit-dataset.md]]
