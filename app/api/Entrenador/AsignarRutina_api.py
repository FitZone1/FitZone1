# ─────────────────────────────────────────────────────────────
# CAPA API — router de FastAPI
# ─────────────────────────────────────────────────────────────

from datetime import datetime
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import Annotated
from fastapi import Header

from app.domain.Entrenador.AsignarRutina_domain import (
    AsignarRutinaCreate,
    AsignarRutinaResponse,
    ErrorResponse,
    ErrorDetail,
)
from app.repository.Entrenador.AsignarRutina_repository import asignar_rutina_repository
from app.repository.Entrenador.CargarRutina_repository  import rutina_repository
from app.repository.iniciosesion.iniciosesion_repositories import sesion_repository
from app.services.Entrenador.AsignarRutina_services import AsignarRutinaService

router          = APIRouter(prefix="/rutinas", tags=["Rutinas"])
asignar_service = AsignarRutinaService(asignar_rutina_repository, rutina_repository)


# ── Helpers ───────────────────────────────────────────────────

def _timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def _error_response(status_code: int, message: str,
                    error_code: str, details: str) -> JSONResponse:
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
    "RUT_NOT_FOUND": (
        404,
        "Rutina no encontrada",
        "No existe una rutina con el ID proporcionado",
    ),
    "RUT_UNAUTHORIZED_EDIT": (
        403,
        "Sin permisos",
        "Solo el entrenador que creó la rutina puede modificar sus ejercicios",
    ),
    "AUTH_UNAUTHORIZED": (
        403,
        "Acceso denegado",
        "Solo los entrenadores pueden asignar rutinas",
    ),
    "AUTH_MISSING_TOKEN": (
        401,
        "Token de autenticación requerido",
        "Debe enviar el header 'token' con una sesión válida",
    ),
}


# ── Dependencia: valida token y rol ──────────────────────────

def _validar_entrenador(token: str, rol: str):
    """
    Valida que:
      - El header token esté presente y corresponda a una sesión activa  → 401
      - El rol sea ENTRENADOR                                             → 403
    Retorna el id_entrenador (int) si todo es válido, o un JSONResponse de error.
    """
    # Caso 6: sin token (header vacío o ausente llega como cadena vacía en FastAPI)
    if not token or token.strip() == "":
        return _error_response(401, "Token de autenticación requerido",
                               "AUTH_MISSING_TOKEN",
                               "Debe enviar el header 'token' con una sesión válida")

    sesion = sesion_repository.obtener_por_token(token)
    if not sesion:
        return _error_response(401, "Token de autenticación requerido",
                               "AUTH_MISSING_TOKEN",
                               "Token inválido o sesión expirada")

    # Caso 5: usuario autenticado pero con rol distinto a ENTRENADOR
    if rol.upper() != "ENTRENADOR":
        return _error_response(403, "Acceso denegado",
                               "AUTH_UNAUTHORIZED",
                               "Solo los entrenadores pueden asignar rutinas")

    return sesion.id_usuario


# ── Endpoints ─────────────────────────────────────────────────

@router.post(
    "/asignar",
    response_model=AsignarRutinaResponse,
    status_code=201,
    responses={
        200: {"model": AsignarRutinaResponse, "description": "Rutina reasignada a un día ya existente"},
        401: {"model": ErrorResponse, "description": "Token ausente o inválido"},
        403: {"model": ErrorResponse, "description": "Acceso denegado o rutina de otro entrenador"},
        404: {"model": ErrorResponse, "description": "Rutina no encontrada"},
        422: {"description": "Datos de entrada inválidos (diaSemana, idRutina, idEntrenador)"},
    },
)
def asignar_rutina(
    datos:         AsignarRutinaCreate,
    token:         Annotated[str, Header(description="Token obtenido al iniciar sesión")],
    x_rol_usuario: Annotated[str, Header(description="Rol del usuario. Debe ser: ENTRENADOR")],
):
    """
    Asigna una rutina a un día de la semana para el entrenador autenticado.

    - Solo se pueden asignar rutinas creadas por el propio entrenador.
    - Si el día ya tenía una rutina asignada, se reemplaza (reasignación).
    - La rutina queda visible para todos los clientes con sesión ese día.

    **Headers requeridos:**
    - `token`: token obtenido al iniciar sesión
    - `x-rol-usuario`: debe ser `ENTRENADOR`

    **Códigos de respuesta:**
    - `201` — rutina asignada por primera vez al día indicado
    - `200` — rutina reasignada (el día ya tenía una rutina previa)
    - `401` — token ausente o inválido
    - `403` — rol incorrecto o rutina pertenece a otro entrenador
    - `404` — rutina no encontrada
    - `422` — datos de entrada inválidos
    """
    # Validar token y rol
    resultado = _validar_entrenador(token, x_rol_usuario)
    if isinstance(resultado, JSONResponse):
        return resultado

    id_entrenador = resultado

    # Detectar si el día ya tenía asignación (para devolver 200 en reasignación)
    habia_asignacion_previa = asignar_rutina_repository.obtener_asignacion(
        id_entrenador, datos.diaSemana
    ) is not None

    try:
        respuesta = asignar_service.asignar_rutina(id_entrenador, datos)

        # Caso 2: reasignación → HTTP 200; Caso 1: nueva asignación → HTTP 201
        status_code = 200 if habia_asignacion_previa else 201
        return JSONResponse(status_code=status_code, content=respuesta.model_dump())

    except ValueError as e:
        codigo = str(e)
        status, message, details = _ERROR_MAP.get(
            codigo, (404, "Error de validación", codigo)
        )
        return _error_response(status, message, codigo, details)

    except PermissionError as e:
        codigo = str(e)
        status, message, details = _ERROR_MAP.get(
            codigo, (403, "Acceso denegado", codigo)
        )
        return _error_response(status, message, codigo, details)