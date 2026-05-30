from pydantic import BaseModel, Field
from typing import Optional


# ── Schema de ENTRADA ─────────────────────────────────────────
class CancelarReservaCreate(BaseModel):
    motivo: Optional[str] = Field(None, description="Motivo de la cancelación")


# ── Schema de SALIDA ──────────────────────────────────────────
class CancelarReservaResponse(BaseModel):
    idReserva: int
    estado:    str   # siempre "CANCELADA"

    class Config:
        from_attributes = True


# ── Modelo interno del dominio ────────────────────────────────
class CancelacionReserva:
    def __init__(self, id_reserva: int, estado_actual: str):
        self.id_reserva    = id_reserva
        self.estado_actual = estado_actual

    # REGLA DE NEGOCIO: solo se puede cancelar si está CONFIRMADA
    def puede_cancelarse(self) -> bool:
        return self.estado_actual == "CONFIRMADA"

    # REGLA DE NEGOCIO: no se puede cancelar si ya fue completada
    def ya_completada(self) -> bool:
        return self.estado_actual == "COMPLETADA"

    def to_response(self) -> dict:
        return {
            "idReserva": self.id_reserva,
            "estado":    "CANCELADA",
        }
