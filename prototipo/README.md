# Prototipo — rebanada vertical para la demostración del 50 %

Recorrido completo desde el DOM de X hasta un veredicto con fuentes enlazadas, con cada
módulo del *pipeline* reducido a su mínima expresión defendible en lugar de omitido.
Cubre el **criterio 7** de la rúbrica de EP2, que se expone el 29/08/2026.

El alcance, las decisiones y lo que queda deliberadamente afuera están en la *spec*:
[issue #18](https://github.com/martinnbejarano/PFI-Wiki/issues/18).

```
prototipo/
├── servicio/    ← FastAPI: un único punto de entrada de análisis
└── extension/   ← Chrome Manifest V3: content script, service worker y ventana emergente
```

No hay base de datos ni despliegue: todo corre local.

## El contrato de la respuesta de análisis

`prototipo/servicio/app/contrato.py` es la definición autoritativa. La extensión refleja
esos mismos nombres en `extension/src/compartido/contrato.ts`, y ambos lados tienen que
moverse juntos.

Es la pieza que sobrevive al cambio de modelo en la Entrega 4: el paso de clasificación se
reemplaza por el clasificador propio sin que la forma de la respuesta cambie. Ese paso vive
detrás del puerto único del proveedor (`servicio/app/proveedor/puerto.py`), así que
sustituirlo es escribir otro adaptador y cambiar la línea de `dependencias.py` que lo
construye.

`afirmacion` viene **vacía** cuando la publicación no contiene ninguna afirmación
verificable —una opinión, una pregunta, una broma, un saludo—. En ese caso el análisis se
corta antes del veredicto y se responde con el estado *sin contraste externo* y una
justificación que dice por qué no hay nada que verificar. No es un error ni un análisis
parcial: emitir un veredicto sobre una opinión sería el error más caro que esta
herramienta puede cometer.

| Campo | Requerimiento que realiza |
|---|---|
| `afirmacion`, `tipo_afirmacion` | RF-04 |
| `fuentes[]` con `tipo` y `postura` | RF-05 |
| `veredicto`, `justificacion`, `razones[]` | RF-06, RNF-06 |
| `analisis_parcial` | RNF-11 |
| `version_modelo`, `version_configuracion_pesos` | RF-16 |

## Cómo se levanta

### Servicio

```bash
cd prototipo/servicio
python3.13 -m venv .venv
./.venv/bin/pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env      # y completar OPENAI_API_KEY
./.venv/bin/uvicorn app.main:aplicacion --reload --port 8000
```

Comprobación sin la extensión:

```bash
curl -sS http://127.0.0.1:8000/salud
curl -sS -X POST http://127.0.0.1:8000/analizar \
  -H 'Content-Type: application/json' \
  -d '{"tweet_id":"1234567890123456789","texto":"A partir del lunes cierran 50 escuelas.","handle":"@ejemplo"}'
```

**Sin credencial, `/analizar` devuelve `200` con un análisis parcial** que lista los tres
módulos que no pudieron ejecutarse, y eso es deliberado por partida doble: el servicio
arranca igual y `GET /salud` responde, de modo que la batería de pruebas corra sin red y
sin clave; y una falla del proveedor nunca sale como error opaco, que es lo que exige
RNF-11. Es también la forma más simple de provocar el estado parcial para una captura;
ver «Cómo se provoca cada estado a mano».

Pruebas del servicio:

```bash
env -u OPENAI_API_KEY ./.venv/bin/python -m pytest -q
```

La documentación interactiva que FastAPI deriva del tipado queda en
<http://localhost:8000/docs>.

#### Prueba manual de la búsqueda de evidencia — pendiente

Exige la credencial y una llamada verdadera, así que **no está corrida**: no hay
ni un número ni una fuente anotados de antemano en ninguna parte de este
repositorio. Con `OPENAI_API_KEY` ya en `prototipo/servicio/.env`:

```bash
cd prototipo/servicio
./.venv/bin/uvicorn app.main:aplicacion --port 8000 --log-level info

curl -sS -X POST http://127.0.0.1:8000/analizar \
  -H 'Content-Type: application/json' \
  -d '{"tweet_id":"1","texto":"🚨 La inflación de julio fue del 15%, el peor dato en años. COMPARTAN antes de que lo bajen 🚨","handle":"@ejemplo"}' \
  | python3 -m json.tool
```

Qué mirar en el resultado:

- `fuentes` trae fuentes **reales y pertinentes** al dato económico, y toda URL
  cae dentro de los dominios de `app/jerarquia.py`.
- Cada fuente abre el documento original si se la pega en el navegador.
- La **postura** de cada fuente se corresponde con lo que el documento dice sobre
  la afirmación. Es lo más frágil del paso: la postura se determina con lo que la
  herramienta de búsqueda trajo de cada resultado, y por eso
  `contexto_de_busqueda` subió de `low` a `medium` al implementarla. Una postura
  sistemáticamente mal puesta se corrige volviendo a `low` y declarando todas las
  fuentes neutrales, no dejándola como está.
- La **latencia del paso de evidencia**, que es donde ese cambio se paga. El
  presupuesto de RNF-02 son ocho segundos en el percentil 95 y este repositorio
  no tiene ni un número de latencia ni uno de costo que no venga de una
  medición.
- Las líneas `proveedor` del registro traen la latencia, las fichas y el costo
  de cada uno de los tres pasos; las líneas `evidencia` dicen qué resultados
  descartó el filtro propio por caer fuera de la jerarquía, que es la forma de
  ver cuánto se le escapa al filtro del proveedor.

### Extensión

```bash
cd prototipo/extension
npm install
npm run build
```

Pruebas de la extensión:

```bash
npm test
```

Después, en Chrome: `chrome://extensions` → activar **Modo de desarrollador** → **Cargar
descomprimida** → elegir `prototipo/extension/dist`.

Con el servicio andando, abrir <https://x.com/home>. Sobre cada tuit aparece el indicador;
al hacer clic pasa al estado transitorio y luego al veredicto que devuelve el servicio.

Cada cambio en `src/` exige volver a correr `npm run build` y recargar la extensión desde
`chrome://extensions`.

## Notas de construcción

**Son dos pasos de Vite y no uno.** Chrome ejecuta los guiones declarados en
`content_scripts` como guiones clásicos, así que el *content script* se construye aparte
como un único archivo IIFE (`vite.config.content.ts`), mientras que el *service worker* —que
sí es un módulo— sale de la construcción principal. Los nombres de salida no llevan huella
porque el manifiesto los referencia literalmente y se mantiene a mano, sin complemento de
Vite para extensiones, tal como decidió `wiki/solucion/tecnologias.md`.

**La interfaz hereda el marcado de los *mockups*.** El HTML y el CSS de
`extension/src/content/indicador.ts` se portan de la pantalla `?pantalla=badge` de
`wiki/assets/mockups/mockups.html`, y los de `extension/src/content/detalle.ts` de la
pantalla `?pantalla=popup` de la misma página, que es lo que esa página ya anticipaba.
Los nombres de clase son los del *mockup*, de modo que la correspondencia con las
figuras impresas en el documento se pueda verificar leyendo. Todo vive dentro de un
*shadow DOM*, de modo que ninguna regla de X entre y ninguna regla propia salga.

**La jerarquía de evidencia vive en un módulo propio.** `servicio/app/jerarquia.py`
declara los tres escalones —fuentes oficiales, medios de referencia,
verificaciones previas— con sus dominios, y trae el filtro que los hace valer.
Ese módulo es también donde quedó anotada **la verificación de la restricción de
dominios del proveedor de búsqueda**, que la *spec* dejó marcada como pendiente:
qué se consultó, cuándo, qué límites tiene el filtro y por qué el filtro propio
se aplica igual. La lista de dominios está ahí y no dentro del adaptador porque
la va a tocar la Entrega 4.

La restricción se aplica en dos capas: el adaptador le declara al proveedor el
filtro de dominios de su herramienta de búsqueda, y el orquestador vuelve a
filtrar sobre las URLs que efectivamente volvieron. No es redundancia: la
primera capa es una caja negra del proveedor y la segunda es código propio,
observable y probado. Es esta última la que los tests ejercitan, haciendo que el
doble devuelva URLs de fuera de la jerarquía y comprobando que no aparecen en la
respuesta HTTP.

**El veredicto sale del combinador y no de una llamada suelta.**
`servicio/app/combinador.py` es el Módulo 4: agrega la postura de las fuentes en
el puntaje de contraste pesándolas según la jerarquía de evidencia, pondera los
tres puntajes parciales en el puntaje final y lo traduce en uno de los tres
niveles de RF-06. El paso que habla con el proveedor va **después** y recibe el
nivel ya decidido: redacta la justificación que lo explica en lugar de
producirlo, que es lo que evita que la respuesta muestre un nivel y un texto que
dicen cosas distintas.

Las dos fórmulas están escritas en ese archivo, con sus casos y con lo que son:
heurísticas de prototipo —un promedio ponderado y dos cortes—, elegidas porque
se explican en una oración y se pueden mover en vivo. No salen de un ajuste
sobre datos etiquetados y el archivo lo dice así.

Dos invariantes del servicio se hacen valer sobre lo que el combinador produce,
en `pipeline.py` y no en la fórmula, de modo que ningún cambio de pesos pueda
alcanzarlas:

- **Sin ninguna fuente admisible el veredicto es *sin contraste externo***,
  cualquiera sea el puntaje (RNF-06).
- **El nivel severo exige una fuente oficial que contradiga.** El nombre del
  nivel dice quién sostiene el juicio; emitirlo sin esa fuente sería atribuirle a
  un organismo algo que no dijo (RNF-07). Cuando el puntaje llega pero la
  contradicción viene de un medio o de un verificador, el veredicto se rebaja a
  *información sospechosa*.

**Los pesos y los umbrales viven en configuración (RNF-16).** Los ocho números
que el combinador usa están declarados en `servicio/app/configuracion.py` y
listados comentados en `servicio/.env.example`. Cambiarlos es escribir una línea
y reiniciar el proceso: no hay que tocar código ni volver a desplegar nada.

```bash
cd prototipo/servicio
PESO_CONTRASTE=0.9 ./.venv/bin/uvicorn app.main:aplicacion --port 8000
```

Es también lo que hace defendible la demostración en vivo: se analiza un tuit, se
levanta el servicio con otro peso, se vuelve a analizar el mismo tuit y se ve
moverse el puntaje final —y, si cruza un umbral, el veredicto—. La batería de
pruebas comprueba lo mismo por el contrato HTTP, sustituyendo la configuración
por dependencia igual que se sustituye el proveedor.

**La versión de la configuración de pesos se calcula, no se escribe.**
`version_configuracion_pesos` viaja en cada respuesta por RF-16 y tiene la forma
`pesos-v1+9e2fd1cb`: una etiqueta que una persona elige más la huella SHA-256 de
los ocho valores en uso. Una cadena fija cumpliría la letra del requerimiento y
no su intención —alguien cambia un peso, se olvida de subir la etiqueta, y dos
análisis distintos quedan asociados a la misma versión—. Derivada de los
valores, no puede quedar desactualizada. La huella identifica; reconstruir los
pesos a partir de ella es tarea de la persistencia que RF-16 pide y que este
prototipo declaró fuera de alcance.

**El panel de evidencia se abre desde el pie del detalle.** El marcado y el CSS
de `extension/src/content/evidencia.ts` se portan de la pantalla
`?pantalla=evidencia` de `wiki/assets/mockups/mockups.html`, la tercera de las
cuatro. Muestra arriba la afirmación verificable extraída con su tipo, y debajo
las fuentes agrupadas y ordenadas según la jerarquía, cada una etiquetada por su
postura —corrobora, contradice o neutral— y con el enlace al documento
original. Es el diferencial del proyecto: no un veredicto, sino el
camino para no depender del veredicto. No se dibujan la cita textual ni la
antigüedad que la figura muestra en cada fila, porque el contrato no las trae e
inventarlas sería fabricar la evidencia que la pantalla existe para mostrar.

**El detalle se abre desde el indicador**, no desde la ventana emergente de la barra de
herramientas: el botón del indicador pide el análisis mientras no hay uno y, una vez
resuelto, despliega y repliega el detalle sobre la propia *timeline*. Muestra la
afirmación verificable extraída con su tipo, la justificación, el desglose de los tres
puntajes parciales con su barra y las razones enlazadas a sus fuentes.

**El módulo de credibilidad de la cuenta aparece marcado como no implementado.**
`servicio/app/credibilidad.py` devuelve un valor arbitrario derivado de un resumen
determinista del *handle*: el mismo tuit muestra siempre el mismo número entre recargas,
que es lo que evita que un valor parpadee durante la exposición. No es una medición y la
interfaz no lo presenta como tal —barra rayada, etiqueta *sin dato* y una nota que dice
qué es—. Deliberadamente no usa `verificada` ni las métricas de propagación, aunque el
lector del DOM ya las lea: una medición a medias sería peor que un valor declaradamente
inventado.

Por lo mismo **pesa cero en el combinador**. Ponderar con cualquier peso mayor que
cero un número derivado de una semilla del *handle* metería ese invento dentro
del puntaje final, que es la cifra que la interfaz muestra como probabilidad
estimada de desinformación. El peso existe como campo de configuración y no está
borrado del combinador: el día que el Módulo 2 mida de verdad, lo único que hay
que cambiar es ese valor. El puntaje entra invertido —más credibilidad, menos
sospecha—, y eso ya está escrito aunque hoy no cambie ningún resultado.

**La lectura del DOM es defensiva.** X no versiona su marcado. Los selectores se apoyan en
los atributos de prueba y un campo que falta saltea el tuit en lugar de romper la
extensión.

**Ninguna falla sale como error (RNF-11).** El servicio no tiene camino de error para las
fallas del proveedor: si un paso no se puede ejecutar, lo que sale sigue siendo un `200`
con la respuesta del contrato, marcada como análisis parcial y con la lista de los módulos
ausentes escrita en palabras que una persona puede leer. Los tres pasos no se degradan
igual, y el porqué de cada decisión está escrito en `servicio/app/pipeline.py`:

| Paso | ¿Sigue el análisis? | Qué queda |
|---|---|---|
| Extracción de la afirmación (RF-04) | **No.** Sin afirmación no hay qué buscar ni sobre qué pronunciarse | Respuesta completa con la afirmación vacía, sin puntaje calculado sobre nada y los tres módulos listados como ausentes |
| Contraste con evidencia (RF-05) | **Sí**, sin contraste | La invariante de RNF-06 hace caer el veredicto en *sin contraste externo* cualquiera sea el puntaje, así que el resultado no se construye sobre el módulo faltante |
| Redacción de la justificación (RF-06) | **Sí** | El veredicto, los puntajes y las fuentes salen del combinador, que es código propio; lo único que se pierde es el texto que los explica |

Detenerse no es devolver un error: en los tres casos la interfaz recibe algo que puede
dibujar entero. La extensión lo señala con el flujo alternativo *6a* que el propio
*mockup* publica —tapa gris que dice «Análisis parcial», guión en lugar del porcentaje,
el aviso que explica qué pasó y la barra rayada con la etiqueta *sin dato* en el módulo
que faltó—, que es el mismo patrón que el módulo de credibilidad ya usaba.

**El indicador nunca queda girando.** Además del tiempo límite que el *service worker*
aplica sobre la petición HTTP, el *content script* corre su propio seguro
(`extension/src/content/tiempo-limite.ts`), más holgado. Cubre el único modo de falla que
el otro no puede cubrir: que el *service worker* de Manifest V3 sea terminado por el
navegador entre el pedido y la respuesta y la promesa quede pendiente para siempre. Un
componente no se puede vigilar a sí mismo cuando el modo de falla es que deje de existir.

**Un tuit ya analizado se resuelve sin volver a llamar al proveedor (RF-07).** La caché
vive en `servicio/app/cache.py`, **en memoria del proceso**: no hay base de datos, así que
**se pierde al reiniciar el servicio**. La clave no es solo el identificador nativo del
tuit sino la terna identificador + versión del modelo + versión de la configuración de
pesos. Sin las versiones, alguien cambia un peso, reinicia, y el mismo tuit sigue
devolviendo el análisis viejo: la demostración en vivo de RNF-16 —mover un peso y ver
moverse el resultado— parecería rota sin estarlo.

**Un análisis parcial no se guarda**, y es la decisión de fondo de ese módulo. Un parcial
es el resultado de una falla, y las fallas de red son casi siempre transitorias:
guardarlo convertiría un corte de tres segundos en un resultado permanente hasta reiniciar
el proceso, y la única salida visible sería reiniciar el servicio delante del tribunal. Se
paga con una llamada fallida por clic mientras el proveedor esté caído —que no consume
fichas— a cambio de que reintentar signifique reintentar. No es el mismo caso que la
publicación sin afirmación verificable: ese análisis **sí** se guarda, porque no es una
falla y volver a pedirlo daría lo mismo.

## Cómo se provoca cada estado a mano

Para las capturas de la demostración. Todo se hace con la configuración que ya existe: no
hay ninguna bandera de prueba escondida en el código, y esa es la idea.

**Análisis parcial con los tres módulos ausentes.** Levantar el servicio sin la credencial:

```bash
cd prototipo/servicio
env -u OPENAI_API_KEY ./.venv/bin/uvicorn app.main:aplicacion --port 8000
```

Cualquier clic en el indicador devuelve `200` con `analisis_parcial.es_parcial` en
verdadero y los tres módulos listados. En la extensión se ve la tapa gris, el guión en
lugar del porcentaje y el aviso.

**Análisis parcial con solo el contraste ausente** —el caso interesante, porque el
análisis del texto sobrevive—. Exige la credencial. Se estrecha el tope de fichas del paso
de búsqueda hasta que la llamada se corte antes de ajustarse al esquema:

```bash
cd prototipo/servicio
MAX_FICHAS_DE_SALIDA_BUSQUEDA=16 ./.venv/bin/uvicorn app.main:aplicacion --port 8000
```

La extracción y la redacción funcionan; la búsqueda falla y el módulo ausente es uno solo.
El detalle muestra la barra de «Contraste con fuentes» rayada y con *sin dato*, y la de
«Análisis del texto» con su cifra. El caso de la redacción ausente no tiene una palanca de
configuración equivalente —el tope general afectaría antes a la extracción, que va
primero— y queda cubierto por la batería de pruebas.

**Estado *sin contraste externo* sin que haya ninguna falla.** Analizar una afirmación
verificable cuya evidencia caiga fuera de los trece dominios de `app/jerarquia.py` —algo
extranjero, deportivo o de espectáculos—: el filtro propio descarta todo lo que vuelve,
`fuentes` queda vacía y el veredicto se emite en ese estado, sin porcentaje y sin marca de
parcial. Una publicación sin ninguna afirmación verificable —una opinión, un saludo—
produce el mismo estado por el otro camino, con el bloque de la afirmación vacío.

**Los estados del indicador.**

| Estado | Cómo se provoca |
|---|---|
| Inicial | Abrir <https://x.com/home> con la extensión cargada; aparece sobre cada tuit sin hacer nada |
| Transitorio | Hacer clic y capturar durante los segundos que tarda la llamada real. Se lo puede alargar con `ESFUERZO_DE_RAZONAMIENTO=high` |
| Los tres niveles y *sin contraste externo* | Clic sobre tuits con afirmaciones de distinto tenor; para forzar un nivel concreto sin depender de lo que traiga la búsqueda, mover `UMBRAL_CONTRADICHO_POR_FUENTES_OFICIALES` o `UMBRAL_INFORMACION_SOSPECHOSA` |
| Parcial | Cualquiera de las dos palancas de arriba |
| Falla de la extensión | No levantar el servicio: el indicador queda en «No se pudo analizar… Tocá para reintentar», nunca en el estado transitorio |

## Credenciales

El proveedor es **OpenAI**, alcanzado por su API de respuestas con salida estructurada.
El modelo concreto queda fijado en `servicio/app/configuracion.py` junto con su tabla de
precios, de modo que cada llamada registre latencia, fichas y costo medidos.

La clave vive **únicamente** en el entorno del servicio, en `prototipo/servicio/.env`
—copiado de `.env.example`—, que está fuera del control de versiones. La extensión nunca la
ve: el *service worker* habla solo con `http://localhost:8000`, declarado en los permisos
de anfitrión del manifiesto.

## Versión de Python

El prototipo corre sobre la versión instalada en la máquina de desarrollo, **3.13.3**.
`wiki/solucion/tecnologias.md` declara 3.14.7. La diferencia se declara y no se resuelve
instalando otra: el argumento de esa página —evitar comprometerse con una versión que
llega a fin de vida durante el PFI— sigue en pie para el sistema, y el prototipo no es el
lugar para gastar tiempo de calendario en alinearlo.
