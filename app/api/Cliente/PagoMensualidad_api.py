from fastapi import APIRouter, HTTPException, status
from app.domain.Cliente.PagoMensualidad_domain import (
    PagoMensualidadCreate,
    PagoMensualidadResponse,
    MetodoPagoResponse,
    METODOS_CON_TARJETA,
)
from app.repository.Cliente.PagoMensualidad_repository import pago_mensualidad_repository
from app.repository.Cliente.procesarplanes_repository import procesar_planes_repository
from app.services.Cliente.PagoMensualidad_services import PagoMensualidadService
from typing import Optional

router = APIRouter(
    prefix="/api/pagos",
    tags=["Pago Mensualidad"],
)

service = PagoMensualidadService(
    repo        = pago_mensualidad_repository,
    planes_repo = procesar_planes_repository,
)


# ── Simulación de pasarela de pago ───────────────────────────
def _pasarela_pago(numero_tarjeta: Optional[str], monto: float) -> str:
    """
    Simula pasarela de pago.
    Solo se invoca cuando el método requiere tarjeta (TARJETA, PSE).
    En producción: reemplazar por integración real con la pasarela.
    """
    if numero_tarjeta == "0000000000000000":
        return "RECHAZADO"
    return "APROBADO"


# ── GET /api/pagos/metodos ────────────────────────────────────
@router.get("/metodos", response_model=list[MetodoPagoResponse])
def listar_metodos_pago():
    """Retorna la lista de métodos de pago habilitados con su flag requiereTarjeta."""
    return service.listar_metodos()


# ── POST /api/pagos ───────────────────────────────────────────
@router.post("/", response_model=PagoMensualidadResponse,
             status_code=status.HTTP_201_CREATED)
def procesar_pago(datos: PagoMensualidadCreate):
    """
    Procesa el pago de la mensualidad.
    - TARJETA / PSE: requiere numeroTarjeta de 16 dígitos.
    - EFECTIVO: no requiere numeroTarjeta.
    """
    try:
        return service.procesar_pago(datos, _pasarela_pago)
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="PAY_PAYMENT_DECLINED",
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
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
            detail=str(e),
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
            detail=str(e),
        )