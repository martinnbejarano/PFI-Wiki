# Mapa — Cierre de los criterios 5 y 6 y saneamiento legal

## Destination

Los criterios **5 (tecnologías)** y **6 (modelo de datos)** de la rúbrica de EP2 quedan cubiertos y sin contradicciones, en dos lugares: las páginas del wiki (`solucion/modelo-datos.md`, `solucion/tecnologias.md`, `proyecto/restricciones-legales-eticas.md`) **y** el texto correspondiente en `documento/chapters/chapter04.tex`. El apartado legal deja de contradecir el diseño y pasa a ser defendible artículo por artículo ante el tutor.

## Notes

**Dominio.** PFI de Ingeniería en Informática (UADE 2026): sistema de detección de desinformación en Twitter/X para español rioplatense. Entrega del 50% el **22/08**, exposición el **29/08**. Rúbrica en `raw/clases/Rubrica-EP2-50porciento.pdf`; alcance en `wiki/proyecto/entrega-50-alcance.md`.

**Este mapa carga ejecución, no solo decisiones.** El destino son artefactos escritos, así que los tickets marcados `task` producen texto —páginas del wiki y LaTeX—, no decisiones. Los `grilling` sí resuelven decisiones y bloquean a los `task`.

**Skills a consultar en cada sesión.** `/grilling` y `/domain-modeling` para los tickets de decisión. El `CLAUDE.md` del repositorio manda en todo lo demás: voz impersonal, terminología consistente, frases prohibidas, citas ISO 690-2010 con `\parencite{}` sobre `biblio.bib`, y *commit* por cada página tocada.

**Preferencias fijadas al trazar el mapa (2026-08-10).**

1. Destino: wiki **y** volcado a `chapter04.tex`, en el mismo esfuerzo. Escribir dos veces es el desperdicio, y los capítulos 3 y 4 vacíos son hoy el riesgo real de la entrega.
2. Legal: **reescritura completa** del archivo, no un parche de la matriz.
3. `tecnologias.md`: técnico puro —lenguajes, *frameworks*, versiones, librerías—; `recursos.md` sigue siendo la página de costos. Se enlazan, no se duplican.
4. DER a nivel **lógico**: atributos, tipos, PK/FK y cardinalidades. Sin DDL ejecutable.

**Regla de corte heredada** de `plan-bloque-diseno.md`: toda entidad del modelo de datos tiene que ser trazable a un RF. Si no lo es, se va.

**Tickets de investigación.** Se resuelven con búsqueda web dentro de su propia sesión, no delegando en un subagente.

## Decisions so far

<!-- una línea por ticket cerrado -->

_Ninguna todavía._

## Not yet specified

- **Impacto sobre `requerimientos.md`.** Si la decisión de retención o la de supresión obligan a un RF nuevo, hay que reabrir las dos tablas y la matriz de trazabilidad. No se puede especificar antes de conocer la decisión.
- **Impacto sobre CU-05 y RF-15.** Si el ticket 02 concluye que el UUID no debe llegar al servidor, el histórico personal se queda sin sustento y hay que rehacer el caso de uso, no solo el esquema.
- **Retoque de diagramas ya exportados.** `c4-componentes`, `flujo-informacion` y `despliegue-red` dibujan qué se persiste y en qué frontera. Si el esquema cambia eso, hay que corregir el `.drawio` y reexportar con `_tools/exportar.py`. Alcance desconocido hasta cerrar el ticket 06.
- **Versionado y migraciones del esquema.** Alembic o equivalente. No está claro si es una decisión de tecnologías o trabajo del Bloque 3.
- **Ubicación del apartado legal en el documento.** El mapa wiki→documento de `CLAUDE.md` manda `wiki/proyecto/` al capítulo 1, pero un desarrollo legal de este porte encaja mejor en el 4. Se decide dentro del ticket 11.

## Out of scope

- **DDL SQL ejecutable y creación real de la base.** Es Bloque 3 (17-18/08), junto con el *vertical slice* de la demo. Fijado en la pregunta de alcance del 2026-08-10.
- **`chapter03.tex`** —user research, competencia y negocio—. Es un esfuerzo aparte con sus propios bloqueos de terceros.
- **Decisiones 4 y 5 de `wiki/sintesis/decisiones-pendientes-2026-08.md`** —tamaño del corpus argentino y número de clases—. Pertenecen a la Entrega 4 y no bloquean el 22/08.
- **Difusión de la encuesta y pedidos de entrevista.** Pendientes reales, pero de otro esfuerzo y dependientes de terceros.
