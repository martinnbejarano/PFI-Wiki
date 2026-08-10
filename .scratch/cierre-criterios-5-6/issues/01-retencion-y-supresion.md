# 01 · Retención y supresión del `@` en claro

Type: grilling
Status: resolved
Blocked by: —

## Question

La decisión 3 del bloque de diseño persiste el `@` del autor sin hashear, y eso es lo que habilita el Módulo 2 y el corpus argentino de la Entrega 4. La defensa de la **recolección** ya está elegida (art. 5 inc. 2.b de la Ley 25.326: fuentes de acceso público irrestricto). Falta lo que viene después de recolectar, que el archivo legal actual no toca en ninguna parte:

1. **Art. 4 inc. 7** — los datos deben destruirse cuando dejan de ser necesarios para la finalidad. ¿Cuál es la finalidad declarada, cuánto tiempo se conserva el `@` en claro, y qué pasa al vencer el plazo: borrado, hasheo, o nada porque la finalidad no vence?
2. **Art. 16** — derecho de rectificación y supresión. ¿El sistema ofrece un mecanismo para que el titular de una cuenta pida que sus tuits salgan del corpus? ¿Por qué canal, y qué borra exactamente —el `@`, las filas, o también el análisis derivado—?
3. ¿La conservación del análisis y de la evidencia sigue el mismo plazo que la conservación del `@`, o son dos políticas distintas?

**Por qué bloquea el esquema.** Cada respuesta es una columna o una tabla: un plazo obliga a `fecha_captura` más una política de purga; un mecanismo de supresión obliga a poder resolver todas las filas de un `@` y a decidir si queda una tumba (`cuenta_suprimida`) para no volver a capturarla.

**Recomendación de partida.** Finalidad declarada de investigación con conservación mientras el PFI esté vigente; supresión atendida a pedido por correo, borrando el `@` y dejando el texto y el análisis, que sin autor dejan de ser dato personal. Es lo defendible con el menor costo de implementación — pero decidilo vos.

## Answer

Resuelto el 2026-08-10.

**1 · Retención: sin plazo, con finalidad declarada.** No se fija un plazo de destrucción. La postura es que el art. 4 inc. 7 obliga a destruir «cuando hayan dejado de ser necesarios o pertinentes», y no impone un reloj: mientras la finalidad declarada subsista, la necesidad subsiste. La finalidad hay que enunciarla estrecha para que el argumento cierre —investigación y entrenamiento del clasificador, más el historial agregado de cuenta que el Módulo 2 necesita para puntuar credibilidad—, porque una finalidad amplia hace que nunca venza nada y eso es justamente lo que el artículo quiere evitar.

Lo que hace defendible la postura no es el argumento sino lo que la acompaña: existe un canal de supresión que funciona (punto 2) y la disociación es real (punto 3). Retención indefinida sin canal de supresión no se sostiene; con canal, sí.

**Dónde queda expuesta, dicho sin adornos.** El art. 21 exige declarar, entre sus nueve requisitos, el tiempo de conservación. Si la base llega a inscribirse, «indefinido» hay que escribirlo en un formulario y es lo primero que un revisor mira. Esa exposición depende del ticket 12: si la extensión no se publica, no hay inscripción y la pregunta no llega a formularse. Las dos decisiones se sostienen juntas.

**Consecuencia buena, colateral:** sin plazo no hay purga programada, así que no aparece un planificador de tareas en el ticket 09 ni un servicio más en el diagrama de despliegue.

**2 · Canal de supresión: correo, a mano, cinco días hábiles.** Es el plazo del art. 16. Se publica en el *popup* de la extensión y en el panel web. No se construye formulario ni verificación de titularidad: para el volumen de un prototipo, atenderlo a mano es proporcionado y es lo que la ley pide.

**3 · Qué borra la supresión: el `@` y los metadatos de cuenta.** El texto del tuit y el análisis sobreviven disociados. Sin autor no identifican a nadie, así que salen del alcance de la ley.

**4 · Análisis y evidencia: sin plazo, una vez disociados.** Es lo que hace viable el corpus argentino de la Entrega 4. La evidencia, además, nunca fue dato personal del autor: son enlaces y textos de medios y de fuentes oficiales.

---

### Lo que esto le entrega al ticket 06

**Columnas y estructura:**

- `cuenta` necesita marcar la supresión, no solo vaciar campos: un `suprimida` booleano con `fecha_supresion`, para que el sistema no vuelva a enriquecer esa fila la próxima vez que aparezca el mismo tuit.
- No hace falta `fecha_purga` ni política de retención en ninguna tabla. No hay reloj.
- No hace falta lista de exclusión.

**Dos agujeros que la disociación abre y que hay que resolver en el ticket 06, porque si no la anonimización es de mentira:**

1. **La URL del tuit contiene el `@`.** `x.com/usuario/status/123` reidentifica al autor con solo mirarla. Borrar `cuenta.handle` y dejar `tuit.url` intacta no anonimiza nada. O la URL se reconstruye desde el identificador nativo —que funciona: `x.com/i/status/123` redirige—, o se borra junto con el `@`.
2. **El identificador nativo del tuit permite recuperar el `@` consultando X.** La disociación es reversible por cualquiera que tenga la fila. Es una tensión real y no tiene salida limpia: ese identificador es lo que hace reproducible el análisis meses después, que es lo que exige el trabajo experimental de la Entrega 5. Hay que elegir y escribir la elección; ocultarla es peor que resolverla mal.

**Para el ticket 08:** la finalidad declarada, el plazo del art. 16 y la dirección de contacto son texto del apartado legal. El punto de la reversibilidad del identificador nativo va escrito y no omitido — un análisis legal que reconoce su propio límite vale más que uno que lo tapa.
