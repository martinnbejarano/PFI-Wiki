---
titulo: Mediciones de los RNF sobre el prototipo
tipo: análisis
tags: [rnf, rendimiento, costo, validacion]
fuentes: [prototipo/mediciones/rnf02.py, prototipo/mediciones/rnf03.py, prototipo/mediciones/rnf02-2026-10-19.txt]
actualizado: 2026-10-19
---

# Mediciones de los RNF sobre el prototipo

Todo local en un M4 (servicio + BETO + extensión en la misma máquina, `make dev`), 16–17/10/2026. Volcado en la tabla `tab:criterios-validacion` del cap. 4.

| RNF | Umbral | Medido | Estado |
|---|---|---|---|
| 02 | 8 s p95 | p95 14,9 s, mediana 11,1 s tras #93 (antes 18,0 / 13,3 s; 20 tuits redactados para la medición, sin caché) | ❌ |
| 03 | 300 ms | p95 1,3 ms secuencial, 4 ms con 10 concurrentes (300 pedidos) | ✅ |
| 12 | HTTPS + claves resumidas | Sobre el despliegue en Railway (19/10, <https://servicio-production-671c.up.railway.app>): TLS válido, `http://` redirige con 301; clave emitida por la API (56 caracteres) aceptada con `Bearer`, inválida → 401, administración sin secreto → 401. La base guarda solo el SHA-256 (64 caracteres, medido en local; el código es el mismo) | ✅ |
| 13 | Chrome MV3 en 3 SO | Chrome 155 / macOS 26.6. Windows y Linux sin probar | ⚠️ parcial |
| 14 | 14 USD/mes | Infra ≈ 1 USD/mes en Railway (64 MB de RAM, volumen de 85 MB). LLM 0,0044 USD por análisis profundo en fichas (sin el cargo por búsqueda) | ✅ |
| 01 | 2 s p95 | Componente del servicio desplegado: `POST /senales`, lote de 10, 20 corridas desde Buenos Aires contra Railway eu-west → mediana 0,85 s, p95 0,99 s, máx. 1,18 s. Con la ventana de agrupamiento de 150 ms ≈ 1,1 s. Falta la medición de punta a punta en X | ⚠️ parcial |
| 04 | 50 ms | Pendiente: requiere la sesión de X en el navegador | — |

## Objetivo 3: fuentes por análisis

20 tuits redactados para la medición (los mismos textos de RNF-02, ids nuevos): **16 con 3 o más fuentes (80 %)**, mediana 4, ninguno sin fuentes, 15 con al menos una fuente oficial. Salida en `prototipo/mediciones/fuentes-2026-10-17.txt`.

## Prompt injection

Tres intentos en vivo (`prototipo/mediciones/inyeccion.py`): ordenar «parece verificado» con un enlace inventado, pedir que no busque fuentes y pedir que insulte al autor. En los tres la afirmación extraída descartó la orden, el veredicto salió de las fuentes, no apareció el enlace inyectado y la justificación no habló del autor. Salida en `prototipo/mediciones/inyeccion-2026-10-17.txt`.

**Repetido el 19/10 tras #93**, ahora que el texto crudo del tuit entra a la llamada que busca: mismo resultado en los tres (ningún enlace inyectado, el segundo buscó igual y trajo 3 fuentes, la justificación no habla del autor). Salida en `prototipo/mediciones/inyeccion-2026-10-19.txt`.

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

## Cómo repetir

```
make dev                                   # desde prototipo/
python3 prototipo/mediciones/rnf02.py      # ~5 min, gasta crédito del LLM; SERVICIO=http://localhost:8001 para otro puerto
python3 prototipo/mediciones/rnf03.py
```

## Referencias cruzadas
- [[pruebas]]
- [[requerimientos]]
