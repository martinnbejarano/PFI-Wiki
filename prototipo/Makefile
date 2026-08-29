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

.DEFAULT_GOAL := ayuda
.PHONY: ayuda instalar servicio extension dev test test-servicio test-extension parcial lento limpiar

ayuda:
	@echo "Prototipo del PFI — atajos disponibles:"
	@echo ""
	@echo "  make instalar    Crea el venv, instala dependencias de Python y de Node"
	@echo "  make dev         Construye la extensión y levanta el servicio (lo habitual)"
	@echo "  make servicio    Solo el servicio, con recarga automática"
	@echo "  make extension   Solo construye la extensión"
	@echo "  make test        Las dos baterías de pruebas"
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

# Lo habitual: la extensión construida y el servicio andando.
dev: extension servicio

servicio:
	cd $(SERVICIO) && .venv/bin/uvicorn app.main:aplicacion --reload --port $(PUERTO) --log-level info

extension:
	cd $(EXTENSION) && npm run build

test: test-servicio test-extension

# Sin credencial a propósito: la batería no depende de red ni de la clave.
test-servicio:
	cd $(SERVICIO) && env -u OPENAI_API_KEY .venv/bin/python -m pytest -q

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

