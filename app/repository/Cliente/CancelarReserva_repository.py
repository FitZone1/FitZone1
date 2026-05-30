from app.domain.Cliente.ReservaSesion_domain import Reserva
from app.repository.Cliente.ReservaSesion_repository import ReservaSesionRepository, reserva_sesion_repository
from typing import Optional


class CancelarReservaRepository:

    def __init__(self, reserva_repo: ReservaSesionRepository):
        # Reutiliza el repositorio de reservas
        self.reserva_repo = reserva_repo

    def obtener_por_id(self, id: int) -> Optional[Reserva]:
        return self.reserva_repo.obtener_por_id(id)

    def cancelar(self, id: int) -> Optional[Reserva]:
        return self.reserva_repo.actualizar_estado(id, "CANCELADA")


# Instancia única compartida (Singleton simple)
cancelar_reserva_repository = CancelarReservaRepository(reserva_repo=reserva_sesion_repository)
