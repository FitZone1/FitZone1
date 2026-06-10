from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime, timezone
import re


# ── Schema de ENTRADA — generar factura ──────────────────────
class FacturaCreate(BaseModel):
    idPago:    str = Field(..., description="ID del pago aprobado (ej: PAY-987654)")
    idCliente: int = Field(..., gt=0, description="ID del cliente")

    @field_validator("idPago")
    @classmethod
    def formato_id_pago(cls, v: str) -> str:
        if not re.fullmatch(r"PAY-\d{6}", v):
            raise ValueError("El idPago debe tener el formato PAY-XXXXXX (6 dígitos)")
        return v


# ── Schema de SALIDA — factura ────────────────────────────────
class FacturaResponse(BaseModel):
    idFactura:     str
    idPago:        str
    monto:         float
    fecha:         str
    urlDescarga:   str
    plan:          str
    nombreCliente: str

    class Config:
        from_attributes = True


# ── Modelo interno — Pago (referencia) ───────────────────────
class Pago:
    """Referencia mínima de un pago. El módulo de pagos real lo ampliaría."""
    def __init__(self, id_pago: str, id_cliente: int,
                 monto: float, estado: str, plan: str, nombre_cliente: str):
        self.id_pago        = id_pago
        self.id_cliente     = id_cliente
        self.monto          = monto
        self.estado         = estado   # "APROBADO" | "RECHAZADO" | "PENDIENTE"
        self.plan           = plan
        self.nombre_cliente = nombre_cliente

    # REGLA DE NEGOCIO: solo pagos APROBADOS generan factura
    def esta_aprobado(self) -> bool:
        return self.estado == "APROBADO"


# ── Modelo interno — Factura ──────────────────────────────────
class Factura:
    def __init__(self, id_factura: str, id_pago: str,
                 monto: float, fecha: str, url_descarga: str,
                 plan: str, nombre_cliente: str):
        self.id_factura     = id_factura
        self.id_pago        = id_pago
        self.monto          = monto
        self.fecha          = fecha
        self.url_descarga   = url_descarga
        self.plan           = plan
        self.nombre_cliente = nombre_cliente

    def to_response(self) -> dict:
        return {
            "idFactura":     self.id_factura,
            "idPago":        self.id_pago,
            "monto":         self.monto,
            "fecha":         self.fecha,
            "urlDescarga":   self.url_descarga,
            "plan":          self.plan,
            "nombreCliente": self.nombre_cliente,
        }