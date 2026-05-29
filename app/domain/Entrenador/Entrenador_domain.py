from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re


# ── Schema de ENTRADA (lo que recibe la API del cliente) ──────
class RegistroEntrenadorCreate(BaseModel):
    nombre:       str = Field(..., min_length=2, description="Nombre completo del entrenador")
    correo:       str = Field(..., description="Correo electrónico único del entrenador")
    contrasena:   str = Field(..., min_length=8, description="Contraseña con mínimo 8 caracteres")
    especialidad: str = Field(..., min_length=3, description="Especialidad principal del entrenador")
    gimnasioId:   int = Field(..., gt=0, description="ID del gimnasio al que pertenece")

    @field_validator("correo")
    @classmethod
    def correo_valido(cls, v):
        patron = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        if not re.match(patron, v):
            raise ValueError("El correo electrónico no tiene un formato válido")
        return v.strip().lower()

    @field_validator("contrasena")
    @classmethod
    def contrasena_segura(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError("La contraseña debe contener al menos una letra mayúscula")
        if not any(c.isdigit() for c in v):
            raise ValueError("La contraseña debe contener al menos un número")
        return v

    @field_validator("especialidad")
    @classmethod
    def especialidad_sin_numeros(cls, v):
        if any(c.isdigit() for c in v):
            raise ValueError("La especialidad no puede contener números")
        return v.strip().title()


# ── Schema de SALIDA (lo que devuelve la API al cliente) ──────
class RegistroEntrenadorResponse(BaseModel):
    idUsuario:    int
    nombre:       str
    rol:          str
    especialidad: str

    class Config:
        from_attributes = True


# ── Modelo interno del dominio ────────────────────────────────
class Entrenador:
    ROL = "ENTRENADOR"

    def __init__(self, id: int, nombre: str, correo: str,
                 contrasena: str, especialidad: str,
                 gimnasio_id: int, estado: str = "ACTIVO"):
        self.id          = id
        self.nombre      = nombre
        self.correo      = correo
        self.contrasena  = contrasena
        self.especialidad = especialidad
        self.gimnasio_id = gimnasio_id
        self.estado      = estado
        self.rol         = self.ROL

    def es_visible(self) -> bool:
        return self.estado == "ACTIVO"

    def puede_realizar_pago(self) -> bool:
        return False

    def to_response(self) -> dict:
        return {
            "idUsuario":    self.id,
            "nombre":       self.nombre,
            "rol":          self.rol,
            "especialidad": self.especialidad,
        }