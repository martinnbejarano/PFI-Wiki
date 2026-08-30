# Guion de la defensa — Entrega 50 %

Texto completo, para decir tal cual. **7:50 en total.**

---

## Lámina 1 · Portada — 0:20

Buenos días. Mi nombre es Juan Martín Bejarano Arce, estudiante de Ingeniería en
Informática, y mi tutor es Fidel Giro Uribazo.

Vengo a defender el avance del cincuenta por ciento de mi proyecto final: un sistema de
detección automática de desinformación en redes sociales.

## Lámina 2 · Qué se construyó — 0:20

Lo que construí es una extensión de Chrome que funciona sobre X. Sobre cada publicación te
dice si lo que afirma se sostiene, y te muestra las fuentes que lo respaldan.

Eso es el producto: un veredicto, y al lado la evidencia que lo sostiene.

## Lámina 3 · El problema — 0:35

El problema de fondo es de escala.

En Argentina hay treinta y un millones de usuarios de redes sociales. Dos de cada tres no
reconocen una noticia falsa cuando la ven. Y lo falso circula seis veces más rápido que lo
verdadero.

Del otro lado, la verificación profesional existe y es rigurosa, pero se hace de a una
afirmación por vez, y casi siempre después de que la información ya circuló.

El problema no es de rigor. Es de escala.

## Lámina 4 · La encuesta — 0:55

Para validar esto hice una encuesta propia.

El setenta y cuatro por ciento se cruza con desinformación seguido. El setenta y cinco por
ciento resuelve la duda en menos de tres minutos: verifica, pero de forma muy superficial.
Y el ochenta y cuatro por ciento exige neutralidad política.

Pero el hallazgo que ordenó todo el producto es este. Pregunté dos cosas en escala de uno a
cinco: cuánto usarían la herramienta, y cuánto le creerían a un puntaje generado
automáticamente. Usarla dio cuatro coma cero seis. Creerle al puntaje, tres coma cincuenta
y siete.

Quieren la herramienta, pero no le creen del todo al número.

Una aclaración: el corte que entró al documento fue de ciento cuarenta respuestas, ciento
siete dentro del segmento. La recolección sigue abierta y continúa hacia la Entrega 4.

## Lámina 5 · El hueco competitivo — 0:45

Este gráfico compara seis actores en cinco variables. Arriba es más.

Las soluciones automáticas son rápidas, pero se caen en accesibilidad ciudadana: son
productos empresariales, cerrados y caros. La única accesible al ciudadano es Chequeado,
que es verificación manual, y por eso se cae en automatización y en velocidad.

Las automáticas no son accesibles. La accesible no es automática. Esa intersección vacía es
el espacio del proyecto.

Aclaro algo antes de que me lo pregunten: estas son cinco de diez variables. Las otras
cinco son capacidades que decidí no construir, y ahí puntúo más bajo que todos.

## Lámina 6 · El modelo de negocio — 0:45

El modelo de negocio tiene dos lados.

El ciudadano no paga nunca: la extensión es gratis. Y no es filantropía ni un gancho
comercial. Es la fuente del dato.

Lo que se vende está del otro lado: una API de detección por volumen y reportes de
tendencias por suscripción, a medios, verificadores, organismos y marcas. No se vende la
extensión: se vende qué desinformación circula en Argentina ahora.

Y ahí está el activo que no se puede copiar: los competidores miden qué se publica, yo mido
qué se consume.

Los precios son tres: gratis para el ciudadano, doscientos dólares por mes para un medio
chico, y dos mil quinientos para un cliente *enterprise*. La infraestructura cuesta catorce.
El análisis financiero va en la Entrega 4.

## Lámina 7 · Cómo funciona — 0:45

Técnicamente son cuatro módulos.

El primero es el clasificador: lee el texto de la publicación y estima cuán sospechoso es.
Es un modelo de lenguaje multilingüe ajustado al español, con *fine-tuning*.

El segundo mira las señales públicas de la cuenta que publicó, con metadatos. Este no está
implementado todavía y pesa cero en el resultado.

El tercero es el contraste: busca en la web qué dicen las fuentes confiables sobre esa
misma afirmación.

Y el cuarto combina los tres con un promedio ponderado y decide el veredicto.

El recorrido completo es este: una publicación de X, la afirmación que contiene, qué dicen
las fuentes, y un veredicto con sus fuentes.

## Lámina 8 · La demo — 2:00

Es un video de dos minutos.

Antes de arrancar, una aclaración: la interfaz se ve oscura porque es la de X. La extensión
adopta el tema de la plataforma en lugar de imponer el suyo.

*(Arrancás el video y te quedás callado los primeros diez segundos.)*

Acá el indicador aparece solo sobre la publicación, sin que el usuario haga nada. Hago clic
y se abre el veredicto.

Este es el detalle, con los tres puntajes por separado. El puntaje va de cero a cien y mide
sospecha: más alto es peor. Arriba de setenta, contradicho por fuentes oficiales. Entre
cuarenta y setenta, información sospechosa. Abajo de cuarenta, parece verificado.

Y esto es el panel de evidencia. Cada fuente está enlazada al documento original, así que
se puede abrir y leer. Esto es lo que ningún competidor le entrega al ciudadano: no la
conclusión, sino el camino para no depender de ella.

La latencia real, medida de extremo a extremo, es de veinte segundos.

## Lámina 9 · La evidencia, y cierre — 1:25

El sistema no busca en cualquier lado. Busca en una lista cerrada de fuentes, y las muestra
ordenadas por peso.

Primero, fuentes oficiales: INDEC, Banco Central, InfoLEG, Boletín Oficial. Segundo, medios
de referencia: Infobae, Clarín, La Nación, Página/12 y Télam. Y tercero, verificaciones
previas: Chequeado, Reverso y AFP Factual.

Esos cinco medios son de orientación editorial diversa a propósito, porque la neutralidad
política fue la condición más votada de la encuesta.

Y la regla que ordena todo lo demás: si no encuentra ninguna fuente, no emite veredicto. Lo
dice, en lugar de opinar.

Para cerrar, dónde está el proyecto hoy. Entregué un documento de ciento veinticuatro
páginas, con dieciséis requerimientos funcionales y diecisiete no funcionales, nueve
diagramas propios y un prototipo que funciona de punta a punta. Hacia la Entrega 4 quedan
el clasificador entrenado, el corpus argentino y la validación experimental.

Tres cosas quedaron afuera y están declaradas: el módulo de credibilidad no está
implementado, falta la entrevista a una organización de verificación, y el clasificador
propio es trabajo de la Entrega 4. Son recortes declarados, no omisiones.

Y termino con esto. El objetivo no es que el usuario le crea al veredicto. Es que pueda
prescindir de él: el sistema le entrega el camino hacia la evidencia, no solamente la
conclusión.

Gracias.

## Lámina 10 · Gracias — sin tiempo asignado

Pasás a esta al decir «gracias» y la dejás puesta durante todas las preguntas. No hay nada
que decir acá.

---

## Si te dan 15 minutos

Cuatro agregados, en este orden: en la 6 abrís *Precio tentativo al cliente* y recorrés las
franjas; después de la 8 mostrás *Arquitectura — componentes* y contás el camino de una
petición; y en el cierre agregás el marco legal y la estrategia de datos, que están en
[[PREGUNTAS]], respuestas A a D.

## Control de tiempo

A los cinco minutos tenés que estar entrando en la lámina 7. Si vas atrasado, recortá la 5. El cronómetro del deck se activa con **T**.
