# Guion de la exposición — Entrega 90 %

Sábado 31/10/2026, 10:40, grupo SA25. **10:00 en total**, demo en vivo incluida.

Texto para decir tal cual. Los pasajes marcados con **🔒 DE MEMORIA** se dicen palabra
por palabra, sin mirar: son los tres que se perdieron en el 50 % (la escala, las
limitaciones y el cierre).

Todas las cifras salen del documento entregado (capítulos 3 y 4 y conclusiones). Si una
cifra del wiki no coincide, manda el documento.

| # | Lámina | Tiempo | Acumulado |
|---|---|---|---|
| 1 | Portada | 0:15 | 0:15 |
| 2 | Problema y encuesta | 1:15 | 1:30 |
| 3 | Competencia y diferencial | 0:45 | 2:15 |
| 4 | Arquitectura | 1:00 | 3:15 |
| 5 | Resultados de ML | 1:45 | 5:00 |
| 6 | Demo en vivo | 1:45 | 6:45 |
| 7 | Negocio | 2:00 | 8:45 |
| 8 | Limitaciones, trabajo futuro y cierre | 1:15 | 10:00 |
| 9 | Gracias | — | preguntas |

---

## Lámina 1 · Portada — 0:15

Buenos días. Soy Juan Martín Bejarano Arce, de Ingeniería en Informática, y mi tutor es
Fidel Giro Uribazo. Presento el avance del noventa por ciento de mi proyecto: un sistema
de detección automática de desinformación en X.

## Lámina 2 · Problema y encuesta — 1:15

El problema es de escala. En la Argentina hay treinta y un millones de usuarios de redes
sociales, y solo tres de cada diez confían en los medios. Y en X, una afirmación verdadera
tarda unas seis veces más que una falsa en llegar a mil quinientas personas.

La verificación profesional es rigurosa, pero revisa de a una afirmación y casi siempre
después de que circuló. No le falta rigor: le falta escala.

Para validarlo hice una encuesta propia, con ciento dieciséis respuestas del segmento. El
hallazgo que ordenó el producto es este: en una escala de uno a cinco, las ganas de usar la
herramienta dieron cuatro coma cero nueve, y la confianza en un puntaje automático, tres
coma cincuenta y ocho.

Quieren la herramienta, pero no le creen del todo al número. Por eso construí Factum: una
extensión de Chrome que pone sobre cada publicación de X un veredicto con sus fuentes. No
entrega un número solo: entrega el número y el camino para comprobarlo.

## Lámina 3 · Competencia y diferencial — 0:45

La pregunta obvia es si esto ya existe. Arriba es más.

Hay dos diferenciales. El primero es el camino a la evidencia: cada veredicto enlaza el
documento de origen, el INDEC o el Boletín Oficial, y no una nota de otro medio. El
segundo es el alcance: las Notas de la Comunidad llegan cuando hay consenso, horas
después y a una fracción de las publicaciones. Este sistema llega a todas las que el
usuario tiene en pantalla, con fuentes argentinas.

La solución más parecida es InTruth, una extensión gratuita de este año, pero verifica el
audio de debates contra la web abierta, no el texto de X.

## Lámina 4 · Arquitectura — 1:00

Técnicamente son cuatro módulos que terminan en un veredicto.

El primero es un clasificador BETO, un modelo de lenguaje en español que ajusté en dos
etapas: primero con un corpus académico de noticias y después con afirmaciones de
Chequeado. Pesa un cuarto del resultado. El segundo mira señales públicas de la cuenta:
antigüedad, seguidores y verificación. Pesa un diez por ciento, porque esas señales se
compran. El tercero contrasta la afirmación con fuentes oficiales, con los medios de ADEPA
y con verificadores, y pesa sesenta y cinco por ciento. El cuarto combina los tres.

Abajo, cómo se despliega: la extensión le pide el análisis a una API, la API consulta al
clasificador y a un LLM con búsqueda web restringida a las fuentes de la jerarquía, y una
ingesta programada mantiene al día el índice de fuentes oficiales. Todo corre en la nube
por unos trece dólares por mes.

*(Las tecnologías, TypeScript, FastAPI, SQLite, Railway, no se nombran: están en el
respaldo, en el C4 de contenedores, por si preguntan.)*

## Lámina 5 · Resultados de ML — 1:45

Los resultados, en F1 macro, que va de cero a uno: más alto es mejor.

BETO sacó cero coma setenta y seis sobre el corpus académico de prueba, en el rango de
los mejores resultados publicados. Pero sobre noventa y cuatro tuits argentinos ya
verificados cayó a cero coma cuarenta y dos: prácticamente azar. Es desplazamiento de
dominio. Se entrenó con noticias largas y se evaluó con publicaciones de dos líneas, en
otro registro.

Eso confirmó la hipótesis de la arquitectura: el modelo solo no alcanza. El sistema
completo, con el contraste de fuentes, llega a cero coma setenta y uno. Aun después de
adaptar BETO con afirmaciones de Chequeado, el clasificador solo llegaba a cero coma
cincuenta y dos: el contraste suma diecinueve puntos. Y en la clase *falso* tiene una precisión de uno: ninguna
publicación verdadera fue señalada como falsa. Prioricé ese error porque es el que más
daño reputacional y legal causa.

La meta era cero coma setenta y cinco, y no se alcanzó. El intervalo de confianza va de
cero coma sesenta y uno a cero coma ochenta, así que con noventa y cuatro casos no se
puede afirmar ni descartar. La latencia tampoco cumple: el análisis profundo demora
dieciséis segundos en el percentil noventa y cinco, contra una meta de ocho.

Lo validé además con ciento treinta y siete pruebas automatizadas en el servicio, con
noventa y tres por ciento de cobertura, veintisiete en la extensión, y una prueba de
usabilidad con un SUS de setenta y cuatro.

## Lámina 6 · Demo en vivo — 1:45

**🔒 DE MEMORIA — la escala, antes de cualquier número:**

> La cifra que van a ver son las chances de que la afirmación sea verdadera, de cero a
> cien. Más alto es mejor. Por encima de treinta y cuatro, parece verificado; de treinta
> para abajo, contradicho por fuentes oficiales; en el medio, información sospechosa.

*(Cambiás a la ventana de Chrome con X abierto. Ver «La demo, paso a paso».)*

Sobre cada publicación la extensión muestra una señal del texto, que no es un veredicto.
El veredicto aparece al pedir el análisis.

Este es un caso falso que ya analicé: resuelve al instante porque está en la caché.
Contradicho por fuentes oficiales, y acá dice cuál. Este otro es verdadero: parece
verificado, con la página del INDEC enlazada.

Ahora uno nuevo, en vivo. Mientras corre: este es el análisis profundo, el que tarda entre
ocho y dieciséis segundos.

*(Al llegar el resultado, abrís el panel de evidencia.)* Cada fuente abre el documento
original. Y acá abajo, «Cómo se analiza»: contra qué fuentes se contrasta, con el enlace
al padrón de ADEPA. Los medios no los elijo yo.

## Lámina 7 · Negocio — 2:00

El modelo tiene dos lados. El ciudadano no paga: la extensión es gratis, con cinco
análisis nuevos por mes. Pagan las organizaciones. El cliente ideal es un medio o un
verificador que quiere chequear en volumen: la API arranca en doscientos dólares por mes
con cinco mil consultas. Los observatorios pagan trescientos por el panel de tendencias. Y
ese precio no es arbitrario: la cuota de cada nivel está calculada para que el margen siga
positivo aunque el cliente la use entera, y lo comparé con herramientas parecidas.

Lo evalué a cinco años, con impuestos y cargas sociales, a una tasa del veinticinco por
ciento, en tres escenarios. En el neutral, el más probable, el VAN es de sesenta y cuatro
mil dólares, la TIR del setenta y dos por ciento y la inversión se recupera en menos de
tres años. En el pesimista, si los ciudadanos no adoptan la extensión, el proyecto pierde
noventa y cuatro mil dólares y no se recupera. Lo muestro porque es el riesgo real del
modelo: primero tiene que haber adopción gratuita y recién después ventas.

¿Cuánto hace falta y de dónde sale? Al inicio, mil setecientos dólares, con fondos propios.
Hasta cincuenta y tres mil dólares en los dos primeros años, de inversores ángeles, en dos
tramos. El segundo tramo se pide solo si la adopción llega a la del escenario neutral; si
no, el proyecto se corta y la pérdida queda acotada al primero.

Lo que lo sostiene son dos palancas de costo: el tope de cinco análisis por mes y la caché,
porque un tuit viral se analiza una vez y se sirve a todos. Y una advertencia: el precio de
la API es la variable que más pesa, y todavía no está validado con clientes.

## Lámina 8 · Limitaciones, trabajo futuro y cierre — 1:15

**🔒 DE MEMORIA — las limitaciones:**

> El sistema tiene límites que declaro. El puntaje mide cuánto respalda la evidencia a la
> afirmación, no si es verdadera, porque la verdad no admite grados: si una afirmación
> mezcla una parte verdadera con una falsa, es falsa, pero el promedio puede dejarla en el
> medio. Si la fuente oficial se equivoca, el sistema hereda el error. Y analiza una sola
> afirmación por tuit.

Hay tres líneas de trabajo futuro. Primero, mentir con datos verdaderos: un dato real que
calla el contexto que lo contradice, o un contenido viejo que recircula como nuevo; lo
pidieron la periodista que entrevisté y la encuesta. Segundo, los gráficos engañosos, con
el eje recortado. Y tercero, partir la afirmación en predicados lógicos y verificar cada
uno: así una conjunción con una parte falsa queda falsa, y un dato oficial erróneo
contamina solo su predicado.

**🔒 DE MEMORIA — el cierre:**

> El objetivo no es que el usuario le crea al veredicto, sino que pueda prescindir de él.
> Por eso el sistema le entrega el camino hacia la evidencia, no solamente la conclusión.
> Gracias.

## Lámina 9 · Gracias — sin tiempo

Pasás a esta al decir «gracias» y la dejás durante todas las preguntas. Las láminas de
respaldo están después: demo grabada, C4 de contenedores y de componentes, despliegue,
capturas reales del análisis y de la señal de BETO, curva de valor completa,
modelos y matriz de confusión, pruebas, tres escenarios con sensibilidad y mercado, precios
y horas del tesista. Se llega con → desde Gracias.

---

## Control de tiempo

El cronómetro del deck se activa con **T** y se pone rojo pasados los diez minutos.

- A los **3:15** tenés que estar entrando en Resultados (lámina 5).
- A los **6:45** tenés que estar saliendo de la demo.
- Si vas atrasado, recortá en la 4 el párrafo del diagrama y en la 5 la línea de pruebas.
  **Nunca** recortes la escala, las limitaciones, el cierre ni el «cuánto y de dónde» del
  negocio: es lo que más preguntaron los profesores la semana pasada.

---

## La demo, paso a paso

Corre en local, no contra Railway. Si el wifi de UADE falla, el caso nuevo no corre
(necesita el LLM y la búsqueda web), pero los dos casos en caché sí: pasá directo al
panel de evidencia de uno de ellos.

**Arranque** (desde `prototipo/`, con `OPENAI_API_KEY` en `servicio/.env`):

```bash
make dev        # construye la extensión y levanta BETO y el servicio
```

BETO local necesita los pesos en `PESOS_BETO` (por defecto
`~/Downloads/results/pesos/beto_fakedes-chequeado_s42`); confirmarlo el jueves.

Cargar `prototipo/extension/dist` en `chrome://extensions` con el modo de desarrollador.

**La caché es en memoria del proceso** (`servicio/app/cache.py`): se precalienta
analizando los dos primeros casos **después** de arrancar el servicio y **no se reinicia**
hasta terminar la exposición.

**Los tres casos.** Elegirlos el jueves, sobre tuits recientes y con la extensión ya
cargada:

1. **Falso, en caché.** Un tuit que el sistema marque *contradicho por fuentes oficiales*
   o *información sospechosa*, con una fuente oficial enlazada. Que sea un dato, no una
   opinión.
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

**Si algo falla en vivo:** «Les muestro la grabación» → → hasta la lámina de respaldo
*La demo, grabada* (la décima, primera después de Gracias). No intentes arreglarlo frente
al tribunal.

---

## Los tres videos — hasta el 10/11/2026

Los tres salen del mismo deck y de la misma demo. Se graban con pantalla, voz y cámara
chica en una esquina (QuickTime: Nueva grabación de pantalla, con la cámara flotante de
Photo Booth o la superposición de cámara de macOS). Edición: solo cortar y unir.

| Video | Contenido | Láminas | Duración |
|---|---|---|---|
| 1 | Problema, competencia y arquitectura | 1 a 4 | ~3:45 |
| 2 | Resultados, demo corta y negocio | 5 a 7 | ~5:00 |
| 3 | Demo extendida y aclaraciones | demo, 8 y respaldo | ~5:00 |

**Video 3, guion corto:**

1. Demo extendida (2:00): los tres casos, más el desglose «Cómo se llegó al resultado»
   con los tres puntajes, el panel web con el histórico y una publicación sin
   evidencia que queda *sin contraste externo*.
2. *Ex falso* (1:00): el pasaje de memoria de las limitaciones, más un ejemplo concreto
   de afirmación compuesta.
3. «¿Quién verifica al verificador?» (1:00): la respuesta 7 de [PREGUNTAS](PREGUNTAS.md).
4. Trabajo futuro (1:00): las tres ideas propias y el cierre de memoria.

---

## Lista previa a la exposición

- [ ] **Jueves:** elegir los tres casos y grabar la demo de respaldo como
      `presentacion/img/demo-respaldo.mp4` (tema claro, cuentas difuminadas).
- [ ] **Jueves:** ensayo completo cronometrado y grabado; tiene que terminar en
      10:00 ± 0:15.
- [ ] **Viernes:** correr `presentacion/chequear.sh` (chequeo del deck y PDF) y subir
      `presentacion/PRESENTACION.pdf`.
- [ ] **Viernes:** revisar tildes en las láminas, lámina por lámina.
- [ ] **Sábado, antes de salir:** comprobar que x.com carga **con la extensión puesta**
      (paso cero de `prototipo/GUION-CAPTURAS.md`: una extensión de privacidad lo
      rompe).
- [ ] **Sábado, en el aula:** `make dev`, precalentar los dos casos, abrir el deck con
      `presentacion/abrir.sh`, dejar X en otra ventana. No reiniciar el servicio.
- [ ] Laptop enchufada, notificaciones apagadas (No molestar), pestañas de `.env`
      cerradas.
- [ ] Adaptador HDMI propio. La semana pasada dos grupos perdieron minutos con el
      proyector y con Teams; el deck y la demo corren sin internet salvo el caso nuevo.
- [ ] Hablar fuerte y sin apurarse: a un grupo le marcaron el volumen y a otro la
      velocidad.

---

## Mensaje a la cátedra sobre los videos

Borrador, para Fidel o para Nicolás. Las pautas no dicen cómo se entregan.

> Hola, Fidel. ¿Cómo estás? Te escribo por los tres videos de cinco minutos de la
> Entrega Preliminar 3, con plazo hasta el 10/11. Las pautas no indican cómo se entregan:
> ¿se suben al campus, se comparte un enlace (YouTube no listado o Drive) o se envían por
> mail? ¿Hay algún formato o nombre de archivo que debamos respetar? La idea es que dos
> videos repliquen la exposición de diez minutos y el tercero muestre la demo extendida y
> algunas aclaraciones. Gracias.
>
> Juan Martín Bejarano Arce — SA25
