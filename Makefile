# ─────────────────────────────────────────────────────────────────────────────
# GlucoCheck — Makefile para ejecución local
# ─────────────────────────────────────────────────────────────────────────────

PYTHON      ?= python3
VENV        := .venv
VENV_BIN    := $(VENV)/bin
PORT        ?= 8000
ARTIFACTS   := data/processed/model.pkl data/processed/scaler.pkl data/processed/threshold.txt

.DEFAULT_GOAL := help

# ── Activación del venv ───────────────────────────────────────────────────────
ACTIVATE := . $(VENV_BIN)/activate &&

.PHONY: help install pipeline run all clean

help: ## Muestra esta ayuda
	@echo ""
	@echo "  GlucoCheck — comandos disponibles"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	  | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36mmake %-12s\033[0m %s\n", $$1, $$2}'
	@echo ""

# ── Entorno virtual + dependencias ───────────────────────────────────────────
$(VENV)/bin/activate: requirements.txt
	@echo "▶ Creando entorno virtual..."
	$(PYTHON) -m venv $(VENV)
	$(ACTIVATE) pip install --quiet --upgrade pip
	$(ACTIVATE) pip install --quiet -r requirements.txt
	@echo "  ✔ Dependencias instaladas"
	@touch $(VENV)/bin/activate

install: $(VENV)/bin/activate ## Crea el venv e instala todas las dependencias
	@echo "  ✔ Listo"

# ── Pipeline de datos ─────────────────────────────────────────────────────────
pipeline: install ## Ejecuta el pipeline completo (descarga, preprocesamiento, entrenamiento)
	@echo "▶ Ejecutando pipeline de datos..."
	$(ACTIVATE) python -m src.data.download_data
	@echo "  ✔ Datos descargados"
	$(ACTIVATE) python -m src.data.preprocess
	@echo "  ✔ Preprocesamiento completado"
	$(ACTIVATE) python -m src.models.train_model
	@echo "  ✔ Modelo entrenado — artefactos en data/processed/"

# ── Backend ───────────────────────────────────────────────────────────────────
run: install ## Arranca el backend en http://localhost:$(PORT)
	@echo "▶ Iniciando backend en http://localhost:$(PORT) ..."
	@echo "  Documentación API: http://localhost:$(PORT)/docs"
	@echo "  Pulsa Ctrl+C para detener"
	@echo ""
	$(ACTIVATE) uvicorn src.api.main:app --host 0.0.0.0 --port $(PORT) --reload

# ── Todo en uno ───────────────────────────────────────────────────────────────
all: install ## install + pipeline (si faltan artefactos) + run
	@missing=0; \
	for f in $(ARTIFACTS); do [ ! -f "$$f" ] && missing=1 && break; done; \
	if [ $$missing -eq 1 ]; then \
	  echo "▶ Artefactos no encontrados — ejecutando pipeline..."; \
	  $(MAKE) pipeline; \
	else \
	  echo "  ✔ Artefactos ya existen — omitiendo pipeline"; \
	fi
	@$(MAKE) run

# ── Limpieza ──────────────────────────────────────────────────────────────────
clean: ## Elimina el entorno virtual y los artefactos generados
	@echo "▶ Limpiando entorno..."
	rm -rf $(VENV)
	rm -f data/processed/model.pkl data/processed/scaler.pkl data/processed/threshold.txt
	@echo "  ✔ Limpieza completada"
