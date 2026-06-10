# ─────────────────────────────────────────────────────────────
# CAPA API — router de FastAPI
# ─────────────────────────────────────────────────────────────

from datetime import datetime
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.domain.Pagos.ProcesarFactura_domain                import FacturaCreate, FacturaResponse, ErrorResponse, ErrorDetail
from app.repository.Pagos.ProcesarFactura_repository        import procesar_factura_repository
from app.services.Pagos.ProcesarFactura_service             import ProcesarFacturaService

router          = APIRouter(prefix="/pagos/facturas", tags=["Facturas"])
factura_service = ProcesarFacturaService(repo=procesar_factura_repository)


# ── Helpers ───────────────────────────────────────────────────

def _timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def _error_response(status_code: int, message: str, error_code: str, details: str) -> JSONResponse:
    body = ErrorResponse(
        statusCode = status_code,
        message    = message,
        error      = ErrorDetail(
            error_code = error_code,
            details    = details,
            timestamp  = _timestamp(),
        ),
    )
    return JSONResponse(status_code=status_code, content=body.model_dump())


_ERROR_MAP = {
    "PAY_PAYMENT_NOT_FOUND": (404, "Pago no encontrado",    "No existe un pago aprobado con el ID proporcionado"),
    "PAY_INVOICE_NOT_FOUND": (404, "Factura no encontrada", "No existe una factura con el ID proporcionado"),
}


# ── Endpoints ─────────────────────────────────────────────────

@router.post(
    "",
    response_model=FacturaResponse,
    status_code=201,
    responses={
        404: {"model": ErrorResponse, "description": "Pago no encontrado o no aprobado"},
    },
)
def generar_factura(datos: FacturaCreate):
    """
    Genera la factura electrónica de un pago aprobado.

    - Si ya existe factura para ese pago, la retorna sin crear duplicado.
    - El pago debe estar en estado **APROBADO** y pertenecer al `idCliente` enviado.
    """
    try:
        return factura_service.generar_factura(datos)
    except ValueError as e:
        codigo = str(e)
        status, message, details = _ERROR_MAP.get(codigo, (400, "Error de validación", codigo))
        return _error_response(status, message, codigo, details)


@router.get(
    "/{id_factura}",
    response_model=FacturaResponse,
    status_code=200,
    responses={
        404: {"model": ErrorResponse, "description": "Factura no encontrada"},
    },
)
def consultar_factura(id_factura: str):
    """
    Consulta los datos de una factura por su ID.

    Retorna toda la información: monto, plan, fecha y nombre del cliente.
    """
    try:
        return factura_service.obtener_factura(id_factura)
    except ValueError as e:
        codigo = str(e)
        status, message, details = _ERROR_MAP.get(codigo, (404, "No encontrado", codigo))
        return _error_response(status, message, codigo, details)