import sys
import time
import logging
import traceback
import joblib
import numpy as np
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

# Permite ejecutar tanto como módulo (uvicorn src.api.main) como script directo
try:
    from src.api.schemas import (
        PredictionInput, PredictionOutput, HealthResponse, MetricsResponse
    )
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from schemas import (
        PredictionInput, PredictionOutput, HealthResponse, MetricsResponse
    )

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("glucocheck.api")

# ── Constantes ────────────────────────────────────────────────────────────────
PROCESSED_DIR = Path(__file__).resolve().parents[2] / "data" / "processed"

FEATURE_ORDER = [
    "pregnancies", "glucose", "blood_pressure", "skin_thickness",
    "insulin", "bmi", "diabetes_pedigree", "age"
]

MESSAGES = {
    "riesgo_bajo": "Las variables introducidas no muestran combinaciones asociadas a un perfil de riesgo significativo.",
    "riesgo_moderado": "Las variables introducidas presentan algunos factores que podrían estar asociados a un riesgo moderado.",
    "riesgo_alto": "Las variables introducidas presentan una combinación asociada a un perfil de riesgo elevado.",
}

ADVERTENCIA = "Este resultado no constituye un diagnóstico médico."

# ── Métricas en memoria ───────────────────────────────────────────────────────
_metrics: dict = {
    "total_predicciones": 0,
    "distribucion": {
        "riesgo_bajo": 0,
        "riesgo_moderado": 0,
        "riesgo_alto": 0,
    },
    "tiempos_respuesta_ms": [],   # lista de floats para calcular la media
}


def _record_prediction(nivel: str, elapsed_ms: float) -> None:
    _metrics["total_predicciones"] += 1
    _metrics["distribucion"][nivel] += 1
    _metrics["tiempos_respuesta_ms"].append(elapsed_ms)


# ── Artefactos del modelo ─────────────────────────────────────────────────────
def load_artifacts():
    model_path     = PROCESSED_DIR / "model.pkl"
    scaler_path    = PROCESSED_DIR / "scaler.pkl"
    threshold_path = PROCESSED_DIR / "threshold.txt"

    missing = [p for p in [model_path, scaler_path, threshold_path] if not p.exists()]
    if missing:
        raise RuntimeError(
            f"Artefactos no encontrados: {[str(p) for p in missing]}. "
            "Ejecuta primero los scripts de preprocesamiento y entrenamiento."
        )

    model     = joblib.load(model_path)
    scaler    = joblib.load(scaler_path)
    threshold = float(threshold_path.read_text().strip())
    return model, scaler, threshold


try:
    model, scaler, threshold = load_artifacts()
    logger.info("Artefactos cargados correctamente (threshold=%.4f)", threshold)
except RuntimeError as e:
    logger.critical("Error al cargar artefactos: %s", e)
    raise

# ── Aplicación ────────────────────────────────────────────────────────────────
app = FastAPI(
    title="GlucoCheck API",
    description="API de inferencia para clasificación del riesgo de Diabetes Tipo 2",
    version="1.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Handlers globales de error ────────────────────────────────────────────────
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Error 422 — datos de entrada inválidos o fuera de rango clínico."""
    errors = []
    for err in exc.errors():
        field = ".".join(str(loc) for loc in err["loc"] if loc != "body")
        errors.append({"campo": field or "desconocido", "mensaje": err["msg"]})

    logger.warning(
        "Validación fallida en %s — %d error(es): %s",
        request.url.path, len(errors), errors
    )
    return JSONResponse(
        status_code=422,
        content={
            "error": "Error de validación",
            "detalle": "Uno o más campos tienen valores inválidos o fuera del rango clínico aceptado.",
            "campos": errors,
        },
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Error 500 — fallo interno no controlado."""
    logger.error(
        "Error interno en %s: %s\n%s",
        request.url.path, exc, traceback.format_exc()
    )
    return JSONResponse(
        status_code=500,
        content={
            "error": "Error interno del servidor",
            "detalle": "Se produjo un error inesperado. Consulta los logs del servidor para más información.",
        },
    )


# ── Endpoints ─────────────────────────────────────────────────────────────────
@app.get("/health", response_model=HealthResponse)
def health():
    logger.debug("Health check solicitado")
    return HealthResponse(status="ok", model="Random Forest", threshold=threshold)


@app.post("/predict", response_model=PredictionOutput)
def predict(data: PredictionInput):
    t_start = time.perf_counter()

    input_values = data.model_dump()
    logger.info("Predicción solicitada — entrada: %s", input_values)

    try:
        features = np.array([[getattr(data, col) for col in FEATURE_ORDER]])
        features_scaled = scaler.transform(features)
        proba = float(model.predict_proba(features_scaled)[0][1])
    except Exception as e:
        logger.error("Error durante la inferencia: %s\n%s", e, traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error durante la predicción: {e}")

    if proba < 0.3:
        nivel, color = "riesgo_bajo", "verde"
    elif proba <= threshold:
        nivel, color = "riesgo_moderado", "amarillo"
    else:
        nivel, color = "riesgo_alto", "rojo"

    elapsed_ms = (time.perf_counter() - t_start) * 1000
    _record_prediction(nivel, elapsed_ms)

    logger.info(
        "Predicción completada — resultado: %s (%.1f%%) en %.2f ms",
        nivel, proba * 100, elapsed_ms
    )

    return PredictionOutput(
        probabilidad=round(proba, 4),
        nivel_riesgo=nivel,
        color=color,
        mensaje=MESSAGES[nivel],
        advertencia=ADVERTENCIA,
    )


@app.get("/metrics", response_model=MetricsResponse)
def metrics():
    """Estadísticas de uso desde el último arranque del servidor."""
    tiempos = _metrics["tiempos_respuesta_ms"]
    media_ms = round(sum(tiempos) / len(tiempos), 2) if tiempos else 0.0

    logger.debug(
        "Métricas consultadas — total=%d, media=%.2f ms",
        _metrics["total_predicciones"], media_ms
    )

    return MetricsResponse(
        total_predicciones=_metrics["total_predicciones"],
        distribucion=dict(_metrics["distribucion"]),
        tiempo_medio_respuesta_ms=media_ms,
    )


if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
