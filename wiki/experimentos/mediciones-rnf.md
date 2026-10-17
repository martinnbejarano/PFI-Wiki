---
titulo: Mediciones de los RNF sobre el prototipo
tipo: análisis
tags: [rnf, rendimiento, costo, validacion]
fuentes: [prototipo/mediciones/rnf02.py, prototipo/mediciones/rnf03.py]
actualizado: 2026-10-17
---

# Mediciones de los RNF sobre el prototipo

Todo local en un M4 (servicio + BETO + extensión en la misma máquina, `make dev`), 16–17/10/2026. Volcado en la tabla `tab:criterios-validacion` del cap. 4.

| RNF | Umbral | Medido | Estado |
|---|---|---|---|
| 02 | 8 s p95 | p95 18,0 s, mediana 13,3 s (20 tuits redactados para la medición, sin caché) | ❌ |
| 03 | 300 ms | p95 1,3 ms secuencial, 4 ms con 10 concurrentes (300 pedidos) | ✅ |
| 12 | HTTPS + claves resumidas | SHA-256 de 64 caracteres, la clave en claro no está en la base. HTTPS no verificable en local | ⚠️ parcial |
| 13 | Chrome MV3 en 3 SO | Chrome 155 / macOS 26.6. Windows y Linux sin probar | ⚠️ parcial |
| 14 | 14 USD/mes | Infra 0 USD (local). LLM 0,0044 USD por análisis profundo en fichas (sin el cargo por búsqueda) | ✅ |
| 01, 04 | 2 s / 50 ms | Pendientes: requieren la sesión de X en el navegador | — |

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
