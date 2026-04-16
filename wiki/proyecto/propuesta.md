---
titulo: Propuesta de Tema
tipo: proyecto
tags: [propuesta, tema, etapa-1]
actualizado: 2026-04-16
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

## Descripción

Argentina atraviesa una crisis sostenida de credibilidad informativa. Según el **Digital News Report 2024 del Reuters Institute** —relevado para el país por La Nación—, solo el 30% de la población confía en los medios, el nivel más bajo de América Latina, mientras que el interés en noticias cayó del 77% en 2017 al 45% en 2024. Este escenario se desarrolla sobre una infraestructura de consumo masivo: 31,3 millones de argentinos son usuarios activos de redes sociales, con WhatsApp como principal canal de difusión informativa, utilizado por el 93% de los usuarios de internet. En este contexto, la desinformación circula a escala y velocidad que hacen imposible su contención manual. A esto se suma un vector de crecimiento exponencial: el contenido generado por inteligencia artificial. Deepfakes de figuras políticas, imágenes sintéticas y videos manipulados se consolidaron como una de las formas más extendidas de desinformación, con presencia documentada en los ciclos electorales recientes.

Las soluciones existentes presentan limitaciones estructurales. Chequeado.com, referente local de verificación, opera de forma manual y solo puede cubrir un subconjunto acotado de afirmaciones. Las herramientas comerciales como Cyabra o Blackbird.AI están orientadas exclusivamente al segmento enterprise —gobiernos, redacciones y organismos— sin una capa ciudadana que genere datos en tiempo real sobre el ecosistema local de desinformación. El sistema propuesto cierra esta brecha: el acceso gratuito para el ciudadano no es solo un beneficio social, sino el mecanismo que produce el activo diferencial del negocio. La interacción de los usuarios genera, de forma agregada y anonimizada, un mapa continuo de qué desinformación circula, cuándo y en qué plataformas —información que medios, organizaciones de fact-checking y centros de investigación no pueden obtener de otra forma. Sobre esa base se construye el modelo de negocio: API y reportes de tendencias para clientes B2B, financiados por la adopción masiva del producto ciudadano.

El presente proyecto propone desarrollar un sistema de detección automática de desinformación en redes sociales, orientado a ciudadanos argentinos de entre 16 y 80 años que consumen noticias en plataformas digitales, y a periodistas y editores que necesitan evaluar la confiabilidad de fuentes. La solución integra tres módulos: un clasificador de lenguaje natural entrenado en español sobre modelos transformer (BETO o XLM-RoBERTa), un módulo de evaluación de credibilidad de fuente basado en metadatos, y un módulo de contraste semántico contra un corpus de fuentes confiables (Chequeado.com). El sistema se entrega como extensión de Google Chrome con panel web, analiza contenido textual en Twitter/X, Instagram, Facebook, Infobae y Clarín, y devuelve un score de probabilidad acompañado de evidencia que justifica la clasificación.

Respecto de las soluciones existentes, el sistema se diferencia por su foco en el contexto local, su accesibilidad gratuita para el ciudadano común y su capacidad de brindar evidencia explicable en lugar de una clasificación binaria. Como limitación conocida, el modelo puede generar falsos positivos ante contenido satírico o irónico; este riesgo se mitiga presentando el resultado como probabilidad y no como veredicto definitivo.

Dentro del alcance del PFI se incluye el prototipo funcional de los tres módulos y la extensión Chrome. Quedan para versiones futuras el soporte a contenido multimedia —incluyendo imágenes generadas por IA y deepfakes—, la integración con WhatsApp y Telegram, y la detección de campañas coordinadas mediante análisis de grafos de propagación.

## Propuesta de valor

El sistema se diferencia de las soluciones existentes en cuatro dimensiones:

1. **Contexto local**: foco específico en Argentina (política, economía, sociedad), con un modelo entrenado en español rioplatense y fuentes de referencia locales (Chequeado.com, medios argentinos verificados, cuentas oficiales).
2. **Capa ciudadana como ventaja competitiva**: herramienta gratuita para el ciudadano — a diferencia de Cyabra, Blackbird.AI o Newtral FactFlow (exclusivamente enterprise). La adopción ciudadana genera datos anonimizados sobre tendencias de desinformación local, que son el activo diferencial vendible a clientes B2B.
3. **Análisis híbrido de 3 señales**: combina (a) clasificación lingüística del texto, (b) evaluación de credibilidad de la fuente, y (c) contraste semántico con fuentes confiables — más robusto que el análisis de texto solo, sin la complejidad de grafos de propagación.
4. **Evidencia explicable**: no devuelve solo un score binario, sino links a fuentes que corroboran o contradicen el contenido, permitiendo al usuario entender por qué una publicación fue marcada como sospechosa.

## Modelo de negocio

- **Ciudadanos**: extensión Chrome gratuita — generan el dataset de tendencias via uso
- **Clientes B2B (revenue)**: medios de comunicación, organizaciones de fact-checking, centros de investigación — pagan por API y reportes de tendencias de desinformación local
- **Lógica**: la adopción masiva ciudadana financia el servicio profesional. Sin usuarios reales no hay datos; sin datos no hay producto B2B.

## Objetivo general

Desarrollar un servicio de IA para facilitar la identificación de contenido desinformativo en redes sociales y medios digitales argentinos.

## Objetivos específicos

1. **Modelo de IA**: Entrenar un modelo de IA en español para clasificar desinformación.
2. **Credibilidad de fuente**: Evaluar credibilidad de fuente mediante análisis de metadatos.
3. **Contraste semántico**: Contrastar contenido contra fuentes confiables usando similitud semántica.
4. **Extensión web + dashboard**: Integrar los módulos en una extensión de Chrome con dashboard web.

## Alcance preliminar

El alcance comprende el desarrollo de un **prototipo funcional** de una aplicación web: una extensión de Google Chrome y un panel web, sin desarrollo de hardware ni versión mobile. Está orientada a ciudadanos argentinos que consumen noticias en redes sociales y medios digitales, con interfaz en español y uso exclusivo para Argentina. Los usuarios acceden instalando la extensión en Chrome desde una computadora de escritorio. El sistema analiza contenido textual publicado en Twitter/X, Instagram, Facebook, Infobae y Clarín, con foco en política y economía. Quedan excluidos otros idiomas, otras plataformas y contenido multimedia.

## Fuera del alcance (MVP)

- Aplicaciones móviles nativas (iOS / Android)
- Análisis de contenido multimedia: videos, audios, imágenes — solo texto
- Análisis de grafos de propagación o detección de campañas coordinadas de bots
- Otros idiomas además del español
- Plataformas no listadas: YouTube, TikTok, WhatsApp, Telegram, LinkedIn, etc.
- Desarrollo de una plataforma propia de fact-checking
- Procesamiento en streaming a gran escala
- Temáticas no listadas: entretenimiento, deportes, cultura, etc.
- Versiones para otros navegadores: Firefox, Safari, Edge

## Futuros releases (post-PFI)

1. **Soporte multimedia**: detección de imágenes falsas y deepfakes (video + audio)
2. **Nuevas plataformas**: WhatsApp y Telegram (mensajería privada — principal vector de desinformación en Argentina)
3. **Detección de campañas coordinadas**: análisis de grafos de propagación para identificar bots y redes coordinadas

## Segmento target

**Primario — ciudadano común argentino:**
- Rango etario: **16 a 80+ años** — cualquier persona que consume noticias digitales o redes sociales
- Perfil: usuario de Twitter/X, Instagram, Facebook, Infobae, Clarín que se expone a desinformación sin herramientas para detectarla
- No requiere conocimiento técnico — la extensión funciona de fondo mientras navega

**Secundario — periodista / editor:**
- Uso como herramienta de screening: evaluar si una fuente o contenido es confiable antes de citarlo o publicarlo
- Acelera el proceso de verificación sin reemplazar el juicio editorial

## Limitaciones conocidas del sistema

- **Falsos positivos**: el modelo puede marcar contenido satírico, irónico o hiperbólico como sospechoso. Mitigación: score de probabilidad + evidencia explicable (el usuario puede evaluar el contexto).
- **Dependencia del dataset**: la calidad del clasificador está acotada por la disponibilidad de datos en español argentino — se aborda usando Chequeado.com como fuente primaria y técnicas de data augmentation.

## Notas y brainstorming

**Alternativas consideradas y descartadas:**
- *Grafos de propagación (GNN)*: técnicamente robusto (ver wiki/implementaciones/gnn-fakenews-safe-graph), pero requiere acceso a la API de Twitter/X (muy restrictiva y costosa en 2024-2026) y complejidad de implementación alta para el tiempo del PFI.
- *Solo análisis de texto (NLP puro)*: factible pero menos diferenciador frente a soluciones existentes.
- *LLM con RAG puro*: interesante pero caro en inference, difícil de evaluar con métricas estándar.

**Decisión de arquitectura**: híbrido de 3 módulos (NLP + credibilidad de fuente + contraste semántico) como balance entre rigor académico, factibilidad técnica y diferenciación de mercado.

## Referencias cruzadas

- [[wiki/00-resumen]]
- [[wiki/proyecto/cronograma]]
