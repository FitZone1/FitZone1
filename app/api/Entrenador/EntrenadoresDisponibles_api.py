from fastapi import APIRouter, HTTPException, status
from typing import Optional
from app.domain.Entrenador.EntrenadoresDisponibles_domain import EntrenadorDisponibleResponse
from app.repository.Entrenador.EntrenadoresDisponibles_repository import entrenadores_disponibles_repository
from app.services.Entrenador.EntrenadoresDisponibles_services import EntrenadoresDisponiblesService

router = APIRouter(
    prefix="/api/reservas",
    tags=["Entrenadores Disponibles"],
)

service = EntrenadoresDisponiblesService(repo=entrenadores_disponibles_repository)


# ── GET /api/reservas/entrenadores ────────────────────────────
@router.get("/entrenadores", response_model=list[EntrenadorDisponibleResponse])
def listar_entrenadores_disponibles(
    especialidad: Optional[str] = None,
    disponible:   Optional[bool] = True,
):
    """Retorna entrenadores disponibles. Filtra por especialidad opcionalmente."""
    try:
        return service.listar_disponibles(especialidad=especialidad)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
