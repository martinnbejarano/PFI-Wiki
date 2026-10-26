# Preguntas previsibles — exposición del 90 %

**Regla general:** escuchá la pregunta entera, respirá y contestá con el número primero y
la aclaración después. Si no sabés, decilo: «No lo sé con certeza, lo verifico y le
respondo». Si te marcan algo, anotalo y agradecé; no discutas.

Lo que se sabe de las instancias anteriores (ver [[ANALISIS-DEFENSAS]] y
`wiki/presentacion/e50/analisis-feedback.md`): las preguntas duran entre 12 y 20 minutos y
fueron casi todas de negocio. En el 50 % el evaluador anticipó «esto ya existe» y «quién
verifica al verificador».

Todas las cifras salen del documento entregado. Entre paréntesis, dónde están.

---

## Las seis que hay que tener resueltas

### 1 · «El F1 quedó abajo de la meta. ¿Entonces no funciona?»

El sistema completo sacó **0,712** contra una meta de **0,75**, así que RNF-05 **no se
cumple**, y lo digo así en el documento. Tres datos para leerlo bien:

1. **El intervalo de confianza del 95 % va de 0,61 a 0,80** y contiene la meta: con 94
   publicaciones no se puede afirmar ni descartar que el sistema la alcance.
2. **Supera con claridad a la línea base** adaptada (0,510), que queda debajo del extremo
   inferior del intervalo, y mejora diecinueve puntos al clasificador solo (0,518).
3. **La precisión en la clase *falso* es 1,00**: de 46 publicaciones verdaderas, ninguna
   fue señalada como falsa. Es el error que el objetivo pedía evitar, por su costo
   reputacional y legal. El costo está del otro lado: 25 de las 48 falsas pasaron como
   verificadas.

> Si pregunta por qué la meta se movió: el umbral pasó de 0,80 a 0,75 **antes** de evaluar
> el corpus argentino, porque 0,80 exigía superar el mejor resultado publicado sobre el
> corpus académico (0,7666). Y el objeto pasó del clasificador al sistema completo, también
> antes de correrlo. El umbral no se tocó a la vista del resultado. (Cap. 4, evaluación;
> conclusiones.)

### 2 · «¿No está sesgada la evaluación? Chequeado etiqueta y Chequeado es fuente.»

Sí, y lo declaro. **Chequeado figuró entre las fuentes recuperadas en 78 de los 94
análisis**, así que la búsqueda pudo encontrar la misma nota que asignó la etiqueta. El
0,712 **sobreestima** el desempeño ante desinformación nueva.

Hay un sesgo en sentido contrario: **el 77 % de esas publicaciones es anterior a 2022**,
y el sistema está pensado para publicaciones recientes, con la búsqueda viendo la
información de 2026. Los dos sesgos se declaran; ninguno se compensa con el otro. (Cap. 4,
matriz de confusión; conclusiones.)

> La mejora que lo resolvería: un corpus de tuits nuevos etiquetados después del análisis,
> sin que la fuente de la etiqueta esté en la jerarquía.

### 3 · «¿Por qué BETO y no directamente el LLM, si sacó más?»

Es cierto: sobre la partición de prueba del corpus académico el LLM sin ajuste sacó
**0,873** y BETO **0,760**. Elegí BETO por tres razones:

1. **Latencia y costo**: BETO corre sobre todas las publicaciones visibles, en lote, con
   una mediana de 0,85 s por lote y sin costo por consulta. El LLM tarda 2,8 s por
   publicación y se paga por *token*.
2. **Medible y reproducible**: el modelo es mío, con sus pesos versionados. El resultado
   del LLM puede estar contaminado: el corpus es público y pudo estar en su entrenamiento.
3. **El LLM igual está en el sistema**, donde aporta más: en el contraste con fuentes,
   que pesa 65 %. BETO da la señal rápida; el LLM, el análisis profundo a demanda.

### 4 · «¿Es viable económicamente? ¿VAN, TIR, *payback*?»

En el escenario neutral, con impuestos, cargas sociales y capital de trabajo, a una tasa
del 25 %:

| VAN | TIR | *Payback* | Descontado | Equilibrio |
|---|---|---|---|---|
| USD 63.935 | 72,6 % | 2,93 años | 3,46 años | 23 clientes (se proyectan 41,5) |

El VAN se mantiene positivo ante variaciones del 20 % en precio, captación, costo por
análisis o tasa. La variable que más pesa es el **precio de la API**: con una baja del
27 % el VAN se anula. Ese precio se contrastó con herramientas comparables, **no con
clientes**, y es lo primero que habría que validar. (Cap. 3, análisis financiero.)

> El pesimista da VAN negativo (USD −94.162) y no recupera la inversión: lo digo si
> pregunta por riesgos. El optimista no lo cito como argumento. Todo está en la lámina de
> respaldo de escenarios.

### 5 · «¿Quién verifica al verificador?»

Tres respuestas, en este orden:

1. **El criterio de fuentes no es mío.** Publicaciones oficiales del Estado nacional
   (INDEC, BCRA, Boletín Oficial, InfoLEG), todos los medios socios activos de ADEPA y tres
   verificadores profesionales: Chequeado, Reverso y AFP Factual.
2. **Está a la vista.** El detalle del análisis dice, en «Cómo se analiza», contra qué se
   contrastó y enlaza el padrón de ADEPA. Cada fuente abre el documento original.
3. **El objetivo no es que el usuario le crea al veredicto, sino que pueda prescindir de
   él.** Por eso el producto entrega el camino a la evidencia y no solo la conclusión.

> Si repregunta por ADEPA: es una cámara empresaria y refleja a la prensa establecida. Se
> eligió sobre el registro de publicidad oficial justamente para que el criterio no
> dependa del gobierno de turno.

### 6 · «Esto ya existe.»

Hay herramientas parecidas, y las nombro: la más cercana es **InTruth**, una extensión
gratuita de 2026 que escucha el audio de debates y muestra fuentes. Las **Notas de la
Comunidad** ponen contexto dentro de X, y **Grok** responde si lo invocan. Lo que ninguna
combina:

1. **En el texto de X, en el momento de lectura y sobre todas las publicaciones en
   pantalla.** InTruth trabaja sobre audio. Las Notas llegan cuando hay consenso: solo el
   16,9 % de las publicaciones con nota propuesta llega a mostrarla, y la mitad con más de
   23 horas de demora. Grok hay que invocarlo.
2. **Contra un padrón cerrado, público y argentino.** InTruth busca en la web abierta con
   etiquetas de sesgo de una base estadounidense. Acá la evidencia es el documento de
   origen argentino, no una nota de otro medio.

Por eso se plantea como complemento de las Notas, no como reemplazo: la nota aporta juicio
humano sobre lo más viral; el sistema, una señal inmediata sobre el resto. (Cap. 2,
competencia; `wiki/competencia/analisis-competitivo.md`.)

---

## Producto y números en pantalla

### 7 · «Ese número, ¿qué significa? ¿Alto es bueno?»

Son las **chances de que la afirmación sea verdadera, de 0 a 100: más alto es mejor**.
Más de 34, *parece verificado*; de 30 para abajo, *contradicho por fuentes oficiales*; en
el medio, *información sospechosa*. Los cortes son configuración (`pesos-v4`), no código.

> Por dentro el servicio estima lo contrario —el puntaje de desinformación, de 0 a 1— y
> la interfaz muestra el complemento para que número y color vayan en la misma dirección.
> La extensión lo rotula «puntaje de confianza» porque no está calibrado.

### 8 · «¿Por qué esos cortes tan juntos, 30 y 34?»

Salen de calibrar sobre la validación de Chequeado con un criterio fijado antes: la mayor
precisión en la clase *falso*. Con el corte anterior (0,40 en la escala interna), el mismo
análisis señalaba como falsas 14 publicaciones verdaderas. Prioricé no acusar en falso.

### 9 · «¿Por qué tarda tanto?»

El análisis profundo demora **16,0 s en el percentil 95, con mediana de 8,5 s**, y no
cumple la meta de 8 s (RNF-02). La búsqueda web del proveedor se lleva unos siete
segundos. Dos atenuantes: la memoria semántica resuelve en 40 ms las publicaciones
equivalentes a otras ya analizadas, y la caché sirve al instante lo viral. La solución es
extender la ingesta propia a medios y verificadores para sacar la búsqueda del camino
crítico.

### 10 · «¿Está todo hardcodeado?»

No. Pesos y umbrales son configuración: se cambian con una variable de entorno y un
reinicio. Cada análisis guarda la versión de configuración que lo produjo, y esa versión
se calcula a partir de los valores, así que no puede quedar desactualizada.

### 11 · «¿Cómo lo probaste?»

137 pruebas automatizadas en el servicio, con 93 % de cobertura de sentencias; 27 en la
extensión; siete pruebas funcionales, una por caso de uso, todas aprobadas; y una prueba
de usabilidad con SUS de 74,2 sobre 68 de referencia, con tres participantes, así que es un
indicio y no una medición concluyente.

---

## Riesgo, sesgo y legalidad

### 12 · «¿Cómo evitás sesgar políticamente el resultado?»

Tres decisiones, no una promesa: los medios **no los elijo yo** (todos los socios de
ADEPA, con padrón enlazado); el sistema se pronuncia **sobre la afirmación y nunca sobre la
persona**; y el nivel severo **atribuye el juicio a la fuente oficial**. Sin evidencia, no
hay veredicto: queda *sin contraste externo*. La ausencia de sesgo político fue lo que más
pidió la encuesta (82,8 %).

### 13 · «¿Y si marca algo verdadero como falso?»

En la evaluación no pasó: precisión 1,00 en *falso*. El diseño está ordenado así a
propósito: en la encuesta el falso positivo fue la preocupación principal (64,7 %). Y el
producto no bloquea ni oculta nada: muestra una señal con su evidencia al lado.

### 14 · «¿La parte legal?»

La recolección se ampara en la excepción de fuentes de acceso público de la Ley 25.326.
La cuenta autora se guarda seudonimizada con HMAC y **no se agrega ningún resultado por
cuenta**, porque perfilar autores es el archivo que prohíbe el artículo 7. El texto viaja
sin el usuario al proveedor del LLM en EE. UU., y el aviso de primer uso pide el
consentimiento de esa transferencia. El nivel severo se enuncia «contradicho por fuentes
oficiales» y no «falso» por el artículo 113 del Código Penal. (Cap. 3, viabilidad legal.)

### 15 · «¿Por qué solo X? WhatsApp es el vector principal.»

WhatsApp tiene cifrado de extremo a extremo: es una imposibilidad técnica, no una
decisión de alcance. X es una línea de tiempo pública que la extensión puede leer.

### 16 · «¿Qué impide que X o Google lo hagan mañana?»

Nada técnico. La defensa no es una barrera técnica sino el criterio argentino de fuentes y
el registro de qué desinformación circula, que se acumula con el uso.

---

## Investigación

### 17 · «¿La encuesta es representativa?»

No, y está dicho: 152 respuestas, 116 del segmento, muestreo no probabilístico concentrado
entre 18 y 25 años. Describe a las personas alcanzadas; no se extrapola a todos los
usuarios de X. El hallazgo central —4,09 de intención contra 3,58 de confianza en el
puntaje— ordenó el diseño, no el pronóstico de mercado.

### 18 · «¿Con quién hablaste además de la encuesta?»

Entrevistas en profundidad, entre ellas una periodista que verifica a diario. De ahí salió
el peso bajo de las señales de la cuenta (valor informativo alto, validez probatoria baja,
porque se compran) y el pedido de detectar contenido viejo que recircula, que está en el
trabajo futuro.

---

## Las de cortesía, al final

### 19 · «¿Qué te inspiró el tema?»

Veinte segundos, en primera persona y sin cifras. La versión corta y verdadera.

### 20 · «¿Qué sigue hasta diciembre?»

El documento está prácticamente cerrado; queda pulir con este feedback, grabar los videos
y preparar la defensa final. Si pregunta por el producto: extender la ingesta para bajar la
latencia y validar el precio con clientes.

---

## Lo que no tenés que ofrecer si no te preguntan

- Que la caché de análisis es en memoria y se vacía al reiniciar el servicio.
- Que el filtro de dominios del proveedor acepta 100 dominios y la jerarquía tiene más: los
  últimos medios del padrón solo entran por el filtro propio.
- Que `pesos-v4` es la configuración evaluada y servida, pero el aporte aislado del módulo
  de la cuenta no tiene medición propia.

Son honestos y están escritos en el repositorio; no aportan en diez minutos y abren frentes
que nadie abrió.
