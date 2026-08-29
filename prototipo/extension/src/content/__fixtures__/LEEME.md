# Fixtures del lector del DOM de X

Estos archivos son la entrada de las pruebas de `../lector-dom.test.ts`. Cada uno contiene
el `outerHTML` de un único `article[data-testid="tweet"]` tal como X lo emite en el
*timeline*.

## Anonimización

Los fixtures capturados de X real se guardan **anonimizados**: el *handle*, el nombre
visible y el identificador nativo se reemplazan por valores ficticios verosímiles, y la
estructura del marcado —que es lo único que la prueba necesita— queda intacta. Un
repositorio académico no debe señalar cuentas reales, y el propio documento del PFI se
compromete a eso en su apartado ético.

Cada archivo declara en su encabezado si fue capturado y anonimizado, o si es de
fabricación propia.

Los valores de reemplazo están fijados de antemano, en la constante `ANONIMOS` de
`../lector-dom.test.ts`, para que la prueba pueda comprobar el valor exacto en lugar de
conformarse con la forma. Quien coloque un fixture reemplaza **todas** las apariciones del
*handle* y del identificador reales por estos:

| Archivo | *Handle* | Identificador nativo |
|---|---|---|
| `tuit-normal.html` | `@cuenta_ejemplo` | `1900000000000000001` |
| `tuit-con-cita.html` (tuit que cita) | `@cuenta_citadora` | `1900000000000000002` |
| `tuit-con-cita.html` (tuit citado) | `@cuenta_citada` | `1900000000000000003` |
| `tuit-con-multimedia.html` | `@cuenta_multimedia` | `1900000000000000004` |

El nombre visible se reemplaza por uno ficticio cualquiera. Las URL de las imágenes de
perfil y de la multimedia pueden dejarse como están o apuntarse a cualquier lado: el nodo
se analiza sin red y ninguna prueba las descarga.

## Archivos

| Archivo | Origen | Estado |
|---|---|---|
| `tuit-normal.html` | Captura de X real, anonimizada | **Falta** |
| `tuit-con-cita.html` | Captura de X real, anonimizada | **Falta** |
| `tuit-con-multimedia.html` | Captura de X real, anonimizada | **Falta** |
| `nodo-malformado.html` | Fabricación propia | Presente |

Los tres primeros no pudieron capturarse: X rechaza la sesión automatizada con el aviso
sobre extensiones de privacidad. Las pruebas que dependen de ellos están en un bloque
`describe.skip` en `../lector-dom.test.ts`; al colocar los archivos se quita el `.skip` y
las pruebas corren.

El nodo malformado sí es de fabricación propia, y eso es legítimo: representa un artículo
que no tiene la forma esperada, y lo que se prueba es justamente que el lector lo saltee
en lugar de romper la extensión. Fabricar los otros tres y presentarlos como capturas de X
sería falsear la evidencia del entregable.

## Cómo se captura uno

Con la sesión de X abierta en el navegador, sobre `https://x.com/home`, en la consola:

```js
copy(document.querySelectorAll('article[data-testid="tweet"]')[0].outerHTML);
```

Después se pega en el archivo correspondiente, se antepone el comentario de encabezado y
se reemplazan el *handle*, el nombre visible y el identificador del tuit.
