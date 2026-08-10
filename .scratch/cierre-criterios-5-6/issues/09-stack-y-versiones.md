# 09 · Framework del panel web y versiones fijadas del stack

Type: grilling
Status: open
Blocked by: —

## Question

`tecnologias.md` es un *stub* de abril con cuatro `[POR DEFINIR]`. `recursos.md` resuelve **dónde** corre cada cosa —Railway, Vercel, Hugging Face Pro, Tavily— pero no **con qué** se escribe. El criterio 5 evalúa la justificación técnica, no la de costos, así que ese hueco es el criterio entero.

Lo que hay decidido y solo hay que escribir: Python con FastAPI, PostgreSQL 16 con `pgvector` e índice HNSW, Chrome Manifest V3, XLM-T sobre Hugging Face.

Lo que **no** está decidido en ninguna página del wiki:

1. **El framework del panel web.** Es el hueco más grande: `recursos.md` dice Vercel y nada más. React, Next.js, Astro o HTML servido estático. El dashboard B2B ya tiene mockup en HTML y CSS, y la decisión 6 del bloque dice que ese marcado es el punto de partida — eso empuja hacia lo más liviano.
2. **Versiones concretas.** ¿Se compromete Python 3.12 o 3.13, FastAPI 0.1x, PostgreSQL 16? Fijar una versión es defendible; decir «la última» no.
3. **El *bundler* de la extensión.** Manifest V3 con TypeScript necesita empaquetado. Vite, esbuild, o nada y JavaScript plano.
4. **ORM o SQL directo.** SQLAlchemy con Alembic, o `psycopg` y migraciones a mano. Con catorce entidades y una columna vectorial la respuesta no es obvia: `pgvector` se integra bien con SQLAlchemy pero agrega una capa que hay que justificar.
5. **Qué modelo produce los *embeddings*** de la búsqueda por similitud. Es una decisión técnica y a la vez una columna del esquema (ticket 06), así que no puede quedar implícita.
6. **Alternativas por capa.** El criterio premia la justificación comparada. ¿Se compara en todas las capas o solo donde la elección fue disputada?

**Recomendación de partida.** Lo más liviano que sostenga el mockup existente en el panel web, versiones fijadas y explícitas, SQL directo con migraciones versionadas, y comparación solo donde hubo alternativa real — una tabla de alternativas inventadas para rellenar se nota.
