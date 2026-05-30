from app.domain.Cliente.CancelarReserva_domain import CancelarReservaCreate, CancelarReservaResponse
from app.repository.Cliente.CancelarReserva_repository import CancelarReservaRepository


class CancelarReservaService:

    def __init__(self, repo: CancelarReservaRepository):
        self.repo = repo

    def cancelar(self, id_reserva: int, datos: CancelarReservaCreate) -> CancelarReservaResponse:
        reserva = self.repo.obtener_por_id(id_reserva)

        # Regla de negocio: la reserva debe existir
        if not reserva:
            raise ValueError(f"Reserva con id {id_reserva} no encontrada")

        # Regla de negocio: no se puede cancelar una reserva completada
        if reserva.esta_completada():
            raise PermissionError("RES_ALREADY_COMPLETED")

        # Regla de negocio: solo se pueden cancelar reservas CONFIRMADAS
        if not reserva.puede_cancelarse():
            raise ValueError(f"La reserva no puede cancelarse en estado '{reserva.estado}'")

        self.repo.cancelar(id_reserva)
        return CancelarReservaResponse(idReserva=id_reserva, estado="CANCELADA")
