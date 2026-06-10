# ─────────────────────────────────────────────────────────────
# CAPA API — router de FastAPI
# ─────────────────────────────────────────────────────────────

from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import JSONResponse

from app.domain.Pagos.ProcesarFactura_domain         import FacturaCreate, FacturaResponse, ErrorResponse, ErrorDetail
from app.repository.Pagos.ProcesarFactura_repository import pago_repository, factura_repository
from app.repository.iniciosesion.iniciosesion_repositories import sesion_repository
from app.services.Pagos.ProcesarFactura_service       import FacturaService

router          = APIRouter(prefix="/pagos/facturas", tags=["Facturas"])
factura_service = FacturaService(pago_repository, factura_repository)


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


# ── Dependencia: valida token y rol ──────────────────────────

def _validar_cliente(token: str, rol: str) -> int:
    """Verifica que el token sea válido y que el rol sea CLIENTE."""
    if rol != "CLIENTE":
        return _error_response(
            403, "Acceso denegado", "AUTH_UNAUTHORIZED",
            "Solo los clientes pueden acceder a sus facturas",
        )

    sesion = sesion_repository.obtener_por_token(token)
    if not sesion:
        raise HTTPException(status_code=401, detail="Token inválido o sesión expirada")

    return sesion.id_usuario


# ── Endpoints ─────────────────────────────────────────────────

@router.post(
    "",
    response_model=FacturaResponse,
    status_code=201,
    responses={
        404: {"model": ErrorResponse, "description": "Pago no encontrado o no aprobado"},
        401: {"description": "Token inválido o sesión expirada"},
        403: {"model": ErrorResponse, "description": "Acceso denegado — solo CLIENTE"},
    },
)
def generar_factura(
    datos:         FacturaCreate,
    token:         Annotated[str, Header(description="Token obtenido al iniciar sesión")],
    x_rol_usuario: Annotated[str, Header(description="Rol del usuario. Debe ser: CLIENTE")],
):
    """
    Genera la factura electrónica de un pago aprobado.

    - Si ya existe factura para ese pago, la retorna sin crear duplicado.
    - El pago debe estar en estado **APROBADO** y pertenecer al `idCliente` enviado.

    **Headers requeridos:**
    - `token`: token obtenido al iniciar sesión
    - `x-rol-usuario`: debe ser `CLIENTE`
    """
    resultado = _validar_cliente(token, x_rol_usuario)
    if isinstance(resultado, JSONResponse):
        return resultado

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
        401: {"description": "Token inválido o sesión expirada"},
        403: {"model": ErrorResponse, "description": "Acceso denegado — solo CLIENTE"},
    },
)
def consultar_factura(
    id_factura:    str,
    token:         Annotated[str, Header(description="Token obtenido al iniciar sesión")],
    x_rol_usuario: Annotated[str, Header(description="Rol del usuario. Debe ser: CLIENTE")],
):
    """
    Consulta los datos de una factura por su ID.

    Retorna toda la información de la factura: monto, plan, fecha, cliente y URL de referencia.

    **Headers requeridos:**
    - `token`: token obtenido al iniciar sesión
    - `x-rol-usuario`: debe ser `CLIENTE`
    """
    resultado = _validar_cliente(token, x_rol_usuario)
    if isinstance(resultado, JSONResponse):
        return resultado

    try:
        return factura_service.consultar_factura(id_factura)
    except ValueError as e:
        codigo = str(e)
        status, message, details = _ERROR_MAP.get(codigo, (404, "No encontrado", codigo))
        return _error_response(status, message, codigo, details)