from app.domain.Cliente.procesarplanes_domain import Plan, Suscripcion
from typing import Optional


class ProcesarPlanesRepository:

    def __init__(self):
        self._planes: list[Plan] = []
        self._suscripciones: list[Suscripcion] = []
        self._siguiente_suscripcion_id: int = 1
        self._seed()

    def _seed(self):
        self._planes = [
            Plan(1, "Plan Básico",           55000, 30, True),
            Plan(2, "Plan Mensual Premium",  85000, 30, True),
            Plan(3, "Plan Trimestral",      220000, 90, True),
            Plan(4, "Plan Anual",           750000, 365, True),
        ]
        self._siguiente_suscripcion_id = 1

    # ── Planes ────────────────────────────────────────────────
    def obtener_planes_activos(self) -> list[Plan]:
        return [p for p in self._planes if p.activo]

    def obtener_plan_por_id(self, id_plan: int) -> Optional[Plan]:
        return next((p for p in self._planes if p.id == id_plan and p.activo), None)

    # ── Suscripciones ─────────────────────────────────────────
    def obtener_suscripcion_activa(self, id_cliente: int) -> Optional[Suscripcion]:
        return next((s for s in self._suscripciones
                     if s.id_cliente == id_cliente), None)

    def crear_suscripcion(self, id_cliente: int, plan: Plan) -> Suscripcion:
        # Eliminar suscripción anterior si existe
        self._suscripciones = [s for s in self._suscripciones
                                if s.id_cliente != id_cliente]
        nueva = Suscripcion(
            id          = self._siguiente_suscripcion_id,
            id_cliente  = id_cliente,
            id_plan     = plan.id,
            nombre_plan = plan.nombre,
            monto       = plan.monto,
            vigencia    = plan.calcular_vigencia(),
        )
        self._suscripciones.append(nueva)
        self._siguiente_suscripcion_id += 1
        return nueva


# Instancia única compartida (Singleton simple)
procesar_planes_repository = ProcesarPlanesRepository()
