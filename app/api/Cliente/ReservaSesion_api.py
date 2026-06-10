from fastapi import APIRouter, Path, Query, status
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
from app.domain.Cliente.ReservaSesion_domain import ReservaSesionCreate
from app.repository.Cliente.ReservaSesion_repository import reserva_sesion_repository
from app.services.Cliente.ReservaSesion_services import ReservaSesionService

router = APIRouter(
    prefix="/api/reservas",
    tags=["Reserva Sesión"],
)

service = ReservaSesionService(repo=reserva_sesion_repository)


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


# ── Crear reserva ─────────────────────────────────────────────
@router.post(
    "",
    summary="Crear una nueva reserva de sesión",
    description="Crea una reserva con estado CONFIRMADA. Valida conflictos de horario y capacidad máxima del entrenador.",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Reserva creada correctamente"},
        409: {"description": "Horario no disponible o capacidad máxima alcanzada"},
    },
)
def crear_reserva(datos: ReservaSesionCreate):
    try:
        reserva = service.crear_reserva(datos)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "success": True,
                "message": "Reserva creada correctamente",
                "data": reserva.model_dump(),
            }
        )
    except ValueError as e:
        codigo = str(e)
        if codigo == "RES_SCHEDULE_CONFLICT":
            return _error(409, "Horario no disponible", "RES_SCHEDULE_CONFLICT",
                          "El entrenador ya tiene una sesión asignada en ese horario")
        if codigo == "RES_MAX_CAPACITY_REACHED":
            return _error(409, "Capacidad máxima alcanzada", "RES_MAX_CAPACITY_REACHED",
                          "El entrenador ya alcanzó el máximo de clientes para ese día")
        return _error(400, "Solicitud inválida", "RES_BAD_REQUEST", codigo)


# ── Consultar disponibilidad del entrenador ───────────────────
@router.get(
    "/disponibilidad",
    summary="Consultar disponibilidad del entrenador",
    description=(
        "Indica si el entrenador tiene disponibilidad en la fecha y hora indicadas. "
        "Formato: `YYYY-MM-DDTHH:MM:SS`."
    ),
    responses={
        200: {"description": "Consulta realizada correctamente"},
    },
)
def consultar_disponibilidad(
    idEntrenador: int = Query(..., gt=0, description="ID del entrenador"),
    fecha: str = Query(..., description="Fecha y hora a consultar (YYYY-MM-DDTHH:MM:SS)"),
):
    ocupado = reserva_sesion_repository.existe_conflicto(idEntrenador, fecha)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "message": "Consulta realizada correctamente",
            "data": {
                "idEntrenador": idEntrenador,
                "fecha":        fecha,
                "disponible":   not ocupado,
            }
        }
    )


# ── Obtener reserva por ID ────────────────────────────────────
@router.get(
    "/{idReserva}",
    summary="Obtener detalle de una reserva por ID",
    description=(
        "Retorna el detalle completo de una reserva dado su ID. "
        "Si no existe, retorna HTTP 404 con `RES_ID_NOT_FOUND`."
    ),
    responses={
        200: {"description": "Detalle de la reserva"},
        404: {"description": "Reserva no encontrada"},
    },
)
def obtener_reserva(
    idReserva: int = Path(..., gt=0, description="ID de la reserva a consultar"),
):
    try:
        reserva = service.obtener(idReserva)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "message": "Reserva obtenida correctamente",
                "data": reserva.model_dump(),
            }
        )
    except ValueError:
        return _error(404, "Reserva no encontrada", "RES_ID_NOT_FOUND",
                      "No existe una reserva con el ID proporcionado")