# 08 · Reescribir `restricciones-legales-eticas.md`

Type: task
Status: open
Blocked by: 01, 02, 03, 04, 05, 12

## Question

Reescribir el archivo completo. Hoy es un borrador del 19/04 que contradice el diseño en seis puntos y omite los tres artículos que sostienen la defensa acordada.

Lo que el archivo dice y ya no es cierto:

| Línea | Dice | El diseño hace |
|---|---|---|
| 12-16 | «Anonimizamos metadatos personales (ID usuario)» | Persiste el `@` en claro (decisión 3) |
| 29-30 | Riesgo alto: eliminar o hashear el ID de usuario | Ídem |
| 74-77 | *Score*, no veredicto; 0-1, no Verdadero/Falso | Tres niveles con umbrales 0,40 y 0,75 |
| 93 | Usar la API oficial de Twitter | Lectura del DOM por la extensión |
| 95 | Evitar el *scraping* sin permiso | Seis sitios en `recursos.md` |
| 96 | Chequeado: «negociar con el equipo» | Nunca se hizo |

Lo que falta y hay que incorporar: **art. 5 inc. 2.b** (fuentes de acceso público irrestricto, que ampara la recolección), **art. 11** (cesión a terceros, que es la exposición real de la exportación B2B y se mitiga con RF-25 y RNF-10), **art. 4 inc. 7** y **art. 16** (del ticket 01), y **art. 21** (del ticket 05).

La estructura acordada parte el riesgo en dos, porque son dos riesgos distintos con dos defensas distintas: **recolección** —amparada, con su límite explícito: no aplica a cuentas protegidas ni a mensajes directos— y **cesión** —expuesta, mitigada por diseño—.

Corregir de paso «anonymizar», que aparece nueve veces y no es una palabra en castellano.

**Trabajo posterior.** Verificar que RNF-09 y RNF-10 de `requerimientos.md` sigan diciendo lo mismo que el archivo reescrito, y sumar a `biblio.bib` las entradas de la Ley 25.326, el Decreto 1558/2001 y lo que traiga el ticket 05.
