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
