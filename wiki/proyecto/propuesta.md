---
titulo: Propuesta de Tema
tipo: proyecto
tags: [propuesta, tema, etapa-1]
actualizado: 2026-08-11
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

Argentina atraviesa una crisis sostenida de credibilidad informativa. Según el Digital News Report 2024 (Newman et al., 2024), solo el 30% de la población confía en los medios, el nivel más bajo de América Latina, mientras que el interés en noticias cayó del 77% en 2017 al 45% en 2024. Este escenario se desarrolla sobre una infraestructura de consumo masivo: 31,3 millones de argentinos son usuarios activos de redes sociales (DataReportal, 2024), con WhatsApp como principal canal de difusión informativa, utilizado por el 93% de los usuarios de internet. En este contexto, la desinformación circula a escala y velocidad que hacen imposible su contención manual. A esto se suma un vector de crecimiento exponencial: el contenido generado por inteligencia artificial. Deepfakes de figuras políticas, imágenes sintéticas y videos manipulados se consolidaron como una de las formas más extendidas de desinformación, con presencia documentada en los ciclos electorales recientes.

Las soluciones existentes presentan limitaciones estructurales. Chequeado.com, referente local de verificación, opera de forma manual y solo puede cubrir un subconjunto acotado de afirmaciones. Las herramientas comerciales como Cyabra o Blackbird.AI están orientadas exclusivamente al segmento enterprise —gobiernos, redacciones y organismos— sin una capa ciudadana que genere datos en tiempo real sobre el ecosistema local de desinformación. El sistema propuesto cierra esta brecha: el acceso gratuito para el ciudadano no es solo un beneficio social, sino el mecanismo que produce el activo diferencial del negocio. La interacción de los usuarios genera, de forma agregada y anonimizada, un mapa continuo de qué desinformación circula, cuándo y en qué plataformas —información que medios, organizaciones de fact-checking y centros de investigación no pueden obtener de otra forma. Sobre esa base se construye el modelo de negocio: API y reportes de tendencias para clientes B2B, financiados por la adopción masiva del producto ciudadano.

El presente proyecto propone desarrollar un sistema de detección automática de desinformación en redes sociales, orientado a un segmento primario de personas de 18 a 40 años que siguen noticias de política y economía en Twitter/X —aunque la herramienta es usable por cualquier ciudadano sin conocimiento técnico— y a un segmento secundario de periodistas y editores que necesitan evaluar la confiabilidad de fuentes. Por razones operativas, el sistema no infiere la intención del emisor: clasifica contenido potencialmente falso, engañoso o no verificable, y usa "desinformación" como término paraguas. La solución integra cuatro módulos: un clasificador de lenguaje natural entrenado sobre modelos transformer —con XLM-T como modelo principal, por combinar la adaptación al texto de Twitter/X con la transferencia desde conjuntos de datos en inglés, y RoBERTuito y BETO como líneas de comparación—, un módulo de evaluación de credibilidad de fuente basado en metadatos, un módulo de contraste semántico que triangula fuentes periodísticas de referencia, bases de datos oficiales y verificadores como Chequeado, y un módulo ensemble que sintetiza los tres scores anteriores. El sistema se entrega como extensión de Google Chrome con panel web, analiza contenido textual publicado en Twitter/X —única plataforma de detección—, y devuelve un score de probabilidad acompañado de evidencia que justifica la clasificación (links a fuentes de referencia que corroboran o contradicen). Aunque WhatsApp concentra buena parte de la circulación en el país, Twitter/X es el espacio público donde muchas narrativas se originan y amplifican antes de migrar a canales cerrados, lo que lo vuelve un buen primer objetivo de detección. Las fuentes periodísticas de referencia (Infobae, Clarín, La Nación), junto con fuentes oficiales y verificadores, se usan como evidencia para la verificación mediante triangulación —no como objetivos de detección ni como única "verdad".

Respecto de las soluciones existentes, el sistema se diferencia por su foco en el contexto local, su accesibilidad gratuita para el ciudadano común y su capacidad de brindar evidencia explicable en lugar de una clasificación binaria. Como limitación conocida, el modelo puede generar falsos positivos ante contenido satírico o irónico; este riesgo se mitiga presentando el resultado como probabilidad y no como veredicto definitivo.

Dentro del alcance del PFI se incluye el prototipo funcional de los cuatro módulos y la extensión Chrome. Quedan para versiones futuras el soporte a contenido multimedia —incluyendo imágenes generadas por IA y deepfakes—, la integración con WhatsApp y Telegram, y la detección de campañas coordinadas mediante análisis de grafos de propagación.

## Propuesta de valor

El sistema se diferencia de las soluciones existentes en cuatro dimensiones:

1. **Contexto local**: foco específico en Argentina (política, economía, sociedad), con un modelo entrenado en español rioplatense y fuentes de referencia locales (Chequeado.com, medios argentinos verificados, cuentas oficiales).
2. **Capa ciudadana como ventaja competitiva**: herramienta gratuita para el ciudadano — a diferencia de Cyabra, Blackbird.AI o Newtral FactFlow (exclusivamente enterprise). La adopción ciudadana genera datos anonimizados sobre tendencias de desinformación local, que son el activo diferencial vendible a clientes B2B.
3. **Análisis híbrido de 3 señales**: combina (a) clasificación lingüística del texto, (b) evaluación de credibilidad de la fuente, y (c) contraste semántico con fuentes confiables —que el módulo ensemble sintetiza en la decisión final— más robusto que el análisis de texto solo, sin la complejidad de grafos de propagación.
4. **Evidencia explicable**: no devuelve solo un score binario, sino links a fuentes que corroboran o contradicen el contenido, permitiendo al usuario entender por qué una publicación fue marcada como sospechosa.

## Modelo de negocio

Modelo **freemium con monetización B2B**. La extensión es gratuita para el ciudadano, y su uso masivo genera el activo central del negocio: un mapa en tiempo real de qué desinformación circula en Argentina, dónde y con qué intensidad. Ese mapa se vende a clientes B2B.

**Qué se vende:**
- **API de detección** — endpoint para clasificar texto (score + evidencia). Pricing por volumen.
- **Reportes / dashboards de tendencias** — qué temas falsos circulan, en qué plataformas, con qué intensidad. Suscripción mensual.

**Segmentos B2B:**
- Medios de comunicación — necesitan saber qué desinformación priorizar editorialmente.
- Organizaciones de fact-checking (Chequeado) — priorizan qué verificar primero según impacto real.
- Centros de investigación / universidades — acceso a dataset histórico para papers y observatorios.
- Organismos públicos / ONGs — monitoreo electoral en ciclos críticos (2025, 2027).
- Marcas y agencias corporativas — alertas tempranas sobre fake news que afectan a la marca.

**Por qué nuestra data es mejor:** los competidores enterprise (Cyabra, Blackbird.AI) obtienen datos por scraping de APIs — caro, limitado a las plataformas que tienen API, ciego a WhatsApp. Nuestra extensión vive en el navegador del usuario y registra **lo que se consume realmente**, no solo lo que se publica. En Argentina, donde WhatsApp tiene 93% de penetración y es el principal vector de difusión, esta diferencia es estructural.

**Bucle de red de datos:** más usuarios → más posts analizados → mapa más completo → producto B2B más valioso → más revenue → mejor producto ciudadano → más usuarios. Este efecto vuelve al negocio defendible: el primer competidor con adopción ciudadana masiva acumula una ventaja de datos cada vez más difícil de igualar.

> Detalle completo, BMC, FODA, pricing y análisis de riesgos en [[wiki/negocio/modelo-de-negocio]].

## 1. Objetivo general

Desarrollar un servicio de IA para facilitar la identificación de contenido desinformativo en redes sociales.

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
- Primario (segmento de validación): personas de 18 a 40 años que siguen noticias de política y economía en Twitter/X. La herramienta es usable por cualquier ciudadano sin conocimiento técnico, pero el user research se acota a este segmento.
- Secundario: Periodistas y editores que necesitan evaluar confiabilidad de fuentes antes de publicar

**Plataforma de detección (contenido analizado):**
- Twitter/X (posts públicos) — única red social objetivo del prototipo

**Fuentes de evidencia para la verificación (no de detección):**
- Fuentes periodísticas de referencia (Infobae.com, Clarín.com, La Nación, Página/12, Télam), fuentes oficiales argentinas y verificaciones profesionales previas — se usan para contrastar las afirmaciones analizadas mediante triangulación; no son objetivos de detección ni se tratan como única "verdad". Los medios se consultan mediante búsqueda web; las fuentes oficiales, sobre un índice propio que mantiene un proceso de ingesta periódico (RF-28); y las verificaciones previas, sobre lo ya indexado, sin acceso directo al sitio de ningún verificador. El detalle y su justificación están en [[wiki/proyecto/restricciones-legales-eticas]].

**Funcionalidades abarcadas:**
- Análisis de contenido textual publicado en Twitter/X
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
- Modelo NLP: Transformer fine-tuneado para español (XLM-T principal; RoBERTuito y BETO como comparación)
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
- Otras redes sociales además de Twitter/X (Instagram, Facebook)
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
2. **Nuevas plataformas**: Instagram, Facebook, WhatsApp y Telegram (otras redes sociales y mensajería privada — esta última, principal vector de desinformación en Argentina)
3. **Detección de campañas coordinadas**: análisis de grafos de propagación para identificar bots y redes coordinadas

## Segmento target

**Primario — segmento de validación (18 a 40 años):**
- Personas de **18 a 40 años** que siguen noticias de política y economía en Twitter/X. La herramienta es usable por cualquier ciudadano sin conocimiento técnico, pero el user research se acota a este segmento.
- Perfil: usuario de Twitter/X que se expone a desinformación sin herramientas para detectarla
- No requiere conocimiento técnico — la extensión funciona de fondo mientras navega

**Secundario — periodista / editor:**
- Uso como herramienta de screening: evaluar si una fuente o contenido es confiable antes de citarlo o publicarlo
- Acelera el proceso de verificación sin reemplazar el juicio editorial

## Limitaciones conocidas del sistema

- **Falsos positivos**: el modelo puede marcar contenido satírico, irónico o hiperbólico como sospechoso. Mitigación: score de probabilidad + evidencia explicable (el usuario puede evaluar el contexto).
- **Dependencia del dataset**: como no existe un corpus público de desinformación en español argentino, la calidad del clasificador depende de la factibilidad de construir o adaptar uno con etiquetado confiable (tarea costosa y sensible a sesgos de anotación) — se aborda con web search en fuentes de referencia + bases de datos oficiales (a determinar) y técnicas de data augmentation.
- **Sesgo de las fuentes de evidencia**: el ecosistema mediático argentino está polarizado; apoyarse en pocos medios podría sesgar la verificación. Mitigación: triangulación entre fuentes periodísticas de referencia, fuentes oficiales y verificadores independientes.
- **Latencia**: la recuperación de evidencia en tiempo real (web search) puede afectar la experiencia de uso; obliga a optimizar la búsqueda.
- **Privacidad**: el tratamiento de datos de uso plantea desafíos de privacidad y cumplimiento (LPDP); se aborda con agregación, anonimización y minimización de datos personales.

## Notas y brainstorming

**Alternativas consideradas y descartadas:**
- *Grafos de propagación (GNN)*: técnicamente robusto (ver wiki/implementaciones/gnn-fakenews-safe-graph), pero requiere acceso a la API de Twitter/X (muy restrictiva y costosa en 2024-2026) y complejidad de implementación alta para el tiempo del PFI.
- *Solo análisis de texto (NLP puro)*: factible pero menos diferenciador frente a soluciones existentes.
- *LLM con RAG puro*: interesante pero caro en inference, difícil de evaluar con métricas estándar.

**Decisión de arquitectura**: arquitectura de 4 módulos (NLP + credibilidad de fuente + contraste semántico + ensemble combinator) como balance entre rigor académico, factibilidad técnica y diferenciación de mercado.

## Referencias cruzadas

- [[wiki/00-resumen]]
- [[wiki/proyecto/cronograma]]
