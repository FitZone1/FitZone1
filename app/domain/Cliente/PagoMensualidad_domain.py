from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional
from datetime import datetime


# ── Métodos de pago disponibles ───────────────────────────────
METODOS_CON_TARJETA = {"TARJETA", "PSE"}
METODOS_VALIDOS     = {"TARJETA", "PSE", "EFECTIVO"}


# ── Schema de SALIDA — método de pago ─────────────────────────
class MetodoPagoResponse(BaseModel):
    codigo:          str
    nombre:          str
    requiereTarjeta: bool


# ── Schema de ENTRADA ─────────────────────────────────────────
class PagoMensualidadCreate(BaseModel):
    idCliente:     int           = Field(..., gt=0, description="ID del cliente que realiza el pago")
    idPlan:        int           = Field(..., gt=0, description="ID del plan a pagar")
    metodoPago:    str           = Field(..., description="Método de pago: TARJETA, PSE o EFECTIVO")
    numeroTarjeta: Optional[str] = Field(None, description="Número de tarjeta de 16 dígitos (requerido para TARJETA y PSE)")

    @field_validator("metodoPago")
    @classmethod
    def metodo_valido(cls, v):
        if v.upper() not in METODOS_VALIDOS:
            raise ValueError(f"Método de pago no válido. Use uno de: {METODOS_VALIDOS}")
        return v.upper()

    @model_validator(mode="after")
    def validar_tarjeta_segun_metodo(self):
        """
        REGLA DE NEGOCIO:
        - Si el método es TARJETA o PSE: numeroTarjeta es obligatorio y debe
          tener exactamente 16 dígitos numéricos.
        - Si el método es EFECTIVO: numeroTarjeta se ignora sin importar
          qué valor venga (incluyendo el placeholder 'string' de Swagger).
        """
        if self.metodoPago in METODOS_CON_TARJETA:
            # Requiere tarjeta
            if not self.numeroTarjeta:
                raise ValueError("El método de pago seleccionado requiere número de tarjeta")
            if not self.numeroTarjeta.isdigit():
                raise ValueError("El número de tarjeta solo puede contener dígitos")
            if len(self.numeroTarjeta) != 16:
                raise ValueError("El número de tarjeta debe tener exactamente 16 dígitos")
        else:
            # EFECTIVO: limpiar cualquier valor que venga, no se necesita
            self.numeroTarjeta = None

        return self


# ── Schema de SALIDA ──────────────────────────────────────────
class PagoMensualidadResponse(BaseModel):
    idPago:  str
    monto:   float
    estado:  str
    fecha:   str

    class Config:
        from_attributes = True


# ── Modelo interno del dominio ────────────────────────────────
class MetodoPago:
    CATALOGO = [
        {"codigo": "TARJETA",  "nombre": "Tarjeta de crédito/débito", "requiereTarjeta": True},
        {"codigo": "PSE",      "nombre": "PSE - Débito bancario",      "requiereTarjeta": True},
        {"codigo": "EFECTIVO", "nombre": "Pago en efectivo",           "requiereTarjeta": False},
    ]

    @classmethod
    def listar(cls) -> list[dict]:
        return cls.CATALOGO

    @classmethod
    def requiere_tarjeta(cls, codigo: str) -> bool:
        return codigo.upper() in METODOS_CON_TARJETA


class Pago:
    ESTADOS_VALIDOS = {"APROBADO", "RECHAZADO", "PENDIENTE"}

    def __init__(self, id_pago: str, id_cliente: int, id_plan: int,
                 monto: float, estado: str, fecha: str,
                 metodo_pago: str, numero_tarjeta: Optional[str] = None):
        self.id_pago        = id_pago
        self.id_cliente     = id_cliente
        self.id_plan        = id_plan
        self.monto          = monto
        self.estado         = estado
        self.fecha          = fecha
        self.metodo_pago    = metodo_pago
        self.numero_tarjeta = numero_tarjeta

    # REGLA DE NEGOCIO: solo pagos APROBADOS renuevan la suscripción
    def esta_aprobado(self) -> bool:
        return self.estado == "APROBADO"

    # REGLA DE NEGOCIO: el monto debe ser mayor a 0
    def monto_valido(self) -> bool:
        return self.monto > 0

    def to_response(self) -> dict:
        return {
            "idPago":  self.id_pago,
            "monto":   self.monto,
            "estado":  self.estado,
            "fecha":   self.fecha,
        }