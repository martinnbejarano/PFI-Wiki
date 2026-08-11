# Log del Wiki PFI

> Registro cronológico append-only. Formato de cada entrada: `## [YYYY-MM-DD] tipo | descripción`
> Tipos: `setup` | `ingest` | `query` | `lint` | `update`

## [2026-08-11] update | Volcado del bloque de diseño a `chapter04.tex`

El capítulo tenía **diecinueve palabras y cinco `Completar.`** y es lo que efectivamente se evalúa el 22/08. Ahora tiene tres secciones escritas —modelo de datos, tecnologías con su arquitectura de red, y restricciones legales del diseño—, dos figuras apaisadas y tres tablas en formato del template. Quedan cuatro `Completar.`, que son las secciones fuera del alcance de este bloque: metodología, *datasets*, arquitectura del sistema y validación.

**Compila limpio.** `pdflatex`, `biber` y dos pasadas más: sin avisos de `biber`, sin referencias sin resolver, sin cajas desbordadas y sin citas sin definir. 47 páginas.

**El apartado legal va al capítulo de metodología y no al de introducción**, apartándose del mapa wiki→documento del `CLAUDE.md`, que manda `wiki/proyecto/` al Capítulo 1. La razón: ese análisis dejó de ser contexto normativo y pasó a ser la justificación de decisiones concretas de diseño. El artículo 4 inc. 7 explica por qué ninguna entidad lleva fecha de purga; el 16 explica qué tres atributos se borran; el 11 inc. 3 convierte la anonimización en un requerimiento imprescindible; el 113 determina la redacción del nivel severo. En la introducción, el lector encuentra el análisis veinte páginas antes que las decisiones que explica. La excepción queda registrada en `documento/history/04.tex`.

**Dos decisiones de formato que valieron una entrada en `considerations.tex`.** Los dos diagramas apaisados van en `landscape` al 95 % del ancho de línea: a ancho de texto vertical su tipografía interna es ilegible en papel. Y como `landscape` fuerza un salto de página, el bloque se ubica al **final** de su sección y no junto al párrafo que lo menciona — puesto en el medio dejaba media página en blanco.

**La adaptación de tono fue el trabajo real.** Voz impersonal, terminología unificada —«veredicto», «afirmación verificable», «fuente oficial», «medio de referencia»—, listas convertidas a prosa, ninguna de las frases prohibidas del `CLAUDE.md` y ninguna advertencia de contradicción del wiki. Los términos que en el wiki van en inglés se castellanizaron: *hash* pasa a «resumen» o «almacenada resumida», *scraping* desaparece del documento, *score* pasa a «puntaje».

**Se descomentó `chapter04` en `main.tex`.** Mientras el Capítulo 3 siga comentado, la metodología se imprime numerada como Capítulo 3. Es esperado y no produce referencias rotas: ninguna referencia cruzada del documento nombra el número de ese capítulo. Queda anotado en la bitácora.

## [2026-08-10] update | La ingesta de fuentes oficiales entra en la arquitectura, el presupuesto y los diagramas

`arquitectura.md:68` describía un enrutador que consultaba el sitio oficial dentro de la petición del usuario. **Esa consulta en vivo era incompatible con RNF-02**: `argentina.gob.ar` declara `Crawl-delay: 10` y el flujo a demanda dispone de ocho segundos. Una petición cada diez no entra en ese presupuesto, e ignorar el `crawl-delay` contradecía de plano la postura legal, que se apoya en respetar lo que cada sitio declara.

**Las seis fuentes se pre-indexan.** Una tarea programada de Railway arranca, recorre el catálogo respetando el `crawl-delay` de cada sitio, indexa los documentos nuevos, actualiza la fecha de la última corrida y termina. El enrutador del Módulo 3 pasa a buscar por similitud sobre ese índice. Las tres consecuencias son mejoras y no concesiones: RNF-02 se cumple con margen porque la consulta pasa a ser local, el `crawl-delay` se respeta de verdad porque la espera está fuera del camino crítico, y la postura legal se refuerza —acceso cortés y espaciado en lugar de una consulta sincrónica por cada tuit que alguien mire—.

**`recursos.md` tenía cuatro afirmaciones que dejaron de ser ciertas y una lista que contradecía a RF-06.** El *scraping* ya no corre en el mismo servidor del backend; los 512 MB de Railway no existen y el argumento pasa a ser de presupuesto; el cero de Vercel necesitaba su cláusula de uso no comercial; y el cargo de la Chrome Web Store se reclasifica como costo diferido con monto `[sin verificar]`, porque ninguna página de Google lo publica. **El total del período baja de USD 173 a USD 168.**

**Las dos listas de fuentes oficiales se unificaron.** `recursos.md` planificaba Infoleg, INDEC, Casa Rosada, ANMAT, BCRA y Chequeado; RF-06 decía InfoLEG, INDEC, BCRA, Boletín Oficial, MSal y MinEdu. Gana RF-06, que es la lista autoritativa: Casa Rosada queda cubierta por el Boletín Oficial y ANMAT por el Ministerio de Salud. **Chequeado sale** — responde 403 a todo cliente que no sea un navegador, y RF-07 se cubre con lo que el servicio de búsqueda ya tiene indexado.

**Cinco diagramas corregidos y los nueve reexportados.** `c4-contenedores`, `c4-componentes`, `flujo-informacion` y `despliegue-red` incorporan el componente de ingesta y el índice; `c4-contexto` deja de sugerir acceso directo a los sitios de los verificadores. De paso se corrigieron dos cosas que no eran del alcance pero contradecían decisiones ya tomadas: la nota de los 512 MB en el diagrama de contenedores y el rótulo «Módulo 2 — credibilidad», que pasa a «señales de la cuenta» en los tres diagramas donde aparecía.

**Correcciones mecánicas 2 y 3 de `decisiones-pendientes-2026-08.md`, aplicadas.** Serper.dev → Tavily en los cuatro archivos donde nombraba el servicio del PFI —se conservó «Serper/Google» donde describe el montaje del paper citado y no el nuestro— y el costo del período en `modelo-de-negocio.md`.

## [2026-08-10] update | `tecnologias.md` escrita: el criterio 5 en una sola página

Era un *stub* de abril con cuatro `[POR DEFINIR]`. Ahora es una página técnica pura —lenguajes, *frameworks*, versiones, librerías— con los costos enlazados a `recursos.md` y no repetidos.

**Todas las versiones fijadas y verificadas** contra el registro de paquetes el 2026-08-10, incluidas las cuatro que este trabajo agregó: TypeScript 7.0.2, Recharts 3.10.1, BeautifulSoup 4.15.0 y las seis del entorno de experimentación.

**La consecuencia más importante de la tabla es una separación, no una versión.** `transformers`, `torch` y `sentencepiece` viven en el entorno de experimentación y **no forman parte de la imagen que se despliega**: el contenedor de la API habla con Hugging Face por HTTP y su única dependencia de red es `httpx`. Meterlas en el contenedor sería deshacer la separación que sostiene todo el presupuesto de infraestructura.

**Las dos afirmaciones falsas del wiki quedan corregidas en la página.** Railway Hobby no tiene tope de 512 MB de RAM —son USD 5 con crédito de uso y facturación por consumo—, así que el argumento de por qué la inferencia vive afuera se reformula: **es un techo de presupuesto y no de memoria**. La conclusión no cambia; la premisa era verificable y falsa. Y el plan gratuito de Vercel prohíbe el uso comercial, lo que se resuelve con el mismo corte prototipo/producto que el proyecto ya aplicó dos veces: durante el PFI el panel no presta servicio comercial porque no hay cliente ni facturación.

**Los tres huecos que quedaban se cerraron en lugar de declararse.**

*El proveedor de identidad B2B tiene nombre:* Google Identity con OAuth 2.0 y OIDC, que es lo que la decisión de producto sobre identidad ya había fijado y que la arquitectura había dejado como «proveedor externo». No agrega costo, así que no toca RNF-14, y el `subject` que devuelve es exactamente lo que guarda `usuario_b2b.subject_idp`. Las plataformas de identidad como servicio se descartan por alcance: el momento de elegir una es cuando exista un cliente que pida inicio de sesión único.

*TypeScript también en la extensión,* empaquetada con Vite en varias entradas y el manifiesto mantenido a mano. El tipado paga sobre todo en el *content script*, que lee un DOM ajeno que cambia sin aviso: una propiedad que desaparece se ve al compilar y no durante la demostración. Se descartó sumar un complemento específico para extensiones — son tres entradas y un JSON.

*Recharts para RF-24,* porque se declara como componentes de React. Chart.js dibuja sobre `canvas` y obliga a sincronizar el ciclo de vida a mano para ganar un rendimiento que dos gráficos no necesitan.

**La arquitectura de red se escribió entera**, que es la mitad del criterio 5 que ninguna página cubría: las cinco zonas con su grado de control, TLS 1.3 en todo cruce, la red privada donde viven API, ingesta y base sin puerto público, la autenticación por frontera —la extensión no se autentica, el cliente B2B usa clave hasheada con prefijo en claro, el analista va contra el proveedor de identidad— y qué dato exacto cruza cada límite.

## [2026-08-10] update | Requerimientos reescritos con las decisiones de agosto

Aplicadas de una vez las correcciones que dejaron pendientes tres decisiones, para no tocar `requerimientos.md` tres veces y arriesgar que las tablas queden desincronizadas entre sí. Quedan **29 funcionales y 17 no funcionales**.

**RNF-08 prometía lo imposible.** Comprometía «sin dirección IP», que ninguna API sobre HTTPS puede cumplir porque el protocolo la entrega en cada petición. El enunciado nuevo distingue **recibir de persistir**, que es la distinción que se puede sostener y verificar.

**RNF-06 era incumplible y el propio diseño lo incumplía por tres caminos.** El estado *sin contraste externo* lo repara: cuando ningún módulo externo encontró fuente, el indicador se emite igual pero como ausencia declarada y sin porcentaje, en lugar de vestirse de veredicto. La consecuencia que hay que tener presente en la exposición: **el flujo automático ya no emite ninguno de los tres niveles sobre un tuit que ve por primera vez**, porque solo corrió el Módulo 1 y no hay ninguna fuente que enlazar. El indicador sigue apareciendo en dos segundos —RNF-01 vive— pero como marca de atención. El veredicto con nivel y porcentaje aparece con el acierto de caché o con CU-02.

**RNF-07 cambió de objeto.** Dejó de prescribir «probabilidad y no sentencia» —que mitigaba un riesgo cerrado en 2009 y empujaba hacia un *score* desnudo que rompe RNF-15— y pasa a prescribir sobre qué se enuncia y a quién se atribuye.

**Tres requerimientos nuevos.** RF-28, el índice local de fuentes oficiales que mantiene la ingesta periódica, sin el cual RF-06 describía una consulta en vivo incompatible con RNF-02. RF-29, los dos textos de cara al usuario, que son lo que sostiene la retención sin plazo. Y RNF-17, la regla de respetar el `robots.txt` de cada destino y no eludir bloqueos deliberados, que es lo que vuelve auditable la postura sobre la obtención de datos sitio por sitio en lugar de pedirle confianza al lector.

**`parcial` y *sin contraste externo* conviven porque son cosas distintas**: uno marca que un módulo no pudo correr, el otro que corrió y no encontró. Por eso el flujo alternativo *4a* de CU-02 —no hay afirmación verificable— dejó de marcarse como análisis parcial: ningún módulo falló.

**RF-24, RF-25 y RNF-10 dicen «entrega» y no «exportación».** El panel mostrado a un analista de otra organización es una entrega hacia un tercero tanto como un archivo descargado, y era la superficie que la redacción anterior dejaba afuera.

**Los mockups se actualizaron y se recapturaron,** porque dejarlos diciendo «Probablemente falso» mientras el requerimiento dice otra cosa es exactamente la desincronización que este trabajo evita. Cambiaron tres cadenas —el rótulo del nivel severo, el del Módulo 2 y el KPI del panel— y sus pies de figura. También `metodologia-tecnica.md`, donde el extremo inferior de la escala del Módulo 2 decía «fuente no confiable (bot, fake account)» y ahora dice «señales débiles de trayectoria pública»: es el único enunciado del proyecto que afirmaba sobre una persona determinada, y es el flanco que la reforma de 2009 no cubre.

## [2026-08-10] update | Apartado legal reescrito entero

`wiki/proyecto/restricciones-legales-eticas.md` era un borrador del 19/04 que contradecía el diseño en seis puntos y omitía los artículos que sostienen la defensa. Se reescribió completo, **organizado por acto y no por norma**: cada cosa que el sistema hace tiene su riesgo y su defensa, y meterlas todas en una matriz de semáforos es lo que lo volvía indefendible.

**El hallazgo que dio vuelta el análisis: la Ley 26.551.** Dictada en 2009 en cumplimiento de *Kimel vs. Argentina*, eliminó la prisión de la calumnia y la injuria y sacó del ámbito penal «las expresiones referidas a asuntos de interés público o las que no sean asertivas». El archivo venía prescribiendo «*score*, no veredicto» para mitigar un riesgo que la ley había cerrado hace diecisiete años, y a cambio destruía la interpretabilidad del producto. Los tres niveles y los umbrales se conservan; **cambia el enunciado del nivel severo**, que pasa a atribuir a la fuente —«Contradicho por fuentes oficiales»— y con eso entra en la eximente del art. 113.

**El único flanco que la reforma no cierra es el juicio sobre la persona,** y por eso el Módulo 2 se reetiqueta: «Señales de la cuenta autora» en lugar de «Credibilidad de la cuenta», y «señales débiles de trayectoria pública» en lugar de «cuenta no confiable, bot». El valor, el peso y RF-03 no cambian. Con el indicador atribuyendo a la fuente y el renglón de abajo afirmando sobre una persona, el producto blindaba su enunciado más visible y dejaba expuesto el único que ninguna eximente cubre.

**El art. 117 bis inc. 2 no estaba citado y es la única pena de prisión del capítulo** — seis meses a tres años para quien proporcione a un tercero «a sabiendas» información falsa contenida en un archivo de datos personales. La defensa es «a sabiendas»: un clasificador automático no obra a sabiendas.

**La cesión del art. 11 se escribe como el punto expuesto y no como un riesgo resuelto.** La mitigación está en el propio artículo —el inc. 3.e exime cuando media disociación que vuelve inidentificables a los titulares— y es lo que implementan RF-25 y RNF-10, este último ampliado de «exportación» a toda entrega hacia terceros, incluida la pantalla del panel. Se decidió **no** apoyarse en el inc. 3.b, que remite a las excepciones del art. 5: es discutible y dejaría en pie la responsabilidad solidaria del inc. 4.

**Las tres modalidades de obtención de datos se separan.** La lectura del DOM no es *scraping* —el contenido ya fue entregado al navegador del usuario— y el incumplimiento de términos de servicio es contractual, con un riesgo acotado y nombrado: la suspensión de la cuenta del usuario. Los sitios del Estado se justifican uno por uno contra su `robots.txt` verificado, y el del BCRA autoriza expresamente a los rastreadores de entrenamiento de IA. Chequeado sale del alcance porque bloquea por infraestructura. La API de X queda descartada por diseño y no por precio: ningún nivel vende el *timeline* de un usuario.

**Los dos enlaces legales del archivo estaban rotos y devolvían normas ajenas** —un decreto laboral de 1992 y una nota externa de aduana—. Las cinco URLs de la tabla nueva están verificadas contra la fuente oficial, y los textos de los artículos citados se contrastaron literalmente antes de escribirlos. Las mismas entradas se sumaron a `documento/biblio.bib` como `@online`, más la sentencia de la Corte IDH.

**No hay apartado de inscripción ante la AAIP.** Es decisión del autor, registrada en el ticket #15: sin publicación no se cruza el umbral, y el análisis del Decreto 1558/2001 queda archivado en su ticket por si el criterio cambia.

## [2026-08-10] update | Modelo de datos: diecisiete entidades y el DER

Escrita `wiki/solucion/modelo-datos.md` y dibujado `der.drawio`, con lo que se cierra la mitad del criterio 6 y se reparan tres enlaces rotos —`requerimientos.md`, `arquitectura.md` en dos lugares— que apuntaban a una página inexistente.

**Son diecisiete y no catorce, y el número es una consecuencia y no un objetivo.** El «catorce» de `plan-bloque-diseno.md` era una foto de abril, y la regla de corte —toda entidad trazable a un RF— no puede garantizar un número. La ingesta asíncrona trajo `fuente_oficial`, RF-09 trajo `razon`, RF-27 trajo `configuracion_ensamblado` y la evidencia se partió en `documento` más `evidencia`. La definición de terminado del plan se corrigió: el número de entidades sale de ahí.

**La evidencia se parte en dos y eso resuelve tres cosas de una vez.** `documento` guarda lo que es propiedad del documento —URL, texto, vector—; `evidencia` es la tabla puente y guarda lo que es propiedad del vínculo con un análisis: postura, similitud y extracto. Así un documento sostiene varios análisis sin duplicar texto, hay un solo índice HNSW en lugar de tres —absorbe el índice de fuentes oficiales y el corpus de verificaciones previas, con `tipo_fuente` como discriminador— y RF-13 se resuelve con un `ORDER BY` en lugar de una unión de tres tablas. `desmentida` desaparece.

**El seudónimo del panel B2B es el serial que la tabla ya tenía.** RNF-10 pide que ninguna entrega a terceros lleve el `@` en claro y la supresión manda borrarlo. Agrupar por `cuenta.id_cuenta` es irreversible por construcción y no por fuerza criptográfica, sobrevive a la supresión sin comprometerla y no obliga a gestionar ningún secreto. Reemplaza la propuesta previa de un HMAC con clave del servidor.

**La disociación se cierra por los dos agujeros que quedaban abiertos.** `tuit.url` no se persiste —se reconstruye como `x.com/i/status/{id_nativo}`, que redirige— y `id_nativo` se borra en la supresión. El costo queda escrito: esa fila puntual pierde reproducibilidad, el resto del corpus no.

**Decisión de dibujo.** El DER lleva las entidades y las relaciones con su cardinalidad; los atributos viven en las tablas de la página. Un DER con atributos dentro de cada caja se vuelve ilegible impreso a partir de la docena de entidades, y la tabla permite además declarar tipo y nulabilidad, que es donde está la mitad de las decisiones de diseño. El dominio se identifica por color, con referencia en el propio diagrama.

**Hallazgo colateral: `_tools/exportar.py` tenía la ruta de destino mal.** Calculaba `parents[3]`, que resuelve a `wiki/`, y creaba un `wiki/documento/chapters/figures/` fantasma en lugar de escribir en el del documento. Corregido a `parents[4]`. Las ocho exportaciones anteriores habían quedado bien porque se hicieron con el script en otra ubicación.

## [2026-08-13] update | Los ocho diagramas revisados y exportados a figures/

Revisados visualmente uno por uno y exportados a `documento/chapters/figures/`. No hizo falta draw.io de escritorio: se renderizan con el visor web en Chrome *headless*, se inspecciona el PNG y se corrige el `.drawio`. El XML viaja en el fragmento de la URL, así que nunca sale de la máquina. El *toolchain* quedó versionado en `wiki/assets/diagramas/_tools/`.

Siete de los ocho tenían defectos. **Que los ocho validaran sin aristas huérfanas no significaba que estuvieran bien**: la validación estructural no ve un título tapado por una etiqueta ni una arista que atraviesa tres cajas.

**Dos hallazgos que no son cosméticos:**

*El diagrama de flujo tenía un error de modelado.* Mostraba el Módulo 2 y el Módulo 3 en cadena, como si el segundo esperara al primero. Son independientes: ninguno necesita el resultado del otro y el Módulo 4 espera a los dos. Ahora van como bifurcación paralela UML, que además ordena el dibujo — las fuentes externas quedaron alineadas bajo el módulo que las consulta.

*Los mensajes del actor en los diagramas de secuencia salían en diagonal.* La línea de vida del actor usaba una forma con geometría propia y rotada, así que las fracciones de posición no coincidían con las del resto. Un mensaje inclinado en un diagrama de secuencia sugiere que ocurre en un instante distinto en cada extremo, que es exactamente lo que no pasa.

El resto: en `c4-componentes` los títulos de M2 y M4 quedaban ilegibles bajo etiquetas de arista y dos aristas atravesaban cajas; en `c4-contenedores` la etiqueta hacia Hugging Face tapaba el texto de la API; en `despliegue-red` el título de la Zona 4 quedaba pisado; en `casos-de-uso` la etiqueta de *Sistema cliente* caía sobre la cabeza del *Analista B2B*. Solo `c4-contexto` salió limpio.

Se intentó exportar a PDF vectorial con `--print-to-pdf`, pero Chrome imprime en tamaño carta y recorta el contenido. Quedó en PNG a 3x recortado al contenido: entre 2.700 y 4.100 px de ancho, suficiente para impresión.

## [2026-08-13] update | Pipeline de preprocesamiento reescrito hacia XLM-T

Cerrada la **Decisión 3** de [[wiki/sintesis/decisiones-pendientes-2026-08]]. Se eligió la Opción B —reescribir en lugar de poner un aviso— porque, ratificada la Decisión 1, el riesgo de tener que rehacerlo desapareció.

**El principio se invirtió.** La página describía un preprocesamiento pensado para BETO: remover emojis, menciones y hashtags, y pasar todo a minúsculas. Es correcto para un modelo entrenado sobre Wikipedia y es lo peor posible para uno entrenado sobre tuits. Ahora la regla es: **preprocesar es adaptarse al pre-entrenamiento del modelo, no "limpiar" el texto**. Se conservan emojis, mayúsculas, signos repetidos y números; se normalizan URLs a `http` y menciones a `@usuario`; se segmentan los hashtags. La función de limpieza pasó de doce líneas a cinco.

Hay una segunda razón, específica de esta tarea y que la versión anterior pasaba por alto: el emoji, la exclamación repetida y la mayúscula sostenida **son la señal**. El Módulo 1 clasifica registro sensacionalista, no contenido factual. Borrarlos elimina exactamente lo que tiene que detectar.

**Lo más importante apareció al reescribir y no estaba en el diagnóstico del 08/08.** La recomendación anterior de reemplazar los números por un token `<NUM>` no es una optimización discutible: en este dominio es un error grave. Con `<NUM>`, «cerró 500 escuelas» y «cerró 50 escuelas» son la misma entrada para el modelo — y esa diferencia es precisamente la afirmación que el sistema tiene que detectar, el ejemplo que recorre toda [[wiki/solucion/metodologia-tecnica]]. Los números se conservan.

Dos agregados menores pero con consecuencias: RoBERTuito es *uncased* y necesita su propio preprocesamiento al evaluarlo, porque aplicarle el de XLM-T arruinaría la comparación de forma silenciosa; y `score_nlp` debe ser la probabilidad de la clase *falso*, no la confianza del argmax, que invertiría el veredicto cuando el modelo está seguro de que el contenido es verdadero.

Corregida la errata `dcc-uchile/bert-base-spanish-wwm-uncased`, identificador que no existe: la organización en Hugging Face es `dccuchile`, sin guion.

La función `preprocesar` se ejecutó y produce la salida documentada. La partición exacta del tokenizador quedó sin ejecutar —`transformers` no está instalado en este entorno— y por eso la página no afirma un resultado concreto.

## [2026-08-13] update | Ratificado XLM-T como modelo principal del Módulo 1

Cerrada la **Decisión 1** de [[wiki/sintesis/decisiones-pendientes-2026-08]], abierta desde el health-check del 08/08. Se adoptó la Opción C: `cardiffnlp/twitter-xlm-roberta-base` (XLM-T) como modelo principal, con RoBERTuito y BETO como líneas de comparación.

**Qué la destrabó.** Una contradicción concreta: `arquitectura.md`, escrita el 12/08, ya decía XLM-T mientras el resto del wiki y `chapter02.tex` seguían diciendo RoBERTuito principal.

**El argumento no fue de rendimiento sino de datos.** Los ~40.000 ejemplos anotados de LIAR y FakeNewsNet están en inglés y **solo son utilizables con un modelo multilingüe**. Con uno monolingüe el entrenamiento se reduce a FakeDeS (971 ejemplos) más el corpus argentino por construir, y todo el riesgo se traslada a la Entrega 4. XLM-T es el único candidato que conserva la transferencia sin renunciar al registro de Twitter: es XLM-RoBERTa con pre-entrenamiento continuado sobre ~198M de tuits.

**La contra, declarada.** Gouliev et al. (2025) reportan 8–12 puntos de caída de los multilingües frente a los nativos del idioma. Se asume porque esa medición es sobre multilingües *genéricos* y XLM-T está adaptado al dominio — pero eso es plausibilidad, no demostración, y por eso la comparación experimental contra RoBERTuito se mantiene. Si contradice la elección, la elección se revierte.

**La oración que había que reescribir sí o sí.** `chapter02.tex:214` usaba a Albtoush et al. (2025) para sostener que los modelos específicos del idioma superan a los multilingües, con RoBERTuito de ejemplo. Ratificar un modelo de linaje multilingüe sin tocarla dejaba el capítulo contradiciéndose solo. Reformulada sobre el eje **adaptación frente a propósito general**, que es lo que el hallazgo de Albtoush realmente sostiene y que admite tanto a los monolingües en español como a los multilingües adaptados al dominio.

**Cayó de arrastre la Decisión 2:** eliminado el *ensemble* de dos modelos de `modelos-espanol.md`, obsoleto desde el acotamiento del alcance del 13/06. Un solo clasificador saca además un servicio de inferencia del despliegue.

**No se tocó** lo que reporta resultados de terceros: las mediciones de Toapanta et al. (2024) quedan como están, en el wiki y en el documento.

Dos correcciones que aparecieron en el barrido: `drchal-2024-pipeline-multiidioma.md:52` afirmaba que el PFI usa "modelos nativos en español con datos de entrenamiento en español", que ya no es cierto; y `chapter01.tex:23` enumeraba tres arquitecturas candidatas sin incluir la elegida, así que se sumó XLM-T conservando la redacción agnóstica.

`main.pdf` y `history.pdf` compilan sin referencias ni citas sin resolver. Nueva entrada de bitácora en `documento/history/03.tex`.

## [2026-08-13] update | Flujo de información, secuencias y despliegue: los ocho diagramas del bloque

Generados `flujo-informacion.drawio`, `secuencia-cu01.drawio`, `secuencia-cu02.drawio` y `despliegue-red.drawio`. Con estos cierran el criterio 3 y la parte de *arquitectura de red* del criterio 5. Los ocho `.drawio` del repositorio validan sin aristas huérfanas.

**Flujo de información — actividad UML con calles.** Dos entradas (el tuit que aparece en pantalla y el clic sobre el indicador) que convergen en la consulta de caché y recién después se separan por origen del pedido. Del nodo de medios salen **dos** aristas hacia la evaluación de postura: una pasa por los verificadores y la otra los saltea. La segunda es el camino frecuente, y dibujarla es lo que deja constancia de que la ausencia de verificación previa no degrada el resultado.

**Secuencia: dos diagramas, no uno.** Superponer los dos flujos exigía ocho líneas de vida con fragmentos anidados, ilegible impreso. `secuencia-cu01` tiene seis líneas de vida, un `alt` de caché y un `opt` para el fallo de la inferencia que se resuelve en silencio —no se pinta indicador ni se muestra error, porque el usuario no pidió nada—. `secuencia-cu02` tiene diez, con el Módulo 3 abierto en sus tres fuentes y el `alt` de degradación al final. Separarlos refuerza que RNF-01 y RNF-02 son números distintos por diseño.

**Despliegue: cinco zonas de confianza.** Equipo del ciudadano, organización B2B, borde CDN, nube de la aplicación y terceros. **Tres de las cinco están fuera de todo control del proyecto**, y enunciado así RNF-11 deja de parecer una cláusula de estilo. Lo que vuelve útil al diagrama son los cruces de límite: el `@` del autor saliendo hacia la API (art. 5 inc. 2.b), el texto del tuit saliendo hacia el servicio de inferencia, la afirmación extraída —no el tuit crudo— saliendo hacia las fuentes de evidencia, y la única arista que transporta datos hacia afuera del sistema, la exportación B2B, que sale anonimizada porque es una cesión del art. 11. El argumento legal deja de ser un párrafo y se vuelve dibujo.

**Registrado como pendiente manual:** ninguno de los ocho `.drawio` fue abierto todavía en draw.io. Falta el ajuste de posición y la exportación a `documento/chapters/figures/`. Queda con checklist por archivo en `plan-bloque-diseno.md`.

Corregidas de paso dos inconsistencias del plan del bloque: decía «seis diagramas» cuando son ocho, y su definición de terminado ubicaba las capturas de mockup en `raw/assets/mockups/`, contradiciendo la convención que el propio archivo fija diez líneas antes. `raw/` es inmutable.

## [2026-08-12] update | Modelo C4 en tres niveles y arquitectura reescrita (criterio 3 de EP2)

Reescrita `wiki/solucion/arquitectura.md`, que era el *stub* de abril con `[POR DEFINIR]`. Generados `c4-contexto.drawio`, `c4-contenedores.drawio` y `c4-componentes.drawio` en `wiki/assets/diagramas/`. Los cuatro `.drawio` del repositorio validan sin aristas rotas.

**Nivel 1 — contexto.** Dos personas y **siete sistemas externos**. Documentar esa dependencia con su modo de falla es lo más útil que salió del diagrama: Twitter/X es estructural —si cae no hay producto—, Hugging Face deja mudo el flujo automático, y las fuentes de evidencia degradan a análisis parcial. La jerarquía de evidencia quedó dibujada: oficiales y medios en verde con línea continua, verificadores con línea punteada.

**Nivel 2 — contenedores.** Extensión (Manifest V3), panel web (React sobre Vercel), API REST (FastAPI sobre Railway), PostgreSQL con `pgvector`, y la inferencia en Hugging Face como contenedor externo. La separación entre *content script* y *service worker* no es un detalle de implementación: el primero corre en el hilo de la página y por eso RNF-04 le pone 50 ms de techo por tuit. Todo lo que no sea leer el DOM e inyectar el indicador tiene que ocurrir en el *service worker*.

**Nivel 3 — componentes de la API.** Dos endpoints separados y no uno parametrizado, porque el contrato B2B es un producto con precio y no debería moverse cuando cambia la extensión. El orquestador es donde vive la decisión de los dos flujos y también el que marca el resultado como parcial, en lugar de dejar que el ensamblador promedie sobre datos faltantes. El Módulo 3 quedó abierto en cinco componentes cuya disposición **es** la jerarquía de evidencia: enrutador de fuentes oficiales y cliente de medios siempre activos, buscador vectorial de verificaciones previas con línea punteada porque es opcional.

**Ocho decisiones de arquitectura** documentadas con sus alternativas evaluadas —dos flujos, inferencia separada, Railway, `pgvector`, panel estático, identidad en dos niveles, autenticación delegada y degradación a parcial—. La tabla es lo que responde el criterio 5 de la rúbrica cuando pide justificar y no solo enumerar.

**Declarado como pendiente de la Entrega 4:** esquema de reintentos y *timeouts* por servicio externo, política de expiración del caché, y versionado del contrato de la API B2B.

## [2026-08-11] update | Jerarquía de evidencia: los medios pasan a ser la columna vertebral del contraste

Corrección de diseño pedida por el usuario y aplicada en cuatro capas. El sistema apoyaba el Módulo 3 demasiado en Chequeado, tanto en los ejemplos de `metodologia-tecnica.md` como en los requerimientos y los mockups recién escritos.

**La jerarquía queda establecida como fuentes oficiales → medios de referencia → verificadores**, con la justificación documentada en `metodologia-tecnica.md`:

- Los **verificadores** cubren pocas afirmaciones por día y publican con días de demora. El propio `modelo-de-negocio.md` identifica ese cuello de botella como el problema que el proyecto resuelve — no puede ser también su fuente principal de verdad. La desinformación que interesa detectar es, por definición, la que todavía nadie verificó.
- Los **cinco medios de referencia** (Infobae, Clarín, La Nación, Página/12, Télam) cubren cualquier tema con relevancia pública en horas, dan consenso —una afirmación contradicha por tres redacciones independientes es señal fuerte— y publican con URL estable. La contrapartida, sus líneas editoriales, se mitiga construyendo la señal sobre el consenso de varios y nunca sobre uno solo.

**Cambios concretos:**

- `metodologia-tecnica.md`: nueva sección "Jerarquía de evidencia" con tabla de cobertura y latencia por clase de fuente; los tres casos de uso y el ejemplo end-to-end reescritos para arrancar por la fuente oficial y los medios.
- `requerimientos.md`: RF-05 pasa a ser medios de referencia y RF-06 fuentes oficiales, ambos imprescindibles; los verificadores bajan a RF-07 con prioridad *importante*. Nuevo **RF-09**: cada razón derivada de evidencia externa debe llevar el enlace a la fuente que la respalda. RF-13 ordena el panel por jerarquía. Flujos alternativos de CU-02 reescritos: la ausencia de cobertura en los cinco medios es en sí misma una señal, y la ausencia de verificación previa es el caso frecuente y no degrada el análisis.
- **Renumeración**: los RF-09 a RF-26 originales corrieron a RF-10 a RF-27. Total: 27 requerimientos funcionales. Propagada a `mockups.md`, `mockups.html`, `plan-bloque-diseno.md` y este log.
- `mockups.html`: la línea de motivo del indicador ahora **nombra las fuentes** en lugar de contarlas; las razones del popup llevan enlace por razón, separando visualmente lo que el sistema encontró (con enlace) de lo que infirió (etiqueta gris); el panel de evidencia se reordenó a oficiales → medios → verificaciones, se sumó Télam y la verificación de Chequeado quedó última con su fecha visible.

## [2026-08-11] update | Mockups del frontend (criterio 2 de la rúbrica EP2)

Creadas `wiki/solucion/mockups.md` y `wiki/assets/mockups/mockups.html`, con las capturas en `wiki/assets/mockups/*.png` copiadas a `documento/chapters/figures/`.

Cuatro pantallas en un único archivo autocontenido, conmutables con `?pantalla=` y con las flechas del teclado. Construidas en HTML y CSS reales en lugar de dibujadas: la extensión del Bloque 3 hereda este marcado, así que el *mockup* y la demo son un solo trabajo. Las capturas se generan con Chrome en modo *headless* a doble resolución, con `&captura=1` para esconder la barra de navegación del prototipo.

Todo el contenido es ficticio y cada pantalla lo rotula visiblemente, para que el documento no señale a ninguna cuenta identificable como fuente de desinformación.

**Las cuatro pantallas y qué decisión encarna cada una:**

1. **Indicador sobre el tuit** (RF-11, CU-01) — los cuatro estados. El estado se comunica por color, forma del ícono y texto a la vez, para no depender de la percepción del color (RNF-15). Ningún indicador afirma falsedad: el más severo dice *probablemente* y expone el porcentaje, que es RNF-07 hecho pantalla.
2. **Detalle del veredicto** (RF-12 y RF-14, CU-02) — dos estados en la misma imagen: el flujo principal con el desglose por módulo, y el flujo alternativo *6a* cuando la búsqueda web no responde. En el parcial no hay porcentaje sino un guión, y la barra del módulo faltante aparece rayada. Es RNF-11: la ausencia de un módulo se muestra como ausencia, no se disimula con aritmética.
3. **Panel de evidencia** (RF-13, CU-03) — seis fuentes agrupadas por tipo y etiquetadas por postura, con la afirmación extraída visible arriba de todo. Se incluyeron a propósito una fuente que corrobora parcialmente y otra neutral: un panel donde todo apunta al mismo lado es un panel de confirmación, no de evidencia.
4. **Panel de tendencias B2B** (RF-24 y RF-25, CU-07) — con la columna de cuentas hasheada, porque un *mockup* que mostrara los `@` en claro contradiría el apartado legal del propio documento.

**Pendiente declarado:** no hay pantalla de reporte de falso positivo, con lo cual CU-04 no tiene respaldo visual; tampoco hay estados de error más allá del análisis parcial. Ninguno afecta a los ocho criterios de la rúbrica.

## [2026-08-09] update | Requerimientos y casos de uso (criterio 1 de la rúbrica EP2)

Reescrita `wiki/solucion/requerimientos.md`, que era un *stub* de abril con `[POR DEFINIR]`. Primer artefacto del bloque de diseño.

**26 requerimientos funcionales** con prioridad MoSCoW, en cinco grupos: detección y análisis (RF-01 a RF-10), presentación (RF-11 a RF-16), retroalimentación (RF-17 a RF-19), plataforma B2B (RF-20 a RF-25) y persistencia y trazabilidad (RF-26 y RF-27).

**16 requerimientos no funcionales**, cada uno con un valor verificable en lugar de un adjetivo. Los que no son genéricos sino consecuencia de decisiones ya tomadas:

- **RNF-01 y RNF-02 comprometen latencias distintas** (2 s y 8 s en percentil 95) porque el análisis ocurre en dos flujos. Con un solo flujo habría un solo número y tendría que ser el peor de los dos.
- **RNF-07** —comunicar probabilidad, nunca sentencia— es la mitigación del riesgo de falsos positivos ante sátira e ironía que declara la propuesta. El error no es eliminable; la respuesta de diseño es no presentar el resultado con una autoridad que el sistema no tiene.
- **RNF-09** ancla el tratamiento de contenido de terceros en el art. 5 inc. 2.b de la Ley 25.326 y excluye expresamente cuentas protegidas y mensajes directos.
- **RNF-11** exige análisis parcial identificado ante la caída de cualquiera de los cuatro servicios externos, en lugar de un veredicto calculado con módulos faltantes.
- **RF-25 y RNF-10** son la mitigación del art. 11 (cesión a terceros): toda exportación B2B sale agregada o anonimizada. RF-25 quedó como imprescindible aunque el resto del grupo B2B es importante, porque si la plataforma existe ese requerimiento no es opcional.

**Siete casos de uso** desarrollados con actor, precondición, flujo principal, flujos alternativos y postcondición: CU-01 análisis automático del *timeline* (actor de sistema), CU-02 análisis profundo a demanda, CU-03 consulta de evidencia, CU-04 reporte de veredicto incorrecto, CU-05 histórico personal, CU-06 consumo de la API y CU-07 panel de tendencias.

Los flujos alternativos son la parte que más trabajo dio y la que más sirve después: el tuit sin texto analizable, la afirmación no verificable, la ausencia de verificaciones previas, la caída de la búsqueda web y el acierto de caché son los que van a fijar los estados del diagrama de secuencia y las pantallas de los mockups.

**Diagrama de casos de uso** generado en `wiki/assets/diagramas/casos-de-uso.drawio`: cuatro actores —Ciudadano, Extensión y Sistema cliente como actores de sistema, y Analista B2B—, los siete casos de uso dentro del límite del subsistema, y dos relaciones `<<include>>` (CU-02 incluye a CU-01, CU-03 incluye a CU-02). Queda el ajuste visual y la exportación.

**Convención de ubicación de artefactos gráficos:** fuentes `.drawio` en `wiki/assets/diagramas/`, exportaciones en `documento/chapters/figures/` (donde las busca `\includegraphics`), capturas de mockups en `wiki/assets/mockups/`. Nada de esto va en `raw/`, reservado para fuentes originales inmutables.

**Matriz de trazabilidad** CU ↔ RF incluida, que funciona además como regla de corte del modelo de datos: toda entidad tiene que ser trazable hasta un requerimiento. RF-16 y RF-19 quedan sin caso de uso asociado por ser opciones de configuración, ambos de prioridad deseable.

## [2026-08-08] update | Plan detallado del bloque de diseño y ocho decisiones de producto

Creada `wiki/proyecto/plan-bloque-diseno.md`. Los Bloques 1 y 2 de `plan-entrega-50.md` se **fusionan** en un tramo único del 9 al 14/08: los mockups le dan retroalimentación a los casos de uso y el modelo de datos recién se estabiliza cuando los tres artefactos convergen. El 15 y 16 quedan de colchón antes del bloque de la demo.

**Ocho decisiones de producto que bloqueaban los tres artefactos a la vez:**

1. **Modo de análisis híbrido.** El Módulo 1 corre automático sobre los tuits visibles; los Módulos 2, 3 y 4 solo al hacer clic. La búsqueda web del Módulo 3 cuesta dinero y tarda segundos por tuit. Consecuencia: hay **dos flujos**, y eso atraviesa el diagrama de secuencia, el de flujo de información y el campo `origen` de la tabla de análisis.
2. **Identidad en dos niveles.** Extensión ciudadana anónima con UUID local; clientes B2B con cuenta de organización (Google OAuth) y clave de API. Es lo que ya decía el Business Model Canvas de `modelo-de-negocio.md`, que no estaba reflejado en ninguna página de solución.
3. **Persistencia completa, con el `@` del autor en claro.** Habilita el Módulo 2 (que necesita metadatos de cuenta) y el corpus argentino de la E4.
4. **Defensa legal partida en dos.** La recolección se ampara en el art. 5 inc. 2.b de la Ley 25.326 (fuentes de acceso público irrestricto). El punto realmente expuesto no es recolectar sino **ceder**: vender el dataset a un medio cae bajo el art. 11, y se mitiga exportando agregado o anonimizado. Obliga a reescribir la matriz de riesgo de `restricciones-legales-eticas.md:29-30`, que hoy propone hashear el identificador y por lo tanto contradice el diseño.
5. **Diagramas en draw.io**, con el `.drawio` generado como XML versionado en git y el ajuste visual manual.
6. **Mockups en HTML y CSS reales**, capturados desde Chrome: el mismo marcado es el punto de partida de la extensión del Bloque 3, así que mockup y demo son un solo trabajo.
7. **`pgvector` sobre el PostgreSQL de Railway**, con Qdrant y Pinecone documentados como alternativas evaluadas. `pgvector` implementa HNSW igual que un motor dedicado; la ventaja de los dedicados aparece arriba del millón de vectores, y el prototipo va a tener decenas de miles. Documentar la comparación puntúa para el criterio 5.
8. **Contenido ficticio verosímil en los mockups**, para que el documento no señale a ninguna cuenta identificable como fuente de desinformación.

**Alcance del bloque:** requerimientos funcionales agrupados por módulo de producto y no funcionales con un número por categoría; siete casos de uso con flujos alternativos; cuatro pantallas de mockup; seis diagramas más el de casos de uso; DER de catorce entidades en cuatro dominios (contenido, análisis, uso ciudadano, plataforma B2B).

## [2026-08-08] update | Plan de trabajo de los 14 días hasta la entrega del 50%

Creada `wiki/proyecto/plan-entrega-50.md`. Cinco bloques ordenados por **dependencia**, no por importancia: de los casos de uso salen los mockups, los diagramas y el modelo de datos, así que empezar por otro lado obliga a rehacer.

- **Bloque 0 (8-9/08)** — lo que depende de terceros: reactivar la encuesta con intercambio de respuestas en el grupo del curso, mandar los pedidos de entrevista, y consultar al tutor las dos cosas que el chat dejó sin resolver (qué se sube el 22, si la demo es obligatoria).
- **Bloque 1 (10-13/08)** — requerimientos, casos de uso y su diagrama (criterio 1).
- **Bloque 2 (14-16/08)** — mockups, diagramas de componentes y flujo, modelo de datos y arquitectura (criterios 2, 3 y 6).
- **Bloque 3 (17-18/08)** — tecnologías, que es en buena parte un traslado desde `recursos.md` salvo la arquitectura de red que falta por completo; y la demo como *vertical slice* (FastAPI + XLM-T desde HuggingFace + extensión mínima que lee el DOM), no como MVP (criterios 5 y 7).
- **Bloque 4 (19-21/08)** — redacción de `chapter03.tex` y `chapter04.tex` más los anexos.

**Estado de partida:** 2 de 8 criterios cumplidos, 6 en cero, sin código, encuesta con 7 respuestas.

**Fuera de alcance declarado:** análisis financiero (la parte económica no entra), decisión definitiva del modelo y reescritura del pipeline (Entrega 4 — para la demo alcanza XLM-T sin *fine-tuning*), y construcción del corpus argentino.

**Nota sobre la muestra.** Se evaluó y se descartó extrapolar las 7 respuestas reales a 150 sintéticas: es fabricación de datos de investigación y anula la entrega. La ruta adoptada es empujar respuestas reales por el canal de reciprocidad del grupo del curso y declarar el tamaño de muestra con honestidad. Contexto que baja la presión: el user research **no está entre los ocho criterios de la rúbrica** y el mínimo de 120 proviene solo de la comisión de Monzón, no del tutor propio.

## [2026-08-08] ingest | Rúbrica EP2 (50%) + chat del curso — corrección del alcance de la entrega

Ingesta de dos fuentes aportadas por el autor: la **rúbrica oficial de la Entrega Parcial 2** y el export del chat de WhatsApp del curso (~1.900 mensajes, 13/03 a 07/08).

**Corrección de alcance (importante).** El wiki y el anexo del documento asumían que la entrega del 50% cubría user research, competencia y modelo de negocio. **La rúbrica dice otra cosa**: evalúa la solución. Sus ocho criterios son requerimientos (casos de uso o historias de usuario, RF/RNF), mockups del frontend, diagramas (flujo de información, componentes, clases, objetos), competencias con herramientas de marketing (triple P, FODA, Cruz de Porter, Matriz Boston Consulting), tecnologías justificadas con la arquitectura de red, modelo de datos (diagrama de BD + diagrama de arquitectura), demo con capturas de avance de implementación, y tabla comparativa en el estado del arte. Consecuencia: `solucion/requerimientos`, `solucion/arquitectura` y `solucion/tecnologias` —que el lint de hoy clasificó como bloqueantes de octubre— son **bloqueantes del 22 de agosto**.

**Fechas corregidas:** documento el **22/08** (comisiones de sábado; los martes el 18/08), exposición el **29/08**. El chat resuelve la confusión 18 vs. 22.

**Lo que agrega la clase por fuera de la rúbrica** (transcripción del 04/07): user research sí entra en el 50%; exposición de ~20 minutos mitad negocio mitad técnica; demo en vivo, con capturas comentadas o en video; **la parte económica no entra** —lo que saca el análisis financiero de la ruta crítica—; y no pasar las transcripciones de entrevistas por un LLM porque se detecta.

**Evaluación de consenso en el chat**, a pedido del autor:
- **FODA — contradicción, no consenso.** Monzón pide no hacerlo; la rúbrica lo lista explícitamente. Prevalece la rúbrica.
- **Cantidad de entrevistas — sin consenso.** Circulan 3, 5 y "ninguna si hacés encuesta". Lo estable: con encuesta alcanza con menos.
- **Mínimo de 120 respuestas — no verificado.** Sale solo de la clase de Monzón, no de la rúbrica ni del tutor propio.
- **Transcripción sin grabación y sin LLM — consenso.**
- **Qué se sube el 22 (documento solo, o también presentación y demo) — sin resolver.** Pendiente de confirmar con el tutor.

**Hallazgo:** el autor **ya publicó su encuesta el 04/07** (`forms.gle/yresENK6F6YWsvv67`). El wiki la daba por no iniciada. Falta el conteo de respuestas y el análisis.

**Verificado:** el criterio 8 de la rúbrica (tabla comparativa en el estado del arte) **ya está cumplido** — `chapter02.tex:244`, tabla `tab:competidores`.

Archivos: `raw/clases/Rubrica-EP2-50porciento.pdf`; `raw/clases/notas-chat-pfi-2026.md` (destilado — no se archiva el export crudo del chat porque contiene teléfonos y nombres completos de ~150 compañeros y el repositorio es git); `wiki/proyecto/entrega-50-alcance.md` (nueva); `wiki/proyecto/cronograma.md` (fechas y ruta crítica reordenada por criterio de rúbrica); `index.md`.

## [2026-08-08] update | Cronograma con fechas confirmadas + página de decisiones pendientes

**Fecha confirmada por el autor: Entrega 3 (50%) el 28/08/2026** — 20 días desde hoy. Volcada a `cronograma.md`, que estaba vacío desde el 2026-04-12 (15 celdas `[fecha]`, todo "Pendiente", tutor Monzón). Reescrito completo: las cinco entregas con sus fechas y estados (E1 y E2 entregadas), el plan de actividades A-01…A-08 alineado con `tab:plan-actividades` del anexo del documento, una ruta crítica semanal hacia el 28/08 y los hitos posteriores. Tutor corregido a Giro Uribazo.

Creada `wiki/sintesis/decisiones-pendientes-2026-08.md` (primera página de `sintesis/`) con las cinco decisiones abiertas del lint, cada una con opciones y costo:

1. **Modelo principal.** Hallazgo que reduce el costo de cambiar: `chapter01.tex:23` —los objetivos específicos ya presentados— está redactado de forma agnóstica ("BETO, XLM-RoBERTa o RoBERTuito"); solo el capítulo 2 se inclina por RoBERTuito, en tres oraciones (L50, L214, L301). Verificada la duda del autor sobre la confiabilidad de RoBERTuito: es LREC 2022 (Pérez et al., pp. 7235–7243), mismo tipo de venue que XLM-RoBERTa (ACL 2020), y ya evaluado en la tarea exacta por Toapanta et al. Opciones: (A) XLM-RoBERTa, (B) RoBERTuito, (C) **XLM-T** — `cardiffnlp/twitter-xlm-roberta-base`, XLM-RoBERTa re-pre-entrenado sobre ~198M de tweets (Barbieri et al., LREC 2022, pp. 258–266), que resuelve la tensión entre linaje multilingüe y ajuste al dominio, (D) declararlo comparación experimental de cuatro modelos. El trade-off real no es el prestigio del laboratorio sino la transferencia desde el inglés: sin modelo multilingüe, el Tier 1 de 40.000 ejemplos de LIAR + FakeNewsNet no existe.
2. **Ensemble de dos modelos** en `modelos-espanol.md:106-112`: resto del alcance previo al 2026-06-13.
3. **Pipeline en BETO**: el problema serio no es el checkpoint sino que la limpieza borra emojis, hashtags y menciones — correcto para BETO, contraproducente para cualquier modelo pre-entrenado sobre tweets.
4. **Tamaño del corpus argentino**: 200–500 y 2.000–5.000 son roles distintos (test vs. entrenamiento), no una contradicción irreconciliable.
5. **Número de clases**: binario vs. tres (verdadero / falso / no verificable).

Más una tabla de nueve correcciones mecánicas sin decisión asociada. Actualizado `index.md` (encabezado, sección Síntesis, descripciones de `cronograma` y `recursos`).

**Criterio de prioridad registrado:** las decisiones 1 a 3 corresponden a la Entrega 4 (octubre) y no bloquean el 28 de agosto; las tres semanas que quedan van al trabajo de campo del user research, el análisis financiero y `chapter03.tex`.

## [2026-08-08] lint | Health-check completo del wiki (51 páginas) + documento LaTeX

Análisis del grafo de links (determinístico), contradicciones de contenido y cruce wiki ↔ documento LaTeX. El grafo está sano y la bibliografía del documento es consistente (45 claves, 0 citadas sin definir, 0 definidas sin citar). Los problemas se concentran en (a) el riesgo de la entrega del 50% —que según el cronograma del documento vence este mes—, (b) la decisión "RoBERTuito como modelo principal" (2026-07-04) no propagada al pipeline técnico ni a la estrategia de datos, y (c) reincidencias de los tres lints anteriores nunca aplicadas.

**RIESGO DE ENTREGA (prioridad máxima).** `documento/chapters/appendix/schedule_of_activities.tex` fija la Entrega 3 (50%) en **agosto de 2026** con contenido: User Research + competencia + modelo de negocio, más el inicio de la construcción del dataset argentino. Hoy es 2026-08-08 y el estado es: `chapters/chapter03.tex` tiene 18 palabras (cinco `Completar.`); el trabajo de campo del user research no arrancó (0 respuestas de encuesta sobre una meta de 120+, 0 entrevistas, personas en `[a completar]`); `negocio/analisis-financiero.md` sigue siendo el stub del 2026-04-12; `annex.tex` mantiene comentados `surveys.tex` e `interviews.tex`; y no hay ninguna página que registre avance en la construcción del dataset argentino.

**Contradicciones (prioridad alta):**

1. **Modelo principal vs. estrategia de datos — incoherencia metodológica.** `modelos-overview`, `enfoques-deteccion` y `propuesta` fijan **RoBERTuito** como clasificador principal, pero la estrategia de datos (`comparacion-datasets`, Tier 1) se apoya en *transfer learning* desde inglés con LIAR + FakeNewsNet, que solo XLM-RoBERTa soporta — la propia tabla de `modelos-espanol.md:102` marca RoBERTuito con "Transfer desde inglés ✗". Aun así `propuesta.md:129` y `recursos.md:75` describen "RoBERTuito fine-tuneado sobre LIAR + FakeNewsNet". Requiere decisión: o RoBERTuito con datos en español únicamente (FakeDeS + corpus argentino), o XLM-RoBERTa si se quiere aprovechar el inglés.
2. **`modelos-espanol.md:106-112` recomienda un ensemble de dos modelos** (RoBERTuito para redes + XLM-RoBERTa para artículos periodísticos). Contradice a `modelos-overview` (un clasificador, BETO/XLM-R solo como líneas de comparación) y al alcance Twitter/X: los artículos periodísticos son evidencia, no objetos de clasificación. Resto stale del pre-2026-06-13.
3. **`pipeline-preprocesamiento.md` (487 líneas) sigue íntegramente en BETO.** No se tocó en la corrección del 2026-07-04: checkpoint `dcc-uchile/bert-base-spanish-wwm-uncased` (además mal escrito — el id real es `dccuchile/…`), "768 dimensiones (BETO)", tabla de modelos con "BETO base ✅ PFI MVP". Más grave que el nombre: su etapa de limpieza remueve emojis, *mentions* y hashtags y pasa a minúsculas, mientras que RoBERTuito se pre-entrenó preservando esos elementos (preprocesamiento de pysentimiento). Aplicado tal cual, el pipeline anula la ventaja de dominio que justifica elegir RoBERTuito.
4. **`metodologia-tecnica.md` se contradice internamente**: L43 dice "Fine-tune RoBERTuito (principal)" y la tabla resumen de L427 dice "Transformer (BETO)".
5. **Servicio de búsqueda web.** `recursos.md` eligió **Tavily**; cinco páginas siguen presentando **Serper.dev** como el módulo del PFI: `fact-checking-automatico.md:73` y `:117`, `comparativa-llms-2024-2025.md:74` y `:96`, `toapanta-2024-latam.md:53`, `modelo-de-negocio.md:115-116`. (Las menciones a Serper como parte del experimento de Tian et al. son correctas y no deben tocarse.)
6. **Costo del PFI.** `modelo-de-negocio.md:140` (FODA) dice "~USD 65 en período PFI"; `recursos.md` dice **$173 USD** desde que se agregaron HF Pro ($9/mes) y Tavily.
7. **Tamaño del dataset argentino.** `dataset-recomendacion.md` pide 200-500 posts anotados; `comparacion-datasets.md:58` fija la meta en 2.000-5.000 como contribución académica. El documento (cap. 2) lo menciona sin número.
8. **Número de clases sin decidir.** `dataset-recomendacion.md:34` colapsa LIAR a binario y luego su esquema de anotación usa 3 etiquetas (0/1/2); `metodologia-tecnica.md:45` devuelve 3 clases `[real, falso, sin_verificar]`. No hay una definición única del espacio de salida.
9. **Tamaño de FakeNewsNet inconsistente**: 11.8k (`dataset-recomendacion.md:42`), ~23k (`datasets-overview.md:19`), ~28k (`comparacion-datasets.md:18`).
10. **[REINCIDENTE] Tutor incorrecto.** El lint del 2026-06-04 corrigió "Monzón" → Giro Uribazo, pero quedaron tres: `cronograma.md:39`, `pruebas.md:24`, `fake-news-detector-br.md:78`. (La mención en `user-research.md` es legítima: refiere a la consigna de otra comisión.)
11. **[REINCIDENTE] Alcance Twitter/X.** El lint del 2026-07-04 arregló `information-tracer` y `fake-news-detector-br` pero no `newtral-factflow.md:54` y `:81` ("Twitter/X, Instagram, Facebook" como plataformas del PFI) ni `toapanta-2024-latam.md:54` ("Twitter + Instagram").
12. **[REINCIDENTE desde 2026-04-19] Chequeado como corpus de contraste.** `enfoques-deteccion.md:179` sigue diciendo "contraste semántico contra corpus confiable (Chequeado.com)"; la decisión del 2026-04-19 lo reemplazó por web search + fuentes oficiales. Relacionado: `analisis-competitivo.md:35` describe el dataset de entrenamiento como "Español (LIAR, FakeNewsNet + Chequeado)" — LIAR y FakeNewsNet son en inglés y Chequeado ya no es fuente de entrenamiento.
13. **`cronograma.md` está vacío mientras el documento tiene el cronograma real.** La página que `CLAUDE.md` designa como fuente de fechas confirmadas tiene 15 celdas `[fecha]` y todo en "Pendiente" (incluido "Tema definido y aprobado"), pese a que `schedule_of_activities.tex` fija las cinco entregas (25 abr · 13 jun · agosto · octubre · diciembre) y da E1 y E2 por completadas.
14. **Overviews que se contradicen con sus propias secciones.** `implementaciones-overview.md` dice "Sistemas analizados: *(vacío)*" con 5 páginas de implementaciones ya escritas; `experimentos-overview.md` deja "Baseline de referencia: [Definir antes de empezar]" cuando `modelos-overview` ya lo fija (TF-IDF + Regresión Logística, F1 macro objetivo 0,80).

**Links:**
- [REINCIDENTE] `implementaciones-overview.md` → `[[raw/papers/nombre.pdf]]` (residuo del template) y `[[wiki/estado-del-arte/]]` (link a carpeta).
- [REINCIDENTE] `datasets-overview.md` → `[[wiki/estado-del-arte/]]` (link a carpeta).
- `user-research.md` → `[[raw/clases/PFI_MarcoTeorico_EstadoDelArte_UserResearch-Sabados.pdf]]` no existe.
- ✅ Resuelto: el link roto `modelos-overview` → `nlp` ya no está.

**Trazabilidad de fuentes:** `raw/clases/`, `raw/articulos/` y `raw/implementaciones/` están **vacíos**. Las slides de la cátedra, el PFI de ejemplo (Sparkle) y el chat del curso se citan como fuentes en `user-research.md` y `recomendaciones-profesor.md` pero nunca se archivaron; los artículos web de `information-tracer` y `diggity-mediaparty` viven en la raíz de `raw/`, no en `raw/articulos/`.

**Huérfanas (0 links entrantes):** `drchal-2024-pipeline-multiidioma`, `fake-news-detector-br`, `proyecto/metodologia`, `proyecto/recomendaciones-profesor`, `proyecto/recursos`. (`newtral-factflow` salió de la lista: `analisis-competitivo` la enlaza con alias escapado.)

**Stubs `[POR DEFINIR]` sin tocar desde 2026-04-12:** `negocio/analisis-financiero` (bloquea la entrega de agosto), `solucion/arquitectura`, `solucion/requerimientos`, `solucion/tecnologias`, `solucion/pruebas`, `proyecto/metodologia` (bloquean la entrega de octubre) y `datasets/datasets-overview` — este último flagged en los lints del 2026-06-04 y 2026-07-04 y todavía en "[POR DEFINIR]" pese a que `comparacion-datasets` y `dataset-recomendacion` ya lo resuelven.

**Metadatos:** encabezado de `index.md` desactualizado (dice "Actualizado: 2026-06-04" y describe `recursos` con Serper.dev). Frontmatter `actualizado:` sin bumpear en páginas editadas después: `analisis-competitivo` (2026-04-13, editada el 2026-06-13 según el log). Deriva en el campo `tipo:` respecto de la taxonomía de `CLAUDE.md` (`concepto|entidad|fuente|análisis|proyecto`): aparecen `desarrollo`, `solución`, `solucion` y `dataset`.

**Sugerencias:** (1) tratar el capítulo 3 y el trabajo de campo del user research como la prioridad del mes; (2) cerrar la decisión modelo↔datos del punto 1 y propagarla a `pipeline-preprocesamiento` antes de escribir código; (3) volcar el cronograma del documento a `cronograma.md`; (4) archivar en `raw/clases/` las fuentes de la cátedra ya citadas.

## [2026-07-04] update | User Research — diseño de instrumentos (encuesta, guía de entrevista, personas)

Arranque del módulo User Research a partir de tres fuentes: diapositivas de la cátedra (método: encuestas + entrevistas + user persona), PFI de ejemplo aprobado 2025 (Feresini/Imbriago, "Sparkle" — estructura 3.1 con 2 entrevistas + encuesta de 160 + 3 personas, transcripciones en anexos) y el chat de WhatsApp del curso PFI 2026.

**Validación del acuerdo entre alumnos (pedido del autor):** no hubo acuerdo común único — la consigna varía por comisión. Notas de la clase de Monzón: dos herramientas base (encuestas, entrevistas, océano azul), **encuestas mínimo 120 resultados**, no hacer FODA, no pegar screenshots del Google Form, en entrevistas "importa el rol". Las diapositivas de los sábados: encuestas + entrevistas + user persona, sin número fijo. Tutor de este PFI (Giro Uribazo) sin consigna confirmada → pendiente validar mínimo de muestra y océano azul con él.

**Decisiones del autor:** diseñar los instrumentos ahora; encuesta al segmento estricto (18-40, política/economía en X) con meta 120+; entrevistas sin contactos aún → guía lista + estrategia de captación + plan B (power-users).

**Producido en `wiki/investigacion/user-research.md`** (rewrite completo, antes stub): objetivo del research, metodología con criterios de la cátedra, cuestionario de encuesta de 15 preguntas (4 bloques: perfil/filtro, exposición, capacidad/comportamiento, apetito/confianza), plan de piloto y distribución, guía de entrevista semiestructurada de 9 preguntas para periodista/fact-checker + variante plan B, estrategia de captación (Chequeado, LinkedIn, academia), plantillas de 2-3 user personas. Actualizado `index.md`.

**Pendiente (trabajo de campo):** piloto de encuesta, distribución hasta 120+, conseguir 2 entrevistados, análisis con gráficos propios, completar personas, volcar a `chapter03.tex` §User Research + anexos.

## [2026-07-04] update | Correcciones del health-check (modelo, alcance, contradicciones)

Aplicadas las correcciones surgidas del lint del mismo día:

- **Modelo principal definido: RoBERTuito** (evaluando el documento LaTeX, que ya lo priorizaba de forma consistente en cap. 2). Propagado a toda la wiki: `modelos-overview.md` (antes "[POR DEFINIR]", ahora RoBERTuito principal + BETO/XLM-RoBERTa/TF-IDF como comparación; secciones 2-5 rellenadas; link roto `nlp`→`nlp-fundacional` arreglado), `transformers-bert.md` (antes "BETO como modelo principal"), `enfoques-deteccion.md` (tabla con doble "candidato principal" corregida; RoBERTuito agregado), `propuesta.md`, `metodologia-tecnica.md`, `recursos.md`. El documento LaTeX ya era coherente; no requirió cambios.
- **Dato corregido en `modelos-espanol.md`**: RoBERTuito es del grupo pysentimiento (Juan Manuel Pérez, UBA/CONICET), no de "Univ. Nac. de San Luis". Accuracy en FakeDeS alineada a Toapanta (~93%).
- **Alcance Twitter/X (#6)**: `information-tracer.md` (decisión ya tomada: MVP solo Twitter/X) y `fake-news-detector-br.md` (patrón de integración reencuadrado a Twitter/X, no Facebook). Nota: la tabla `fake-news-detector-br.md:55` no se tocó — la columna "Infobae" describe a Diggity, no al PFI.
- **Rango etario (#2)**: `propuesta.md` sección "Segmento target" pasada de "16 a 80+ años" a "18 a 40 años", coherente con la decisión del 2026-06-13.
- **Estado (#5)**: checklist de `00-resumen.md` actualizado (marco teórico, EdA y competencia marcados como hechos).

Conteo de módulos en `propuesta.md`: corregido L46 ("tres módulos" → "cuatro módulos", residuo del diseño original de 3 módulos previo al 2026-04-19) y aclarado L54 ("3 señales... que el módulo ensemble sintetiza") para no confundir las señales de análisis con el conteo de módulos.

## [2026-07-04] lint | Health-check completo del wiki (49 páginas)

Análisis del grafo de links (determinístico) + contradicciones de contenido. El grafo está sano; los problemas se concentran en (a) la decisión de alcance del 2026-06-13 (Twitter/X única plataforma de detección) no propagada a todas las páginas, (b) reincidencias del lint 2026-06-04 nunca aplicadas, y (c) páginas stub sin tocar desde abril.

**Contradicciones (prioridad alta):**
1. **Modelo principal inconsistente.** `modelos-espanol.md` concluye que **RoBERTuito** es el modelo más adecuado (entrenado sobre tweets, alineado con el alcance Twitter/X); pero `transformers-bert.md:100` dice "BETO como modelo principal" y `propuesta.md`/`00-resumen.md` dicen "BETO o XLM-RoBERTa" sin mencionar RoBERTuito. Requiere decisión del autor.
2. **`propuesta.md` rango etario.** L42/L102 dicen segmento primario "18 a 40 años"; L161 (sección "Segmento target") dice "16 a 80+ años" — resto stale del cambio del 2026-06-13.
3. **`propuesta.md` conteo de módulos.** L42/L184 dicen "cuatro módulos"; L46 dice "el prototipo funcional de los tres módulos".
4. **[REINCIDENTE] `modelos-overview.md`** sigue en "[POR DEFINIR]" y con secciones 2-5 en "[POR INVESTIGAR]" pese a que `enfoques-deteccion.md` y `modelos-espanol.md` ya lo cubren. Flagged en lint 2026-06-04, nunca aplicado.
5. **[REINCIDENTE] `00-resumen.md`** checklist "Estado actual" todo en `[ ]` (marco teórico, EdA, competencia, etc.) pese a estar hechos. Flagged en lint 2026-06-04, nunca aplicado.
6. **`fake-news-detector-br.md:55`** tabla comparativa: columna PFI "Plataforma objetivo: Sitios de noticias (Infobae, etc.)" — stale, ahora Twitter/X.

**Links:**
- [REINCIDENTE] `modelos-overview.md:75` → `[[wiki/marco-teorico/nlp]]` roto (debe ser `nlp-fundacional`).
- `implementaciones-overview.md` → `[[raw/papers/nombre.pdf]]` (template leftover) y `[[wiki/estado-del-arte/]]` (link a carpeta, no página).
- `datasets-overview.md` → `[[wiki/estado-del-arte/]]` (link a carpeta).

**Huérfanas (0 links entrantes):** `bigcn-deteccion-grafos`, `drchal-2024-pipeline-multiidioma`, `fake-news-detector-br`, `proyecto/metodologia`, `proyecto/recomendaciones-profesor`, `proyecto/recursos`.

**Stubs / placeholders (sin contenido real, casi todos de 2026-04-12):** `solucion/arquitectura`, `solucion/requerimientos`, `solucion/tecnologias`, `solucion/pruebas`, `negocio/analisis-financiero`, `proyecto/metodologia`, `investigacion/user-research`, `modelos/modelos-overview`, `datasets/datasets-overview`. Bloquean Presentaciones Preliminares 3+ (no la del 25%).

**Fuentes ingresadas sin página wiki:** MDFEND (Nan 2021), MultiFC, CREDBANK — marcadas "(pendiente)" en index.md.

**Sugerencias:** decidir RoBERTuito vs BETO como clasificador principal y unificar; evaluar página propia para Chequeado (mencionado en 8+ páginas); conectar huérfanas relevantes desde overviews.

## [2026-06-13] update | Correcciones del análisis comparativo (entrega 25%)

Revisión externa del documento (análisis comparativo contra tesis ejemplo) → correcciones de coherencia, justificación de alcance, validación de fuentes y precisión conceptual antes de la entrega del 25%:

- **Justificación Twitter/X vs WhatsApp**: se explicita por qué X es el primer objetivo de detección pese a que WhatsApp sea más masivo (espacio público donde se originan/amplifican narrativas).
- **Definición operativa**: el sistema no infiere intención; clasifica contenido "potencialmente falso, engañoso o no verificable" y usa "desinformación" como término paraguas.
- **Fuentes de evidencia**: "medios de confianza" → "fuentes periodísticas de referencia" + triangulación con fuentes oficiales y verificadores (Chequeado); ya no se tratan como única "verdad".
- **Citas**: el dato de 31,3 M usuarios y 93 % WhatsApp se reatribuye a DataReportal (no Reuters). Se suaviza el claim de "inaccesibilidad" de Cyabra/Blackbird. Raza et al. actualizado a su versión publicada (KAIS 2025); DOI corregido en Gouliev et al. (ECML PKDD).
- **Meta F1**: se adopta F1 macro como métrica principal, con justificación del umbral y atención al recall de la clase de interés.
- **Dataset**: "disponibilidad" → "factibilidad de construir/adaptar" un corpus argentino.
- **Usuarios**: segmento primario acotado (18-40, política/economía en X) + secundario (periodistas).
- **Privacidad**: cláusula de agregación/anonimización en el modelo de negocio.
- **Nueva subsección "Riesgos y desafíos del proyecto"** en cap. 1.
- **Cronograma**: pasado a página apaisada (pdflscape), filas más espaciadas, ya no se ve comprimido.

Archivos: documento/chapters/chapter01.tex, chapter02.tex; documento/biblio.bib (+DataReportal2024, Raza/Gouliev); documento/main.tex (pdflscape); documento/chapters/appendix/schedule_of_activities.tex; wiki/proyecto/propuesta.md; wiki/00-resumen.md; wiki/negocio/modelo-de-negocio.md.

## [2026-06-13] update | Acotar alcance: Twitter/X única plataforma de detección

Decisión de alcance: la extensión detecta desinformación **únicamente sobre Twitter/X**. Los medios digitales de confianza (Infobae, Clarín, La Nación, Página/12, Télam) dejan de ser objetivos de detección y pasan a usarse solo como **fuentes de evidencia** para el módulo de contraste semántico (scraping + búsqueda web). Instagram y Facebook quedan fuera del alcance del MVP (futuros releases).

Justificación: una extensión de navegador lee el DOM de la sesión del usuario, por lo que no depende de la API restringida de X; Twitter/X concentra el mayor respaldo de datasets y literatura, es texto-céntrico (alineado con RoBERTuito) y permite una arquitectura extensible por adaptadores a otras fuentes.

Archivos actualizados: documento/chapters/chapter01.tex (objetivos, alcance, limitaciones); wiki/proyecto/propuesta.md; wiki/00-resumen.md; wiki/competencia/analisis-competitivo.md; wiki/marco-teorico/modelos-espanol.md; wiki/solucion/metodologia-tecnica.md; wiki/solucion/pipeline-preprocesamiento.md; wiki/datasets/dataset-recomendacion.md; CLAUDE.md.

## [2026-06-04] update | Creación de 17 páginas wiki — Marco Teórico (5), Datasets (6), Estado del Arte (6)

Páginas creadas en wiki/marco-teorico/:
- nlp-fundacional.md — tokenización, Word2Vec, GloVe, FastText, embeddings contextuales
- transformers-bert.md — Transformer (Vaswani 2017), BERT (Devlin 2019), fine-tuning
- fact-checking-automatico.md — pipeline canónico: claim detection → evidence retrieval → verdict
- modelos-espanol.md — BETO, XLM-RoBERTa, RoBERTuito, MarIA; comparativa y recomendación
- difusion-desinformacion.md — Wardle 2017, Vosoughi 2018, Lazer 2018

Páginas creadas en wiki/datasets/:
- liar-dataset.md — 12.836 samples, 6 clases, benchmark de referencia
- fakenewsnet.md — PolitiFact + GossipCop + contexto social (grafos)
- pheme-dataset.md — ~6.500 tweets, 9 eventos, 3 clases
- fakeddit.md — 1M+ Reddit, multimodal (texto + imagen)
- spanish-fake-news-corpus.md — FakeDeS, 971 muestras; gap crítico documentado
- comparacion-datasets.md — tabla comparativa + estrategia de datos PFI (3 tiers)

Páginas creadas en wiki/estado-del-arte/:
- toapanta-2024-latam.md — MarIA 96%, BETO 93%; el comparador directo del PFI
- brechas-espanol-latam.md — 83% inglés, 0 papers Argentina, domain shift ~26pp
- fakebert-kaliyar-2021.md — BERT + CNN baseline; contexto crítico sobre evaluación in-domain
- comparativa-llms-2024-2025.md — BERT fine-tuned > LLMs; web retrieval +20pp F1
- bigcn-deteccion-grafos.md — grafos de propagación; +10pp sobre texto solo
- drchal-2024-pipeline-multiidioma.md — pipeline "any language" que excluye español

Actualizado: index.md con 17 páginas nuevas.

## [2026-06-04] ingest | Deep research Marco Teórico + Estado del Arte — 37 papers + 7 datasets a raw/

Fuentes agregadas a raw/papers/ (37 fichas):
- Vaswani 2017 (Transformer), Devlin 2019 (BERT), Conneau 2020 (XLM-RoBERTa)
- Cañete 2023 (BETO), Pérez 2022 (RoBERTuito), Yenikent 2024 (fake news español)
- Mikolov 2013 (Word2Vec), Pennington 2014 (GloVe), Bojanowski 2017 (FastText)
- Chai 2023 (preprocesamiento NLP), Guo 2022 (survey fact-checking)
- Vosoughi 2018 (difusión fake news), Lazer 2018 (ciencia fake news)
- Wardle & Derakhshan 2017 (information disorder), Srba 2025 (credibilidad)
- Wang 2017 (LIAR paper), Shu 2020 (FakeNewsNet), Kaliyar 2021 (FakeBERT)
- Hassan 2017 (ClaimBuster), Bian 2020 (BiGCN), Nan 2021 (MDFEND)
- Toapanta 2024 (LATAM Ecuador), Tian 2024 (web retrieval agents)
- Raza 2024 (BERT vs LLMs), Gouliev 2025 (PolyTruth), Hasan 2025 (generalization LIAR)
- Wang 2024 survey (low-resource), Drchal 2024 (pipeline multilingüe), Panchendrarajan 2024

Fuentes agregadas a raw/datasets/ (7 fichas):
- LIAR, FakeNewsNet, PHEME, Fakeddit, MultiFC, CREDBANK, Spanish-Fake-News-Corpus

## [2026-06-04] ingest | Slides del profesor: Marco Teórico, Estado del Arte, User Research + ejemplo PFI Sparkle

Fuentes procesadas:
- PFI_MarcoTeorico_EstadoDelArte_UserResearch-Sabados.pdf (slides de clase 2026)
- [GR_M15_Feresini_Imbriago][Entrega Final PFI 2025_V_2].pdf (ejemplo PFI aprobado)

Acciones:
- Creada wiki/proyecto/recomendaciones-profesor.md con guía completa de Marco Teórico, Estado del Arte, User Research y checklist de entrega.
- Agregadas en CLAUDE.md: sección "Estilo de escritura académica" (voz, terminología, frases prohibidas, estructura de párrafos) y sección "Citas y bibliografía — ISO 690-2010" (formato en texto, formato de entradas bib, reglas del profesor, fuentes académicas prioritarias).

## [2026-06-04] lint | Formulario de propuesta oficial — health-check y correcciones

Contradicciones encontradas y corregidas a partir del formulario de propuesta oficial (PDF, 25/04/2026):

1. **CRÍTICA — Tutor incorrecto**: Todo el repo tenía a Monzón, Nicolás Alberto como tutor. El formulario oficial indica Giro Uribazo, Fidel Valentin (fgirouribazo@uade.edu.ar, UADE interno). Corregido en CLAUDE.md, wiki/00-resumen.md, wiki/proyecto/reuniones.md, documento/chapters/title.tex, documento/main.tex.
2. **Título incompleto**: Faltaba "y Medios Digitales" al final del título oficial. Corregido en CLAUDE.md, wiki/00-resumen.md, wiki/proyecto/propuesta.md, documento/chapters/title.tex, documento/main.tex.
3. **LU del alumno**: Completado con 1150726 en documento/chapters/title.tex.
4. **Redes sociales "POR DEFINIR"** en CLAUDE.md: actualizado con las plataformas oficiales (X, Instagram, Facebook, Infobae, Clarín).

Acciones adicionales:
- Completado chapter01.tex con introducción, objetivos y alcance del formulario oficial.
- Agregada referencia Newman2024 (Reuters Institute DNR 2024) a biblio.bib.
- Renombrado macro \Nico{} → \Fidel{} en documento/main.tex y considerations.tex.

---

## [2026-06-04] lint | Health-check del wiki — contradicciones, huérfanas, faltantes

**Páginas analizadas:** 32 páginas wiki + index.md + log.md

**Contradicciones encontradas:**
1. `wiki/00-resumen.md` — checklist de estado desactualizado: marco teórico, estado del arte y análisis competitivo marcados como `[ ]` (pendiente) cuando ya están iniciados/completados con páginas reales.
2. `wiki/modelos/modelos-overview.md` — dice "Modelo elegido: [POR DEFINIR]" pero `metodologia-tecnica.md` y `enfoques-deteccion.md` ya lo definen como BETO/XLM-RoBERTa.
3. `wiki/datasets/datasets-overview.md` — dice "Dataset elegido: [POR DEFINIR]" pero `dataset-recomendacion.md` ya define LIAR + FakeNewsNet.

**Referencia rota:**
- `wiki/modelos/modelos-overview.md` línea 76: `[[wiki/marco-teorico/nlp]]` — esa página no existe.

**Páginas huérfanas (sin links entrantes desde otras páginas wiki):**
- `wiki/proyecto/recursos.md`
- `wiki/proyecto/contexto-problema.md`
- `wiki/implementaciones/fake-news-detector-br.md`
- `wiki/implementaciones/implementaciones-overview.md`

**Conceptos clave sin página propia:**
- BETO — modelo central del proyecto, sin página en `wiki/modelos/`
- XLM-RoBERTa — modelo alternativo clave, sin página en `wiki/modelos/`
- Chequeado.com — mencionado en 8+ páginas, sin análisis propio

**Placeholders críticos (importantes para el PFI, aún vacíos):**
- `wiki/solucion/arquitectura.md` — [POR DEFINIR], bloquea Presentación Preliminar 3
- `wiki/solucion/requerimientos.md` — [POR DEFINIR]
- `wiki/solucion/tecnologias.md` — [POR DEFINIR]
- `wiki/negocio/analisis-financiero.md` — [POR DEFINIR]
- `wiki/proyecto/metodologia.md` — [POR DEFINIR]
- `wiki/investigacion/user-research.md` — [POR DEFINIR]

**Fuentes a ingresar (citadas pero no formalizadas):**
- Reuters Institute Digital News Report 2024 (citado en propuesta.md)
- Paper BETO: Cañete et al. 2023
- Paper XLM-RoBERTa: Conneau et al.
- Dataset en español para fake news (pendiente de investigar)

---

## [2026-04-29] update | Modelo de negocio detallado (qué se vende, segmentos B2B, moat, BMC, FODA, pricing)

**Páginas actualizadas:** `wiki/negocio/modelo-de-negocio.md` (rewrite completo, antes era stub vacío con `[POR DEFINIR]`), `wiki/proyecto/propuesta.md` (sección "Modelo de negocio" expandida con qué se vende, segmentos B2B, moat de datos y bucle de red), `index.md`.

**Trigger:** consulta del usuario al preparar pitch para tutor — la sección original de la propuesta ("ciudadanos gratis → B2B paga") era demasiado abstracta para defender el modelo. No quedaba claro qué se vendía, a quién, ni por qué pagarían.

**Decisiones clave documentadas:**
- **Qué se vende exactamente:** no la extensión, sino información sobre qué desinformación circula en Argentina en tiempo real. Dos productos: API de detección (pricing por volumen) + reportes/dashboards de tendencias (suscripción mensual).
- **Cinco segmentos B2B:** medios de comunicación, fact-checkers (Chequeado), centros de investigación, organismos públicos / ONGs (especialmente en ciclos electorales), marcas y agencias corporativas. Cada uno con problema concreto y razón específica para pagar.
- **Moat de datos:** ventaja estructural frente a Cyabra/Blackbird.AI/Newtral FactFlow. Ellos obtienen datos por scraping de APIs (caro, limitado, ciego a WhatsApp). Nosotros, sensor distribuido en navegadores reales — registramos consumo, no solo publicación, y vemos WhatsApp cuando los usuarios abren links en el navegador.
- **Bucle de red de datos:** más usuarios → mejor dataset → producto B2B más valioso → más revenue → mejor producto ciudadano → más usuarios. Defendibilidad a largo plazo.
- **Pricing tentativo:** API Pro USD 200/mes, Enterprise USD 1.500-5.000/mes, dashboards USD 300/mes, contratos electorales USD 10k-50k.
- **Riesgos identificados:** dependencia de adopción ciudadana inicial, regulación LPDP, riesgo reputacional de sesgo percibido, riesgo de competidor enterprise pivotando.

BMC, FODA y 5 fuerzas completados con esta visión.

---

## [2026-04-22] update | Presupuesto estimado de infraestructura cloud

Creación de `wiki/proyecto/recursos.md` con el presupuesto completo del PFI. Costos fijos: $5 USD (Chrome Web Store) + dominio opcional ($15). Costos mensuales: $5/mes (Railway backend+DB), $0 Vercel, $0 HF Inference API, $0 Serper.dev. Total estimado período PFI (~12 meses): $65 USD. Incluye análisis comparativo de opciones para web search API y modelo NLP.

---

## [2026-04-19] lint | Health check del wiki — contradicciones resueltas

**Contradicciones identificadas y resueltas:**
1. **Módulos (3 vs 4):** propuesta.md línea 119 decía "3 módulos", contradice metodologia-tecnica.md. Actualizado a "4 módulos" (NLP + Credibilidad + Contraste + Ensemble).
2. **Fuente primaria para entrenamiento:** propuesta.md línea 110 mencionaba "Chequeado.com como fuente primaria", contradice metodologia-tecnica.md y dataset-recomendacion.md que describen "web search + bases de datos oficiales". Actualizado a "web search en medios confiables + bases de datos de fuentes oficiales (a determinar)".
3. **Página para Chequeado.com:** Analizado. Conclusión: Chequeado.com aparece en tabla comparativa (analisis-competitivo.md), no requiere página propia de análisis.

**Páginas analizadas:** 00-resumen.md, propuesta.md, metodologia-tecnica.md, analisis-competitivo.md, dataset-recomendacion.md, pipeline-preprocesamiento.md, restricciones-legales-eticas.md

**Estado de salud del wiki:**
- ✅ Referencias cruzadas correctas
- ✅ Index.md actualizado
- ✅ Log.md mantiene cronología
- ✅ Sin páginas huérfanas
- ✅ Nuevas páginas bien conectadas

---

## [2026-04-19] update | Restricciones legales, datasets y pipeline de preprocesamiento

**Páginas creadas:**
- `wiki/proyecto/restricciones-legales-eticas.md` — análisis de LPDP, derechos de autor, ToS, compliance
- `wiki/datasets/dataset-recomendacion.md` — estrategia de datasets (LIAR, FakeNewsNet, validación argentina)
- `wiki/solucion/pipeline-preprocesamiento.md` — pipeline de limpieza, normalización, tokenización, BETO

**Páginas actualizadas:** `index.md`, `wiki/proyecto/propuesta.md` (arquitectura 4 módulos), `wiki/competencia/analisis-competitivo.md` (tabla comparativa + ERIC)

Respuestas documentadas a preguntas sobre:
1. **Restricciones ético/legales:** Datos públicos only, LPDP compliance, copyright fair use, no ToS violations si usas APIs oficiales
2. **Selección de datasets:** LIAR (12.8k en inglés) + FakeNewsNet (11.8k) para entrenamiento; recolección manual de 200-500 posts argentinos para validación
3. **Pipeline de datos:** Limpieza (remover URLs, mentions, emojis) → Normalización (minúsculas, números → `<NUM>`) → Tokenización (spaCy) → Vectorización (BETO + pooling `[CLS]`)
4. **Manejo de español rioplatense:** Voseo OK, diminutivos/aumentativos OK, watchout spanglish

---

## [2026-04-19] update | Metodología técnica — arquitectura ML/DL de 4 módulos

**Páginas creadas:** `wiki/solucion/metodologia-tecnica.md`
**Páginas actualizadas:** `index.md`

Documento completo que especifica:
- **Módulo 1 (Deep Learning):** Fine-tune Transformer (BETO/XLM-RoBERTa) para clasificación de contenido desinformativo
- **Módulo 2 (Machine Learning):** Logistic Regression o pequeña NN para evaluación de credibilidad de fuente (metadatos de cuenta)
- **Módulo 3 (DL + Information Retrieval):** Web search en medios confiables + búsqueda en fuentes oficiales (infoleg.gob.ar, indec.gob.ar, bcra.gob.ar, minedu.gob.ar, boletin.gob.ar, etc.) — sin dependencia de Chequeado.com, expandido a múltiples fuentes de verdad
- **Módulo 4 (Ensemble):** Weighted combination o pequeña NN que sintetiza los 3 scores en decisión final

Decisión clave: reemplazo de búsqueda en Chequeado.com por **web search + fuentes oficiales**. Esto permite:
- Detectar desinformación nueva (antes de que medios la cubran)
- Acceso a "verdad de campo" (leyes, datos oficiales, decretos)
- Reducción de sesgo editorial (múltiples fuentes)
- Mayor precisión para claims sobre legislación, datos económicos, salud, educación

Incluye: casos de uso, limitaciones, ventajas, flujo end-to-end ejemplificado, tabla resumen de técnicas ML/DL usadas.

---

## [2026-04-16] update | Descripción final de la propuesta de tema

**Páginas actualizadas:** `wiki/proyecto/propuesta.md`

Sección "Descripción" finalizada y guardada. Cubre: contexto del problema (Reuters Institute 2024), crisis de confianza en medios argentinos, IA generativa como vector nuevo, gap de las soluciones existentes, modelo de negocio ciudadano+B2B, solución técnica de 3 módulos, segmento target 16-80 años, pros/contras, MVP y futuros releases.

---

## [2026-04-16] update | Modelo de negocio y diferenciador definidos

**Páginas actualizadas:** `wiki/proyecto/propuesta.md`

Decisión clave: modelo ciudadano-gratuito + B2B. La capa ciudadana no es filantropía — genera datos anonimizados de tendencias de desinformación local que se venden como API y reportes a medios, fact-checkers y centros de investigación. Diferenciador vs Cyabra/Blackbird.AI: ellos son pure enterprise sin capa ciudadana; nosotros construimos el activo diferencial (datos reales) a través de la adopción masiva.

---

## [2026-04-16] update | Propuesta — segmento target, futuros releases, limitaciones

**Páginas actualizadas:** `wiki/proyecto/propuesta.md`

Decisiones incorporadas: segmento target 16-80+ años (ciudadano común + periodista/editor como screening tool). Futuros releases: multimedia/deepfakes, WhatsApp/Telegram, grafos de propagación. Limitación principal reconocida: falsos positivos en contenido satírico/irónico.

---

## [2026-04-16] ingest | Contexto del problema — estadísticas de desinformación en Argentina

**Páginas creadas:** `wiki/proyecto/contexto-problema.md`
**Páginas actualizadas:** `index.md`

Relevamiento de estadísticas verificadas para la Propuesta de Tema. Fuente principal: Reuters Institute Digital News Report 2024 (cobertura local: La Nación). Datos clave: confianza en medios 30% (menor de LATAM), interés en noticias colapsó de 77% (2017) a 45% (2024), WhatsApp 93% de penetración. Vector nuevo documentado: IA generativa (deepfakes políticos, AI slop) como protagonista de la desinformación 2024-2025. Narrativa base definida para usar en la Descripción de la propuesta.

---

## [2026-04-16] ingest | Kwon & Jang (IEEE 2025) — Survey de detección de fake text (misinformación + LM-generated)

**Fuente:** `raw/A Comprehensive Survey of Fake Text Detection on Misinformation and LM-Generated Texts.md`  
**Páginas creadas:**
- `wiki/estado-del-arte/kwon-jang-2025-survey-fake-text.md`
- `wiki/marco-teorico/tipos-fake-text.md`
- `wiki/marco-teorico/enfoques-deteccion.md`

**Páginas actualizadas:** `index.md`

Primer survey que unifica misinformación y texto generado por LM. Cubre: TF-IDF/SVM (baseline), CNN/RNN/LSTM, GNN (propagación), Transformers (BERT/XLNet/RoBERTa), DetectGPT, watermarking. Resultado destacado: ensemble BERT+ALBERT+XLNet → 99% en COVID fake news. Justifica el uso de transformers + features de contexto de fuente para el PFI.

---

## [2026-04-16] ingest | Albtoush et al. (PeerJ 2025) — Survey fake news detection, foco árabe (análogo al español)

**Fuente:** `raw/Fake news detection state-of-the-art review and advances with attention to Arabic language aspects.md`  
**Páginas creadas:** (compartidas con ingest anterior — tipos-fake-text, enfoques-deteccion)  
**Páginas actualizadas:** `wiki/estado-del-arte/albtoush-2025-arabic-fake-news.md`, `index.md`

Survey 2020-2024 de ML/DL/Transformers para fake news. El foco en árabe es directamente análogo al desafío en español rioplatense: idioma low-resource, dialectos, datasets escasos. Resultado clave: transformers especializados en el idioma (AraBERT ≈ BETO/XLM-RoBERTa para español) superan consistentemente a modelos genéricos. Incluye tabla comparativa de 13+ estudios y datasets. Justifica BETO o XLM-RoBERTa como modelo principal del PFI.

---

## [2026-04-13] update | Objetivo general, objetivos específicos y alcance definidos

**Páginas actualizadas:** `wiki/proyecto/propuesta.md`, `wiki/00-resumen.md`

Decisiones clave tomadas:
- **Objetivo**: servicio de detección de desinformación para ciudadanos argentinos en redes sociales y medios digitales
- **Arquitectura de 3 módulos**: (1) clasificador NLP (BETO/XLM-RoBERTa), (2) score de credibilidad de fuente, (3) contraste semántico con fuentes confiables (similitud vectorial + corpus Chequeado.com)
- **Output**: score de probabilidad + evidencia (links a fuentes que corroboran/contradicen)
- **Plataformas**: Twitter/X, Instagram, Facebook, Infobae.com, Clarín.com
- **Temática**: política, economía y sociedad argentina
- **Entregables MVP**: extensión Chrome + modelo en HuggingFace + dashboard web
- **Dataset**: en español, a construir/adaptar (Chequeado.com como fuente principal)
- **Usuario objetivo**: ciudadanos comunes (primario) + periodistas/editores (secundario)
- **Fuera del alcance**: apps móviles, análisis multimedia, grafos de propagación, otros idiomas/plataformas

---

## [2026-04-13] ingest | Web search — competidores e implementaciones de referencia

**Fuentes:** búsquedas web (GitHub, G2, TechCrunch, LatAm Journalism Review, JournalismAI, etc.)
**Páginas creadas:**
- `wiki/implementaciones/gnn-fakenews-safe-graph.md`
- `wiki/implementaciones/fake-news-detector-br.md`
- `wiki/implementaciones/newtral-factflow.md`

**Páginas actualizadas:** `wiki/competencia/analisis-competitivo.md`, `index.md`

Panorama de competidores y repos de referencia relevados:
- **Competidores comerciales**: Cyabra, Blackbird.AI, Newtral FactFlow, Information Tracer
- **Implementaciones open-source**: safe-graph/GNN-FakeNews (grafos de propagación), fake-news-detector (Chrome/Firefox + crowdsourcing, LATAM)
- **Repos BERT**: múltiples implementaciones en PyTorch (LIAR dataset, BERT+GAT, DistilBERT, Siamese BERT)
- **Contexto LATAM en español**: Newtral FactFlow (70% español), Fake News Detector BR (portugués), Chequeado.com (Argentina, fact-checkers humanos)

---

## [2026-04-13] ingest | Information Tracer — plataforma de inteligencia en redes sociales

**Fuente:** `raw/Information Tracer.md` (artículo web, informationtracer.com)
**Página creada:** `wiki/implementaciones/information-tracer.md`
**Páginas actualizadas:** `wiki/competencia/analisis-competitivo.md`, `index.md`

Plataforma SaaS de detección de manipulación coordinada y bots en X, Facebook, Instagram, Reddit, YouTube, Bluesky y LinkedIn. Usado por periodistas (Tortoise Media) y académicos (CMU, Tsinghua). Modelo cerrado. Enfoque en manipulación coordinada, no en verificación de claims individuales.

---

## [2026-04-13] ingest | Diggity — MediaParty Trust API, análisis de calidad periodística

**Fuente:** `raw/timmd-9216mediaparty-trust-api Diggity a tool for checking the quality of journalistic content.md` (GitHub)
**Página creada:** `wiki/implementaciones/diggity-mediaparty.md`
**Páginas actualizadas:** `wiki/competencia/analisis-competitivo.md`, `index.md`

Herramienta open-source ganadora del MediaParty Hackathon 2025 (Buenos Aires). FastAPI + Stanford Stanza (español) + OpenRouter + DSPy + extensión Chrome. Evalúa calidad periodística (adjetivos cualitativos, extensión, complejidad, tiempos verbales). Sponsors LATAM: Fundación Avina, FUNDAR.

---

## [2026-04-13] update | Tema definido + capa de desarrollo

**Tema:** Sistema de Detección Automática de Desinformación en Redes Sociales (IA)
**Integrantes:** Juan Martín Bejarano Arce

**Nuevas carpetas raw/:** `papers/`, `articulos/`, `implementaciones/`, `datasets/`, `clases/`

**Nuevas páginas wiki:**
- `wiki/datasets/datasets-overview.md` — panorama de datasets
- `wiki/modelos/modelos-overview.md` — taxonomía de enfoques ML
- `wiki/experimentos/experimentos-overview.md` — tabla de experimentos
- `wiki/implementaciones/implementaciones-overview.md` — repos y sistemas de referencia

**Páginas actualizadas:** `CLAUDE.md`, `00-resumen.md`, `proyecto/propuesta.md`, `index.md`

---

## [2026-04-12] setup | Inicialización del wiki

Creación del esqueleto completo del wiki PFI.

**Estructura creada:**
- `CLAUDE.md` — esquema y reglas de operación
- `index.md` — índice de contenido
- `wiki/00-resumen.md` — visión general
- `wiki/proyecto/` — propuesta, cronograma, reuniones, metodología
- `wiki/solucion/` — requerimientos, arquitectura, tecnologías, pruebas
- `wiki/investigacion/user-research.md`
- `wiki/negocio/` — modelo de negocio, análisis financiero
- `wiki/competencia/analisis-competitivo.md`
- `raw/` y `raw/assets/` — directorios para fuentes

**Estado:** Tema del PFI pendiente de definición. Wiki listo para recibir la primera fuente.

**Próximo paso:** Definir el tema del proyecto y actualizar `wiki/proyecto/propuesta.md` y `wiki/00-resumen.md`.
