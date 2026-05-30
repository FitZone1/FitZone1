# ─────────────────────────────────────────────────────────────
# CAPA API — rutas HTTP con FastAPI
# Solo recibe peticiones y llama al servicio.
# Aquí NO hay lógica de negocio.
# ─────────────────────────────────────────────────────────────

from fastapi import APIRouter, HTTPException, status
from app.domain.Cliente.PagoMensualidad_domain import PagoMensualidadCreate, PagoMensualidadResponse
from app.repository.Cliente.PagoMensualidad_repository import pago_mensualidad_repository
from app.repository.Cliente.procesarplanes_repository import procesar_planes_repository
from app.services.Cliente.PagoMensualidad_services import PagoMensualidadService

router = APIRouter(
    prefix="/api/pagos",
    tags=["Pago Mensualidad"],
)

service = PagoMensualidadService(
    repo        = pago_mensualidad_repository,
    planes_repo = procesar_planes_repository,
)


# ── Simulación de pasarela de pago ───────────────────────────
def _pasarela_pago(numero_tarjeta: str, monto: float) -> str:
    """Simula pasarela de pago. En producción: integración real."""
    return "APROBADO" if numero_tarjeta != "0000000000000000" else "RECHAZADO"


# ── POST /api/pagos ───────────────────────────────────────────
@router.post("/", response_model=PagoMensualidadResponse,
             status_code=status.HTTP_201_CREATED)
def procesar_pago(datos: PagoMensualidadCreate):
    """Procesa el pago de la mensualidad del cliente."""
    try:
        return service.procesar_pago(datos, _pasarela_pago)
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="PAY_PAYMENT_DECLINED"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


# ── GET /api/pagos/{id_pago} ──────────────────────────────────
@router.get("/{id_pago}", response_model=PagoMensualidadResponse)
def obtener_pago(id_pago: str):
    """Retorna un pago por su ID."""
    try:
        return service.obtener(id_pago)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


# ── GET /api/pagos/cliente/{id_cliente} ───────────────────────
@router.get("/cliente/{id_cliente}", response_model=list[PagoMensualidadResponse])
def pagos_por_cliente(id_cliente: int):
    """Retorna todos los pagos de un cliente."""
    try:
        return service.listar_por_cliente(id_cliente)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
