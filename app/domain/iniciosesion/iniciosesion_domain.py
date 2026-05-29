from pydantic import BaseModel, Field, field_validator
import re


# ── Schema de ENTRADA ─────────────────────────────────────────
class InicioSesionCreate(BaseModel):
    correo:     str = Field(..., description="Correo electrónico registrado")
    contrasena: str = Field(..., min_length=1, description="Contraseña del usuario")

    @field_validator("correo")
    @classmethod
    def correo_valido(cls, v):
        patron = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        if not re.match(patron, v):
            raise ValueError("El correo electrónico no tiene un formato válido")
        return v.strip().lower()


# ── Schema de SALIDA ──────────────────────────────────────────
class InicioSesionResponse(BaseModel):
    idUsuario: int
    nombre:    str
    rol:       str
    token:     str

    class Config:
        from_attributes = True


# ── Modelo interno del dominio ────────────────────────────────
class Sesion:
    ROLES_VALIDOS = {"CLIENTE", "ENTRENADOR"}

    def __init__(self, id_usuario: int, nombre: str, rol: str, token: str):
        self.id_usuario = id_usuario
        self.nombre     = nombre
        self.rol        = rol
        self.token      = token

    def rol_es_valido(self) -> bool:
        return self.rol in self.ROLES_VALIDOS

    def token_generado(self) -> bool:
        return bool(self.token and self.token.strip())

    def to_response(self) -> dict:
        return {
            "idUsuario": self.id_usuario,
            "nombre":    self.nombre,
            "rol":       self.rol,
            "token":     self.token,
        }
