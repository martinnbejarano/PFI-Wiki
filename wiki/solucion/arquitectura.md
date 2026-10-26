---
titulo: Arquitectura de la Solución
tipo: análisis
tags: [arquitectura, diseño, infraestructura, c4, componentes, adr, secuencia, despliegue, red]
fuentes: [Rubrica-EP2-50porciento.pdf]
actualizado: 2026-10-26
---

# Arquitectura de la Solución

Cubre el **criterio 3** de la rúbrica de EP2, aporta la mitad del **criterio 6** y la parte de *arquitectura de red* del **criterio 5**. El modelo de datos vive en [[wiki/solucion/modelo-datos]].

**Fuentes de los diagramas:** los `.svg` de `wiki/assets/diagramas/svg/` (los `.drawio` de la carpeta de arriba quedan como histórico). Se renderizan a `documento/chapters/figures/` con `wiki/assets/diagramas/svg/render.sh`.

> **Tal como está construido (2026-10-19, #71).** Dos piezas desplegables: la extensión de Chrome y la API FastAPI en Railway, región `eu-west` (Ámsterdam), con HTTPS. La persistencia es **SQLite** en un volumen montado en `/data`: siete tablas (`cuenta`, `tuit`, `analisis`, `reporte`, `organizacion`, `api_key`, `consumo_api`; ver `prototipo/servicio/app/historial.py`), sin PostgreSQL, sin `pgvector` y sin Alembic. La evidencia la recupera la búsqueda web de OpenAI restringida a los dominios de la jerarquía; **desde el 2026-10-26 (#107) la complementa el índice local de fuentes oficiales**, que llena una ingesta diaria (ver la última sección). BETO corre como segundo servicio de Railway (`clasificador`, `eu-west`), que la API llama por la red privada (`http://clasificador.railway.internal:7860`); los pesos se bajan al arrancar del repositorio privado de Hugging Face `martinnbejarano/beto-fakedes-chequeado`. No hay Space (los Space Docker gratuitos ya no existen). El flujo a demanda (`POST /analizar`) hace dos llamadas al LLM: extracción + evidencia en una sola (#93) y, después de que el combinador decide el veredicto, la redacción de la justificación; los Módulos 1 y 2 no dependen de la primera. El flujo automático (`POST /senales`, lotes ≤ 20) devuelve una señal de prioridad sin veredicto y no se persiste (#92); `GET /analisis/{id}` sirve el veredicto previo desde una caché en memoria. Lo que sigue en esta página es el diseño completo; el capítulo 4 del documento ya está alineado a lo construido (diagramas de casos de uso, contenedores, componentes, secuencias, DER y despliegue).

## Descripción general

El sistema es una extensión de navegador con un servicio de análisis detrás. Se estructura en cuatro piezas desplegables —la extensión, un panel web, una API y una tarea programada de ingesta— más una base de datos y un servicio de inferencia contratado. Sobre la API corren los cuatro módulos descritos en [[wiki/solucion/metodologia-tecnica]].

Dos restricciones dieron forma a todo lo demás y conviene enunciarlas antes de los diagramas, porque explican decisiones que de otro modo parecen arbitrarias:

**El análisis ocurre en dos flujos con costos muy distintos.** El Módulo 1 corre automáticamente sobre los tuits visibles; los Módulos 2, 3 y 4 solo cuando el usuario hace clic. La búsqueda web y las consultas a fuentes oficiales tienen costo monetario y latencia de segundos, y ejecutarlas sobre cada tuit del *scroll* no se sostiene ni en presupuesto ni en RNF-01. Esa bifurcación atraviesa el orquestador, el caché y el diagrama de secuencia.

**La inferencia no puede correr donde corre la API, y el motivo es de presupuesto y no de memoria.** El plan Hobby de Railway no impone un techo de RAM: son cinco dólares mensuales con un crédito de uso equivalente y facturación por consumo. Un contenedor con un *transformer* de unos 125 millones de parámetros residente consume memoria de forma continua y quema ese crédito en días, mientras que la inferencia bajo demanda se paga por invocación. El techo que decide es RNF-14. Por eso Hugging Face aparece como contenedor externo y no como una biblioteca dentro del servicio.

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
| **Panel web** | React 19.2.8 sobre Vite, servido estático en Vercel | Histórico del ciudadano y panel de tendencias B2B. No hace cómputo pesado, por eso puede servirse estático |
| **API REST** | Python y FastAPI sobre Railway | Orquesta los cuatro módulos, resuelve el caché, autentica clientes B2B y aplica cuotas. Siempre activa: no se duerme por inactividad, que es lo que descartó las alternativas gratuitas |
| **Base de datos** | SQLite en un volumen de Railway (`/data`) | Histórico por instalación, informes de error, cuentas y tuits del panel de tendencias, organizaciones, claves y consumo. *Diseño original: PostgreSQL 16 con `pgvector` para los* embeddings*; descartado al reemplazar el índice local por la búsqueda web* |
| **Ingesta programada** | Python, dentro del contenedor de la API; la dispara un servicio cron de Railway (`curlimages/curl`) | Recorre cinco fuentes oficiales respetando `robots.txt` y el `crawl-delay`, y las indexa (RF-05). Construida el 2026-10-26 (#107); complementa la búsqueda web, no la reemplaza. *Diseño original: un contenedor propio que corre y termina*; ver la última sección |
| **Servicio de inferencia** | XLM-T y `multilingual-e5-base` en Hugging Face | Clasificación del Módulo 1 y codificación de los *embeddings* |

La separación entre el *content script* y el *service worker* no es un detalle de implementación: el primero corre en el hilo de la página y por eso RNF-04 le pone un techo de 50 ms por tuit. Todo lo que no sea leer el DOM e inyectar el indicador tiene que ocurrir en el *service worker*, que es donde además se agrupan los pedidos para no disparar una solicitud por cada tuit que entra en pantalla.

## Nivel 3 — Componentes de la API

Ver `c4-componentes.drawio`.

Tres puntos de entrada: el endpoint de análisis que usa la extensión, el endpoint de clasificación que se le vende a los clientes B2B, y el componente de autenticación y cuotas que protege al segundo. Que sean dos endpoints separados y no uno con un parámetro es deliberado: el contrato B2B es un producto con precio y no debería moverse cuando cambia la extensión.

El **orquestador** es el componente donde vive la decisión de los dos flujos. Recibe el pedido, consulta el caché, y según el flujo ejecuta solo el Módulo 1 o los cuatro. También es el que marca el resultado como parcial cuando un módulo falla, en lugar de dejar que el ensamblador promedie sobre datos faltantes.

El **Módulo 3** aparece como un único componente en el dibujo y se detalla acá, que es la forma de mantener el diagrama legible impreso sin perder el detalle. Su composición interna es la jerarquía de evidencia hecha estructura:

- **Extractor de afirmaciones** — un LLM extrae la afirmación y la clasifica por tipo, que es lo que después rutea la consulta. El LLM también recupera evidencia y redacta la justificación, pero **no** produce el puntaje del Módulo 1: ese sale del clasificador propio servido en un Hugging Face Space en CPU. En el prototipo lo resuelve un adaptador compuesto del puerto del proveedor (`ADAPTADOR=compuesto`): el clasificador puntúa el texto del tuit, su versión viaja en `version_modelo` (RF-16), una falla o un tiempo límite dejan el análisis parcial (RNF-11), y el servicio llama al Space periódicamente para que no se duerma (ticket #32). **Desde el 2026-10-13 el prototipo no usa el Space:** el mismo contenedor (`prototipo/clasificador/space/`) corre en local con `make dev`, que levanta BETO de dos etapas en `:7860` junto al servicio (`URL_CLASIFICADOR=http://localhost:7860`, despertador apagado). Medido en un M4: ~490 MB de RAM, ~40 ms por tuit en caliente. Hugging Face exige hoy un plan pago (PRO) para crear un Space Docker o Gradio en CPU, aunque el *hardware* CPU Basic no se cobre por hora [consultado el 2026-09-28; impacta RNF-14, decisión pendiente].
- **Enrutador de fuentes oficiales** (prioridad 1) — según el tipo de afirmación busca por similitud sobre los documentos ya indexados de InfoLEG, INDEC, BCRA, Boletín Oficial, MSal o MinEdu. **Consulta el índice local, no el sitio.**
- **Cliente de medios de referencia** (prioridad 2) — consulta los medios socios de ADEPA y mide consenso.
- **Buscador vectorial** (prioridad 3) — verificaciones previas por similitud sobre `pgvector`. Es opcional: cuando no hay verificación equivalente —el caso frecuente— el contraste no se degrada.
- **Evaluador de postura** — clasifica cada fuente como corrobora, contradice o neutral y sintetiza `score_similarity` junto con el arreglo de fuentes vinculadas.

Los **repositorios** son el único punto de acceso a la base. No es purismo: el buscador vectorial y el caché consultan la misma base que persiste los análisis, y concentrar el acceso es lo que permite que la decisión de `pgvector` no se filtre a los módulos.

## La ingesta de fuentes oficiales

Es el componente que más cambió respecto de la versión anterior de esta página, que describía un enrutador consultando el sitio oficial en el momento de la petición. **Esa consulta en vivo era incompatible con RNF-02.** `argentina.gob.ar` —que aloja los contenidos de MSal y MinEdu— declara `Crawl-delay: 10`, y el flujo a demanda dispone de ocho segundos en el percentil 95. Una petición cada diez segundos no entra en ese presupuesto, y la alternativa de ignorar el `crawl-delay` contradice de plano la postura de [[wiki/proyecto/restricciones-legales-eticas]], que se apoya en respetar lo que cada sitio declara.

**Las seis fuentes oficiales se pre-indexan.** *(En el prototipo son cinco: INDEC, BCRA, Salud, Educación y Boletín Oficial; InfoLEG no se construyó.)* Una tarea programada arranca cada tanto, recorre el catálogo de fuentes, respeta el `crawl-delay` declarado por cada sitio, extrae el texto de los documentos nuevos, obtiene su vector del servicio de inferencia, los inserta en el almacén de documentos y actualiza la fecha de la última corrida de esa fuente. Después termina. Es RF-05, y no es un servicio siempre encendido: se paga solo el tiempo de ejecución.

Tres consecuencias, y las tres son mejoras y no concesiones:

- **RNF-02 se cumple con margen**, porque la consulta del enrutador pasa a ser local: una búsqueda por similitud sobre el mismo índice HNSW que ya usaba el buscador vectorial.

  > ⚠️ CONTRADICCION: la medición de #112 (2026-10-26) muestra lo contrario en el prototipo. El índice no reemplaza la búsqueda web sino que se suma a ella, y los fragmentos alargan el mensaje al LLM: la mediana sube de 13,5 s a 16,4 s. Ver [[wiki/experimentos/mediciones-rnf]].
- **El `crawl-delay` se respeta de verdad**, porque la espera no está en el camino crítico de ninguna petición de usuario.
- **Refuerza la postura legal**: acceso cortés, espaciado y de baja frecuencia, en lugar de una consulta sincrónica por cada tuit que alguien mire.

**El índice es uno solo, y eso es una decisión del modelo de datos.** Los documentos oficiales, las notas de los medios y las verificaciones previas viven en la misma entidad, discriminados por tipo de fuente, sobre un único índice HNSW. Las tres poblaciones se consultan de la misma forma —búsqueda por similitud sobre el texto de una fuente— así que separarlas era triplicar un índice sin ganar nada. El detalle está en [[wiki/solucion/modelo-datos]].

La periodicidad exacta por fuente queda abierta: el Boletín Oficial publica todos los días hábiles y el INDEC según su calendario de difusión, así que no todas necesitan la misma frecuencia. Es afinamiento, no arquitectura.

## Flujo de información

Ver `flujo-informacion.drawio`. Es un diagrama de actividad UML con cinco calles —extensión, orquestador, módulos, base de datos y servicios externos— y su elemento central es la bifurcación que separa los dos flujos.

El recorrido tiene dos entradas y una sola salida. La entrada automática es un tuit que aparece en el área visible; la entrada a demanda es un clic sobre un indicador ya pintado. Ambas convergen en la misma pregunta —si existe un análisis vigente en caché— y recién después se separan según el origen del pedido. La rama automática ejecuta únicamente el Módulo 1 y tiene que resolverse en 2 segundos; la rama a demanda ejecuta los Módulos 2, 3 y 4 y dispone de 8.

Dentro de la rama a demanda, el Módulo 2 y el Módulo 3 corren **en paralelo**, dibujados con una bifurcación y una unión. No es una licencia del dibujo: son independientes —el uno evalúa la cuenta y el otro la afirmación, y ninguno necesita el resultado del otro— y el Módulo 4 espera a ambos. Modelarlos en cadena sugeriría una dependencia que no existe y haría parecer que la latencia de los dos se suma cuando en realidad se solapa.

Dentro del Módulo 3 el orden de las tres consultas no es casual: primero la fuente oficial —resuelta contra el índice local y no contra el sitio—, después los medios de referencia, y solo entonces los verificadores, dibujados con línea punteada. Del nodo de medios salen dos aristas hacia la evaluación de postura: una pasa por los verificadores y la otra los saltea. La segunda es el camino frecuente, y que esté dibujada es lo que deja constancia de que la ausencia de una verificación previa no degrada el resultado.

Hay dos puntos de persistencia, no uno. Tras el Módulo 1 se guardan el tuit y su `score_nlp`; tras el Módulo 4, el análisis completo con su evidencia y la versión de modelo que lo produjo. El segundo es lo que hace reproducible un veredicto meses más tarde, que es una exigencia del trabajo experimental de la Entrega 5.

El camino de excepción desemboca en un nodo de análisis parcial que alimenta igual al Módulo 4. La alternativa —devolver error, o promediar sobre lo que haya sin avisar— produce en un caso una pérdida de trabajo ya hecho y en el otro un veredicto peor sin que nadie lo sepa.

## Secuencia

Dos diagramas en lugar de uno, por la misma razón por la que RNF-01 y RNF-02 son números distintos: son dos recorridos con actores, costos y techos de latencia diferentes, y superponerlos en un solo dibujo con fragmentos anidados los vuelve ilegibles sin explicar nada más.

**`secuencia-cu01.drawio` — flujo automático.** Seis líneas de vida. El mensaje que importa es el que va del *service worker* a la API: es uno por lote de tuits visibles, no uno por tuit. Un fragmento `alt` separa el acierto de caché, que retorna dentro de los 300 milisegundos, del recorrido completo contra el servicio de inferencia. Un fragmento `opt` cubre el fallo de la inferencia, y su resolución es deliberadamente silenciosa: no se pinta indicador y no se muestra error, porque el usuario no pidió nada y un aviso de fallo sobre un tuit que apenas pasó por pantalla sería ruido. Lo que vuelve es una **señal de prioridad del texto, no un veredicto** (#92); en el prototipo la señal no se persiste.

**`secuencia-cu02.drawio` — flujo a demanda.** Diez líneas de vida, con el Módulo 3 abierto en sus tres fuentes. La llamada a los verificadores está dentro de un `opt` y el retorno del Módulo 3 ocurre igual cuando ese fragmento no se ejecuta. El fragmento `alt` del final es el de degradación: si alguna fuente externa no respondió, el Módulo 4 recibe los *scores* disponibles junto con la marca de parcial, y esa marca viaja hasta la pantalla.

La nota sobre el *content script* del primer diagrama registra una restricción que ningún otro artefacto dejaba escrita: como corre en el hilo de la página, el techo de 50 milisegundos de RNF-04 aplica solo a él. Leer el DOM e inyectar el indicador es todo lo que puede hacer; agrupar pedidos, custodiar el UUID y hablar con la API tienen que ocurrir en el *service worker*.

## Despliegue y arquitectura de red

Ver `despliegue-red.drawio`. Cubre a la vez el diagrama de arquitectura que pide el criterio 6 y la arquitectura de red del criterio 5. Está organizado en cinco zonas ordenadas por grado de control:

| Zona | Qué contiene | Control |
|---|---|---|
| Equipo del ciudadano | Chrome con la extensión y el almacenamiento local con el UUID anónimo | Ninguno |
| Organización cliente B2B | El sistema que consume la API y el navegador del analista | Ninguno |
| Borde CDN — Vercel | Panel web estático, TLS terminado en el borde | Configuración |
| Nube de la aplicación — Railway `eu-west` | Contenedor FastAPI con la base SQLite como archivo de un volumen en `/data`, sin puerto de base de datos | Total |
| Terceros | Inferencia, búsqueda web, fuentes oficiales, medios, verificadores y proveedor de identidad | Ninguno |

Tres de las cinco zonas están fuera de todo control del proyecto. Enunciado así, RNF-11 deja de parecer una cláusula de estilo: la degradación a análisis parcial es la consecuencia directa de que el sistema dependa de siete servicios ajenos.

Lo que vuelve útil a este diagrama no son los nodos sino lo que marca en los cruces de límite, porque es donde el argumento legal deja de ser un párrafo y se vuelve visible:

- **Extensión hacia la API.** Sale el texto del tuit y el `@` del autor en claro. Es el dato de tercero amparado en el art. 5 inc. 2 ap. a) de la Ley 25.326, que exime del consentimiento a los datos obtenidos de fuentes de acceso público irrestricto. El límite del amparo también está declarado: no alcanza a cuentas protegidas ni a mensajes directos.
- **API hacia el servicio de inferencia.** El texto del tuit sale hacia un tercero. Conviene que esté dibujado y no escondido detrás de una caja rotulada *modelo*.
- **API hacia las fuentes de evidencia.** Sale la afirmación extraída, no el tuit crudo. Es una diferencia real de exposición y por eso se dibuja distinto.
- **API hacia el cliente B2B.** Es la única arista que transporta datos hacia afuera del sistema, y es una cesión en los términos del art. 11. Por eso sale agregada o con la cuenta autora anonimizada. Que esa mitigación sea RF-15 con prioridad imprescindible, y no una buena intención, es lo que la vuelve verificable.
- **API con la base de datos.** SQLite es un archivo del volumen del propio contenedor: no hay puerto de base de datos ni credencial que circule por la red.

## Decisiones de arquitectura

| Decisión | Alternativas evaluadas | Por qué |
|---|---|---|
| Análisis en dos flujos, uno automático y barato y otro a demanda y caro | Todo automático; todo a demanda | Todo automático no se sostiene en costo ni en latencia; todo a demanda le quita a la extensión su razón de ser, que es avisar sin que se lo pidan |
| Inferencia en Hugging Face, separada de la API | Cargar el modelo en el mismo contenedor | Un *transformer* de ~125M parámetros residente consume memoria de forma continua y quema el crédito mensual de Railway en días; bajo demanda se paga por invocación. El techo es RNF-14 y no una hoja de especificaciones |
| Backend en Railway | Render Starter (7 USD, sin base incluida), Fly.io Hobby (sin base, más configuración) | PostgreSQL incluido y servicio *always-on*. Los planes gratuitos que se duermen rompen una extensión que llama en tiempo real |
| `pgvector` sobre el mismo PostgreSQL | Qdrant, Pinecone | Implementa HNSW igual que un motor dedicado. La ventaja de los dedicados aparece arriba del millón de vectores; el prototipo tendrá decenas de miles. Costo adicional cero y un servicio menos en el despliegue |
| Panel web estático en Vercel, separado del backend | Servir el panel desde la misma API | No requiere cómputo; separarlo lo hace gratis y saca tráfico del contenedor pago |
| Identidad en dos niveles: ciudadano anónimo, B2B autenticado | Cuenta única para todos; sin cuentas | El ciudadano no necesita cuenta y no tenerla elimina el tratamiento de datos personales del usuario (RNF-08). El B2B la necesita porque hay un plan y una cuota que cobrar |
| Autenticación B2B delegada a un proveedor externo | Usuarios y contraseñas propios | Evita almacenar y rotar contraseñas, y quita superficie de seguridad sin perder nada |
| Degradación a análisis parcial | Reintentar hasta obtener todos los módulos; devolver error | Reintentar rompe RNF-02; devolver error desperdicia los módulos que sí respondieron. La tercera vía es informar qué falta (RNF-11) |
| Fuentes oficiales pre-indexadas por una tarea programada | Consultarlas en vivo dentro de la petición; un planificador dentro del proceso de FastAPI | `argentina.gob.ar` declara `Crawl-delay: 10` y RNF-02 da ocho segundos: una petición cada diez no entra en ese presupuesto. Un planificador dentro de FastAPI habría metido esas esperas en el mismo proceso que tiene que cumplir RNF-01 |

## Lo que este nivel de detalle no resuelve todavía

No están definidos el esquema de reintentos y *timeouts* por servicio externo, ni la política de expiración del caché, ni la periodicidad exacta de la ingesta por fuente, ni cómo se versiona el contrato de la API B2B. Los cuatro son decisiones de implementación que corresponden a la Entrega 4 y que hoy no bloquean ningún criterio de la rúbrica.

## Módulo 2 en el prototipo (2026-10-08)

Regla fija, sin entrenamiento (`prototipo/servicio/app/credibilidad.py`):

```
credibilidad = 0,35·antigüedad + 0,30·seguidores + 0,20·relación + 0,15·verificada
antigüedad = min(días / 730, 1)              # satura a los 2 años
seguidores = min(log10(seg + 1) / 5, 1)      # satura en 100 000
relación   = min(seg / (seguidos + 1), 1)
verificada = 1 con insignia, 0,5 sin ella    # la insignia se compra
```

- **Peso en el veredicto:** 0,10 (clasificador 0,25, contraste 0,65; `pesos-v3`). Pesa poco porque se juzga la afirmación y no a quien la publica: la trayectoria de la cuenta aporta contexto, no prueba.
- **Origen de los datos:** un guion de la extensión en el mundo de la página (`extension/src/pagina/`) lee el objeto del autor de las propiedades de React del tuit en pantalla (`__reactFiber$…`), a pedido del *content script* con un evento síncrono del DOM. **Sin pedidos propios**: se sostiene el argumento de [[restricciones-legales-eticas]] y no suma latencia (RNF-02; 3 ms para 9 tuits). Probado en x.com con sesión el 2026-10-08: 13 de 13 tuits distintos con el autor correcto.
- **Descartado:** interceptar `/i/api/graphql/`. En 2026 el *timeline* llega por `POST /i/api/1.1/flow/timeline.json` con cuerpo vacío, y los datos no pasan por ahí.
- **Sin datos:** el módulo devuelve `null` y el combinador lo excluye, repartiendo su peso entre los otros dos en la misma proporción.
- **Evaluación:** el sistema con `pesos-v4` (0,25 / 0,10 / 0,65) obtuvo F1 macro 0,712 (IC 0,61–0,80) sobre 94 tuits; el módulo intervino en 88. Su aporte aislado no tiene medición propia (cap. 4 y conclusiones).

## Memoria semántica de evidencia en el Módulo 3 (2026-10-22, PRD #100)

- **Qué es:** adaptador `MemoriaDeEvidencia` (`prototipo/servicio/app/proveedor/memoria.py`) que envuelve al LLM con el puerto `ProveedorDeAnalisis`, dentro del proveedor compuesto. Compara el **texto de la publicación** (no la afirmación: extraerla ya es la llamada que se quiere evitar) con `paraphrase-multilingual-MiniLM-L12-v2` (384 dim., `POST /embeber` del contenedor del clasificador) y `sqlite-vec` sobre el mismo SQLite del histórico (k=1, coseno).
- **Acierto:** similitud ≥ 0,95, mismas cifras en los dos textos (guarda numérica) y evidencia de ≤ 7 días. Se reutilizan afirmación y fuentes con postura; clasificador, credibilidad, combinador y justificación se recalculan.
- **Escritura y fallas:** solo análisis completos con afirmación y fuentes admitidas. Embebedor o almacén caídos → búsqueda web, sin marcar parcial.
- **Mediciones** (`prototipo/mediciones/memoria-2026-10-22.txt`): 62 pares sobre 31 titulares de la prueba de FakeDeS; precisión 0,938 y cobertura 0,484 (sin guarda: 0,593 y 0,516). Acierto: mediana 30 ms, p95 40 ms (local, por HTTP de extremo a extremo) contra 8,46 s y 15,97 s de la búsqueda. Costo evitado ≈ 0,0246 USD (estimación). RNF-02 se cumple solo en los aciertos.
- **Pendiente:** Railway no incluye la memoria. El índice local de fuentes oficiales se construyó después (2026-10-26, ver la sección siguiente). Documento: cap. 4 (4.2.5, alcance implementado, modelo de datos, mediciones), resumen, abstract y conclusiones (#104).

## Índice de fuentes oficiales en el Módulo 3 (2026-10-26, PRD #107)

- **Qué es:** `IndiceDeFuentes` (`prototipo/servicio/app/proveedor/indice.py`) sobre el mismo SQLite del histórico: tablas `fuente_oficial`, `documento` (una fila por fragmento) y `documento_vector` (`sqlite-vec`, 384 dim., coseno). Comparte el embebedor con la memoria semántica (`paraphrase-multilingual-MiniLM-L12-v2`, `POST /embeber`); el cliente memoriza el último texto, así que hay un solo `/embeber` por análisis.
- **Consulta:** dentro del adaptador del LLM (`proveedor/openai.py`), no del puerto: un acierto de la memoria ni llega a consultarlo. Se buscan los **3 fragmentos** más cercanos al texto de la publicación y entran los de similitud **≥ 0,60** en un bloque `<documentos_oficiales>` del mensaje, escapados contra *prompt injection*. El LLM los devuelve en `fuentes` como una fuente más, con su postura. Si el índice falla, está vacío o nada supera el umbral, el análisis sigue sin el bloque y sin marcarse parcial; el registro anota `indice | fragmentos=N | similitud=… | motivo=…`.
- **Ingesta** (`prototipo/servicio/app/ingesta.py`): cinco fuentes, cada una con su descubridor:
  - INDEC: informes técnicos por tema, a partir del `sitemap.xml`;
  - BCRA: `sitemap_index.xml` sin las páginas en inglés;
  - Salud y Educación: rutas `/salud` y `/educacion` del sitemap de `argentina.gob.ar` (sin `/noticias/`);
  - Boletín Oficial: listado de la primera sección de cada día (no tiene sitemap).

  Ventana de **90 días**, tope de **200 documentos** por fuente y corrida, HTML (`html.parser`) y PDF (`pypdf`), fragmentos de **45 palabras** (el modelo trunca a 128 *tokens*). Al final purga lo vencido y anota la corrida.
- **Rastreo (RNF-17):** reglas del grupo `*` de `robots.txt` con comodines y la regla más larga como ganadora (RFC 9309), aplicadas a todo pedido; demora declarada o 1 s, la mayor; redirecciones seguidas a mano para que cada salto pase por robots y demora; un **429 corta la fuente** hasta la corrida siguiente. User-Agent propio (`Factum-ingesta/1.0`), no de navegador.
- **Disparo (#111):** `POST /ingesta` con `X-Secreto-Administrador` (401 sin él, 202 al lanzar, 409 si hay una corrida) lanza `python -m app.ingesta` en un **subproceso del contenedor de la API**, porque los volúmenes de Railway no se comparten entre servicios. Una corrida a la vez por `flock` sobre `<base>.ingesta`. Lo llama un servicio cron aparte, `0 6 * * *` UTC (pasos en `prototipo/README.md`).
- **Carga del 2026-10-25/26 (local):** 779 documentos y 15 756 fragmentos: Salud 385, Boletín Oficial 200, BCRA 100, Educación 66, INDEC 28. La base está versionada en `prototipo/servicio/datos/indice-medicion.sqlite3`.
- **Medición:** ver [[wiki/experimentos/mediciones-rnf]] (#112).
- **Huecos:**
  - faltan los PDF de publicaciones del BCRA (`page-sitemap.xml` da *timeout*) y las noticias de los ministerios;
  - el Boletín solo cubre desde el 13/10, por el corte ante 429;
  - InfoLEG no está.

## Referencias cruzadas

- [[wiki/solucion/requerimientos]]
- [[wiki/solucion/mockups]]
- [[wiki/solucion/metodologia-tecnica]]
- [[wiki/solucion/modelo-datos]]
- [[wiki/solucion/tecnologias]]
- [[wiki/proyecto/recursos]]
- [[wiki/proyecto/plan-bloque-diseno]]
- [[wiki/negocio/modelo-de-negocio]]
