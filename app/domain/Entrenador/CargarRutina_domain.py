# ─────────────────────────────────────────────────────────────
# CAPA DOMAIN — modelos de datos y reglas de validación
# ─────────────────────────────────────────────────────────────

from pydantic import BaseModel, Field
from typing import List


class EjercicioCreate(BaseModel):
    nombre:       str = Field(..., min_length=1, description="Nombre del ejercicio")
    series:       int = Field(..., gt=0,         description="Número de series")
    repeticiones: int = Field(..., gt=0,         description="Número de repeticiones")


class RutinaCreate(BaseModel):
    """
    Body que recibe el endpoint.
    idEntrenador NO viene aquí — se extrae del token de sesión.
    La lista puede llegar vacía desde el cliente; la validación
    de negocio se hace en el service para devolver el error correcto.
    """
    nombre:     str                   = Field(..., min_length=1, description="Nombre de la rutina")
    ejercicios: List[EjercicioCreate] = Field(default=[], description="Lista de ejercicios")


# ── Respuestas según contrato .md ─────────────────────────────

class RutinaData(BaseModel):
    idRutina:        int
    nombre:          str
    totalEjercicios: int


class RutinaResponse(BaseModel):
    success: bool  = True
    message: str   = "Rutina cargada exitosamente"
    data:    RutinaData


class ErrorDetail(BaseModel):
    error_code: str
    details:    str
    timestamp:  str


class ErrorResponse(BaseModel):
    success:    bool = False
    statusCode: int
    message:    str
    error:      ErrorDetail