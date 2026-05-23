from pydantic import BaseModel
from typing import Optional


# ── Modelo base: campos comunes ──────────────────
class ClienteBase(BaseModel):
    name: str
    correo: str
    telefono: int
    ciudad: str


# ── Para CREAR un cliente (sin ID) ─────────────
class ClienteCreate(ClienteBase):
    pass


# ── Respuesta completa (con ID) ──────────────────
class Cliente(ClienteBase):
    id: int

    class Config:
        # Permite leer datos desde atributos de objeto
        from_attributes = True