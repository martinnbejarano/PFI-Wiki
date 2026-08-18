---
titulo: Plan de volcado al documento — Entrega 50%
tipo: proyecto
tags: [plan, entrega, 50, volcado, latex, rubrica]
fuentes: [Rubrica-EP2-50porciento.pdf]
actualizado: 2026-08-18
---

# Plan de volcado al documento — Entrega 50%

Especificación del contenido que va a entrar al documento LaTeX para la Entrega del 50 %: qué se produjo en el wiki entre el 09 y el 11 de agosto, cómo se produjo, qué le falta, y **qué texto, qué tablas y qué figuras concretas aparecerían en cada sección**. Nada se vuelca hasta que este plan tenga el visto bueno.

Faltan cuatro días para el 22/08. Tres estados distintos, y conviene no confundirlos:

- **Ya está en el documento:** tecnologías con su arquitectura de red y modelo de datos (criterios 5 y 6), volcados el 11/08. Solo se revisan.
- **Escrito en el wiki, sin volcar:** requerimientos, mockups, diagramas y competencia (criterios 1, 2, 3 y 4). Es el volcado propiamente dicho: el contenido existe y hay que traducirlo.
- **Ni escrito ni volcado:** metodología de desarrollo y validación del sistema. Las páginas del wiki son *stubs* de abril con `[POR DEFINIR]`. Esto **no es volcado, es escritura desde cero**, y el plan del 08/08 no lo tenía contemplado.

---

## Criterio 1 — Requerimientos y casos de uso

**Origen:** [[wiki/solucion/requerimientos]], 313 líneas. **Destino:** `chapter04.tex`, sección nueva ubicada **antes** de *Modelo de datos*, para que los RF-xx queden definidos antes de que la matriz de trazabilidad del modelo de datos los invoque.

### Qué se hizo y cómo

Los requerimientos no se enumeraron a partir de una lluvia de ideas: se derivaron del alcance de [[wiki/proyecto/propuesta]] y de las ocho decisiones de producto registradas en [[wiki/proyecto/plan-bloque-diseno]], y cada uno quedó atado a un módulo del sistema. El resultado son **veintinueve requerimientos funcionales** repartidos en cinco bloques temáticos y **diecisiete no funcionales** en once categorías. Los funcionales llevan prioridad MoSCoW con un criterio explícito de qué significa cada nivel: *imprescindible* es lo que sin ello no hay producto y entra en el prototipo del PFI, *importante* es lo que el prototipo debería tener si el cronograma lo permite, *deseable* queda declarado sin comprometer la entrega. Los no funcionales se escribieron **con un número comprometido en lugar de un adjetivo** —2 segundos en el percentil 95, 8 segundos para el flujo profundo, 300 milisegundos desde caché, 50 milisegundos en el hilo principal del navegador, F1 macro de 0,80 con 10 puntos sobre la línea base, 14 dólares mensuales de infraestructura— justamente para que sean verificables y no declamativos.

Tres decisiones estructurales atraviesan la lista entera y son las que hay que poder defender frente al tutor. La primera es que **el análisis ocurre en dos flujos con costos muy distintos**: el clasificador de lenguaje natural corre automáticamente sobre cada tuit que entra en pantalla, mientras que las señales de la cuenta, el contraste con fuentes y el ensamblado corren solo cuando el usuario hace clic, porque la búsqueda web tiene costo monetario y latencia de segundos y correrla sobre cada tuit del *scroll* no se sostiene ni en presupuesto ni en latencia. De esa bifurcación salen dos requerimientos de rendimiento distintos en lugar de uno solo que tendría que ser el peor de los dos. La segunda es que **hay dos tipos de usuario con necesidades opuestas** —el ciudadano anónimo y gratuito, y el cliente organizacional autenticado y pago—, y el modelo de negocio depende de que ambos existan. La tercera es que **la evidencia tiene jerarquía**: primero la fuente oficial, después los cinco medios de referencia, y recién después los verificadores profesionales, que cubren pocas afirmaciones por día y publican con días de demora. Los siete casos de uso se escribieron con actor, precondición, flujo principal numerado, flujos alternativos identificados por el paso donde se bifurcan y postcondición, con cuatro actores en juego: Ciudadano, Extensión (actor de sistema), Analista B2B y Sistema cliente (actor de sistema).

### Qué contenido entra en el documento

`\section{Requerimientos}` con esta estructura:

1. **Párrafo de encuadre** con las tres decisiones estructurales y la regla de numeración no reciclada —RF-28 y RF-29 aparecen al final de sus tablas aunque pertenezcan temáticamente a bloques anteriores—, porque sin esa aclaración la numeración salteada se lee como error de edición.
2. **`\subsection{Requerimientos funcionales}`** con cinco tablas, una por bloque, en el formato ya usado en el capítulo (`[t]`, `\small`, columna de descripción con `p{}`, `\caption` terminado en «Fuente: elaboración propia», `\label{tab:rf-...}`):
   - *Detección y análisis* (RF-01 a RF-10 y RF-28): identificación de tuits visibles y extracción de texto, identificador nativo, cuenta autora y métricas de propagación; clasificación con el puntaje del Módulo 1; señales públicas de la cuenta autora tratadas como atributo del contenido y no como juicio sobre la persona; extracción de la afirmación verificable y su clasificación por tipo (normativa, dato económico, salud, educación u otro); consulta a los cinco medios de referencia con clasificación de postura; contraste contra la fuente oficial que corresponda al tipo de afirmación, recuperada del índice local; búsqueda de verificaciones previas equivalentes por similitud semántica; ensamblado en un veredicto de tres niveles más el estado *sin contraste externo*; justificación en lenguaje natural con enlace por cada razón derivada de evidencia externa; reutilización de análisis vigentes; y el proceso de ingesta periódica que mantiene el índice de fuentes oficiales respetando el `crawl-delay` de cada sitio.
   - *Presentación al usuario* (RF-11 a RF-16): el indicador sobre el tuit con sus cinco estados, el detalle con desglose por módulo, las fuentes ordenadas por jerarquía y etiquetadas por postura, la marca de análisis parcial, el histórico personal y la desactivación por sitio.
   - *Retroalimentación y configuración* (RF-17 a RF-19 y RF-29): reporte de veredicto incorrecto distinguiendo falso positivo de falso negativo, registro de esos reportes para revisión y reentrenamiento, ajuste de sensibilidad de los umbrales, y los dos textos de cara al usuario que declaran la finalidad del tratamiento y la vía de supresión del art. 16 de la Ley 25.326.
   - *Plataforma para organizaciones* (RF-20 a RF-25): alta de organización y autenticación delegada, emisión y revocación de claves, endpoint de clasificación autenticado, cuota mensual por plan con registro de consumo, panel de tendencias con cuentas seudonimizadas, y la regla de que toda entrega hacia un tercero sale agregada o anonimizada.
   - *Persistencia y trazabilidad* (RF-26 y RF-27): persistencia del contenido, los metadatos, el resultado y la evidencia; y la asociación de cada análisis a la versión de modelo y a la configuración de pesos que lo produjeron.
   - **Tres párrafos de justificación** que sí valen la pena en el documento y no son historial de trabajo: por qué RF-29 no es una cláusula de cortesía sino la condición que sostiene la retención sin plazo; por qué RF-25 tiene prioridad más alta que los requerimientos B2B que lo rodean, siendo la mitigación de diseño del riesgo del art. 11; y por qué RF-26 y RF-27 no son requerimientos de infraestructura disfrazados, sino los que hacen posible el corpus argentino y la reproducibilidad experimental de las entregas siguientes.
3. **`\subsection{Requerimientos no funcionales}`** con una tabla de diecisiete filas y tres columnas (identificador, categoría, descripción), seguida de cuatro párrafos que explican los que no son genéricos: por qué RNF-01 y RNF-02 son números distintos a propósito; qué repara el estado *sin contraste externo* en RNF-06; por qué RNF-07 prescribe sobre qué se enuncia y a quién se atribuye en lugar de prescribir «probabilidad y no sentencia»; y por qué RNF-11 no es una cláusula de estilo, dado que el sistema depende de siete servicios de terceros.
4. **`\subsection{Casos de uso}`** con la figura `casos-de-uso.png` y los siete casos en prosa estructurada: párrafo introductorio con actor y precondición, flujo principal como `\begin{enumerate}`, flujos alternativos como `\begin{itemize}` con el identificador de paso en negrita, y postcondición. **El contenido sustantivo de cada uno:** CU-01 es el análisis automático del *timeline* y su consecuencia más discutible —el flujo automático **no emite ninguno de los tres niveles de veredicto** sobre un tuit que ve por primera vez, porque solo corrió un módulo y afirmar sin evidencia rompería RNF-06—; CU-02 es el análisis profundo a pedido con sus seis flujos alternativos, incluido el caso frecuente de que no exista verificación previa equivalente y el caso de que no haya afirmación verificable; CU-03 es la consulta de evidencia, que es el caso de uso que materializa la propuesta de valor; CU-04 el reporte de error, con la asociación a la versión de modelo que permite distinguir un error ya corregido de uno vigente; CU-05 el histórico atado al navegador y no a una persona, que es la contrapartida aceptada de no recolectar datos personales; CU-06 el consumo de la API por un sistema cliente con validación de clave y cuota; y CU-07 el panel de tendencias, que es literalmente el producto que se le vende a los segmentos del capítulo de negocio.
5. **Matriz de trazabilidad** como séptima tabla, más el párrafo que justifica los cuatro requerimientos sin caso de uso asociado: dos son opciones de configuración que no constituyen un objetivo de usuario, RF-28 es un proceso programado que nadie observa y funciona como precondición de CU-02, y RF-29 es un requerimiento de superficie y no de flujo.

**Lo que NO va al documento:** las notas del wiki que explican por qué un requerimiento cambió respecto de su versión anterior —que RNF-08 prometía lo imposible, que RNF-06 era incumplible, que RNF-07 mitigaba un riesgo cerrado en 2009—. Es historial de trabajo y su lugar es `documento/history/`. Los comentarios de opinión («es el caso de uso que más veces se ejecuta») se convierten a voz impersonal o se eliminan.

**Extensión estimada:** 9 a 11 páginas, siete tablas y una figura. Es la sección más larga del capítulo.

### Qué falta o necesita validación

- **Ningún requerimiento fue validado con usuarios.** Los valores de los no funcionales son objetivos de diseño, no mediciones, y el documento tiene que decirlo con esas palabras; se validan experimentalmente en la Entrega 5.
- **El F1 macro de 0,80 de RNF-05 no tiene respaldo experimental propio.** Sale de la literatura: [[wiki/estado-del-arte/toapanta-2024-latam]] reporta 96 % en FakeDeS con MarIA y [[wiki/estado-del-arte/brechas-espanol-latam]] documenta caídas de ~26 pp fuera de dominio, y XLM-T carga además la contra multilingüe de 8 a 12 puntos que Gouliev et al. (2025) reportan. Es el único número del documento que compromete un resultado que todavía no se corrió.
- **Los 2 y los 8 segundos son presupuesto repartido entre módulos**, no una medición: nada está implementado.
- **RF-16, RF-17 y RF-19 no tienen mockup**, así que CU-04 llega al documento sin respaldo visual.

---

## Criterio 2 — Mockups

**Origen:** [[wiki/solucion/mockups]] y `wiki/assets/mockups/mockups.html`. **Destino:** `chapter04.tex`, subsección propia después de requerimientos.

### Qué se hizo y cómo

Cuatro pantallas construidas **en HTML y CSS reales en lugar de dibujadas en una herramienta de diseño**, por una razón práctica: la extensión de la demo hereda este marcado, así que el indicador que se inyecta sobre el tuit es el mismo componente y no una reimplementación. Se navegan con parámetros de URL y las capturas se generan con Chrome en modo *headless* a doble resolución, con un parámetro que esconde la barra de navegación. Las cuatro capturas ya están en `documento/chapters/figures/`: `badge.png`, `popup.png`, `evidencia.png` y `dashboard.png`. El contenido es íntegramente ficticio —cuentas, tuits, titulares y verificaciones inventados sobre temas argentinos verosímiles—, y cada pantalla lleva un rótulo visible que lo aclara para que el documento no señale a ninguna cuenta identificable como fuente de desinformación, que sería contradecir el apartado ético dos secciones antes.

Las cuatro pantallas no son ilustración: cada una materializa una decisión de diseño que sostiene un requerimiento. **El indicador comunica el estado por tres canales a la vez** —color, forma del ícono y texto—, de modo que quien no distingue rojo de verde lee «Contradicho por fuentes oficiales» y ve un triángulo en lugar de un tilde: es lo que hace cumplible RNF-15. **Ningún indicador afirma por sí mismo que el contenido sea falso**: el nivel más severo atribuye el juicio a las fuentes que lo sostienen, que es la traducción visual de RNF-07 y lo que hace entrar el enunciado en la eximente de atribución fiel del art. 113 del Código Penal. **La ausencia de un módulo se muestra como ausencia** —barra rayada, etiqueta *sin dato*, guión en lugar de porcentaje— en vez de disimularse promediando sobre lo que haya, que es RNF-11 hecho pantalla. Y **la columna de cuentas del panel para organizaciones aparece seudonimizada**, porque un *mockup* que mostrara los `@` en claro estaría contradiciendo el apartado legal del propio documento.

### Qué contenido entra en el documento

`\subsection{Interfaz de usuario}` con un párrafo introductorio sobre el método —HTML y CSS reales, contenido ficticio, herencia del marcado hacia la implementación— y cuatro figuras, cada una con un pie extenso que hace el trabajo pesado, porque una captura sin explicación no muestra decisiones de diseño:

| Figura | Qué muestra | Requisitos que realiza | Pie |
|---|---|---|---|
| `badge.png` | Cuatro tuits del *timeline* con los tres niveles de veredicto y el estado transitorio | RF-11, RNF-15, RNF-07 | Los tres canales de comunicación del estado y la línea de motivo que nombra las fuentes en lugar de decir «3 medios» |
| `popup.png` | Dos estados: flujo principal con desglose de los tres puntajes, y flujo degradado sin búsqueda web | RF-12, RF-14, RF-09, RNF-11 | Cómo el desglose vuelve auditable el veredicto, y por qué la ausencia se muestra como ausencia |
| `evidencia.png` | Siete fuentes ordenadas por jerarquía y etiquetadas por postura, con la afirmación extraída arriba | RF-13, RNF-06 | Por qué el verificador aparece último y con la fecha visible, y por qué se incluyó a propósito una fuente que corrobora parcialmente y otra neutral |
| `dashboard.png` | Volumen, tasa de contenido marcado, evolución diaria, temas, cuentas seudonimizadas y consumo de cuota | RF-24, RF-25, RNF-10 | Por qué las cuentas van seudonimizadas y qué relación tiene con el art. 11 |

Los cuatro pies aclaran que el contenido es ficticio. `badge` y `popup` son verticales y entran a `0.6\linewidth`; `evidencia` y `dashboard` son anchas y probablemente necesiten `landscape`, como ya se hizo con el DER.

**Extensión estimada:** 3 a 4 páginas, casi todo figura.

### Qué falta o necesita validación

- **Nadie las vio.** No hay prueba de usabilidad ni validación con usuarios; la rúbrica no la pide en esta instancia pero es la pregunta obvia del tutor.
- **El rótulo de contenido ficticio tiene que sobrevivir al pie de figura.** Si el PDF muestra un `@` que parece real señalado como fuente de desinformación, el documento se contradice a sí mismo.
- **Faltan tres pantallas**: instalación y configuración, formulario de reporte de falso positivo, y estados de error de red del lado del usuario. Ninguna afecta a la rúbrica; la del reporte es la que más conviene sumar si sobra tiempo.

---

## Criterio 3 — Diagramas y arquitectura

**Origen:** [[wiki/solucion/arquitectura]], 165 líneas, más los nueve `.drawio` de `wiki/assets/diagramas/`. **Destino:** `chapter04.tex`, sección *Arquitectura del sistema*, que hoy dice `Completar.`

### Qué se hizo y cómo

El sistema se describió como una extensión de navegador con un servicio de análisis detrás, estructurado en cuatro piezas desplegables —extensión, panel web, API y tarea programada de ingesta— más una base de datos y un servicio de inferencia contratado, con los cuatro módulos corriendo sobre la API. Dos restricciones le dieron forma a todo lo demás y se enuncian antes que los diagramas porque explican decisiones que de otro modo parecen arbitrarias: **el análisis en dos flujos con costos muy distintos**, y que **la inferencia no puede correr donde corre la API por presupuesto y no por memoria** —el plan Hobby de Railway no impone techo de RAM, son cinco dólares con crédito de uso, y un *transformer* residente de unos 125 millones de parámetros quema ese crédito en días mientras que la inferencia bajo demanda se paga por invocación; el techo que decide es el requerimiento de costo—.

Los nueve diagramas se dibujaron en draw.io y se revisaron visualmente uno por uno con un *toolchain* propio que los renderiza en Chrome *headless*, inspecciona el PNG y corrige el XML. **Siete de los ocho que existían entonces tenían defectos**, y dos no eran cosméticos: el diagrama de flujo mostraba el Módulo 2 y el Módulo 3 en cadena, como si el segundo esperara al primero, cuando son independientes y el Módulo 4 espera a ambos —ahora van como bifurcación paralela UML—; y los mensajes del actor en los diagramas de secuencia salían en diagonal, lo que en un diagrama de secuencia sugiere que el mensaje ocurre en un instante distinto en cada extremo. El resto eran títulos tapados por etiquetas de arista y aristas que atravesaban cajas. Se exportaron a PNG a 3× recortado al contenido, entre 2.700 y 4.100 px de ancho.

### Qué contenido entra en el documento

`\section{Arquitectura del sistema}` con seis subsecciones:

1. **Descripción general** con las dos restricciones que le dan forma al diseño.
2. **`\subsection{Vista de contexto}`** — figura `c4-contexto.png` y **tabla de dependencias externas con su modo de falla**: Twitter/X como dependencia estructural sin la cual no hay producto; el servicio de inferencia, cuya caída deja mudo al flujo automático; las fuentes oficiales y los medios de referencia, cuya caída produce análisis parcial señalado; los verificadores, cuya ausencia es el caso frecuente y no degrada nada; la API de búsqueda; y el proveedor de identidad, que afecta solo al panel de organizaciones. La tabla es lo que convierte a RNF-11 de cláusula de estilo en consecuencia: **tres de las cinco zonas del despliegue están fuera de todo control del proyecto**.
3. **`\subsection{Vista de contenedores}`** — figura `c4-contenedores.png` y tabla de seis contenedores con tecnología y responsabilidad: extensión bajo Manifest V3 con su separación entre *content script* y *service worker* —que no es un detalle de implementación, porque el primero corre en el hilo de la página y por eso lleva el techo de 50 milisegundos—; panel web estático en Vercel; API en FastAPI sobre Railway, siempre activa porque los planes que se duermen rompen una extensión que llama en tiempo real; PostgreSQL con `pgvector`; la tarea de ingesta; y el servicio de inferencia externo.
4. **`\subsection{Vista de componentes}`** — figura `c4-componentes.png`. Tres puntos de entrada, y que sean dos endpoints separados en lugar de uno con un parámetro es deliberado: el contrato que se vende es un producto con precio y no debería moverse cuando cambia la extensión. El orquestador es donde vive la decisión de los dos flujos y el que marca el resultado como parcial en lugar de dejar que el ensamblador promedie sobre datos faltantes. **El Módulo 3 está abierto en cinco componentes y su disposición interna es la jerarquía de evidencia hecha estructura**: extractor de afirmaciones, enrutador de fuentes oficiales que consulta el índice local y no el sitio, cliente de medios de referencia, buscador vectorial que entra con línea punteada porque es opcional, y evaluador de postura.
5. **`\subsection{Ingesta de fuentes oficiales}`** — el cambio más importante respecto de la versión de abril. La versión anterior consultaba el sitio oficial dentro de la petición del usuario, y **esa consulta en vivo era incompatible con el presupuesto de latencia**: `argentina.gob.ar` declara `Crawl-delay: 10` y el flujo a demanda dispone de ocho segundos. Las seis fuentes se pre-indexan con una tarea programada que respeta el `crawl-delay` de cada sitio, y las tres consecuencias son mejoras y no concesiones: el requerimiento de latencia se cumple con margen porque la consulta pasa a ser local, el `crawl-delay` se respeta de verdad porque la espera queda fuera del camino crítico, y la postura legal se refuerza.
6. **`\subsection{Flujo de información}`** — figura `flujo-informacion.png`, actividad UML con cinco calles. Dos entradas y una sola salida; ambas convergen en la misma pregunta —si existe análisis vigente— y recién después se separan. Los Módulos 2 y 3 en paralelo. Dentro del Módulo 3, dos aristas salen del nodo de medios hacia la evaluación de postura, una pasando por los verificadores y otra salteándolos, y **que la segunda esté dibujada es lo que deja constancia de que la ausencia de verificación previa no degrada el resultado**. Dos puntos de persistencia y no uno, siendo el segundo lo que hace reproducible un veredicto meses después.
7. **`\subsection{Vistas de secuencia}`** — figuras `secuencia-cu01.png` y `secuencia-cu02.png`. Dos diagramas y no uno, por la misma razón por la que hay dos números de latencia. El mensaje que importa en el primero es el que va del *service worker* a la API: **uno por lote de tuits visibles, no uno por tuit**. El fragmento `opt` que cubre el fallo de la inferencia se resuelve de forma deliberadamente silenciosa, porque el usuario no pidió nada. El segundo abre el Módulo 3 en sus tres fuentes y termina con el fragmento de degradación.
8. **`\subsection{Decisiones de arquitectura}`** — tabla de nueve decisiones con su alternativa evaluada y el motivo del descarte. **Es la tabla que más puntúa de toda la sección**, porque muestra que hubo evaluación y no elección por defecto: los dos flujos frente a todo automático o todo a demanda; la inferencia separada; Railway frente a Render y Fly.io; `pgvector` frente a Qdrant y Pinecone, con el umbral explícito de que la ventaja de un motor dedicado aparece arriba del millón de vectores y el prototipo tendrá decenas de miles; el panel estático separado del backend; la identidad en dos niveles; la autenticación delegada; la degradación a análisis parcial frente a reintentar o devolver error; y las fuentes oficiales pre-indexadas.
9. **Cierre con las decisiones diferidas**: reintentos y *timeouts* por servicio externo, política de expiración del caché, periodicidad exacta de la ingesta por fuente y versionado del contrato de la API. Van declaradas, igual que se hizo en la sección de modelo de datos.

La figura `despliegue-red.png` y la tabla de las cinco zonas **ya están en el documento**, dentro de la sección de tecnologías. No se repiten: se referencian con `\ref{}`.

**Extensión estimada:** 8 a 10 páginas, dos tablas y siete figuras nuevas.

### Qué falta o necesita validación

- **Nada de esto está implementado.** La sección tiene que estar enunciada en voz de propuesta y no como si el sistema existiera.
- **Ninguna latencia está medida** y ningún servicio externo fue probado bajo carga.
- **La periodicidad de la ingesta queda abierta** —el Boletín Oficial publica todos los días hábiles y el INDEC según su calendario— y eso es afinamiento, no arquitectura, pero conviene que el documento lo diga y no que lo omita.

---

## Criterio 4 — Competencia, marketing y modelo de negocio

**Origen:** [[wiki/competencia/analisis-competitivo]] (13/04) y [[wiki/negocio/modelo-de-negocio]] (11/08). **Destino:** `chapter03.tex`, **que hoy está comentado en `main.tex`**.

### Qué se hizo y cómo

Del lado competitivo se relevaron seis soluciones con fortalezas y debilidades: Information Tracer y Cyabra y Blackbird.AI como SaaS comerciales orientados a gobiernos y grandes organizaciones, con precio no público y sin capa ciudadana; Newtral FactFlow como sistema profesional cerrado que corre sobre Telegram con un LLM entrenado sobre más de un millón de mensajes en español; Diggity como prototipo *open-source* ganador de un hackathon en Buenos Aires que evalúa calidad periodística y no veracidad; y Botometer como herramienta académica gratuita que clasifica cuentas como bot o humano, que no es lo mismo que detectar desinformación. Sobre eso se armó una matriz comparativa de once variables —modelo de acceso, plataformas, idiomas, tipo de contenido, velocidad, automatización, escalabilidad, precio público, contexto local, evidencia explicable y datos de entrenamiento— y un análisis de océano azul que identifica el nicho vacío en la intersección de tres características que ningún competidor reúne: gratuito para el ciudadano, automático y escalable, y con contexto local argentino. La conclusión de fondo del análisis es que **la ventaja competitiva no es técnica sino de modelo de negocio**: los *transformers* son *commodity* en 2026, y lo diferencial es que la capa ciudadana genera datos que se monetizan.

Del lado del negocio se escribió un modelo *freemium* con monetización organizacional: no se vende la extensión, se vende información sobre qué desinformación circula ahora mismo, en dos formatos —API de detección con precio por volumen, y reportes y paneles de tendencias por suscripción—. Hay cinco segmentos de clientes desarrollados (medios de comunicación, organizaciones de verificación, centros de investigación y observatorios, organismos públicos y ONGs, y marcas y agencias), un Business Model Canvas completo en sus nueve bloques, una tabla de *pricing* tentativo que va desde el nivel gratuito de mil consultas mensuales hasta contratos de monitoreo electoral de USD 10.000 a 50.000, un FODA en los cuatro cuadrantes, las cinco fuerzas de Porter con su evaluación y su mitigación, misión y visión, y cuatro riesgos del modelo con mitigación —adopción, regulatorio, reputacional y competitivo—. El argumento central es el bucle de red de datos: más usuarios ciudadanos producen un mapa más completo, que hace más valioso el producto pago, que financia un mejor producto ciudadano.

### Qué contenido entra en el documento

`\section{Análisis de Competencia}` y `\section{Modelo de Negocio}` en `chapter03.tex`:

- **Panorama de soluciones**, breve, **remitiendo con `\ref{}` a la matriz comparativa que ya está impresa en el capítulo 2** (`tab:competidores`, sección *Soluciones comerciales y de mercado*). El capítulo 3 no la repite: aporta lo que el capítulo 2 no tiene, que es el análisis estratégico.
- **Océano azul**: el nicho no ocupado y el argumento de que la ventaja no es técnica.
- **Matriz ERIC** como tabla de cuatro columnas con sus diez atributos: qué se elimina (grafos de propagación, multiidioma), qué se reduce (multimodalidad, verificación manual, detección de bots puros), qué se incrementa (automatización, velocidad, accesibilidad ciudadana, evidencia explicable) y qué se crea (datos de tendencias locales).
- **FODA** como tabla de cuadrantes.
- **Cinco fuerzas de Porter** en prosa, con la evaluación de cada fuerza y su mitigación.
- **Business Model Canvas** como tabla de nueve bloques.
- **Segmentos de clientes** en prosa, con lo que cada uno compraría.
- **Tabla de *pricing*** declarada explícitamente como tentativa y sujeta a validación de mercado.
- **Misión, visión y riesgos del modelo.**

**Extensión estimada:** 6 a 8 páginas, de las cuales cuatro son tablas.

### Qué falta o necesita validación — y las cuatro contradicciones

Este es el material que más atención necesita antes de volcarse, porque **el análisis competitivo es de abril y nunca se actualizó con las decisiones de agosto**. Hay cuatro contradicciones que un evaluador que lea el documento completo va a encontrar:

1. **La cobertura de WhatsApp.** `modelo-de-negocio.md` afirma que el sensor cubre «cualquier sitio donde el usuario navegue» y que un enlace de WhatsApp abierto en el navegador queda registrado, apoyándose en el 93 % de penetración de WhatsApp en Argentina. **Contradice el alcance del capítulo 1**, que declara Twitter/X como única plataforma de detección, y roza el requerimiento de privacidad, porque registrar qué enlaces abre un usuario es otra cosa que analizar tuits públicos. Es la contradicción más grave de las cuatro porque está exactamente en la parte del argumento que sostiene el activo diferencial del negocio: sacarla debilita el *moat*, dejarla contradice el alcance.
2. **El dataset de entrenamiento** en la matriz comparativa dice «LIAR, FakeNewsNet + Chequeado». Chequeado salió del alcance en agosto —responde 403 a todo cliente que no sea un navegador y RNF-17 prohíbe eludir bloqueos deliberados— y el modelo elegido es XLM-T.
3. **La matriz ERIC dice «reducir a español rioplatense»** como si el modelo fuera monolingüe, y el BMC repite «modelo NLP entrenado en español rioplatense». XLM-T es multilingüe; lo que se acota es el dominio de los datos, no la capacidad del modelo.
4. **Chequeado figura como socio clave del BMC** —«sinergia, posible cliente y partner académico»— mientras el apartado legal explica que se lo excluye del acceso automatizado. Las dos cosas pueden convivir, porque un socio comercial no es una fuente de la que se extraen datos, pero hay que escribirlo: leído en crudo parece incoherente.

Y dos cuestiones de encuadre que no son contradicciones pero cambian qué se escribe:

- **La rúbrica nombra cuatro herramientas de marketing** —triple P, FODA, Cruz de Porter y Matriz Boston Consulting— y el proyecto tiene FODA, Porter, ERIC y océano azul. ERIC y océano azul son herramientas legítimas de estrategia competitiva pero no están en esa lista, así que conviene sumar una de las nombradas.
- **Descomentar `chapter03` arrastra la sección de User Research**, que hoy son tres `Completar.` y cuyo trabajo de campo no se corrió: la encuesta tenía 7 respuestas al 08/08 y no hay entrevistas.

---

## Criterio 5 — Tecnologías y arquitectura de red *(ya en el documento)*

Volcado el 11/08, `chapter04.tex` líneas 111-186. Contiene la tabla de componentes por capa con versiones fijadas y verificadas contra el registro de paquetes el 10/08; ocho decisiones con su alternativa descartada; la separación entre el entorno de experimentación y la imagen que se despliega, que es lo que sostiene todo el presupuesto de infraestructura; y la arquitectura de red completa con sus cinco zonas por grado de control, TLS 1.3 en todo cruce, la red privada donde viven API, ingesta y base sin puerto público, la autenticación por frontera y qué dato exacto cruza cada límite.

**Lo único a revisar:** las versiones se verificaron el 10/08 y el documento las presenta como vigentes. O se revalidan o se agrega la fecha de verificación al pie de la tabla; es lo que un evaluador técnico comprueba en un minuto.

---

## Criterio 6 — Modelo de datos *(ya en el documento)*

Volcado el 11/08, `chapter04.tex` líneas 16-110, con el DER como figura apaisada. Diecisiete entidades en cinco dominios con atributos, tipos, cardinalidades y la matriz de trazabilidad entidad → requerimiento funcional, que es lo que hace verificable la regla de corte: toda entidad se traza hasta un requerimiento, y por eso el número de entidades es una consecuencia y no un objetivo. La revisión del 11/08 ya corrigió el error de conteo de relaciones que estaba impreso.

**No queda trabajo**, más allá de ubicar la sección de requerimientos antes que esta para que los RF-xx queden definidos antes de invocarse.

---

## Lo que no es volcado sino escritura desde cero

El plan del 08/08 daba por hecho que las cuatro `Completar.` restantes del capítulo 4 se cerraban con material existente. Al revisar el wiki, **dos de las cuatro no tienen fuente**:

| Sección de `chapter04.tex` | Fuente en el wiki | Estado real |
|---|---|---|
| *Metodología* | [[wiki/proyecto/metodologia]] | **Stub de abril con `[POR DEFINIR]`.** No hay metodología elegida, ni herramientas de gestión, ni definición de iteraciones ni criterio de terminado. Hay que decidirla y escribirla |
| *Datasets* | [[wiki/datasets/comparacion-datasets]] y [[wiki/datasets/dataset-recomendacion]] | Hay material abundante, pero **el capítulo 2 ya tiene una tabla comparativa de datasets**. Esta sección tiene que ser la *estrategia de datos del proyecto* —los tres niveles: transferencia desde inglés, adaptación al español, corpus argentino como contribución—, no un relevamiento. Y arrastra dos decisiones abiertas: el tamaño del corpus argentino y el número de clases |
| *Arquitectura del sistema* | [[wiki/solucion/arquitectura]] | La absorbe el criterio 3 |
| *Validación del sistema* | [[wiki/solucion/pruebas]] | **Stub de abril con `[POR DEFINIR]`.** Una sola fila `CP-01 [POR DEFINIR]`. Hay que diseñar el plan de pruebas: casos de prueba funcionales, protocolo de usabilidad y estrategia de validación con usuarios |

De las dos que hay que escribir, **la metodología es la barata** —se decide la forma de trabajo, se declara el tablero de *issues* que ya está en uso y el control de versiones, y se escribe en una hora—. **La validación es la cara**, porque diseñar casos de prueba para un sistema no implementado obliga a definir qué se va a probar y cómo, y es la sección donde el tutor Monzón insiste con validación real y no de laboratorio.

---

## Orden de ejecución propuesto

El orden importa: la sección de requerimientos define los RF-xx que las otras tres referencian.

| # | Trabajo | Dónde | Estimación |
|---|---|---|---|
| 1 | Resolver las cuatro contradicciones del material de competencia y negocio | wiki | 1 h |
| 2 | Requerimientos y casos de uso | `chapter04.tex` | media jornada |
| 3 | Mockups | `chapter04.tex` | 2 h |
| 4 | Arquitectura y diagramas | `chapter04.tex` | media jornada |
| 5 | Competencia, marketing y modelo de negocio | `chapter03.tex` | 3 h |
| 6 | Metodología de desarrollo (decidir + escribir) | wiki → `chapter04.tex` | 1 h |
| 7 | Estrategia de datos | `chapter04.tex` | 2 h |
| 8 | Plan de validación (diseñar + escribir) | wiki → `chapter04.tex` | 3 h |

---

## Decisiones abiertas

1. **Casos de uso: ¿los siete completos, o dos completos y cinco abreviados?** Los siete con todos sus flujos alternativos son unas 5 de las 9-11 páginas de la sección. Recomiendo CU-01 y CU-02 completos —son los que tienen los flujos que importan— y CU-03 a CU-07 con flujo principal más los alternativos que aportan una decisión de diseño.
2. **`chapter03` y el User Research.** Descomentarlo para el criterio 4 deja tres `Completar.` visibles. ¿Se corre campo y se escribe el 20/08 con lo que haya, o se reordena el capítulo para que la ausencia no quede como hueco?
3. **La herramienta de marketing que falta.** Recomiendo sumar el mix de marketing (4P), que está en la lista de la rúbrica y se escribe en media hora. La Matriz Boston Consulting no aplica: exige una cartera de productos y acá hay uno solo.
4. **RNF-05, el F1 macro de 0,80.** ¿Se sostiene como objetivo declarado o se baja? Es el único número del documento que compromete un resultado experimental sin correr.
5. **La contradicción de WhatsApp.** ¿Se saca del argumento del *moat*, o se reformula como línea futura declarada fuera del alcance del prototipo? Las otras tres contradicciones son correcciones mecánicas.
6. **Volumen del capítulo 4.** Pasa de 5.229 palabras a unas 12.000 y de 2 figuras a 13. ¿Van todas al cuerpo o alguna al anexo? Recomiendo todas al cuerpo: el evaluador las busca en el capítulo.
7. **Metodología de desarrollo: ¿cuál?** Kanban sobre el tablero de *issues* que ya está en uso es lo honesto —es literalmente cómo se viene trabajando— frente a declarar Scrum con *sprints* que no existieron.
8. **Validación del sistema.** Con el sistema sin implementar, ¿la sección declara el plan de pruebas diseñado, o se deja `Completar.` y se asume la pérdida en ese ítem?

---

## Referencias cruzadas

- [[wiki/proyecto/entrega-50-alcance]]
- [[wiki/proyecto/plan-entrega-50]]
- [[wiki/proyecto/plan-bloque-diseno]]
- [[wiki/solucion/requerimientos]]
- [[wiki/solucion/mockups]]
- [[wiki/solucion/arquitectura]]
- [[wiki/solucion/modelo-datos]]
- [[wiki/solucion/tecnologias]]
- [[wiki/solucion/pruebas]]
- [[wiki/proyecto/metodologia]]
- [[wiki/competencia/analisis-competitivo]]
- [[wiki/negocio/modelo-de-negocio]]
- [[wiki/datasets/comparacion-datasets]]
