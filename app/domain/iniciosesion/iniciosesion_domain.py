from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re


# ── Schema de ENTRADA (lo que recibee la API del cliente) ──────
class InicioSesionCreate(BaseModel):
    correo:     str = Field(..., description="Correo electrónico registrado")
    contrasena: str = Field(..., min_length=1, description="Contraseña del usuario")

    # ── REGLA DE NEGOCIO: correo debe tener formato válido ───
    @field_validator("correo")
    @classmethod
    def correo_valido(cls, v):
        patron = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        if not re.match(patron, v):
            raise ValueError("El correo electrónico no tiene un formato válido")
        return v.strip().lower()


# ── Schema de SALIDA (lo que devuelve la API al cliente) ──────
class InicioSesionResponse(BaseModel):
    idUsuario: int
    nombre:    str
    rol:       str    # "CLIENTE" o "ENTRENADOR"
    token:     str    # JWT generado por el backend

    class Config:
        from_attributes = True


# ── Modelo interno del dominio (la "entidad real") ────────────
class Sesion:
    ROLES_VALIDOS = {"CLIENTE", "ENTRENADOR"}

    def __init__(self, id_usuario: int, nombre: str, rol: str, token: str):
        self.id_usuario = id_usuario
        self.nombre     = nombre
        self.rol        = rol
        self.token      = token

    # REGLA DE NEGOCIO: el rol del token debe ser CLIENTE o ENTRENADOR
    def rol_es_valido(self) -> bool:
        return self.rol in self.ROLES_VALIDOS

    # REGLA DE NEGOCIO: el token no puede estar vacío
    def token_generado(self) -> bool:
        return bool(self.token and self.token.strip())

    def to_response(self) -> dict:
        return {
            "idUsuario": self.id_usuario,
            "nombre":    self.nombre,
            "rol":       self.rol,
            "token":     self.token,
        }