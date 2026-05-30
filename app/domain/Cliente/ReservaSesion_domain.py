from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


# ── Schema de ENTRADA ─────────────────────────────────────────
class ReservaSesionCreate(BaseModel):
    idCliente:    int = Field(..., gt=0, description="ID del cliente que reserva")
    idEntrenador: int = Field(..., gt=0, description="ID del entrenador a reservar")
    fecha:        str = Field(..., description="Fecha y hora de la sesión (ISO 8601)")
    idZona:       int = Field(..., gt=0, description="ID de la zona del gimnasio")

    @field_validator("fecha")
    @classmethod
    def fecha_valida(cls, v):
        try:
            datetime.fromisoformat(v)
        except ValueError:
            raise ValueError("La fecha debe tener formato ISO 8601: YYYY-MM-DDTHH:MM:SS")
        return v


# ── Schema de SALIDA ──────────────────────────────────────────
class ReservaSesionResponse(BaseModel):
    idReserva:    int
    estado:       str
    fecha:        str
    idEntrenador: int
    idCliente:    int

    class Config:
        from_attributes = True


# ── Modelo interno del dominio ────────────────────────────────
class Reserva:
    ESTADOS_VALIDOS = {"CONFIRMADA", "CANCELADA", "COMPLETADA"}

    def __init__(self, id: int, id_cliente: int, id_entrenador: int,
                 fecha: str, id_zona: int, estado: str = "CONFIRMADA"):
        self.id            = id
        self.id_cliente    = id_cliente
        self.id_entrenador = id_entrenador
        self.fecha         = fecha
        self.id_zona       = id_zona
        self.estado        = estado

    # REGLA DE NEGOCIO: solo se puede cancelar si está CONFIRMADA
    def puede_cancelarse(self) -> bool:
        return self.estado == "CONFIRMADA"

    # REGLA DE NEGOCIO: no se puede reservar si ya está completada
    def esta_completada(self) -> bool:
        return self.estado == "COMPLETADA"

    def to_response(self) -> dict:
        return {
            "idReserva":    self.id,
            "estado":       self.estado,
            "fecha":        self.fecha,
            "idEntrenador": self.id_entrenador,
            "idCliente":    self.id_cliente,
        }
