# ─────────────────────────────────────────────────────────────
# CAPA API — rutas HTTP con FastAPI
# Solo recibe peticiones y llama al servicio.
# Aquí NO hay lógica de negocio.
# ─────────────────────────────────────────────────────────────

from fastapi import APIRouter, HTTPException, status
from app.domain.ControlPermisos.ControlPermisos_domain import ValidarAutorizacionCreate, ValidarAutorizacionResponse
from FitZone1.app.repository.ControlPermisos.ControlPermisos_repository import control_permisos_repository
from app.services.ControlPermisos.ControlPermisos_services import ControlPermisosService

router = APIRouter(
    prefix="/api/auth",
    tags=["Control de Permisos"],
)

service = ControlPermisosService(repo=control_permisos_repository)


# ── Función utilitaria ────────────────────────────────────────
def _decodificar_token(token: str) -> dict | None:
    """Simula decodificación de JWT. En producción: jwt.decode()"""
    try:
        partes = token.split("_")
        return {"id_usuario": int(partes[1]), "rol": partes[2]}
    except Exception:
        return None


# ── POST /api/auth/validar-autorizacion ──────────────────────
@router.post("/validar-autorizacion", response_model=ValidarAutorizacionResponse)
def validar_autorizacion(datos: ValidarAutorizacionCreate):
    """Valida si el token tiene permisos para ejecutar la acción sobre el recurso."""
    try:
        return service.validar_autorizacion(
            datos             = datos,
            decodificar_token = _decodificar_token,
        )
    except PermissionError as e:
        codigo = str(e)
        if codigo == "TOKEN_INVALIDO":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="El token no es válido o ha expirado"
            )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado"
        )


# ── POST /api/auth/roles ──────────────────────────────────────
@router.post("/roles")
def asignar_rol(id_usuario: int, rol: str):
    """Asigna un rol a un usuario del sistema."""
    try:
        return service.asignar_rol(id_usuario, rol)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# ── DELETE /api/auth/roles/{id_usuario} ──────────────────────
@router.delete("/roles/{id_usuario}")
def revocar_acceso(id_usuario: int):
    """Revoca todos los permisos de un usuario."""
    try:
        return service.revocar_acceso(id_usuario)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


# ── GET /api/auth/roles/{rol} ─────────────────────────────────
@router.get("/roles/{rol}", response_model=list[ValidarAutorizacionResponse])
def usuarios_por_rol(rol: str):
    """Lista todos los usuarios que tienen asignado un rol específico."""
    try:
        return service.listar_por_rol(rol)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )