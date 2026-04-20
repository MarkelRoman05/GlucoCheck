from pydantic import BaseModel, field_validator, model_validator
from typing import Literal

# Rangos clínicos válidos para cada variable
FIELD_RANGES = {
    "pregnancies":       (0,    17,   "Número de embarazos"),
    "glucose":           (44,   199,  "Glucosa en ayunas (mg/dL)"),
    "blood_pressure":    (24,   122,  "Presión arterial diastólica (mmHg)"),
    "skin_thickness":    (7,    99,   "Grosor del pliegue cutáneo (mm)"),
    "insulin":           (0,    846,  "Insulina sérica (μU/mL)"),
    "bmi":               (18.0, 67.0, "Índice de masa corporal"),
    "diabetes_pedigree": (0.08, 2.42, "Función pedigrí diabetes"),
    "age":               (21,   81,   "Edad (años)"),
}


def _validate_range(field: str, value: float) -> float:
    low, high, label = FIELD_RANGES[field]
    if value < low or value > high:
        raise ValueError(
            f"{label} fuera de rango clínico: se recibió {value}, "
            f"el rango válido es [{low}, {high}]."
        )
    return value


class PredictionInput(BaseModel):
    pregnancies: float
    glucose: float
    blood_pressure: float
    skin_thickness: float
    insulin: float
    bmi: float
    diabetes_pedigree: float
    age: float

    @field_validator("*", mode="before")
    @classmethod
    def must_be_numeric(cls, v):
        try:
            return float(v)
        except (TypeError, ValueError):
            raise ValueError("Todos los campos deben ser numéricos")

    @field_validator("pregnancies")
    @classmethod
    def validate_pregnancies(cls, v: float) -> float:
        return _validate_range("pregnancies", v)

    @field_validator("glucose")
    @classmethod
    def validate_glucose(cls, v: float) -> float:
        return _validate_range("glucose", v)

    @field_validator("blood_pressure")
    @classmethod
    def validate_blood_pressure(cls, v: float) -> float:
        return _validate_range("blood_pressure", v)

    @field_validator("skin_thickness")
    @classmethod
    def validate_skin_thickness(cls, v: float) -> float:
        return _validate_range("skin_thickness", v)

    @field_validator("insulin")
    @classmethod
    def validate_insulin(cls, v: float) -> float:
        return _validate_range("insulin", v)

    @field_validator("bmi")
    @classmethod
    def validate_bmi(cls, v: float) -> float:
        return _validate_range("bmi", v)

    @field_validator("diabetes_pedigree")
    @classmethod
    def validate_diabetes_pedigree(cls, v: float) -> float:
        return _validate_range("diabetes_pedigree", v)

    @field_validator("age")
    @classmethod
    def validate_age(cls, v: float) -> float:
        return _validate_range("age", v)


class PredictionOutput(BaseModel):
    probabilidad: float
    nivel_riesgo: Literal["riesgo_bajo", "riesgo_moderado", "riesgo_alto"]
    color: Literal["verde", "amarillo", "rojo"]
    mensaje: str
    advertencia: str


class HealthResponse(BaseModel):
    status: str
    model: str
    threshold: float


class MetricsResponse(BaseModel):
    total_predicciones: int
    distribucion: dict
    tiempo_medio_respuesta_ms: float
