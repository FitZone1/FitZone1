from app.domain.Entrenador.EntrenadoresDisponibles_domain import EntrenadoresDisponiblesFilter, EntrenadorDisponibleResponse
from app.repository.Entrenador.EntrenadoresDisponibles_repository import EntrenadoresDisponiblesRepository
from typing import Optional


class EntrenadoresDisponiblesService:

    def __init__(self, repo: EntrenadoresDisponiblesRepository):
        self.repo = repo

    def listar_disponibles(self, especialidad: Optional[str] = None) -> list[EntrenadorDisponibleResponse]:
        if especialidad:
            entrenadores = self.repo.obtener_por_especialidad(especialidad)
        else:
            entrenadores = self.repo.obtener_disponibles()

        if not entrenadores:
            raise ValueError("No se encontraron entrenadores con los filtros seleccionados")

        return [EntrenadorDisponibleResponse(**e.to_response()) for e in entrenadores]
