# ─────────────────────────────────────────────────────────────
# CAPA REPOSITORIO — única responsabilidad: guardar y recuperar
# Solo manipula datos. Sin lógica de negocio aquí.
# ─────────────────────────────────────────────────────────────

from domain.Controlpermisos.control_permisos_domain import ControlPermisos
from typing import Optional


class ControlPermisosRepository:

    def __init__(self):
        # Almacén en memoria: { id_usuario: ControlPermisos }
        self._datos: dict[int, ControlPermisos] = {}

        # Datos de ejemplo para arrancar el sistema
        self._seed()

    def _seed(self):
        """Carga perfiles de permisos iniciales de ejemplo."""
        iniciales = [
            ControlPermisos(1,  "CLIENTE"),
            ControlPermisos(2,  "CLIENTE"),
            ControlPermisos(10, "ENTRENADOR"),
            ControlPermisos(11, "ENTRENADOR"),
        ]
        for cp in iniciales:
            self._datos[cp.id_usuario] = cp

    # ── Operaciones de consulta ───────────────────────────────

    def obtener_por_usuario(self, id_usuario: int) -> Optional[ControlPermisos]:
        """Devuelve el perfil de permisos de un usuario por su ID."""
        return self._datos.get(id_usuario)

    def obtener_todos(self) -> list[ControlPermisos]:
        return list(self._datos.values())

    # ── Operaciones de escritura ──────────────────────────────

    def crear(self, id_usuario: int, rol: str) -> ControlPermisos:
        """Registra el perfil de permisos de un usuario recién creado."""
        nuevo = ControlPermisos(id_usuario=id_usuario, rol=rol)
        self._datos[id_usuario] = nuevo
        return nuevo

    def actualizar_rol(self, id_usuario: int, nuevo_rol: str) -> Optional[ControlPermisos]:
        """Cambia el rol asignado a un usuario."""
        perfil = self.obtener_por_usuario(id_usuario)
        if not perfil:
            return None
        perfil.rol = nuevo_rol.upper()
        return perfil

    def eliminar(self, id_usuario: int) -> bool:
        """Elimina el perfil de permisos de un usuario."""
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