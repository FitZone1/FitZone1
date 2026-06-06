from app.domain.Entrenador.EntrenadoresDisponibles_domain import EntrenadorDisponible
from typing import Optional


class EntrenadoresDisponiblesRepository:

    def __init__(self):
        self._datos: list[EntrenadorDisponible] = []
        self._seed()

    def _seed(self):
        iniciales = [
            EntrenadorDisponible(1, "Carlos Villamizar", "Musculación", 4.8, True),
            EntrenadorDisponible(2, "Sofía Ramírez",     "Yoga",        4.5, True),
            EntrenadorDisponible(3, "Andrés Torres",     "Crossfit",    4.2, False),
            EntrenadorDisponible(4, "Laura Gómez",       "Musculación", 4.9, True),
        ]
        self._datos = iniciales

    def obtener_todos(self) -> list[EntrenadorDisponible]:
        return self._datos.copy()

    def obtener_disponibles(self) -> list[EntrenadorDisponible]:
        return [e for e in self._datos if e.disponible]

    def obtener_por_especialidad(self, especialidad: str) -> list[EntrenadorDisponible]:
        return [e for e in self._datos
                if e.especialidad.lower() == especialidad.lower() and e.disponible]

    def obtener_por_id(self, id: int) -> Optional[EntrenadorDisponible]:
        return next((e for e in self._datos if e.id == id), None)

    def actualizar_disponibilidad(self, id: int, disponible: bool) -> Optional[EntrenadorDisponible]:
        entrenador = self.obtener_por_id(id)
        if not entrenador:
            return None
        entrenador.disponible = disponible
        return entrenador


# Instancia única compartida (Singleton simple)
entrenadores_disponibles_repository = EntrenadoresDisponiblesRepository()