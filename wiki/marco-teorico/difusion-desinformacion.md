---
titulo: Difusión de Desinformación — Marcos Teóricos y Evidencia Empírica
tipo: concepto
tags: [desinformacion, misinformacion, difusion, redes-sociales, twitter, wardle, vosoughi, lazer]
fuentes: [Information Disorder Framework - Wardle Derakhshan 2017.md, The Spread of True and False News Online - Vosoughi 2018.md, The Science of Fake News - Lazer 2018.md]
actualizado: 2026-06-04
---

# Difusión de Desinformación — Marcos Teóricos y Evidencia Empírica

La detección automatizada de desinformación requiere una comprensión precisa de qué se detecta (taxonomía), cómo se propaga (dinámica) y cuál es la evidencia empírica de su impacto. Esta página consolida los tres marcos teóricos fundamentales del campo.

## Taxonomía: "Desorden de Información" (Wardle & Derakhshan, 2017)

El informe de Wardle & Derakhshan (2017) para el Consejo de Europa establece la distinción conceptual más citada del campo. La clasificación distingue tres tipos según la **intención del emisor** y la **veracidad del contenido**:

| Tipo | Definición | Intención | Veracidad |
|---|---|---|---|
| **Misinformación** | Información falsa compartida sin intención de dañar | Sin intención maliciosa | Falsa |
| **Desinformación** | Información falsa creada y compartida deliberadamente para dañar | Intencional | Falsa |
| **Malinformación** | Información verdadera compartida con intención de dañar | Maliciosa | Verdadera |

Esta trilogía es fundamental porque **"fake news"** es un término políticamente cargado y semánticamente impreciso. La literatura académica prefiere *misinformation* y *disinformation* (en inglés) como términos técnicos.

### Formatos de contenido dañino (Wardle, 2017)

Wardle identifica 7 tipos de contenido que circulan en redes:

1. **Sátira o parodia**: sin intención de daño, pero puede engañar
2. **Contenido engañoso**: uso engañoso de información real
3. **Contenido impostor**: falsificación de fuentes genuinas
4. **Contenido fabricado**: contenido nuevo 100% falso
5. **Contenido de contexto falso**: información verídica + contexto falso
6. **Contenido manipulado**: información genuina manipulada (deepfake, photo editing)
7. **Conexión falsa**: titulares, visuales o leyendas no respaldados por el contenido

Esta taxonomía orienta el **diseño de los labels** del sistema del PFI y justifica por qué la clasificación binaria (verdadero/falso) es insuficiente.

## Evidencia empírica: "The Spread of True and False News Online" (Vosoughi et al., 2018)

Vosoughi, Roy & Aral (2018), publicado en *Science*, analizó todos los rumores verificados difundidos en Twitter entre 2006 y 2017: **126.000 *claim cascades*** propagadas por ~3 millones de usuarios.

### Hallazgos principales

- Las noticias falsas se propagan **6 veces más rápido** que las verdaderas
- Llegan a **20 veces más personas** que las noticias verdaderas
- Tienen **70% más probabilidad de ser retwitteadas** que las verdaderas
- Las noticias falsas son **más novedosas** (mayor distancia semántica de tweets previos) — la novedad activa la respuesta emocional y el compartido
- Los **humanos** (no los bots) son los principales amplificadores de desinformación

### Implicaciones para el PFI

Estos hallazgos justifican dos decisiones de diseño del sistema:
1. La velocidad de propagación como **señal de detección** (un contenido que se difunde anormalmente rápido merece más atención)
2. El análisis del **grafo de propagación** como fuente de evidencia complementaria al texto

> ⚠️ CONTRADICCION potencial: la afirmación "los humanos amplifican más que los bots" contrasta con narrativas comunes sobre la influencia de las granjas de bots. Ver evidencia adicional en [[wiki/estado-del-arte/brechas-espanol-latam]].

## Marco institucional: "The Science of Fake News" (Lazer et al., 2018)

Lazer et al. (2018) publicaron en *Science* un artículo de revisión firmado por 24 investigadores de múltiples disciplinas. Establece el marco interdisciplinario para el estudio científico de las *fake news*.

### Definición operacional

El artículo define *fake news* como "información fabricada que imita el formato de contenido noticioso pero carece de los procesos editoriales que garantizan la precisión y la credibilidad". Esta es la definición que adopta el PFI para el módulo de clasificación.

### Causas de propagación identificadas

1. **Sesgo de confirmación** (*confirmation bias*): los usuarios comparten contenido que confirma sus creencias previas
2. **Heurísticas de compartido**: si viene de alguien conocido, se comparte sin verificar
3. **Incentivos económicos**: las *fake news* generan clicks → ingresos publicitarios
4. **Plataformas algorítmicas**: los algoritmos de recomendación amplifican contenido con alta interacción, sin importar su veracidad

### Recomendaciones de los autores

- Colaboración plataformas-académicos para acceso a datos (relevante para el PFI: scraping vs. APIs)
- Alfabetización digital como intervención complementaria
- Fact-checkers independientes como fuente de ground truth

## Relación entre los tres marcos

Los tres papers son complementarios y se citan mutuamente:

```
Wardle & Derakhshan (2017) → DEFINE qué es desinformación
       ↓
Vosoughi et al. (2018) → MIDE cómo se propaga
       ↓
Lazer et al. (2018) → EXPLICA por qué se propaga y cómo combatirla
```

Los tres son obligatorios en el Marco Teórico del documento LaTeX (chapter02.tex).

## Contexto argentino

La evidencia de Vosoughi et al. (2018) aplica globalmente, pero el contexto argentino tiene particularidades:
- WhatsApp como vector principal de difusión (mensajería cerrada, no monitoreable)
- Ecosistema de medios polarizado (La Nación, Clarín, Página 12, Infobae)
- Período electoral 2023–2025 como pico de producción de desinformación documentado

Ver: [[wiki/proyecto/contexto-problema]] para estadísticas locales.

## Referencias cruzadas
- [[wiki/marco-teorico/tipos-fake-text]]
- [[wiki/marco-teorico/fact-checking-automatico]]
- [[wiki/proyecto/contexto-problema]]
- [[wiki/estado-del-arte/brechas-espanol-latam]]

## Fuentes
- [[raw/papers/Information Disorder Framework - Wardle Derakhshan 2017.md]]
- [[raw/papers/The Spread of True and False News Online - Vosoughi 2018.md]]
- [[raw/papers/The Science of Fake News - Lazer 2018.md]]
