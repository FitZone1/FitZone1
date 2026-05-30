from app.domain.Entrenador.GestionHorarios_domain import GestionHorariosCreate, GestionHorariosResponse
from app.repository.Entrenador.GestionHorarios_repository import GestionHorariosRepository
from app.repository.Cliente.ReservaSesion_repository import ReservaSesionRepository


class GestionHorariosService:

    def __init__(self, repo: GestionHorariosRepository,
                 reserva_repo: ReservaSesionRepository):
        self.repo         = repo
        self.reserva_repo = reserva_repo

    def publicar_disponibilidad(self, datos: GestionHorariosCreate) -> GestionHorariosResponse:
        # Regla de negocio: verificar si ya existe un horario para este entrenador
        horario_existente = self.repo.obtener_por_entrenador(datos.idEntrenador)

        if horario_existente:
            # Regla de negocio: no se puede modificar si hay reservas confirmadas activas
            reservas_activas = self.reserva_repo.obtener_por_entrenador(datos.idEntrenador)
            confirmadas = [r for r in reservas_activas if r.estado == "CONFIRMADA"]
            if confirmadas:
                raise PermissionError("HOR_ACTIVE_BOOKING_EXISTS")

            h = self.repo.actualizar(
                id_entrenador    = datos.idEntrenador,
                dias_disponibles = datos.diasDisponibles,
                hora_inicio      = datos.horaInicio,
                hora_fin         = datos.horaFin,
            )
        else:
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
            raise ValueError(f"No hay horario registrado para el entrenador {id_entrenador}")
        return GestionHorariosResponse(**h.to_response())
