from fastapi import APIRouter, Path, status
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


def _ok(entrenadores):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "message": "Entrenadores encontrados correctamente",
            "data": [e.model_dump() for e in entrenadores],
        }
    )


def _not_found():
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


# ── CASO 1: Todos los entrenadores disponibles ────────────────
@router.get(
    "/entrenadores",
    summary="Caso 1 – Listar todos los entrenadores disponibles",
    description=(
        "Retorna la lista completa de entrenadores cuyo campo `disponible` es `true`. "
        "No requiere parámetros adicionales."
    ),
    responses={
        200: {"description": "Lista de entrenadores disponibles"},
        404: {"description": "No hay entrenadores disponibles"},
    },
)
def listar_entrenadores_disponibles():
    try:
        entrenadores = service.listar_disponibles(especialidad=None, disponible=True)
        return _ok(entrenadores)
    except ValueError:
        return _not_found()


# ── CASO 2: Filtro por especialidad ───────────────────────────
@router.get(
    "/entrenadores/especialidad/{especialidad}",
    summary="Caso 2 – Filtrar entrenadores disponibles por especialidad",
    description=(
        "Retorna los entrenadores disponibles que coincidan con la especialidad indicada. "
        "Ejemplo: `/api/reservas/entrenadores/especialidad/Musculación`"
    ),
    responses={
        200: {"description": "Entrenadores filtrados por especialidad"},
        404: {"description": "Sin entrenadores para esa especialidad"},
    },
)
def listar_por_especialidad(
    especialidad: str = Path(..., description="Nombre de la especialidad (ej: Musculación, Yoga, Crossfit)")
):
    try:
        entrenadores = service.listar_disponibles(especialidad=especialidad, disponible=True)
        return _ok(entrenadores)
    except ValueError:
        return _not_found()


# ── CASO 3: Sin resultados (especialidad inexistente) ─────────
@router.get(
    "/entrenadores/sin-resultados",
    summary="Caso 3 – Verificar respuesta cuando no hay entrenadores disponibles",
    description=(
        "Endpoint de prueba que siempre simula el escenario donde ningún entrenador "
        "cumple los filtros aplicados. Retorna HTTP 404 con `error_code: RES_TRAINERS_NOT_FOUND`."
    ),
    responses={
        404: {"description": "Sin entrenadores disponibles con los filtros aplicados"},
    },
)
def sin_entrenadores_disponibles():
    return _not_found()