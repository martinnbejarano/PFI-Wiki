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

Desarrollar un servicio de IA para facilitar la identificación de contenido desinformativo en redes sociales y medios digitales argentinos.

## Objetivos específicos

1. **Modelo de IA**: Entrenar un modelo de IA en español para clasificar desinformación.
2. **Credibilidad de fuente**: Evaluar credibilidad de fuente mediante análisis de metadatos.
3. **Contraste semántico**: Contrastar contenido contra fuentes confiables usando similitud semántica.
4. **Extensión web + dashboard**: Integrar los módulos en una extensión de Chrome con dashboard web.

## Alcance preliminar

El alcance comprende el desarrollo de un **prototipo funcional** de una aplicación web: una extensión de Google Chrome y un panel web, sin desarrollo de hardware ni versión mobile. Está orientada a ciudadanos argentinos que consumen noticias en redes sociales y medios digitales, con interfaz en español y uso exclusivo para Argentina. Los usuarios acceden instalando la extensión en Chrome desde una computadora de escritorio. El sistema analiza contenido textual publicado en Twitter/X, Instagram, Facebook, Infobae y Clarín, con foco en política y economía. Quedan excluidos otros idiomas, otras plataformas y contenido multimedia.

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
