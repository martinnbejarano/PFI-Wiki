---
titulo: Análisis Competitivo
tipo: análisis
tags: [competencia, mercado, diferenciacion, oceano-azul]
actualizado: 2026-09-27
---

# Análisis Competitivo

## Soluciones existentes

| Competidor                                                       | Tipo                    | Descripción                                                                                                      | Fortalezas                                                                                                   | Debilidades                                                                         |
| ---------------------------------------------------------------- | ----------------------- | ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------- |
| [[wiki/implementaciones/information-tracer\|Information Tracer]] | SaaS comercial          | Detección de manipulación coordinada y bots en X, Facebook, Instagram, Reddit, YouTube, Bluesky, LinkedIn        | Multi-plataforma, visualización de narrativas, partnerships académicos (CMU, Tsinghua)                       | Cerrado, sin soporte para español/LATAM declarado, no verifica hechos individuales  |
| [[wiki/implementaciones/newtral-factflow\|Newtral FactFlow]]     | Profesional / cerrado   | Fact-checking automático en Telegram con LLM (Qwen), entrenado en 1M+ mensajes en español                        | 70% contenido en español, 10M registros procesados, reduce a segundos el monitoreo                           | Solo Telegram, solo para fact-checkers profesionales, código cerrado                |
| Cyabra                                                           | SaaS comercial          | Detección en tiempo real de perfiles falsos, deepfakes y narrativas dañinas en redes sociales                    | Multi-plataforma, alertas en tiempo real, IA para detección de bots, contratos con gobiernos y corporaciones | Orientado a grandes clientes (gobiernos, corporaciones), precio no público, cerrado |
| Blackbird.AI                                                     | SaaS comercial          | Plataforma de "Narrative Intelligence" — detecta y mide riesgo narrativo en +25 idiomas (texto, imágenes, memes) | 25+ idiomas, cubre dark web + social + noticias, análisis de deepfakes y memes                               | Precio enterprise no público, orientado a grandes organizaciones, cerrado           |
| Botometer                                                        | Académico (gratuito)    | Clasifica cuentas de Twitter como bot o humano mediante machine learning                                         | Gratuito, API pública, bien documentado, publicado por OSoMe (Indiana University)                            | Solo Twitter/X, detecta bots no desinformación en sí, depende de la API de X        |

## Tabla comparativa de variables

| Variable | Nuestra solución | Cyabra | Blackbird.AI | Newtral FactFlow | Chequeado.com |
|---|---|---|---|---|---|
| **Modelo de acceso** | Gratuito (ciudadano) + B2B | Enterprise solo | Enterprise solo | Enterprise solo | Gratuito (manual) |
| **Plataformas soportadas** | Twitter/X (detección); medios de confianza como evidencia | +25 plataformas | +25 plataformas (dark web, imágenes) | Solo Telegram | Web (manual) |
| **Idiomas** | Español rioplatense (modelo multilingüe, dominio acotado) | Multiidioma | 25+ idiomas | Español | Español (Argentina) |
| **Tipo de contenido** | Texto solo (MVP) | Texto, metadatos, bots | Texto, imágenes, memes, deepfakes | Texto (LLM) | Texto (manual) |
| **Velocidad detección** | Segundos (API REST) | Real-time | Real-time | Segundos (Telegram) | Manual (horas/días) |
| **Automatización** | 100% automática (ML/DL) | 100% automática (IA) | 100% automática (IA) | 100% automática (LLM) | 0% (fact-checkers humanos) |
| **Escalabilidad** | Altamente escalable | Escalable (enterprise) | Escalable (enterprise) | Escalable (Telegram) | No escalable |
| **Precio público** | $0 ciudadano | No disponible | No disponible | No disponible | $0 (manual) |
| **Contexto local Argentina** | ✅ Específico | ❌ Genérico | ❌ Genérico | ❌ Genérico | ✅ Nativo |
| **Evidencia explicable** | ✅ Links a fuentes | ❌ Score solo | ❌ Score solo | ✅ Contexto LLM | ✅ Verificación completa |
| **Dataset entrenamiento** | XLM-T adaptado sobre LIAR y FakeNewsNet, más corpus argentino propio | Proprietario | Proprietario | 1M+ mensajes español | Manual (verificadores) |

## Océano Azul — Espacio diferencial

**Nicho no ocupado:** La intersección de tres características no existe en competencia:

1. **Gratuito para ciudadano** (todos los competidores comerciales son enterprise; Chequeado.com es manual)
2. **Automático y escalable** (Chequeado.com es manual; commercial solutions no tienen capa ciudadana)
3. **Contexto local Argentina** (competidores comerciales son genéricos; Chequeado es manual)

**La ventaja competitiva no es la técnica** (BERT/Transformers es commodity en 2026), **es el modelo de negocio**: la capa ciudadana genera datos reales de tendencias de desinformación local que se monetizan como API + reportes B2B.

## Matriz ERIC

| | Eliminar | Reducir | Incrementar | Crear |
|---|---|---|---|---|
| **Análisis de propagación / Grafos (GNN)** | Sí (complejidad sin ROI para MVP) | — | — | — |
| **Multimodalidad (imágenes, video, audio)** | — | Sí (MVP = texto; futuros releases) | — | — |
| **Fact-checking manual** | — | Sí (automatización > verificación manual) | — | — |
| **Múltiples idiomas** | — | Sí (el modelo es multilingüe; el dominio de datos y de evidencia se acota al español rioplatense) | — | — |
| **Detección de cuentas automatizadas** | Sí (el objeto de análisis es el contenido, no la naturaleza de la cuenta) | — | — | — |
| **Automatización** | — | — | Sí (100% automática) | — |
| **Velocidad** | — | — | Sí (segundos, no horas) | — |
| **Accesibilidad ciudadana** | — | — | Sí (gratuito, no enterprise) | — |
| **Datos de tendencias locales** | — | — | — | Sí (activo diferencial B2B) |
| **Evidencia explicable** | — | — | Sí (links a fuentes, no blackbox) | — |

## Diccionario de variables

Las diez variables de la matriz ERIC, con su definición operativa. La definición empieza siempre con el verbo de la acción, para que se lea qué se hace con cada una y no solo qué es.

**Eliminar**
- *Análisis de propagación mediante grafos*: eliminar el modelado de la red de difusión (quién retuiteó a quién, en qué orden), que exige datos de la API de X y agrega complejidad sin retorno proporcional en un prototipo.
- *Detección de cuentas automatizadas*: eliminar el juicio sobre si la cuenta es humana o automatizada. El objeto de análisis es el contenido, no la naturaleza del emisor.

**Reducir**
- *Multimodalidad*: acotar el análisis al texto, dejando fuera imagen, video y audio, que se difieren a versiones posteriores.
- *Verificación manual*: reducir a cero la intervención humana en el veredicto. La automatización es el objeto del trabajo.
- *Cobertura multilingüe*: acotar el dominio de datos y de evidencia al español rioplatense, aunque el modelo subyacente sea multilingüe.

**Incrementar**
- *Automatización del proceso*: llevar a la totalidad del recorrido, desde la lectura de la publicación hasta el veredicto, sin intervención humana.
- *Velocidad de respuesta*: reducir el tiempo hasta el veredicto de días a segundos, que es la diferencia entre advertir antes o después de que el contenido circuló.
- *Accesibilidad para el ciudadano*: ampliar el acceso a cualquier persona con un navegador, sin registro, sin costo y sin conocimiento técnico previo.
- *Evidencia verificable*: aumentar lo que el usuario puede comprobar por su cuenta, entregando los enlaces a las fuentes y el desglose de los puntajes parciales en lugar de un número sin justificación.

**Crear**
- *Información sobre circulación local*: crear un registro de qué desinformación circula en Argentina, en qué volumen y sobre qué temas, que hoy no produce ningún actor y que constituye el activo comercial del proyecto.

## Curva de valor

### Regla de conversión

Las variables se puntúan de 0 a 5 con esta escala, para que la asignación sea auditable y no impresionista:

| Valor | Significado |
|---|---|
| 0 | Ausente |
| 1 | Marginal o incidental |
| 2 | Presente con limitaciones importantes |
| 3 | Presente |
| 4 | Fortaleza declarada del producto |
| 5 | Capacidad central del producto |

La puntuación surge de la documentación pública de cada competidor, resumida en la tabla comparativa de arriba. En las cinco variables de *Eliminar* y *Reducir*, **un valor más bajo es mejor para la propuesta**: son exactamente las capacidades que se decidió no construir.

### Matriz de puntuación

| Variable | Acción | Propia | Information Tracer | Newtral FactFlow | Cyabra | Blackbird.AI | Chequeado |
|---|---|---|---|---|---|---|---|
| Análisis de propagación | E | 0 | 5 | 0 | 4 | 4 | 0 |
| Detección de cuentas automatizadas | E | 1 | 4 | 0 | 5 | 3 | 0 |
| Multimodalidad | R | 0 | 2 | 1 | 4 | 5 | 3 |
| Verificación manual | R | 0 | 0 | 1 | 0 | 0 | 5 |
| Cobertura multilingüe | R | 1 | 3 | 2 | 4 | 5 | 1 |
| Automatización del proceso | I | 5 | 5 | 4 | 5 | 5 | 0 |
| Velocidad de respuesta | I | 5 | 4 | 4 | 5 | 5 | 0 |
| Accesibilidad para el ciudadano | I | 5 | 1 | 0 | 0 | 0 | 4 |
| Evidencia verificable | I | 5 | 2 | 4 | 1 | 1 | 5 |
| Información sobre circulación local | C | 5 | 1 | 1 | 1 | 1 | 2 |

### Lectura

La propuesta **no puntúa alto en todo**, y eso es lo que hace legible la curva. Queda en 0 o 1 en las cinco primeras variables, que son justamente las que decidió no construir, y Chequeado la iguala en evidencia verificable y queda cerca en accesibilidad.

El despegue ocurre en un solo punto: **accesibilidad para el ciudadano combinada con automatización y velocidad**. Los cuatro competidores automáticos puntúan 0 o 1 en accesibilidad; el único accesible, Chequeado, puntúa 0 en automatización y velocidad. Ningún actor reúne las tres, y esa intersección vacía es el espacio que ocupa la propuesta.

La variable creada, información sobre circulación local, es la única donde la distancia es de cuatro puntos contra el competidor más cercano. No es casual que sea también la que sostiene el modelo de negocio.

## Ventajas vs competencia

| Competidor | Nuestras ventajas | Sus ventajas | Gap |
|---|---|---|---|
| **Cyabra** | Gratuito, local, escalable | Multi-plataforma, bots, real-time | Cobertura multimedia (futuros releases) |
| **Blackbird.AI** | Gratuito, local, español AR | 25 idiomas, deepfakes, dark web | Deepfakes (futuros releases) |
| **Newtral FactFlow** | Gratuito, 70% español, multi-plataforma | LLM (RAG), contexto verificado | Cobertura Argentina específica |
| **Chequeado.com** | Automático, escalable, velocidad | Verificación manual confiable, histórico | Manual = no escala; sin capa ciudadana |

## Síntesis del análisis competitivo

**Por qué hay espacio en el mercado:**

1. **Vacío de oferta**: no existe producto automático gratuito para ciudadano argentino. Competencia commercial = enterprise; Chequeado = manual.

2. **Modelo de negocio único**: la capa ciudadana no es filantropía, es el mecanismo de generación de datos diferencial. Los datos de tendencias reales de desinformación local son vendibles a medios, fact-checkers y centros de investigación como API + reportes.

3. **Contexto local sin perder escala**: enfoque específico en Argentina (español rioplatense, fuentes locales, ciclos electorales) que los competidores genéricos no ofrecen, pero sin renunciar a escalabilidad técnica.

4. **Alineación con regulación emergente**: medidas de desinformación y "fake news" están en agenda legislativa global. Producto alineado con demanda futura de gobiernos y medios por inteligencia local en desinformación.

## Diferencial frente a «esto ya existe»

Responde al punto 1 del feedback de la exposición del 50 % ([[wiki/presentacion/e50/analisis-feedback]]): el evaluador dijo que hay herramientas parecidas desde hace unos cuatro años y nombró dos. El diferencial se apoya en dos ejes:

- **(a) Camino a la evidencia**: el ciudadano recibe las fuentes enlazadas al documento original, no solo el veredicto. El objetivo no es que el usuario le crea al veredicto, es que pueda prescindir de él.
- **(b) Capa ciudadana → datos B2B**: el uso gratuito genera datos agregados y anonimizados de qué desinformación circula en Argentina, que se venden a medios, verificadores e investigadores.

### Las dos herramientas que nombró el evaluador

**La herramienta de verificación en vivo de políticos.** El candidato más probable es **InTruth**, por lo reciente y por coincidir casi punto por punto con lo descripto: extensión de Chrome gratuita, lanzada en 2026 por una estudiante de USC, que escucha el audio de un debate o entrevista, detecta afirmaciones verificables y muestra un veredicto con fuentes. En agosto de 2026 declaraba 23 500 usuarios semanales ([Deseret News](https://www.deseret.com/business/2026/08/11/college-student-develops-political-debate-fact-checker/), [Chrome Web Store](https://chromewebstore.google.com/detail/intruth/ikmpglbpcdoapfelcbfpoaddmhmaaocg), [repositorio](https://github.com/rpanigrahi222/intruth-factcheck)). Que sea esta y no otra es `[sin verificar]`: con la misma descripción también encajan Full Fact AI, Chequeabot o ClaimBuster, que están abajo.

**El equipo interno de la farmacéutica.** La transcripción dice «Roamers», que casi seguro es **Laboratorios Roemmers**. No se encontró ninguna fuente que documente un equipo interno de Roemmers dedicado a detectar desinformación `[sin verificar]`. Lo único que aparece es que en marzo de 2020 Roemmers fue **blanco** de una noticia falsa sobre el monopolio de reactivos de COVID-19 y la desmintió con un comunicado del directorio ([Pharmabiz, 27/03/2020](https://www.pharmabiz.net/roemmers-aclara-a-la-opinion/)). Sea como sea, un equipo interno de una empresa protege la reputación de esa empresa: es monitoreo corporativo, no una herramienta para el ciudadano. Es el mismo segmento que Cyabra y Blackbird.AI.

### Contraste por eje

| Herramienta | Qué hace | Para quién | (a) Camino a la evidencia para el ciudadano | (b) Capa ciudadana que genera datos B2B |
|---|---|---|---|---|
| **InTruth** | Extensión de Chrome, verifica en vivo audio de video (debates, entrevistas); 16 idiomas; el usuario pone su propia clave de API | Ciudadano, gratis | ✅ **Sí**: veredicto con enlaces a fuentes de la web abierta, etiquetadas por sesgo con el dataset de MBFC | ❌ No: el desarrollador declara que no recolecta ni guarda nada |
| **Full Fact AI** ([fullfact.org/ai](https://fullfact.org/ai/)) | Monitoreo de TV, prensa, redes; detecta afirmaciones y las cruza contra chequeos previos; en vivo | Verificadores (40+ organizaciones, 30 países), licencia paga | ❌ No: el ciudadano ve solo la nota final que escribe el verificador | ❌ No: es B2B directo, sin capa ciudadana |
| **Chequeabot** ([chequeado.com/chequeabot](https://chequeado.com/chequeabot/)) | Desde 2015 detecta frases chequeables; desde 2019 transcribe en vivo debates y discursos | Verificadores (7 países) | ⚠️ Indirecto: la nota de Chequeado trae fuentes, pero la escribe un humano y llega horas o días después, fuera de X | ❌ No |
| **ClaimBuster** ([UTA](https://idir.uta.edu/claimbuster/debates), [VLDB 2017](https://www.vldb.org/pvldb/vol10/p1945-li.pdf)) | Puntúa qué tan chequeable es una frase y la cruza contra chequeos profesionales; usado en los debates de 2016 | Académico y periodistas | ⚠️ Parcial: remite al chequeo previo, si existe | ❌ No |
| **Factiverse** ([factiverse.ai](https://www.factiverse.ai/)) | Detección y verificación en 114 idiomas, en vivo, contra fuentes que configura el cliente | Medios, gobiernos nórdicos, defensa; se vende con demo | ⚠️ Al cliente profesional, no al ciudadano | ❌ No |
| **Notas de la Comunidad de X** ([API de redactores IA](https://communitynotes.x.com/guide/en/api/overview)) | Notas escritas por usuarios, y desde julio de 2025 también por bots de IA, que se publican si las califican útiles personas con puntos de vista distintos | Ciudadano, dentro de X | ✅ **En parte**: la nota suele traer un enlace `[sin verificar que sea obligatorio]`, pero aparece solo cuando hay consenso, y eso llega tarde o nunca | ⚠️ X publica los datos de las notas en abierto `[sin verificar]`, pero no los analiza por país ni los vende |
| **Grok y Perplexity en X** ([Indicator](https://indicator.media/p/grok-is-this-true-how-x-s-chatbot-performs-as-a-fact-checking-tool), [preprint](https://osf.io/preprints/psyarxiv/85quw_v1)) | El usuario etiqueta al bot («@grok is this true?») y el bot responde en el hilo | Ciudadano, dentro de X | ⚠️ Irregular: a veces cita, a veces no. Coincide con verificadores humanos en el 54,5 % (Grok) y el 57,7 % (Perplexity) de una muestra de 100 posteos | ❌ No, ninguno para terceros |
| **NewsGuard** ([newsguardtech.com](https://www.newsguardtech.com/how-it-works/)) | Extensión que califica **sitios** (0–100) con criterios periodísticos; aparece junto a enlaces en redes y buscadores | Ciudadano (suscripción) y empresas | ❌ No: califica el medio, no la afirmación | ⚠️ Tiene las dos puntas (ciudadano y empresa), pero el dato es la calificación de un medio, no una tendencia de circulación |
| **Logically** ([UKTN](https://www.uktech.news/ai/ai-fact-checker-logically-sold-off-in-administration-deal-20250707)) | Verificación con IA y humanos para plataformas y gobiernos | B2B | ❌ No | ❌ No. Entró en administración en julio de 2025, después de perder los contratos con Meta y TikTok |
| **Roemmers** (equipo interno) | `[sin verificar]` | Uso interno de la empresa | ❌ No | ❌ No |
| **Propuesta** | Extensión en X: separa las afirmaciones de un tuit y contrasta cada una contra fuentes oficiales argentinas, socios de ADEPA y verificadores | Ciudadano, gratis + B2B | ✅ Enlace al documento original por afirmación, con el padrón de fuentes público | ✅ Cada consulta alimenta el agregado anonimizado de tendencias locales |

### Lectura honesta

**El eje (a), solo, no es diferencial.** InTruth ya entrega veredicto con fuentes enlazadas, gratis y en el navegador, y las Notas de la Comunidad ponen contexto con enlaces dentro de X. Si en la defensa se dice «somos los únicos que muestran las fuentes», el argumento se cae con un ejemplo.

Lo que no tiene ninguno es **dónde está, contra qué y cuándo**:

1. **En el texto de X, en el momento de lectura.** InTruth trabaja sobre audio de video y no sirve para posteos de texto. Las Notas de la Comunidad llegan cuando hay consenso, que puede tardar o no llegar nunca. Grok hay que invocarlo, y acierta poco.
2. **Contra un padrón cerrado, público y argentino.** InTruth busca en la web abierta y agrega etiquetas de sesgo de MBFC, que es estadounidense. La propuesta contrasta contra fuentes oficiales argentinas y todos los socios de ADEPA, con el padrón enlazado. La evidencia es el documento de origen (el INDEC, el Boletín Oficial), no una nota de otro medio.
3. **Con el desglose y la afirmación a la vista.** El usuario ve qué afirmación se extrajo del tuit, los puntajes parciales y la postura de cada fuente, no un rótulo suelto. Ojo: hoy se evalúa **una sola afirmación por tuit** (la más central); descomponer el posteo en varias es trabajo futuro (ver [[wiki/solucion/metodologia-tecnica]], reparo del *ex falso*). No prometer «afirmación por afirmación» en la defensa.

**El eje (b) es el que no tiene nadie.** Todas las herramientas pensadas para el ciudadano (InTruth, Notas de la Comunidad, Grok, Chequeado) terminan en el veredicto. Las que venden a empresas (Full Fact, Factiverse, Cyabra, Blackbird.AI, Logically) no tienen capa ciudadana: monitorean lo que el cliente les pide mirar. Ninguna usa lo que el ciudadano consulta como señal de qué desinformación circula en Argentina. NewsGuard es lo más parecido en estructura (extensión para el ciudadano y venta a empresas), pero su dato es la calificación de un medio, no la circulación de una afirmación. La salvedad: el valor de (b) depende de tener volumen de uso, y eso hoy no está demostrado.

**Conclusión:** el diferencial no es ninguna de las dos piezas por separado, es **la combinación**. El ciudadano recibe gratis la evidencia argentina de origen, dentro de X y en el momento de lectura, y ese mismo uso produce el único registro de circulación local de desinformación, que es lo que se vende.

### Respuesta para la defensa

> «Es cierto que hay herramientas parecidas: InTruth verifica debates en vivo con fuentes, y Full Fact o Chequeabot hacen lo mismo para los verificadores profesionales. Lo que ninguna combina es darle gratis al ciudadano, dentro de X y mientras lee, el enlace al documento oficial argentino que sostiene o contradice la afirmación, para que pueda prescindir de nuestro veredicto, y a la vez convertir ese uso en el único registro de qué desinformación circula en Argentina, que es lo que se vende a medios y verificadores. Las herramientas para el ciudadano terminan en el veredicto, y las que se venden a empresas no tienen ciudadanos: nosotros estamos en el medio.»

## Referencias cruzadas

- [[wiki/presentacion/e50/analisis-feedback]]
- [[wiki/negocio/modelo-de-negocio]]
- [[wiki/proyecto/propuesta]]
