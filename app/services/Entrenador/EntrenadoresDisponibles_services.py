from app.domain.Entrenador.EntrenadoresDisponibles_domain import EntrenadoresDisponiblesFilter, EntrenadorDisponibleResponse
from app.repository.Entrenador.EntrenadoresDisponibles_repository import EntrenadoresDisponiblesRepository
from typing import Optional


class EntrenadoresDisponiblesService:

    def __init__(self, repo: EntrenadoresDisponiblesRepository):
        self.repo = repo

    def listar_disponibles(
        self,
        especialidad: Optional[str] = None,
        disponible: Optional[bool] = True,
    ) -> list[EntrenadorDisponibleResponse]:

        if especialidad:
            # Caso 2: filtro por especialidad (solo entre disponibles)
            entrenadores = self.repo.obtener_por_especialidad(especialidad)
        elif disponible:
            # Caso 1: todos los disponibles
            entrenadores = self.repo.obtener_disponibles()
        else:
            # disponible=false explícito: retornar todos sin filtro
            entrenadores = self.repo.obtener_todos()

        if not entrenadores:
            raise ValueError("No se encontraron entrenadores con los filtros seleccionados")

        return [EntrenadorDisponibleResponse(**e.to_response()) for e in entrenadores]