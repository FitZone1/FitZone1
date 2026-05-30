from app.domain.ControlPermisos.ControlPermisos_domain import ControlPermisos
from typing import Optional


class ControlPermisosRepository:

    def __init__(self):
        self._datos: dict[int, ControlPermisos] = {}
        self._seed()

    def _seed(self):
        iniciales = [
            ControlPermisos(1,  "CLIENTE"),
            ControlPermisos(2,  "CLIENTE"),
            ControlPermisos(10, "ENTRENADOR"),
            ControlPermisos(11, "ENTRENADOR"),
        ]
        for cp in iniciales:
            self._datos[cp.id_usuario] = cp

    def obtener_por_usuario(self, id_usuario: int) -> Optional[ControlPermisos]:
        return self._datos.get(id_usuario)

    def obtener_todos(self) -> list[ControlPermisos]:
        return list(self._datos.values())

    def crear(self, id_usuario: int, rol: str) -> ControlPermisos:
        nuevo = ControlPermisos(id_usuario=id_usuario, rol=rol)
        self._datos[id_usuario] = nuevo
        return nuevo

    def actualizar_rol(self, id_usuario: int, nuevo_rol: str) -> Optional[ControlPermisos]:
        perfil = self.obtener_por_usuario(id_usuario)
        if not perfil:
            return None
        perfil.rol = nuevo_rol.upper()
        return perfil

    def eliminar(self, id_usuario: int) -> bool:
        if id_usuario not in self._datos:
            return False
        del self._datos[id_usuario]
        return True

    def usuario_registrado(self, id_usuario: int) -> bool:
        return id_usuario in self._datos

    def obtener_por_rol(self, rol: str) -> list[ControlPermisos]:
        return [cp for cp in self._datos.values()
                if cp.rol.upper() == rol.upper()]


# Instancia única compartida (Singleton simple)
control_permisos_repository = ControlPermisosRepository()