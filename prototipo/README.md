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

**Sin credencial, `/analizar` devuelve `503` con un mensaje explícito**, y eso es
deliberado: el servicio arranca igual y `GET /salud` responde. Solo falla la llamada
verdadera al proveedor, de modo que la batería de pruebas corra sin red y sin clave.

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
la van a tocar el ticket #24 y la Entrega 4.

La restricción se aplica en dos capas: el adaptador le declara al proveedor el
filtro de dominios de su herramienta de búsqueda, y el orquestador vuelve a
filtrar sobre las URLs que efectivamente volvieron. No es redundancia: la
primera capa es una caja negra del proveedor y la segunda es código propio,
observable y probado. Es esta última la que los tests ejercitan, haciendo que el
doble devuelva URLs de fuera de la jerarquía y comprobando que no aparecen en la
respuesta HTTP.

**El panel de evidencia se abre desde el pie del detalle.** El marcado y el CSS
de `extension/src/content/evidencia.ts` se portan de la pantalla
`?pantalla=evidencia` de `wiki/assets/mockups/mockups.html`, la tercera de las
cuatro. Muestra arriba la afirmación verificable extraída con su tipo, y debajo
las fuentes agrupadas y ordenadas según la jerarquía, cada una con el enlace al
documento original. Es el diferencial del proyecto: no un veredicto, sino el
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

**La lectura del DOM es defensiva.** X no versiona su marcado. Los selectores se apoyan en
los atributos de prueba y un campo que falta saltea el tuit en lugar de romper la
extensión.

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
