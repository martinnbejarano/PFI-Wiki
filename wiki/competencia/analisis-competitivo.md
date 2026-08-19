---
titulo: Análisis Competitivo
tipo: análisis
tags: [competencia, mercado, diferenciacion, oceano-azul]
actualizado: 2026-08-19
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

## Referencias cruzadas

- [[wiki/negocio/modelo-de-negocio]]
- [[wiki/proyecto/propuesta]]
