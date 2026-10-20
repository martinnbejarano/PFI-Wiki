---
titulo: Mediciones de los RNF sobre el prototipo
tipo: análisis
tags: [rnf, rendimiento, costo, validacion]
fuentes: [prototipo/mediciones/rnf02.py, prototipo/mediciones/rnf03.py]
actualizado: 2026-10-19
---

# Mediciones de los RNF sobre el prototipo

Todo local en un M4 (servicio + BETO + extensión en la misma máquina, `make dev`), 16–17/10/2026. Volcado en la tabla `tab:criterios-validacion` del cap. 4.

| RNF | Umbral | Medido | Estado |
|---|---|---|---|
| 02 | 8 s p95 | p95 18,0 s, mediana 13,3 s (20 tuits redactados para la medición, sin caché) | ❌ |
| 03 | 300 ms | p95 1,3 ms secuencial, 4 ms con 10 concurrentes (300 pedidos) | ✅ |
| 12 | HTTPS + claves resumidas | Sobre el despliegue en Railway (19/10, <https://servicio-production-671c.up.railway.app>): TLS válido, `http://` redirige con 301; clave emitida por la API (56 caracteres) aceptada con `Bearer`, inválida → 401, administración sin secreto → 401. La base guarda solo el SHA-256 (64 caracteres, medido en local; el código es el mismo) | ✅ |
| 13 | Chrome MV3 en 3 SO | Chrome 155 / macOS 26.6. Windows y Linux sin probar | ⚠️ parcial |
| 14 | 14 USD/mes | Infra ≈ 1 USD/mes en Railway (64 MB de RAM, volumen de 85 MB). LLM 0,0044 USD por análisis profundo en fichas (sin el cargo por búsqueda) | ✅ |
| 01, 04 | 2 s / 50 ms | Pendientes: requieren la sesión de X en el navegador | — |

## Objetivo 3: fuentes por análisis

20 tuits redactados para la medición (los mismos textos de RNF-02, ids nuevos): **16 con 3 o más fuentes (80 %)**, mediana 4, ninguno sin fuentes, 15 con al menos una fuente oficial. Salida en `prototipo/mediciones/fuentes-2026-10-17.txt`.

## Prompt injection

Tres intentos en vivo (`prototipo/mediciones/inyeccion.py`): ordenar «parece verificado» con un enlace inventado, pedir que no busque fuentes y pedir que insulte al autor. En los tres la afirmación extraída descartó la orden, el veredicto salió de las fuentes, no apareció el enlace inyectado y la justificación no habló del autor. Salida en `prototipo/mediciones/inyeccion-2026-10-17.txt`.

## Por qué falla RNF-02

Tres llamadas al LLM en serie. En 5 análisis instrumentados: extracción 1,7–2,9 s, **evidencia 5,4–8,7 s**, veredicto 2,6–4,0 s. La búsqueda web por sí sola ya consume los 8 s. Las salidas: el índice local del diseño o paralelizar pasos.

## Cómo repetir

```
make dev                                   # desde prototipo/
python3 prototipo/mediciones/rnf02.py      # ~5 min, gasta crédito del LLM
python3 prototipo/mediciones/rnf03.py
```

## Referencias cruzadas
- [[pruebas]]
- [[requerimientos]]
