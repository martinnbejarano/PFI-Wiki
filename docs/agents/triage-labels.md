# Etiquetas de triage

Las *skills* hablan en términos de cinco roles canónicos. Esta tabla los mapea a las cadenas de etiqueta que realmente usa el *tracker* de este repo.

| Rol en mattpocock/skills | Etiqueta en este repo | Significado |
| --- | --- | --- |
| `needs-triage` | `needs-triage` | Hay que evaluar el *issue* |
| `needs-info` | `needs-info` | Esperando más información de quien lo reportó |
| `ready-for-agent` | `ready-for-agent` | Completamente especificado, listo para un agente sin supervisión |
| `ready-for-human` | `ready-for-human` | Requiere trabajo humano |
| `wontfix` | `wontfix` | No se va a hacer |

Cuando una *skill* menciona un rol —por ejemplo, «aplicar la etiqueta de listo para agente»— se usa la cadena de la columna del medio.

Se mantuvieron los nombres por defecto: el repositorio no tenía ninguna etiqueta creada, así que no había vocabulario previo con el que chocar. Para cambiarlos, editar la columna del medio.

Las etiquetas se crean en GitHub la primera vez que `/triage` las necesite:

```bash
gh label create needs-triage    --color D93F0B
gh label create needs-info      --color FBCA04
gh label create ready-for-agent --color 0E8A16
gh label create ready-for-human --color 1D76DB
gh label create wontfix         --color CCCCCC
```
