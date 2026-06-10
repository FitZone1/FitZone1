# ─────────────────────────────────────────────────────────────
# CAPA API — router de FastAPI
# ─────────────────────────────────────────────────────────────

from datetime import datetime
from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import JSONResponse
from typing import Annotated

from app.domain.Entrenador.CargarRutina_domain         import RutinaCreate, RutinaResponse, ErrorResponse, ErrorDetail
from app.repository.Entrenador.CargarRutina_repository import rutina_repository
from app.repository.iniciosesion.iniciosesion_repositories import sesion_repository
from app.services.Entrenador.CargarRutina_services       import RutinaService

router         = APIRouter(prefix="/rutinas", tags=["Rutinas"])
rutina_service = RutinaService(rutina_repository)


# ── Helpers ───────────────────────────────────────────────────

def _timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def _error_response(status_code: int, message: str, error_code: str, details: str) -> JSONResponse:
    body = ErrorResponse(
        statusCode = status_code,
        message    = message,
        error      = ErrorDetail(
            error_code = error_code,
            details    = details,
            timestamp  = _timestamp(),
        ),
    )
    return JSONResponse(status_code=status_code, content=body.model_dump())


_ERROR_MAP = {
    "RUT_EMPTY_EXERCISES": (400, "Rutina sin ejercicios",      "La rutina debe tener al menos un ejercicio registrado"),
    "RUT_DUPLICATE_NAME":  (400, "Nombre de rutina duplicado", "Ya tienes una rutina con ese nombre"),
    "RUT_NOT_FOUND":       (404, "Rutina no encontrada",       "No existe una rutina con ese ID"),
    "AUTH_UNAUTHORIZED":   (403, "Acceso denegado",            "No tienes permiso para acceder a este recurso"),
}


# ── Dependencia: valida token y rol ──────────────────────────

def _validar_entrenador(token: str, rol: str) -> int:
    if rol != "ENTRENADOR":
        return _error_response(
            403, "Acceso denegado", "AUTH_UNAUTHORIZED",
            "Solo los entrenadores pueden cargar rutinas"
        )

    sesion = sesion_repository.obtener_por_token(token)
    if not sesion:
        raise HTTPException(status_code=401, detail="Token inválido o sesión expirada")

    return sesion.id_usuario


# ── Endpoints ─────────────────────────────────────────────────

@router.post(
    "",
    response_model=RutinaResponse,
    status_code=201,
    responses={
        400: {"model": ErrorResponse, "description": "Rutina sin ejercicios o nombre duplicado"},
        401: {"description": "Token inválido o sesión expirada"},
        403: {"model": ErrorResponse, "description": "Acceso denegado — solo ENTRENADOR"},
    },
)
def cargar_rutina(
    datos:         RutinaCreate,
    token:         Annotated[str, Header(description="Token obtenido al iniciar sesión")],
    x_rol_usuario: Annotated[str, Header(description="Rol del usuario. Debe ser: ENTRENADOR")],
):
    """
    Crea una nueva rutina para el entrenador autenticado.
    El `idEntrenador` se obtiene automáticamente del token — **no va en el body**.

    **Headers requeridos:**
    - `token`: token obtenido al iniciar sesión
    - `x-rol-usuario`: debe ser `ENTRENADOR`
    """
    resultado = _validar_entrenador(token, x_rol_usuario)

    # Si _validar_entrenador devuelve un JSONResponse es porque falló el rol
    if isinstance(resultado, JSONResponse):
        return resultado

    id_entrenador = resultado

    try:
        return rutina_service.cargar_rutina(id_entrenador, datos)
    except ValueError as e:
        codigo = str(e)
        status, message, details = _ERROR_MAP.get(codigo, (400, "Error de validación", codigo))
        return _error_response(status, message, codigo, details)


@router.get(
    "",
    status_code=200,
    responses={
        401: {"description": "Token inválido o sesión expirada"},
        403: {"model": ErrorResponse, "description": "Acceso denegado — solo ENTRENADOR"},
    },
)
def listar_rutinas(
    token:         Annotated[str, Header(description="Token obtenido al iniciar sesión")],
    x_rol_usuario: Annotated[str, Header(description="Rol del usuario. Debe ser: ENTRENADOR")],
):
    """Lista todas las rutinas del entrenador autenticado."""
    resultado = _validar_entrenador(token, x_rol_usuario)
    if isinstance(resultado, JSONResponse):
        return resultado

    rutinas = rutina_service.listar_rutinas(resultado)
    return {"success": True, "data": rutinas}


@router.get(
    "/{id_rutina}",
    status_code=200,
    responses={
        403: {"model": ErrorResponse, "description": "Acceso denegado"},
        404: {"model": ErrorResponse, "description": "Rutina no encontrada"},
    },
)
def obtener_rutina(
    id_rutina:     int,
    token:         Annotated[str, Header(description="Token obtenido al iniciar sesión")],
    x_rol_usuario: Annotated[str, Header(description="Rol del usuario. Debe ser: ENTRENADOR")],
):
    """Retorna una rutina específica, solo si pertenece al entrenador autenticado."""
    resultado = _validar_entrenador(token, x_rol_usuario)
    if isinstance(resultado, JSONResponse):
        return resultado

    try:
        rutina = rutina_service.obtener_rutina(id_rutina, resultado)
        return {"success": True, "data": rutina}
    except ValueError as e:
        codigo = str(e)
        status, message, details = _ERROR_MAP.get(codigo, (404, "No encontrado", codigo))
        return _error_response(status, message, codigo, details)
    except PermissionError as e:
        codigo = str(e)
        status, message, details = _ERROR_MAP.get(codigo, (403, "Acceso denegado", codigo))
        return _error_response(status, message, codigo, details)