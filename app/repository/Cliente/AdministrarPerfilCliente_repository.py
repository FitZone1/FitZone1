from app.domain.Cliente.AdministrarPerfilCliente_domain import PerfilCliente
from typing import Optional


class AdministrarPerfilClienteRepository:

    def __init__(self):
        self._datos: list[PerfilCliente] = []
        self._seed()

    def _seed(self):
        iniciales = [
            PerfilCliente(42, "Angela Shilel", "3001234567", "Bajar de peso",       68.5),
            PerfilCliente(43, "Carlos Pérez",  "3109876543", "Ganar masa muscular", 75.0),
            PerfilCliente(44, "Laura Gómez",   "3157654321", "Mejorar resistencia", 62.0),
        ]
        self._datos = iniciales

    def obtener_por_id(self, id_usuario: int) -> Optional[PerfilCliente]:
        return next((p for p in self._datos if p.id_usuario == id_usuario), None)

    def actualizar(self, id_usuario: int, nombre: str, telefono: str,
                   objetivos: str, peso_actual: float) -> Optional[PerfilCliente]:
        perfil = self.obtener_por_id(id_usuario)
        if not perfil:
            return None
        perfil.nombre      = nombre
        perfil.telefono    = telefono
        perfil.objetivos   = objetivos
        perfil.peso_actual = peso_actual
        return perfil

    def registrar_objetivos(self, id_usuario: int, objetivos: str,
                            peso_meta: float, plazo_meses: int) -> Optional[PerfilCliente]:
        perfil = self.obtener_por_id(id_usuario)
        if not perfil:
            return None
        perfil.objetivos   = objetivos
        perfil.peso_meta   = peso_meta
        perfil.plazo_meses = plazo_meses
        return perfil


# Instancia única compartida (Singleton simple)
administrar_perfil_cliente_repository = AdministrarPerfilClienteRepository()
