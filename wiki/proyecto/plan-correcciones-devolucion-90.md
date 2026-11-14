---
titulo: Plan de correcciones de la devolución del 90 %
tipo: proyecto
tags: [entrega-90, devolucion, defensa-final, plan]
fuentes: [devolucion-presentacion-90.md]
actualizado: 2026-11-14
---

# Plan de correcciones de la devolución del 90 %

Plan acordado el 14/11/2026 para atender la [[wiki/proyecto/devolucion-presentacion-90]] antes de la defensa (9 al 14/12/2026). El trabajo avanza en dos ramas en paralelo y cada ítem tiene su *issue* en GitHub.

## Decisiones tomadas

| Tema | Decisión |
|---|---|
| Infraestructura (J7, J8) | Migrar a GCP `europe-west4` en el código y en el documento. Railway queda como antecedente y se da de baja cuando GCP esté verificado |
| Cuenta de GCP | Prueba de USD 300 por 90 días, que cubre hasta después de la defensa |
| Base de datos | PostgreSQL + `pgvector` en todos los entornos: Cloud SQL en producción y Docker en local y en los tests. Sin doble implementación |
| Clasificador BETO | Cloud Run con *ingress* interno + IAM, **escala a cero**, con los pesos dentro de la imagen. Se enciende solo para demos y la defensa |
| Inversión del año 0 (J6) | Llevarla a unos USD 8.000: contador e impuestos (~USD 120/mes × 12), horas del fundador (2 meses de sueldo Sysarmy sin cargas, ≈ USD 3.580), infraestructura recalculada con GCP y una reserva operativa hasta el primer tramo. Se revierte la decisión del 18/10 de no imputar horas |
| Plan individual (J3) | Plan pago de USD 5/mes con 150 análisis (costo ≈ USD 3,7), con una conversión de gratuito a pago del 2 al 3 % según el escenario |
| Organización | Dos ramas en paralelo, issues en GitHub, entrada en `history/`, actualización de guion y preguntas |

## Rama A: `feat/financiero-devolucion` (cap. 3)

1. **D1:** nuevos renglones de inversión del año 0, cada uno con su fuente.
2. **D2:** plan individual en `tab:pricing` y en el modelo, con su conversión.
3. **D5:** una oración que vincule el escenario pesimista con la brecha entre la intención de uso (encuesta) y la adopción.
4. **D4:** que la viabilidad legal diga explícitamente qué se guarda de la cuenta autora (HMAC) y qué no.
5. Regenerar el modelo (`scripts/generar_modelo_financiero.py`, `scripts/validar_modelo_financiero.py`, tablas `.tex`) y actualizar las cifras citadas en el texto, el resumen, el *abstract* y la conclusión.

## Rama B: `feat/migracion-gcp` (código y cap. 4)

1. Portar SQLite y `sqlite-vec` a Postgres + `pgvector` en `app/historial.py`, `app/proveedor/memoria.py` y `app/proveedor/indice.py`. Postgres local en Docker levantado desde el `Makefile`.
2. Desplegar en GCP:
   - API en Cloud Run.
   - BETO en Cloud Run (interno, IAM, escala a cero).
   - Cloud SQL.
   - Cloud Scheduler para la ingesta.
   - Secret Manager.
   - `make desplegar` con `gcloud`.
3. Cambiar la URL del servicio en `prototipo/extension/`. Medir el costo mensual, el arranque en frío de BETO y RNF-01 en el despliegue nuevo.
4. **D3 + D6 en el cap. 4:**
   - Evaluación comparada (Railway, Cloud Run, VPS) con costo, operación, seguridad y región.
   - Razones del despliegue reescritas.
   - Diagrama de despliegue.
   - Seguridad y validación (RNF-12, RNF-14, RNF-16).
   - Cita de precios de GCP.
5. Baja de Railway.

## Cierre (con las dos ramas mergeadas)

- Costos fijos de infraestructura de GCP en el modelo financiero y recálculo definitivo.
- `presentacion/GUION.md` y `PREGUNTAS.md`:
  - Cierre de memoria.
  - Cifras correctas (USD 1.716 pasan a la nueva inversión; TIR 72,6 % o el valor nuevo).
  - Pesimista explicado con los tramos.
  - Primera persona singular.
  - Notas de la Comunidad con el 16,9 % y las 23 h.
  - Respuestas sobre inversión, nube y legal.
- Wiki (`analisis-financiero`, `tecnologias`, `arquitectura`), `log.md` y una entrada en `documento/history/`.

## Acción manual

Crear el proyecto de GCP, activar la prueba (pide tarjeta), `brew install google-cloud-sdk` y `gcloud auth login`.

## Riesgo

El port a Postgres es lo más largo. Si para el ~1/12 no está desplegado, el cap. 4 lleva la evaluación comparada con el plan de migración y el código queda en la rama.

## Referencias cruzadas
- [[wiki/proyecto/devolucion-presentacion-90]]
- [[wiki/negocio/analisis-financiero]]
- [[wiki/solucion/tecnologias]]
- [[wiki/solucion/arquitectura]]
- [[wiki/proyecto/cronograma]]
