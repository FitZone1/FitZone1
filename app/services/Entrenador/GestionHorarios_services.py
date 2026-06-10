from app.domain.Entrenador.GestionHorarios_domain import GestionHorariosCreate, GestionHorariosResponse
from app.repository.Entrenador.GestionHorarios_repository import GestionHorariosRepository
from app.repository.Cliente.ReservaSesion_repository import ReservaSesionRepository


class GestionHorariosService:

    def __init__(self, repo: GestionHorariosRepository,
                 reserva_repo: ReservaSesionRepository):
        self.repo         = repo
        self.reserva_repo = reserva_repo

    def publicar_disponibilidad(self, datos: GestionHorariosCreate) -> GestionHorariosResponse:
        # Regla de negocio: validar rango horario
        if datos.horaFin <= datos.horaInicio:
            raise ValueError("HOR_INVALID_TIME_RANGE")

        h = self.repo.crear(
            id_entrenador    = datos.idEntrenador,
            dias_disponibles = datos.diasDisponibles,
            hora_inicio      = datos.horaInicio,
            hora_fin         = datos.horaFin,
        )
        return GestionHorariosResponse(**h.to_response())

    def obtener_horario(self, id_entrenador: int) -> GestionHorariosResponse:
        h = self.repo.obtener_por_entrenador(id_entrenador)
        if not h:
            raise ValueError("HOR_NOT_FOUND")
        return GestionHorariosResponse(**h.to_response())