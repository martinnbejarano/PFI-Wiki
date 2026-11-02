# Video 02 — Cómo funciona

Archivo final: **`02 - Como funciona.mp4`**. Entrega: 10/11/2026.

**Duración objetivo: 4:00** (máximo 5:00). Una sola toma, sin cortes, con la demo **en
vivo** sobre X.

**Qué se ve:** arranca en la lámina 4 del deck (la arquitectura del video 1), pasa a Chrome
con X y la extensión, y termina en Chrome. La cámara chica sigue en una esquina.

Mismas reglas que el video 1: primera persona singular, sin nombrar el proveedor de nube,
cifras tal cual.

| # | Tramo | Pantalla | Tiempo | Acumulado |
|---|---|---|---|---|
| 1 | Apertura y escala | Deck, lámina 4 | 0:30 | 0:30 |
| 2 | La señal de BETO | Chrome, X | 0:20 | 0:50 |
| 3 | Caso falso en caché | Chrome, X | 0:40 | 1:30 |
| 4 | Caso nuevo en vivo | Chrome, X | 1:30 | 3:00 |
| 5 | Desglose | Chrome, X | 0:45 | 3:45 |
| 6 | Puente | Chrome, X | 0:10 | 3:55 |

---

## Los casos (elegirlos el día de la grabación)

Anotar acá los links antes de grabar. Que sean datos, no opiniones, y preferir cuentas
institucionales o medios a personas.

1. **Falso, en caché:** un tuit que el sistema marque *contradicho por fuentes oficiales*,
   con una fuente oficial enlazada. Ideal: el de empleados públicos frente a privados
   registrados de la lámina 1b (SIPA: unos 6,2 millones de asalariados privados
   registrados contra 3,4 millones públicos). Probarlo antes: si no lo contradice con una
   fuente oficial, usar otro.
   Link: ____________________
2. **Nuevo, en vivo:** un tuit con una cifra económica del día que nadie haya analizado.
   Link: ____________________
3. **Nuevo, de reserva:** otro candidato por si el 2 no extrae afirmación.
   Link: ____________________

---

## 1 · Apertura y escala — deck, lámina 4 · 0:30

Hola, soy Juan Martín Bejarano. Este es el segundo de 3 videos sobre Factum. En el
anterior mostré cómo se analiza un tuit; ahora lo muestro funcionando sobre X.

**🔒 DE MEMORIA — la escala, antes de cualquier número:**

> La cifra que van a ver son las chances de que la afirmación sea verdadera, de 0 a 100.
> Más alto es mejor. Por encima de 34, parece verificado; de 30 para abajo, contradicho
> por fuentes oficiales; en el medio, información sospechosa.

*(Cambiás a Chrome con X abierto, en la *timeline*.)*

## 2 · La señal de BETO — X · 0:20

*(Señalá el indicador al pie de 2 o 3 publicaciones mientras bajás despacio.)*

Esto es X con la extensión puesta. Sobre cada publicación aparece una señal del texto: es
el clasificador BETO, que corre sobre todo lo que hay en pantalla. Esa señal no es un
veredicto. El veredicto aparece al pedir el análisis.

## 3 · Caso falso en caché — X · 0:40

*(Abrís el caso 1.)*

Este es un caso que ya analicé, así que resuelve al instante: un tuit viral se analiza una
vez y se sirve a todos. *(Pedís el análisis.)* Contradicho por fuentes oficiales. Y acá
dice cuál: *(señalás la fuente)* el dato oficial que lo contradice, enlazado. No hace falta
creerle al número: se puede abrir el documento y comprobarlo.

## 4 · Caso nuevo en vivo — X · 1:30

*(Abrís el caso 2 y pedís el análisis.)*

Ahora uno nuevo, que nadie analizó. Mientras corre, les cuento qué está pasando: la
extensión le mandó el tuit a la API. En paralelo, BETO lee el texto, se miran las señales
públicas de la cuenta, y un LLM extrae la afirmación y la busca solo en fuentes oficiales,
medios socios de ADEPA y verificadores. Al LLM le llega el texto, nunca la cuenta autora. Este es el
análisis profundo, el que tarda entre 8 y 16 segundos.

*(Llega el resultado. Lo leés en voz alta: veredicto y cifra.)*

*(Abrís el panel de evidencia.)* Este es el panel de evidencia. Cada fuente abre el
documento original *(abrís uno y volvés)*. Las fuentes oficiales pesan más que los medios.

*(Bajás hasta «Cómo se analiza».)* Y acá abajo, «Cómo se analiza»: contra qué fuentes se
contrasta, con el enlace al padrón de ADEPA. Los medios no los elijo yo: son los socios de
una asociación pública.

### Plan B, sin cortar la toma

- **Si el caso 2 no extrae una afirmación:** «Este no tiene una afirmación verificable, y
  el sistema lo dice en lugar de inventar un veredicto. Pruebo con otro.» → caso 3.
- **Si tarda más de 25 segundos o da error:** «La búsqueda depende de un servicio externo;
  cuando falla, el sistema entrega un análisis parcial identificado como tal. Sigo con el
  caso anterior.» → volvés al caso 1 y hacés el panel de evidencia y el desglose sobre él.
- **Si falla todo antes de empezar** (X no carga, el servicio no responde): no grabes.
  Arreglalo y empezá la toma de nuevo.

## 5 · Desglose — X · 0:45

*(En el mismo caso, abrís «Cómo se llegó al resultado».)*

Y esto conecta con la arquitectura del primer video. «Cómo se llegó al resultado» muestra
los 3 puntajes por separado: el del texto, que es la señal de BETO; el de la cuenta; y el
del contraste con fuentes, que es el que más pesa. *(Leés los 3 valores.)* El combinador
los pondera, 25, 10 y 65 %, y de ahí sale la cifra de arriba. Si el contraste no encuentra
evidencia, el resultado lo dice: «sin contraste externo», y no se presenta como verificado.

## 6 · Puente — X · 0:10

En el último video les muestro cómo lo evalué, qué resultados dio, sus límites y su
viabilidad como negocio.

*(Dejá 1 segundo en silencio y cortá la grabación.)*

---

## Antes de grabar

- [ ] **Paso cero:** comprobar que x.com carga con la extensión puesta (una extensión de
      privacidad lo rompe; ver `prototipo/GUION-CAPTURAS.md`).
- [ ] Desde `prototipo/`, con `OPENAI_API_KEY` en `servicio/.env`: `make dev`. Cargar
      `prototipo/extension/dist` en `chrome://extensions`.
- [ ] **Precalentar la caché:** analizar el caso 1 *después* de arrancar el servicio. La
      caché es en memoria: no reiniciar el servicio hasta terminar la toma.
- [ ] Probar el caso 2 **sin** analizarlo (que la publicación cargue); si se analiza, deja
      de ser nuevo. Probar el caso 3 en otra cuenta o no tocarlo.
- [ ] X en **tema claro**, zoom del navegador al 125 %, pestañas con `.env` cerradas.
- [ ] Cuentas de personas: preferir no mostrarlas. Si aparece una en la *timeline*, bajá
      rápido; no se puede difuminar en una toma única.
- [ ] Cámara chica en una esquina que no tape el panel de evidencia (probarlo antes).
- [ ] «No molestar» activado.
- [ ] Ensayo con un caso de prueba: tiene que dar entre 3:45 y 4:30.
