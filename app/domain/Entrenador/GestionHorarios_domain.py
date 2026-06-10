from pydantic import BaseModel, Field
from typing import List


DIAS_VALIDOS = {"LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES", "SABADO", "DOMINGO"}


# ── Schema de ENTRADA ─────────────────────────────────────────
class GestionHorariosCreate(BaseModel):
    idEntrenador:    int       = Field(..., gt=0, description="ID del entrenador")
    diasDisponibles: List[str] = Field(..., description="Días disponibles de la semana")
    horaInicio:      str       = Field(..., description="Hora de inicio (HH:MM)")
    horaFin:         str       = Field(..., description="Hora de fin (HH:MM)")


# ── Schema de SALIDA ──────────────────────────────────────────
class GestionHorariosResponse(BaseModel):
    idHorario:       int
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

    def rango_valido(self) -> bool:
        return self.hora_inicio < self.hora_fin

    def dia_disponible(self, dia: str) -> bool:
        return dia.upper() in self.dias_disponibles

    def to_response(self) -> dict:
        return {
            "idHorario":       self.id,
            "idEntrenador":    self.id_entrenador,
            "diasDisponibles": self.dias_disponibles,
            "horaInicio":      self.hora_inicio,
            "horaFin":         self.hora_fin,
        }