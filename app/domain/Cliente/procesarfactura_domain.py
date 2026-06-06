from pydantic import BaseModel, Field


# ── Schema de ENTRADA ─────────────────────────────────────────
class ProcesarFacturaCreate(BaseModel):
    idPago:    str = Field(..., description="ID del pago aprobado")
    idCliente: int = Field(..., gt=0, description="ID del cliente")


# ── Schema de SALIDA ──────────────────────────────────────────
class ProcesarFacturaResponse(BaseModel):
    idFactura:    str
    idPago:       str
    monto:        float
    fecha:        str
    urlDescarga:  str

    class Config:
        from_attributes = True


# ── Modelo interno del dominio ────────────────────────────────
class Factura:
    def __init__(self, id_factura: str, id_pago: str, id_cliente: int,
                 monto: float, fecha: str, url_descarga: str):
        self.id_factura   = id_factura
        self.id_pago      = id_pago
        self.id_cliente   = id_cliente
        self.monto        = monto
        self.fecha        = fecha
        self.url_descarga = url_descarga

    # REGLA DE NEGOCIO: la URL de descarga debe estar disponible
    def tiene_url_valida(self) -> bool:
        return bool(self.url_descarga and self.url_descarga.strip())

    def to_response(self) -> dict:
        return {
            "idFactura":   self.id_factura,
            "idPago":      self.id_pago,
            "monto":       self.monto,
            "fecha":       self.fecha,
            "urlDescarga": self.url_descarga,
        }
