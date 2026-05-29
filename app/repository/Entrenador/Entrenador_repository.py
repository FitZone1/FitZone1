# ─────────────────────────────────────────────────────────────
# CAPA REPOSITORIO — única responsabilidad: guardar y recuperar
# Solo manipula datos. Sin lógica de negocio aquí.
# ─────────────────────────────────────────────────────────────

from domain.Entrenador.Entrenador_domain import Entrenador
from typing import Optional


class EntrenadorRepository:

    def __init__(self):
        # Almacén en memoria: lista de objetos Entrenador
        self._datos: list[Entrenador] = []
        self._siguiente_id: int = 1

        # Datos de ejemplo para arrancar el sistema
        self._seed()

    def _seed(self):
        """Carga datos iniciales de ejemplo."""
        iniciales = [
            Entrenador(1, "Carlos Villamizar", "carlos@fitzone.com", "hashed_pass_1", "Musculación",  1, "ACTIVO"),
            Entrenador(2, "Sofía Ramírez",     "sofia@fitzone.com",  "hashed_pass_2", "Yoga",         1, "ACTIVO"),
            Entrenador(3, "Andrés Torres",     "andres@fitzone.com", "hashed_pass_3", "Crossfit",     2, "INACTIVO"),
        ]
        self._datos = iniciales
        self._siguiente_id = 4

    # ── CRUD básicoo ───────────────────────────────────────────

    def obtener_todos(self) -> list[Entrenador]:
        return self._datos.copy()

    def obtener_por_id(self, id: int) -> Optional[Entrenador]:
        return next((e for e in self._datos if e.id == id), None)

    def obtener_por_correo(self, correo: str) -> Optional[Entrenador]:
        return next((e for e in self._datos
                     if e.correo.lower() == correo.lower()), None)

    def crear(self, nombre: str, correo: str, contrasena: str,
              especialidad: str, gimnasio_id: int) -> Entrenador:
        nuevo = Entrenador(
            id              = self._siguiente_id,
            nombre          = nombre,
            correo          = correo,
            contrasena = contrasena,
            especialidad    = especialidad,
            gimnasio_id     = gimnasio_id,
            estado          = "ACTIVO",   # entrenador queda activo al registrarse
        )
        self._datos.append(nuevo)
        self._siguiente_id += 1
        return nuevo

    def actualizar(self, id: int, nombre: str, especialidad: str,
                   gimnasio_id: int) -> Optional[Entrenador]:
        entrenador = self.obtener_por_id(id)
        if not entrenador:
            return None
        entrenador.nombre       = nombre
        entrenador.especialidad = especialidad
        entrenador.gimnasio_id  = gimnasio_id
        return entrenador

    def actualizar_estado(self, id: int, estado: str) -> Optional[Entrenador]:
        entrenador = self.obtener_por_id(id)
        if not entrenador:
            return None
        entrenador.estado = estado
        return entrenador

    def eliminar(self, id: int) -> bool:
        entrenador = self.obtener_por_id(id)
        if not entrenador:
            return False
        self._datos.remove(entrenador)
        return True

    def correo_existe(self, correo: str) -> bool:
        return self.obtener_por_correo(correo) is not None

    def obtener_por_gimnasio(self, gimnasio_id: int) -> list[Entrenador]:
        return [e for e in self._datos if e.gimnasio_id == gimnasio_id]

    def obtener_activos(self) -> list[Entrenador]:
        return [e for e in self._datos if e.estado == "ACTIVO"]


# Instancia única compartida (Singleton simple)
entrenador_repository = EntrenadorRepository()