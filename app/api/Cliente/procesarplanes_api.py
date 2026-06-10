from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
from app.domain.Cliente.procesarplanes_domain import (
    PlanCreate, PlanUpdate, SuscribirPlanCreate,
)
from app.repository.Cliente.procesarplanes_repository import procesar_planes_repository
from app.services.Cliente.procesarplanes_services import ProcesarPlanesService

router = APIRouter(
    prefix="/api/pagos/planes",
    tags=["Procesar Planes"],
)

service = ProcesarPlanesService(repo=procesar_planes_repository)


# ── Helpers ───────────────────────────────────────────────────
def _ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")

def _error(status_code: int, message: str, error_code: str, details: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "success":    False,
            "statusCode": status_code,
            "message":    message,
            "error": {
                "error_code": error_code,
                "details":    details,
                "timestamp":  _ts(),
            },
        }
    )


# ── GET /api/pagos/planes ─────────────────────────────────────
@router.get("/")
def listar_planes():
    """Retorna todos los planes de suscripción activos."""
    try:
        planes = service.listar_planes()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "message": "Planes obtenidos correctamente",
                "data":    [p.model_dump() for p in planes],
            }
        )
    except ValueError:
        return _error(404, "Sin planes disponibles", "PAY_NO_PLANS_FOUND",
                      "No hay planes de suscripción activos en el sistema")


# ── POST /api/pagos/planes ────────────────────────────────────
@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_plan(datos: PlanCreate):
    """Crea un nuevo plan de suscripción."""
    plan = service.crear_plan(datos)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "success": True,
            "message": "Plan creado correctamente",
            "data":    plan.model_dump(),
        }
    )


# ── PUT /api/pagos/planes/{id_plan} ───────────────────────────
@router.put("/{id_plan}")
def actualizar_plan(id_plan: int, datos: PlanUpdate):
    """Actualiza los datos de un plan existente."""
    try:
        plan = service.actualizar_plan(id_plan, datos)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "message": "Plan actualizado correctamente",
                "data":    plan.model_dump(),
            }
        )
    except ValueError:
        return _error(404, "Plan no encontrado", "PAY_PLAN_NOT_FOUND",
                      "No existe un plan con el ID proporcionado")


# ── DELETE /api/pagos/planes/{id_plan} ────────────────────────
@router.delete("/{id_plan}")
def dar_de_baja_plan(id_plan: int):
    """Da de baja lógica un plan (no lo elimina físicamente)."""
    try:
        resultado = service.dar_de_baja_plan(id_plan)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "message": "Plan eliminado correctamente",
                "data":    resultado.model_dump(),
            }
        )
    except ValueError as e:
        error_code = str(e)
        if error_code == "PAY_PLAN_HAS_ACTIVE_SUBSCRIPTIONS":
            return _error(
                409,
                "Plan con suscripciones activas",
                "PAY_PLAN_HAS_ACTIVE_SUBSCRIPTIONS",
                "No se puede eliminar un plan que tiene suscripciones activas asociadas",
            )
        return _error(404, "Plan no encontrado", "PAY_PLAN_NOT_FOUND",
                      "No existe un plan con el ID proporcionado")


# ── POST /api/pagos/planes/suscribir ─────────────────────────
@router.post("/suscribir")
def suscribir_plan(datos: SuscribirPlanCreate):
    """Suscribe al cliente a un plan de membresía."""
    try:
        suscripcion = service.suscribir(datos)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "success": True,
                "message": "Suscripción activada correctamente",
                "data":    suscripcion.model_dump(),
            }
        )
    except ValueError:
        return _error(404, "Plan no disponible", "PAY_PLAN_NOT_FOUND",
                      "El plan seleccionado no existe o fue dado de baja")


# ── GET /api/pagos/planes/cliente/{id_cliente} ────────────────
@router.get("/cliente/{id_cliente}")
def obtener_suscripcion(id_cliente: int):
    """Retorna la suscripción activa de un cliente."""
    try:
        suscripcion = service.obtener_suscripcion(id_cliente)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "message": "Suscripción obtenida correctamente",
                "data":    suscripcion.model_dump(),
            }
        )
    except ValueError as e:
        return _error(404, "Sin suscripción activa", "PAY_SUBSCRIPTION_NOT_FOUND",
                      str(e))