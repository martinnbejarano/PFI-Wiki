# 02 · ¿El UUID de la extensión llega al servidor?

Type: grilling
Status: open
Blocked by: —

## Question

La decisión 2 dice «extensión ciudadana **anónima** con UUID en el almacenamiento local del navegador». Pero **RF-15** compromete que el panel web muestre «el histórico de los análisis solicitados desde su instalación», y eso solo funciona si el servidor sabe qué análisis pertenecen a qué instalación. Lo mismo con **RF-17**, el reporte de falso positivo.

Si el UUID viaja, deja de ser almacenamiento local y pasa a ser un identificador persistente de dispositivo del lado servidor. El propio `restricciones-legales-eticas.md` lista las *cookies* como dato personal en su línea 23, así que la etiqueta «anónima» no se sostiene sola.

Hay que decidir:

1. ¿El UUID se envía en cada consulta, o el histórico se arma del lado del cliente sin que el servidor lo sepa?
2. Si se envía: ¿existe la entidad `usuario_extension` con filas por instalación, y qué guarda además del UUID?
3. Si no se envía: ¿RF-15 y CU-05 sobreviven, se reducen a un histórico local, o se caen?
4. ¿Cambia la respuesta para el reporte de falso positivo, que necesita evitar el envío repetido del mismo usuario?

**Por qué bloquea el esquema.** Define si `usuario_extension` existe, y si existe, si la base contiene una segunda categoría de datos personales —la del propio usuario del producto— además de la de los autores de los tuits. Son defensas legales distintas: el art. 5.2.b no ampara al usuario de la extensión, que sí requiere consentimiento informado.

**Recomendación de partida.** El UUID viaja, `usuario_extension` existe, y la defensa deja de ser «no hay datos personales» —que es falso— para pasar a ser «hay consentimiento informado en el momento de instalar, y el dato es un identificador sin vínculo con una persona». Es menos cómodo de decir y mucho más difícil de refutar.
