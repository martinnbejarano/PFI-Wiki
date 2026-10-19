---
titulo: Investigación — marco legal (ToS de X, Ley 25.326 y AAIP)
tipo: análisis
tags: [legal, lpdp, aaip, x, tos, transferencia-internacional, disclaimer, investigacion]
fuentes: [https://x.com/tos, https://developer.x.com/en/developer-terms/agreement-and-policy, https://servicios.infoleg.gob.ar/infolegInternet/anexos/60000-64999/64790/texact.htm, https://servicios.infoleg.gob.ar/infolegInternet/anexos/70000-74999/70368/norma.htm, https://servicios.infoleg.gob.ar/infolegInternet/anexos/265000-269999/267922/texact.htm]
actualizado: 2026-10-19
---

# Investigación — marco legal (ToS de X, Ley 25.326 y AAIP)

Resuelve el *issue* #75. Complementa a [[wiki/proyecto/restricciones-legales-eticas]], que ya analiza recolección (art. 5), calidad (art. 4), cesión (art. 11), supresión (art. 16), honor y propiedad intelectual. Esta página cubre lo que esa no tenía verificado o no trataba: el texto vigente de los términos de X, la política para desarrolladores, los arts. 7, 12 y 21, las normas de la AAIP sobre transferencia internacional y modelos de *disclaimer*.

**Producto analizado:** una extensión de Chrome lee los tuits que ya están en pantalla en X y los manda a un servicio propio (FastAPI). El servicio llama a un LLM de OpenAI y busca evidencia en la web. Se verificó en `prototipo/servicio/app/proveedor/openai.py` que a OpenAI **solo se envía el texto de la publicación**, no el `@`. El *prompt* lo dice explícito: «No sabés quién publicó la afirmación y no tenés que saberlo».

Todas las fuentes se consultaron el **2026-10-19**. Las URLs están en la tabla final.

## 1. Términos de servicio de X (vigentes desde el 9/10/2026)

**Nota de método.** Desde este entorno, `x.com`, `developer.x.com` y `docs.x.com` no respondieron (tiempo agotado, también por navegador). El texto se tomó de la copia que guarda Open Terms Archive en GitHub (`OpenTermsArchive/pga-versions`, archivos `X/Terms of Service.md`, último *commit* del 2026-10-10, y `X/Developer Terms.md`, último *commit* del 2026-09-18). Ese repositorio registra el texto publicado sin editarlo, pero conviene contrastarlo con `x.com/tos` desde otra red antes de citarlo en el documento.

Esto **corrige** a [[wiki/proyecto/restricciones-legales-eticas]], que citaba la versión de 2024 como `[sin verificar]`. La versión vigente lleva la fecha «**Effective: October 9, 2026**».

| Punto | Texto (cita corta) | Lectura para el PFI |
|---|---|---|
| Contraparte para Argentina | «agreement between you and X Corp.» (sección para quien vive fuera de la UE, la AELC y el Reino Unido) | Es la versión que aplica al usuario argentino |
| Acceso automatizado | «crawling or scraping the Services in any form, for any purpose without our prior written consent is expressly prohibited» | La extensión no hace *crawling*: lee el DOM que el navegador del usuario ya recibió. El argumento de la página legal sigue en pie |
| Facilitar incumplimientos | «a violation of these Terms to facilitate or assist others in violating these Terms, including by distributing products or services that enable or encourage violation» | **Riesgo nuevo.** Alcanza a quien distribuye la herramienta, no solo al usuario. Vale solo si lo que hace el usuario ya incumple; leer su propio *timeline* no lo es |
| Daños pactados | «$15,000 USD per 1,000,000 posts» por acceder a más de 1.000.000 de publicaciones en 24 horas | El prototipo está órdenes de magnitud por debajo. Sirve para dimensionar el riesgo, no para descartarlo |
| Ley y tribunal | «The laws of the State of Texas … will govern»; tribunales de los condados de Wichita o Tarrant, Texas | El conflicto es contractual y se litiga en Texas: no hay sanción en el derecho argentino |
| Licencia sobre el contenido | El usuario otorga a X una licencia mundial, incluso para entrenar «our machine learning and artificial intelligence models» | La licencia es para X. **No habilita a terceros** a entrenar con los tuits |

## 2. Developer Agreement y Developer Policy de X

El Developer Agreement (última actualización: «April 27, 2026») rige el acceso a la **API**. El prototipo no usa la API, así que no lo obliga en lo formal. Igual conviene conocerlo por dos razones: sería el contrato aplicable si el producto pasara a la API, y muestra qué usos considera X ilegítimos aun con acceso autorizado.

- **Entrenamiento de modelos.** La sección III.A(k) prohíbe «use the X API or X Content to fine-tune or train a foundation or frontier model». La Developer Policy lo repite con una sola excepción: Grok. El PFI no entrena un modelo fundacional: hace *fine-tuning* de un clasificador chico y usa un LLM en modo *zero-shot*. Aun así, el *fine-tuning* con tuits de X queda en zona gris, y el documento tiene que decir de dónde salió el corpus de entrenamiento.
- **Información sensible.** La Developer Policy manda: «Never derive or infer, or store derived or inferred, information about a X user's» salud, situación financiera negativa, afiliación o creencias políticas, origen étnico, religión, vida sexual, afiliación sindical y la «Alleged or actual commission of a crime». La misma política permite el análisis agregado que no guarde identificadores: «Aggregate analysis of X content that does not store any personal data … is permitted».
- **Redistribución.** Hacia terceros solo se pueden distribuir identificadores de publicación, y hasta «1,500,000 Post IDs» cada 30 días. Coincide con la decisión de que lo B2B salga agregado o anonimizado (RF-15).

**Lectura.** El historial por cuenta («esta cuenta publicó N desinformaciones») es exactamente lo que la Developer Policy marca como sensible cuando el tema es político. No obliga al prototipo, pero coincide con el riesgo del art. 7 de la Ley 25.326 (sección 3.2). Es un argumento más para que la señal de cuenta se muestre agregada y nunca como juicio sobre la persona.

## 3. Ley 25.326 — artículos que faltaban

Texto actualizado de InfoLEG (norma 64790).

### 3.1 Art. 2 y art. 4: ya cubiertos, con texto confirmado

- Art. 2: dato personal es información sobre personas «determinadas o determinables». El tratamiento incluye la «recolección, conservación, ordenación, almacenamiento, modificación, relacionamiento, evaluación». Guardar y evaluar tuits con su `@` es tratamiento.
- Art. 4 inc. 1: los datos deben ser «ciertos, adecuados, pertinentes y no excesivos». El inc. 3 prohíbe usarlos para «finalidades distintas o incompatibles». El inc. 7 manda destruirlos cuando «hayan dejado de ser necesarios».

Nada contradice lo que ya dice [[wiki/proyecto/restricciones-legales-eticas]].

### 3.2 Art. 7: datos sensibles (no estaba analizado)

El art. 2 define como sensibles los datos que revelan, entre otras cosas, «opiniones políticas, convicciones religiosas». El art. 7 inc. 3 prohíbe formar archivos que **directa o indirectamente** revelen datos sensibles; la prohibición empieza con «Queda prohibida la formación de archivos, bancos o registros». El inc. 2 permite tratarlos con fines estadísticos o científicos cuando los titulares no puedan ser identificados.

**Lectura.** Un tuit político guardado junto al `@` del autor puede revelar su opinión política. Una tabla de cuentas con su historial sobre temas políticos se acerca a un «registro» que lo revela indirectamente. Es un flanco que la página legal no trata. Las defensas disponibles:

1. El art. 5 inc. 2 a) (fuente pública) exime del **consentimiento**, pero no de la prohibición del art. 7 inc. 3. Son cosas distintas, y el documento no debería mezclarlas.
2. La salida del inc. 2 —fines científicos con titulares no identificables— es la misma disociación que ya usa la cesión (art. 11 inc. 3.e). Lo que va al corpus de investigación y a lo B2B tiene que estar disociado.
3. El sistema clasifica **afirmaciones**, no opiniones ni personas. La señal de cuenta mide trayectoria de veracidad, no orientación política. Es un argumento de finalidad que conviene escribir.

`[sin verificar]`: no se encontró jurisprudencia ni dictamen de la AAIP sobre si un tuit público con opinión política es «dato sensible» a los fines del art. 7 inc. 3.

### 3.3 Art. 12: transferencia internacional (no estaba analizado)

El inc. 1 prohíbe transferir datos personales a países «que no propocionen niveles de protección adecuados» (la errata es del texto oficial). Las excepciones del inc. 2 (cooperación judicial, datos médicos, transferencias bancarias, tratados, inteligencia) no cubren este caso.

El Decreto 1558/2001 (Anexo I, art. 12) agrega tres salidas:

- **Consentimiento:** la prohibición «no rige cuando el titular de los datos hubiera consentido expresamente la cesión».
- **Contrato:** el nivel adecuado también puede surgir de «las cláusulas contractuales que prevean la protección de datos personales».
- La lista de países adecuados la decide la autoridad de aplicación.

**¿EE. UU. tiene nivel adecuado? No.** El art. 3 de la Disposición DNPDP 60-E/2016, en el texto que fijó la Resolución AAIP 34/2019, enumera: UE y EEE, Reino Unido, Suiza, Guernsey, Jersey, Isla de Man, Islas Feroe, Canadá («sólo respecto de su sector privado»), Andorra, Nueva Zelanda, Uruguay e Israel («sólo respecto de los datos que reciban un tratamiento automatizado»). Estados Unidos no figura. Los considerandos aclaran que no figurar no equivale a una calificación negativa, pero en la práctica obliga a usar otro mecanismo.

**Instrumentos de la AAIP para transferir a un país no adecuado:**

- **Disposición 60-E/2016**, art. 1: aprueba dos contratos tipo, uno para cesión (Anexo I) y otro para **prestación de servicios** (Anexo II). Art. 2: un contrato distinto de los modelos se presenta ante la autoridad dentro de los «TREINTA (30) días corridos de su firma».
- **Resolución AAIP 198/2023** (13/10/2023, publicada el 18/10/2023): incorpora las cláusulas modelo de la Red Iberoamericana de Protección de Datos. Según sus considerandos, son «compatibles con las cláusulas contractuales tipo» de 2016, que siguen vigentes.

**Lectura para el PFI.** Hay dos flujos hacia EE. UU.:

1. **Servicio → OpenAI.** Va solo el texto del tuit, sin `@`. El argumento fuerte es que, sin autor, el texto no refiere a una persona determinada (art. 2). Tiene un límite: el texto puede nombrar o mencionar a otras personas (`@terceros`, nombres propios), así que el envío no queda del todo libre de datos personales. OpenAI actúa como prestador de servicios, que es la situación del Anexo II. Su página de controles de datos dice que lo enviado por la API «is not used to train or improve OpenAI models» salvo que se lo active, y que los registros de abuso se guardan «for up to 30 days». No se pudo leer el DPA de OpenAI (HTTP 403), así que **no se verificó** si incluye cláusulas compatibles con la normativa argentina `[sin verificar]`.
2. **Extensión → servicio, y servicio → base.** El servicio corre en Railway. La región de despliegue no está documentada en el wiki `[sin verificar]`. Si es EE. UU., el `@` y los metadatos de cuenta **sí** se transfieren a un país no adecuado, y esta transferencia es más difícil de defender que la de OpenAI.

### 3.4 Art. 21: inscripción en el registro (no estaba analizado)

El inc. 1 obliga a inscribir todo archivo público y todo archivo privado «destinado a proporcionar informes». El Decreto 1558/2001 (Anexo I, art. 1) incluye ahí a los que «exceden el uso exclusivamente personal» y a los que tienen como fin la cesión de datos, «sin distinguir» si es onerosa o gratuita. El inc. 2 enumera lo que se declara al inscribir: responsable, finalidad, naturaleza de los datos, destinatarios, medidas de seguridad, tiempo de conservación y forma de ejercer los derechos de acceso.

**Lectura.** El prototipo académico, sin usuarios externos ni clientes, puede sostener que no está destinado a dar informes. El producto **sí** queda alcanzado: la extensión entrega a terceros un informe sobre publicaciones con datos de su autor, y lo B2B vende análisis. Hay que separar las dos etapas, como ya se hizo con la tienda de Chrome: no se inscribe para el PFI y la inscripción es condición previa a operar.

## 4. AAIP e inteligencia artificial

La **Resolución AAIP 161/2023** (30/08/2023, publicada el 04/09/2023) creó el «Programa de transparencia y protección de datos personales en el uso de la Inteligencia Artificial». Sus líneas de acción incluyen «Guías de buenas prácticas para entidades públicas y privadas» y la «Documentación de los Sistemas de Decisiones Automatizados (SDA)». Es un programa y no impone obligaciones. Sirve para fundamentar que documentar el sistema (qué decide, con qué datos, con qué límites) sigue el criterio de la autoridad.

La AAIP publicó además una guía para una IA responsable que recomienda evaluaciones de impacto y explicabilidad. Solo se vio el anuncio en `argentina.gob.ar`; no se leyó el texto ni se ubicó el acto que la aprueba `[sin verificar]`.

## 5. Modelos de *disclaimer*

| Actor | Qué declara (cita corta) | Qué se toma |
|---|---|---|
| **Chequeado**, Política de uso de IA (30/09/2025) | «la IA no reemplaza el criterio editorial ni profesional de nuestro equipo»; la IA tampoco se considera «una fuente de información primaria»; toda salida es «revisada y validada por una persona responsable» antes de publicarse | Declarar que la IA no es fuente y decir quién responde. El PFI **no tiene** revisión humana previa, así que debe decir lo contrario de forma explícita: el resultado es automático y no lo revisa una persona |
| **Community Notes** (documentación oficial, repo `twitter/communitynotes`) | «X doesn't rate or moderate notes»; las notas pueden proponerlas personas o «AI note writers» | Decir quién produce el juicio y cómo. El análogo del PFI: lo produce un modelo con evidencia recuperada, no un verificador |
| **NewsGuard**, Términos de servicio (22/07/2026) | «THERE MAY BE DELAYS, OMISSIONS, INTERRUPTIONS, AND INACCURACIES IN THE CONTENT»; las respuestas de su IA «may still contain errors»; «bias is, itself, a matter of opinion» | Reconocer errores posibles y limitar la responsabilidad. El tono de cláusula de exención en mayúsculas no sirve para la interfaz, pero sí para unos términos de uso |

Patrón común: (1) quién o qué produce el juicio, (2) que puede equivocarse, (3) que no reemplaza el criterio propio ni una verificación profesional, (4) dónde reclamar. El texto de finalidad que ya figura en la página legal cubre (1) y (3) en parte. Le faltan (2) y (4) dicho desde el lado del usuario, y la ausencia de revisión humana.

## Implicancias para el PFI

Qué tendría que decir el documento (cap. 2 §marco normativo y cap. 3 §viabilidad legal). No es redacción:

1. **Actualizar la cita de X a la versión del 9/10/2026** y sacar el `[sin verificar]`. Citar tres cláusulas: prohibición de *scraping*, prohibición de facilitar incumplimientos y ley y tribunal de Texas. La subsección «términos de las plataformas» tiene que reconocer la cláusula de facilitación: es la única que apunta a quien distribuye la extensión. La respuesta es que leer el DOM del *timeline* propio no incumple nada y que el prototipo no se distribuye.
2. **Declarar que el Developer Agreement no aplica porque no se usa la API**, y aun así mencionar la prohibición de entrenar modelos fundacionales y la lista de inferencias sensibles como límites que el diseño respeta. Decir de dónde sale el corpus de *fine-tuning* del clasificador y que no se entrena con tuits capturados por la extensión. Si se entrena con ellos, hay que reconocerlo como riesgo frente a los términos de X.
3. **Agregar el art. 7 (datos sensibles)** en la subsección de datos personales. El consentimiento (art. 5) y la prohibición de archivos sensibles (art. 7 inc. 3) son cosas distintas. La defensa es disociación más finalidad: se juzgan afirmaciones y no personas.
4. **Agregar el art. 12 (transferencia internacional)**: EE. UU. no está en la lista de la Disp. 60-E/2016 (texto de la Res. 34/2019). A OpenAI va solo el texto, sin `@`, que es el argumento fuerte, con el límite de las menciones a terceros. Para el producto, nombrar los instrumentos disponibles: contrato de prestación de servicios del Anexo II de la Disp. 60-E/2016 o cláusulas de la Res. 198/2023. **Antes de escribir, confirmar la región de Railway**: si es EE. UU., el `@` también cruza la frontera y hay que decirlo.
5. **Agregar el art. 21 (registro)** separando etapas: el prototipo académico no está destinado a dar informes y el producto, con extensión pública y B2B, sí debería inscribirse.
6. **Citar la Res. AAIP 161/2023** como respaldo de la documentación del sistema de decisiones automatizadas. Encaja con el principio de explicabilidad que ya cumple RNF-06.
7. **Bibliografía nueva** para `biblio.bib`: Disposición DNPDP 60-E/2016, Resolución AAIP 34/2019, Resolución AAIP 198/2023, Resolución AAIP 161/2023, X Developer Agreement and Policy (2026), y actualizar `XCorp2024` a la versión de 2026.

**Disclaimer a agregar en la extensión.** Hoy el texto de finalidad dice «no una verificación profesional ni un veredicto definitivo». Faltan cuatro cosas, tomadas del patrón de la sección 5:

- Que el resultado lo genera **automáticamente** un modelo de lenguaje, **sin revisión humana** previa.
- Que **puede equivocarse**, y que el usuario debe abrir las fuentes enlazadas antes de compartir o actuar.
- Que **juzga la afirmación y no a la persona** que la publicó. Hoy está en el *prompt*, pero no en la interfaz.
- Que el texto analizado se envía a un **proveedor externo en EE. UU.** (OpenAI) sin el nombre de usuario del autor. Además, si se eligiera el consentimiento como vía del art. 12, este aviso sería su presupuesto: el Decreto 1558/2001 exige que el consentimiento esté «precedido de una explicación».

## Referencias cruzadas

- [[wiki/proyecto/restricciones-legales-eticas]]
- [[wiki/solucion/arquitectura]]
- [[wiki/solucion/tecnologias]]
- [[wiki/solucion/modelo-datos]]
- [[wiki/solucion/requerimientos]]

## Fuentes

Todas consultadas el 2026-10-19.

| Fuente | URL |
|---|---|
| X — Terms of Service (vigente desde el 9/10/2026), copia de Open Terms Archive | https://x.com/tos · https://github.com/OpenTermsArchive/pga-versions/blob/main/X/Terms%20of%20Service.md |
| X — Developer Agreement (27/04/2026) y Developer Policy, copia de Open Terms Archive | https://developer.x.com/en/developer-terms/agreement-and-policy · https://github.com/OpenTermsArchive/pga-versions/blob/main/X/Developer%20Terms.md |
| Ley 25.326, texto actualizado | https://servicios.infoleg.gob.ar/infolegInternet/anexos/60000-64999/64790/texact.htm |
| Decreto 1558/2001 | https://servicios.infoleg.gob.ar/infolegInternet/anexos/70000-74999/70368/norma.htm |
| Disposición DNPDP 60-E/2016 (texto actualizado por la Res. AAIP 34/2019) | https://servicios.infoleg.gob.ar/infolegInternet/anexos/265000-269999/267922/texact.htm |
| Resolución AAIP 34/2019 | https://www.boletinoficial.gob.ar/detalleAviso/primera/202373/20190226 |
| Resolución AAIP 198/2023 | https://www.boletinoficial.gob.ar/detalleAviso/primera/296189/20231018 |
| Resolución AAIP 161/2023 | https://www.argentina.gob.ar/normativa/nacional/norma-389231/texto |
| OpenAI — Data controls in the OpenAI platform | https://developers.openai.com/api/docs/guides/your-data |
| Chequeado — Política de uso de IA | https://chequeado.com/politica-de-uso-de-ia-en-chequeado/ |
| Community Notes — documentación (repo oficial) | https://github.com/twitter/communitynotes/blob/main/documentation/about/introduction.md |
| NewsGuard — Terms of Service | https://www.newsguardtech.com/terms-of-service/ |
