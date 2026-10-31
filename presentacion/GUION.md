# Guion de la exposición — Entrega 90 %

Sábado 31/10/2026, 10:40, grupo SA25. **10:00 en total**, demo en vivo incluida.

Texto para decir tal cual. Los pasajes marcados con **🔒 DE MEMORIA** se dicen palabra
por palabra, sin mirar: son los 3 que se perdieron en el 50 % (la escala, las
limitaciones y el cierre).

Todas las cifras salen del documento entregado (capítulos 3 y 4 y conclusiones). Si una
cifra del wiki no coincide, manda el documento.

| # | Lámina | Tiempo | Acumulado |
|---|---|---|---|
| 1 | Portada | 0:05 | 0:05 |
| 1b | ¿Cuáles son verdad? | 0:15 | 0:20 |
| 2 | Problema | 0:30 | 0:50 |
| 2b | La respuesta | 0:20 | 1:10 |
| 3 | Competencia y diferencial | 1:00 | 2:10 |
| 4 | Arquitectura | 1:00 | 3:10 |
| 5 | Demo, en vivo y grabada | 3:35 | 6:45 |
| 6 | Negocio | 2:00 | 8:45 |
| 7 | Limitaciones, trabajo futuro y cierre | 1:15 | 10:00 |
| 8 | Gracias | — | preguntas |

---

## Lámina 1 · Portada — 0:05

Buenos días, soy Juan Martín Bejarano y les presento Factum.

*(La carrera, el tutor y la entrega ya están en la portada: no se dicen.)*

## Lámina 1b · ¿Cuáles son verdad? — 0:15

*(6 publicaciones en el estilo de X, con el indicador de la extensión al pie. Dejás que
las lean 2 segundos.)*

Todos los días entramos a X para enterarnos de lo que pasa en el país: política,
economía. Y nos cruzamos con publicaciones como estas. ¿Cuáles son verdad? No lo sabemos.
Y casi nadie sale a chequearlo: lo que leemos ahí termina formando nuestra opinión, sea
cierto o no.

*(No se responde todavía: la respuesta llega en la 2b, después del problema.)*

## Lámina 2 · Problema — 0:30

El problema es de escala. En la Argentina hay 31 millones de usuarios de redes
sociales, y solo 3 de cada 10 confían en los medios. Y en X, una afirmación verdadera
tarda unas 6 veces más que una falsa en llegar a 1.500 personas.

La verificación profesional es rigurosa, pero revisa de a una afirmación y casi siempre
después de que circuló. No le falta rigor: le falta escala.

*(La encuesta no se presenta: queda para las preguntas, ver PREGUNTAS.md.)*

## Lámina 2b · La respuesta — 0:20

*(Vuelven las 6 publicaciones; al medio segundo aparece el veredicto de cada una.)*

Por eso Factum es una extensión de Chrome que pone sobre cada publicación de X un veredicto
con sus fuentes. Las 6 de recién: 3 son verdad y 3 son falsas, y cada una dice con
qué fuente se comprobó. No entrega un número solo: entrega el número y el camino para
comprobarlo.

*(Si preguntan: son publicaciones de ejemplo, con las cuentas enmascaradas; los
veredictos en vivo, en la demo. Datos verificados el 30/10/2026: SIPA, unos 6,2 millones
de asalariados privados registrados contra 3,4 millones públicos; INDEC, inflación 2023
211,4 % y pobreza del primer semestre de 2024 52,9 %; Ley 27.610, aborto legal hasta la
semana 14, vigente desde enero de 2021; Ley 27.742, YPF quedó fuera de la lista de
privatizaciones; ANMAT, las vacunas no contienen chips.)*

## Lámina 3 · Competencia y diferencial — 1:00

Hay 3 diferenciales. El primero es el camino a la evidencia: cada veredicto enlaza el
documento de origen, el INDEC o el Boletín Oficial, y no una nota de otro medio. El
segundo es el alcance: las Notas de la Comunidad llegan cuando hay consenso, horas
después y a una fracción de las publicaciones. Este sistema llega a todas las que el
usuario tiene en pantalla, con fuentes argentinas. El tercero es el acceso: las
herramientas automáticas, como Cyabra o Blackbird.AI, se venden con licencias para
empresas y gobiernos, y NewsGuard cobra 8 dólares por mes y no cubre la Argentina.
Factum es gratis para el ciudadano.

La solución más parecida es InTruth, una extensión gratuita de este año, pero verifica el
audio de debates contra la web abierta, no el texto de X.

## Lámina 4 · Arquitectura — 1:00

Así se analiza un tuit, de izquierda a derecha. La extensión lo toma de X y se lo manda a
una API, que lo reparte en 3 módulos en paralelo.

El primero es un clasificador basado en BETO, un modelo de NLP preentrenado en español, al
que le hice *fine-tuning* en 2 etapas: primero con un corpus académico de noticias y
después con afirmaciones de Chequeado. Con la segunda etapa, sobre tuits argentinos, el F1
pasó de 0,42 a 0,52. Pesa 25 % del resultado.

El segundo mira señales públicas de la cuenta: antigüedad, seguidores y verificación. Pesa
un 10 %, porque esas señales se compran.

El tercero contrasta la afirmación con fuentes oficiales, con los medios de ADEPA y con
verificadores, usando un LLM con búsqueda web restringida a esas fuentes. Abajo, una ingesta
programada mantiene al día el índice de fuentes oficiales. Pesa 65 %.

El cuarto, el combinador, junta los 3 en un veredicto con su fuente, que vuelve a la
extensión. Todo corre en la nube por unos 13 dólares por mes.

*(Las tecnologías, TypeScript, FastAPI, SQLite, Railway, no se nombran, y la base de datos
del histórico no está en la lámina: todo eso está en el respaldo, en el C4 de contenedores,
por si preguntan.)*

*(Si preguntan por el fine-tuning: NLP es procesamiento de lenguaje natural. Sobre los
94 tuits argentinos verificados, la primera etapa dio F1 macro 0,422 y AUC-ROC 0,534; con
la segunda, F1 0,518 y AUC 0,545. El F1 sube 10 puntos, pero el AUC casi no se mueve:
el clasificador solo sigue cerca del azar, y por eso el contraste de fuentes pesa 65 %.
Sobre el corpus académico, después de la primera etapa, BETO había sacado F1 0,76.
Fuente: tablas del capítulo 4.)*

*(Si preguntan por los resultados, ya no hay lámina: F1 macro del sistema completo 0,712,
con intervalo de 0,61 a 0,80, contra una meta de 0,75 que no se alcanzó. BETO solo: 0,76
en el corpus académico, 0,42 en los 94 tuits argentinos y 0,52 después de Chequeado; el
contraste suma 19 puntos. Precisión 1,00 en la clase *falso*: ninguna publicación
verdadera señalada como falsa. Latencia del análisis profundo: 16 s en el percentil 95,
contra 8. Pruebas: 137 en el servicio con 93 % de cobertura, 27 en la extensión, SUS 74.
La tabla está en el respaldo.)*

## Lámina 5 · Demo, en vivo y grabada — 3:35

*(La lámina muestra la grabación. Primero va la demo en vivo: decís la escala con la
lámina en pantalla y cambiás a Chrome.)*

**🔒 DE MEMORIA — la escala, antes de cualquier número:**

> La cifra que van a ver son las chances de que la afirmación sea verdadera, de 0 a
> 100. Más alto es mejor. Por encima de 34, parece verificado; de 30
> para abajo, contradicho por fuentes oficiales; en el medio, información sospechosa.

*(Cambiás a la ventana de Chrome con X abierto. Ver «La demo, paso a paso».)*

Sobre cada publicación la extensión muestra una señal del texto, que no es un veredicto.
El veredicto aparece al pedir el análisis.

Este es un caso falso que ya analicé: resuelve al instante porque está en la caché.
Contradicho por fuentes oficiales, y acá dice cuál. Este otro es verdadero: parece
verificado, con la página del INDEC enlazada.

Ahora uno nuevo, en vivo. Mientras corre: este es el análisis profundo, el que tarda entre
8 y 16 segundos.

*(Al llegar el resultado, abrís el panel de evidencia.)* Cada fuente abre el documento
original. Y acá abajo, «Cómo se analiza»: contra qué fuentes se contrasta, con el enlace
al padrón de ADEPA. Los medios no los elijo yo.

*(Volvés al deck, a la misma lámina 5.)*

Esta es la misma demo, grabada para la defensa del 50 %: el mismo recorrido
sobre una publicación que no estaba en la caché, de punta a punta.

*(Reproducís el video y lo narrás por encima. Dura 2:37: cortala a los 1:45 o antes. Si la
demo en vivo falló, acá está todo el recorrido; si salió bien, mostrá solo el tramo del
panel de evidencia y pasá. Para que se escuche tu voz, bajá el volumen del video.)*

## Lámina 6 · Negocio — 2:00

El modelo tiene 2 lados. El ciudadano no paga: la extensión es gratis, con 5
análisis nuevos por mes. Pagan las organizaciones. El cliente ideal es un medio o un
verificador que quiere chequear en volumen: la API arranca en 200 dólares por mes
con 5.000 consultas. Los observatorios pagan 300 por el panel de tendencias. Y
ese precio no es arbitrario: la cuota de cada nivel está calculada para que el margen siga
positivo aunque el cliente la use entera, y lo comparé con herramientas parecidas.

Lo evalué a 5 años, con impuestos y cargas sociales, a una tasa del 25 %, en 3
escenarios. En el neutral, el más probable, el VAN es de 64.000 dólares, la TIR del
72 % y la inversión se recupera en menos de 3 años. En el pesimista, si los ciudadanos no adoptan la extensión, el proyecto pierde
94.000 dólares y no se recupera. Lo muestro porque es el riesgo real del
modelo: primero tiene que haber adopción gratuita y recién después ventas.

¿Cuánto hace falta y de dónde sale? Al inicio, 1.700 dólares, con fondos propios.
Hasta 53.000 dólares en los 2 primeros años, de inversores ángeles, en 2
tramos. El segundo tramo se pide solo si la adopción llega a la del escenario neutral; si
no, el proyecto se corta y la pérdida queda acotada al primero.

Lo que lo sostiene son 2 palancas de costo: el tope de 5 análisis por mes y la caché,
porque un tuit viral se analiza una vez y se sirve a todos. Y una advertencia: el precio de
la API es la variable que más pesa, y todavía no está validado con clientes.

## Lámina 7 · Limitaciones, trabajo futuro y cierre — 1:15

**🔒 DE MEMORIA — las limitaciones:**

> El sistema tiene límites que declaro. El puntaje mide cuánto respalda la evidencia a la
> afirmación, no si es verdadera, porque la verdad no admite grados: si una afirmación
> mezcla una parte verdadera con una falsa, es falsa, pero el promedio puede dejarla en el
> medio. Si la fuente oficial se equivoca, el sistema hereda el error. Y analiza una sola
> afirmación por tuit.

Hay 3 líneas de trabajo futuro. Primero, mentir con datos verdaderos: un dato real que
calla el contexto que lo contradice, o un contenido viejo que recircula como nuevo; lo
pidieron la periodista que entrevisté y la encuesta. Segundo, los gráficos engañosos, con
el eje recortado. Y tercero, que analice todas las afirmaciones de un tuit, no solo una:
así, si una de ellas es falsa, el tuit queda marcado como falso.

**🔒 DE MEMORIA — el cierre:**

> El objetivo no es que el usuario le crea al veredicto, sino que pueda prescindir de él.
> Por eso el sistema le entrega el camino hacia la evidencia, no solamente la conclusión.
> Gracias.

## Lámina 8 · Gracias — sin tiempo

Pasás a esta al decir «gracias» y la dejás durante todas las preguntas. Las láminas de
respaldo están después: demo grabada, C4 de contenedores y de componentes, despliegue,
capturas reales del análisis y de la señal de BETO, curva de valor completa,
modelos y matriz de confusión, pruebas, 3 escenarios con sensibilidad y mercado, precios
y horas del tesista. Se llega con → desde Gracias.

---

## Control de tiempo

El cronómetro del deck se activa con **T** y se pone rojo pasados los 10 minutos.

- A los **3:10** tenés que estar entrando en la demo (lámina 5).
- A los **6:45** tenés que estar saliendo de la demo, con la grabación incluida.
- Si vas atrasado, recortá en la 4 el párrafo del diagrama y cortá antes la grabación de la 5.
  **Nunca** recortes la escala, las limitaciones, el cierre ni el «cuánto y de dónde» del
  negocio: es lo que más preguntaron los profesores la semana pasada.

---

## La demo, paso a paso

Corre en local, no contra Railway. Si el wifi de UADE falla, el caso nuevo no corre
(necesita el LLM y la búsqueda web), pero los 2 casos en caché sí: pasá directo al
panel de evidencia de uno de ellos.

**Arranque** (desde `prototipo/`, con `OPENAI_API_KEY` en `servicio/.env`):

```bash
make dev        # construye la extensión y levanta BETO y el servicio
```

BETO local necesita los pesos en `PESOS_BETO` (por defecto
`~/Downloads/results/pesos/beto_fakedes-chequeado_s42`); confirmarlo el jueves.

Cargar `prototipo/extension/dist` en `chrome://extensions` con el modo de desarrollador.

**La caché es en memoria del proceso** (`servicio/app/cache.py`): se precalienta
analizando los 2 primeros casos **después** de arrancar el servicio y **no se reinicia**
hasta terminar la exposición.

**Los 3 casos.** Elegirlos el jueves, sobre tuits recientes y con la extensión ya
cargada:

1. **Falso, en caché.** Un tuit que el sistema marque *contradicho por fuentes oficiales*
   o *información sospechosa*, con una fuente oficial enlazada. Que sea un dato, no una
   opinión. Idealmente, uno de los falsos de las láminas 1b y 2b (empleados públicos frente
   a privados registrados): la demo muestra en vivo lo que la 2b anticipó. Probarlo antes:
   si el sistema no lo contradice con una fuente oficial, usar otro tuit.
2. **Verdadero, en caché.** Un dato oficial reciente, como el del INDEC sobre la inflación
   que figura en el capítulo 4 (*parece verificado*, 95).
3. **Nuevo, en vivo.** Un tuit con una cifra económica del día que nadie haya analizado.
   Tener anotado un segundo candidato por si el primero no extrae afirmación.

**Para mostrar en pantalla:**

- X en **tema claro** (Configuración → Accesibilidad, pantalla e idiomas → Pantalla).
- Cuentas reales **difuminadas** en la grabación de respaldo, como exige el apartado
  ético del documento. En vivo, preferir cuentas institucionales (INDEC, medios) a
  personas.
- Zoom del navegador al 125 % para que el detalle se lea desde el fondo.

**Si un profesor pide probar con otro caso** (a otro grupo le dictaron uno en vivo): buscá
en X, con la búsqueda de la propia red, una publicación reciente sobre el dato que
propone, y analizala. Si no hay afirmación verificable, el sistema lo dice: mostralo como
un resultado válido, no como una falla.

**Si algo falla en vivo:** «Les muestro la grabación» → volvés al deck, que quedó en la
lámina 5, *La demo, grabada*. La misma grabación sigue también en el respaldo, después de Gracias. No intentes arreglarlo frente
al tribunal.

---

## Los 3 videos — hasta el 10/11/2026

Los 3 salen del mismo deck y de la misma demo. Se graban con pantalla, voz y cámara
chica en una esquina (QuickTime: Nueva grabación de pantalla, con la cámara flotante de
Photo Booth o la superposición de cámara de macOS). Edición: solo cortar y unir.

| Video | Contenido | Láminas | Duración |
|---|---|---|---|
| 1 | Problema, competencia y arquitectura | 1 a 4 | ~3:45 |
| 2 | Demo corta y negocio | 5 y 6 | ~5:00 |
| 3 | Demo extendida y aclaraciones | demo, 7 y respaldo | ~5:00 |

**Video 3, guion corto:**

1. Demo extendida (2:00): los 3 casos, más el desglose «Cómo se llegó al resultado»
   con los 3 puntajes, el panel web con el histórico y una publicación sin
   evidencia que queda *sin contraste externo*.
2. *Ex falso* (1:00): el pasaje de memoria de las limitaciones, más un ejemplo concreto
   de afirmación compuesta.
3. «¿Quién verifica al verificador?» (1:00): la respuesta 7 de [PREGUNTAS](PREGUNTAS.md).
4. Trabajo futuro (1:00): las 3 ideas propias y el cierre de memoria.

---

## Lista previa a la exposición

- [ ] **Jueves:** elegir los 3 casos y grabar la demo de respaldo como
      `presentacion/img/demo-respaldo.mp4` (tema claro, cuentas difuminadas). Si no
      se llega, el deck reproduce el video de la defensa del 50 % (`img/demo.mp4`,
      2:37, grabado el 28/08): modo oscuro, cuentas sin difuminar y sin la señal del
      texto sobre cada publicación, que llegó después. Adelantarlo a mano.
- [ ] **Jueves:** ensayo completo cronometrado y grabado; tiene que terminar en
      10:00 ± 0:15.
- [ ] **Viernes:** correr `presentacion/chequear.sh factum.html` (chequeo del deck y PDF)
      y subir `presentacion/factum.pdf`.
- [ ] **Viernes:** revisar tildes en las láminas, lámina por lámina.
- [ ] **Sábado, antes de salir:** comprobar que x.com carga **con la extensión puesta**
      (paso cero de `prototipo/GUION-CAPTURAS.md`: una extensión de privacidad lo
      rompe).
- [ ] **Sábado, en el aula:** `make dev`, precalentar los 2 casos, abrir el deck con
      `presentacion/abrir.sh`, dejar X en otra ventana. No reiniciar el servicio.
- [ ] Laptop enchufada, notificaciones apagadas (No molestar), pestañas de `.env`
      cerradas.
- [ ] Adaptador HDMI propio. La semana pasada 2 grupos perdieron minutos con el
      proyector y con Teams; el deck y la demo corren sin internet salvo el caso nuevo.
- [ ] Hablar fuerte y sin apurarse: a un grupo le marcaron el volumen y a otro la
      velocidad.

---

## Mensaje a la cátedra sobre los videos

Borrador, para Fidel o para Nicolás. Las pautas no dicen cómo se entregan.

> Hola, Fidel. ¿Cómo estás? Te escribo por los 3 videos de 5 minutos de la
> Entrega Preliminar 3, con plazo hasta el 10/11. Las pautas no indican cómo se entregan:
> ¿se suben al campus, se comparte un enlace (YouTube no listado o Drive) o se envían por
> mail? ¿Hay algún formato o nombre de archivo que debamos respetar? La idea es que 2
> videos repliquen la exposición de 10 minutos y el tercero muestre la demo extendida y
> algunas aclaraciones. Gracias.
>
> Juan Martín Bejarano Arce — SA25

---

## Preguntas que pueden hacer

**¿Con qué corpus se entrenó BETO?** Con el *Spanish Fake News Corpus* (Posadas-Durán y
otros, 2019): 971 noticias de México y España, etiquetadas como verdaderas o falsas. Fue
la primera etapa del *fine-tuning*; la segunda, con 2.107 afirmaciones de Chequeado,
compensa que tenga poco español rioplatense. En el código figura como FakeDeS.

**¿Qué devuelve el clasificador?** Un número entre 0 y 1: la probabilidad de que el texto
tenga forma de desinformación, más una etiqueta. Lee solo el texto, no la cuenta ni las
fuentes, y detecta cómo está escrito: lenguaje de alarma, mayúsculas, «compartí antes de
que lo borren». No comprueba el dato. Por eso pesa 25 %: el estilo acompaña a la
desinformación, pero no la prueba, y castiga a quien cuenta una verdad indignado.

**¿Cómo se guardan los *embeddings*?** Con sqlite-vec, en el mismo archivo SQLite del
histórico: vectores de 384 dimensiones de un MiniLM multilingüe, con búsqueda por
similitud coseno. Sirven para 2 cosas: la memoria semántica (un tuit casi igual a uno ya
analizado reusa su evidencia si la similitud supera 0,95, las cifras coinciden y la
evidencia tiene menos de 7 días) y el índice de fuentes oficiales (se le pasan al LLM
los 3 fragmentos más parecidos).

**¿Qué son los 3 números del negocio?** El VAN de cada escenario, en dólares, a 5
años y con una tasa del 25 %. Neutral, 63.935, el que se defiende: se recupera en 2,9
años. Pesimista, −94.162: si los ciudadanos no adoptan la extensión, no hay datos que
venderles a los medios y no se recupera. Optimista, 833.353: es el límite superior del
modelo, no una meta.

**¿Qué es el VAN?** El valor actual neto: la plata que deja el proyecto, en dólares de
hoy, después de pagar la inversión y de exigirle un 25 % anual por el riesgo. Positivo,
conviene; negativo, no. En una frase: «es la ganancia del proyecto en plata de hoy,
después de exigirle un 25 % anual».

**¿Qué es la TIR?** La tasa interna de retorno: el rendimiento anual del proyecto. Se
compara con el 25 % exigido. En el neutral da 72 %. En el pesimista no está definida,
porque el flujo nunca se vuelve positivo, y en el optimista da miles por ciento, un número
sin sentido económico porque la inversión inicial es muy chica: ahí manda el VAN.

**¿Cómo se relacionan el VAN y la TIR?** Salen de la misma cuenta. El VAN fija la tasa
(25 %) y dice cuánta plata sobra; la TIR busca la tasa que deja el VAN en cero. No se
suman: uno es plata y el otro un porcentaje. Ejemplo chico: ponés 100 y al año sacás
150. La TIR es 50 %, lo que rindió. Si exigías 25 %, tendrías que haber sacado 125;
sobraron 25, que en plata de hoy son unos 20: ese es el VAN. Como 50 % supera a 25 %, el
VAN da positivo. En Factum: rinde 72 % por año, se le exige 25 %, y sobran 63.935
dólares.

---

## Láminas de respaldo: cómo explicar cada una

Están después de Gracias. Se llega con → desde Gracias, o abriendo `factum.html#N`.

**R1 · La demo, grabada.** La misma grabación de la lámina 5. Solo por si se pide de
nuevo durante las preguntas.

**R2 · C4 de contenedores.** «Es el diagrama del capítulo 4. La extensión de Chrome, en
TypeScript, le habla a una API en FastAPI. La API llama a un contenedor aparte con BETO y
el modelo de *embeddings*, al LLM de OpenAI con búsqueda web, y guarda todo en SQLite. El
panel web lo sirve la misma API.» Usala si preguntan por tecnologías o por la base de
datos, que no está en la lámina 4.

**R3 · C4 de componentes.** «Es el interior de la API: el orquestador recibe el pedido,
consulta la caché y la memoria semántica, llama a los 3 módulos y el combinador arma el
veredicto con su justificación.» Usala si preguntan cómo se organiza el código.

**R4 · Despliegue y zonas de red.** «El sistema se divide en 4 zonas, numeradas
según cuánto las controlo, y 3 de las 4 no dependen de mí. Por eso, si falla un
servicio externo, el sistema entrega un análisis parcial identificado como tal. Todo viaja
por HTTPS. Al clasificador solo le llega el texto, por la red privada de Railway; a
OpenAI, el texto sin la cuenta autora.» Usala si preguntan por seguridad, privacidad o qué
pasa si se cae OpenAI.

**R5 · El prototipo sobre X.** Capturas reales del capítulo 4. Usala si la demo en vivo
no se ve bien en el proyector o si piden ver el panel de evidencia con calma.

**R6 · Curva de valor completa.** «Es la curva del capítulo 2 con todas las variables.
Las marcadas con asterisco son capacidades que decidí no construir. Factum sube en
evidencia, contexto argentino y acceso gratuito, y no compite en lo que no hace.» Usala si
preguntan contra quién compite o por qué no hace algo que hace otra herramienta.

**R7 · Modelos y matriz de confusión.** «Comparé 5 modelos sobre el corpus académico.
BETO fue el mejor en prueba, con 0,76, pero en los tuits argentinos cae a 0,42. El sistema
completo llega a 0,712.» Y la matriz: «de las 46 verdaderas, ninguna salió como falsa; de
las 48 falsas, detecta 23 y deja pasar 25 como verdaderas. Prioricé no acusar a una
verdadera». Decí siempre la advertencia de abajo: Chequeado apareció como fuente en 78 de
los 94 análisis, así que el valor sobreestima el desempeño ante desinformación nueva, y el
77 % del corpus es anterior a 2022.

**R8 · Pruebas y requerimientos medidos.** «137 pruebas automatizadas en el servicio con
93 % de cobertura, 27 en la extensión, los 7 casos de uso aprobados. SUS de 74, sobre
una meta de 68, con 3 participantes: es un indicio, no una prueba. 2 metas no se
cumplen: la latencia, 16 segundos en el percentil 95 contra 8, porque la búsqueda web del
proveedor ya se lleva unos 7; y el F1 de 0,712 contra 0,75.» Usala si preguntan por
pruebas, latencia o resultados.

**R9 · Tres escenarios, sensibilidad y mercado.** Los 3 escenarios están explicados
arriba, en las preguntas. La sensibilidad: «lo que más mueve el VAN es el precio de la API
superior; si baja un 20 %, el VAN cae de 64.000 a 17.000. Por eso digo que el precio
todavía no está validado con clientes». La necesidad de financiamiento del neutral es de
unos 53.000 dólares, que coincide con lo que se pide a inversores ángeles.

**R10 · Precios y horas del tesista.** La tabla de precios por segmento. Si preguntan por
qué la inversión inicial es de solo 1.716 dólares: «mis horas del año 0 no se imputan
al flujo; a valor de mercado serían unos 24.000 dólares». Y si preguntan de dónde salen
los precios: «los contrasté con herramientas comparables, no con clientes».
