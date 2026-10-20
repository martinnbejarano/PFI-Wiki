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
.PHONY: beto-encender beto-apagar ayuda instalar instalar-clasificador clasificador servicio extension extension-desplegada desplegar dev test test-servicio test-extension parcial lento limpiar

ayuda:
	@echo "Prototipo del PFI — atajos disponibles:"
	@echo ""
	@echo "  make instalar    Crea el venv, instala dependencias de Python y de Node"
	@echo "  make dev         Construye la extensión y levanta BETO y el servicio (lo habitual)"
	@echo "  make servicio    Solo el servicio, con recarga automática"
	@echo "  make extension   Solo construye la extensión"
	@echo "  make extension-desplegada  La extensión contra el servicio de Railway"
	@echo "  make desplegar   Sube servicio/ a Railway (requiere \`railway login\`)"
	@echo "  make test        Las dos baterías de pruebas"
	@echo "  make clasificador  BETO local en :7860 (Módulo 1 con ADAPTADOR=compuesto)"
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

clasificador:
	cd $(CLASIFICADOR) && PYTHONPATH=.. MODELO=$(PESOS_BETO) .venv/bin/uvicorn app:app --port 7860

# Lo habitual: la extensión construida, BETO y el servicio andando en la misma
# terminal. Ctrl+C corta los dos.
dev: extension
	$(MAKE) -j2 clasificador servicio

servicio:
	cd $(SERVICIO) && .venv/bin/uvicorn app.main:aplicacion --reload --port $(PUERTO) --log-level info

extension:
	cd $(EXTENSION) && npm run build

# El servicio en Railway (proyecto `factum`, ver README «Despliegue»).
URL_DESPLEGADA := https://servicio-production-671c.up.railway.app
RAILWAY_PROYECTO := b477733d-cbf8-43dc-a40a-1355d22e7230

extension-desplegada:
	cd $(EXTENSION) && VITE_URL_SERVICIO=$(URL_DESPLEGADA) npm run build

# BETO en Railway cuesta ≈ 12 USD/mes encendido: se prende solo para demos y mediciones.
# Apagado, el Módulo 1 lo puntúa el LLM y /senales devuelve una lista vacía.
beto-encender:
	cd $(SERVICIO) && railway service scale -s clasificador eu-west=1
	cd $(SERVICIO) && railway variable set -s servicio ADAPTADOR=compuesto

beto-apagar:
	cd $(SERVICIO) && railway variable set -s servicio ADAPTADOR=llm
	cd $(SERVICIO) && railway service scale -s clasificador eu-west=0

desplegar:
	cd $(SERVICIO) && railway up -p $(RAILWAY_PROYECTO) -s servicio -e production --ci
	curl -fsS $(URL_DESPLEGADA)/salud

test: test-servicio test-extension

# Sin credencial ni Space a propósito: la batería no depende de red ni de la clave.
test-servicio:
	cd $(SERVICIO) && env -u OPENAI_API_KEY ADAPTADOR=llm INTERVALO_DESPERTAR_CLASIFICADOR_S=3600 .venv/bin/python -m pytest -q

test-extension:
	cd $(EXTENSION) && npx tsc --noEmit && npm test

# Sin credencial el servicio degrada en vez de romper: sirve para la captura
# del análisis parcial (RNF-11) sin tocar nada más.
parcial:
	cd $(SERVICIO) && env -u OPENAI_API_KEY .venv/bin/uvicorn app.main:aplicacion --port $(PUERTO)

# Alarga la llamada al proveedor, que es lo que deja el indicador el tiempo
# suficiente en su estado transitorio como para capturarlo.
lento:
	cd $(SERVICIO) && ESFUERZO_DE_RAZONAMIENTO=high .venv/bin/uvicorn app.main:aplicacion --port $(PUERTO)

limpiar:
	rm -rf $(EXTENSION)/dist
	find $(SERVICIO) -name __pycache__ -type d -prune -exec rm -rf {} +
	rm -rf $(SERVICIO)/.pytest_cache

