from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re


# ── Schema de ENTRADA (lo que recibe la API del cliente) ──────
class RegistroClienteCreate(BaseModel):
    nombre:     str = Field(..., min_length=2, description="Nombre completo del cliente")
    correo:     str = Field(..., description="Correo electrónico único del cliente")
    telefono:   str = Field(..., min_length=7, description="Número de teléfono del cliente")
    contrasena: str = Field(..., min_length=8, description="Contraseña con mínimo 8 caracteres")

    # ── REGLA DE NEGOCIO: correo debe tener formato válido ───
    @field_validator("correo")
    @classmethod
    def correo_valido(cls, v):
        patron = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        if not re.match(patron, v):
            raise ValueError("El correo electrónico no tiene un formato válido")
        return v.strip().lower()

    # ── REGLA DE NEGOCIO: contraseña debe tener al menos una mayúscula y un número ──
    @field_validator("contrasena")
    @classmethod
    def contrasena_segura(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError("La contraseña debe contener al menos una letra mayúscula")
        if not any(c.isdigit() for c in v):
            raise ValueError("La contraseña debe contener al menos un número")
        return v

    # ── REGLA DE NEGOCIO: teléfono solo dígitos ─────────────
    @field_validator("telefono")
    @classmethod
    def telefono_solo_digitos(cls, v):
        limpio = v.replace(" ", "").replace("-", "")
        if not limpio.isdigit():
            raise ValueError("El teléfono solo puede contener dígitos")
        return limpio


# ── Schema de SALIDA (lo que devuelve la API al cliente) ──────
class RegistroClienteResponse(BaseModel):
    idUsuario: int
    nombre:    str
    rol:       str   # siempre "CLIENTE"
    estado:    str   # "PENDIENTE" hasta verificar correo

    class Config:
        from_attributes = True


# ── Modelo interno del dominio (la "entidad real") ────────────
class Cliente:
    ROL = "CLIENTE"

    def __init__(self, id: int, nombre: str, correo: str,
                 telefono: str, contrasena: str,
                 estado: str = "PENDIENTE"):
        self.id               = id
        self.nombre           = nombre
        self.correo           = correo
        self.telefono         = telefono
        self.contrasena       = contrasena
        self.estado           = estado   # PENDIENTE | ACTIVO | INACTIVO
        self.rol              = self.ROL

    # REGLA DE NEGOCIO: solo clientes ACTIVOS pueden iniciar sesión
    def puede_iniciar_sesion(self) -> bool:
        return self.estado == "ACTIVO"

    # REGLA DE NEGOCIO: activar cuenta tras verificar correo
    def activar_cuenta(self) -> None:
        if self.estado != "PENDIENTE":
            raise ValueError("Solo se pueden activar cuentas en estado PENDIENTE")
        self.estado = "ACTIVO"

    def to_response(self) -> dict:
        return {
            "idUsuario": self.id,
            "nombre":    self.nombre,
            "rol":       self.rol,
            "estado":    self.estado,
        }