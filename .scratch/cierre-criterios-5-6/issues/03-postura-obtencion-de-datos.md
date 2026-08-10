# 03 · Postura sobre las tres formas de obtener datos

Type: grilling
Status: open
Blocked by: —

## Question

El archivo legal dice hoy, en su tabla de la línea 95, que el *scraping* sin permiso hay que **evitarlo**, y en la 93 recomienda usar la API oficial de Twitter. El diseño hace otra cosa, y en tres modalidades distintas que el archivo no distingue:

1. **Lectura del DOM por la extensión.** No es *scraping* de servidor ni uso de API: es el propio usuario, ya autenticado, mirando su *timeline*, y un programa que él instaló leyendo lo que su pantalla ya muestra. Es la modalidad más defendible y el archivo no la contempla.
2. **Scraping de sitios `.gob.ar`.** `recursos.md` planifica seis: Infoleg, INDEC, Casa Rosada, ANMAT, BCRA y Chequeado. Los cinco primeros son información pública del Estado.
3. **Chequeado.** Está en la misma lista pero **no** es un organismo público: es una ONG con contenido propio y ToS propios. El archivo, en su línea 96, dice «negociar con el equipo» y eso nunca se hizo.

Hay que fijar una postura por modalidad, y decidir además:

- ¿Se sostiene todavía la recomendación de pedir acceso a la API de Twitter, o queda formalmente descartada? Hoy el archivo la recomienda y el diseño no la usa.
- ¿Qué se hace con Chequeado: escribirles, limitarse al `robots.txt` y a la cita con enlace, o sacarlo del alcance del prototipo?
- ¿La Ley 11.723 permite almacenar el texto completo del tuit, o solo procesarlo? La línea 53 del archivo dice que publicar un *dataset* de mil *posts* necesita permiso, y el corpus argentino de la Entrega 4 es exactamente eso.

**Recomendación de partida.** Separar las tres modalidades explícitamente —es lo que le da fuerza al argumento—, descartar la API de Twitter por escrito, y con Chequeado quedarse en el uso citado con enlace sin redistribuir el texto, dejando el contacto como trabajo futuro.
