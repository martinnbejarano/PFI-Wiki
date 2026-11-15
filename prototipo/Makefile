# Atajos del prototipo. Se corren desde `prototipo/`.
#
# El servicio es Python y la extensión es Node, así que los comandos de cada uno
# viven en herramientas distintas. Este archivo es el único lugar donde hace
# falta acordarse de cuál es cuál.

SERVICIO := servicio
EXTENSION := extension
PY := $(SERVICIO)/.venv/bin/python
PIP := $(SERVICIO)/.venv/bin/pip
UVICORN := $(SERVICIO)/.venv/bin/uvicorn
PUERTO ?= 8000
CLASIFICADOR := clasificador/space
# Los pesos de BETO de dos etapas (salida de `fine_tuning.ipynb`); no viven en el repo.
PESOS_BETO ?= $(HOME)/Downloads/results/pesos/beto_fakedes-chequeado_s42

.DEFAULT_GOAL := ayuda
.PHONY: base base-apagar migrar-sqlite desplegar-clasificador encender beto-encender beto-apagar apagar ayuda instalar instalar-clasificador clasificador servicio extension extension-desplegada desplegar dev test test-servicio test-extension parcial lento limpiar

ayuda:
	@echo "Prototipo del PFI — atajos disponibles:"
	@echo ""
	@echo "  make instalar    Crea el venv, instala dependencias de Python y de Node"
	@echo "  make dev         Construye la extensión y levanta BETO y el servicio (lo habitual)"
	@echo "  make servicio    Solo el servicio, con recarga automática"
	@echo "  make extension   Solo construye la extensión"
	@echo "  make extension-desplegada  La extensión contra el servicio de Azure"
	@echo "  make desplegar   Sube servicio/ a Azure Container Apps (requiere \`az login\`)"
	@echo "  make test        Las dos baterías de pruebas"
	@echo "  make clasificador  BETO local en :7860 (Módulo 1 con ADAPTADOR=compuesto)"
	@echo "  make base        PostgreSQL + pgvector en Docker, en :5433 (lo levantan servicio y test)"
	@echo "  make base-apagar Detiene el contenedor; los datos quedan en el volumen"
	@echo "  make migrar-sqlite SQLITE=ruta.sqlite3  Copia una base SQLite vieja a PostgreSQL"
	@echo ""
	@echo "  make parcial     El servicio sin credencial: fuerza el análisis parcial"
	@echo "  make lento       El servicio con razonamiento alto: alarga el estado transitorio"
	@echo ""
	@echo "  Variables: PUERTO=8001 make servicio"
	@echo ""
	@echo "  La extensión se carga en chrome://extensions → Modo de desarrollador"
	@echo "  → Cargar descomprimida → prototipo/extension/dist"

instalar:
	python3.13 -m venv $(SERVICIO)/.venv
	$(PIP) install -q -r $(SERVICIO)/requirements.txt -r $(SERVICIO)/requirements-dev.txt
	cd $(EXTENSION) && npm install
	@test -f $(SERVICIO)/.env || (cp $(SERVICIO)/.env.example $(SERVICIO)/.env && \
		echo "" && echo "Creado servicio/.env — falta completar OPENAI_API_KEY")

# El Space corrido en local. En macOS torch sale de PyPI: la rueda `+cpu` del
# requirements.txt es solo para la imagen Linux.
instalar-clasificador:
	uv venv -q -p 3.13 $(CLASIFICADOR)/.venv
	grep -v -e '^--extra-index-url' -e '^torch' $(CLASIFICADOR)/requirements.txt \
		| uv pip install -q -p $(CLASIFICADOR)/.venv/bin/python -r - torch==2.14.0
	uv pip install -q -p $(CLASIFICADOR)/.venv/bin/python -r clasificador/requirements-dev.txt

clasificador:
	cd $(CLASIFICADOR) && PYTHONPATH=.. MODELO=$(PESOS_BETO) .venv/bin/uvicorn app:app --port 7860

# La base del servicio (#121): PostgreSQL con pgvector en Docker. En :5433 para
# no chocar con un Postgres local en :5432; `DATABASE_URL` apunta acá por
# defecto. Los datos viven en el volumen `pfi-postgres` y sobreviven a
# `base-apagar`. Los tests usan la base `pfi_pruebas` del mismo contenedor.
POSTGRES := pfi-postgres

base:
	@docker start $(POSTGRES) >/dev/null 2>&1 || docker run -d --name $(POSTGRES) \
		-e POSTGRES_USER=pfi -e POSTGRES_PASSWORD=pfi -e POSTGRES_DB=pfi -p 5433:5432 \
		-v pfi-postgres:/var/lib/postgresql/data pgvector/pgvector:pg17 >/dev/null
	@until docker exec $(POSTGRES) pg_isready -q -h localhost -U pfi; do sleep 0.5; done

base-apagar:
	docker stop $(POSTGRES)

# Una base SQLite de antes de #121 (histórico, memoria, índice) a la de
# DATABASE_URL. sqlite-vec se agrega solo para esta corrida.
SQLITE ?= $(SERVICIO)/prototipo.sqlite3
migrar-sqlite: base
	uv run -q --no-project -p $(PY) --with sqlite-vec==0.1.9 python $(SERVICIO)/migrar_sqlite.py $(SQLITE)

# Lo habitual: la extensión construida, BETO y el servicio andando en la misma
# terminal. Ctrl+C corta los dos.
dev: extension
	$(MAKE) -j2 clasificador servicio

servicio: base
	cd $(SERVICIO) && .venv/bin/uvicorn app.main:aplicacion --reload --port $(PUERTO) --log-level info

extension:
	cd $(EXTENSION) && npm run build

# El despliegue en Azure Container Apps (#122, ver README «Despliegue»): resource
# group `factum` en chilecentral, imágenes en el ACR `factumacr`, que las apps
# bajan con la identidad administrada `factum-id` (AcrPull). Requiere `az login`.
URL_DESPLEGADA := https://servicio.proudglacier-c502e042.chilecentral.azurecontainerapps.io
GRUPO := factum
ACR := factumacr.azurecr.io
ETIQUETA := $(shell git rev-parse --short HEAD)

extension-desplegada:
	cd $(EXTENSION) && VITE_URL_SERVICIO=$(URL_DESPLEGADA) npm run build

# La API y el job de la ingesta comparten imagen. La etiqueta es el commit, para
# que `update` cree una revisión nueva.
desplegar:
	az acr login -n factumacr
	docker buildx build --platform linux/amd64 -t $(ACR)/factum-servicio:$(ETIQUETA) --push $(SERVICIO)
	az containerapp update -g $(GRUPO) -n servicio --image $(ACR)/factum-servicio:$(ETIQUETA) -o none
	az containerapp job update -g $(GRUPO) -n ingesta --image $(ACR)/factum-servicio:$(ETIQUETA) -o none
	curl -fsS $(URL_DESPLEGADA)/salud

# BETO con los pesos dentro de la imagen (PESOS_BETO, la salida de `fine_tuning.ipynb`).
desplegar-clasificador:
	az acr login -n factumacr
	D=$$(mktemp -d) && rsync -a --exclude .venv --exclude __pycache__ $(CLASIFICADOR)/ $$D/ \
		&& cp clasificador/datos.py $$D/ && rsync -a $(PESOS_BETO)/ $$D/modelo/ \
		&& docker buildx build --platform linux/amd64 -t $(ACR)/factum-clasificador:$(ETIQUETA) --push $$D
	az containerapp update -g $(GRUPO) -n clasificador --image $(ACR)/factum-clasificador:$(ETIQUETA) -o none

# BETO escala a cero solo: apagado no cuesta nada y el primer pedido después de
# un rato espera el arranque en frío (TIEMPO_LIMITE_CLASIFICADOR_S=120 en la API).
# Encendido deja una réplica caliente, para demos y mediciones.
beto-encender:
	az containerapp update -g $(GRUPO) -n clasificador --min-replicas 1 -o none

beto-apagar:
	az containerapp update -g $(GRUPO) -n clasificador --min-replicas 0 -o none

# La API a cero réplicas (despierta con el primer pedido) y BETO apagado. La base
# sigue encendida: `az postgres flexible-server stop` la frena hasta 7 días.
apagar: beto-apagar
	az containerapp update -g $(GRUPO) -n servicio --min-replicas 0 -o none

encender:
	az containerapp update -g $(GRUPO) -n servicio --min-replicas 1 -o none

test: test-servicio test-extension

# Sin credencial ni Space a propósito: la batería no depende de red ni de la clave.
test-servicio: base
	cd $(SERVICIO) && env -u OPENAI_API_KEY ADAPTADOR=llm INTERVALO_DESPERTAR_CLASIFICADOR_S=3600 .venv/bin/python -m pytest -q

test-extension:
	cd $(EXTENSION) && npx tsc --noEmit && npm test

# Sin credencial el servicio degrada en vez de romper: sirve para la captura
# del análisis parcial (RNF-11) sin tocar nada más.
parcial: base
	cd $(SERVICIO) && env -u OPENAI_API_KEY .venv/bin/uvicorn app.main:aplicacion --port $(PUERTO)

# Alarga la llamada al proveedor, que es lo que deja el indicador el tiempo
# suficiente en su estado transitorio como para capturarlo.
lento: base
	cd $(SERVICIO) && ESFUERZO_DE_RAZONAMIENTO=high .venv/bin/uvicorn app.main:aplicacion --port $(PUERTO)

limpiar:
	rm -rf $(EXTENSION)/dist
	find $(SERVICIO) -name __pycache__ -type d -prune -exec rm -rf {} +
	rm -rf $(SERVICIO)/.pytest_cache

