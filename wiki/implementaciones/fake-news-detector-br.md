---
titulo: Fake News Detector (Brazil) — Extensión Chrome/Firefox con clasificación colaborativa
tipo: entidad
tags: [implementacion, open-source, chrome-extension, firefox, portugues, latam, crowdsourcing, clasificacion-multi-clase]
fuentes: []
actualizado: 2026-07-04
---

# Fake News Detector — Proyecto Brasileño

## Qué es

Extensión open-source para Chrome y Firefox que detecta y etiqueta noticias directamente en Facebook. El usuario ve badges sobre el contenido que consume mientras navega. Originalmente desarrollado para contexto brasileño (portugués), con planes de internacionalización.

- Repo principal: https://github.com/fake-news-detector/fake-news-detector
- Repo extensión: https://github.com/fake-news-detector/extension
- Backend IA ("Robinho"): https://github.com/fake-news-detector/fake-news-detector/tree/master/robinho
- Tipo: open-source

## Qué hace

Clasifica contenido en **6 categorías**, no solo binario (real/falso):

| Categoría | Descripción |
|---|---|
| **Legítimo** | Noticia verificable, fuente confiable |
| **Fake News** | Contenido deliberadamente falso |
| **Click Bait** | Titular engañoso diseñado para generar clics |
| **Extremadamente Sesgado** | Opinión presentada como noticia objetiva |
| **Sátira** | Contenido humorístico mal interpretado como real |
| **No es noticia** | Contenido que no aplica análisis |

Esta taxonomía de 6 clases es más realista que la clasificación binaria real/falso. La desinformación raramente es 100% falsa — frecuentemente es clickbait, sesgo extremo o sátira sacada de contexto.

## Arquitectura

- **Frontend**: Extensión Chrome/Firefox (JavaScript) integrada con el feed de Facebook
- **Backend "Robinho"**: API de IA que recibe el URL/texto del artículo y devuelve la clasificación
- **Modelo**: [sin verificar] clasificador de texto entrenado sobre datos etiquetados por la comunidad
- **Componente colaborativo**: los usuarios pueden votar sobre clasificaciones → los votos retroalimentan el modelo

## Stack (inferido del repo)

| Componente | Tecnología |
|---|---|
| Extensión | JavaScript, WebExtensions API |
| Backend | API REST |
| Modelo | ML sobre texto (detalles en `robinho/`) |
| Idioma primario | Portugués brasileño |

## Diferencias con Diggity

| Dimensión | Fake News Detector (BR) | Diggity |
|---|---|---|
| Plataforma objetivo | Facebook (feed) | Sitios de noticias (Infobae, etc.) |
| Clasificación | 6 clases (fake, clickbait, sesgo, sátira...) | 4 métricas de calidad periodística |
| Enfoque | Veracidad + tipo de contenido | Calidad lingüística / objetividad |
| Crowdsourcing | Sí (votos de usuarios) | No |
| Idioma | Portugués (+ internacionalización planeada) | Español (Stanza) |

## Relevancia para el PFI

### Taxonomía de 6 clases

Este es probablemente el aporte más valioso para el PFI. La clasificación binaria (real/falso) es demasiado simplista:
- Un artículo con titular clickbait pero contenido mayormente correcto no es "fake news"
- La sátira mal interpretada es desinformación pero no mentira deliberada
- El sesgo extremo es diferente a la falsedad factual

**Para el PFI**: considerar clasificación multi-clase como esta en lugar de solo binario.

### Patrón de integración en Facebook

La extensión inyecta badges directamente en el feed de Facebook — es el mismo patrón de integración (leer el DOM del feed e inyectar feedback visual) que el PFI aplica sobre el *timeline* de Twitter/X, su única plataforma de detección. El repo muestra cómo detectar contenido en el feed y cómo mostrar feedback visual sin depender de la API de la red social.

### Crowdsourcing como señal adicional

Los votos de usuarios son una señal de ground truth distribuido. Interesante para el PFI si hay un componente de validación con usuarios reales, previsto para la Entrega 5.

### Contexto LATAM

Aunque es en portugués brasileño, el dominio (desinformación en redes sociales en Sudamérica) es directamente análogo al contexto argentino/latinoamericano del PFI.

## Limitaciones

- El proyecto parece estar inactivo o con poco mantenimiento reciente
- La integración con el feed de Facebook depende de que Facebook no cambie su HTML (frágil)
- El componente colaborativo requiere masa crítica de usuarios para funcionar bien
- No está claro qué modelo específico usa "Robinho" — la documentación es limitada

## Anti-patrones a tener en cuenta

- Depender del DOM de Facebook para detectar artículos es un anti-patrón: cualquier rediseño de UI rompe la extensión
- Un patrón más robusto: detectar la URL del artículo y analizarla directamente

## Proyectos relacionados en la misma línea

- **ro-afonso/fake-news-pt-eu**: Detección de fake news en portugués europeo con extensión Chrome + app Android + AWS EC2 + ML/DL — https://github.com/ro-afonso/fake-news-pt-eu
- **Fake.br-Corpus**: Dataset de noticias falsas y verdaderas en portugués brasileño (alineadas) — https://github.com/roneysco/Fake.br-Corpus
- **brauliotegui/FAKE**: Detector de fake news brasileño basado en NLP ML — https://github.com/brauliotegui/FAKE

## Referencias cruzadas

- [[wiki/implementaciones/implementaciones-overview]]
- [[wiki/implementaciones/diggity-mediaparty]]
- [[wiki/implementaciones/information-tracer]]
- [[wiki/solucion/arquitectura]]
- [[wiki/solucion/requerimientos]]
