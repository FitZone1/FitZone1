from pydantic import BaseModel, Field, field_validator


# ── Mapa de permisos por rol ──────────────────────────────────
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
        "horarios":     {"CREAR", "VER", "EDITAR"},
    },
}


# ── Schema de ENTRADA ─────────────────────────────────────────
class ValidarAutorizacionCreate(BaseModel):
    token:   str = Field(..., description="JWT del usuario autenticado")
    recurso: str = Field(..., min_length=2, description="Recurso al que se intenta acceder")
    accion:  str = Field(..., min_length=2, description="Acción que se desea ejecutar")

    @field_validator("accion")
    @classmethod
    def accion_en_mayusculas(cls, v):
        return v.strip().upper()

    @field_validator("recurso")
    @classmethod
    def recurso_en_minusculas(cls, v):
        return v.strip().lower()


# ── Schema de SALIDA ──────────────────────────────────────────
class ValidarAutorizacionResponse(BaseModel):
    idUsuario:  int
    autorizado: bool

    class Config:
        from_attributes = True


# ── Modelo interno del dominio ────────────────────────────────
class ControlPermisos:
    def __init__(self, id_usuario: int, rol: str):
        self.id_usuario = id_usuario
        self.rol        = rol.upper()

    # REGLA DE NEGOCIO: verificar si el rol tiene permiso
    def tiene_permiso(self, recurso: str, accion: str) -> bool:
        permisos_rol = PERMISOS.get(self.rol, {})
        acciones_permitidas = permisos_rol.get(recurso.lower(), set())
        return accion.upper() in acciones_permitidas

    # REGLA DE NEGOCIO: clientes NO pueden crear ni modificar rutinas
    def cliente_puede_modificar_rutina(self) -> bool:
        return self.rol != "CLIENTE"

    ## REGLA DE NEGOCIO: entrenadores NO pueden realizar pagos
    def entrenador_puede_pagar(self) -> bool:
        return self.rol != "ENTRENADOR"

    def to_response(self) -> dict:
        return {
            "idUsuario":  self.id_usuario,
            "autorizado": True,
        }