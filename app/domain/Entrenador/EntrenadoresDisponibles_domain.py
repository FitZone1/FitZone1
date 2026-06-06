from pydantic import BaseModel, Field, field_validator
from typing import Optional


# ── Schema de ENTRADA ─────────────────────────────────────────
class EntrenadoresDisponiblesFilter(BaseModel):
    especialidad: Optional[str] = Field(None, description="Filtro por especialidad")
    disponible:   Optional[bool] = Field(True, description="Filtro por disponibilidad")


# ── Schema de SALIDA ──────────────────────────────────────────
class EntrenadorDisponibleResponse(BaseModel):
    idEntrenador: int
    nombre:       str
    especialidad: str
    calificacion: float
    disponible:   bool

    class Config:
        from_attributes = True


# ── Modelo interno del dominio ────────────────────────────────
class EntrenadorDisponible:
    def __init__(self, id: int, nombre: str, especialidad: str,
                 calificacion: float, disponible: bool):
        self.id           = id
        self.nombre       = nombre
        self.especialidad = especialidad
        self.calificacion = calificacion
        self.disponible   = disponible

    # REGLA DE NEGOCIO: solo entrenadores disponibles se muestran
    def esta_disponible(self) -> bool:
        return self.disponible

    # REGLA DE NEGOCIO: calificación debe estar entre 0 y 5
    def calificacion_valida(self) -> bool:
        return 0.0 <= self.calificacion <= 5.0

    def to_response(self) -> dict:
        return {
            "idEntrenador": self.id,
            "nombre":       self.nombre,
            "especialidad": self.especialidad,
            "calificacion": self.calificacion,
            "disponible":   self.disponible,
        }