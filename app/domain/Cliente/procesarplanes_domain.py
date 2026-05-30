from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timedelta


# ── Schema de ENTRADA — suscripción ──────────────────────────
class SuscribirPlanCreate(BaseModel):
    idCliente: int = Field(..., gt=0, description="ID del cliente")
    idPlan:    int = Field(..., gt=0, description="ID del plan a suscribir")


# ── Schema de SALIDA — plan ───────────────────────────────────
class PlanResponse(BaseModel):
    idPlan:       int
    nombre:       str
    monto:        float
    duracionDias: int

    class Config:
        from_attributes = True


# ── Schema de SALIDA — suscripción ───────────────────────────
class SuscripcionResponse(BaseModel):
    idSuscripcion: int
    idCliente:     int
    plan:          str
    monto:         float
    vigencia:      str

    class Config:
        from_attributes = True


# ── Modelos internos del dominio ──────────────────────────────
class Plan:
    def __init__(self, id: int, nombre: str, monto: float,
                 duracion_dias: int, activo: bool = True):
        self.id            = id
        self.nombre        = nombre
        self.monto         = monto
        self.duracion_dias = duracion_dias
        self.activo        = activo

    # REGLA DE NEGOCIO: solo planes activos pueden suscribirse
    def esta_activo(self) -> bool:
        return self.activo

    def calcular_vigencia(self) -> str:
        return (datetime.now() + timedelta(days=self.duracion_dias)).strftime("%Y-%m-%d")

    def to_response(self) -> dict:
        return {
            "idPlan":       self.id,
            "nombre":       self.nombre,
            "monto":        self.monto,
            "duracionDias": self.duracion_dias,
        }


class Suscripcion:
    def __init__(self, id: int, id_cliente: int, id_plan: int,
                 nombre_plan: str, monto: float, vigencia: str):
        self.id          = id
        self.id_cliente  = id_cliente
        self.id_plan     = id_plan
        self.nombre_plan = nombre_plan
        self.monto       = monto
        self.vigencia    = vigencia

    def to_response(self) -> dict:
        return {
            "idSuscripcion": self.id,
            "idCliente":     self.id_cliente,
            "plan":          self.nombre_plan,
            "monto":         self.monto,
            "vigencia":      self.vigencia,
        }
