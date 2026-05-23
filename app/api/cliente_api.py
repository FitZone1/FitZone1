# ─────────────────────────────────────────────────────────────
# CAPA API — rutas HTTP con FastAPI
# Solo recibe peticiones y llama al servicio.
# Aquí NO hay lógica de negocio.
# ─────────────────────────────────────────────────────────────

from fastapi import APIRouter, HTTPException, status
from app.domain.cliente_domain import RegistroClienteCreate, RegistroClienteResponse
from app.respository.cliente_repositories import ClienteRepository, cliente_repository
from app.services.cliente_service import ClienteService
# Crear el router con prefijo y etiqueta para la documentación
router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Registro Cliente"],
)

# Instanciar el servicio con inyección del repositorio
service = ClienteService(repo=cliente_repository)


# ── POST /api/v1/auth/registro ────────────────────────────────
@router.post("/registro", response_model=RegistroClienteResponse,
             status_code=status.HTTP_201_CREATED)
def registrar_cliente(datos: RegistroClienteCreate):
    """Registra un nuevo cliente. El estado inicial es PENDIENTE hasta verificar correo."""
    try:
        # En producción la contraseña se hashea aquí antes de pasar al servicio
        contrasena_hash = f"hashed_{datos.contrasena}"
        return service.registrar(datos, contrasena_hash)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


# ── GET /api/v1/auth/clientes ─────────────────────────────────
@router.get("/clientes", response_model=list[RegistroClienteResponse])
def listar_clientes():
    """Retorna todos los clientes registrados."""
    return service.listar()


# ── GET /api/v1/auth/clientes/{id} ───────────────────────────
@router.get("/clientes/{id}", response_model=RegistroClienteResponse)
def obtener_cliente(id: int):
    """Retorna un cliente por su ID."""
    try:
        return service.obtener(id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


# ── PATCH /api/v1/auth/clientes/{id}/estado ───────────────────
@router.patch("/clientes/{id}/estado", response_model=RegistroClienteResponse)
def cambiar_estado(id: int, estado: str):
    """Cambia el estado del cliente: ACTIVO, INACTIVO o PENDIENTE."""
    try:
        return service.cambiar_estado(id, estado)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# ── DELETE /api/v1/auth/clientes/{id} ────────────────────────
@router.delete("/clientes/{id}")
def eliminar_cliente(id: int):
    """Elimina un cliente por su ID."""
    try:
        return service.eliminar(id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


# ── GET /api/v1/auth/clientes/estado/{estado} ────────────────
@router.get("/clientes/estado/{estado}",
            response_model=list[RegistroClienteResponse])
def clientes_por_estado(estado: str):
    """Filtra clientes por estado (PENDIENTE, ACTIVO, INACTIVO)."""
    try:
        return service.por_estado(estado)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )