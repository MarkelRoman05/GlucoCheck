# CLAUDE.md — GlucoCheck

Guía de referencia para Claude Code al trabajar en este repositorio.

## Proyecto

**GlucoCheck** es una aplicación de ML académica que clasifica el riesgo de Diabetes Tipo 2 a partir de 8 variables clínicas. Stack: Python 3.10, FastAPI, scikit-learn (Random Forest), Pydantic v2, Uvicorn.

Repositorio equipo: `MarkelRoman05/GlucoCheck`
Fork personal: `masmke/glucocheck-migue`
Deploy v2: `masmke/GlucoCheck-v2` → Railway (backend) + Netlify (frontend)

---

## Estructura del repositorio

```
src/
  api/
    main.py        # FastAPI app — endpoints /health /predict /metrics
    schemas.py     # Pydantic v2 — PredictionInput, PredictionOutput, MetricsResponse
  data/
    download_data.py
    preprocess.py
  models/
    train_model.py
data/
  raw/             # CSVs ignorados por .gitignore
  processed/       # model.pkl, scaler.pkl, threshold.txt (incluidos en repo)
frontend/
  index.html       # SPA vanilla JS — formulario + historial + validación en tiempo real
scripts/
  start.sh         # Arranque local Mac/Linux (detecta Python, crea venv, pipeline si faltan artefactos)
  start.bat        # Arranque local Windows
tests/
  test_api.py
  test_model.py
Makefile           # make install | pipeline | run | all | clean
Dockerfile
docker-compose.yml
```

---

## Comandos de desarrollo

```bash
# Entorno virtual + dependencias
make install

# Pipeline completo (descarga → preprocesamiento → entrenamiento)
make pipeline

# Arrancar backend en http://localhost:8000
make run

# Todo en uno (install + pipeline si falta + run)
make all

# O directamente con el script
bash scripts/start.sh

# Tests
pytest tests/ -v
```

---

## API

| Método | Ruta       | Descripción                              |
|--------|------------|------------------------------------------|
| GET    | `/health`  | Estado del servidor y threshold del modelo |
| POST   | `/predict` | Inferencia — devuelve nivel de riesgo    |
| GET    | `/metrics` | Estadísticas de uso en memoria           |

### Payload `/predict`

```json
{
  "pregnancies": 2,
  "glucose": 120,
  "blood_pressure": 70,
  "skin_thickness": 25,
  "insulin": 80,
  "bmi": 28.5,
  "diabetes_pedigree": 0.5,
  "age": 35
}
```

### Rangos clínicos válidos (src/api/schemas.py)

| Campo              | Mín  | Máx   |
|--------------------|------|-------|
| pregnancies        | 0    | 17    |
| glucose            | 44   | 199   |
| blood_pressure     | 24   | 122   |
| skin_thickness     | 7    | 99    |
| insulin            | 0    | 846   |
| bmi                | 18.0 | 67.0  |
| diabetes_pedigree  | 0.08 | 2.42  |
| age                | 21   | 81    |

Valores fuera de rango devuelven **422** con `{"error": "Error de validación", "campos": [...]}`.

---

## Artefactos del modelo

`data/processed/model.pkl`, `scaler.pkl`, `threshold.txt` están **incluidos en el repositorio** (no ignorados). Generados con Random Forest + SMOTE + StandardScaler sobre el dataset Pima Indians. El threshold por defecto es `0.63`.

Para regenerarlos:
```bash
make pipeline
```

---

## Docker

```bash
docker-compose up --build   # backend en :8000, frontend nginx en :80
docker-compose down
```

La imagen del backend no expone `ENV PORT` — el puerto se lee desde `os.environ.get("PORT", 8000)` en `main.py`.

---

## Despliegue (Railway)

- Builder: **Nixpacks**
- Arranque: `python src/api/main.py` (via Procfile)
- `railway.json` no incluye `startCommand` — Railway usa el Procfile
- **No añadir `ENV PORT` en el Dockerfile**: Railway inyecta su propio `$PORT`

```
Procfile → web: python src/api/main.py
railway.json → { "build": {"builder": "NIXPACKS"}, "deploy": {"restartPolicyType": "ON_FAILURE"} }
```

---

## Convenciones de código

- **Pydantic v2**: usar `field_validator`, `model_dump()` (no `dict()`)
- **Imports duales en main.py**: bloque `try/except ModuleNotFoundError` para ejecutar tanto con `uvicorn src.api.main:app` como con `python src/api/main.py`
- **Logging**: `logging.getLogger("glucocheck.api")` — nivel INFO en producción
- **Métricas**: `_metrics` dict en memoria, se resetea al reiniciar el servidor

---

## Tests

```bash
pytest tests/ -v              # todos
pytest tests/test_api.py -v   # solo API
pytest tests/test_model.py -v # solo modelo
```

11/11 tests pasan en la rama main. Los tests de API usan `httpx.TestClient`.

---

## Ramas

| Rama    | Propósito                              |
|---------|----------------------------------------|
| main    | Código estable — fuente de verdad      |
| develop | Desarrollo activo (fork masmke)        |

PRs van de `develop → main` en el fork personal, y de `masmke/glucocheck-migue → MarkelRoman05/GlucoCheck` para sincronizar al equipo.
