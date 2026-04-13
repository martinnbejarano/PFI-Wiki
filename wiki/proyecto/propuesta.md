---
titulo: Propuesta de Tema
tipo: proyecto
tags: [propuesta, tema, etapa-1]
actualizado: 2026-04-13
---

# Propuesta de Tema

## Estado: EN ELABORACION

## Criterios de evaluación de la propuesta (según cátedra)

- ¿Es interesante para el autor?
- ¿Aporta algo nuevo?
- ¿La temática es novedosa?
- ¿Hay acceso a fuentes sobre el tema?
- Brainstorming validado

## Tema troncal elegido

**Inteligencia Artificial**

## Nombre del proyecto

**Sistema de Detección Automática de Desinformación en Redes Sociales**

## Idea del proyecto

Construir un sistema que detecte automáticamente contenido desinformativo en redes sociales utilizando técnicas de NLP y modelos de machine learning. El sistema analizará posts/artículos y los clasificará según su veracidad, proporcionando una explicación de la clasificación.

## Problema que resuelve

La desinformación en redes sociales es un problema creciente con impactos reales en la sociedad (salud pública, política, economía). La verificación manual de contenido es inescalable. No existen herramientas accesibles que automaticen este proceso de forma confiable y explicable.

## Propuesta de valor

El sistema se diferencia de las soluciones existentes en cuatro dimensiones:

1. **Contexto local**: foco específico en Argentina (política, economía, sociedad), con un modelo entrenado en español rioplatense y fuentes de referencia locales (Chequeado.com, medios argentinos verificados, cuentas oficiales).
2. **Accesibilidad**: herramienta gratuita y abierta para ciudadanos comunes, a diferencia de competidores comerciales como Cyabra, Blackbird.AI o Newtral FactFlow (orientados a gobiernos y redacciones profesionales).
3. **Análisis híbrido de 3 señales**: combina (a) clasificación lingüística del texto, (b) evaluación de credibilidad de la fuente, y (c) contraste semántico con fuentes confiables — más robusto que el análisis de texto solo, sin la complejidad de grafos de propagación.
4. **Evidencia explicable**: no devuelve solo un score binario, sino links a fuentes que corroboran o contradicen el contenido, permitiendo al usuario entender por qué una publicación fue marcada como sospechosa.

## Objetivo general

Desarrollar un servicio que, mediante la aplicación de técnicas de procesamiento del lenguaje natural e inteligencia artificial, facilite a ciudadanos argentinos la identificación de contenido potencialmente desinformativo en redes sociales y medios digitales, permitiéndoles tomar decisiones informadas sobre la veracidad del contenido que consumen y comparten, en Argentina durante el año 2026.

## Objetivos específicos

1. **Modelo NLP**: Diseñar e implementar un modelo de clasificación de texto basado en arquitectura Transformer (BETO o XLM-RoBERTa) fine-tuneado para detectar indicadores lingüísticos de desinformación en publicaciones en español.
2. **Credibilidad de fuente**: Implementar un módulo que evalúe metadatos de la cuenta o medio publicante (antigüedad, verificación, historial) para complementar el análisis textual con un score de credibilidad de fuente.
3. **Contraste semántico**: Implementar un módulo de contraste contra un corpus de fuentes confiables (medios verificados, cuentas oficiales, verificaciones de Chequeado.com) usando búsqueda de similitud vectorial, que determine si alguna fuente confiable corrobora o contradice el contenido analizado.
4. **Extensión web**: Desarrollar una extensión de navegador web (Google Chrome) que integre los tres módulos y permita al usuario analizar contenido en tiempo real mientras navega por las plataformas objetivo, mostrando un score de confiabilidad con evidencia asociada.
5. **Dashboard**: Desarrollar un panel web donde el usuario pueda consultar el historial de análisis realizados y estadísticas de uso.
6. **Dataset en español**: Construir o adaptar un dataset de entrenamiento en español con foco en contenido argentino/latinoamericano, utilizando verificaciones de Chequeado.com como fuente de etiquetado principal.
7. **Evaluación**: Evaluar el sistema con métricas estándar (Accuracy, Precision, Recall, F1, AUC-ROC) comparando contra baselines (TF-IDF + Logistic Regression) y validando con usuarios reales.

## Alcance preliminar

**Incluido en el MVP:**

| Dimensión | Detalle |
|---|---|
| Plataformas | Twitter/X, Instagram, Facebook, Infobae.com, Clarín.com |
| Temática | Política, economía y sociedad argentina (2026) |
| Idioma | Español (variante rioplatense/argentina) |
| Contenido analizado | Texto (publicaciones, titulares, artículos) |
| Interfaz principal | Extensión de Google Chrome |
| Interfaz secundaria | Dashboard web con historial de análisis por usuario |
| Modelo | Publicado en HuggingFace al finalizar el proyecto |
| Validación | Con usuarios reales (ciudadanos y periodistas) |

## Fuera del alcance

- Aplicaciones móviles nativas (iOS / Android)
- Análisis de contenido multimedia: videos, audios, imágenes — solo texto
- Análisis de grafos de propagación o detección de campañas coordinadas de bots
- Otros idiomas además del español
- Plataformas no listadas: YouTube, TikTok, WhatsApp, Telegram, LinkedIn, etc.
- Desarrollo de una plataforma propia de fact-checking
- Procesamiento en streaming a gran escala
- Temáticas no listadas: entretenimiento, deportes, cultura, etc.
- Versiones para otros navegadores: Firefox, Safari, Edge

## Notas y brainstorming

**Alternativas consideradas y descartadas:**
- *Grafos de propagación (GNN)*: técnicamente robusto (ver wiki/implementaciones/gnn-fakenews-safe-graph), pero requiere acceso a la API de Twitter/X (muy restrictiva y costosa en 2024-2026) y complejidad de implementación alta para el tiempo del PFI.
- *Solo análisis de texto (NLP puro)*: factible pero menos diferenciador frente a soluciones existentes.
- *LLM con RAG puro*: interesante pero caro en inference, difícil de evaluar con métricas estándar.

**Decisión de arquitectura**: híbrido de 3 módulos (NLP + credibilidad de fuente + contraste semántico) como balance entre rigor académico, factibilidad técnica y diferenciación de mercado.

## Referencias cruzadas

- [[wiki/00-resumen]]
- [[wiki/proyecto/cronograma]]
