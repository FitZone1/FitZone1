from fastapi import APIRouter, HTTPException, status
from app.domain.Cliente.ReservaSesion_domain import ReservaSesionCreate, ReservaSesionResponse
from app.repository.Cliente.ReservaSesion_repository import reserva_sesion_repository
from app.services.Cliente.ReservaSesion_services import ReservaSesionService

router = APIRouter(
    prefix="/api/reservas",
    tags=["Reserva Sesión"],
)

service = ReservaSesionService(repo=reserva_sesion_repository)


# ── POST /api/reservas ────────────────────────────────────────
@router.post("/", response_model=ReservaSesionResponse,
             status_code=status.HTTP_201_CREATED)
def crear_reserva(datos: ReservaSesionCreate):
    """Crea una nueva reserva de sesión de entrenamiento."""
    try:
        return service.crear_reserva(datos)
    except ValueError as e:
        codigo = str(e)
        if codigo in ("RES_SCHEDULE_CONFLICT", "RES_MAX_CAPACITY_REACHED"):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=codigo)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=codigo)


# ── GET /api/reservas ─────────────────────────────────────────
@router.get("/", response_model=list[ReservaSesionResponse])
def listar_reservas():
    """Retorna todas las reservas registradas."""
    return service.listar()


# ── GET /api/reservas/{id} ────────────────────────────────────
@router.get("/{id}", response_model=ReservaSesionResponse)
def obtener_reserva(id: int):
    """Retorna una reserva por su ID."""
    try:
        return service.obtener(id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
