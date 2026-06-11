from pydantic import BaseModel, Field


# ── Schema de ENTRADA: actualizar perfil ──────────────────────
class PerfilClienteUpdate(BaseModel):
    nombre:     str   = Field(..., description="Nombre completo del cliente")
    telefono:   str   = Field(..., description="Teléfono de contacto")
    objetivos:  str   = Field(..., description="Objetivos de entrenamiento")
    pesoActual: float = Field(..., gt=0, description="Peso actual en kg")


# ── Schema de ENTRADA: registrar objetivos ────────────────────
class ObjetivosCreate(BaseModel):
    objetivos:  str   = Field(..., description="Descripción de los objetivos")
    pesoMeta:   float = Field(..., gt=0, description="Peso meta en kg")
    plazoMeses: int   = Field(..., gt=0, description="Plazo en meses para alcanzar el objetivo")


# ── Schema de SALIDA ──────────────────────────────────────────
class PerfilClienteResponse(BaseModel):
    idUsuario:  int
    nombre:     str
    correo:     str
    telefono:   str
    objetivos:  str
    pesoActual: float

    class Config:
        from_attributes = True


class ObjetivosResponse(BaseModel):
    idUsuario:  int
    objetivos:  str
    pesoMeta:   float
    plazoMeses: int

    class Config:
        from_attributes = True


# ── Modelo interno del dominio ────────────────────────────────
class PerfilCliente:
    def __init__(self, id_usuario: int, nombre: str, telefono: str,
                 objetivos: str, peso_actual: float,
                 peso_meta: float = 0.0, plazo_meses: int = 0):
        self.id_usuario  = id_usuario
        self.nombre      = nombre
        self.telefono    = telefono
        self.objetivos   = objetivos
        self.peso_actual = peso_actual
        self.peso_meta   = peso_meta
        self.plazo_meses = plazo_meses

    def to_response(self) -> dict:
        return {
            "idUsuario":  self.id_usuario,
            "nombre":     self.nombre,
            "objetivos":  self.objetivos,
            "pesoActual": self.peso_actual,
        }

    def to_objetivos_response(self) -> dict:
        return {
            "idUsuario":  self.id_usuario,
            "objetivos":  self.objetivos,
            "pesoMeta":   self.peso_meta,
            "plazoMeses": self.plazo_meses,
        }