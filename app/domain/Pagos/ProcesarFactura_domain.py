from pydantic import BaseModel, Field


# ─────────────────────────────────────────────────────────────
# CAPA DOMAIN — modelos de datos
# ─────────────────────────────────────────────────────────────


class FacturaCreate(BaseModel):
    """Body que recibe el endpoint POST /api/pagos/facturas."""
    idPago:    str = Field(..., description="ID del pago. Formato: PAY-XXXXXX")
    idCliente: int = Field(..., description="ID del cliente dueño del pago")


class FacturaData(BaseModel):
    idFactura:   str
    idPago:      str
    monto:       float
    fecha:       str
    plan:        str
    nombreCliente: str
    urlDescarga: str   # Formato: /facturas/FAC-XXXXXX.pdf (referencia, no archivo real)


class FacturaResponse(BaseModel):
    success: bool      = True
    message: str       = "Factura generada correctamente"
    data:    FacturaData


class ErrorDetail(BaseModel):
    error_code: str
    details:    str
    timestamp:  str


class ErrorResponse(BaseModel):
    success:    bool = False
    statusCode: int
    message:    str
    error:      ErrorDetail