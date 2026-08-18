---
titulo: Restricciones Legales y Éticas — Contexto Argentino
tipo: proyecto
tags: [legal, ético, privacidad, argentina, compliance, lpdp, honor, robots-txt]
fuentes: []
actualizado: 2026-08-11
---

# Restricciones Legales y Éticas — Contexto Argentino

## Cómo leer este apartado

El análisis está organizado por **acto**, no por norma. Cada cosa que el sistema hace —recolectar, almacenar, obtener de un sitio ajeno, publicar un juicio, entregar datos a un tercero— tiene su propio riesgo y su propia defensa, y mezclarlos en una sola matriz de semáforos es lo que vuelve indefendible un apartado legal. Las citas son al texto vigente de cada norma, verificado contra la fuente oficial el 2026-08-10; las URLs están en la tabla del final.

Dos advertencias de método que valen para todo lo que sigue.

**No se afirma que no haya riesgo.** Se identifica dónde está, qué lo mitiga y qué queda expuesto. Un análisis que reconoce su propio límite vale más que uno que lo tapa, y los límites están escritos en su propia sección.

**La postura distingue el prototipo del producto.** Varias obligaciones se disparan por hechos que el PFI no ejecuta: publicar la extensión en una tienda, prestar servicio comercial, distribuir el corpus. Donde ese corte importa, está enunciado.

## Dos poblaciones de datos, dos defensas distintas

La base contiene datos de dos grupos de personas y sus defensas no son la misma. Confundirlos es el error que hacía contradictoria la versión anterior de este archivo.

| Población | Qué se guarda | Defensa |
|---|---|---|
| **Autores de los tuits analizados** | Texto del tuit, `@`, métricas públicas, señales de la cuenta | Son datos personales. Amparados por el art. 5 inc. 2 ap. a): fuentes de acceso público irrestricto |
| **Usuarios de la extensión** | Un UUID generado localmente y la fecha de instalación | Se sostiene que no constituyen dato personal en los términos del art. 2 |

## Ley 25.326 — Protección de los Datos Personales

### Qué es dato personal, y por qué el UUID de la extensión no lo es

El art. 2 define dato personal como «información de cualquier tipo referida a personas físicas o de existencia ideal **determinadas o determinables**». La determinabilidad es la condición, y es lo que resuelve el caso del identificador de la extensión.

`usuario_extension` guarda dos columnas: un UUID generado en el navegador y la fecha de instalación. Sin correo, sin nombre, sin cuenta y sin ningún atributo que permita llegar a una persona. La postura del proyecto es que ese identificador **no determina a nadie** y por lo tanto queda fuera del alcance de la ley. La configuración de la extensión —los umbrales del indicador y la desactivación por sitio— no sale del almacenamiento local, precisamente para que esa fila siga siendo tan flaca como el argumento necesita.

**El flanco, escrito y no omitido.** La postura queda expuesta en dos puntos concretos, y conviene tenerlos preparados antes de la defensa y no descubrirlos en ella:

1. El sistema **sí cruza** el UUID contra la lista de tuits que esa instalación consultó, porque de eso vive RF-10. Es el mismo tipo de cruce que este apartado analiza con cuidado cuando el sujeto es el autor de un tuit, y sería incoherente aplicarle otra vara cuando el sujeto es el usuario propio.
2. Combinado con la retención sin plazo, queda un identificador persistente atado a un historial de consultas. El canal de supresión del art. 16 que se describe abajo cubre a los autores de los tuits, no al usuario de la extensión.

Se consideró convertir el argumento en un hecho de diseño —un botón de «borrar mi histórico» que regenerara el UUID localmente y disparara el borrado en el servidor— y se decidió no incorporarlo al alcance del prototipo. La postura se sostiene sobre el texto del art. 2, y esa función queda identificada como el refuerzo natural si el producto llegara a publicarse.

### Recolección: amparada por el art. 5 inc. 2 ap. a)

El art. 5 inc. 1 declara ilícito el tratamiento sin consentimiento libre, expreso e informado. El inciso 2 lista las excepciones, y la primera es exactamente el caso de este sistema:

> No será necesario el consentimiento cuando: a) Los datos se obtengan de **fuentes de acceso público irrestricto**.

Un tuit publicado en una cuenta abierta es una fuente de acceso público irrestricto: cualquier persona lo lee sin credencial, sin pago y sin autorización previa. La recolección del contenido y de las señales públicas de la cuenta autora se ampara ahí, y por eso el sistema no pide ni podría pedir consentimiento a los autores de los tuits que analiza.

**El límite del amparo es tan importante como el amparo.** «Irrestricto» significa sin restricción de acceso, y eso deja dos cosas expresamente afuera:

- **Las cuentas protegidas**, cuyo contenido exige que el titular apruebe a cada lector. Ahí hay restricción, y el inciso no aplica.
- **Los mensajes directos**, que no son públicos en ningún sentido.

Las dos exclusiones están declaradas como requerimiento no funcional (RNF-09) y no como buena intención, que es lo que las vuelve verificables.

El art. 4 inc. 1 agrega una condición que se cumple por diseño: los datos recogidos deben ser «adecuados, pertinentes y no excesivos en relación al ámbito y finalidad». El sistema captura el texto, las métricas públicas de propagación y las señales de trayectoria de la cuenta —lo que los Módulos 1 y 2 consumen— y nada más.

### Retención: sin plazo de destrucción, con finalidad estrecha

El art. 4 inc. 7 manda que «los datos deben ser destruidos cuando hayan **dejado de ser necesarios o pertinentes** a los fines para los cuales hubiesen sido recolectados». No impone un reloj: impone una condición. Mientras la finalidad declarada subsista, la necesidad subsiste.

**Por eso no se fija plazo de destrucción, y por eso la finalidad se enuncia estrecha.** La finalidad declarada del tratamiento es la investigación y el entrenamiento del clasificador, más el historial agregado por cuenta que el Módulo 2 necesita para producir su señal. Una finalidad amplia haría que nunca venciera nada, que es precisamente lo que el artículo quiere evitar; una finalidad estrecha es lo que hace que «sin plazo» sea una consecuencia del texto legal y no una comodidad operativa.

Lo que vuelve defendible la postura no es el argumento sino lo que lo acompaña: que exista un canal de supresión que funcione y que la disociación sea real. Retención indefinida sin canal de supresión no se sostiene; con canal, sí.

### Supresión: el art. 16, cinco días hábiles y qué se borra

El art. 16 inc. 1 da a toda persona derecho a que se supriman sus datos personales, y el inc. 2 fija el plazo: **cinco días hábiles** desde el reclamo.

**Canal.** Una dirección de correo publicada en el *popup* de la extensión y en el panel web, atendida a mano. No se construye formulario ni verificación de titularidad: para el volumen de un prototipo, atenderlo a mano es proporcionado y es lo que la ley pide.

**Qué borra la supresión.** El `@` y los metadatos de la cuenta, más el identificador nativo del tuit. El texto del tuit, el análisis y la evidencia sobreviven **disociados**: sin autor no identifican a nadie, así que salen del alcance de la ley. La fila de `cuenta` queda marcada como suprimida, para que el sistema no vuelva a enriquecerla la próxima vez que aparezca un tuit de esa misma cuenta.

**Los dos agujeros de reidentificación quedaron cerrados en el modelo de datos**, y esto es lo que hace que la disociación no sea una promesa:

- La URL del tuit contenía el `@` y lo habría dejado en claro en una segunda columna. **No se persiste**: se reconstruye siempre como `x.com/i/status/{id_nativo}`, forma que redirige.
- El identificador nativo permitía recuperar el `@` consultando la plataforma. **Se borra en la supresión.**

**El costo, escrito y no tapado.** Esa fila puntual deja de ser reproducible para el trabajo experimental posterior. Es un costo acotado a las filas efectivamente suprimidas, y es el escenario correcto: quien ejerció el art. 16 obtuvo lo que pidió. El detalle está en [[wiki/solucion/modelo-datos]].

### Cesión a terceros: el art. 11 es la exposición real

Este es el punto expuesto del proyecto, y conviene decirlo antes que su mitigación. El art. 11 inc. 1 exige, para ceder datos personales, interés legítimo de ambas partes **y consentimiento previo del titular**. El inc. 4 agrega que el cesionario queda sujeto a las mismas obligaciones y que el cedente **responde solidariamente**.

Consentimiento del titular no hay, y no puede haberlo: los titulares son los autores de los tuits analizados. Así que la plataforma B2B —la API de RF-13 y el panel de tendencias de RF-14— sería una cesión sin base legal si entregara la identidad de la cuenta autora.

**La mitigación está en el propio artículo.** El inc. 3.e exime del consentimiento cuando «se hubiera aplicado un procedimiento de **disociación** de la información, de modo que los titulares de los datos sean **inidentificables**». Esa es exactamente la condición que el diseño implementa:

- **RF-15** —prioridad *imprescindible*, más alta que los requerimientos B2B que lo rodean— exige que toda entrega hacia un cliente B2B salga agregada o con la cuenta autora anonimizada.
- **RNF-10** cubre **toda entrega hacia terceros, incluida la visualización en pantalla del panel**, y no solo las exportaciones de archivo. La pantalla de un analista de otra organización es una entrega tanto como un CSV.
- El seudónimo que agrupa por cuenta es el **serial interno** de la tabla, que no deriva del `@`. Es irreversible por construcción y no por fuerza criptográfica, y sobrevive a la supresión sin comprometerla. Un resumen criptográfico del `@` habría sido un derivado del dato personal, con una clave que gestionar, para lograr lo que el serial da sin costo.

Que la mitigación sea un requerimiento con identificador y prioridad, y no una intención declarada en un párrafo, es lo que la vuelve verificable.

**Lo que queda expuesto igual.** El art. 11 inc. 3.b remite a las excepciones del art. 5 inc. 2, lo que permitiría argumentar que los datos de fuente pública también quedan exentos de consentimiento para la cesión. El proyecto **no se apoya en ese argumento**: la disociación del inc. 3.e es una condición que el diseño cumple y puede demostrar, mientras que la extensión del inc. 3.b a la cesión comercial de perfiles de cuenta es discutible y dejaría en pie la responsabilidad solidaria del inc. 4. Se prefiere la defensa que depende del diseño propio y no de una interpretación.

## Cómo se obtienen los datos

Tres modalidades distintas, con tres argumentos distintos. Tratarlas como un solo acto —«*scraping* sin permiso, zona gris, evitar»— es lo que impedía defender ninguna de las tres.

### Modalidad 1 — La extensión lee el DOM de la página

**No es *scraping*, y aunque lo fuera, los términos de servicio no son ley.** Dos argumentos independientes:

1. **No hay acceso automatizado a los servidores de la plataforma.** El contenido ya fue entregado al navegador del usuario, autenticado, dentro de su propia sesión. La extensión lee lo que la pantalla de esa persona ya está mostrando. Es el mismo acto que ejecutan los lectores de pantalla, los bloqueadores de publicidad y los correctores ortográficos, y ninguno se considera recolección automatizada del servicio.
2. **El incumplimiento de los términos de servicio es contractual, no un ilícito.** Vincula a la plataforma con su usuario. No genera responsabilidad para quien desarrolla la extensión ni para el responsable del tratamiento.

**El riesgo real es uno solo y es del usuario: la suspensión de su cuenta.** Se enuncia así, con esas palabras. Un riesgo acotado y nombrado vale más que una zona gris.

### Modalidad 2 — Sitios públicos del Estado

Cada acceso se justifica contra el `robots.txt` de su destino, no contra un principio general. Es la única forma de que la postura se pueda auditar sitio por sitio en lugar de pedirle confianza al lector. Verificado el 2026-08-10:

| Sitio | Qué declara su `robots.txt` | Lectura |
|---|---|---|
| `indec.gob.ar` | `Disallow:` vacío | Todo permitido, sin reservas |
| `bcra.gob.ar` | Permite explícitamente `GPTBot`, `ClaudeBot`, `Google-Extended` y `CCBot`; bloquea `Bytespider` | **Permiso escrito para rastreadores de entrenamiento de IA** |
| `boletinoficial.gob.ar` | Bloquea solo `/seccion/segunda/*` | La segunda sección son avisos de particulares; la legislación de la primera está permitida |
| `infoleg.gob.ar` | No existe el archivo | Sin restricción declarada |
| `argentina.gob.ar` (MSal y MinEdu) | `Crawl-delay: 10` y `Disallow: /sites/default/files/infoleg/` | **Una petición cada diez segundos** |

El caso del BCRA es el hallazgo que conviene citar textual: un organismo del Estado argentino que **autoriza expresamente** el rastreo para entrenamiento de modelos de inteligencia artificial. Deja de ser un argumento del proyecto sobre lo que la ley permitiría y pasa a ser un permiso escrito por el titular del sitio.

**El `crawl-delay` se respeta de verdad, y eso obligó a un cambio de arquitectura.** Una petición cada diez segundos es incompatible con RNF-02, que exige resolver el flujo a demanda en ocho segundos. Por eso las fuentes oficiales **se pre-indexan**: un proceso de ingesta asíncrono y periódico las recorre y vuelca su contenido a un índice local, y el flujo a demanda consulta el índice y no el sitio. La decisión está desarrollada en [[wiki/solucion/arquitectura]], y refuerza la postura legal además de la técnica: acceso cortés, espaciado y de baja frecuencia, en lugar de una consulta sincrónica por cada tuit que un usuario mire.

### Modalidad 3 — Chequeado queda fuera del alcance

`chequeado.com` devuelve **HTTP 403 a todo cliente que no sea un navegador**, incluido el pedido de su propio `robots.txt`. Verificado el 2026-08-10 con dos clientes independientes. No hay archivo de exclusión que respetar porque el sitio no lo entrega: el bloqueo es de infraestructura y es deliberado.

El sitio no se accede de forma directa. **RF-05 sobrevive** apoyándose en lo que el servicio de búsqueda ya tiene indexado y en la cita enlazada al artículo original.

**Se consideró acceder declarando un identificador de navegador, y se descartó.** Eludir un bloqueo deliberado no es leer un sitio abierto: es el hecho que traslada la discusión desde los términos de servicio hacia el art. 153 bis del Código Penal, acceso indebido a un sistema informático de acceso restringido. Queda escrito que se evaluó y por qué no.

### La API oficial de la plataforma queda descartada por diseño

**Ningún nivel de la API de X entrega el *timeline* de un usuario tal como él lo ve.** El producto analiza lo que la persona está mirando en ese momento, y eso no es algo que la plataforma venda a ningún precio. El techo de costo de RNF-14 es un argumento redundante encima de uno definitivo, y apoyarse en el precio debilitaría la postura: invita a la réplica «con más presupuesto lo harían por la vía correcta», y no existe esa vía.

## Ley 11.723 — Propiedad intelectual

Un tuit es una obra protegida. La distinción que importa es entre **almacenar** y **distribuir**, y el proyecto hace lo primero y no lo segundo.

**El texto del tuit se almacena completo.** Es reproducción con fin de investigación, sin acto de distribución. RF-16 —*imprescindible*— se sostiene sin necesidad de invocar el derecho de cita, y el corpus argentino previsto para las entregas siguientes queda viable.

**El corpus no se distribuye durante el PFI.** Ninguna página del proyecto pide distribuirlo: aparece siempre como insumo de entrenamiento y como activo del modelo de negocio, nunca como algo que se libere. El argumento que cerró la decisión es interno y vale la pena dejarlo escrito: la retención sin plazo solo es defendible porque existe un canal de supresión que funciona, y **una fila se borra, un corpus descargado no**. Distribuir el texto completo habría vuelto incumplible de forma retroactiva la promesa del art. 16.

No es una puerta que se cierre. Publicar más adelante, con el corpus disociado, sigue siendo posible; no publicarlo ahora no es irreversible.

## Delitos contra el honor — lo que la reforma de 2009 cambió

Este apartado se reescribió por completo porque el riesgo estaba mal encuadrado. La prescripción habitual —«*score*, no veredicto»— mitiga un riesgo que la ley cerró en 2009, y a cambio destruye la interpretabilidad del producto.

### La Ley 26.551

Dictada en cumplimiento de la sentencia de la Corte Interamericana de Derechos Humanos en **Kimel vs. Argentina**, la Ley 26.551 sustituyó los arts. 109, 110, 111, 113 y 117 del Código Penal y derogó el 112. Hizo dos cosas a la vez:

- **Eliminó la prisión** de la calumnia y la injuria, que quedaron solo en multa.
- **Sacó del ámbito penal las expresiones sobre asuntos de interés público y las que no sean asertivas.** El art. 109 vigente cierra: «En ningún caso configurarán delito de calumnia las expresiones referidas a asuntos de interés público o las que no sean asertivas». El art. 110 repite la fórmula para la injuria.

«El dólar no cerró a tal valor» o «esa norma no dice lo que el tuit afirma» son asuntos de interés público por definición. El veredicto sobre una afirmación de ese tipo está fuera del tipo penal desde 2009.

### El art. 113 y la eximente que el diseño aprovecha

El art. 113 responsabiliza a quien publica o reproduce el juicio ajeno «**siempre que su contenido no fuera atribuido en forma sustancialmente fiel a la fuente pertinente**». La cláusula es una eximente, y atribuir es literalmente entrar en ella.

**Por eso el nivel severo del indicador se enuncia atribuyendo a la fuente:**

> antes: ⚠ Probablemente falso · 87 %
> después: ⚠ **Contradicho por fuentes oficiales** · 87 %

No es cosmética. El sistema deja de afirmar y pasa a reportar qué dice la fuente, que además es lo que el sistema hace de verdad. Los tres niveles, los umbrales y el porcentaje **no cambian**: lo que cambia es el enunciado.

Se descartó el *score* desnudo. Rompe RNF-15 —un número pelado no es interpretable sin instrucción previa—, obliga a rehacer las capturas y los requerimientos de presentación, y **no baja el riesgo**: «87 % de probabilidad de desinformación» sigue siendo una imputación asertiva.

### El único flanco que la reforma no cierra: el juicio sobre la persona

Los arts. 109 y 110 exigen que la imputación recaiga sobre una **persona física determinada**, y la exención cubre lo que versa sobre asuntos de interés público. «El dólar no cerró a tal valor» es asunto público; «esta cuenta es poco confiable, es un bot» es una imputación asertiva sobre una persona determinada que no versa sobre asunto público alguno, y es exactamente lo que describe el art. 110.

**Por eso el Módulo 2 se enuncia como señales del contenido y no como juicio sobre quien publica:**

- El rótulo es **«Señales de la cuenta autora»**, no «credibilidad de la cuenta».
- El extremo inferior de la escala se describe como **«señales débiles de trayectoria pública»**, no como cuenta falsa ni automatizada.
- RF-03 enuncia el `score_source` como atributo del contenido evaluado.

El valor mostrado, el peso del 20 % en el ensamblado y el requerimiento no cambian. Lo que cambia es que el producto deje de blindar su enunciado más visible mientras afirma sobre una persona en el renglón de abajo.

### El art. 117 bis inc. 2, que el análisis anterior no citaba

Es la única pena de prisión que queda en el capítulo —seis meses a tres años— y su tipo describe la forma de este sistema:

> La pena será de seis meses a tres años, al que proporcionara a un tercero **a sabiendas** información falsa contenida en un archivo de datos personales.

**La defensa es «a sabiendas».** Un clasificador automático no obra a sabiendas: produce una estimación probabilística, la acompaña de la evidencia que la sostiene y declara explícitamente cuándo no la tiene. La exigencia de conocimiento del tipo penal no se satisface con un error de clasificación, y el diseño lo refuerza en tres puntos —RNF-06, que obliga a enlazar evidencia; RNF-07, que prohíbe el enunciado sentencioso; y el estado «sin contraste externo», que muestra la ausencia de evidencia como ausencia—.

El art. 117 permite además la retractación pública antes de contestar la querella, que exime de pena.

### Por qué el riesgo penal, en conjunto, es bajo

Cuatro defensas independientes, en orden de fuerza. Un análisis con cuatro patas vale más que uno que promete no decir «falso»:

1. **El juicio no es público.** El indicador lo inyecta el *content script* en el navegador de quien instaló la extensión. Con RNF-10 ampliado a toda entrega hacia terceros, no queda ninguna superficie donde un tercero vea el veredicto de un tuit atribuido a una cuenta identificable.
2. **La acción es privada.** El art. 73 inc. 1 pone las calumnias e injurias entre las acciones privadas, y agrega que la acción «podrá ser ejercitada sólo por el ofendido». Sin querella del ofendido no hay proceso, y no hay impulso fiscal de oficio.
3. **El enunciado atribuye a la fuente**, que es la eximente del art. 113.
4. **Versa sobre asuntos de interés público**, exento desde la Ley 26.551.

### Lo que esto prescribe sobre el diseño

Las prescripciones que reemplazan a «*score*, no veredicto»:

1. **Atribución fiel a la fuente** en el enunciado del veredicto severo.
2. **Evidencia enlazada obligatoria** para todo veredicto que afirme algo (RNF-06), y un estado propio y sin porcentaje —«sin contraste externo»— cuando no la haya.
3. **No asertividad sobre personas**: el Módulo 2 informa señales del contenido, no condición de la cuenta.
4. **Anonimización en toda entrega hacia terceros**, incluida la pantalla del panel (RF-15, RNF-10).

## Distribución de la extensión

**La extensión no se publica en la Chrome Web Store durante el PFI.** Se distribuye sin empaquetar, en modo desarrollador, para la demostración y la defensa. En una defensa se ve idéntica a una extensión publicada.

Es una decisión con consecuencias legales y no solo de presupuesto. Publicarla habría traído, de forma inevitable, una política de privacidad y una pantalla de consentimiento: Google cuenta como *user data* el «contenido y los recursos de los sitios web con los que el usuario interactúa», y aclara que el tratamiento local no exime. Las tres variantes de visibilidad —pública, no listada y privada— pagan el mismo cargo, pasan la misma revisión y exigen la misma política, así que no existía el modo intermedio que comprara alcance sin comprar obligaciones.

**Un choque que la decisión evita, y que conviene dejar anotado.** La exigencia de divulgación prominente y consentimiento en la interfaz que impone Google no se satisface con el argumento del art. 2 de la Ley 25.326: son dos ordenamientos distintos, y resolver la ley argentina no resuelve nada frente a la tienda. Al no publicar, el choque no se materializa. Si alguna vez se publica, hay que resolverlo.

El cargo único de registro de desarrollador queda en [[wiki/proyecto/recursos]] como costo diferido de lanzamiento, fuera del período del PFI.

## Los dos textos que la extensión muestra

Son entregables reales y son lo que sostiene la retención sin plazo: sin ellos, esa decisión se cae. Van en el *popup* de la extensión y en el panel web.

**Finalidad declarada:**

> Este sistema analiza publicaciones públicas de Twitter/X para estimar si contienen desinformación. Conserva el texto de la publicación, los datos públicos de la cuenta autora y el resultado del análisis con su evidencia, con dos finalidades: investigar y entrenar el modelo de clasificación, y mantener el historial agregado por cuenta que alimenta una de las señales del análisis. No se analizan cuentas protegidas ni mensajes directos. El resultado es una estimación con la evidencia que la respalda, no una verificación profesional ni un veredicto definitivo.

**Derecho de supresión:**

> Si sos autor de una publicación analizada por este sistema, podés pedir la supresión de tus datos escribiendo a la dirección de contacto del proyecto. El pedido se atiende dentro de los cinco días hábiles que fija el art. 16 de la Ley 25.326. La supresión elimina el nombre de usuario, los datos de la cuenta y el identificador de la publicación; el texto y el análisis se conservan disociados, sin ningún dato que permita atribuirlos a una persona.

Se difieren la política de privacidad en URL propia y la pantalla de consentimiento dentro de la interfaz. Las dos existen únicamente porque las exigiría la tienda, y no hay publicación.

## Lo que viene: la reforma en curso

La Ley 25.326 es de 2000 y su reglamentación de 2001. Hay reforma con estado parlamentario: sobre la base del anteproyecto de la Agencia de Acceso a la Información Pública, que perdió estado a fines de 2024, se presentaron varios proyectos, entre ellos el **1751-D-2026**, de 72 artículos, que deroga expresamente la 25.326 y su reglamentación. Incorporan responsabilidad proactiva, privacidad por diseño y por defecto, portabilidad y —lo que apunta directo a un sistema como este— el **derecho de oposición a decisiones automatizadas** que produzcan efectos jurídicos o afecten negativamente al titular.

**El sistema ya anticipa el núcleo de ese derecho sin que la ley se lo exija.** El veredicto no produce efecto jurídico alguno: no bloquea, no oculta ni restringe contenido. Es informativo, va acompañado de la evidencia que lo sostiene, declara cuándo no la tiene y admite que el usuario reporte un resultado incorrecto (RF-11), que es una forma de contradicción efectiva. No se incorpora como requerimiento funcional ni como pantalla, porque lo trae un proyecto que todavía no es ley y porque sin publicación no hay titulares que puedan ejercerlo.

## Ética del sistema, más allá de lo exigible

Tres compromisos que ninguna norma obliga y que el diseño sostiene igual, porque son la razón de ser del producto:

**El sistema no censura.** No oculta, no bloquea y no restringe nada. Inyecta información al lado del contenido y quien decide es la persona. Argentina no tiene ley específica sobre desinformación, y la ausencia de esa ley no se lee como una licencia sino como el motivo por el que la herramienta tiene que ser informativa y no correctiva.

**El error se declara.** El modelo puede marcar contenido satírico o irónico. La respuesta de diseño no es prometer que eso no pasa —no es eliminable— sino no presentar nunca el resultado con una autoridad que el sistema no tiene, y ofrecer el canal de reporte de RF-11.

**Los ejemplos del documento no señalan a nadie.** Las pantallas y los ejemplos usan contenido ficticio verosímil sobre temas argentinos reales, marcado como ilustrativo. El documento no atribuye desinformación a ninguna persona identificable.

## Normas citadas

URLs verificadas contra la fuente oficial el 2026-08-10.

| Norma | Qué aporta | Fuente |
|---|---|---|
| Ley 25.326 — Protección de los Datos Personales | Arts. 2, 4, 5, 11 y 16: definición, calidad, consentimiento, cesión y supresión | https://www.argentina.gob.ar/normativa/nacional/ley-25326-64790/actualizacion |
| Decreto 1558/2001 — Reglamentación | Reglamenta la Ley 25.326. No se lo cita en el análisis: se lista porque toda referencia a la ley remite a él, y porque es donde vive el umbral de inscripción de bases privadas que este apartado no desarrolla | https://www.argentina.gob.ar/normativa/nacional/decreto-1558-2001-70368/actualizacion |
| Ley 11.723 — Propiedad Intelectual | Reproducción y distribución de obras | https://www.argentina.gob.ar/normativa/nacional/ley-11723-42755/texto |
| Ley 11.179 — Código Penal (texto actualizado) | Arts. 73, 109 a 117 bis: acciones privadas y delitos contra el honor | https://www.argentina.gob.ar/normativa/nacional/ley-11179-16546/actualizacion |
| Ley 26.551 — Modificación del Código Penal | Sustituye los arts. 109, 110, 111, 113 y 117; deroga el 112 | https://www.argentina.gob.ar/normativa/nacional/ley-26551-160774/texto |

Los enlaces de la versión anterior de este archivo estaban rotos y devolvían normas ajenas: el de la Ley 25.326 traía un decreto laboral de 1992 y el del Código Penal una nota externa de aduana. Verificado y corregido.

## Referencias cruzadas

- [[wiki/proyecto/propuesta]]
- [[wiki/proyecto/recursos]]
- [[wiki/solucion/requerimientos]]
- [[wiki/solucion/modelo-datos]]
- [[wiki/solucion/arquitectura]]
- [[wiki/solucion/mockups]]
- [[wiki/datasets/dataset-recomendacion]]
- [[wiki/solucion/pipeline-preprocesamiento]]
