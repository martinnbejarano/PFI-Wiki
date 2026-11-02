# Video 01 — Problema y propuesta

Archivo final: **`01 - Problema y propuesta.mp4`**. Entrega: 10/11/2026.

**Duración objetivo: 4:15** (máximo 5:00). Una sola toma, sin cortes. Unas 600 palabras
a ritmo de exposición.

**Qué se ve:** el deck (`presentacion/factum.html`) a pantalla completa, láminas 1 a 4 en
orden, con la cámara chica en una esquina. Se avanza con →.

**Reglas para los 3 videos:**

- Primera persona singular: «desarrollé», «elegí». Nunca «nosotros» ni «le damos».
- No se nombra el proveedor de nube ni su costo: va a cambiar antes de diciembre.
- Las cifras se dicen tal cual están acá. Si una no coincide con el documento, manda el
  documento.

| # | Tramo | Lámina | Tiempo | Acumulado |
|---|---|---|---|---|
| 1 | Apertura | 1 · Portada | 0:10 | 0:10 |
| 2 | Gancho | 1b · ¿Cuáles son verdad? | 0:20 | 0:30 |
| 3 | Problema | 2 · La verificación manual no escala | 0:30 | 1:00 |
| 4 | La respuesta | 2b · Los veredictos | 0:20 | 1:20 |
| 5 | Competencia | 3 · Qué lo distingue | 1:40 | 3:00 |
| 6 | Arquitectura | 4 · Cuatro módulos, un veredicto | 1:10 | 4:10 |
| 7 | Puente | 4 | 0:05 | 4:15 |

---

## 1 · Apertura — lámina 1 · 0:10

Hola, soy Juan Martín Bejarano. Este es el primero de 3 videos sobre Factum, mi Proyecto
Final de Ingeniería en Informática.

## 2 · Gancho — lámina 1b · 0:20

*(Dejá 2 segundos de silencio para que se lean las publicaciones.)*

Todos los días entramos a X para enterarnos de lo que pasa en el país: política,
economía. Y nos cruzamos con publicaciones como estas. ¿Cuáles son verdad? No lo sabemos.
Y casi nadie sale a chequearlo: lo que leemos ahí termina formando nuestra opinión, sea
cierto o no.

## 3 · Problema — lámina 2 · 0:30

El problema es de escala. En la Argentina hay 31 millones de usuarios de redes sociales, y
solo 3 de cada 10 confían en los medios. Y en X, una afirmación verdadera tarda unas 6
veces más que una falsa en llegar a 1.500 personas.

La verificación profesional es rigurosa, pero revisa de a una afirmación y casi siempre
después de que circuló. No le falta rigor: le falta escala.

## 4 · La respuesta — lámina 2b · 0:20

*(Vuelven las 6 publicaciones; esperá que aparezcan los veredictos.)*

Por eso desarrollé Factum: una extensión de Chrome que pone sobre cada publicación de X un
veredicto con sus fuentes. Las 6 de recién: 3 son verdad y 3 son falsas, y cada una dice
con qué fuente se comprobó. No entrega un número solo: entrega el número y el camino para
comprobarlo.

## 5 · Competencia — lámina 3 · 1:40

*(Arriba está la curva de valor; abajo, los 3 diferenciales. Señalá la curva primero.)*

Antes de construirlo, comparé lo que ya existe. En esta curva, cada línea es una
herramienta y cada columna, una capacidad: la línea gruesa es Factum.

Chequeado es la referencia en verificación profesional: tiene la evidencia más sólida,
pero es manual, así que no llega a la velocidad ni al volumen de X. Grok, la inteligencia
artificial de X, es automática y rápida, pero hay que invocarla publicación por
publicación y no muestra el documento de origen. Y las Notas de la Comunidad, el sistema
de X en el que los usuarios agregan contexto, dependen del consenso entre ellos.

De esa comparación salen 3 diferenciales.

El primero es la evidencia: cada veredicto enlaza el documento de origen, el INDEC o el
Boletín Oficial, y no una nota de otro medio.

El segundo es el alcance. Las Notas de la Comunidad llegan tarde y a pocas publicaciones:
solo el 16,9 % de las publicaciones con una nota propuesta llega a mostrarla, y la mitad lo
hace con más de 23 horas de demora, cuando la publicación ya circuló. Esa demora no es de
cómputo, es humana: hace falta que usuarios que suelen estar en desacuerdo coincidan.
Factum, en cambio, da una señal sobre todas las publicaciones que el usuario tiene en
pantalla, con fuentes argentinas. No reemplaza a las Notas: las complementa en todo lo que
no es viral.

El tercero es el acceso. Las herramientas automáticas, como Cyabra o Blackbird.AI, se
venden con licencias para empresas y gobiernos, y NewsGuard cobra 8 dólares por mes y no
cubre la Argentina. Factum es gratis para el ciudadano.

La solución más parecida es InTruth, una extensión gratuita de este año, pero verifica el
audio de debates contra la web abierta, no el texto de X.

## 6 · Arquitectura — lámina 4 · 1:10

Así se analiza un tuit, de izquierda a derecha. La extensión lo toma de X y se lo manda a
una API, que lo reparte en 3 módulos en paralelo.

El primero es un clasificador basado en BETO, un modelo de lenguaje preentrenado en
español, al que le hice *fine-tuning* en 2 etapas: primero con un corpus académico de
noticias falsas y después con afirmaciones verificadas por Chequeado. Lee solo el texto y
detecta cómo está escrito: lenguaje de alarma, mayúsculas, urgencia. Pesa 25 %, porque el
estilo acompaña a la desinformación, pero no la prueba.

El segundo mira señales públicas de la cuenta: antigüedad, seguidores y verificación.
Pesa solo 10 %, porque esas señales se compran.

El tercero, el que más pesa, con 65 %, contrasta la afirmación con fuentes oficiales, con
los medios socios de ADEPA y con verificadores, usando un LLM con búsqueda web restringida
a esas fuentes. Abajo, una ingesta programada mantiene al día el índice de fuentes
oficiales.

El cuarto, el combinador, junta los 3 resultados en un veredicto con su fuente, que vuelve
a la extensión.

## 7 · Puente — lámina 4 · 0:05

En el próximo video lo muestro funcionando sobre X.

*(Dejá 1 segundo en silencio y cortá la grabación.)*

---

## Antes de grabar

- [ ] Abrir el deck con `presentacion/abrir.sh` y dejarlo en la lámina 1. Ocultar el
      cursor y las barras del navegador (pantalla completa).
- [ ] Cámara chica abajo a la derecha, sin tapar texto de las láminas 3 y 4 (probarlo
      antes en esas 2).
- [ ] «No molestar» activado, notificaciones de Slack y WhatsApp cerradas.
- [ ] Ensayo cronometrado en voz alta: tiene que dar entre 4:00 y 4:30. Si da más,
      recortá en el tramo 5 el párrafo de InTruth.
- [ ] Revisar la grabación completa antes de darla por buena: audio, que no se corte
      la última frase y que la cámara no tape nada.
