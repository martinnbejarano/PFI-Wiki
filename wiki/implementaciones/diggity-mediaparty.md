---
titulo: Diggity (MediaParty Trust API) — Análisis de calidad periodística con NLP + LLM
tipo: entidad
tags: [implementacion, open-source, chrome-extension, nlp, llm, periodismo, latam, stanza, fastapi, dspy]
fuentes: [timmd-9216mediaparty-trust-api Diggity a tool for checking the quality of journalistic content.md]
actualizado: 2026-04-13
---

# Diggity — MediaParty Trust API

## Qué es

Herramienta open-source de **evaluación de calidad periodística** construida en el MediaParty Hackathon 2025. Ganó el primer premio. Combina NLP + LLMs para evaluar la objetividad y calidad de artículos periodísticos.

- Repo: https://github.com/timmd-9216/mediaparty-trust-api
- Evento: MediaParty Hackathon 2025 (Buenos Aires, Argentina)
- Sponsors: The World Bank, Internet Society, Fundación Avina, FUNDAR
- Tipo: open-source, Python 3.12+

## Stack técnico

| Componente | Tecnología |
|---|---|
| Backend API | FastAPI (Python) |
| NLP | Stanford Stanza (POS tagging, dependency parsing, **soporta español**) |
| LLM | OpenRouter + DSPy (filtrado de adjetivos cualitativos) |
| Frontend | Extensión de Chrome |
| Arquitectura | API REST + extensión browser |

## Qué hace

Analiza artículos periodísticos en 4 métricas:

| Métrica | Descripción | Umbral |
|---|---|---|
| Adjetivos cualitativos | % de adjetivos de opinión vs. descriptivos (filtrados por LLM) | ≤5% excelente, ≤10% moderado, >10% alto |
| Conteo de palabras | Longitud del artículo | Más palabras = más cobertura |
| Complejidad de oraciones | Promedio de palabras por oración | Óptimo: 15-25 palabras |
| Análisis de tiempos verbales | Distribución de tiempos verbales | Noticias: 40-70% verbos en pasado |

### Flujo de procesamiento

1. Ingesta del artículo (texto + título + autor + URL + fecha)
2. NLP con Stanza: POS tagging, dependency parsing
3. LLM con OpenRouter + DSPy: filtra adjetivos subjetivos vs. objetivos
4. Cálculo de 4 métricas
5. API devuelve scores + explicación en lenguaje natural

### Extensión de Chrome

- Detecta automáticamente cuándo el usuario está en un artículo de noticias (ej: Infobae)
- Análisis con un clic
- Muestra badges de colores directamente en la página (🟢 bueno, 🟡 moderado, 🔴 malo)
- Sin copy-paste manual

## API

**Endpoint:** `POST /api/v1/articles/analyze`

**Request:**
```json
{
    "body": "texto del artículo",
    "title": "título",
    "author": "autor",
    "link": "https://...",
    "date": "YYYY-MM-DD",
    "media_type": "article"
}
```

**Response:** lista de métricas con `criteria_name`, `explanation`, `flag`, `score`

## Relevancia para el PFI

### Qué podemos adaptar

**1. Patrón de extensión de Chrome**
El PFI podría adoptar el mismo patrón: extensión de browser que analiza el contenido en tiempo real mientras el usuario navega. Es un UX limpio que no requiere que el usuario cambie de contexto. Diggity demuestra que es técnicamente viable incluso en un hackathon de 48hs.

**2. Stanford Stanza para español**
Stanza tiene soporte nativo para español. Si el PFI apunta a contenido en español (contexto LATAM), Stanza es una alternativa sólida a spaCy. El hecho de que Diggity lo usara con Infobae (sitio en español) valida su aplicabilidad.

**3. LLM via DSPy + OpenRouter para análisis lingüístico**
El patrón de usar un LLM para tareas de clasificación lingüística fina (distinguir adjetivos cualitativos de descriptivos) con DSPy como framework es replicable. Para el PFI: podría usarse LLM para detectar sesgos o sensacionalismo en el lenguaje.

**4. Arquitectura API-first**
FastAPI como backend con endpoints REST es una arquitectura limpia y extensible. Si el PFI implementa un sistema similar, este patrón de diseño sirve como referencia directa.

**5. Contexto LATAM**
MediaParty es un evento con fuerte presencia argentina/latinoamericana. Los sponsors (Fundación Avina, FUNDAR) y el testeo con Infobae sugieren que el nicho de análisis de medios en español es activo. El PFI entraría en ese mismo espacio.

### Diferencias clave con el PFI

| Dimensión              | Diggity                                              | PFI (tentativo)                                       |
| ---------------------- | ---------------------------------------------------- | ----------------------------------------------------- |
| Foco                   | Calidad lingüística / objetividad periodística       | Veracidad del contenido (fact-checking)               |
| Verificación de hechos | No — evalúa estilo, no verdad                        | Sí — clasificación de veracidad                       |
| Fuentes externas       | No consulta bases de hechos                          | Podría usar fact-checking databases                   |
| Plataformas            | Solo artículos web                                   | Redes sociales (posts, tweets, etc.)                  |
| Dataset                | No usa dataset de entrenamiento — reglas heurísticas | Requiere dataset etiquetado (LIAR, FakeNewsNet, etc.) |
| Modelo ML              | No hay modelo entrenado — análisis lingüístico + LLM | Modelo de clasificación supervisada                   |

### Limitación clave

Diggity evalúa **cómo** está escrito un artículo (estilo, objetividad), no **si lo que dice es verdad**. Una noticia falsa puede estar escrita en perfecto estilo periodístico. El PFI necesita un enfoque diferente: verificación de claims contra evidencia externa o clasificación entrenada con datos etiquetados.

## Limitaciones técnicas del proyecto

- No hay tests implementados aún (`pytest` marcado como "coming soon")
- Requiere API key de OpenRouter para la funcionalidad LLM (aunque degrada gracefully sin ella)
- La extensión de Chrome solo soporta sitios configurados (ej: Infobae) — no es universal
- Construido en hackathon de 48hs: código de prototipo, no producción

## Anti-patrones a evitar

- Métricas únicamente heurísticas sin validación estadística — no está claro si los umbrales (≤5% adjetivos) son empíricamente significativos
- Soporte limitado de sitios en la extensión de Chrome — si el PFI apunta a múltiples redes, necesita una solución más general

## Referencias cruzadas

- [[wiki/implementaciones/implementaciones-overview]]
- [[wiki/implementaciones/information-tracer]]
- [[wiki/solucion/arquitectura]]
- [[wiki/solucion/tecnologias]]
- [[wiki/modelos/modelos-overview]]

## Fuentes

- [[raw/timmd-9216mediaparty-trust-api Diggity a tool for checking the quality of journalistic content.md]]
