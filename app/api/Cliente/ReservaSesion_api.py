from fastapi import APIRouter, Path, Query, status
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
from app.domain.Cliente.ReservaSesion_domain import ReservaSesionCreate
from app.repository.Cliente.ReservaSesion_repository import reserva_sesion_repository
from app.services.Cliente.ReservaSesion_services import ReservaSesionService, MAX_CLIENTES_POR_DIA

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


# ── CASO 1: Crear reserva ─────────────────────────────────────
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


# ── CASO 3 y 4: Consultar capacidad del entrenador ────────────
@router.get(
    "/capacidad",
    summary="Consultar capacidad del entrenador en una fecha",
    description=(
        "Retorna cuántas reservas tiene el entrenador en la fecha indicada "
        "y cuántos lugares quedan disponibles. "
        "Formato de fecha: `YYYY-MM-DD`."
    ),
    responses={
        200: {"description": "Capacidad consultada correctamente"},
    },
)
def consultar_capacidad(
    idEntrenador: int = Query(..., gt=0, description="ID del entrenador"),
    fecha: str = Query(..., description="Fecha a consultar (YYYY-MM-DD)"),
):
    reservas_actuales = reserva_sesion_repository.contar_reservas_dia(idEntrenador, fecha + "T00:00:00")
    lugares_disponibles = max(0, MAX_CLIENTES_POR_DIA - reservas_actuales)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "message": "Capacidad consultada correctamente",
            "data": {
                "idEntrenador":       idEntrenador,
                "fecha":              fecha,
                "capacidadMaxima":    MAX_CLIENTES_POR_DIA,
                "reservasActuales":   reservas_actuales,
                "lugaresDisponibles": lugares_disponibles,
            }
        }
    )


# ── CASO 2 y 8: Obtener reserva por ID ───────────────────────
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