from fastapi import APIRouter, Path, status
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
from app.domain.Cliente.AdministrarPerfilCliente_domain import PerfilClienteUpdate, ObjetivosCreate
from app.repository.Cliente.cliente_repositories import cliente_repository
from app.services.Cliente.AdministrarPerfilCliente_services import AdministrarPerfilClienteService

router = APIRouter(
    prefix="/api/perfiles",
    tags=["Administrar Perfil Cliente"],
)

service = AdministrarPerfilClienteService(repo=cliente_repository)


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


# ── GET /api/perfiles/{idUsuario} ─────────────────────────────
@router.get(
    "/{idUsuario}",
    summary="Ver perfil del cliente",
    description="Retorna los datos del perfil del cliente.",
    responses={
        200: {"description": "Perfil obtenido correctamente"},
        404: {"description": "Cliente no encontrado"},
    },
)
def ver_perfil(
    idUsuario: int = Path(..., gt=0, description="ID del cliente"),
):
    try:
        perfil = service.ver_perfil(idUsuario)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "message": "Perfil obtenido correctamente",
                "data": perfil.model_dump(),
            }
        )
    except ValueError:
        return _error(404, "Cliente no encontrado", "PROF_CLIENT_NOT_FOUND",
                      "No existe un cliente con el ID proporcionado")


# ── PUT /api/perfiles/cliente/{idUsuario} ─────────────────────
@router.put(
    "/cliente/{idUsuario}",
    summary="Actualizar perfil del cliente",
    description="Actualiza nombre, teléfono, objetivos y peso actual del cliente.",
    responses={
        200: {"description": "Perfil actualizado correctamente"},
        404: {"description": "Cliente no encontrado"},
    },
)
def actualizar_perfil(
    idUsuario: int = Path(..., gt=0, description="ID del cliente"),
    datos: PerfilClienteUpdate = ...,
):
    try:
        perfil = service.actualizar_perfil(idUsuario, datos)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "message": "Perfil actualizado correctamente",
                "data": perfil.model_dump(),
            }
        )
    except ValueError:
        return _error(404, "Cliente no encontrado", "PROF_CLIENT_NOT_FOUND",
                      "No existe un cliente con el ID proporcionado")


# ── POST /api/perfiles/{idUsuario}/objetivos ──────────────────
@router.post(
    "/{idUsuario}/objetivos",
    summary="Registrar objetivos del cliente",
    description="Registra los objetivos de entrenamiento, peso meta y plazo en meses del cliente.",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Objetivos registrados correctamente"},
        404: {"description": "Cliente no encontrado"},
    },
)
def registrar_objetivos(
    idUsuario: int = Path(..., gt=0, description="ID del cliente"),
    datos: ObjetivosCreate = ...,
):
    try:
        objetivos = service.registrar_objetivos(idUsuario, datos)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "success": True,
                "message": "Objetivos registrados correctamente",
                "data": objetivos.model_dump(),
            }
        )
    except ValueError:
        return _error(404, "Cliente no encontrado", "PROF_CLIENT_NOT_FOUND",
                      "No existe un cliente con el ID proporcionado")