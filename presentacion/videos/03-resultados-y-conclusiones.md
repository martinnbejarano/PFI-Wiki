# Video 03 — Resultados y conclusiones

Archivo final: **`03 - Resultados y conclusiones.mp4`**. Entrega: 10/11/2026.

**Duración objetivo: 4:50** (máximo 5:00). Una sola toma, sin cortes.

**Cifras:** las del documento entregado el 24/10 (decisión del 09/11). No se nombra el
proveedor de nube ni el plan de USD 20 para individuos: ninguno de los dos está en el
documento.

**Qué se ve:** el deck con solo 4 láminas, en el orden del video. Con `abrir.sh` corriendo,
abrir en Chrome:

```
http://127.0.0.1:8777/factum.html?laminas=21,8,9,10
```

Quedan, en orden: resultados (la lámina corta hecha para este video), negocio (6),
limitaciones y trabajo futuro (7) y Gracias. Se avanza con →. Cámara chica en una esquina.

| # | Tramo | Lámina | Tiempo | Acumulado |
|---|---|---|---|---|
| 1 | Apertura | Resultados | 0:10 | 0:10 |
| 2 | Resultados | Resultados | 1:15 | 1:25 |
| 3 | Negocio | 6 · El ciudadano no paga | 1:45 | 3:10 |
| 4 | Limitaciones y trabajo futuro | 7 · Lo que el sistema todavía no ve | 1:25 | 4:35 |
| 5 | Cierre | 8 · Gracias | 0:15 | 4:50 |

---

## 1 · Apertura — Resultados · 0:10

Hola, soy Juan Martín Bejarano. Este es el último de 3 videos sobre Factum: qué
resultados dio, si es viable y qué le falta.

## 2 · Resultados — Resultados · 1:15

Empiezo por el clasificador. BETO es un modelo de lenguaje ya preentrenado en español, y
le hice *fine-tuning* en 2 etapas. Primero, con un corpus académico de 971 noticias
verdaderas y falsas de México y España: ahí llegó a un F1 de 0,76. Pero el español de X
argentino es otro, así que hice una segunda etapa con 2.107 afirmaciones verificadas por
Chequeado.

Después evalué todo sobre 94 tuits argentinos ya verificados. BETO, con la primera etapa,
llega a 0,42, y con la segunda, a 0,52. El sistema completo, con el contraste de fuentes,
llega a 0,712: no alcanza la meta de 0,75, pero muestra que lo que sostiene el resultado
es la evidencia, no el estilo del texto.

Y se cumple lo que más me importaba: de las 46 publicaciones verdaderas, ninguna salió
como falsa. Prioricé no acusar a quien dice la verdad. Una advertencia: Chequeado fue
fuente en 78 de los 94 análisis, así que el valor sobreestima el desempeño ante
desinformación nueva.

## 3 · Negocio — lámina 6 · 1:45

*(Señalá las 2 cajas de arriba.)*

El modelo tiene 2 lados. El ciudadano no paga: la extensión es gratis, con 5 análisis
nuevos por mes. Es una decisión, no un descuido: si el ciudadano tuviera que pagar para
saber si algo es falso, la herramienta llegaría solo a quien ya desconfía. Y la adopción
gratuita es lo que genera el valor que se vende después.

Pagan las organizaciones. El cliente ideal es un medio o un verificador que necesita
chequear en volumen: la API arranca en 200 dólares por mes con 5.000 consultas. Los
observatorios pagan 300 por el panel de tendencias, que muestra qué desinformación circula
sobre un tema. Cada cuota está calculada para que el margen siga positivo aunque el
cliente la use entera.

*(Señalá los 3 números.)*

Lo evalué a 5 años, con impuestos y cargas sociales, a una tasa del 25 %, en 3
escenarios. En el neutral, el más probable, el VAN es de 63.935 dólares, la TIR de 72,6 %
y la inversión se recupera en 2,9 años. En el pesimista pierde 94.162 dólares. La
encuesta mide intención de uso, no adopción, y el pesimista es justamente el caso en que
los ciudadanos no adoptan la extensión: sin adopción no hay ventas a organizaciones.

Por eso el financiamiento va en 2 tramos. Al inicio, 1.716 dólares de fondos propios, que
cubren dominio, registro de marca y la asesoría legal para constituir la sociedad. Después,
hasta 52.694 dólares de inversores ángeles, y el segundo tramo se pide solo si la adopción
llega a la del neutral. Si no llega, el proyecto se corta y la pérdida queda acotada. La
variable que más pesa es el precio de la API, y todavía no está validado con clientes.

Lo que sostiene los costos son 2 palancas: el tope de 5 análisis por mes y la caché,
porque un tuit viral se analiza una vez y se sirve a todos.

## 4 · Limitaciones y trabajo futuro — lámina 7 · 1:25

**🔒 DE MEMORIA — las limitaciones:**

> El sistema tiene límites que declaro. El puntaje mide cuánto respalda la evidencia a la
> afirmación, no si es verdadera, porque la verdad no admite grados: si una afirmación
> mezcla una parte verdadera con una falsa, es falsa, pero el promedio puede dejarla en el
> medio. Si la fuente oficial se equivoca, el sistema hereda el error. Y analiza una sola
> afirmación por tuit.

Un ejemplo: un tuit que cita bien un dato del INDEC y le agrega una conclusión falsa. Si el
sistema toma el dato, lo da por verificado, y el tuit en su conjunto es falso. Por eso la
cifra no se presenta como la verdad, sino junto con la fuente para que cada uno la revise.
Y las fuentes no las elijo yo: son los organismos oficiales y el padrón público de ADEPA.

Hay 3 líneas de trabajo futuro. Primero, los datos verdaderos que engañan: un dato real
sin el contexto que lo contradice, o un contenido viejo que recircula como nuevo. Segundo,
analizar imágenes, porque mucha desinformación circula como captura. Y tercero, analizar
todas las afirmaciones de un tuit: si una es falsa, el tuit queda marcado como falso.

## 5 · Cierre — lámina 8 · 0:15

*(Pasás a Gracias.)*

**🔒 DE MEMORIA — el cierre:**

> El objetivo no es que el usuario le crea al veredicto, sino que pueda prescindir de él.
> Por eso el sistema le entrega el camino hacia la evidencia, no solamente la conclusión.
> Gracias.

*(Dejá 1 segundo en silencio y cortá la grabación.)*

---

## Antes de grabar

- [ ] `presentacion/abrir.sh` y después abrir la URL con `?laminas=21,8,9,10`. Comprobar
      que la primera lámina es «Lo que sostiene el resultado es el contraste» y la
      última, Gracias.
- [ ] Pantalla completa, cámara chica que no tape los números de la lámina de resultados
      ni los del negocio.
- [ ] «No molestar» activado.
- [ ] Ensayo cronometrado: entre 4:30 y 4:55. Si da más, recortá en el tramo 3 el
      párrafo de las 2 palancas de costo.
- [ ] Repasar las cifras: **1.716** (no 1.300), **72,6 %** (no 74), **52.694**.

---

## Entrega (10/11)

1. Nombres: `01 - Problema y propuesta.mp4`, `02 - Como funciona.mp4`,
   `03 - Resultados y conclusiones.mp4`. QuickTime graba `.mov`: convertir a mp4.
2. Comprimir para que los 3 entren en el mail (Outlook, unos 20 MB en total):

   ```bash
   ffmpeg -i entrada.mov -vf "scale=-2:720,fps=24" -c:v libx264 -crf 30 -preset slow \
     -c:a aac -b:a 64k -ac 1 "01 - Problema y propuesta.mp4"
   ```

   Si no entran, subir `-crf` a 32 o 34 y revisar que el texto de las láminas se lea.
3. Subir los 3 a YouTube como **no listados** (o a Drive con «cualquier persona con el
   enlace»), y probar cada link en una ventana de incógnito.
4. Documento con los 3 links, en orden, adjunto al mail.
5. Mail a `PFI_Inf_Docentes@uade.edu.ar`, CC al tutor (fgirouribazo@uade.edu.ar). Asunto
   con el formato `[E90 PFI - <código del curso> Curso 551221 - Bejarano][Entrega de videos - PFI 2026]`;
   confirmar el código del curso (en el ejemplo, «MAR»).
