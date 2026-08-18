---
titulo: Requerimientos y Casos de Uso
tipo: análisis
tags: [requerimientos, funcionales, no-funcionales, casos-de-uso, moscow]
fuentes: [Rubrica-EP2-50porciento.pdf, GR_M15_Feresini_Imbriago-EntregaFinal2025.pdf]
actualizado: 2026-08-18
---

# Requerimientos y Casos de Uso

Cubre el **criterio 1** de la rúbrica de EP2. Se apoya en el alcance de [[wiki/proyecto/propuesta]], en la arquitectura de cuatro módulos de [[wiki/solucion/metodologia-tecnica]] y en las decisiones de producto de [[wiki/proyecto/plan-bloque-diseno]].

Tres decisiones estructurales atraviesan toda la lista y conviene tenerlas presentes al leer:

- **El análisis ocurre en dos flujos, no en uno.** El Módulo 1 corre de forma automática sobre los tuits visibles y pinta el indicador; los Módulos 2, 3 y 4 se ejecutan solo cuando el usuario lo pide. La búsqueda web del Módulo 3 tiene costo monetario y latencia de segundos, y correrla sobre cada tuit del *scroll* es inviable.
- **Hay dos tipos de usuario con necesidades opuestas.** El ciudadano usa la extensión de forma anónima y gratuita; el cliente organizacional consume la API y el panel de tendencias bajo una cuenta con plan y cuota.
- **La evidencia tiene jerarquía.** El contraste se apoya, en este orden, en fuentes oficiales, en los cinco medios de referencia y recién después en verificadores profesionales, que cubren pocas afirmaciones por día y publican con días de demora.

## Sobre la cantidad y la numeración

La lista se consolidó el 2026-08-18 tras la calibración contra la tesis de referencia ([[wiki/proyecto/calibracion-tesis-referencia]]): de veintinueve requerimientos funcionales repartidos en cinco tablas se pasó a **dieciséis en una sola tabla**. La reducción es de forma y no de contenido — lo que antes eran varios requerimientos que describían una misma capacidad partida en etapas ahora es uno solo.

Son dieciséis y no trece porque dos de las fusiones previstas rompían argumentos que otros capítulos ya usan: **RF-15** se mantiene separado porque el apartado legal lo cita como la mitigación del art. 11 con prioridad más alta que los requerimientos que lo rodean, y **RF-07** se mantiene porque la reutilización del análisis sostiene el caché y una columna del modelo de datos.

**La numeración no se recicla de acá en adelante.** Un requerimiento que se elimine se marca como tal en lugar de liberar su número.

## Prioridades

Se usa MoSCoW. **Imprescindible** es lo que sin ello no hay producto y entra en el prototipo del PFI; **Importante** es lo que el prototipo debería tener y se implementa si el cronograma lo permite; **Deseable** queda declarado pero no compromete la entrega.

---

## Requerimientos funcionales

| ID | Descripción | Prioridad |
|---|---|---|
| RF-01 | El sistema debe identificar los tuits visibles en el *timeline* de Twitter/X y extraer de cada uno su texto, su identificador nativo, la cuenta autora y sus métricas públicas de propagación | Imprescindible |
| RF-02 | El sistema debe clasificar automáticamente el texto de cada tuit visible mediante el clasificador de lenguaje natural y obtener un `score_nlp` en el rango [0,1] | Imprescindible |
| RF-03 | El sistema debe obtener un `score_source` a partir de las señales públicas de la cuenta autora —antigüedad, seguidores y seguidos, verificación e historial de contenido marcado—, tratadas como atributo del contenido evaluado y no como juicio sobre la persona | Imprescindible |
| RF-04 | El sistema debe extraer del tuit la afirmación verificable que contiene y clasificarla por tipo: normativa, dato económico, salud, educación u otro | Imprescindible |
| RF-05 | El sistema debe contrastar la afirmación siguiendo la jerarquía de evidencia —la fuente oficial que corresponda a su tipo, recuperada de un índice local que un proceso de ingesta periódico mantiene respetando el `crawl-delay` de cada sitio; los cinco medios de referencia; y las verificaciones previas equivalentes cuando existan— y determinar para cada resultado si corrobora, contradice o es neutral | Imprescindible |
| RF-06 | El sistema debe combinar los tres puntajes parciales en un veredicto de tres niveles —contradicho por fuentes oficiales, información sospechosa, parece verificado— y generar una justificación en lenguaje natural donde cada razón derivada de evidencia externa lleve el enlace a la fuente que la respalda. Cuando ningún módulo de contraste haya encontrado fuente, el resultado se emite en el estado *sin contraste externo* y no como uno de los tres niveles | Imprescindible |
| RF-07 | El sistema debe reutilizar un análisis previo cuando el mismo tuit vuelve a solicitarse y el resultado sigue vigente | Importante |
| RF-08 | La extensión debe mostrar sobre cada tuit analizado un indicador visual con su estado —los tres niveles de RF-06, el estado *sin contraste externo* sin porcentaje y un estado transitorio— y señalar explícitamente cuando el análisis es parcial porque algún módulo no pudo ejecutarse | Imprescindible |
| RF-09 | La extensión debe permitir abrir, desde el indicador, el detalle del análisis con el puntaje final, el desglose de los tres puntajes parciales y las fuentes vinculadas ordenadas según la jerarquía de evidencia y etiquetadas por postura, cada una con el enlace al documento original | Imprescindible |
| RF-10 | El panel web debe permitir al usuario consultar el histórico de los análisis solicitados desde su instalación | Importante |
| RF-11 | El usuario debe poder reportar que un veredicto es incorrecto, indicando si se trata de un falso positivo o de un falso negativo y el motivo, y el sistema debe registrar esos reportes de forma que puedan usarse para la revisión de errores y el reentrenamiento del modelo | Importante |
| RF-12 | La extensión y el panel web deben mostrar la finalidad declarada del tratamiento y la vía de supresión del art. 16 de la Ley 25.326, con su plazo de cinco días hábiles | Imprescindible |
| RF-13 | El sistema debe permitir el alta de una organización cliente con autenticación de sus usuarios mediante un proveedor de identidad externo, la emisión y revocación de claves de API, y un endpoint de clasificación autenticado por clave que aplique la cuota mensual del plan contratado y registre el consumo | Importante |
| RF-14 | El panel web debe ofrecer a los clientes organizacionales una vista de tendencias: temas con mayor circulación de contenido marcado, evolución temporal y cuentas con mayor volumen, identificadas mediante un seudónimo que no permita recuperar la cuenta original | Importante |
| RF-15 | Toda entrega de datos hacia un cliente organizacional —exportación de archivo, respuesta de la API o visualización en pantalla— debe entregarse agregada o con la cuenta autora anonimizada | Imprescindible |
| RF-16 | El sistema debe persistir el contenido analizado, los metadatos de la cuenta autora, el resultado del análisis y la evidencia recolectada, asociando cada análisis a la versión de modelo y a la configuración de pesos del ensamblado que lo produjeron | Imprescindible |

Tres de estos merecen una nota porque no se explican solos.

**RF-12 no es una cláusula de cortesía.** La retención sin plazo que fija [[wiki/proyecto/restricciones-legales-eticas]] se sostiene sobre dos condiciones —finalidad declarada estrecha y canal de supresión que funcione— y estos dos textos son la superficie donde ambas se hacen efectivas. Sin ellos, esa decisión se cae.

**RF-15 tiene prioridad más alta que los requerimientos organizacionales que lo rodean, a propósito.** Es la mitigación de diseño del riesgo del art. 11 de la Ley 25.326, y la condición que activa la excepción del inciso 3.e, que exime del consentimiento cuando media un procedimiento de disociación que vuelve inidentificables a los titulares. Dice «entrega» y no «exportación» porque el panel mostrado a un analista de otra organización es una entrega hacia un tercero tanto como un archivo descargado.

**RF-16 no es un requerimiento de infraestructura disfrazado.** Su primera mitad es lo que hace posible el activo del modelo de negocio y el corpus argentino previsto para la Entrega 4; la segunda es lo que permite reproducir un resultado meses después, que es una exigencia del trabajo experimental de la Entrega 5.

### Funcionalidades declaradas fuera de prioridad

Dos capacidades quedan enunciadas sin número propio porque su prioridad era *deseable* y no comprometen la entrega: la **desactivación de la extensión por sesión o por sitio** sin desinstalarla, y el **ajuste de la sensibilidad del indicador** desplazando los umbrales de los tres veredictos. Ambas se configuran en el almacenamiento local del navegador y no persisten en el servidor.

---

## Requerimientos no funcionales

Los valores comprometidos son objetivos de diseño y se validan experimentalmente en la Entrega 5. Se declaran con número y no con adjetivo justamente para que sean verificables.

| ID | Categoría | Descripción |
|---|---|---|
| RNF-01 | Rendimiento | El flujo automático debe mostrar el indicador dentro de los 2 segundos desde que el tuit entra en el área visible, en el percentil 95 |
| RNF-02 | Rendimiento | El flujo a demanda, que incluye búsqueda web y consulta a fuentes oficiales, debe resolverse dentro de los 8 segundos en el percentil 95 |
| RNF-03 | Rendimiento | Un tuit ya analizado y vigente debe resolverse desde caché dentro de los 300 milisegundos |
| RNF-04 | Rendimiento | El procesamiento en el navegador no debe degradar la fluidez del *scroll*: el trabajo ejecutado en el hilo principal por cada tuit no debe superar los 50 milisegundos |
| RNF-05 | Calidad del modelo | El clasificador debe alcanzar un F1 macro de 0,80 y superar en al menos 10 puntos porcentuales a la línea base de TF-IDF con regresión logística |
| RNF-06 | Explicabilidad | Todo veredicto que afirme algo sobre la afirmación analizada debe presentarse acompañado de al menos una fuente enlazada verificable. Cuando ninguna exista, el sistema debe emitir el estado *sin contraste externo* en lugar de un veredicto |
| RNF-07 | Explicabilidad | El resultado debe enunciarse sobre la afirmación analizada y nunca sobre la persona que la publicó, y el nivel severo debe atribuir el juicio a la fuente que lo sostiene en lugar de afirmarlo el sistema por su cuenta |
| RNF-08 | Privacidad | El sistema no persiste datos personales del usuario de la extensión. La dirección IP se recibe en tránsito por el propio protocolo y no se registra ni en la base ni en los *logs* de aplicación. La identificación es un UUID generado localmente, sin correo y sin perfilado |
| RNF-09 | Privacidad | El tratamiento del contenido de terceros se ampara en el art. 5 inc. 2 ap. a) de la Ley 25.326, que exime del consentimiento a los datos de fuentes de acceso público irrestricto. Quedan expresamente excluidas del análisis las cuentas protegidas y los mensajes directos |
| RNF-10 | Privacidad | Ninguna entrega hacia terceros, incluida la visualización en pantalla del panel organizacional, debe contener la identidad de la cuenta autora en claro |
| RNF-11 | Disponibilidad | Ante la indisponibilidad del servicio de inferencia o de la API de búsqueda, el sistema debe devolver un análisis parcial identificado como tal, nunca un error opaco ni un veredicto construido sobre módulos faltantes |
| RNF-12 | Seguridad | Toda comunicación debe realizarse sobre HTTPS y las claves de API deben almacenarse hasheadas |
| RNF-13 | Compatibilidad | El sistema debe funcionar sobre Google Chrome de escritorio bajo Manifest V3, en Windows, macOS y Linux. No se contempla soporte móvil ni otros navegadores |
| RNF-14 | Costo operativo | La infraestructura no debe superar los 14 dólares mensuales durante el período del PFI |
| RNF-15 | Usabilidad | El indicador debe ser interpretable sin instrucción previa por un usuario sin conocimiento técnico |
| RNF-16 | Mantenibilidad | Los umbrales de los veredictos y los pesos del ensamblado deben ser configurables sin necesidad de volver a desplegar el servicio |
| RNF-17 | Legalidad | Todo acceso automatizado a un sitio de terceros debe respetar lo declarado en su `robots.txt`, incluido el `crawl-delay`, y no debe eludir ningún bloqueo de acceso deliberado |

Cuatro merecen una nota, porque no son genéricos sino consecuencia de decisiones ya tomadas.

**RNF-01 y RNF-02 son distintos a propósito.** Si hubiera un solo flujo habría un solo número, y ese número tendría que ser el peor de los dos. Separarlos es lo que permite que el indicador aparezca rápido sin renunciar a la profundidad del contraste semántico.

**RNF-06 es lo que obliga al estado *sin contraste externo*.** Sin él, el flujo automático emitiría un veredicto apoyado únicamente en el texto, sin ninguna fuente que enlazar. La ausencia de evidencia se muestra como ausencia en lugar de vestirse de veredicto.

**RNF-08 distingue recibir de persistir**, que es la distinción que efectivamente se puede sostener: ninguna API sobre HTTPS puede prometer que no recibe la dirección IP, porque el protocolo la entrega en cada petición.

**RNF-17 es lo que hace auditable la postura sobre la obtención de datos.** No es un principio general sino una regla contra un archivo concreto y verificable por cualquiera, sitio por sitio. Su segunda mitad —no eludir bloqueos deliberados— es la que deja fuera del alcance el sitio de Chequeado, que responde 403 a todo cliente que no sea un navegador.

---

## Casos de uso

Actores del sistema:

- **Ciudadano** — usuario de la extensión, anónimo, sin cuenta.
- **Extensión** — actor de sistema; ejecuta el análisis automático sin intervención humana.
- **Analista B2B** — usuario autenticado de una organización cliente.
- **Sistema cliente** — actor de sistema; consume la API mediante clave.

### CU-01 — Analizar automáticamente el *timeline*

**Actor principal:** Extensión.
**Actores secundarios:** Twitter/X, servicio de inferencia.

**Descripción:** mientras el usuario navega su *timeline*, la extensión detecta los tuits que entran en el área visible, obtiene su clasificación de texto y pinta sobre cada uno un indicador. Es el único caso de uso que nadie dispara a mano y el que más veces se ejecuta.

**Flujo de eventos:**

1. El usuario desplaza el *timeline* y uno o más tuits entran en el área visible.
2. La extensión extrae de cada tuit su identificador, su texto y los metadatos públicos de la cuenta.
3. La extensión consulta al servicio si existe un análisis vigente para esos identificadores.
4. Para los que no lo tienen, solicita la clasificación del Módulo 1 en un único pedido agrupado.
5. La extensión inyecta sobre cada tuit el indicador en el estado *sin contraste externo*, que señala que hay señales en el texto y todavía no hay evidencia que las contraste.

**Flujos alternativos:**

- Si existe un análisis completo vigente en caché, se pinta directamente el nivel que corresponda con su evidencia ya asociada.
- Si el servicio de inferencia no responde dentro del tiempo límite, el tuit queda sin marcar y no se muestra error, porque el usuario no pidió nada.
- Si el tuit no contiene texto analizable —solo imagen o video—, queda fuera del alcance del prototipo y no se marca.

**Precondición:** la extensión está instalada y activa, y el usuario navega Twitter/X.
**Postcondición:** los tuits visibles tienen indicador y el resultado quedó registrado.

El flujo automático no emite ninguno de los tres niveles de veredicto sobre un tuit que ve por primera vez: solo corrió el Módulo 1, no hay ninguna fuente que enlazar y afirmar sería afirmar sin respaldo. El indicador aparece igual —RNF-01 se cumple y la extensión sigue avisando sin que se lo pidan— pero como marca de atención.

### CU-02 — Solicitar el análisis profundo de un tuit

**Actor principal:** Ciudadano.
**Actores secundarios:** fuentes oficiales, medios de referencia, API de búsqueda.

**Descripción:** el usuario hace clic sobre el indicador para obtener el análisis completo. El sistema evalúa las señales de la cuenta, extrae la afirmación verificable, la contrasta contra las fuentes según su jerarquía y emite el veredicto con su justificación enlazada.

**Flujo de eventos:**

1. El usuario hace clic sobre el indicador y la extensión muestra el estado transitorio.
2. El servicio ejecuta el Módulo 2 sobre los metadatos de la cuenta.
3. El servicio extrae la afirmación verificable y la clasifica por tipo.
4. El servicio recupera del índice local los documentos de la fuente oficial correspondiente, consulta los cinco medios de referencia, incorpora la verificación previa si existe y clasifica la postura de cada resultado.
5. El Módulo 4 combina los tres puntajes y genera el veredicto y su justificación.
6. La extensión actualiza el indicador y despliega el detalle con el desglose por módulo.

**Flujos alternativos:**

- Si no se identifica ninguna afirmación verificable —opinión, humor, contenido personal—, el resultado se emite en el estado *sin contraste externo*, apoyado solo en los Módulos 1 y 2, y no se marca como parcial porque ningún módulo falló.
- Si la afirmación no tiene cobertura en ninguno de los cinco medios, la ausencia de cobertura se comunica como señal en sí misma y no como falta de datos.
- Si la búsqueda web o la fuente oficial no responden, se devuelve un análisis parcial identificado como tal.

**Precondición:** el tuit tiene indicador visible producto de CU-01.
**Postcondición:** existe un análisis completo persistido, con su evidencia y la versión de modelo que lo produjo.

### CU-03 — Consultar la evidencia de un veredicto

**Actor principal:** Ciudadano.
**Actor secundario:** Sistema.

**Descripción:** el usuario abre el panel de evidencia para ver qué fuentes sostienen el veredicto, con qué postura y con qué cita, y accede al documento original de cada una. Es el caso de uso que materializa la propuesta de valor: sin él, el producto es un clasificador ciego indistinguible de los competidores.

**Flujo de eventos:**

1. El usuario abre el panel de evidencia desde el detalle del análisis.
2. El sistema presenta la afirmación extraída y las fuentes vinculadas agrupadas por tipo y por postura.
3. El usuario abre el enlace a una fuente y accede al documento original.

**Flujos alternativos:**

- Si no hay ninguna fuente vinculada, el panel declara que el análisis está en el estado *sin contraste externo* y aclara que el resultado se sostiene únicamente en el texto y en las señales de la cuenta, en lugar de mostrarse vacío.

**Precondición:** existe un análisis completo producto de CU-02.
**Postcondición:** el usuario accedió a la evidencia y puede verificarla por su cuenta.

### CU-04 — Reportar un veredicto incorrecto

**Actor principal:** Ciudadano.
**Actor secundario:** Sistema.

**Descripción:** el usuario en desacuerdo con un resultado lo reporta indicando el tipo de error y su motivo. El reporte queda asociado a la versión de modelo vigente, que es lo que después permite distinguir un error ya corregido de uno vigente.

**Flujo de eventos:**

1. El usuario elige reportar el resultado.
2. Indica si se trata de un falso positivo o de un falso negativo y agrega el motivo.
3. El sistema registra el reporte asociado al análisis, al UUID anónimo y a la versión de modelo vigente.
4. El sistema confirma la recepción.

**Flujos alternativos:**

- Si el envío falla, el reporte se conserva localmente y se reintenta en la sesión siguiente.

**Precondición:** el usuario tiene a la vista un análisis con el que está en desacuerdo.
**Postcondición:** el reporte queda disponible para la revisión de errores y el reentrenamiento.

### CU-05 — Consultar el histórico personal

**Actor principal:** Ciudadano.
**Actor secundario:** Panel web.

**Descripción:** el usuario abre el panel web y consulta los análisis que solicitó desde que instaló la extensión. El histórico está atado al navegador y no a una persona, que es la contrapartida aceptada de no recolectar datos personales.

**Flujo de eventos:**

1. El usuario abre el panel web desde la extensión.
2. La extensión transmite el UUID almacenado localmente.
3. El panel muestra los análisis asociados, ordenados por fecha, con su veredicto.
4. El usuario abre uno y accede a su detalle y su evidencia.

**Flujos alternativos:**

- Si el usuario abre el panel sin la extensión instalada, no hay histórico que asociar y el panel ofrece únicamente la información institucional del producto.

**Precondición:** el usuario tiene al menos un análisis solicitado desde su instalación.
**Postcondición:** el usuario consultó su histórico; sin sincronización entre dispositivos.

### CU-06 — Consumir la API de detección

**Actor principal:** Sistema cliente.
**Actor secundario:** Sistema.

**Descripción:** un sistema externo envía un texto al endpoint de clasificación con su clave y recibe el veredicto con su evidencia. El consumo se registra contra la cuota de la organización.

**Flujo de eventos:**

1. El sistema cliente envía un texto al endpoint de clasificación con su clave.
2. El servicio valida la clave y verifica la cuota disponible.
3. El servicio ejecuta el análisis completo.
4. El servicio devuelve el puntaje, el veredicto, la justificación y las fuentes vinculadas.
5. El servicio registra el consumo contra la cuota de la organización.

**Flujos alternativos:**

- Si la clave es inválida o fue revocada, se rechaza la solicitud.
- Si la cuota está agotada, se rechaza la solicitud informando el límite del plan y su fecha de renovación.

**Precondición:** la organización tiene una clave de API activa y cuota disponible.
**Postcondición:** la respuesta fue entregada y el consumo quedó registrado.

### CU-07 — Consultar el panel de tendencias

**Actor principal:** Analista B2B.
**Actores secundarios:** proveedor de identidad, Sistema.

**Descripción:** el analista de una organización cliente consulta qué temas con contenido marcado circulan en el período, cómo evolucionan y qué cuentas concentran mayor volumen, y exporta el recorte que le interesa. Es el caso de uso que conecta el capítulo de negocio con el de solución: es literalmente el producto que se vende.

**Flujo de eventos:**

1. El analista se autentica mediante el proveedor de identidad externo.
2. El sistema resuelve la organización y su plan.
3. El panel presenta los temas con mayor circulación en el período, su evolución temporal y las cuentas con mayor volumen, bajo seudónimo.
4. El analista exporta el recorte que le interesa, agregado o con la cuenta autora anonimizada.

**Flujos alternativos:**

- Si la suscripción de la organización no está vigente, el panel se muestra en modo de solo lectura del período ya facturado.

**Precondición:** el analista pertenece a una organización con suscripción vigente.
**Postcondición:** la información fue entregada sin identidad de cuenta autora en claro.

---

## Matriz de trazabilidad

Cada caso de uso realiza un conjunto de requerimientos funcionales. La matriz sirve además como regla de corte para el modelo de datos: toda entidad que se cree tiene que ser trazable hasta acá.

| Caso de uso | Requerimientos que realiza |
|---|---|
| CU-01 | RF-01, RF-02, RF-06, RF-07, RF-08, RF-16 |
| CU-02 | RF-03, RF-04, RF-05, RF-06, RF-08, RF-09, RF-16 |
| CU-03 | RF-09 |
| CU-04 | RF-11 |
| CU-05 | RF-10 |
| CU-06 | RF-13, RF-15 |
| CU-07 | RF-13, RF-14, RF-15 |

**RF-12 es el único requerimiento sin caso de uso asociado**, y no por descuido: es un requerimiento de superficie y no de flujo. Los dos textos están visibles en el *popup* y en el panel web, y ningún caso de uso los tiene como objetivo. Su ausencia en la matriz no lo vuelve opcional, y por eso su prioridad es *imprescindible*.

## Diagrama de casos de uso

Fuente: `wiki/assets/diagramas/casos-de-uso.drawio`. Contiene los cuatro actores y los siete casos de uso, con dos relaciones `<<include>>`: CU-02 incluye a CU-01 —el análisis profundo presupone que el tuit ya fue detectado y clasificado— y CU-03 incluye a CU-02, porque no hay evidencia que consultar sin análisis completo. CU-06 y CU-07 quedan del lado organizacional, separados por el límite del subsistema.

## Referencias cruzadas

- [[wiki/proyecto/propuesta]]
- [[wiki/proyecto/calibracion-tesis-referencia]]
- [[wiki/proyecto/plan-bloque-diseno]]
- [[wiki/solucion/metodologia-tecnica]]
- [[wiki/solucion/arquitectura]]
- [[wiki/solucion/mockups]]
- [[wiki/solucion/modelo-datos]]
- [[wiki/proyecto/restricciones-legales-eticas]]
- [[wiki/negocio/modelo-de-negocio]]
