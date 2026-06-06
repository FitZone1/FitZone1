from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from typing import Optional
from datetime import datetime, timezone
from app.domain.Entrenador.EntrenadoresDisponibles_domain import EntrenadorDisponibleResponse
from app.repository.Entrenador.EntrenadoresDisponibles_repository import entrenadores_disponibles_repository
from app.services.Entrenador.EntrenadoresDisponibles_services import EntrenadoresDisponiblesService

router = APIRouter(
    prefix="/api/reservas",
    tags=["Entrenadores Disponibles"],
)

service = EntrenadoresDisponiblesService(repo=entrenadores_disponibles_repository)


def _ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")


# ── GET /api/reservas/entrenadores ────────────────────────────
@router.get("/entrenadores")
def listar_entrenadores_disponibles(
    especialidad: Optional[str] = None,
    disponible:   Optional[bool] = True,
):
    """
    Retorna entrenadores disponibles.
    - Sin parámetros: todos los disponibles.
    - ?especialidad=X: filtra por especialidad entre los disponibles.
    """
    try:
        entrenadores = service.listar_disponibles(
            especialidad=especialidad,
            disponible=disponible,
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "message": "Entrenadores encontrados correctamente",
                "data": [e.model_dump() for e in entrenadores],
            }
        )
    except ValueError:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "statusCode": 404,
                "message": "Sin resultados",
                "error": {
                    "error_code": "RES_TRAINERS_NOT_FOUND",
                    "details": "No se encontraron entrenadores con los filtros seleccionados",
                    "timestamp": _ts(),
                }
            }
        )