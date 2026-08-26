# Guion de capturas — criterio 7 de EP2

Material de trabajo para el [issue #26](https://github.com/martinnbejarano/PFI-Wiki/issues/26).
El criterio 7 pide capturas que muestren avances en el desarrollo de las funcionalidades, y
es el único de los ocho que quedó pendiente del documento entregado el 22/08.

Cada captura lleva un comentario que **nombra el requerimiento que realiza**. Esa
correspondencia es lo que convierte un puñado de pantallas en evidencia de avance.

---

## Antes de capturar

**1. La credencial.** En `prototipo/servicio/.env`:

```
OPENAI_API_KEY=...
```

Sin ella todo degrada a análisis parcial, que sirve para *una* captura pero no para las otras.

**2. Los dos artefactos andando.**

```bash
cd prototipo/servicio && ./.venv/bin/uvicorn app.main:aplicacion --port 8000 --log-level info
cd prototipo/extension && npm run build
```

Cargar `prototipo/extension/dist` en `chrome://extensions` con el modo de desarrollador
activo.

**3. Paso cero, y es el que puede arruinar todo: comprobar que x.com carga con la extensión
puesta.** X devuelve *«Some privacy related extensions may cause issues on x.com»* cuando
detecta una extensión que bloquea peticiones de red. Con ese cartel la *timeline* no monta y
no hay nada que capturar. Hay que verificar, **con las dos extensiones cargadas a la vez**,
que la *timeline* aparece. Si no aparece, desactivar la extensión de privacidad y volver a
probar hasta aislar cuál es.

Esto vale para la exposición del 29 tanto como para las capturas: la máquina que demuestre
tiene que estar en ese estado comprobado, no en el habitual.

**4. Higiene, que es criterio de aceptación.** Ninguna captura puede mostrar la credencial ni
datos personales. Antes de disparar: cerrar la pestaña de `.env` y la del editor, ocultar la
barra de marcadores, y usar una cuenta o una vista donde no aparezcan mensajes privados ni
notificaciones. Si un tuit capturado pertenece a una cuenta identificable, **difuminar el
nombre y el `@`** — el apartado ético del propio documento prohíbe señalar cuentas reales
como fuente de desinformación, y una captura que lo hace contradice el capítulo 3.

---

## Las capturas

Ocho, en este orden. Los estados se provocan con la configuración que ya existe: no hay
banderas de prueba escondidas. El detalle de cada palanca está en la sección «Cómo se
provoca cada estado a mano» del [README](README.md).

### 1 · El indicador sobre la *timeline*

**Realiza:** RF-08 · **Caso de uso:** CU-01

La *timeline* de X con el indicador inyectado sobre varios tuits. Es la pantalla más
importante del producto: la única que el usuario ve sin haber pedido nada.

**Comentario:** *El sistema inyecta un indicador sobre cada publicación del* timeline *de X,
sin degradar la página (RF-08).*

### 2 · El estado transitorio

**Realiza:** RF-08

Un clic en el indicador, capturado mientras resuelve. Si pasa demasiado rápido para
capturarlo, alargarlo con `ESFUERZO_DE_RAZONAMIENTO=high` al levantar el servicio.

**Comentario:** *El análisis es a demanda: se dispara por clic y el estado transitorio informa
que el sistema está trabajando (RF-08).*

### 3 · Los tres niveles de veredicto

**Realiza:** RF-06, RF-08 · **Caso de uso:** CU-02

Los tres —contradicho por fuentes oficiales, información sospechosa, parece verificado— sobre
tuits reales. Si el material del día no los produce naturalmente, se alcanzan moviendo los
umbrales en la configuración, **que es lo que RNF-16 existe para permitir**.

**Comentario:** *El veredicto se emite en los tres niveles definidos, y el más severo atribuye
el juicio a las fuentes que lo sostienen en lugar de afirmarlo el sistema (RF-06, RNF-07).*

### 4 · El estado *sin contraste externo*

**Realiza:** RF-06, RNF-06

Una afirmación cuya evidencia caiga fuera de los trece dominios de la jerarquía, o una
publicación sin afirmación verificable. Sin porcentaje: la ausencia de evidencia se muestra
como ausencia.

**Comentario:** *Cuando ningún módulo de contraste encuentra fuente, el sistema emite* sin
contraste externo *en lugar de un veredicto sin respaldo (RNF-06).*

### 5 · El detalle con el desglose de los tres puntajes

**Realiza:** RF-09, RF-08 · **Caso de uso:** CU-02

Abierto desde el indicador. Tiene que verse la afirmación extraída con su tipo, y el desglose
de los tres puntajes parciales. **El puntaje de credibilidad tiene que aparecer con barra
rayada y etiqueta *sin dato*** — es el recorte declarado del Módulo 2 y mostrarlo así es lo
que hace defendible el recorte.

**Comentario:** *El desglose de los tres puntajes parciales hace auditable el resultado. El
Módulo 2 aparece marcado como no implementado y no pondera en el puntaje final (RF-09).*

### 6 · El panel de evidencia

**Realiza:** RF-05, RF-09, RNF-06 · **Caso de uso:** CU-03

Es **la captura más importante de las ocho**: es el diferencial del proyecto y lo que ningún
competidor de la matriz comparativa entrega al ciudadano. Tienen que verse las fuentes
agrupadas por jerarquía —oficiales, medios, verificadores— con su postura y su enlace.

Conviene acompañarla de **una segunda captura con una de esas fuentes abierta en su sitio
original**, mostrando que el enlace lleva al documento real. Eso es lo que convierte «el
sistema dice» en «el usuario puede comprobar».

**Comentario:** *Cada veredicto viaja con las fuentes que lo respaldan, restringidas a la
jerarquía de evidencia y enlazadas al documento original (RF-05, RNF-06).*

### 7 · El análisis parcial

**Realiza:** RNF-11, RF-08

Se provoca sin credencial:

```bash
cd prototipo/servicio
env -u OPENAI_API_KEY ./.venv/bin/uvicorn app.main:aplicacion --port 8000
```

Tiene que verse la tapa de análisis parcial, el guión en lugar del porcentaje y los módulos
ausentes nombrados.

**Comentario:** *Ante la caída del servicio de inferencia el sistema devuelve un análisis
parcial identificado como tal, nunca un error opaco ni un veredicto construido sobre módulos
faltantes (RNF-11).*

### 8 · Los pesos configurables

**Realiza:** RNF-16, RF-16

El mismo tuit analizado dos veces con distintos pesos del combinador, mostrando que el
puntaje final cambia **y que `version_configuracion_pesos` cambia con él**. Es la captura que
menos se espera y la que mejor responde a un tribunal que pregunte si el sistema es ajustable
o está clavado.

```bash
PESO_CONTRASTE=0.9 ./.venv/bin/uvicorn app.main:aplicacion --port 8000
```

**Comentario:** *Los pesos del ensamblado y los umbrales de los veredictos se ajustan sin
volver a desplegar el servicio, y cada análisis queda asociado a la versión de configuración
que lo produjo (RNF-16, RF-16).*

---

## El video de respaldo

Un recorrido corto —dos o tres minutos— del flujo completo: abrir X, hacer clic en un
indicador, ver el veredicto, abrir el detalle, abrir el panel de evidencia, abrir una fuente.

Existe por una razón concreta: la cátedra aceptó que la demostración sea en vivo, con capturas
comentadas o en video, y **el video es lo que salva el criterio 7 si el 29 falla la red, la
sesión de X o el proveedor**. Grabarlo el día antes, no el mismo día.

Lo que el video **no** cubre es que X se niegue a cargar por el cartel de extensiones de
privacidad. Ese es el riesgo que la *spec* dejó explícitamente sin mitigar al decidir
demostrar sobre X real y no sobre un *fixture*.

---

## Dónde va el material

En `prototipo/capturas/`, versionado en el repositorio, para que la presentación pueda
referenciarlo. Nombres que digan qué son: `01-indicador-timeline.png`,
`06-panel-evidencia.png`, y así.
