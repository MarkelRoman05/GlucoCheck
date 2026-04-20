#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# GlucoCheck — Script de arranque local (Mac / Linux)
# Uso: bash scripts/start.sh
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$ROOT_DIR/.venv"
ARTIFACTS_DIR="$ROOT_DIR/data/processed"
FRONTEND="$ROOT_DIR/frontend/index.html"
PORT=8000

# ── Colores ──────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

step()  { echo -e "\n${CYAN}${BOLD}▶ $1${NC}"; }
ok()    { echo -e "  ${GREEN}✔ $1${NC}"; }
warn()  { echo -e "  ${YELLOW}⚠ $1${NC}"; }
error() { echo -e "  ${RED}✖ $1${NC}"; exit 1; }

echo -e "\n${BOLD}╔══════════════════════════════════════╗"
echo -e "║   GlucoCheck — Arranque local        ║"
echo -e "╚══════════════════════════════════════╝${NC}"

# ── 1. Comprobar Python 3.10+ ────────────────────────────────────────────────
step "Comprobando Python 3.10+..."

PYTHON=""
for cmd in python3.12 python3.11 python3.10 python3 python; do
  if command -v "$cmd" &>/dev/null; then
    version=$("$cmd" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null)
    major=$(echo "$version" | cut -d. -f1)
    minor=$(echo "$version" | cut -d. -f2)
    if [ "$major" -eq 3 ] && [ "$minor" -ge 10 ]; then
      PYTHON="$cmd"
      ok "Usando $cmd (versión $version)"
      break
    fi
  fi
done

[ -z "$PYTHON" ] && error "No se encontró Python 3.10+. Instálalo desde https://www.python.org/downloads/"

# ── 2. Entorno virtual ───────────────────────────────────────────────────────
step "Preparando entorno virtual..."

if [ ! -d "$VENV_DIR" ]; then
  "$PYTHON" -m venv "$VENV_DIR"
  ok "Entorno virtual creado en .venv/"
else
  ok "Entorno virtual ya existe (.venv/)"
fi

# Activar
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

# ── 3. Instalar dependencias ─────────────────────────────────────────────────
step "Instalando dependencias..."

pip install --quiet --upgrade pip
pip install --quiet -r "$ROOT_DIR/requirements.txt"
ok "Dependencias instaladas"

# ── 4. Pipeline de datos (solo si faltan artefactos) ────────────────────────
ARTIFACTS_OK=true
for f in model.pkl scaler.pkl threshold.txt; do
  [ ! -f "$ARTIFACTS_DIR/$f" ] && ARTIFACTS_OK=false && break
done

if [ "$ARTIFACTS_OK" = false ]; then
  step "Ejecutando pipeline de datos (primera ejecución)..."
  warn "Esto puede tardar unos minutos..."

  cd "$ROOT_DIR"
  python -m src.data.download_data  && ok "Datos descargados"
  python -m src.data.preprocess     && ok "Preprocesamiento completado"
  python -m src.models.train_model  && ok "Modelo entrenado"

  for f in model.pkl scaler.pkl threshold.txt; do
    [ ! -f "$ARTIFACTS_DIR/$f" ] && error "No se generó el artefacto: $f"
  done
  ok "Artefactos generados correctamente"
else
  ok "Artefactos ya existen (model.pkl, scaler.pkl, threshold.txt) — omitiendo pipeline"
fi

# ── 5. Abrir frontend en el navegador ───────────────────────────────────────
step "Abriendo frontend..."

if [ -f "$FRONTEND" ]; then
  if command -v open &>/dev/null; then
    open "$FRONTEND"
  elif command -v xdg-open &>/dev/null; then
    xdg-open "$FRONTEND"
  fi
  ok "Frontend abierto: $FRONTEND"
else
  warn "No se encontró frontend/index.html"
fi

# ── 6. Arrancar backend ──────────────────────────────────────────────────────
step "Arrancando backend en http://localhost:$PORT ..."
echo ""
echo -e "  ${GREEN}Backend disponible en:${NC} http://localhost:$PORT"
echo -e "  ${GREEN}Documentación API:${NC}    http://localhost:$PORT/docs"
echo -e "  ${YELLOW}Pulsa Ctrl+C para detener${NC}"
echo ""

cd "$ROOT_DIR"
uvicorn src.api.main:app --host 0.0.0.0 --port "$PORT" --reload
