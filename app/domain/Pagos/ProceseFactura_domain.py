from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone


# ── Schema de ENTRADA — generar factura ──────────────────────
class FacturaCreate(BaseModel):
    idPago:    str = Field(..., description="ID del pago aprobado (ej: PAY-987654)")
    idCliente: int = Field(..., gt=0, description="ID del cliente")


# ── Schema de SALIDA — factura ────────────────────────────────
class FacturaResponse(BaseModel):
    idFactura:   str
    idPago:      str
    monto:       float
    fecha:       str
    urlDescarga: str

    class Config:
        from_attributes = True


# ── Modelo interno — Pago (referencia) ───────────────────────
class Pago:
    """Referencia mínima de un pago. El módulo de pagos real lo ampliaría."""
    def __init__(self, id_pago: str, id_cliente: int,
                 monto: float, estado: str, plan: str):
        self.id_pago    = id_pago
        self.id_cliente = id_cliente
        self.monto      = monto
        self.estado     = estado   # "APROBADO" | "RECHAZADO" | "PENDIENTE"
        self.plan       = plan

    # REGLA DE NEGOCIO: solo pagos APROBADOS generan factura
    def esta_aprobado(self) -> bool:
        return self.estado == "APROBADO"


# ── Modelo interno — Factura ──────────────────────────────────
class Factura:
    def __init__(self, id_factura: str, id_pago: str,
                 monto: float, fecha: str, url_descarga: str):
        self.id_factura   = id_factura
        self.id_pago      = id_pago
        self.monto        = monto
        self.fecha        = fecha
        self.url_descarga = url_descarga

    def to_response(self) -> dict:
        return {
            "idFactura":   self.id_factura,
            "idPago":      self.id_pago,
            "monto":       self.monto,
            "fecha":       self.fecha,
            "urlDescarga": self.url_descarga,
        }