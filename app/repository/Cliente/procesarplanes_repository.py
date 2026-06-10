from app.domain.Cliente.procesarplanes_domain import Plan, Suscripcion
from typing import Optional


class ProcesarPlanesRepository:

    def __init__(self):
        self._planes: list[Plan] = []
        self._suscripciones: list[Suscripcion] = []
        self._siguiente_plan_id: int = 1
        self._siguiente_suscripcion_id: int = 1
        self._seed()

    def _seed(self):
        self._planes = [
            Plan(1, "Plan Básico",          55000,  30,  True),
            Plan(2, "Plan Mensual Premium", 85000,  30,  True),
            Plan(3, "Plan Trimestral",      220000, 90,  True),
            Plan(4, "Plan Anual",           750000, 365, True),
        ]
        self._siguiente_plan_id = 5
        self._siguiente_suscripcion_id = 1

    # ── CRUD Planes ───────────────────────────────────────────

    def obtener_planes_activos(self) -> list[Plan]:
        return [p for p in self._planes if p.activo]

    def obtener_plan_por_id(self, id_plan: int) -> Optional[Plan]:
        return next((p for p in self._planes if p.id == id_plan), None)

    def crear_plan(self, nombre: str, monto: float, duracion_dias: int) -> Plan:
        nuevo = Plan(
            id           = self._siguiente_plan_id,
            nombre       = nombre,
            monto        = monto,
            duracion_dias= duracion_dias,
            activo       = True,
        )
        self._planes.append(nuevo)
        self._siguiente_plan_id += 1
        return nuevo

    def actualizar_plan(self, id_plan: int, datos: dict) -> Optional[Plan]:
        plan = self.obtener_plan_por_id(id_plan)
        if not plan:
            return None
        if "nombre"       in datos and datos["nombre"]       is not None:
            plan.nombre        = datos["nombre"]
        if "monto"        in datos and datos["monto"]        is not None:
            plan.monto         = datos["monto"]
        if "duracionDias" in datos and datos["duracionDias"] is not None:
            plan.duracion_dias = datos["duracionDias"]
        if "activo"       in datos and datos["activo"]       is not None:
            plan.activo        = datos["activo"]
        return plan

    def dar_de_baja_plan(self, id_plan: int) -> Optional[Plan]:
        plan = self.obtener_plan_por_id(id_plan)
        if not plan:
            return None
        plan.dar_de_baja()
        return plan

    # ── Suscripciones ─────────────────────────────────────────

    def obtener_suscripcion_activa(self, id_cliente: int) -> Optional[Suscripcion]:
        return next((s for s in self._suscripciones
                     if s.id_cliente == id_cliente), None)

    def crear_suscripcion(self, id_cliente: int, plan: Plan) -> Suscripcion:
        # REGLA: solo un plan activo por cliente — se reemplaza el anterior
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