from fastapi import APIRouter, HTTPException, status
from app.domain.Entrenador.GestionHorarios_domain import GestionHorariosCreate, GestionHorariosResponse
from app.repository.Entrenador.GestionHorarios_repository import gestion_horarios_repository
from app.repository.Cliente.ReservaSesion_repository import reserva_sesion_repository
from app.services.Entrenador.GestionHorarios_services import GestionHorariosService

router = APIRouter(
    prefix="/api/horarios",
    tags=["Gestión de Horarios"],
)

service = GestionHorariosService(
    repo         = gestion_horarios_repository,
    reserva_repo = reserva_sesion_repository,
)


# ── POST /api/horarios/disponibilidad ─────────────────────────
@router.post("/disponibilidad", response_model=GestionHorariosResponse,
             status_code=status.HTTP_201_CREATED)
def publicar_disponibilidad(datos: GestionHorariosCreate):
    """Publica o actualiza la disponibilidad semanal del entrenador."""
    try:
        return service.publicar_disponibilidad(datos)
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# ── GET /api/horarios/{id_entrenador} ─────────────────────────
@router.get("/{id_entrenador}", response_model=GestionHorariosResponse)
def obtener_horario(id_entrenador: int):
    """Retorna el horario de disponibilidad de un entrenador."""
    try:
        return service.obtener_horario(id_entrenador)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
