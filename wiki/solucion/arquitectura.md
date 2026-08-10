---
titulo: Arquitectura de la Solución
tipo: análisis
tags: [arquitectura, diseño, infraestructura, c4, componentes, adr, secuencia, despliegue, red]
fuentes: [Rubrica-EP2-50porciento.pdf]
actualizado: 2026-08-13
---

# Arquitectura de la Solución

Cubre el **criterio 3** de la rúbrica de EP2, aporta la mitad del **criterio 6** y la parte de *arquitectura de red* del **criterio 5**. El modelo de datos vive en [[wiki/solucion/modelo-datos]].

**Fuentes de los diagramas**, todos en `wiki/assets/diagramas/`: `c4-contexto.drawio`, `c4-contenedores.drawio`, `c4-componentes.drawio`, `flujo-informacion.drawio`, `secuencia-cu01.drawio`, `secuencia-cu02.drawio` y `despliegue-red.drawio`. Se editan y exportan desde draw.io; las exportaciones van a `documento/chapters/figures/`.

## Descripción general

El sistema es una extensión de navegador con un servicio de análisis detrás. Se estructura en tres piezas desplegables —la extensión, un panel web y una API— más una base de datos y un servicio de inferencia contratado. Sobre la API corren los cuatro módulos descritos en [[wiki/solucion/metodologia-tecnica]].

Dos restricciones dieron forma a todo lo demás y conviene enunciarlas antes de los diagramas, porque explican decisiones que de otro modo parecen arbitrarias:

**El análisis ocurre en dos flujos con costos muy distintos.** El Módulo 1 corre automáticamente sobre los tuits visibles; los Módulos 2, 3 y 4 solo cuando el usuario hace clic. La búsqueda web y las consultas a fuentes oficiales tienen costo monetario y latencia de segundos, y ejecutarlas sobre cada tuit del *scroll* no se sostiene ni en presupuesto ni en RNF-01. Esa bifurcación atraviesa el orquestador, el caché y el diagrama de secuencia.

**La inferencia no puede correr donde corre la API.** El plan Hobby de Railway ofrece 512 MB de RAM: alcanzan para FastAPI, no para cargar un *transformer*. Son dos cómputos con costo separado, y por eso Hugging Face aparece como contenedor externo y no como una biblioteca dentro del servicio.

## Nivel 1 — Contexto del sistema

Ver `c4-contexto.drawio`.

Interactúan dos personas: el **ciudadano**, que usa la extensión de forma anónima, y el **analista B2B**, autenticado y perteneciente a una organización con suscripción. El sistema depende de siete sistemas externos, y esa dependencia es en sí misma un riesgo arquitectónico que el diagrama expone de entrada:

| Sistema externo | Para qué | Si cae |
|---|---|---|
| Twitter/X | Superficie de detección: se lee el DOM público del *timeline* | No hay producto. Es la dependencia estructural |
| Hugging Face Inference | Ejecuta el modelo XLM-T del Módulo 1 | No se pinta indicador; el flujo automático queda mudo |
| Fuentes oficiales argentinas | Contraste contra el documento — prioridad 1 | Análisis parcial señalado (RNF-11) |
| Medios de referencia | Contraste y consenso — prioridad 2 | Análisis parcial señalado |
| Verificadores profesionales | Verificación equivalente — prioridad 3 | Sin efecto: es el caso frecuente |
| API de búsqueda web | Recupera las notas de los medios para una afirmación | Cae el camino de medios del Módulo 3 |
| Proveedor de identidad | Autentica a los usuarios B2B | Afecta solo al panel B2B; el ciudadano no se autentica |

La jerarquía de evidencia está dibujada en el diagrama: las fuentes oficiales y los medios van en verde y con línea continua; los verificadores van con línea punteada porque su cobertura es baja y su latencia de días. La justificación completa está en [[wiki/solucion/metodologia-tecnica]].

## Nivel 2 — Contenedores

Ver `c4-contenedores.drawio`.

| Contenedor | Tecnología | Responsabilidad |
|---|---|---|
| **Extensión de Chrome** | JavaScript, Manifest V3 | *Content script* que lee el DOM e inyecta el indicador; *service worker* que agrupa pedidos y custodia el UUID anónimo; *popup* con el veredicto y la evidencia |
| **Panel web** | React sobre Vercel | Histórico del ciudadano y panel de tendencias B2B. No hace cómputo pesado, por eso puede servirse estático y gratis |
| **API REST** | Python y FastAPI sobre Railway | Orquesta los cuatro módulos, resuelve el caché, autentica clientes B2B y aplica cuotas. Siempre activa: no se duerme por inactividad, que es lo que descartó las alternativas gratuitas |
| **Base de datos** | PostgreSQL 16 con `pgvector` sobre Railway | Contenido analizado, evidencia, análisis y plataforma B2B. Los *embeddings* viven acá, en columnas `vector` con índice HNSW |
| **Servicio de inferencia** | XLM-T en Hugging Face | Clasificación del Módulo 1 |

La separación entre el *content script* y el *service worker* no es un detalle de implementación: el primero corre en el hilo de la página y por eso RNF-04 le pone un techo de 50 ms por tuit. Todo lo que no sea leer el DOM e inyectar el indicador tiene que ocurrir en el *service worker*, que es donde además se agrupan los pedidos para no disparar una solicitud por cada tuit que entra en pantalla.

## Nivel 3 — Componentes de la API

Ver `c4-componentes.drawio`.

Tres puntos de entrada: el endpoint de análisis que usa la extensión, el endpoint de clasificación que se le vende a los clientes B2B, y el componente de autenticación y cuotas que protege al segundo. Que sean dos endpoints separados y no uno con un parámetro es deliberado: el contrato B2B es un producto con precio y no debería moverse cuando cambia la extensión.

El **orquestador** es el componente donde vive la decisión de los dos flujos. Recibe el pedido, consulta el caché, y según el flujo ejecuta solo el Módulo 1 o los cuatro. También es el que marca el resultado como parcial cuando un módulo falla, en lugar de dejar que el ensamblador promedie sobre datos faltantes.

El **Módulo 3** está abierto en cinco componentes, y su disposición interna es la jerarquía de evidencia hecha estructura:

- **Extractor de afirmaciones** — NER más clasificación por tipo, que es lo que después rutea la consulta.
- **Enrutador de fuentes oficiales** (prioridad 1) — según el tipo de afirmación va a InfoLEG, INDEC, BCRA, Boletín Oficial, MSal o MinEdu.
- **Cliente de medios de referencia** (prioridad 2) — consulta los cinco medios y mide consenso.
- **Buscador vectorial** (prioridad 3) — verificaciones previas por similitud sobre `pgvector`. Entra con línea punteada: es opcional, y cuando no hay verificación equivalente —el caso frecuente— el contraste no se degrada.
- **Evaluador de postura** — clasifica cada fuente como corrobora, contradice o neutral y sintetiza `score_similarity` junto con el arreglo de fuentes vinculadas.

Los **repositorios** son el único punto de acceso a la base. No es purismo: el buscador vectorial y el caché consultan la misma base que persiste los análisis, y concentrar el acceso es lo que permite que la decisión de `pgvector` no se filtre a los módulos.

## Flujo de información

Ver `flujo-informacion.drawio`. Es un diagrama de actividad UML con cinco calles —extensión, orquestador, módulos, base de datos y servicios externos— y su elemento central es la bifurcación que separa los dos flujos.

El recorrido tiene dos entradas y una sola salida. La entrada automática es un tuit que aparece en el área visible; la entrada a demanda es un clic sobre un indicador ya pintado. Ambas convergen en la misma pregunta —si existe un análisis vigente en caché— y recién después se separan según el origen del pedido. La rama automática ejecuta únicamente el Módulo 1 y tiene que resolverse en 2 segundos; la rama a demanda ejecuta los Módulos 2, 3 y 4 y dispone de 8.

Dentro del Módulo 3 el orden de las tres consultas no es casual: primero la fuente oficial, después los cinco medios, y solo entonces los verificadores, dibujados con línea punteada. Del nodo de medios salen dos aristas hacia la evaluación de postura: una pasa por los verificadores y la otra los saltea. La segunda es el camino frecuente, y que esté dibujada es lo que deja constancia de que la ausencia de una verificación previa no degrada el resultado.

Hay dos puntos de persistencia, no uno. Tras el Módulo 1 se guardan el tuit y su `score_nlp`; tras el Módulo 4, el análisis completo con su evidencia y la versión de modelo que lo produjo. El segundo es lo que hace reproducible un veredicto meses más tarde, que es una exigencia del trabajo experimental de la Entrega 5.

El camino de excepción desemboca en un nodo de análisis parcial que alimenta igual al Módulo 4. La alternativa —devolver error, o promediar sobre lo que haya sin avisar— produce en un caso una pérdida de trabajo ya hecho y en el otro un veredicto peor sin que nadie lo sepa.

## Secuencia

Dos diagramas en lugar de uno, por la misma razón por la que RNF-01 y RNF-02 son números distintos: son dos recorridos con actores, costos y techos de latencia diferentes, y superponerlos en un solo dibujo con fragmentos anidados los vuelve ilegibles sin explicar nada más.

**`secuencia-cu01.drawio` — flujo automático.** Seis líneas de vida. El mensaje que importa es el que va del *service worker* a la API: es uno por lote de tuits visibles, no uno por tuit. Un fragmento `alt` separa el acierto de caché, que retorna dentro de los 300 milisegundos, del recorrido completo contra el servicio de inferencia. Un fragmento `opt` cubre el fallo de la inferencia, y su resolución es deliberadamente silenciosa: no se pinta indicador y no se muestra error, porque el usuario no pidió nada y un aviso de fallo sobre un tuit que apenas pasó por pantalla sería ruido.

**`secuencia-cu02.drawio` — flujo a demanda.** Diez líneas de vida, con el Módulo 3 abierto en sus tres fuentes. La llamada a los verificadores está dentro de un `opt` y el retorno del Módulo 3 ocurre igual cuando ese fragmento no se ejecuta. El fragmento `alt` del final es el de degradación: si alguna fuente externa no respondió, el Módulo 4 recibe los *scores* disponibles junto con la marca de parcial, y esa marca viaja hasta la pantalla.

La nota sobre el *content script* del primer diagrama registra una restricción que ningún otro artefacto dejaba escrita: como corre en el hilo de la página, el techo de 50 milisegundos de RNF-04 aplica solo a él. Leer el DOM e inyectar el indicador es todo lo que puede hacer; agrupar pedidos, custodiar el UUID y hablar con la API tienen que ocurrir en el *service worker*.

## Despliegue y arquitectura de red

Ver `despliegue-red.drawio`. Cubre a la vez el diagrama de arquitectura que pide el criterio 6 y la arquitectura de red del criterio 5. Está organizado en cinco zonas ordenadas por grado de control:

| Zona | Qué contiene | Control |
|---|---|---|
| Equipo del ciudadano | Chrome con la extensión y el almacenamiento local con el UUID anónimo | Ninguno |
| Organización cliente B2B | El sistema que consume la API y el navegador del analista | Ninguno |
| Borde CDN — Vercel | Panel web estático, TLS terminado en el borde | Configuración |
| Nube de la aplicación — Railway | Contenedor FastAPI y PostgreSQL con `pgvector`, unidos por red privada sin puerto público | Total |
| Terceros | Inferencia, búsqueda web, fuentes oficiales, medios, verificadores y proveedor de identidad | Ninguno |

Tres de las cinco zonas están fuera de todo control del proyecto. Enunciado así, RNF-11 deja de parecer una cláusula de estilo: la degradación a análisis parcial es la consecuencia directa de que el sistema dependa de siete servicios ajenos.

Lo que vuelve útil a este diagrama no son los nodos sino lo que marca en los cruces de límite, porque es donde el argumento legal deja de ser un párrafo y se vuelve visible:

- **Extensión hacia la API.** Sale el texto del tuit y el `@` del autor en claro. Es el dato de tercero amparado en el art. 5 inc. 2.b de la Ley 25.326, que exime del consentimiento a los datos obtenidos de fuentes de acceso público irrestricto. El límite del amparo también está declarado: no alcanza a cuentas protegidas ni a mensajes directos.
- **API hacia el servicio de inferencia.** El texto del tuit sale hacia un tercero. Conviene que esté dibujado y no escondido detrás de una caja rotulada *modelo*.
- **API hacia las fuentes de evidencia.** Sale la afirmación extraída, no el tuit crudo. Es una diferencia real de exposición y por eso se dibuja distinto.
- **API hacia el cliente B2B.** Es la única arista que transporta datos hacia afuera del sistema, y es una cesión en los términos del art. 11. Por eso sale agregada o con la cuenta autora anonimizada. Que esa mitigación sea RF-25 con prioridad imprescindible, y no una buena intención, es lo que la vuelve verificable.
- **API con la base de datos.** Red privada de Railway: la base no expone puerto público a internet.

## Decisiones de arquitectura

| Decisión | Alternativas evaluadas | Por qué |
|---|---|---|
| Análisis en dos flujos, uno automático y barato y otro a demanda y caro | Todo automático; todo a demanda | Todo automático no se sostiene en costo ni en latencia; todo a demanda le quita a la extensión su razón de ser, que es avisar sin que se lo pidan |
| Inferencia en Hugging Face, separada de la API | Cargar el modelo en el mismo contenedor | Railway Hobby tiene 512 MB de RAM. No entra un *transformer* de ~125M parámetros |
| Backend en Railway | Render Starter (7 USD, sin base incluida), Fly.io Hobby (sin base, más configuración) | PostgreSQL incluido y servicio *always-on*. Los planes gratuitos que se duermen rompen una extensión que llama en tiempo real |
| `pgvector` sobre el mismo PostgreSQL | Qdrant, Pinecone | Implementa HNSW igual que un motor dedicado. La ventaja de los dedicados aparece arriba del millón de vectores; el prototipo tendrá decenas de miles. Costo adicional cero y un servicio menos en el despliegue |
| Panel web estático en Vercel, separado del backend | Servir el panel desde la misma API | No requiere cómputo; separarlo lo hace gratis y saca tráfico del contenedor pago |
| Identidad en dos niveles: ciudadano anónimo, B2B autenticado | Cuenta única para todos; sin cuentas | El ciudadano no necesita cuenta y no tenerla elimina el tratamiento de datos personales del usuario (RNF-08). El B2B la necesita porque hay un plan y una cuota que cobrar |
| Autenticación B2B delegada a un proveedor externo | Usuarios y contraseñas propios | Evita almacenar y rotar contraseñas, y quita superficie de seguridad sin perder nada |
| Degradación a análisis parcial | Reintentar hasta obtener todos los módulos; devolver error | Reintentar rompe RNF-02; devolver error desperdicia los módulos que sí respondieron. La tercera vía es informar qué falta (RNF-11) |

## Lo que este nivel de detalle no resuelve todavía

No están definidos el esquema de reintentos y *timeouts* por servicio externo, ni la política de expiración del caché, ni cómo se versiona el contrato de la API B2B. Los tres son decisiones de implementación que corresponden a la Entrega 4 y que hoy no bloquean ningún criterio de la rúbrica.

## Referencias cruzadas

- [[wiki/solucion/requerimientos]]
- [[wiki/solucion/mockups]]
- [[wiki/solucion/metodologia-tecnica]]
- [[wiki/solucion/modelo-datos]]
- [[wiki/solucion/tecnologias]]
- [[wiki/proyecto/recursos]]
- [[wiki/proyecto/plan-bloque-diseno]]
- [[wiki/negocio/modelo-de-negocio]]
