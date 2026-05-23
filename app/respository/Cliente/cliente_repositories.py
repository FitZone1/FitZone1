# ─────────────────────────────────────────────────────────────
# CAPA REPOSITORIO — única responsabilidad: guardar y recuperar
# Solo manipula datos. Sin lógica de negocio aquí.
# ─────────────────────────────────────────────────────────────

from domain.Cliente.cliente_domain import Cliente
from typing import Optional

class ClienteRepository:

    def __init__(self):
        # Almacén en memoria: lista de objetos Cliente
        self._datos: list[Cliente] = []
        self._siguiente_id: int = 1

        # Datos de ejemplo para arrancar el sistema
        self._seed()

    def _seed(self):
        """Carga datos iniciales de ejemplo."""
        iniciales = [
            Cliente(1, "Juan Pérez",    "juan@fitzone.com",   "3001234567", "hashed_pass_1", "ACTIVO"),
            Cliente(2, "María López",   "maria@fitzone.com",  "3109876543", "hashed_pass_2", "ACTIVO"),
            Cliente(3, "Carlos Ruiz",   "carlos@fitzone.com", "3205551234", "hashed_pass_3", "PENDIENTE"),
        ]
        self._datos = iniciales
        self._siguiente_id = 4

    # ── CRUD básico ───────────────────────────────────────────

    def obtener_todos(self) -> list[Cliente]:
        return self._datos.copy()

    def obtener_por_id(self, id: int) -> Optional[Cliente]:
        return next((c for c in self._datos if c.id == id), None)

    def obtener_por_correo(self, correo: str) -> Optional[Cliente]:
        return next((c for c in self._datos
                     if c.correo.lower() == correo.lower()), None)

    def crear(self, nombre: str, correo: str,
              telefono: str, contrasena: str) -> Cliente:
        nuevo = Cliente(
            id              = self._siguiente_id,
            nombre          = nombre,
            correo          = correo,
            telefono        = telefono,
            contrasena = contrasena,
            estado          = "PENDIENTE",   # siempre inicia pendiente
        )
        self._datos.append(nuevo)
        self._siguiente_id += 1
        return nuevo

    def actualizar_estado(self, id: int, estado: str) -> Optional[Cliente]:
        cliente = self.obtener_por_id(id)
        if not cliente:
            return None
        cliente.estado = estado
        return cliente

    def eliminar(self, id: int) -> bool:
        cliente = self.obtener_por_id(id)
        if not cliente:
            return False
        self._datos.remove(cliente)
        return True

    def correo_existe(self, correo: str) -> bool:
        return self.obtener_por_correo(correo) is not None

    def obtener_por_estado(self, estado: str) -> list[Cliente]:
        return [c for c in self._datos
                if c.estado.upper() == estado.upper()]


# Instancia única compartida (Singleton simple)
cliente_repository = ClienteRepository()