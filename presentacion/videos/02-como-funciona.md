# Video 02 — Cómo funciona

Archivo final: **`02 - Como funciona.mp4`**. Entrega: 10/11/2026.

**Duración objetivo: 3:30** (máximo 5:00). Una sola toma, sin cortes, con la demo sobre
X: un caso verdadero y uno falso, los 2 ya analizados (en la caché).

**Qué se ve:** arranca en la lámina 4 del deck (la arquitectura del video 1), pasa a Chrome
con X y la extensión, y termina en Chrome. La cámara chica sigue en una esquina.

Mismas reglas que el video 1: primera persona singular, sin nombrar el proveedor de nube,
cifras tal cual.

| # | Tramo | Pantalla | Tiempo | Acumulado |
|---|---|---|---|---|
| 1 | Apertura y escala | Deck, lámina 4 | 0:30 | 0:30 |
| 2 | La señal de BETO | Chrome, X | 0:20 | 0:50 |
| 3 | Caso verdadero | Chrome, X | 0:45 | 1:35 |
| 4 | Caso falso y su evidencia | Chrome, X | 1:15 | 2:50 |
| 5 | Desglose | Chrome, X | 0:30 | 3:20 |
| 6 | Puente | Chrome, X | 0:10 | 3:30 |

---

## Los casos (ya analizados el 10/11, en la caché del servicio)

1. **Verdadero:** https://x.com/somosbullmarket/status/2119892784651858306 — *parece
   verificado*: el INDEC publica la inflación de octubre el jueves 12/11.
2. **Falso:** https://x.com/DaniMirin10/status/2120078179217838501 — *contradicho por
   fuentes oficiales*: «la pobreza bajó a la mitad»; lo contradicen 2 informes de pobreza
   del INDEC. Es una respuesta: arriba aparece el tuit al que responde. Bajá hasta el de
   @DaniMirin10 y no muestres su perfil.

**La caché vive en la memoria del servicio: si se reinicia `make dev`, se pierde** y los 2
casos vuelven a tardar como nuevos (8 a 16 s). No reinicies nada entre la preparación y la
toma.

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

## 3 · Caso verdadero — X · 0:45

*(Abrís el caso 1 y pedís el análisis.)*

Empiezo por uno verdadero. Pido el análisis: contrasta la afirmación con fuentes oficiales,
medios socios de ADEPA y verificadores, usando un LLM con búsqueda restringida a esas
fuentes. La primera vez tarda entre 8 y 16 segundos; este ya lo analicé, así que sale al
instante: un tuit viral se analiza una vez y se sirve a todos. *(Leés el veredicto y la
cifra.)* Parece verificado, y acá está la fuente oficial que lo respalda.

## 4 · Caso falso y su evidencia — X · 1:15

*(Abrís el caso 2, bajás hasta el tuit de @DaniMirin10 y pedís el análisis.)*

Ahora uno falso. Dice que la pobreza bajó a la mitad. *(Leés el veredicto y la cifra.)*
Contradicho por fuentes oficiales, y dice cuál: el INDEC.

*(Abrís el panel de evidencia.)* Este es el panel de evidencia. Cada fuente abre el
documento original *(abrís el informe del INDEC y volvés)*: no hace falta creerle al
número, se puede comprobar. Las fuentes oficiales pesan más que los medios.

*(Bajás hasta «Cómo se analiza».)* Y acá abajo, «Cómo se analiza»: contra qué fuentes se
contrasta, con el enlace al padrón de ADEPA. Los medios no los elijo yo: son los socios de
una asociación pública.

## 5 · Desglose — X · 0:30

*(En el mismo caso, abrís «Cómo se llegó al resultado».)*

Y esto conecta con la arquitectura del primer video. «Cómo se llegó al resultado» muestra
cada puntaje por separado: el del texto, que es la señal de BETO, y el del contraste con
fuentes, que es el que más pesa. *(Señalás los valores.)* El combinador los pondera y de
ahí sale la cifra de arriba. Cuando X no deja ver los datos de la cuenta, ese módulo no se
pronuncia y el resto se reparte su peso.

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
- [ ] Los 2 casos ya están en la caché: abrirlos y comprobar que el veredicto sale al
      instante. Si alguno tarda, se reinició el servicio: analizalo una vez antes de grabar.
- [ ] X en **tema claro**, zoom del navegador al 125 %, pestañas con `.env` cerradas.
- [ ] Cuentas de personas: preferir no mostrarlas. Si aparece una en la *timeline*, bajá
      rápido; no se puede difuminar en una toma única.
- [ ] Cámara chica en una esquina que no tape el panel de evidencia (probarlo antes).
- [ ] «No molestar» activado.
- [ ] Ensayo cronometrado: entre 3:15 y 4:00.
