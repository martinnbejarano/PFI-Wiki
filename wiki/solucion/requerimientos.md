---
titulo: Requerimientos y Casos de Uso
tipo: análisis
tags: [requerimientos, funcionales, no-funcionales, casos-de-uso, moscow]
fuentes: [Rubrica-EP2-50porciento.pdf]
actualizado: 2026-08-11
---

# Requerimientos y Casos de Uso

Cubre el **criterio 1** de la rúbrica de EP2. Todo lo que sigue se apoya en el alcance declarado en [[wiki/proyecto/propuesta]], en la arquitectura de cuatro módulos de [[wiki/solucion/metodologia-tecnica]] y en las ocho decisiones de producto registradas en [[wiki/proyecto/plan-bloque-diseno]].

Dos de esas decisiones atraviesan todo el documento y conviene tenerlas presentes al leer:

- **El análisis ocurre en dos flujos, no en uno.** El Módulo 1 corre de forma automática sobre los tuits visibles y pinta el indicador; los Módulos 2, 3 y 4 se ejecutan solo cuando el usuario lo pide. La búsqueda web del Módulo 3 tiene costo monetario y latencia de segundos, y correrla sobre cada tuit del *scroll* es inviable.
- **Hay dos tipos de usuario con necesidades opuestas.** El ciudadano usa la extensión de forma anónima y gratuita; el cliente B2B consume la API y el panel de tendencias bajo una cuenta de organización. El modelo de negocio de [[wiki/negocio/modelo-de-negocio]] depende de que ambos existan.
- **La evidencia tiene una jerarquía.** El contraste se apoya, en este orden, en fuentes oficiales, en los cinco medios de referencia y recién después en verificadores profesionales. Los verificadores cubren pocas afirmaciones por día y publican con días de demora: la desinformación que interesa detectar es, por definición, la que todavía nadie verificó. La justificación completa está en [[wiki/solucion/metodologia-tecnica]].

## Prioridades

Se usa MoSCoW. **Imprescindible** es lo que sin ello no hay producto y entra en el prototipo del PFI; **Importante** es lo que el prototipo debería tener y se implementa si el cronograma lo permite; **Deseable** queda declarado pero no compromete la entrega.

**La numeración no se recicla.** Los identificadores se asignan una sola vez: los requerimientos que aparecen después de la primera versión se agregan al final de su tabla aunque pertenezcan temáticamente a un grupo anterior, y uno que se elimine se marcaría como tal en lugar de liberar su número. Es lo que permite que una discusión sobre RF-08 signifique lo mismo en agosto y en noviembre.

---

## Requerimientos funcionales

### Detección y análisis

| ID | Descripción | Prioridad |
|---|---|---|
| RF-01 | El sistema debe identificar los tuits visibles en el *timeline* de Twitter/X y extraer de cada uno su texto, su identificador nativo, la cuenta autora y sus métricas públicas de propagación | Imprescindible |
| RF-02 | El sistema debe clasificar automáticamente el texto de cada tuit visible mediante el clasificador de lenguaje natural y obtener un `score_nlp` en el rango [0,1] | Imprescindible |
| RF-03 | El sistema debe obtener un `score_source` a partir de las señales públicas de la cuenta autora —antigüedad, cantidad de seguidores y seguidos, verificación e historial de contenido marcado—, tratadas como atributo del contenido evaluado y no como juicio sobre la persona | Imprescindible |
| RF-04 | El sistema debe extraer del tuit la afirmación verificable que contiene y clasificarla por tipo: normativa, dato económico, salud, educación u otro | Imprescindible |
| RF-05 | El sistema debe consultar los medios de referencia —Infobae, Clarín, La Nación, Página/12 y Télam— y determinar para cada resultado si corrobora, contradice o es neutral respecto de la afirmación analizada | Imprescindible |
| RF-06 | El sistema debe contrastar la afirmación contra los documentos de la fuente oficial que corresponda a su tipo —InfoLEG, INDEC, BCRA, Boletín Oficial, MSal o MinEdu—, recuperados del índice local que mantiene RF-28 | Imprescindible |
| RF-07 | El sistema debe buscar, por similitud semántica sobre *embeddings*, verificaciones previas equivalentes publicadas por verificadores profesionales, e incorporarlas como una fuente adicional cuando existan. No accede de forma directa al sitio de ningún verificador: se apoya en lo indexado y cita el artículo original enlazado | Importante |
| RF-08 | El sistema debe combinar los tres *scores* parciales en un veredicto de tres niveles —contradicho por fuentes oficiales, información sospechosa, parece verificado— aplicando umbrales configurables. Cuando ningún módulo de contraste externo haya encontrado fuente, el resultado se emite en el estado *sin contraste externo* y no como uno de los tres niveles | Imprescindible |
| RF-09 | El sistema debe generar, junto con el veredicto, una justificación en lenguaje natural donde **cada razón derivada de evidencia externa lleve el enlace a la fuente que la respalda** | Imprescindible |
| RF-10 | El sistema debe reutilizar un análisis previo cuando el mismo tuit vuelve a solicitarse y el resultado sigue vigente | Importante |
| RF-28 | El sistema debe mantener un índice local de los documentos de las seis fuentes oficiales, actualizado por un proceso de ingesta periódico que respete el `crawl-delay` declarado por cada sitio y registre la fecha de la última corrida por fuente | Imprescindible |

### Presentación al usuario

| ID | Descripción | Prioridad |
|---|---|---|
| RF-11 | La extensión debe mostrar sobre cada tuit analizado un indicador visual con el estado resultante: los tres niveles de RF-08, el estado *sin contraste externo* —visualmente distinto de los tres y sin porcentaje— y un estado transitorio mientras el análisis está en curso | Imprescindible |
| RF-12 | La extensión debe permitir abrir, desde el indicador, el detalle del análisis con el *score* final y el desglose de los tres *scores* parciales, rotulando el del Módulo 2 como señales de la cuenta autora y no como juicio sobre quien publica | Imprescindible |
| RF-13 | La extensión debe presentar las fuentes vinculadas ordenadas según la jerarquía de evidencia —fuente oficial, medios de referencia, verificación previa— y etiquetadas por postura, cada una con el enlace al documento original | Imprescindible |
| RF-14 | El sistema debe señalar explícitamente cuando el análisis es parcial porque alguno de los módulos no pudo ejecutarse | Importante |
| RF-15 | El panel web debe permitir al usuario consultar el histórico de los análisis solicitados desde su instalación | Importante |
| RF-16 | La extensión debe permitir desactivarse por sesión o por sitio sin desinstalarse | Deseable |

### Retroalimentación y configuración

| ID | Descripción | Prioridad |
|---|---|---|
| RF-17 | El usuario debe poder reportar que un veredicto es incorrecto, indicando si se trata de un falso positivo o de un falso negativo y el motivo | Importante |
| RF-18 | El sistema debe registrar los reportes de forma que puedan usarse para la revisión de errores y el reentrenamiento del modelo | Importante |
| RF-19 | El usuario debe poder ajustar la sensibilidad del indicador, desplazando los umbrales de los tres veredictos | Deseable |
| RF-29 | La extensión y el panel web deben mostrar la finalidad declarada del tratamiento y la vía de supresión del art. 16 de la Ley 25.326, con su plazo de cinco días hábiles | Imprescindible |

RF-29 no es una cláusula de cortesía. La retención sin plazo que fija [[wiki/proyecto/restricciones-legales-eticas]] se sostiene sobre dos condiciones —finalidad declarada estrecha y canal de supresión que funcione— y estos dos textos son la superficie donde ambas se hacen efectivas. Sin ellos, esa decisión se cae.

### Plataforma B2B

| ID | Descripción | Prioridad |
|---|---|---|
| RF-20 | El sistema debe permitir el alta de una organización cliente y la autenticación de sus usuarios mediante un proveedor de identidad externo | Importante |
| RF-21 | El sistema debe permitir emitir y revocar claves de API asociadas a una organización | Importante |
| RF-22 | El sistema debe exponer un endpoint de clasificación autenticado por clave, que devuelva el *score*, el veredicto y las fuentes vinculadas | Importante |
| RF-23 | El sistema debe aplicar la cuota mensual de consultas correspondiente al plan contratado y registrar el consumo | Importante |
| RF-24 | El panel web debe ofrecer a los clientes B2B una vista de tendencias: temas con mayor circulación de contenido marcado, evolución temporal y cuentas con mayor volumen de contenido marcado, identificadas mediante un seudónimo que no permita recuperar la cuenta original | Importante |
| RF-25 | Toda entrega de datos hacia un cliente B2B —exportación de archivo, respuesta de la API o visualización en pantalla— debe entregarse agregada o con la cuenta autora anonimizada | Imprescindible |

RF-25 tiene prioridad más alta que los requerimientos B2B que lo rodean por una razón deliberada: es la mitigación de diseño del riesgo del art. 11 de la Ley 25.326 que se desarrolla en [[wiki/proyecto/restricciones-legales-eticas]]. Si la plataforma B2B se implementa, ese requerimiento no es opcional. Es además la condición que activa la excepción del inciso 3.e de ese artículo, que exime del consentimiento cuando media un procedimiento de disociación que vuelve inidentificables a los titulares.

**RF-24 y RF-25 dicen «entrega» y no «exportación» a propósito.** El panel de tendencias mostrado a un analista de otra organización es una entrega hacia un tercero tanto como un archivo descargado, y era la superficie que la redacción anterior dejaba afuera.

### Persistencia y trazabilidad

| ID | Descripción | Prioridad |
|---|---|---|
| RF-26 | El sistema debe persistir el contenido analizado, los metadatos de la cuenta autora, el resultado del análisis y la evidencia recolectada | Imprescindible |
| RF-27 | Cada análisis debe quedar asociado a la versión del modelo y a la configuración de pesos del ensamblado que lo produjeron | Imprescindible |

RF-26 y RF-27 no son requerimientos de infraestructura disfrazados. El primero es lo que hace posible el activo del modelo de negocio y el corpus argentino previsto para la Entrega 4; el segundo es lo que permite reproducir un resultado meses después, que es una exigencia del trabajo experimental de la Entrega 5.

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
| RNF-10 | Privacidad | Ninguna entrega hacia terceros, incluida la visualización en pantalla del panel B2B, debe contener la identidad de la cuenta autora en claro |
| RNF-11 | Disponibilidad | Ante la indisponibilidad del servicio de inferencia o de la API de búsqueda, el sistema debe devolver un análisis parcial identificado como tal, nunca un error opaco ni un veredicto construido sobre módulos faltantes |
| RNF-12 | Seguridad | Toda comunicación debe realizarse sobre HTTPS y las claves de API deben almacenarse hasheadas |
| RNF-13 | Compatibilidad | El sistema debe funcionar sobre Google Chrome de escritorio bajo Manifest V3, en Windows, macOS y Linux. No se contempla soporte móvil ni otros navegadores |
| RNF-14 | Costo operativo | La infraestructura no debe superar los 14 dólares mensuales durante el período del PFI |
| RNF-15 | Usabilidad | El indicador debe ser interpretable sin instrucción previa por un usuario sin conocimiento técnico |
| RNF-16 | Mantenibilidad | Los umbrales de los veredictos y los pesos del ensamblado deben ser configurables sin necesidad de volver a desplegar el servicio |
| RNF-17 | Legalidad | Todo acceso automatizado a un sitio de terceros debe respetar lo declarado en su `robots.txt`, incluido el `crawl-delay`, y no debe eludir ningún bloqueo de acceso deliberado |

Cinco de estos merecen una nota, porque no son genéricos sino consecuencia directa de decisiones ya tomadas.

**RNF-01 y RNF-02 son distintos a propósito.** Si hubiera un solo flujo habría un solo número, y ese número tendría que ser el peor de los dos. Separarlos es lo que permite que el indicador aparezca rápido sin renunciar a la profundidad del contraste semántico.

**RNF-06 era incumplible tal como estaba enunciado, y el estado *sin contraste externo* es lo que lo repara.** La versión anterior exigía al menos una fuente enlazada para todo veredicto distinto de *parece verificado*, y el propio diseño la incumplía por tres caminos: CU-01 pinta el indicador con `score_nlp` y sin evidencia alguna; el flujo alternativo *4a* de CU-02 se apoya solo en los Módulos 1 y 2 cuando no hay afirmación verificable; y el *2a* de CU-03 contempla que no haya ninguna fuente vinculada. La mitigación más fuerte del proyecto no era obligatoria. Ahora la ausencia de evidencia se muestra como ausencia en lugar de vestirse de veredicto, y RNF-01 sobrevive: el flujo automático sigue avisando sin que se lo pidan, que es la razón de ser de la extensión.

**RNF-07 dejó de prescribir «probabilidad y no sentencia» y pasa a prescribir sobre qué y a quién se atribuye.** La formulación anterior mitigaba un riesgo que la Ley 26.551 cerró en 2009 —las expresiones sobre asuntos de interés público quedaron fuera del ámbito penal— y a cambio empujaba hacia un *score* desnudo que rompe RNF-15. Lo que sí queda expuesto es el juicio asertivo sobre una persona determinada, y eso es lo que el requerimiento prohíbe ahora. El análisis completo está en [[wiki/proyecto/restricciones-legales-eticas]].

**RNF-08 prometía lo imposible.** El enunciado anterior comprometía «sin dirección IP», que ninguna API sobre HTTPS puede cumplir: el protocolo la entrega en cada petición. La redacción nueva distingue recibir de persistir, que es la distinción que efectivamente se puede sostener y verificar. Se descartó persistirla resumida criptográficamente: sumaba una tercera categoría de dato seudonimizado a la base para limitar un abuso que el prototipo no tiene.

**RNF-11 no es una cláusula de estilo.** El sistema depende de cuatro servicios de terceros sobre los que no tiene control: la inferencia en Hugging Face, la API de búsqueda, los sitios de los medios y los portales oficiales. Un veredicto calculado con el Módulo 3 caído sería un veredicto peor sin avisar que lo es.

**RNF-17 es lo que hace auditable la postura sobre la obtención de datos.** No es un principio general sino una regla contra un archivo concreto y verificable por cualquiera, sitio por sitio. Su segunda mitad —no eludir bloqueos deliberados— es la que deja fuera del alcance el sitio de Chequeado, que responde 403 a todo cliente que no sea un navegador.

**`parcial` y *sin contraste externo* son cosas distintas y por eso conviven.** RF-14 marca que un módulo **no pudo** ejecutarse; el estado de RF-08 marca que el módulo **corrió y no encontró** fuente. Pueden darse a la vez, así que se representan por separado.

---

## Casos de uso

Actores del sistema:

- **Ciudadano** — usuario de la extensión, anónimo, sin cuenta.
- **Extensión** — actor de sistema; ejecuta el análisis automático sin intervención humana.
- **Analista B2B** — usuario autenticado de una organización cliente.
- **Sistema cliente** — actor de sistema; consume la API mediante clave.

### CU-01 — Analizar automáticamente el *timeline*

**Actor:** Extensión (actor de sistema).
**Precondición:** la extensión está instalada y activa, y el usuario está navegando Twitter/X.
**Flujo principal:**

1. El usuario desplaza el *timeline* y uno o más tuits entran en el área visible.
2. La extensión extrae de cada tuit su identificador, su texto y los metadatos públicos de la cuenta.
3. La extensión consulta al servicio si existe un análisis vigente para esos identificadores.
4. Para los que no lo tienen, solicita la clasificación del Módulo 1 en un único pedido agrupado.
5. El servicio devuelve el `score_nlp` de cada tuit.
6. La extensión inyecta sobre cada tuit el indicador en el estado *sin contraste externo*, que señala que hay señales en el texto y todavía no hay evidencia que las contraste.

**Flujos alternativos:**

- *3a.* Existe un análisis completo vigente en caché: se pinta directamente el nivel que corresponda de RF-08, con su evidencia ya asociada, y se omiten los pasos 4 y 5 (RF-10).
- *4a.* El servicio de inferencia no responde dentro del tiempo límite: no se pinta indicador alguno y el tuit queda sin marcar. No se muestra error, porque el usuario no pidió nada.
- *2a.* El tuit no contiene texto analizable —solo imagen o video—: queda fuera del alcance del prototipo y no se marca.

**Postcondición:** los tuits visibles tienen indicador, y el resultado quedó registrado según RF-26.

Es el caso de uso que más veces se ejecuta y el único que nadie dispara a mano. También es el que fija RNF-01 y RNF-04: todo lo que ocurre acá ocurre mientras alguien está haciendo *scroll*.

**El flujo automático no emite ninguno de los tres niveles de RF-08 sobre un tuit que ve por primera vez**, y esa es la consecuencia directa de RNF-06. Solo corrió el Módulo 1, así que no hay ninguna fuente que enlazar y afirmar sería afirmar sin respaldo. El indicador aparece igual —RNF-01 se cumple y la extensión sigue avisando sin que se lo pidan—, pero como marca de atención y no como veredicto. El veredicto con nivel y porcentaje aparece cuando hay evidencia: en el *3a*, si el tuit ya fue analizado a fondo, o en CU-02, si el usuario lo pide.

### CU-02 — Solicitar el análisis profundo de un tuit

**Actor:** Ciudadano.
**Precondición:** el tuit tiene indicador visible producto de CU-01.
**Flujo principal:**

1. El usuario hace clic sobre el indicador.
2. La extensión muestra el estado transitorio de análisis en curso y solicita el análisis completo.
3. El servicio ejecuta el Módulo 2 sobre los metadatos de la cuenta.
4. El servicio extrae la afirmación verificable y la clasifica por tipo (RF-04).
5. El servicio recupera del índice local los documentos de la fuente oficial que corresponde al tipo de afirmación y consulta los cinco medios de referencia, y clasifica la postura de cada resultado (RF-05 y RF-06).
6. El servicio busca, además, si existe una verificación previa equivalente y la suma como una fuente más (RF-07).
7. El Módulo 4 combina los tres *scores* y genera el veredicto y su justificación.
8. La extensión actualiza el indicador y despliega el detalle con el desglose por módulo.

**Flujos alternativos:**

- *4a.* No se identifica ninguna afirmación verificable —opinión, humor, contenido personal—: se informa que el contenido no contiene una afirmación verificable y el resultado se emite en el estado *sin contraste externo*, apoyado solo en los Módulos 1 y 2. **No se marca como análisis parcial:** ningún módulo falló, simplemente no hay nada que contrastar, y RF-14 significa otra cosa.
- *5a.* La afirmación no tiene cobertura en ninguno de los cinco medios: la ausencia de cobertura es en sí misma una señal —un hecho de relevancia pública tendría cobertura— y se comunica como tal, no como falta de datos.
- *6a.* No existe verificación previa equivalente, que es el caso frecuente: `score_similarity` se calcula con la fuente oficial y el consenso de medios, sin degradarse.
- *5b y 6b.* La búsqueda web o la fuente oficial no responden: se devuelve análisis parcial identificado como tal (RNF-11).
- *3a-7a.* El análisis completo ya existe y está vigente: se devuelve desde caché.

**Postcondición:** existe un análisis completo persistido, con su evidencia y la versión de modelo que lo produjo.

### CU-03 — Consultar la evidencia de un veredicto

**Actor:** Ciudadano.
**Precondición:** existe un análisis completo producto de CU-02.
**Flujo principal:**

1. El usuario abre el panel de evidencia desde el detalle del análisis.
2. El sistema presenta las fuentes vinculadas agrupadas por tipo y por postura.
3. El usuario abre el enlace a una fuente y accede al documento original.

**Flujos alternativos:**

- *2a.* No hay ninguna fuente vinculada: el análisis está en el estado *sin contraste externo*, y el panel lo dice con esas palabras en lugar de mostrarse vacío. Se aclara que el resultado se sostiene únicamente en el análisis del texto y en las señales de la cuenta, y que por eso no lleva porcentaje.

Es el caso de uso que materializa la propuesta de valor. Sin él, el producto es un clasificador ciego indistinguible de los competidores de la matriz comparativa de [[wiki/competencia/analisis-competitivo]].

### CU-04 — Reportar un veredicto incorrecto

**Actor:** Ciudadano.
**Precondición:** el usuario tiene a la vista un análisis con el que está en desacuerdo.
**Flujo principal:**

1. El usuario elige reportar el resultado.
2. Indica si se trata de un falso positivo o de un falso negativo y agrega el motivo.
3. El sistema registra el reporte asociado al análisis, al UUID anónimo y a la versión de modelo vigente.
4. El sistema confirma la recepción.

**Postcondición:** el reporte queda disponible para la revisión de errores y el reentrenamiento.

La asociación a la versión de modelo del paso 3 es lo que permite distinguir un error ya corregido de uno vigente cuando se revisen los reportes acumulados.

### CU-05 — Consultar el histórico personal

**Actor:** Ciudadano.
**Precondición:** el usuario tiene al menos un análisis solicitado desde su instalación.
**Flujo principal:**

1. El usuario abre el panel web desde la extensión.
2. La extensión transmite el UUID almacenado localmente.
3. El panel muestra los análisis asociados, ordenados por fecha, con su veredicto.
4. El usuario abre uno y accede a su detalle y su evidencia.

**Flujos alternativos:**

- *2a.* El usuario abre el panel sin la extensión instalada: el panel no puede asociar histórico alguno y ofrece únicamente la información institucional del producto.

El histórico está atado al navegador y no a una persona. Es la contrapartida de RNF-08: sin cuenta no hay sincronización entre dispositivos, y esa limitación es una consecuencia aceptada de no recolectar datos personales.

### CU-06 — Consumir la API de detección

**Actor:** Sistema cliente (actor de sistema).
**Precondición:** la organización tiene una clave de API activa y cuota disponible.
**Flujo principal:**

1. El sistema cliente envía un texto al endpoint de clasificación con su clave.
2. El servicio valida la clave y verifica la cuota disponible.
3. El servicio ejecuta el análisis completo.
4. El servicio devuelve el *score*, el veredicto, la justificación y las fuentes vinculadas.
5. El servicio registra el consumo contra la cuota de la organización.

**Flujos alternativos:**

- *2a.* Clave inválida o revocada: se rechaza la solicitud.
- *2b.* Cuota agotada: se rechaza la solicitud informando el límite del plan y su fecha de renovación.

### CU-07 — Consultar el panel de tendencias

**Actor:** Analista B2B.
**Precondición:** el analista pertenece a una organización con suscripción vigente.
**Flujo principal:**

1. El analista se autentica mediante el proveedor de identidad externo.
2. El sistema resuelve la organización y su plan.
3. El panel presenta los temas con mayor circulación de contenido marcado en el período, su evolución temporal y las cuentas con mayor volumen.
4. El analista exporta el recorte que le interesa.

**Flujos alternativos:**

- *4a.* La exportación se entrega agregada o con la cuenta autora anonimizada, conforme RF-25 y RNF-10. La misma regla rige la pantalla del paso 3: las cuentas se muestran bajo un seudónimo que no permite recuperar la original, porque mostrar en pantalla a un analista de otra organización es una entrega hacia un tercero tanto como un archivo descargado.

Este caso de uso es el que conecta el capítulo de negocio con el de solución: es literalmente el producto que se vende a los segmentos descritos en [[wiki/negocio/modelo-de-negocio]].

---

## Matriz de trazabilidad

Cada caso de uso realiza un conjunto de requerimientos funcionales. La matriz sirve además como regla de corte para el modelo de datos: toda entidad que se cree tiene que ser trazable hasta acá.

| Caso de uso | Requerimientos que realiza |
|---|---|
| CU-01 | RF-01, RF-02, RF-08, RF-10, RF-11, RF-26, RF-27 |
| CU-02 | RF-03, RF-04, RF-05, RF-06, RF-07, RF-08, RF-09, RF-12, RF-14, RF-26, RF-27 |
| CU-03 | RF-13 |
| CU-04 | RF-17, RF-18 |
| CU-05 | RF-15 |
| CU-06 | RF-21, RF-22, RF-23, RF-25 |
| CU-07 | RF-20, RF-24, RF-25 |

Cuatro requerimientos quedan sin caso de uso asociado, y los cuatro se justifican:

- **RF-16 y RF-19**, de prioridad *deseable*, son opciones de configuración que no constituyen un objetivo de usuario en sí mismo.
- **RF-28** es un proceso periódico del sistema, sin actor que lo dispare y sin objetivo de usuario propio. Funciona como precondición de CU-02: cuando el paso 5 recupera documentos oficiales, los recupera de lo que este proceso dejó indexado. Modelarlo como caso de uso habría obligado a inventar un actor para un trabajo programado que nadie observa.
- **RF-29** es un requerimiento de superficie, no de flujo: los dos textos están visibles en el *popup* y en el panel web, y ningún caso de uso los tiene como objetivo. Su ausencia en la matriz no lo vuelve opcional, y por eso su prioridad es *imprescindible*.

## Diagrama de casos de uso

Fuente: `wiki/assets/diagramas/casos-de-uso.drawio`. Contiene los cuatro actores —Ciudadano, Extensión, Analista B2B y Sistema cliente— y los siete casos de uso, con dos relaciones `<<include>>`: CU-02 incluye a CU-01 (el análisis profundo presupone que el tuit ya fue detectado y clasificado) y CU-03 incluye a CU-02 (no hay evidencia que consultar sin análisis completo). CU-06 y CU-07 quedan del lado B2B, separados por el límite del subsistema.

## Referencias cruzadas

- [[wiki/proyecto/propuesta]]
- [[wiki/proyecto/plan-bloque-diseno]]
- [[wiki/solucion/metodologia-tecnica]]
- [[wiki/solucion/arquitectura]]
- [[wiki/solucion/modelo-datos]]
- [[wiki/proyecto/restricciones-legales-eticas]]
- [[wiki/proyecto/recursos]]
- [[wiki/negocio/modelo-de-negocio]]
- [[wiki/investigacion/user-research]]
- [[wiki/modelos/modelos-overview]]
