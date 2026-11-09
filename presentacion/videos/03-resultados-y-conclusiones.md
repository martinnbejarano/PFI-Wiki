# Video 03 — Resultados y conclusiones

Archivo final: **`03 - Resultados y conclusiones.mp4`**. Entrega: 10/11/2026.

**Duración objetivo: 4:30** (máximo 5:00). Una sola toma, sin cortes.

**Cifras:** las del documento entregado el 24/10 (decisión del 09/11). No se nombra el
proveedor de nube ni el plan de USD 20 para individuos: ninguno de los dos está en el
documento.

**Qué se ve:** el deck con solo 5 láminas, en el orden del video. Con `abrir.sh` corriendo,
abrir en Chrome:

```
http://127.0.0.1:8777/factum.html?laminas=17,18,8,9,10
```

Quedan, en orden: modelos y matriz de confusión (R7), pruebas (R8), negocio (6),
limitaciones y trabajo futuro (7) y Gracias. Se avanza con →. Cámara chica en una esquina.

| # | Tramo | Lámina | Tiempo | Acumulado |
|---|---|---|---|---|
| 1 | Apertura | R7 · Modelos y matriz | 0:10 | 0:10 |
| 2 | Resultados del modelo | R7 · Modelos y matriz | 1:10 | 1:20 |
| 3 | Pruebas y requerimientos | R8 · Pruebas | 0:40 | 2:00 |
| 4 | Negocio | 6 · El ciudadano no paga | 1:20 | 3:20 |
| 5 | Limitaciones y trabajo futuro | 7 · Lo que el sistema todavía no ve | 1:00 | 4:20 |
| 6 | Cierre | 8 · Gracias | 0:10 | 4:30 |

---

## 1 · Apertura — R7 · 0:10

Hola, soy Juan Martín Bejarano. Este es el último de 3 videos sobre Factum: cómo lo
evalué, si es viable y qué le falta.

## 2 · Resultados del modelo — R7 · 1:10

*(Señalá la tabla de arriba.)*

Comparé 5 modelos sobre un corpus académico de noticias en español. BETO fue el mejor,
con un F1 de 0,76. Pero sobre 94 tuits argentinos verificados cae a 0,42: el corpus es de
México y España, y anterior a 2022. Con una segunda etapa de *fine-tuning* sobre
afirmaciones de Chequeado sube a 0,52. Por eso el clasificador pesa solo 25 %: lo que
levanta el resultado es el contraste con fuentes. El sistema completo llega a 0,712, con
un intervalo de 0,61 a 0,80. La meta era 0,75 y no se alcanzó.

*(Señalá la matriz.)*

Lo que sí se cumple es lo que más me importaba: de las 46 publicaciones verdaderas,
ninguna salió como falsa. Prioricé no acusar a quien dice la verdad. El costo es que de
las 48 falsas detecta 23. Y una advertencia: Chequeado apareció como fuente en 78 de los
94 análisis, así que este valor sobreestima el desempeño ante desinformación nueva.

## 3 · Pruebas y requerimientos — R8 · 0:40

El servicio tiene 137 pruebas automatizadas con 93 % de cobertura, la extensión 27, y los
7 casos de uso pasaron sus pruebas funcionales. La usabilidad dio un SUS de 74 sobre una
meta de 68, con 3 participantes: es un indicio, no una prueba.

Hay 2 metas que no se cumplen y las declaro: el F1, que ya vimos, y la latencia del
análisis profundo, 16 segundos en el percentil 95 contra una meta de 8, porque la
búsqueda web del proveedor ya se lleva unos 7.

## 4 · Negocio — lámina 6 · 1:20

El modelo tiene 2 lados. El ciudadano no paga: la extensión es gratis, con 5 análisis
nuevos por mes. Pagan las organizaciones: medios y verificadores, con una API desde 200
dólares por mes, y observatorios, con un panel de tendencias de 300.

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

## 5 · Limitaciones y trabajo futuro — lámina 7 · 1:00

**🔒 DE MEMORIA — las limitaciones:**

> El sistema tiene límites que declaro. El puntaje mide cuánto respalda la evidencia a la
> afirmación, no si es verdadera, porque la verdad no admite grados: si una afirmación
> mezcla una parte verdadera con una falsa, es falsa, pero el promedio puede dejarla en el
> medio. Si la fuente oficial se equivoca, el sistema hereda el error. Y analiza una sola
> afirmación por tuit.

Hay 3 líneas de trabajo futuro. Primero, los datos verdaderos que engañan: un dato real
sin el contexto que lo contradice, o un contenido viejo que recircula como nuevo. Segundo,
analizar imágenes, porque mucha desinformación circula como captura. Y tercero, analizar
todas las afirmaciones de un tuit: si una es falsa, el tuit queda marcado como falso.

## 6 · Cierre — lámina 8 · 0:10

*(Pasás a Gracias.)*

**🔒 DE MEMORIA — el cierre:**

> El objetivo no es que el usuario le crea al veredicto, sino que pueda prescindir de él.
> Por eso el sistema le entrega el camino hacia la evidencia, no solamente la conclusión.
> Gracias.

*(Dejá 1 segundo en silencio y cortá la grabación.)*

---

## Antes de grabar

- [ ] `presentacion/abrir.sh` y después abrir la URL con `?laminas=17,18,8,9,10`. Comprobar
      que la primera lámina es «Modelos y matriz de confusión» y la última, Gracias.
- [ ] Pantalla completa, cámara chica que no tape la matriz de R7 ni la tabla de R8.
- [ ] «No molestar» activado.
- [ ] Ensayo cronometrado: entre 4:15 y 4:45. Si da más, recortá en el tramo 4 la
      composición de los USD 1.716.
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
