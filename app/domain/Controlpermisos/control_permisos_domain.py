from pydantic import BaseModel, Field, field_validator
from typing import Literal


# ── Mapa de permisos por rol ──────────────────────────────────
# Define qué acciones puede ejecutar cada rol sobre cada recurso
PERMISOS: dict[str, dict[str, set[str]]] = {
    "CLIENTE": {
        "rutinas":      {"VER"},
        "pagos":        {"CREAR", "VER"},
        "planes":       {"SUSCRIBIR", "VER"},
        "reservas":     {"CREAR", "VER", "CANCELAR"},
        "perfil":       {"VER", "EDITAR"},
    },
    "ENTRENADOR": {
        "rutinas":      {"CREAR", "VER", "EDITAR", "ELIMINAR"},
        "reservas":     {"VER"},
        "perfil":       {"VER", "EDITAR"},
        "clientes":     {"VER"},
    },
}


# ── Schema de ENTRADA (lo que recibe la API del cliente) ──────
class ValidarAutorizacionCreate(BaseModel):
    token:   str = Field(..., description="JWT del usuario autenticado")
    recurso: str = Field(..., min_length=2, description="Recurso al que se intenta acceder")
    accion:  str = Field(..., min_length=2, description="Acción que se desea ejecutar")

    # ── REGLA DE NEGOCIO: acción debe estar en mayúsculas ────
    @field_validator("accion")
    @classmethod
    def accion_en_mayusculas(cls, v):
        return v.strip().upper()

    # ── REGLA DE NEGOCIO: recurso en minúsculas para consistencia ──
    @field_validator("recurso")
    @classmethod
    def recurso_en_minusculas(cls, v):
        return v.strip().lower()


# ── Schema de SALIDA (lo que devuelve la API al cliente) ──────
class ValidarAutorizacionResponse(BaseModel):
    idUsuario:  int
    autorizado: bool

    class Config:
        from_attributes = True


# ── Modelo interno del dominio (la "entidad real") ────────────
class ControlPermisos:
    def __init__(self, id_usuario: int, rol: str):
        self.id_usuario = id_usuario
        self.rol        = rol.upper()

    # REGLA DE NEGOCIO: verificar si el rol tiene permiso para la acción sobre el recurso
    def tiene_permiso(self, recurso: str, accion: str) -> bool:
        permisos_rol = PERMISOS.get(self.rol, {})
        acciones_permitidas = permisos_rol.get(recurso.lower(), set())
        return accion.upper() in acciones_permitidas

    # REGLA DE NEGOCIO: clientes NO pueden crear ni modificar rutinas
    def cliente_puede_modificar_rutina(self) -> bool:
        if self.rol == "CLIENTE":
            return False
        return True

    # REGLA DE NEGOCIO: entrenadores NO pueden realizar pagos ni suscribirse a planes
    def entrenador_puede_pagar(self) -> bool:
        if self.rol == "ENTRENADOR":
            return False
        return True

    def to_response(self) -> dict:
        return {
            "idUsuario":  self.id_usuario,
            "autorizado": True,
        }