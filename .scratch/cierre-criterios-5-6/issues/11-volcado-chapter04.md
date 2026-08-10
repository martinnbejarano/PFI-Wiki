# 11 · Volcado a `chapter04.tex`

Type: task
Status: open
Blocked by: 07, 08, 10

## Question

Llevar al documento lo que los tickets anteriores dejaron en el wiki. Hoy `chapter04.tex` tiene **19 palabras y cinco `Completar.`**, y es lo que efectivamente se evalúa el 22/08.

Trabajo:

1. Sección de **modelo de datos** con el DER incluido vía `\input{figures/...}` o `\includegraphics`, referenciado con `\ref{}`, y las tablas de entidades en formato del template —numeración romana por capítulo, ubicación `[t]`—.
2. Sección de **tecnologías y arquitectura de red**, con el diagrama de despliegue ya exportado.
3. El **apartado legal**. Decisión abierta dentro de este ticket: el mapa wiki→documento de `CLAUDE.md` manda `wiki/proyecto/` al capítulo 1, pero un desarrollo de este porte encaja mejor en el 4, junto a las decisiones de diseño que lo justifican. Elegir y, si se aparta del mapa, dejarlo escrito en `documento/history/`.
4. Descomentar la línea de `chapter04` en `main.tex:276-277`. **Hoy están comentados los capítulos 3 y 4**, y por eso una referencia cruzada a este capítulo salió como `Capítulo ??` en el bloque anterior.
5. Sumar a `biblio.bib` lo que traigan los tickets 05 y 08 —la Ley 25.326, el Decreto 1558/2001 y las fuentes de la AAIP— con el formato `@online` y su `note` de fecha de consulta.

**Adaptación de tono, que es donde está el trabajo real.** El wiki es exploratorio y el documento es académico: voz impersonal, terminología consistente, nada de las frases prohibidas del `CLAUDE.md`, listas de *bullets* convertidas a prosa o a `\begin{enumerate}`, cita al final de toda afirmación que la requiera, y ninguna advertencia de contradicción del wiki.

**Verificación.** `cd documento && pdflatex main && biber main && pdflatex main` sin advertencias de `biber`, sin referencias sin resolver y sin `Completar.` en las secciones tocadas.

**Fuera de alcance.** El resto de `chapter04.tex` —metodología de desarrollo, *datasets*, validación— y `chapter03.tex` entero. Este ticket cubre los criterios 5 y 6 y el apartado legal, nada más.
