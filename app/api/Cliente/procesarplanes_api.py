from fastapi import APIRouter, HTTPException, status
from app.domain.Cliente.procesarplanes_domain import SuscribirPlanCreate, PlanResponse, SuscripcionResponse
from app.repository.Cliente.procesarplanes_repository import procesar_planes_repository
from app.services.Cliente.procesarplanes_services import ProcesarPlanesService

router = APIRouter(
    prefix="/api/pagos/planes",
    tags=["Procesar Planes"],
)

service = ProcesarPlanesService(repo=procesar_planes_repository)


# ── GET /api/pagos/planes ─────────────────────────────────────
@router.get("/", response_model=list[PlanResponse])
def listar_planes():
    """Retorna todos los planes de suscripción activos."""
    try:
        return service.listar_planes()
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


# ── POST /api/pagos/planes/suscribir ─────────────────────────
@router.post("/suscribir", response_model=SuscripcionResponse,
             status_code=status.HTTP_201_CREATED)
def suscribir_plan(datos: SuscribirPlanCreate):
    """Suscribe al cliente a un plan de membresía."""
    try:
        return service.suscribir(datos)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


# ── GET /api/pagos/planes/cliente/{id_cliente} ────────────────
@router.get("/cliente/{id_cliente}", response_model=SuscripcionResponse)
def obtener_suscripcion(id_cliente: int):
    """Retorna la suscripción activa de un cliente."""
    try:
        return service.obtener_suscripcion(id_cliente)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
