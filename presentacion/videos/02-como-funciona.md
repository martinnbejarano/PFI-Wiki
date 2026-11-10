# Video 02 — Cómo funciona

Archivo final: **`02 - Como funciona.mp4`**. Entrega: 10/11/2026.

**Duración: unos 3:30** (máximo 5:00). Una sola toma, sin cortes. Primera persona
singular, sin nombrar el proveedor de nube.

**Qué se ve:** arranca en la lámina 4 del deck (arquitectura) y sigue en Chrome con X y la
extensión. Cámara chica en una esquina.

## Los 2 casos (ya analizados, en la caché)

| Caso | Link | Qué muestra |
|---|---|---|
| **Verdadero** | https://x.com/somosbullmarket/status/2119892784651858306 | *Parece verificado*: el INDEC publica la inflación de octubre el jueves 12/11 |
| **Falso** | https://x.com/DaniMirin10/status/2120078179217838501 | *Contradicho por fuentes oficiales*: «la pobreza bajó a la mitad»; lo contradice el INDEC |

El falso es una respuesta: arriba aparece el tuit al que contesta. Bajá hasta el de
@DaniMirin10 antes de pedir el análisis y no abras su perfil.

---

## Antes de grabar (5 minutos)

- [ ] **No reinicies `make dev`.** La caché vive en la memoria del servicio: si se
      reinicia, los 2 casos tardan 8 a 16 segundos y el guion deja de coincidir.
- [ ] Abrí los 2 links en pestañas y comprobá que el veredicto aparece al instante.
- [ ] Una tercera pestaña con la *timeline* de X (`x.com/home`), para el tramo 2.
- [ ] El deck abierto en la lámina 4: `http://127.0.0.1:8777/factum.html#6`
      (con `presentacion/abrir.sh` corriendo), en pantalla completa.
- [ ] Zoom de Chrome al 125 %, pestañas con `.env` cerradas, «No molestar» activado.
- [ ] Cámara en una esquina que no tape el panel de evidencia.
- [ ] Un ensayo cronometrado: entre 3:15 y 4:00.

---

| # | Tramo | Pantalla | Tiempo | Acumulado |
|---|---|---|---|---|
| 1 | Apertura y escala | Deck, lámina 4 | 0:30 | 0:30 |
| 2 | La señal de BETO | X, *timeline* | 0:20 | 0:50 |
| 3 | Caso verdadero | X, caso 1 | 0:45 | 1:35 |
| 4 | Caso falso y su evidencia | X, caso 2 | 1:15 | 2:50 |
| 5 | Desglose | X, caso 2 | 0:30 | 3:20 |
| 6 | Puente | X, caso 2 | 0:10 | 3:30 |

## 1 · Apertura y escala — deck, lámina 4 · 0:30

Hola, soy Juan Martín Bejarano. Este es el segundo de 3 videos sobre Factum. En el
anterior mostré cómo se analiza un tuit; ahora lo muestro funcionando sobre X.

**🔒 DE MEMORIA — la escala:**

> La cifra que van a ver son las chances de que la afirmación sea verdadera, de 0 a 100.
> Más alto es mejor. Por encima de 34, parece verificado; de 30 para abajo, contradicho
> por fuentes oficiales; en el medio, información sospechosa.

*(Cambiás a la pestaña de la timeline.)*

## 2 · La señal de BETO — timeline · 0:20

*(Bajás despacio y señalás el indicador al pie de 2 o 3 publicaciones.)*

Esto es X con la extensión puesta. Sobre cada publicación aparece una señal del texto: es
el clasificador BETO, que corre sobre todo lo que hay en pantalla. Esa señal no es un
veredicto. El veredicto aparece al pedir el análisis.

## 3 · Caso verdadero — caso 1 · 0:45

*(Pasás a la pestaña del caso 1 y tocás «Verificar esta publicación».)*

Empiezo por uno verdadero. Al pedir el análisis, el sistema contrasta la afirmación con
fuentes oficiales, medios socios de ADEPA y verificadores, usando un LLM con búsqueda
restringida a esas fuentes. La primera vez tarda entre 8 y 16 segundos; este ya lo
analicé, así que sale al instante: un tuit viral se analiza una vez y se sirve a todos.

*(Leés el veredicto y la cifra.)* Parece verificado, y acá está la fuente oficial que lo
respalda.

## 4 · Caso falso y su evidencia — caso 2 · 1:15

*(Pasás a la pestaña del caso 2, bajás hasta el tuit de @DaniMirin10 y tocás «Verificar».)*

Ahora uno falso. Dice que la pobreza bajó a la mitad. *(Leés el veredicto y la cifra.)*
Contradicho por fuentes oficiales, y dice cuál: el INDEC.

*(Abrís el panel de evidencia.)* Este es el panel de evidencia. Cada fuente abre el
documento original. *(Abrís el informe del INDEC y volvés.)* No hace falta creerle al
número: se puede comprobar. Las fuentes oficiales pesan más que los medios.

*(Bajás hasta «Cómo se analiza».)* Y acá abajo, «Cómo se analiza»: contra qué fuentes se
contrasta, con el enlace al padrón de ADEPA. Los medios no los elijo yo: son los socios de
una asociación pública.

## 5 · Desglose — caso 2 · 0:30

*(Abrís «Cómo se llegó al resultado».)*

Esto conecta con la arquitectura del primer video. Acá se ve cada puntaje por separado: el
del texto, que es la señal de BETO, y el del contraste con fuentes, que es el que más
pesa. *(Señalás los valores.)* El combinador los pondera y de ahí sale la cifra de arriba.
Cuando X no deja ver los datos de la cuenta, ese módulo no se pronuncia y los otros se
reparten su peso.

## 6 · Puente — caso 2 · 0:10

En el último video les muestro qué resultados dio, si es viable como negocio y qué le
falta.

*(Dejá 1 segundo en silencio y cortá la grabación.)*
