# ─────────────────────────────────────────────────────────────
# CAPA API — rutas HTTP con FastAPI
# Solo recibe peticiones y llama al servicio.
# Aquí NO hay lógica de negocio.
# ─────────────────────────────────────────────────────────────

from fastapi import APIRouter, HTTPException, status
from domain.iniciosesion.iniciosesion_domain import InicioSesionCreate, InicioSesionResponse
from services.iniciosesion.iniciosesion_services import SesionService
from respository.iniciosesion.iniciosesion_repositories import sesion_repository
from respository.Cliente.cliente_repositories import cliente_repository
from respository.Entrenador.Entrenador_repository import entrenador_repository

# Crear el router con prefijo y etiqueta para la documentación
router = APIRouter(
    prefix="/api/auth",
    tags=["Inicio de Sesión"],
)

# Instanciar el servicio con inyección de los tres repositorios
service = SesionService(
    sesion_repo     = sesion_repository,
    cliente_repo    = cliente_repository,
    entrenador_repo = entrenador_repository,
)


# ── Funciones utilitarias (en producción irían en un módulo aparte) ──
def _verificar_contrasena(hash_guardado: str, plain: str) -> bool:
    """Simula verificación de contraseña. En producción: bcrypt.checkpw()"""
    return hash_guardado == f"hashed_{plain}"

def _generar_token(id_usuario: int, rol: str) -> str:
    """Simula generación de JWT. En producción: jwt.encode()"""
    return f"jwt_{id_usuario}_{rol}_token"


# ── POST /api/auth/login ──────────────────────────────────────
@router.post("/login", response_model=InicioSesionResponse)
def iniciar_sesion(datos: InicioSesionCreate):
    """Autentica al usuario y retorna un token JWT con su rol."""
    try:
        return service.iniciar_sesion(
            datos               = datos,
            verificar_contrasena = _verificar_contrasena,
            generar_token       = _generar_token,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


# ── POST /api/auth/logout ─────────────────────────────────────
@router.post("/logout")
def cerrar_sesion(token: str):
    """Invalida el token JWT activo del usuario."""
    try:
        return service.cerrar_sesion(token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


# ── GET /api/auth/sesion ──────────────────────────────────────
@router.get("/sesion", response_model=InicioSesionResponse)
def obtener_sesion_activa(token: str):
    """Retorna los datos de la sesión asociada al token."""
    try:
        return service.obtener_sesion(token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )