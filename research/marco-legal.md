---
titulo: Investigación — marco legal (ToS de X, Ley 25.326, AAIP y disclaimers)
tipo: análisis
tags: [legal, investigacion, lpdp, aaip, x-tos, disclaimer, borrador]
fuentes: []
actualizado: 2026-10-19
---

# Marco legal: ToS de X, Ley 25.326, AAIP y modelos de *disclaimer*

Responde al *issue* #75. Todas las fuentes se consultaron el **2026-10-19**. El objetivo es cubrir lo que hoy falta en la sección «Viabilidad legal» del capítulo 3 (`sec:legal`, `documento/chapters/chapter03.tex`) y en [[wiki/proyecto/restricciones-legales-eticas]].

**Relación con la página previa.** Esta misma rama ya tenía un commit (`34da7c4`) con `wiki/sintesis/investigacion-marco-legal-x-25326.md`, hecho en otra sesión. Este archivo es la versión pedida en `research/`. Coincide con aquella en casi todo y agrega tres cosas: el art. 24 de la ley, que cambia la lectura sobre la inscripción del prototipo (§2.5), la verificación del DPA de OpenAI, que estaba pendiente por un 403 (§2.4), y el procedimiento vigente de inscripción ante la AAIP (§2.6).

**Criterio de citas.** Las normas argentinas se citan textuales y completas. Los términos de empresas privadas (X, NewsGuard, Chequeado, OpenAI) son textos con derechos de autor: se citan en fragmentos breves y el resto se resume.

---

## 1. Términos de X

### 1.1 Fuente y versión

- **Terms of Service**, *«Effective: October 9, 2026»*. La versión vigente es la de https://x.com/tos.
- x.com y docs.x.com no respondieron desde este entorno (*timeout* en WebFetch y en Chrome). El texto se leyó en la copia de **Open Terms Archive**, que archiva el documento oficial sin modificarlo: `OpenTermsArchive/pga-versions`, archivo `X/Terms of Service.md`, *commit* `990ea3e` del 2026-10-10. Lo que se baja es https://x.com/tos, según `pga-declarations/declarations/X.json`.
- **Developer Agreement** (*«Last Updated: April 27, 2026»*), **Developer Policy** y **Restricted uses of the X API**: misma fuente, archivo `X/Developer Terms.md`, *commit* `6b59c5d` del 2026-09-18. Las páginas originales son https://docs.x.com/developer-terms/agreement, https://docs.x.com/developer-terms/policy y https://docs.x.com/developer-terms/restricted-use-cases.
- La clave `XCorp2024` de `biblio.bib` quedó desactualizada: la versión vigente es del 9/10/2026.

### 1.2 Qué dicen las cláusulas que importan

| Cláusula (ToS, sección «Misuse of the Services» salvo que se indique) | Fragmento textual | Lectura para la extensión |
|---|---|---|
| Acceso solo por interfaces publicadas, inc. (iii) | prohibido acceder «by any means (automated or otherwise) other than through our currently available, published interfaces» | La interfaz web de x.com **es** una interfaz publicada. La extensión lee lo que esa interfaz ya le mostró al usuario, así que el argumento del capítulo 3 se sostiene. |
| *Scraping* | «crawling or scraping the Services in any form, for any purpose without our prior written consent is expressly prohibited» | El término *scraping* no está definido. X podría leer como *scraping* la lectura del DOM con envío del texto a un servidor. **Riesgo interpretativo, no resuelto por el texto.** |
| **Facilitación (nuevo frente al análisis previo)** | infracción también «to facilitate or assist others in violating these Terms, including by distributing products or services that enable or encourage violation» | **Apunta a quien distribuye la extensión, no solo al usuario.** Contradice la afirmación de la wiki de que el incumplimiento no genera responsabilidad para quien desarrolla la extensión (ver §4). |
| Daños pactados (sección «Liquidated Damages») | quien viole los términos, «or you induce or knowingly facilitate others to do so», responde por «$15,000 USD per 1,000,000 posts» por encima de un millón de publicaciones en 24 h | El umbral es por volumen. Una extensión que analiza lo que una persona mira queda muy lejos, salvo que se sume el volumen de todos los usuarios bajo la figura de «facilitate». Exposición teórica baja, pero el texto la nombra. |
| Ley y foro | «The laws of the State of Texas … will govern»; tribunales de Texas (Irlanda para residentes de la UE, la AELC y el Reino Unido) | Un usuario argentino contrata con X Corp. (Austin, Texas). |
| Suspensión | X puede suspender la cuenta si cree razonablemente que «you have violated these Terms» | Confirma el riesgo del usuario que ya nombra la wiki. |
| Titularidad del contenido | «What's yours is yours — you own your Content» | El autor del tuit sigue siendo su titular. Coincide con la Ley 11.723 del capítulo 3. |
| Exactitud del contenido | X no garantiza la «truthfulness, accuracy, or reliability» de lo publicado | Sirve también como modelo de *disclaimer* (§3). |

### 1.3 Developer Agreement y Developer Policy

- **Ámbito.** *«Licensed Material» means … the X API and X Content*. *X Content* son las publicaciones y los datos «made available to you through the X API or by any other means authorized by X». La extensión no usa la API, así que el Agreement **no la vincula directamente**. Si X sostuviera que leer el DOM es un medio no autorizado, tampoco se aplicaría el Agreement: se aplicarían los ToS.
- **Límites que conviene declarar igual**, como pauta de buena práctica:
  - Agreement, III.A (k): prohíbe usar el contenido de X «to fine-tune or train a foundation or frontier model». Ajustar XLM-T como clasificador no es entrenar un modelo fundacional, pero conviene decirlo así.
  - Developer Policy / Restricted uses, apartado «Sensitive information»: prohíbe inferir o almacenar lo inferido sobre la «Political affiliation or beliefs» de un usuario, o la «Alleged or actual commission of a crime». Admite el análisis agregado que no guarda identificadores.
  - Redistribución: a terceros solo se pueden entregar IDs de publicaciones y de usuarios, no el contenido. Coincide con la decisión de no distribuir el corpus.

---

## 2. Ley 25.326 y normativa de la AAIP

Texto consolidado de la ley: https://servicios.infoleg.gob.ar/infolegInternet/anexos/60000-64999/64790/texact.htm. Decreto reglamentario 1558/2001: https://servicios.infoleg.gob.ar/infolegInternet/anexos/70000-74999/70368/norma.htm.

### 2.1 Art. 2: definiciones

> Datos sensibles: Datos personales que revelan origen racial y étnico, opiniones políticas, convicciones religiosas, filosóficas o morales, afiliación sindical e información referente a la salud o a la vida sexual.

> Tratamiento de datos: Operaciones y procedimientos sistemáticos, electrónicos o no, que permitan la recolección, conservación, ordenación, almacenamiento, modificación, relacionamiento, evaluación, bloqueo, destrucción, y en general el procesamiento de datos personales, así como también su cesión a terceros a través de comunicaciones, consultas, interconexiones o transferencias.

### 2.2 Art. 5 inc. 2 a): fuentes de acceso público

> 2. No será necesario el consentimiento cuando: a) Los datos se obtengan de fuentes de acceso público irrestricto;

Exime **del consentimiento** y de nada más. No exime de los arts. 7, 12 ni 21.

### 2.3 Art. 7: datos sensibles (no tratado en el capítulo 3)

> 1. Ninguna persona puede ser obligada a proporcionar datos sensibles.
> 2. Los datos sensibles sólo pueden ser recolectados y objeto de tratamiento cuando medien razones de interés general autorizadas por ley. También podrán ser tratados con finalidades estadísticas o científicas cuando no puedan ser identificados sus titulares.
> 3. Queda prohibida la formación de archivos, bancos o registros que almacenen información que directa o indirectamente revele datos sensibles. Sin perjuicio de ello, la Iglesia Católica, las asociaciones religiosas y las organizaciones políticas y sindicales podrán llevar un registro de sus miembros.

Decreto 1558/2001, art. 7: «Sin reglamentar.»

**Lectura.** La base guarda el texto del tuit junto con el `@` del autor. Un tuit político con su autor identificado es información que «directa o indirectamente» revela opiniones políticas. El inc. 3 prohíbe formar ese archivo, y el art. 5 inc. 2 a) no lo salva, porque solo exime del consentimiento. La única salida que da el propio artículo es el inc. 2, segunda oración: finalidad estadística o científica **con titulares no identificables**. En consecuencia:

- La defensa se apoya en la **disociación**, la misma del art. 11 inc. 3 e) que ya usa el capítulo 3, aplicada también al almacenamiento y no solo a la cesión.
- Concuerda con el art. 28 inc. 1, que excluye de la ley las «investigaciones científicas … en la medida que los datos recogidos no puedan atribuirse a una persona determinada o determinable».
- **Flanco abierto:** mientras el `@` se conserve en claro, y el historial por cuenta del Módulo 2 lo necesita, el inc. 3 queda expuesto. Un argumento de defensa: el sistema evalúa la veracidad de una afirmación fáctica, no la opinión del autor, y no clasifica a nadie por su ideología. Ese argumento es interpretativo `[sin verificar en doctrina o jurisprudencia]`.

### 2.4 Art. 12: transferencia internacional (no tratado en el capítulo 3)

> 1. Es prohibida la transferencia de datos personales de cualquier tipo con países u organismos internacionales o supranacionales, que no propocionen niveles de protección adecuados.

(«propocionen» figura así en el texto oficial.) El inc. 2 enumera las excepciones: colaboración judicial, datos médicos, transferencias bancarias, tratados e inteligencia. Ninguna aplica.

**Decreto 1558/2001, art. 12:**

> La prohibición de transferir datos personales hacia países u organismos internacionales o supranacionales que no proporcionen niveles de protección adecuados, no rige cuando el titular de los datos hubiera consentido expresamente la cesión.

> Se entiende que un Estado u organismo internacional proporciona un nivel adecuado de protección cuando dicha tutela se deriva directamente del ordenamiento jurídico vigente, o de sistemas de autorregulación, o del amparo que establezcan las cláusulas contractuales que prevean la protección de datos personales.

**EE. UU. no es país adecuado.** Disposición DNPDP 60-E/2016, art. 3 (https://www.argentina.gob.ar/normativa/nacional/267922/texto): la lista comprende los Estados de la UE y del EEE, Suiza, Guernsey, Jersey, Isla de Man, Islas Feroe, Canadá (solo el sector privado), Andorra, Nueva Zelanda, Uruguay e Israel (solo datos con tratamiento automatizado). La Resolución AAIP 34/2019 agregó al Reino Unido. **Estados Unidos no figura.**

**Instrumentos disponibles:**

- Disposición 60-E/2016, art. 1: aprueba cláusulas contractuales tipo «para la cesión y prestación de servicios» (Anexos I y II). Art. 2: quien use un contrato distinto del modelo debe pedir su aprobación a la autoridad de control dentro de los «TREINTA (30) días corridos de su firma».
- **Resolución AAIP 198/2023** (RESOL-2023-198-APN-AAIP, 13/10/2023, BO 18/10/2023, https://www.boletinoficial.gob.ar/detalleAviso/primera/296189/20231018), art. 1: «Aprobar las cláusulas contractuales modelo para transferencias internacionales» de la guía de la Red Iberoamericana. Los considerandos las declaran «compatibles con las cláusulas contractuales tipo aprobadas por la Disposición de la DNPDP N° 60/2016».
- **OpenAI** (https://openai.com/es-ES/enterprise-privacy/, «Actualización: 8 de enero de 2026», leído en Chrome): ofrece firmar un «Anexo de Tratamiento de Datos (DPA)» para la API y declara que «De forma predeterminada, no entrenamos nuestros modelos con tus datos». **Esto resuelve el pendiente de la página previa.** El contenido del DPA (si incluye cláusulas tipo, y cuáles) no se verificó: el texto está detrás de un formulario.

**Lectura.**

- **Servicio → OpenAI.** Según `prototipo/servicio/app/proveedor/openai.py`, el *prompt* lleva solo el texto de la publicación, sin el `@`. Sin autor, el texto no refiere en principio a una persona determinada (art. 2). En ese caso no hay dato personal y el art. 12 no se activa. **Límite:** el texto puede nombrar a terceros (`@menciones`, nombres propios), y en esa medida sí cruza la frontera un dato personal, posiblemente sensible si es político.
- **Para el producto:** firmar el DPA de OpenAI y verificar que contenga cláusulas equivalentes a las del Anexo II de la Disp. 60-E/2016 o a las de la Res. 198/2023. Si difieren, presentarlo ante la AAIP dentro de los 30 días (Disp. 60-E/2016, art. 2).
- **Transferencia propia del servicio:** si la base de datos o el servicio se alojan en EE. UU., el `@` y los metadatos de cuenta sí se transfieren. La región de alojamiento no está documentada `[sin verificar]`.
- **Encargado del tratamiento:** OpenAI actúa como prestador de servicios del art. 25 de la ley, que prohíbe aplicar los datos «con un fin distinto al que figure en el contrato de servicios». El art. 25 del decreto exige que esos contratos contengan los niveles de seguridad y las obligaciones de confidencialidad.

### 2.5 Arts. 3, 21 y 24: inscripción de la base (no tratado en el capítulo 3)

Ley, art. 3:

> La formación de archivos de datos será lícita cuando se encuentren debidamente inscriptos, observando en su operación los principios que establece la presente ley y las reglamentaciones que se dicten en su consecuencia.

Ley, art. 21 inc. 1:

> Todo archivo, registro, base o banco de datos público, y privado destinado a proporcionar informes debe inscribirse en el Registro que al efecto habilite el organismo de control.

El inc. 2 enumera lo que se declara: responsable, finalidad, naturaleza de los datos, forma de recolección, destino, interrelación, seguridad, «Tiempo de conservación de los datos» y modo de acceso. El inc. 3 agrega:

> Ningún usuario de datos podrá poseer datos personales de naturaleza distinta a los declarados en el registro.

Ley, art. 24 (no citado en la página previa):

> Los particulares que formen archivos, registros o bancos de datos que no sean para un uso exclusivamente personal deberán registrarse conforme lo previsto en el artículo 21.

Decreto 1558/2001, art. 1:

> … quedan comprendidos en el concepto de archivos, registros, bases o bancos de datos privados destinados a dar informes, aquellos que exceden el uso exclusivamente personal y los que tienen como finalidad la cesión o transferencia de datos personales, independientemente de que la circulación del informe o la información producida sea a título oneroso o gratuito.

**Lectura (difiere de la página previa).** El criterio legal no es si la base «da informes» en sentido coloquial, sino si **excede el uso exclusivamente personal**. La página previa sostiene que el prototipo académico «puede sostener que no está destinado a dar informes». Esa posición es débil:

- la base guarda datos de terceros (los autores de los tuits);
- se construye para un sistema que entrega resultados a otros usuarios;
- la finalidad declarada incluye el historial por cuenta y el producto B2B.

La postura defendible es más estrecha. Mientras el prototipo lo use solo su autor, en modo desarrollador, puede argumentarse uso personal con fines académicos. Desde que lo usen terceros, aun gratis, la base excede el uso personal y debe inscribirse (art. 24). El art. 3 además condiciona la **licitud** del archivo a la inscripción. El tiempo de conservación (inc. 2 h) deberá declararse aunque la ley no fije un plazo, y la finalidad estrecha del capítulo 3 es lo que se declararía.

### 2.6 Estado actual del registro ante la AAIP

- **Procedimiento vigente** (https://www.argentina.gob.ar/aaip/datospersonales/tramites): tiene dos pasos. «La inscripción del responsable es requisito previo para registrar una base de datos personales».
  - Responsable privado: https://www.argentina.gob.ar/servicio/inscribir-un-responsable-de-bases-de-datos-personales-privadas, por Trámites a Distancia con clave fiscal nivel 2. Costo: «Gratuito».
  - Base privada: https://www.argentina.gob.ar/registrar-bases-de-datos-personales-privadas, con el número de registro del responsable. Costo: «Gratuito».
  - La AAIP emite un certificado de inscripción con código QR.
- **Resoluciones recientes vinculadas:** Res. AAIP 126/2024 y **179/2025** (30/09/2025) sobre el **Registro de Infractores** de las Leyes 25.326 y 26.951, no sobre el de bases (https://www.argentina.gob.ar/normativa/nacional/norma-418053/texto). No se encontró una resolución de 2025–2026 que cambie la inscripción de bases privadas `[búsqueda en BO no exhaustiva]`.
- **Inteligencia artificial:** la Res. AAIP 161/2023 creó un programa de transparencia y protección de datos en el uso de IA. No impone obligaciones; ver la página previa.
- **Reforma:** el proyecto 1751-D-2026 sigue sin ser ley; ya está tratado en [[wiki/proyecto/restricciones-legales-eticas]].

---

## 3. Modelos de *disclaimer* de herramientas de verificación

| Fuente | Qué dice (fragmento breve y resumen) | Qué tomar para Factum |
|---|---|---|
| **Chequeado**, Política de confidencialidad (https://chequeado.com/politica-de-confidencialidad/, leída en Chrome porque el sitio bloquea clientes que no son navegadores) | Declara que no asume «responsabilidad alguna por cualquier demora, inexactitud, error u omisión» en su material, ni por los sitios enlazados. Cita la Ley 25.326 y se abstiene de pedir datos sensibles (art. 7). | Separar la responsabilidad por las fuentes enlazadas. Mencionar la Ley 25.326 en el aviso. |
| **Chequeado**, Métodos (https://chequeado.com/metodo/) | Admite que «nadie es perfecto» y se compromete a rectificar la información inexacta, con una política de correcciones. | Un verificador profesional promete corregir y no infalibilidad. El canal de reporte de RF-11 cumple ese papel. |
| **NewsGuard**, Terms of Service (https://www.newsguardtech.com/terms-of-service/, «Last Updated On July 22, 2026») | §6.1: servicio «AS IS», sin garantía de estar libre de errores. §6.2: las respuestas las redacta IA generativa y «some errors remain possible»; además, «bias is, itself, a matter of opinion». §6.3: limita la responsabilidad por daños indirectos. §5.1: la extensión de navegador es «for personal use only». | Es el modelo más cercano a un sistema con LLM. Dice explícitamente que hay IA generativa en la redacción, que puede errar y que la imparcialidad es discutible. |
| **X**, ToS | No garantiza la exactitud del contenido; uso «at your own risk». | Esquema de base para la exclusión de garantías. |

**Elementos recomendados para el texto de la extensión**, como complemento de la «Finalidad declarada» que ya está en la wiki:

1. El resultado lo produce un sistema automático con un modelo de lenguaje, sin revisión humana (NewsGuard §6.2).
2. Puede equivocarse, y el usuario puede reportarlo (Chequeado, RF-11).
3. El resultado juzga la afirmación y no a la persona que la publicó (art. 113 CP y Developer Policy de X).
4. Las fuentes enlazadas son de terceros, y Factum no responde por su contenido (Chequeado).
5. El texto analizado se envía, sin el nombre de usuario, a un proveedor externo con servidores en EE. UU. Si se optara por el consentimiento del art. 12, el Decreto 1558/2001, art. 5, exige que esté «precedido de una explicación».
6. Uso personal de la extensión (NewsGuard §5.1).

---

## 4. Contradicciones con lo que hoy afirma el documento o la wiki

> ⚠️ CONTRADICCION: [[wiki/proyecto/restricciones-legales-eticas]] («Modalidad 1») afirma que el incumplimiento de los términos «No genera responsabilidad para quien desarrolla la extensión». Los ToS del 9/10/2026 tipifican como infracción «distributing products or services that enable or encourage violation» de los términos y extienden los daños pactados a quien «knowingly facilitate». El riesgo sigue siendo contractual y de baja probabilidad, pero ya no es solo del usuario.

> ⚠️ CONTRADICCION: el capítulo 3, `sec:legal`, apoya la recolección solo en el art. 5 inc. 2 a). Ese inciso exime del consentimiento, no de la prohibición del **art. 7 inc. 3** sobre archivos que revelen opiniones políticas, y el capítulo no menciona el art. 7.

> ⚠️ CONTRADICCION: el capítulo 3 llama a la cesión (art. 11) «el punto más expuesto». No analiza la **transferencia internacional del art. 12** (EE. UU. no es país adecuado) ni la **inscripción de los arts. 3, 21 y 24**, que condiciona la licitud misma del archivo. Las dos exposiciones son al menos tan relevantes como la cesión.

> ⚠️ Matiz: el capítulo 3 dice que la extensión opera «sin acceder de forma automatizada a sistema alguno». Es correcto frente a la cláusula de las interfaces publicadas, pero no responde a la prohibición de *scraping* «in any form» ni a la cláusula de facilitación. Conviene nombrarlas y responderlas.

> ⚠️ Matiz: `XCorp2024` en `biblio.bib` y la nota de la wiki «año 2024 … `[sin verificar]`» quedan superados por la versión del 9/10/2026.

## 5. Pendientes

- Región de alojamiento de la base y del servicio. Define si el `@` se transfiere a EE. UU.
- Contenido del DPA de OpenAI y su equivalencia con el Anexo II de la Disp. 60-E/2016 o con la Res. 198/2023.
- Confirmar la vigencia del texto de X directamente en x.com desde un navegador (aquí se usó la copia de Open Terms Archive).
- Doctrina o jurisprudencia sobre si un tuit político con autor identificado configura un archivo de datos sensibles (art. 7 inc. 3).

## Fuentes (consultadas el 2026-10-19)

| Fuente | URL |
|---|---|
| Ley 25.326 (texto actualizado) | https://servicios.infoleg.gob.ar/infolegInternet/anexos/60000-64999/64790/texact.htm |
| Decreto 1558/2001 | https://servicios.infoleg.gob.ar/infolegInternet/anexos/70000-74999/70368/norma.htm |
| Disposición DNPDP 60-E/2016 | https://www.argentina.gob.ar/normativa/nacional/267922/texto |
| Resolución AAIP 198/2023 | https://www.boletinoficial.gob.ar/detalleAviso/primera/296189/20231018 |
| Resolución AAIP 179/2025 | https://www.argentina.gob.ar/normativa/nacional/norma-418053/texto |
| AAIP — trámites del Registro Nacional de Bases de Datos | https://www.argentina.gob.ar/aaip/datospersonales/tramites |
| AAIP — inscribir responsable privado | https://www.argentina.gob.ar/servicio/inscribir-un-responsable-de-bases-de-datos-personales-privadas |
| AAIP — registrar base privada | https://www.argentina.gob.ar/registrar-bases-de-datos-personales-privadas |
| X Terms of Service (9/10/2026) | https://x.com/tos (copia: https://github.com/OpenTermsArchive/pga-versions/blob/main/X/Terms%20of%20Service.md) |
| X Developer Agreement, Policy y Restricted uses | https://docs.x.com/developer-terms/agreement · https://docs.x.com/developer-terms/policy · https://docs.x.com/developer-terms/restricted-use-cases (copia: https://github.com/OpenTermsArchive/pga-versions/blob/main/X/Developer%20Terms.md) |
| OpenAI — Privacidad empresarial (8/1/2026) | https://openai.com/es-ES/enterprise-privacy/ |
| Chequeado — Política de confidencialidad | https://chequeado.com/politica-de-confidencialidad/ |
| Chequeado — Métodos | https://chequeado.com/metodo/ |
| NewsGuard — Terms of Service (22/7/2026) | https://www.newsguardtech.com/terms-of-service/ |

## Referencias cruzadas

- [[wiki/proyecto/restricciones-legales-eticas]]
- [[wiki/sintesis/investigacion-marco-legal-x-25326]]
- [[wiki/solucion/modelo-datos]]
