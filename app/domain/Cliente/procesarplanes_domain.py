from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timedelta


# ── Schema de ENTRADA — crear plan ───────────────────────────
class PlanCreate(BaseModel):
    nombre:       str   = Field(..., min_length=1, description="Nombre del plan")
    monto:        float = Field(..., gt=0, description="Precio del plan en pesos")
    duracionDias: int   = Field(..., gt=0, description="Duración del plan en días")


# ── Schema de ENTRADA — actualizar plan ──────────────────────
class PlanUpdate(BaseModel):
    nombre:       Optional[str]   = Field(None, min_length=1, description="Nuevo nombre del plan")
    monto:        Optional[float] = Field(None, gt=0, description="Nuevo precio del plan")
    duracionDias: Optional[int]   = Field(None, gt=0, description="Nueva duración en días")
    activo:       Optional[bool]  = Field(None, description="Estado activo/inactivo del plan")


# ── Schema de ENTRADA — suscribir cliente a plan ─────────────
class SuscribirPlanCreate(BaseModel):
    idCliente: int = Field(..., gt=0, description="ID del cliente")
    idPlan:    int = Field(..., gt=0, description="ID del plan a suscribir")


# ── Schema de SALIDA — plan ───────────────────────────────────
class PlanResponse(BaseModel):
    idPlan:       int
    nombre:       str
    monto:        float
    duracionDias: int
    activo:       bool  # incluido según contrato del API

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


# ── Schema de SALIDA — baja de plan ──────────────────────────
class PlanDeleteResponse(BaseModel):
    idPlan: int
    activo: bool   # siempre False tras la baja

    class Config:
        from_attributes = True


# ── Modelo interno — Plan ─────────────────────────────────────
class Plan:
    def __init__(self, id: int, nombre: str, monto: float,
                 duracion_dias: int, activo: bool = True):
        self.id            = id
        self.nombre        = nombre
        self.monto         = monto
        self.duracion_dias = duracion_dias
        self.activo        = activo

    # REGLA DE NEGOCIO: solo planes activos son visibles al cliente
    def esta_activo(self) -> bool:
        return self.activo

    # REGLA DE NEGOCIO: la vigencia se calcula desde la fecha actual
    def calcular_vigencia(self) -> str:
        return (datetime.now() + timedelta(days=self.duracion_dias)).strftime("%Y-%m-%d")

    # REGLA DE NEGOCIO: dar de baja es lógico (no se elimina el registro)
    def dar_de_baja(self) -> None:
        self.activo = False

    def to_response(self) -> dict:
        return {
            "idPlan":       self.id,
            "nombre":       self.nombre,
            "monto":        self.monto,
            "duracionDias": self.duracion_dias,
            "activo":       self.activo,  # campo requerido por el contrato
        }

    def to_delete_response(self) -> dict:
        return {
            "idPlan": self.id,
            "activo": self.activo,
        }


# ── Modelo interno — Suscripcion ──────────────────────────────
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