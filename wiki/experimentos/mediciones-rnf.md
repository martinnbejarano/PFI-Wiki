---
titulo: Mediciones de los RNF sobre el prototipo
tipo: análisis
tags: [rnf, rendimiento, costo, validacion]
fuentes: [prototipo/mediciones/indice.py, prototipo/mediciones/indice-2026-10-26.txt, prototipo/mediciones/rnf02.py, prototipo/mediciones/rnf03.py, prototipo/mediciones/rnf02-2026-10-19.txt]
actualizado: 2026-10-26
---

# Mediciones de los RNF sobre el prototipo

Todo local en un M4 (servicio + BETO + extensión en la misma máquina, `make dev`), 16–17/10/2026. Volcado en la tabla `tab:criterios-validacion` del cap. 4.

| RNF | Umbral | Medido | Estado |
|---|---|---|---|
| 02 | 8 s p95 | p95 14,9 s, mediana 11,1 s tras #93 (antes 18,0 / 13,3 s; 20 tuits redactados para la medición, sin caché) | ❌ |
| 03 | 300 ms | p95 1,3 ms secuencial, 4 ms con 10 concurrentes (300 pedidos) | ✅ |
| 12 | HTTPS + claves resumidas | Sobre el despliegue en Railway (19/10, <https://servicio-production-671c.up.railway.app>): TLS válido, `http://` redirige con 301; clave emitida por la API (56 caracteres) aceptada con `Bearer`, inválida → 401, administración sin secreto → 401. La base guarda solo el SHA-256 (64 caracteres, medido en local; el código es el mismo) | ✅ |
| 13 | Chrome MV3 en 3 SO | Chrome 155 / macOS 26.6. Windows y Linux sin probar | ⚠️ parcial |
| 14 | 14 USD/mes | Infra en Railway: API ≈ 1 USD/mes (64 MB de RAM, volumen de 85 MB); clasificador BETO encendido ≈ 1,23 GB estable → ≈ 12 USD/mes, total ≈ 13 USD/mes. Por eso BETO queda apagado por defecto (`make beto-apagar`) y el modo normal cuesta ≈ 1 USD/mes. LLM 0,0044 USD por análisis profundo en fichas (sin el cargo por búsqueda) | ✅ |
| 01 | 2 s p95 | Componente del servicio desplegado: `POST /senales`, lote de 10, 20 corridas desde Buenos Aires contra Railway eu-west → mediana 0,85 s, p95 0,99 s, máx. 1,18 s. Con la ventana de agrupamiento de 150 ms ≈ 1,1 s. Falta la medición de punta a punta en X | ⚠️ parcial |
| 04 | 50 ms | Pendiente: requiere la sesión de X en el navegador | — |

## Objetivo 3: fuentes por análisis

20 tuits redactados para la medición (los mismos textos de RNF-02, ids nuevos): **16 con 3 o más fuentes (80 %)**, mediana 4, ninguno sin fuentes, 15 con al menos una fuente oficial. Salida en `prototipo/mediciones/fuentes-2026-10-17.txt`.

## Prompt injection

Tres intentos en vivo (`prototipo/mediciones/inyeccion.py`): ordenar «parece verificado» con un enlace inventado, pedir que no busque fuentes y pedir que insulte al autor. En los tres la afirmación extraída descartó la orden, el veredicto salió de las fuentes, no apareció el enlace inyectado y la justificación no habló del autor. Salida en `prototipo/mediciones/inyeccion-2026-10-17.txt`.

**Repetido el 19/10 tras #93**, ahora que el texto crudo del tuit entra a la llamada que busca: mismo resultado en los tres (ningún enlace inyectado, el segundo buscó igual y trajo 3 fuentes, la justificación no habla del autor). Salida en `prototipo/mediciones/inyeccion-2026-10-19.txt`.

## RNF-02 con una sola llamada (2026-10-20)

Se sacó la llamada de redacción (`c497769`): la búsqueda devuelve una `razon` por fuente y la justificación la arma el adaptador con el veredicto del combinador. Medición por pasos antes del cambio: búsqueda mediana 7,3 s (6,4–18,3), redacción 2,5–13 s. Resultado de punta a punta con los mismos 20 textos (`prototipo/mediciones/rnf02-2026-10-20.txt`): **mediana 8,46 s, p95 15,97 s** (antes 11,08 / 14,89). La cola es de la búsqueda.

Probado y descartado: dos búsquedas en paralelo quedándose con la primera dan **mediana 7,70 s, p95 9,12 s**, pero duplican el cargo por búsqueda (≈ 80 % del costo por análisis). Decisión del autor (2026-10-20): una sola búsqueda. Esfuerzo `none` en la búsqueda baja la mediana a 4,8 s pero trae menos fuentes y en un caso ninguna; descartado sin el corpus para medir el F1.

## Por qué falla RNF-02

**Antes (17/10).** Tres llamadas al LLM en serie. En 5 análisis instrumentados: extracción 1,7–2,9 s, **evidencia 5,4–8,7 s**, veredicto 2,6–4,0 s.

**Optimización de #93 (19/10).**

- La extracción va en la misma llamada que la búsqueda web (`extraer_y_recuperar` en el puerto): una llamada menos. Si esa llamada falla, se pierde el contraste y se reintenta la extracción sola, así que la degradación de RNF-11 queda igual.
- Esfuerzo de razonamiento: el paso que redacta pasa a `none` (`ESFUERZO_DE_RAZONAMIENTO_VEREDICTO`). La llamada conjunta sigue en `low`: con `none`, en 5 de 20 tuits el modelo **no buscó** (0 fuentes, ~2 s) y bajaron los análisis con 3+ fuentes de 16 a 13. Bajaba la mediana a 8,8 s a costa del objetivo 3 y de RNF-06, así que se descartó.
- Carga progresiva (módulos 1 y 2 primero): **no se hizo**. Exige un endpoint nuevo con una respuesta sin veredicto y un estado intermedio en el indicador y el detalle de la extensión; no entra en el contrato actual sin cambiarlo. Con BETO, el Módulo 1 tarda 0,05 s y el 2 es local, así que esa vía mostraría algo en menos de 0,1 s.

**Resultado** (`make dev` con `ADAPTADOR=compuesto`, los mismos 20 tuits, ids nuevos): p95 **14,9 s**, mediana **11,1 s**, máximo 14,9 s; ningún análisis parcial. Salida en `prototipo/mediciones/rnf02-2026-10-19.txt`. Desglose por etapa en una corrida en proceso de los mismos 20:

| Etapa | Mediana | Rango |
|---|---|---|
| Clasificador BETO (Módulo 1) | 0,05 s | 0,04–0,06 s |
| Extracción + evidencia (una llamada) | 8,4 s | 5,9–11,9 s |
| Veredicto (`none`) | 3,3 s | 2,6–4,2 s |

RNF-02 **sigue sin cumplirse**. La búsqueda web por sí sola ya ronda los 8 s y la redacción suma ~3 s que dependen de las fichas de salida, no del razonamiento. Lo que queda para llegar: el índice local del diseño en lugar de la búsqueda web, o la carga progresiva con su cambio de contrato.

> ⚠️ CONTRADICCION: el índice construido (#107) **no reemplaza** la búsqueda web sino que se le suma, y medido el 2026-10-26 sube la mediana unos 3 s (sección siguiente). Para que ayude a RNF-02, la búsqueda tendría que salir del camino crítico cuando el índice ya trae evidencia, y eso no se construyó.

## Índice de fuentes oficiales (#112, 2026-10-26)

Efecto del índice sobre **19 publicaciones reales de X** sobre datos oficiales, juntadas a mano el 2026-10-25 (`prototipo/mediciones/indice-publicaciones.csv`):

- **Temas:** IPC de septiembre, salarios, pobreza, desempleo, EMAE, el informe de la AGN sobre el oro del BCRA, Resolución 1447/2026, ORSNA 69/2026, Decreto 1128/2026, DEIS y Ley 27.795.
- **Método:** cada una se analizó con y sin índice (`UMBRAL_SIMILITUD_INDICE=1.01`), con dos servicios del proveedor compuesto real sobre una copia de la base con el índice cargado.
  - La memoria estuvo apagada en los dos.
  - Todo en local (M4, BETO y embebedor en `:7860`).
  - Umbral durante la corrida: 0,55, con K=3.

| | Con índice | Sin índice |
|---|---|---|
| Latencia mediana | 16,4 s | 13,5 s |
| Latencia p95 (máx.) | 19,1 s | 21,5 s |

- **Aciertos del índice:** 14 de 19 (74 %) devuelven al menos una fuente cuya URL está indexada. Las 19 recibieron fragmentos.
- **Veredictos que cambian:** 3 de 19.
  - **AGN y el oro del BCRA** (`ElEconomista_/2108296365604491407`): `contradicho_por_fuentes_oficiales` con índice, `parece_verificado` sin él, **usando fragmentos del BCRA**. La publicación cita un informe de la AGN, que no está indexada. Probable falso contradicho causado por el índice: un fragmento cercano pero ajeno.
  - **Lula y la pobreza** (`VictorMarcano`): `contradicho` con índice, sin una fuente del índice en el resultado.
  - **Desempleo e informalidad** (`ElEconomista_/2100697960681980113`): `parece_verificado` con índice y `sospechosa` sin él, también sin una fuente del índice.

  Los dos últimos no usaron el índice, así que es probable que sean variación propia del LLM.
- **Latencia:** el índice suma unos 3 s de mediana; los fragmentos alargan el mensaje y el LLM tiene que clasificar su postura. El p95 no empeora, pero con 19 casos lo domina la cola de la búsqueda web. Va contra la expectativa de US 6 de que el índice no agregara latencia.
- **Calibración del umbral: 0,55 → 0,60** (`app/configuracion.py`).
  - La similitud máxima de los 19 casos va de 0,593 a 0,808 (mediana 0,718).
  - Seis textos de control ajenos al índice (fútbol, música, un teléfono, saludos) dan entre 0,281 y 0,592. Los escribió el autor y no son publicaciones de X, y solo se midió su similitud, sin LLM. El de Boca (0,592) habría pasado con 0,55.
  - Con 0,60 entran 18 de 19 casos y ningún control. El que queda afuera (0,593, Ley 27.795) no había devuelto fuentes del índice.
  - La medición no se volvió a correr con 0,60.
- **Límites:**
  - una sola corrida, sin repeticiones, y un único anotador eligió los casos;
  - los controles son sintéticos;
  - los veredictos no tienen etiqueta de referencia, así que la medición dice si cambian, no si mejoran.
  - No toca RNF-05.

## Cómo repetir

```
make dev                                   # desde prototipo/
python3 prototipo/mediciones/rnf02.py      # ~5 min, gasta crédito del LLM; SERVICIO=http://localhost:8001 para otro puerto
python3 prototipo/mediciones/rnf03.py
prototipo/servicio/.venv/bin/python prototipo/mediciones/indice.py   # índice (#112): 2 análisis profundos por publicación; RUTA_BASE_DE_DATOS con el índice cargado
```

## Referencias cruzadas
- [[pruebas]]
- [[requerimientos]]

## Memoria del clasificador en Railway

`railway metrics -s clasificador` (2026-10-19, última hora): 1,23 GB de memoria en régimen, CPU media 0,03 vCPU (pico 1,7 al cargar). Base del ≈ 12 USD/mes con BETO encendido.
