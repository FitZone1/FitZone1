from pydantic import BaseModel, Field, field_validator
from typing import List


DIAS_VALIDOS = {"LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES", "SABADO", "DOMINGO"}


# ── Schema de ENTRADA ─────────────────────────────────────────
class GestionHorariosCreate(BaseModel):
    idEntrenador:    int       = Field(..., gt=0, description="ID del entrenador")
    diasDisponibles: List[str] = Field(..., description="Días disponibles de la semana")
    horaInicio:      str       = Field(..., description="Hora de inicio (HH:MM)")
    horaFin:         str       = Field(..., description="Hora de fin (HH:MM)")

    @field_validator("diasDisponibles")
    @classmethod
    def dias_validos(cls, v):
        for dia in v:
            if dia.upper() not in DIAS_VALIDOS:
                raise ValueError(f"Día '{dia}' no válido. Use: {DIAS_VALIDOS}")
        return [d.upper() for d in v]

    @field_validator("horaFin")
    @classmethod
    def rango_horario_valido(cls, v, info):
        hora_inicio = info.data.get("horaInicio")
        if hora_inicio and v <= hora_inicio:
            raise ValueError("La hora de inicio no puede ser mayor a la hora de fin")
        return v


# ── Schema de SALIDA ──────────────────────────────────────────
class GestionHorariosResponse(BaseModel):
    idEntrenador:    int
    diasDisponibles: List[str]
    horaInicio:      str
    horaFin:         str

    class Config:
        from_attributes = True


# ── Modelo interno del dominio ────────────────────────────────
class HorarioDisponible:
    def __init__(self, id: int, id_entrenador: int, dias_disponibles: list,
                 hora_inicio: str, hora_fin: str):
        self.id               = id
        self.id_entrenador    = id_entrenador
        self.dias_disponibles = dias_disponibles
        self.hora_inicio      = hora_inicio
        self.hora_fin         = hora_fin

    # REGLA DE NEGOCIO: hora inicio debe ser menor que hora fin
    def rango_valido(self) -> bool:
        return self.hora_inicio < self.hora_fin

    # REGLA DE NEGOCIO: el día debe estar en la lista de disponibles
    def dia_disponible(self, dia: str) -> bool:
        return dia.upper() in self.dias_disponibles

    def to_response(self) -> dict:
        return {
            "idEntrenador":    self.id_entrenador,
            "diasDisponibles": self.dias_disponibles,
            "horaInicio":      self.hora_inicio,
            "horaFin":         self.hora_fin,
        }
