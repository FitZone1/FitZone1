from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
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
        msg = str(e)
        if msg == "PAY_PAYMENT_NOT_FOUND":
            return _error(404, "Pago no encontrado", "PAY_PAYMENT_NOT_FOUND",
                          "No existe un pago aprobado con el ID proporcionado")
        return _error(500, "Error interno", "PAY_INTERNAL_ERROR",
                      "Ocurrió un error inesperado al generar la factura")
    except Exception:
        return _error(500, "Error interno del servidor", "PAY_INTERNAL_ERROR",
                      "Ocurrió un error inesperado. Intente más tarde.")


# ── Manejador de errores de validación (400) ──────────────────
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errores = [
        {"campo": ".".join(str(x) for x in e["loc"]), "mensaje": e["msg"]}
        for e in exc.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "success":    False,
            "statusCode": 400,
            "message":    "Parámetros inválidos",
            "error": {
                "error_code": "PAY_INVALID_PARAMS",
                "details":    errores,
                "timestamp":  _ts(),
            },
        }
    )


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