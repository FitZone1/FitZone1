# ─────────────────────────────────────────────────────────────
# CAPA DOMAIN — modelos de datos y reglas de validación
# ─────────────────────────────────────────────────────────────

from pydantic import BaseModel, Field, field_validator
from typing import Literal


DIAS_VALIDOS = {"LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES", "SÁBADO", "DOMINGO"}


class AsignarRutinaCreate(BaseModel):
    idRutina:     int = Field(..., gt=0, description="ID de la rutina a asignar")
    idEntrenador: int = Field(..., gt=0, description="ID del entrenador autenticado")
    diaSemana:    str = Field(..., description="Día de la semana: LUNES, MARTES, MIÉRCOLES, JUEVES, VIERNES, SÁBADO, DOMINGO")

    @field_validator("diaSemana")
    @classmethod
    def dia_valido(cls, v):
        if v.upper() not in DIAS_VALIDOS:
            raise ValueError(f"Valor no permitido para diaSemana. Use uno de: {sorted(DIAS_VALIDOS)}")
        return v.upper()


# ── Respuestas según contrato .md ─────────────────────────────

class AsignarRutinaData(BaseModel):
    idRutina:  int
    nombre:    str
    diaSemana: str


class AsignarRutinaResponse(BaseModel):
    success: bool             = True
    message: str              = "Rutina asignada correctamente"
    data:    AsignarRutinaData


class ErrorDetail(BaseModel):
    error_code: str
    details:    str
    timestamp:  str


class ErrorResponse(BaseModel):
    success:    bool = False
    statusCode: int
    message:    str
    error:      ErrorDetail