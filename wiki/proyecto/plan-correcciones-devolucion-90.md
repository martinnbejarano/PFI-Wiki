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
| Infraestructura (J7, J8) | Migrar a Azure `chilecentral` (Santiago, por latencia; la suscripción de estudiante solo permite Chile, Canadá, Nueva Zelanda, Sudáfrica y EE. UU.) en el código y en el documento. Railway queda como antecedente y se da de baja cuando Azure esté verificado. Se había elegido GCP, pero la prueba de USD 300 ya estaba usada en la cuenta (14/11) |
| Cuenta de nube | Azure for Students: USD 100 sin tarjeta por 12 meses |
| Base de datos | PostgreSQL + `pgvector` en todos los entornos: Azure Database for PostgreSQL (servidor flexible) en producción y Docker en local y en los tests. Sin doble implementación |
| Clasificador BETO | Azure Container Apps con *ingress* interno (solo dentro del entorno), **escala a cero**, con los pesos dentro de la imagen. Se enciende solo para demos y la defensa |
| Inversión del año 0 (J6) | Llevarla a unos USD 8.000: contador e impuestos (~USD 120/mes × 12), horas del fundador (2 meses de sueldo Sysarmy sin cargas, ≈ USD 3.580), infraestructura recalculada con Azure y una reserva operativa hasta el primer tramo. Se revierte la decisión del 18/10 de no imputar horas |
| Plan individual (J3) | Plan pago de USD 5/mes con 150 análisis (costo ≈ USD 3,7), con una conversión de gratuito a pago del 2 al 3 % según el escenario |
| Ley 25.326 | Se saca solo el argumento del art. 12 (país adecuado, UE). El alojamiento en Chile queda cubierto por el mismo consentimiento de primer uso que ya ampara la transferencia a OpenAI. El resto del análisis (HMAC, art. 7, fuentes de acceso público) se mantiene para J5 |
| Organización | Dos ramas en paralelo, issues en GitHub, entrada en `history/`, actualización de guion y preguntas |

## Rama A: `feat/financiero-devolucion` (cap. 3)

1. **D1:** nuevos renglones de inversión del año 0, cada uno con su fuente.
2. **D2:** plan individual en `tab:pricing` y en el modelo, con su conversión.
3. **D5:** una oración que vincule el escenario pesimista con la brecha entre la intención de uso (encuesta) y la adopción.
4. **D4:** que la viabilidad legal diga explícitamente qué se guarda de la cuenta autora (HMAC) y qué no.
5. Regenerar el modelo (`scripts/generar_modelo_financiero.py`, `scripts/validar_modelo_financiero.py`, tablas `.tex`) y actualizar las cifras citadas en el texto, el resumen, el *abstract* y la conclusión.

## Rama B: `feat/migracion-azure` (código y cap. 4)

1. Portar SQLite y `sqlite-vec` a Postgres + `pgvector` en `app/historial.py`, `app/proveedor/memoria.py` y `app/proveedor/indice.py`. Postgres local en Docker levantado desde el `Makefile`.
2. Desplegar en Azure `chilecentral`:
   - API en Container Apps.
   - BETO en Container Apps (*ingress* interno, escala a cero).
   - PostgreSQL flexible con `pgvector`.
   - Container Apps Job con cron para la ingesta.
   - Secretos de Container Apps.
   - Imágenes en GHCR (gratis) en lugar de Azure Container Registry.
   - `make desplegar` con `az`.
3. Cambiar la URL del servicio en `prototipo/extension/`. Medir el costo mensual, el arranque en frío de BETO y RNF-01 en el despliegue nuevo.
4. **Art. 12:** cap. 3 (viabilidad legal, l. ~533 y el aviso de consentimiento), cap. 4 (región y razones del despliegue) y [[wiki/proyecto/restricciones-legales-eticas]]: sacar «UE = país adecuado» y extender el consentimiento al alojamiento en Chile.
5. **D3 + D6 en el cap. 4:**
   - Evaluación comparada (Railway, Azure Container Apps, VPS; GCP Cloud Run como alternativa equivalente) con costo, operación, seguridad y región.
   - Razones del despliegue reescritas.
   - Diagrama de despliegue.
   - Seguridad y validación (RNF-12, RNF-14, RNF-16).
   - Cita de precios de Azure.
6. Baja de Railway.

## Cierre (con las dos ramas mergeadas)

- Costos fijos de infraestructura de Azure en el modelo financiero y recálculo definitivo.
- `presentacion/GUION.md` y `PREGUNTAS.md`:
  - Cierre de memoria.
  - Cifras correctas (USD 1.716 pasan a la nueva inversión; TIR 72,6 % o el valor nuevo).
  - Pesimista explicado con los tramos.
  - Primera persona singular.
  - Notas de la Comunidad con el 16,9 % y las 23 h.
  - Respuestas sobre inversión, nube y legal.
- Wiki (`analisis-financiero`, `tecnologias`, `arquitectura`), `log.md` y una entrada en `documento/history/`.

## Acción manual

Activar Azure for Students con el correo de UADE, `brew install azure-cli` y `az login`. Verificar en el portal si PostgreSQL flexible tiene horas gratuitas en la suscripción; si no, cuesta unos USD 13 a 15 por mes contra el crédito.

## Riesgo

El port a Postgres es lo más largo. Si para el ~1/12 no está desplegado, el cap. 4 lleva la evaluación comparada con el plan de migración y el código queda en la rama.

## Referencias cruzadas
- [[wiki/proyecto/devolucion-presentacion-90]]
- [[wiki/negocio/analisis-financiero]]
- [[wiki/solucion/tecnologias]]
- [[wiki/solucion/arquitectura]]
- [[wiki/proyecto/cronograma]]
