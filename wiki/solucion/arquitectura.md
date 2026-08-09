---
titulo: Arquitectura de la Solución
tipo: análisis
tags: [arquitectura, diseño, infraestructura, c4, componentes, adr]
fuentes: [Rubrica-EP2-50porciento.pdf]
actualizado: 2026-08-12
---

# Arquitectura de la Solución

Cubre el **criterio 3** de la rúbrica de EP2 y aporta la mitad del **criterio 6**. Los diagramas de flujo de información, secuencia y despliegue se agregan el 13/08; el modelo de datos vive en [[wiki/solucion/modelo-datos]].

**Fuentes de los diagramas:** `wiki/assets/diagramas/c4-contexto.drawio`, `c4-contenedores.drawio`, `c4-componentes.drawio`. Se editan y exportan desde draw.io; las exportaciones van a `documento/chapters/figures/`.

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
