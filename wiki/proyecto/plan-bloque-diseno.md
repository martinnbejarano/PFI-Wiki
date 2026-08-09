---
titulo: Plan detallado — Bloque de diseño (requerimientos, mockups, diagramas y modelo de datos)
tipo: proyecto
tags: [plan, entrega, 50, ep2, diseño, mockups, diagramas, modelo-de-datos]
fuentes: [Rubrica-EP2-50porciento.pdf]
actualizado: 2026-08-08
---

# Plan detallado — Bloque de diseño

**Del 9 al 14 de agosto de 2026.** Los Bloques 1 y 2 de [[wiki/proyecto/plan-entrega-50]] se fusionan en un tramo único: los mockups le dan retroalimentación a los casos de uso y el modelo de datos se estabiliza recién cuando los tres artefactos convergen, así que separarlos por una barrera de tres días obligaba a rehacer.

Cubre cuatro de los ocho criterios de la rúbrica: **1 (requerimientos)**, **2 (mockups)**, **3 (diagramas)** y **6 (modelo de datos)**, y deja preparado el **5 (tecnologías)** que se cierra en el bloque siguiente.

---

## Decisiones de producto tomadas el 2026-08-08

Ninguno de los artefactos se podía escribir sin estas ocho definiciones. Quedan registradas acá porque son las premisas de todo lo que sigue y porque varias hay que defenderlas en la exposición.

| # | Decisión | Qué se resolvió | Consecuencia directa |
|---|---|---|---|
| 1 | **Modo de análisis** | Híbrido. El Módulo 1 corre automático sobre los tuits visibles y pinta el badge; los Módulos 2, 3 y 4 se disparan solo al hacer clic | Hay **dos flujos**, no uno. Atraviesa el diagrama de secuencia, el de flujo de información y el campo `origen` de la tabla de análisis |
| 2 | **Identidad** | Dos niveles. Extensión ciudadana anónima con UUID en el almacenamiento local del navegador; clientes B2B con cuenta de organización (Google OAuth) y clave de API | Suma cuatro entidades al modelo de datos y conecta el capítulo de negocio con el de solución |
| 3 | **Persistencia** | Completa, incluido el `@` del autor en claro | Habilita el Módulo 2 (que necesita metadatos de cuenta reales) y el corpus argentino de la Entrega 4. **Obliga a reescribir la matriz de riesgo legal** |
| 4 | **Defensa legal** | Recolección amparada en el art. 5 inc. 2.b de la Ley 25.326 (fuentes de acceso público irrestricto); exportación B2B agregada o anonimizada por el art. 11 (cesión) | Tarea explícita del bloque, no un pendiente vago |
| 5 | **Toolchain de diagramas** | draw.io. Se generan los `.drawio` como XML versionado en el repositorio; el ajuste visual y la exportación son manuales | El fuente queda en git y una corrección del tutor no es rehacer el dibujo |
| 6 | **Mockups** | HTML y CSS reales, capturados desde Chrome, con contenido ficticio verosímil | El mismo HTML es el punto de partida de la extensión del Bloque 3: el mockup y la demo son un solo trabajo |
| 7 | **Almacén vectorial** | `pgvector` sobre el PostgreSQL de Railway, con Qdrant y Pinecone documentados como alternativas evaluadas | Costo adicional cero, un solo motor en el diagrama de despliegue, y una justificación comparada para el criterio 5 |
| 8 | **Contenido de los mockups** | Tuits ficticios verosímiles sobre temas argentinos reales, marcados como ilustrativos | El documento no señala a ninguna persona identificable como fuente de desinformación |

---

## Calendario

| Día | Foco | Entregable al cierre |
|---|---|---|
| **Domingo 9/08** | Requerimientos funcionales y no funcionales | `wiki/solucion/requerimientos.md` con las dos tablas completas |
| **Lunes 10/08** | Casos de uso desarrollados + diagrama de casos de uso | Casos de uso cerrados; `casos-de-uso.drawio` generado |
| **Martes 11/08** | Mockups (las cuatro pantallas) | HTML/CSS + capturas en `raw/assets/mockups/` |
| **Miércoles 12/08** | Diagramas de arquitectura (contexto, contenedores, componentes) | Tres `.drawio` generados; `wiki/solucion/arquitectura.md` reescrita |
| **Jueves 13/08** | Flujo de información, secuencia y despliegue | Tres `.drawio` restantes |
| **Viernes 14/08** | Modelo de datos + reescritura legal + cierre | `wiki/solucion/modelo-datos.md`, DER, `restricciones-legales-eticas.md` actualizada |

El orden no es arbitrario: los mockups van **entre** los casos de uso y los diagramas a propósito. Dibujar la pantalla obliga a descubrir estados que el caso de uso escrito no contempla —qué se muestra mientras el Módulo 3 tarda, qué pasa si la búsqueda web no devuelve nada— y esos estados son los que después aparecen en el diagrama de secuencia.

---

## Artefacto 1 — Requerimientos (criterio 1)

Destino: `wiki/solucion/requerimientos.md`, hoy un *stub* de abril con `[POR DEFINIR]`.

**Requerimientos funcionales.** Numeración `RF-NN`, agrupados por módulo de producto y con prioridad MoSCoW. Los grupos previstos:

- Detección y análisis (RF-01 a RF-08): análisis automático del *timeline*, análisis profundo a demanda, extracción de la afirmación verificable, consulta a fuentes oficiales según el tipo de afirmación, generación del veredicto en tres niveles y del `reasoning` en lenguaje natural.
- Presentación al usuario (RF-09 a RF-14): badge en tres estados, desglose por módulo, panel de evidencia con las fuentes enlazadas, histórico local.
- Retroalimentación (RF-15 a RF-17): reporte de falso positivo, ajuste de sensibilidad, desactivación por sitio.
- Plataforma B2B (RF-18 a RF-23): alta de organización, emisión y revocación de claves de API, endpoint de clasificación, cuotas por plan, dashboard de tendencias, exportación anonimizada.

**Requerimientos no funcionales.** Numeración `RNF-NN` con categoría. Salen casi todos de decisiones ya tomadas y por eso son defendibles con un número, no con un adjetivo:

| Categoría | Qué se compromete | De dónde sale |
|---|---|---|
| Rendimiento | El flujo automático no supera cierta latencia por tuit; el flujo a demanda tiene un techo distinto porque incluye búsqueda web | Decisión 1 |
| Calidad del modelo | F1 macro objetivo de 0,80 y al menos 10 puntos porcentuales sobre la línea base TF-IDF + regresión logística | [[wiki/modelos/modelos-overview]] |
| Privacidad | Cero datos personales del usuario de la extensión; tratamiento de datos de terceros conforme al art. 5.2.b; exportación B2B anonimizada | Decisiones 2, 3 y 4 |
| Compatibilidad | Chrome de escritorio, Manifest V3 | [[wiki/proyecto/propuesta]] |
| Costo operativo | Techo mensual de infraestructura para el período del PFI | [[wiki/proyecto/recursos]] |
| Disponibilidad | Degradación elegante: si cae Hugging Face o la API de búsqueda, el sistema informa análisis parcial en lugar de fallar |  Decisión 1 |
| Explicabilidad | Todo veredicto viene acompañado de al menos una fuente enlazada verificable | [[wiki/solucion/metodologia-tecnica]] |

**Casos de uso.** Siete, desarrollados con actor, precondición, flujo principal, flujos alternativos y postcondición:

1. **CU-01 — Analizar automáticamente el *timeline*.** Actor: extensión. Es el caso de uso que más se ejecuta y el que nadie dispara a mano.
2. **CU-02 — Solicitar el análisis profundo de un tuit.** Actor: ciudadano. Dispara los Módulos 2, 3 y 4.
3. **CU-03 — Consultar la evidencia de un veredicto.** Actor: ciudadano. Es el caso de uso que materializa la explicabilidad.
4. **CU-04 — Reportar un falso positivo.** Actor: ciudadano. Alimenta la corrección del modelo.
5. **CU-05 — Consultar el histórico personal.** Actor: ciudadano.
6. **CU-06 — Consumir la API de detección.** Actor: sistema cliente B2B, autenticado por clave.
7. **CU-07 — Consultar el dashboard de tendencias.** Actor: analista de una organización B2B.

Los flujos alternativos importan tanto como los principales: el tuit ya está en caché, la búsqueda web no devuelve resultados, el servicio de inferencia no responde, la afirmación no es verificable. Son los que después justifican los estados de las pantallas.

---

## Artefacto 2 — Mockups (criterio 2)

Destino: `wiki/solucion/mockups.md` y las capturas en `raw/assets/mockups/`. Se construyen con HTML y CSS reales y se capturan desde Chrome, para que el Bloque 3 herede el marcado.

| Pantalla | Qué muestra | Por qué está |
|---|---|---|
| **Badge en el *timeline*** | El indicador inyectado sobre el tuit, en sus tres estados: probablemente falso, información sospechosa, parece verificado. Más el cuarto estado real: analizando | Es el producto. Si esta pantalla no se entiende en dos segundos, no hay producto |
| **Popup con el veredicto** | Score final, los tres niveles de veredicto con su umbral, desglose por módulo y las razones en lenguaje natural | Muestra que el sistema no es una caja negra binaria |
| **Panel de evidencia** | Las fuentes vinculadas agrupadas por tipo (desmentida previa, medio confiable, fuente oficial) y por postura (corrobora, contradice, neutral), con el enlace al documento original | Es lo único que ningún competidor de la matriz comparativa entrega al ciudadano |
| **Dashboard B2B** | Histórico, tendencias semanales, cuentas con más contenido marcado, y el panel de claves de API | Justifica que exista un backend con base de datos y conecta el capítulo de negocio con el de solución |

Cada pantalla lleva un pie explicativo en el documento. La rúbrica no premia cantidad sino que sean *claras y significativas*, así que cuatro bien resueltas superan a ocho a medias.

---

## Artefacto 3 — Diagramas (criterios 3 y 5)

Seis diagramas. Para cada uno se genera el `.drawio` con las cajas, las etiquetas y las flechas ya puestas; queda el ajuste de posición y la exportación.

**1. Contexto — C4 nivel 1.** El sistema como una sola caja. Actores: ciudadano y cliente B2B. Sistemas externos: Twitter/X, la API de inferencia de Hugging Face, la API de búsqueda web, los medios confiables, las fuentes oficiales argentinas y las organizaciones de *fact-checking*. Es el diagrama que contesta la primera pregunta de cualquier evaluador técnico: de qué terceros depende esto.

**2. Contenedores — C4 nivel 2.** Extensión de Chrome (*content script*, *service worker*, *popup*), panel web en Vercel, API REST en Railway, PostgreSQL con `pgvector` en Railway, servicio de inferencia en Hugging Face. Cada flecha rotulada con protocolo y formato.

**3. Componentes de la API.** El interior del contenedor de Railway: orquestador, los cuatro módulos —con el Módulo 3 abierto en sus cuatro partes: extractor de afirmaciones, buscador vectorial, buscador web y enrutador de fuentes oficiales—, la capa de caché y la de repositorios.

**4. Flujo de información.** Del tuit al veredicto, con los dos caminos de la decisión 1 claramente separados: el flujo automático barato y el flujo a demanda caro. Marca en qué punto se consulta el caché y en cuál se persiste.

**5. Secuencia end-to-end.** Líneas de vida: usuario, *content script*, *service worker*, API, caché y base de datos, inferencia, búsqueda web, fuente oficial. Dos fragmentos alternativos: acierto de caché y análisis completo. Incluye el camino de degradación cuando un servicio externo no responde.

**6. Despliegue y arquitectura de red.** El único que cubre a la vez el criterio 6 (*diagrama de arquitectura*) y la parte de *arquitectura de red* que pide el criterio 5. Navegador del usuario, CDN de Vercel, contenedor de Railway con su base gestionada, endpoint de Hugging Face y APIs de terceros, con los protocolos, el cifrado en tránsito y los límites de confianza dibujados.

El diagrama de casos de uso, aunque pertenece al criterio 1, se genera con el mismo toolchain el 10/08.

---

## Artefacto 4 — Modelo de datos (criterio 6)

Destino: `wiki/solucion/modelo-datos.md`. Motor ya decidido en [[wiki/proyecto/recursos]]: PostgreSQL gestionado en Railway, con la extensión `pgvector` para las columnas de *embeddings*.

Catorce entidades agrupadas en cuatro dominios:

**Contenido analizado** — `tuit` (identificador nativo, texto, `@` del autor, fecha de publicación, plataforma, URL, métricas de propagación, fecha de captura), `cuenta` (antigüedad, seguidores, seguidos, verificación, historial agregado) y `medio_confiable`.

**Análisis** — `analisis` (los tres *scores* parciales, el final, la confianza, el veredicto, el origen automático o a demanda y la versión de modelo usada), `claim` (texto de la afirmación, tipo, y la columna `vector` con su *embedding*), `evidencia` (tipo de fuente, URL, texto, similitud y postura) y `desmentida` (el corpus indexado de Chequeado y Reverso, también con columna vectorial).

**Uso ciudadano** — `usuario_extension` (solo el UUID anónimo y la configuración), `reporte_falso_positivo` y `modelo_version` (nombre del *checkpoint*, fecha de entrenamiento, F1 macro, dataset), que es lo que hace trazable qué modelo produjo qué veredicto.

**Plataforma B2B** — `organizacion`, `usuario_b2b`, `api_key` y `consumo_api`, que es lo que hace ejecutable el *pricing* por volumen del modelo de negocio.

La columna `vector` de `claim` y `desmentida` con índice HNSW es lo que implementa el buscador por similitud del Módulo 3 sin sumar un servicio al despliegue.

---

## Artefacto 5 — Reescritura del apartado legal

Consecuencia obligada de la decisión 3. `wiki/proyecto/restricciones-legales-eticas.md` marca hoy en su matriz (líneas 29-30) como riesgo alto guardar el identificador de usuario sin anonimizar y propone hashearlo. Al persistir el `@` en claro esa matriz queda desactualizada y contradice el diseño.

La reescritura tiene dos partes, porque el riesgo real está partido en dos:

1. **Recolección.** Amparada por el art. 5 inc. 2.b de la Ley 25.326, que exime del consentimiento a los datos obtenidos de fuentes de acceso público irrestricto. Un tuit público encaja de lleno. Se documenta el criterio y su límite: no aplica a cuentas protegidas ni a mensajes directos.
2. **Cesión a terceros.** Es el punto expuesto, y es el art. 11. Vender el dataset a un medio es una cesión de datos personales. La mitigación de diseño es que toda exportación B2B sale agregada o con el autor anonimizado, y eso pasa a ser un requerimiento no funcional con su identificador, no una buena intención.

---

## Riesgos del bloque

| Riesgo | Señal temprana | Mitigación |
|---|---|---|
| Los mockups se comen el tiempo de los diagramas | El 11/08 termina sin las cuatro pantallas capturadas | Congelar el CSS en lo que haya y pasar a diagramas; el pulido estético vuelve en el Bloque 4 si sobra tiempo |
| El ajuste manual de seis `.drawio` es más lento de lo previsto | El 13/08 quedan dos sin exportar | Los de contexto y componentes son los más simples y pueden exportarse sin ajuste; el esfuerzo se concentra en secuencia y despliegue |
| El modelo de datos crece sin control | Aparecen entidades que ningún caso de uso usa | Regla de corte: toda entidad tiene que ser trazable a un RF. Si no lo es, se va |
| Las decisiones de producto se contradicen con lo ya escrito en el wiki | Aparecen afirmaciones viejas sobre un solo flujo de análisis | Al cerrar el bloque, pasar por [[wiki/solucion/metodologia-tecnica]] y [[wiki/proyecto/propuesta]] y alinear |

## Definición de terminado

El bloque cierra el 14/08 cuando: las dos tablas de requerimientos están completas y sin `[POR DEFINIR]`; los siete casos de uso están desarrollados con sus flujos alternativos; las cuatro capturas de mockup existen en `raw/assets/mockups/`; los siete `.drawio` (seis más el de casos de uso) están exportados a PNG o PDF; el DER tiene sus catorce entidades con atributos y cardinalidades; y la matriz legal ya no se contradice con el diseño.

Lo que **no** entra en este bloque: escribir `chapter04.tex` (es el Bloque 4), el *vertical slice* de la demo (Bloque 3), y la justificación tecnológica completa (Bloque 3), aunque este bloque le deja preparado el diagrama de red que ese criterio exige.

## Referencias cruzadas

- [[wiki/proyecto/plan-entrega-50]]
- [[wiki/proyecto/entrega-50-alcance]]
- [[wiki/proyecto/cronograma]]
- [[wiki/solucion/requerimientos]]
- [[wiki/solucion/arquitectura]]
- [[wiki/solucion/metodologia-tecnica]]
- [[wiki/proyecto/restricciones-legales-eticas]]
- [[wiki/proyecto/recursos]]
- [[wiki/negocio/modelo-de-negocio]]
