from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
from app.domain.Pagos.ProcesarFactura_domain import FacturaCreate
from app.repository.Pagos.ProcesarFactura_repository import procesar_factura_repository
from app.services.Pagos.ProcesarFactura_service import ProcesarFacturaService

router = APIRouter(
    prefix="/api/pagos/facturas",
    tags=["Procesar Factura"],
)

service = ProcesarFacturaService(repo=procesar_factura_repository)


# ── Helpers ───────────────────────────────────────────────────
def _ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")

def _error(status_code: int, message: str, error_code: str, details: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "success":    False,
            "statusCode": status_code,
            "message":    message,
            "error": {
                "error_code": error_code,
                "details":    details,
                "timestamp":  _ts(),
            },
        }
    )


# ── POST /api/pagos/facturas ──────────────────────────────────
@router.post("/")
def generar_factura(datos: FacturaCreate):
    """Genera una factura electrónica para un pago aprobado."""
    try:
        factura = service.generar_factura(datos)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "success": True,
                "message": "Factura generada correctamente",
                "data":    factura.model_dump(),
            }
        )
    except ValueError as e:
        if str(e) == "PAY_PAYMENT_NOT_FOUND":
            return _error(404, "Pago no encontrado", "PAY_PAYMENT_NOT_FOUND",
                          "No existe un pago aprobado con el ID proporcionado")
        return _error(500, "Error interno", "PAY_INTERNAL_ERROR",
                      "Ocurrió un error inesperado al generar la factura")


# ── GET /api/pagos/facturas/{id_factura} ──────────────────────
@router.get("/{id_factura}")
def obtener_factura(id_factura: str):
    """Consulta y descarga una factura existente por su ID."""
    try:
        factura = service.obtener_factura(id_factura)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "message": "Factura obtenida correctamente",
                "data":    factura.model_dump(),
            }
        )
    except ValueError:
        return _error(404, "Factura no encontrada", "PAY_INVOICE_NOT_FOUND",
                      "No existe una factura con el ID proporcionado")