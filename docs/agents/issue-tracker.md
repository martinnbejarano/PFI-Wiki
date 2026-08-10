# Issue tracker: GitHub

Los *issues* y las *specs* de este repo viven como *issues* de GitHub, en `martinnbejarano/PFI-Wiki`. Todas las operaciones se hacen con la CLI `gh`, que infiere el repo desde `git remote -v` cuando se corre dentro del clon.

## Convenciones

- **Crear**: `gh issue create --title "..." --body "..."`. Para cuerpos de varias líneas, *heredoc*.
- **Leer**: `gh issue view <n> --comments`.
- **Listar**: `gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'`, con los filtros `--label` y `--state` que correspondan.
- **Comentar**: `gh issue comment <n> --body "..."`
- **Etiquetar**: `gh issue edit <n> --add-label "..."` / `--remove-label "..."`
- **Cerrar**: `gh issue close <n> --comment "..."`

**Idioma.** Títulos y cuerpos en castellano, como el resto del repositorio. Los nombres de etiqueta se dejan en inglés porque son identificadores que las *skills* leen literalmente.

## Pull requests como superficie de triage

**PRs como superficie de pedidos: no.** _(Poner `sí` si este repo tratara los PR externos como pedidos de funcionalidad; `/triage` lee esta bandera.)_

Es un repositorio de un solo autor sin colaboradores externos, así que la bandera queda apagada.

## Cuando una skill dice «publicar en el issue tracker»

Crear un *issue* de GitHub.

## Cuando una skill dice «traer el ticket correspondiente»

`gh issue view <n> --comments`.

## Operaciones de wayfinding

Las usa `/wayfinder`. El **mapa** es un *issue* con *issues* hijos como tickets.

- **Mapa**: un *issue* con la etiqueta `wayfinder:map`, que contiene el cuerpo de Destino / Notas / Decisiones tomadas / Niebla. `gh issue create --label wayfinder:map`.
- **Ticket hijo**: un *issue* vinculado al mapa como *sub-issue* de GitHub (`gh api` sobre el *endpoint* de *sub-issues*). Si los *sub-issues* no estuvieran habilitados, se agrega el hijo a una lista de tareas en el cuerpo del mapa y se pone `Part of #<mapa>` al principio del cuerpo del hijo. Etiquetas: `wayfinder:<tipo>` — `research`, `prototype`, `grilling` o `task`. Al reclamarlo, el ticket se asigna a quien conduce el mapa.
- **Bloqueo**: las **dependencias nativas** de GitHub, que son la representación canónica y visible en la interfaz. Se agrega una arista con `gh api --method POST repos/<owner>/<repo>/issues/<hijo>/dependencies/blocked_by -F issue_id=<id-de-base-del-bloqueante>`, donde ese id es el **id numérico de base de datos** del bloqueante (`gh api repos/<owner>/<repo>/issues/<n> --jq .id`, **no** el `#número` ni el `node_id`). GitHub informa `issue_dependencies_summary.blocked_by`, que cuenta solo bloqueantes abiertos y es la compuerta viva. Si las dependencias no estuvieran disponibles, se cae a una línea `Blocked by: #<n>, #<n>` al principio del cuerpo del hijo. Un ticket está desbloqueado cuando todos sus bloqueantes están cerrados.
- **Consulta de frontera**: listar los hijos abiertos del mapa (`gh issue list --state open`, acotado a los *sub-issues* o a la lista de tareas), descartar los que tengan un bloqueante abierto (`issue_dependencies_summary.blocked_by > 0`) o una persona asignada; gana el primero en el orden del mapa.
- **Reclamar**: `gh issue edit <n> --add-assignee @me`, y es la primera escritura de la sesión.
- **Resolver**: `gh issue comment <n> --body "<respuesta>"`, después `gh issue close <n>`, y por último agregar el puntero de contexto —resumen más enlace— a las Decisiones tomadas del mapa.

## Etiquetas de wayfinder

Se crean una sola vez, si no existen:

```bash
gh label create wayfinder:map       --color 0E8A16 --description "Mapa de wayfinder"
gh label create wayfinder:research  --color 1D76DB --description "Ticket de investigación (AFK)"
gh label create wayfinder:grilling  --color 5319E7 --description "Ticket de entrevista (con humano)"
gh label create wayfinder:prototype --color D93F0B --description "Ticket de prototipo (con humano)"
gh label create wayfinder:task      --color FBCA04 --description "Ticket de trabajo manual"
```
