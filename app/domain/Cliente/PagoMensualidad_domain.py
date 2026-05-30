from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


# ── Schema de ENTRADA ─────────────────────────────────────────
class PagoMensualidadCreate(BaseModel):
    idCliente:     int = Field(..., gt=0, description="ID del cliente que realiza el pago")
    idPlan:        int = Field(..., gt=0, description="ID del plan a pagar")
    metodoPago:    str = Field(..., description="Método de pago (TARJETA, PSE, etc.)")
    numeroTarjeta: str = Field(..., min_length=16, max_length=16, description="Número de tarjeta de 16 dígitos")

    @field_validator("numeroTarjeta")
    @classmethod
    def tarjeta_solo_digitos(cls, v):
        if not v.isdigit():
            raise ValueError("El número de tarjeta solo puede contener dígitos")
        return v

    @field_validator("metodoPago")
    @classmethod
    def metodo_valido(cls, v):
        metodos = {"TARJETA", "PSE", "EFECTIVO"}
        if v.upper() not in metodos:
            raise ValueError(f"Método de pago no válido. Use: {metodos}")
        return v.upper()


# ── Schema de SALIDA ──────────────────────────────────────────
class PagoMensualidadResponse(BaseModel):
    idPago:  str
    monto:   float
    estado:  str
    fecha:   str

    class Config:
        from_attributes = True


# ── Modelo interno del dominio ────────────────────────────────
class Pago:
    ESTADOS_VALIDOS = {"APROBADO", "RECHAZADO", "PENDIENTE"}

    def __init__(self, id_pago: str, id_cliente: int, id_plan: int,
                 monto: float, estado: str, fecha: str):
        self.id_pago    = id_pago
        self.id_cliente = id_cliente
        self.id_plan    = id_plan
        self.monto      = monto
        self.estado     = estado
        self.fecha      = fecha

    # REGLA DE NEGOCIO: solo pagos APROBADOS renuevan la suscripción
    def esta_aprobado(self) -> bool:
        return self.estado == "APROBADO"

    # REGLA DE NEGOCIO: el monto debe ser mayor a 0
    def monto_valido(self) -> bool:
        return self.monto > 0

    def to_response(self) -> dict:
        return {
            "idPago":  self.id_pago,
            "monto":   self.monto,
            "estado":  self.estado,
            "fecha":   self.fecha,
        }
