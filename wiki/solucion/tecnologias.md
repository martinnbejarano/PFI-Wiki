---
titulo: Tecnologías y Servicios
tipo: análisis
tags: [tecnologias, stack, versiones, red, tls, criterio-5]
fuentes: [Rubrica-EP2-50porciento.pdf]
actualizado: 2026-10-20
---

# Tecnologías y Servicios

## Stack construido (*as-built*, 2026-10-20)

> Esta sección manda. Lo que sigue a partir de «Panorama por capa» es el **diseño original** (2026-08/09): React + Vercel, PostgreSQL + pgvector, Hugging Face Space, ingesta programada, Google Identity, Tavily. Nada de eso se construyó. Se conserva como registro de decisiones. Fuente de la justificación: `documento/chapters/chapter04.tex`, sección «Tecnologías utilizadas» (#70).

| Capa | Tecnología | Versión | Por qué |
|---|---|---|---|
| Extensión | TypeScript + Vite, Node.js para construir | 7.0.2 · 8.2.1 · 24.19.0 | Sin cambios respecto del diseño |
| API | Python | **3.13** (`servicio/.python-version`) | Mismo lenguaje y versión que el entrenamiento (`transformers`/`torch`); un solo lenguaje para un equipo de una persona. El diseño decía 3.14.7; la 3.13 también cumple el criterio de vigencia |
| | FastAPI + Uvicorn + Pydantic (+ pydantic-settings) | 0.141.1 · 0.52.1 · 2.13.4 · 2.15.0 | Validación Pydantic en la frontera de confianza; OpenAPI automática para la API B2B (RF-13); los manejadores `def` corren en un grupo de hilos, así que la espera del LLM no bloquea caché ni `/senales` (`FastAPI2026`) |
| | SDK de OpenAI | 3.3.1 | Cliente del LLM |
| Panel web | HTML generado por la API | — | No hay Vercel ni React: un despliegue menos y CSP sin JS |
| Datos | SQLite (`sqlite3` de la biblioteca estándar) en el volumen `/data` | — | Una instancia, escritura baja, cero administración. **Techo:** un escritor por archivo (`SQLite2026`); varias instancias exigen PostgreSQL → trabajo futuro |
| Clasificador | Python 3.13, PyTorch 2.14.0 CPU, Transformers 5.17.0, FastAPI | — | BETO (FakeDeS → Chequeado). Segundo servicio de Railway, red privada, pesos del repo privado de HF al arrancar |
| LLM | `gpt-5.6-luna` (OpenAI) con `web_search` filtrado por dominios | — | Escalón más barato (0,20/1,20 USD por M de fichas, `OpenAI2026`), salida estructurada y búsqueda con `allowed_domains`. 2 llamadas por análisis, 0,0044 USD en fichas, mediana 11,1 s. Autoalojado: GPU continua (T4 0,50 USD/h) muy por encima de RNF-14 y sin búsqueda web |
| Despliegue | Railway `eu-west` (Ámsterdam) | — | UE = legislación adecuada (Disposición 60-E/2016, art. 3) para el art. 12 de la Ley 25.326; red privada; `make desplegar` por CLI; cobro por uso (10 USD/GB RAM/mes, 20 USD/vCPU/mes, `RailwayPrecios2026`) |

**Costo (RNF-14, umbral 14 USD/mes de infraestructura).** API ≈ 1 USD/mes (64 MB, CPU ociosa, volumen 85 MB). Clasificador encendido ≈ 1,23 GB estable → ≈ 12 USD/mes. Con ambos ≈ 13 USD/mes, sin margen.

**Decisión (autor, 2026-10-19): BETO apagado por defecto.** Se enciende solo para demos y mediciones: `make beto-encender` / `make beto-apagar` (`prototipo/Makefile`, commit 984fc9d), que cambian a la vez la escala del servicio `clasificador` y `ADAPTADOR` de la API. Apagado: `ADAPTADOR=llm`, el Módulo 1 del análisis profundo lo puntúa el LLM y `/senales` no devuelve señales (el flujo automático no muestra nada). Todas las mediciones del Módulo 1 y del flujo automático se hicieron con BETO encendido.

Cubre el **criterio 5** de la rúbrica de EP2 completo, incluida la parte de *arquitectura de red*. Es una página **técnica**: lenguajes, *frameworks*, versiones, librerías y el porqué de cada elección. Los costos viven en [[wiki/proyecto/recursos]] y no se repiten acá; donde hace falta, se enlaza.

**Todas las versiones están fijadas y verificadas contra el registro de paquetes o el sitio del proyecto el 2026-08-10.** Fijarlas importa por una razón concreta: un PFI se desarrolla a lo largo de un año y una dependencia que llega a fin de vida a mitad de camino es un riesgo de cronograma, no un detalle de instalación.

## Panorama por capa

| Capa | Tecnología | Versión | Por qué |
|---|---|---|---|
| **Extensión** | TypeScript sobre Chrome Manifest V3 | TS 7.0.2 | El tipado paga solo en el *content script*, que manipula un DOM ajeno y cambiante; el error de forma se ve al compilar y no en la demo |
| | Vite (empaquetado multi-entrada) | 8.2.1 | Ya hace falta para el panel: extenderlo a la extensión no suma herramienta |
| **Panel web** | React | 19.2.8 | Confirma lo que la arquitectura ya declaraba; ecosistema conocido por quien escribe el código |
| | Vite | 8.2.1 | *Build* estático, sin servidor |
| | Recharts | 3.10.1 | Gráficos de RF-14 sobre componentes de React, sin manipular el DOM por fuera |
| | Node.js (solo para construir) | 24.19.0 LTS activo | No corre en producción: el despliegue es HTML, CSS y JavaScript estáticos |
| **API** | Python | 3.14.7 | Ver la nota sobre la versión más abajo |
| | FastAPI | 0.141.1 | Validación y documentación de la API derivadas del tipado, que es lo que hace barato el contrato B2B de RF-13 |
| | Uvicorn | 0.52.1 | Servidor ASGI de FastAPI |
| | Pydantic | 2.13.4 | Esquemas de entrada y salida; es de donde sale la especificación de la API |
| | SQLAlchemy | 2.0.51 | Acceso a la base desde los repositorios |
| | psycopg | 3.3.4 | Controlador de PostgreSQL |
| | httpx | 0.28.1 | Cliente HTTP asíncrono hacia inferencia, búsqueda y fuentes |
| **Ingesta programada** | El mismo tiempo de ejecución de la API | | Es el mismo repositorio y las mismas entidades; no es un servicio con vida propia |
| | BeautifulSoup | 4.15.0 | Extracción del texto de los documentos oficiales |
| **Base de datos** | PostgreSQL | 16.14 | Serie soportada hasta el 2028-11-09, que cubre el PFI entero |
| | pgvector | 0.8.6 | Índice HNSW sobre las columnas `vector(768)` |
| | Alembic | 1.19.1 | Migraciones versionadas del esquema |
| **Inferencia** | Clasificador propio en un Hugging Face Space (CPU) | — | Módulo 1. El modelo sale de la comparación de cinco (ver [[pruebas]]); XLM-T es el candidato principal |
| | LLM de terceros | — | Extracción de la afirmación y su tipo (RF-04), recuperación de evidencia (RF-05) y justificación (RF-06) |
| | `intfloat/multilingual-e5-base` sobre Hugging Face | 768 dimensiones, MIT | Codificador de los *embeddings* de `claim` y `documento` |
| **Identidad B2B** | OAuth 2.0 / OIDC con Google Identity | — | Ver la sección de identidad |
| **Experimentación** | `transformers` · `tokenizers` · `sentencepiece` · `torch` · `scikit-learn` · spaCy | 5.15.0 · 0.23.1 · 0.2.2 · 2.13.0 · 1.9.0 · 3.8.15 | **No se despliegan.** Ver la nota siguiente |
| **Pruebas** | pytest | 9.1.1 | Ver [[wiki/solucion/pruebas]] |

**Las librerías de *transformers* no viajan al servidor.** Es la consecuencia más importante de la tabla y conviene enunciarla: `transformers`, `torch` y `sentencepiece` viven en el entorno de experimentación —ajuste fino, evaluación y construcción del corpus— y **no forman parte de la imagen que se despliega**. El contenedor de la API habla con Hugging Face por HTTP y su única dependencia de red es `httpx`. Meter el *transformer* dentro del contenedor sería deshacer la separación que sostiene todo el presupuesto de infraestructura.

**Python 3.14 y no 3.10.** FastAPI exige `>=3.10` y el presupuesto no fija número, pero **3.10 llega a fin de vida en octubre de 2026**: comprometerse con ella sería comprometerse con algo que muere durante el PFI. La versión elegida cubre el desarrollo, la entrega final y el período posterior.

## Dos límites de plataforma que el wiki tenía mal

No son decisiones sino hechos verificables, y están acá porque de cada uno depende un argumento que el documento sostiene. La versión anterior de ambos era comprobable y falsa.

### El plan Hobby de Railway no tiene un tope de 512 MB de RAM

El wiki lo afirmaba en cuatro lugares. El plan vigente son **USD 5 mensuales con USD 5 de crédito de uso**, con facturación por consumo y hasta 48 vCPU y 48 GB por servicio. No hay techo de memoria.

Importa porque sobre ese número se apoyaba **toda la justificación de por qué la inferencia no corre en el mismo servidor que la API**. La conclusión no cambia; la premisa sí, y la premisa anterior era verificable y falsa. El argumento correcto es de **presupuesto y no de memoria**: un contenedor con un *transformer* de unos 125 millones de parámetros residente consume memoria de forma continua y quema el crédito mensual en días, mientras que la inferencia bajo demanda se paga por invocación. El techo que decide es RNF-14, no una hoja de especificaciones.

### El plan Hobby de Vercel prohíbe el uso comercial

La documentación vigente restringe ese plan a uso personal y no comercial. El panel es exactamente donde vive RF-14, la vista de tendencias para organizaciones con plan y cuota.

**Se resuelve con el mismo corte prototipo/producto que el proyecto ya aplica en otras dos decisiones:** durante el PFI el panel **no presta servicio comercial**, porque no hay cliente, no hay facturación y no hay suscripción. El plan de pago corresponde a la explotación comercial, que está fuera del alcance. Lo que hay que escribir en el presupuesto no es un cero a secas —un cero sin explicación es lo que hace que un evaluador abra la página de precios— sino la cláusula y el corte.

## Decisiones con alternativa real

Solo se documentan las elecciones donde hubo una alternativa que se evaluó y se descartó por un criterio explícito. Las demás están en la tabla de arriba con su justificación en una línea.

### React sobre Vite, no Next.js

Next.js trae renderizado en servidor y funciones sin servidor que ni RF-10 ni RF-14 piden, y ata el panel a un proveedor justo donde la restricción de uso comercial podría obligar a mudarlo. El panel es una aplicación estática: tablas, texto y dos gráficos.

**Los costos, escritos y no escondidos.** El marcado de los *mockups* —28 KB, sin dependencias externas— hay que portarlo a JSX en lugar de reutilizarlo tal cual, lo que relativiza la promesa de que la extensión y el panel heredan el marcado del *mockup*. Y se envía el tiempo de ejecución de React a pantallas que son tablas y texto. Son costos aceptados a cambio de un ecosistema conocido por quien va a escribir el código solo, y de no tener que corregir la arquitectura ya publicada.

### La ingesta corre como tarea programada de Railway, no dentro de FastAPI

Un servicio programado arranca, recorre el catálogo de fuentes respetando el `crawl-delay` de cada sitio, inserta los documentos, actualiza la fecha de la última corrida y termina. Railway lo soporta de forma nativa, con intervalo mínimo de cinco minutos, en UTC, y saltea la corrida siguiente si la anterior sigue viva, que es exactamente el comportamiento que hace falta.

- Respeta el `Crawl-delay: 10` de `argentina.gob.ar` **fuera del camino crítico**, que es el motivo por el que la consulta salió de la petición del usuario.
- No agrega un servicio siempre encendido compitiendo por el crédito mensual: se paga solo el tiempo de ejecución.
- Es una fila más en el diagrama de despliegue, no una arquitectura nueva.

Se descartó un planificador dentro del proceso de FastAPI, que habría metido esperas de diez segundos en el mismo proceso que tiene que cumplir RNF-01 y RNF-02. Y se descartó un planificador externo al proveedor, que obligaba a exponer la base a internet o a construir un *endpoint* de ingesta autenticado: una superficie más que asegurar para ahorrar un costo ya cubierto.

### `multilingual-e5-base` para los *embeddings*, con 768 dimensiones

Verificado contra el archivo de configuración del modelo: `hidden_size` 768, arquitectura `XLMRobertaModel`, licencia MIT. Es el número que fija las columnas `vector(768)` de [[wiki/solucion/modelo-datos]], y cambiarlo obliga a reindexar.

Tres argumentos, en orden:

1. **No suma un sistema externo.** Hugging Face ya está en el despliegue y ya se paga para el clasificador. Cargar el codificador dentro del servicio de ingesta habría vuelto a abrir el argumento de memoria que la corrección de más arriba dejó mal parado.
2. **Es de la misma familia que el clasificador.** `XLMRobertaModel` es la arquitectura sobre la que también se construye XLM-T. Un solo *tokenizer* multilingüe y un solo criterio de preprocesamiento.
3. **768 es el punto medio entre calidad y tamaño del índice** para las decenas de miles de vectores que proyecta la arquitectura. Un codificador de 1.024 dimensiones habría engordado el índice HNSW en torno a un tercio sobre una base con presupuesto ajustado.

### `pgvector` sobre el mismo PostgreSQL, no un motor vectorial dedicado

Ya estaba decidido en [[wiki/solucion/arquitectura]] contra Qdrant y Pinecone: implementa HNSW igual que un motor dedicado, la ventaja de los dedicados aparece arriba del millón de vectores y el prototipo tendrá decenas de miles. Costo adicional cero y un servicio menos en el despliegue. Acá solo se le pone versión.

**PostgreSQL 16 es una elección deliberada y no una herencia.** Las plantillas actuales del proveedor con `pgvector` traen la serie 18. La 16 está soportada hasta el 2028-11-09, cubre el PFI entero con margen y es la que la arquitectura ya declaraba. La instancia hay que verificar que efectivamente sea 16 en lugar de heredar lo que la plantilla ponga.

### TypeScript en la extensión, y un solo empaquetador

Con React el panel necesita Vite de todos modos, así que la cadena de herramientas ya existe y extenderla a la extensión es barato. El tipado paga sobre todo en el *content script*, que es el componente que lee un DOM ajeno, no versionado y que cambia sin aviso: una propiedad que desaparece se ve como error de compilación en lugar de como indicador que no se pinta durante la demostración.

El empaquetado usa **Vite con varias entradas** —*content script*, *service worker* y *popup*—, con el manifiesto de Manifest V3 mantenido a mano. Se descartó agregar un complemento específico para extensiones: son tres entradas y un archivo JSON, y una dependencia más en la cadena de construcción es una cosa más que puede romperse a doce días de la entrega.

### Recharts para los gráficos de RF-14

La evolución temporal de RF-14 es una serie de líneas y un par de barras. Recharts se declara como componentes de React y no exige manipular el DOM por fuera del ciclo de vida del *framework*, que es el problema real de envolver una librería imperativa. Se descartó Chart.js, que dibuja sobre `canvas` y obliga a mantener una referencia y a sincronizar el ciclo de vida a mano para ganar un rendimiento que dos gráficos no necesitan.

### Alembic para las migraciones

El esquema de [[wiki/solucion/modelo-datos]] tiene diecisiete entidades y va a cambiar durante el desarrollo. Alembic es el compañero natural de SQLAlchemy y deja las migraciones versionadas en el repositorio, que es lo que permite reconstruir la base desde cero y lo que evita que el esquema real y el documentado se separen.

### Identidad B2B: OAuth 2.0 / OIDC con Google Identity

La arquitectura decía «delegada a un proveedor externo» sin nombrarlo, y un documento no puede dejar así una pieza del *stack*. El proveedor es **Google Identity**, con OAuth 2.0 y OpenID Connect, que es lo que la decisión de producto sobre identidad ya había fijado en el plan del bloque de diseño.

Tres razones: **no agrega costo**, y por lo tanto no toca RNF-14; evita almacenar y rotar contraseñas, que es superficie de seguridad que se elimina en lugar de asegurarse; y el `subject` que devuelve es exactamente lo que `usuario_b2b.subject_idp` guarda.

Se descartaron las plataformas de identidad como servicio —del tipo Auth0, Clerk o WorkOS— no por capacidad sino por precio y por alcance: sus planes gratuitos alcanzan para un prototipo, pero el momento de elegir una es cuando exista un cliente que pida inicio de sesión único corporativo, y eso es funcionalidad de entregas posteriores. El ciudadano **no se autentica** y esta pieza no lo toca.

## Arquitectura de red

Fuente: `wiki/assets/diagramas/despliegue-red.drawio`, exportado a `documento/chapters/figures/despliegue-red.png`. El diagrama está organizado en cinco zonas ordenadas por grado de control, y lo que lo vuelve útil no son los nodos sino lo que marca en los cruces de frontera.

| Zona | Qué contiene | Control |
|---|---|---|
| 1 · Equipo del ciudadano | Chrome con la extensión y el almacenamiento local con el UUID | Ninguno |
| 2 · Organización cliente B2B | El sistema que consume la API y el navegador del analista | Ninguno |
| 3 · Borde CDN | Panel web estático, con TLS terminado en el borde | Configuración |
| 4 · Nube de la aplicación | Contenedor de la API, base de datos y tarea programada de ingesta, unidos por red privada | Total |
| 5 · Terceros | Inferencia, búsqueda web, fuentes oficiales, medios, verificadores y proveedor de identidad | Ninguno |

**Protocolos y cifrado.** Todo el tráfico entre zonas viaja sobre HTTPS con TLS 1.3, conforme RNF-12. El panel se sirve desde el borde con certificado gestionado por la plataforma; la API expone un único origen HTTPS y no acepta tráfico en claro. La comunicación entre la API, la tarea de ingesta y la base de datos ocurre **dentro de la red privada** del proveedor: la base no expone puerto público a internet y no hay credencial de base de datos viajando por la red pública.

**Autenticación por frontera.** La extensión no se autentica: envía su UUID y nada más, y ese es el motivo por el que existe la postura del art. 2 del apartado legal. El cliente B2B se autentica con una clave de API que la base guarda **hasheada** (RNF-12), con un prefijo en claro que permite identificarla y revocarla sin conservar el secreto. El analista B2B se autentica contra el proveedor de identidad y nunca contra la API.

**Qué cruza cada frontera, que es donde el argumento legal se vuelve visible:**

- **Extensión hacia la API.** Sale el texto del tuit y el `@` del autor en claro. Es el dato de tercero amparado por el art. 5 inc. 2 ap. a), con su límite declarado: no alcanza a cuentas protegidas ni a mensajes directos.
- **API hacia el servicio de inferencia.** El texto del tuit sale hacia un tercero. Conviene que esté dibujado y no escondido detrás de una caja rotulada *modelo*.
- **API hacia las fuentes de evidencia.** Sale la **afirmación extraída**, no el tuit crudo. Es una diferencia real de exposición y por eso se dibuja distinto.
- **Ingesta hacia los sitios oficiales.** Sale una petición de lectura sin ningún dato de usuario, espaciada según el `crawl-delay` de cada destino (RNF-17).
- **API hacia el cliente B2B.** Es la única arista que transporta datos hacia afuera del sistema. Es una cesión en los términos del art. 11 y por eso sale agregada o con la cuenta autora anonimizada (RF-15, RNF-10).

El detalle legal de cada cruce está en [[wiki/proyecto/restricciones-legales-eticas]].

## Librerías del *pipeline* de lenguaje natural

Coherentes con [[wiki/solucion/pipeline-preprocesamiento]], y con la separación de arriba: estas librerías son del entorno de experimentación.

| Librería | Versión | Para qué |
|---|---|---|
| `transformers` | 5.15.0 | Carga del modelo, ajuste fino y evaluación |
| `tokenizers` | 0.23.1 | Implementación del tokenizador; llega como dependencia de `transformers` |
| `sentencepiece` | 0.2.2 | XLM-T hereda de XLM-RoBERTa el tokenizador SentencePiece con vocabulario Unigram de 250.000 piezas, no WordPiece |
| `torch` | 2.13.0 | Tiempo de ejecución del entrenamiento |
| `scikit-learn` | 1.9.0 | Línea base de TF-IDF con regresión logística (RNF-05) y las métricas de evaluación |
| spaCy | 3.8.15 | Previsto para el extractor de afirmaciones (RF-04); el prototipo usa un LLM para esa tarea |

**El preprocesamiento es deliberadamente flaco, y eso es una decisión y no una omisión.** Se normalizan las URLs y las menciones, se segmentan los *hashtags*, y **todo lo demás se conserva**: emojis, mayúsculas, signos repetidos y números. XLM-T fue pre-entrenado sobre unos 198 millones de publicaciones donde esos elementos estaban presentes, así que borrarlos produce una distribución de entrada que el modelo nunca vio. Y en esta tarea en particular son **la señal**: el Módulo 1 clasifica registro sensacionalista, no contenido factual. La justificación completa, incluida la razón por la que los números no se reemplazan por un símbolo genérico, está en [[wiki/solucion/pipeline-preprocesamiento]].

## Servicios contratados

Sin cifras: el detalle de costos, planes y alternativas evaluadas está en [[wiki/proyecto/recursos]].

| Servicio | Para qué | Plan |
|---|---|---|
| Railway | API, base de datos y tarea de ingesta | Hobby |
| Vercel | Panel web estático | Hobby, con el corte prototipo/producto de más arriba |
| Hugging Face | Inferencia del clasificador y del codificador de *embeddings* | Pro |
| Tavily | Búsqueda web sobre los medios de referencia | Gratuito |
| Google Identity | Autenticación B2B | Sin costo |

## Lo que este nivel de detalle no resuelve

**La política de vigencia del caché.** La columna que la implementa existe y queda nulable; el criterio que la puebla se difiere a la Entrega 4. Es una decisión de producto, no de tecnología.

**El esquema de reintentos y tiempos límite por servicio externo**, y el versionado del contrato de la API B2B. Son decisiones de implementación que no bloquean ningún criterio de la rúbrica.

**La plataforma de identidad como servicio**, si alguna vez hace falta inicio de sesión único corporativo. La decisión de arriba cubre el prototipo; la de producto se toma cuando exista el cliente que la pida.

## Referencias cruzadas

- [[wiki/solucion/arquitectura]]
- [[wiki/solucion/modelo-datos]]
- [[wiki/solucion/requerimientos]]
- [[wiki/solucion/pipeline-preprocesamiento]]
- [[wiki/solucion/metodologia-tecnica]]
- [[wiki/solucion/pruebas]]
- [[wiki/proyecto/recursos]]
- [[wiki/proyecto/restricciones-legales-eticas]]
- [[wiki/negocio/analisis-financiero]]

## Fuentes

- [[raw/clases/Rubrica-EP2-50porciento.pdf]]
