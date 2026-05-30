from app.domain.Cliente.procesarplanes_domain import SuscribirPlanCreate, PlanResponse, SuscripcionResponse
from app.repository.Cliente.procesarplanes_repository import ProcesarPlanesRepository


class ProcesarPlanesService:

    def __init__(self, repo: ProcesarPlanesRepository):
        self.repo = repo

    def listar_planes(self) -> list[PlanResponse]:
        planes = self.repo.obtener_planes_activos()
        if not planes:
            raise ValueError("PAY_NO_PLANS_FOUND")
        return [PlanResponse(**p.to_response()) for p in planes]

    def suscribir(self, datos: SuscribirPlanCreate) -> SuscripcionResponse:
        # Regla de negocio: el plan debe existir y estar activo
        plan = self.repo.obtener_plan_por_id(datos.idPlan)
        if not plan:
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
