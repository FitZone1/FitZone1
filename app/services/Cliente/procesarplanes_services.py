from app.domain.Cliente.procesarplanes_domain import (
    PlanCreate, PlanUpdate, SuscribirPlanCreate,
    PlanResponse, PlanDeleteResponse, SuscripcionResponse,
)
from app.repository.Cliente.procesarplanes_repository import ProcesarPlanesRepository


class ProcesarPlanesService:

    def __init__(self, repo: ProcesarPlanesRepository):
        self.repo = repo

    # ── CRUD Planes ───────────────────────────────────────────

    def listar_planes(self) -> list[PlanResponse]:
        planes = self.repo.obtener_planes_activos()
        if not planes:
            raise ValueError("PAY_NO_PLANS_FOUND")
        return [PlanResponse(**p.to_response()) for p in planes]

    def crear_plan(self, datos: PlanCreate) -> PlanResponse:
        plan = self.repo.crear_plan(
            nombre       = datos.nombre,
            monto        = datos.monto,
            duracion_dias= datos.duracionDias,
        )
        return PlanResponse(**plan.to_response())

    def actualizar_plan(self, id_plan: int, datos: PlanUpdate) -> PlanResponse:
        plan = self.repo.actualizar_plan(id_plan, datos.model_dump(exclude_none=False))
        if not plan:
            raise ValueError("PAY_PLAN_NOT_FOUND")
        return PlanResponse(**plan.to_response())

    def dar_de_baja_plan(self, id_plan: int) -> PlanDeleteResponse:
        plan = self.repo.dar_de_baja_plan(id_plan)
        if not plan:
            raise ValueError("PAY_PLAN_NOT_FOUND")
        return PlanDeleteResponse(**plan.to_delete_response())

    # ── Suscripciones ─────────────────────────────────────────

    def suscribir(self, datos: SuscribirPlanCreate) -> SuscripcionResponse:
        # REGLA: el plan debe existir y estar activo
        plan = self.repo.obtener_plan_por_id(datos.idPlan)
        if not plan or not plan.esta_activo():
            raise ValueError("PAY_PLAN_NOT_FOUND")

        suscripcion = self.repo.crear_suscripcion(
            id_cliente = datos.idCliente,
            plan       = plan,
        )
        return SuscripcionResponse(**suscripcion.to_response())

    def obtener_suscripcion(self, id_cliente: int) -> SuscripcionResponse:
        s = self.repo.obtener_suscripcion_activa(id_cliente)
        if not s:
            raise ValueError(f"No hay suscripción activa para el cliente {id_cliente}")
        return SuscripcionResponse(**s.to_response())