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
    idCliente:  int
    nombre:     str
    objetivos:  str
    pesoActual: float

    class Config:
        from_attributes = True


class ObjetivosResponse(BaseModel):
    idCliente:  int
    objetivos:  str
    pesoMeta:   float
    plazoMeses: int

    class Config:
        from_attributes = True


# ── Modelo interno del dominio ────────────────────────────────
class PerfilCliente:
    def __init__(self, id_cliente: int, nombre: str, telefono: str,
                 objetivos: str, peso_actual: float,
                 peso_meta: float = 0.0, plazo_meses: int = 0):
        self.id_cliente  = id_cliente
        self.nombre      = nombre
        self.telefono    = telefono
        self.objetivos   = objetivos
        self.peso_actual = peso_actual
        self.peso_meta   = peso_meta
        self.plazo_meses = plazo_meses

    def to_response(self) -> dict:
        return {
            "idCliente":  self.id_cliente,
            "nombre":     self.nombre,
            "objetivos":  self.objetivos,
            "pesoActual": self.peso_actual,
        }

    def to_objetivos_response(self) -> dict:
        return {
            "idCliente":  self.id_cliente,
            "objetivos":  self.objetivos,
            "pesoMeta":   self.peso_meta,
            "plazoMeses": self.plazo_meses,
        }
