# ─────────────────────────────────────────────────────────────
# CAPA API — rutas HTTP con FastAPI
# Solo recibe peticiones y llama al servicio.
# Aquí NO hay lógica de negocio.
# ─────────────────────────────────────────────────────────────

from fastapi import APIRouter, HTTPException, status
from domain.Entrenador.Entrenador_domain import RegistroEntrenadorCreate, RegistroEntrenadorResponse
from services.Entrenador.Entrenador_services import EntrenadorService
from respository.Entrenador.Entrenador_repository import entrenador_repository

# Crear el router con prefijo y etiqueta para la documentación
router = APIRouter(
    prefix="/api/v1/entrenadores",
    tags=["Registro Entrenador"],
)

# Instanciar el servicio con inyección del repositorio
service = EntrenadorService(repo=entrenador_repository)


# ── POST /api/v1/entrenadores ─────────────────────────────────
@router.post("/", response_model=RegistroEntrenadorResponse,
             status_code=status.HTTP_201_CREATED)
def registrar_entrenador(datos: RegistroEntrenadorCreate):
    """Registra un nuevo entrenador con sus datos personales y especialidad."""
    try:
        # En producción la contraseña se hashea aquí antes de pasar al servicio
        contrasena_hash = f"hashed_{datos.contrasena}"
        return service.registrar(datos, contrasena_hash)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


# ── GET /api/v1/entrenadores ──────────────────────────────────
@router.get("/", response_model=list[RegistroEntrenadorResponse])
def listar_entrenadores():
    """Retorna todos los entrenadores registrados."""
    return service.listar()


# ── GET /api/v1/entrenadores/activos ─────────────────────────
@router.get("/activos", response_model=list[RegistroEntrenadorResponse])
def listar_entrenadores_activos():
    """Retorna solo los entrenadores con estado ACTIVO (visibles para clientes)."""
    try:
        return service.listar_activos()
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


# ── GET /api/v1/entrenadores/{id} ────────────────────────────
@router.get("/{id}", response_model=RegistroEntrenadorResponse)
def obtener_entrenador(id: int):
    """Retorna un entrenador por su ID."""
    try:
        return service.obtener(id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


# ── PUT /api/v1/entrenadores/{id} ────────────────────────────
@router.put("/{id}", response_model=RegistroEntrenadorResponse)
def actualizar_entrenador(id: int, datos: RegistroEntrenadorCreate):
    """Actualiza los datos de un entrenador existente."""
    try:
        return service.actualizar(id, datos)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


# ── DELETE /api/v1/entrenadores/{id} ─────────────────────────
@router.delete("/{id}")
def eliminar_entrenador(id: int):
    """Elimina un entrenador por su ID."""
    try:
        return service.eliminar(id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


# ── GET /api/v1/entrenadores/gimnasio/{gimnasio_id} ──────────
@router.get("/gimnasio/{gimnasio_id}",
            response_model=list[RegistroEntrenadorResponse])
def entrenadores_por_gimnasio(gimnasio_id: int):
    """Filtra entrenadores por gimnasio."""
    try:
        return service.por_gimnasio(gimnasio_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )