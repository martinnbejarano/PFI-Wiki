---
titulo: Propuesta de Tema
tipo: proyecto
tags: [propuesta, tema, etapa-1]
actualizado: 2026-04-19
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

Argentina atraviesa una crisis sostenida de credibilidad informativa. Según el Digital News Report 2024 (Newman et al., 2024), solo el 30% de la población confía en los medios, el nivel más bajo de América Latina, mientras que el interés en noticias cayó del 77% en 2017 al 45% en 2024. Este escenario se desarrolla sobre una infraestructura de consumo masivo: 31,3 millones de argentinos son usuarios activos de redes sociales, con WhatsApp como principal canal de difusión informativa, utilizado por el 93% de los usuarios de internet. En este contexto, la desinformación circula a escala y velocidad que hacen imposible su contención manual. A esto se suma un vector de crecimiento exponencial: el contenido generado por inteligencia artificial. Deepfakes de figuras políticas, imágenes sintéticas y videos manipulados se consolidaron como una de las formas más extendidas de desinformación, con presencia documentada en los ciclos electorales recientes.

Las soluciones existentes presentan limitaciones estructurales. Chequeado.com, referente local de verificación, opera de forma manual y solo puede cubrir un subconjunto acotado de afirmaciones. Las herramientas comerciales como Cyabra o Blackbird.AI están orientadas exclusivamente al segmento enterprise —gobiernos, redacciones y organismos— sin una capa ciudadana que genere datos en tiempo real sobre el ecosistema local de desinformación. El sistema propuesto cierra esta brecha: el acceso gratuito para el ciudadano no es solo un beneficio social, sino el mecanismo que produce el activo diferencial del negocio. La interacción de los usuarios genera, de forma agregada y anonimizada, un mapa continuo de qué desinformación circula, cuándo y en qué plataformas —información que medios, organizaciones de fact-checking y centros de investigación no pueden obtener de otra forma. Sobre esa base se construye el modelo de negocio: API y reportes de tendencias para clientes B2B, financiados por la adopción masiva del producto ciudadano.

El presente proyecto propone desarrollar un sistema de detección automática de desinformación en redes sociales, orientado a ciudadanos argentinos de entre 16 y 80 años que consumen noticias en plataformas digitales, y a periodistas y editores que necesitan evaluar la confiabilidad de fuentes. La solución integra cuatro módulos: un clasificador de lenguaje natural entrenado en español sobre modelos transformer (BETO o XLM-RoBERTa), un módulo de evaluación de credibilidad de fuente basado en metadatos, un módulo de contraste semántico contra múltiples fuentes (web search en medios confiables + bases de datos oficiales), y un módulo ensemble que sintetiza los tres scores anteriores. El sistema se entrega como extensión de Google Chrome con panel web, analiza contenido textual en Twitter/X, Instagram, Facebook, Infobae y Clarín, y devuelve un score de probabilidad acompañado de evidencia que justifica la clasificación (links a fuentes que corroboran o contradicen).

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

## 1. Objetivo general

Desarrollar un servicio de IA para facilitar la identificación de contenido desinformativo en redes sociales y medios digitales argentinos.

## 2. Objetivos específicos

1. **Modelo de IA**: Entrenar un modelo de IA en español para clasificar desinformación.
2. **Credibilidad de fuente**: Evaluar credibilidad de fuente mediante análisis de metadatos.
3. **Contraste semántico**: Contrastar contenido contra fuentes confiables usando similitud semántica.
4. **Extensión web + dashboard**: Integrar los módulos en una extensión de Chrome con dashboard web.

## 3. Alcance

El alcance del PFI comprende el desarrollo de un **prototipo funcional** de un sistema de detección automática de desinformación, entregado como una extensión de navegador web y un panel de dashboard.

**Forma de entrega y acceso:**
- Extensión de Google Chrome instalable desde repositorio local o store
- Panel web complementario para visualización de análisis históricos y reportes
- Sin desarrollo de aplicaciones móviles nativas (iOS/Android)
- Sin desarrollo de hardware
- Compatible únicamente con el navegador Google Chrome en computadoras de escritorio
- Sistema operativo: Windows, macOS, Linux (cualquier SO que soporte Chrome)

**Usuarios objetivo:**
- Primario: Ciudadanos argentinos de 16 a 80+ años que consumen noticias en redes sociales y medios digitales
- Secundario: Periodistas y editores que necesitan evaluar confiabilidad de fuentes antes de publicar

**Plataformas y canales de contenido analizados:**
- Twitter/X (posts públicos)
- Instagram (posts públicos, captions)
- Facebook (posts públicos)
- Infobae.com (artículos)
- Clarín.com (artículos)

**Funcionalidades abarcadas:**
- Análisis de contenido textual publicado en las plataformas listadas
- Clasificación automática mediante modelo de NLP entrenado en español
- Evaluación de credibilidad de fuente basada en metadatos
- Contraste semántico del contenido contra fuentes confiables (web search + bases de datos oficiales)
- Score de probabilidad (0-1) acompañado de evidencia (links a fuentes que corroboran/contradicen)
- Panel web para consulta de análisis históricos

**Temática y contexto:**
- Foco exclusivo en Argentina: política, economía y sociedad
- Interfaz en español rioplatense
- Uso exclusivo para contexto argentino (no internacionalización)
- Datos públicos únicamente; sin acceso a mensajes privados, datos de cuenta o información protegida

**Tecnologías contempladas:**
- Backend: Python + Flask/FastAPI para API de análisis
- Modelo NLP: Transformers (BETO o XLM-RoBERTa) fine-tuneado en español
- Extensión: JavaScript + Chrome Extension APIs
- Datos de entrenamiento: LIAR dataset + FakeNewsNet + validación con posts reales argentinos
- Métricas: Accuracy, Precision, Recall, F1-score

**Entregas MVP (Minimum Viable Product):**
- Prototipo de extensión Chrome funcional (análisis en tiempo real de posts)
- Modelo de IA entrenado y evaluado en datos en español
- Panel web con histórico de análisis
- Documentación técnica y manual de usuario
- Código fuente en repositorio

**Excluyentes explícitos (fuera del alcance MVP):**
- Análisis de contenido multimedia (imágenes, videos, audios)
- Detección de deepfakes o manipulación de imágenes
- Detección de campañas coordinadas o grafos de propagación
- Integración con WhatsApp, Telegram u otras plataformas de mensajería
- Otros idiomas además del español
- Versiones para navegadores Firefox, Safari, Edge, etc.
- Aplicaciones móviles nativas
- Comercialización de la extensión (prototipo académico)
- Almacenamiento de datos personales de usuarios
- Procesamiento en streaming a escala masiva

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
- **Dependencia del dataset**: la calidad del clasificador está acotada por la disponibilidad de datos en español argentino — se aborda mediante web search en medios confiables + bases de datos de fuentes oficiales (a determinar) y técnicas de data augmentation.

## Notas y brainstorming

**Alternativas consideradas y descartadas:**
- *Grafos de propagación (GNN)*: técnicamente robusto (ver wiki/implementaciones/gnn-fakenews-safe-graph), pero requiere acceso a la API de Twitter/X (muy restrictiva y costosa en 2024-2026) y complejidad de implementación alta para el tiempo del PFI.
- *Solo análisis de texto (NLP puro)*: factible pero menos diferenciador frente a soluciones existentes.
- *LLM con RAG puro*: interesante pero caro en inference, difícil de evaluar con métricas estándar.

**Decisión de arquitectura**: arquitectura de 4 módulos (NLP + credibilidad de fuente + contraste semántico + ensemble combinator) como balance entre rigor académico, factibilidad técnica y diferenciación de mercado.

## Referencias cruzadas

- [[wiki/00-resumen]]
- [[wiki/proyecto/cronograma]]
