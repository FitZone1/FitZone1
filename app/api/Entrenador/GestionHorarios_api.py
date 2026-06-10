from fastapi import APIRouter, Path, status
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
from app.domain.Entrenador.GestionHorarios_domain import GestionHorariosCreate
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


def _ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")


def _error(status_code: int, message: str, error_code: str, details: str):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "statusCode": status_code,
            "message": message,
            "error": {
                "error_code": error_code,
                "details": details,
                "timestamp": _ts(),
            }
        }
    )


# ── POST /api/horarios/disponibilidad ─────────────────────────
@router.post(
    "/disponibilidad",
    summary="Publicar Disponibilidad",
    description="Publica la disponibilidad semanal del entrenador con días, hora de inicio y hora de fin.",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Disponibilidad publicada correctamente"},
        400: {"description": "Rango horario inválido"},
    },
)
def publicar_disponibilidad(datos: GestionHorariosCreate):
    try:
        horario = service.publicar_disponibilidad(datos)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "success": True,
                "message": "Disponibilidad publicada correctamente",
                "data": horario.model_dump(),
            }
        )
    except ValueError as e:
        codigo = str(e)
        if codigo == "HOR_INVALID_TIME_RANGE":
            return _error(400, "Rango horario inválido", "HOR_INVALID_TIME_RANGE",
                          "La hora de inicio no puede ser mayor a la hora de fin")
        return _error(400, "Solicitud inválida", "HOR_BAD_REQUEST", codigo)


# ── GET /api/horarios/{id_entrenador} ─────────────────────────
@router.get(
    "/{id_entrenador}",
    summary="Obtener Horario",
    description="Retorna el horario de disponibilidad registrado para un entrenador.",
    responses={
        200: {"description": "Horario obtenido correctamente"},
        404: {"description": "Horario no encontrado"},
    },
)
def obtener_horario(
    id_entrenador: int = Path(..., gt=0, description="ID del entrenador"),
):
    try:
        horario = service.obtener_horario(id_entrenador)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "message": "Horario obtenido correctamente",
                "data": horario.model_dump(),
            }
        )
    except ValueError:
        return _error(404, "Horario no encontrado", "HOR_NOT_FOUND",
                      "No existe un horario de disponibilidad para el entrenador indicado")