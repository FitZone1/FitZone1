from app.domain.Cliente.ReservaSesion_domain import ReservaSesionCreate, ReservaSesionResponse
from app.repository.Cliente.ReservaSesion_repository import ReservaSesionRepository

MAX_CLIENTES_POR_DIA = 8


class ReservaSesionService:

    def __init__(self, repo: ReservaSesionRepository):
        self.repo = repo

    def crear_reserva(self, datos: ReservaSesionCreate) -> ReservaSesionResponse:
        # Regla de negocio: no puede haber conflicto de horario para el entrenador
        if self.repo.existe_conflicto(datos.idEntrenador, datos.fecha):
            raise ValueError("RES_SCHEDULE_CONFLICT")

        # Regla de negocio: el cliente no puede tener dos reservas en el mismo horario
        if self.repo.cliente_tiene_conflicto(datos.idCliente, datos.fecha):
            raise ValueError("RES_SCHEDULE_CONFLICT")

        # Regla de negocio: el entrenador no puede superar el máximo de clientes por día
        if self.repo.contar_reservas_dia(datos.idEntrenador, datos.fecha) >= MAX_CLIENTES_POR_DIA:
            raise ValueError("RES_MAX_CAPACITY_REACHED")

        r = self.repo.crear(
            id_cliente    = datos.idCliente,
            id_entrenador = datos.idEntrenador,
            fecha         = datos.fecha,
            id_zona       = datos.idZona,
        )
        return ReservaSesionResponse(**r.to_response())

    def listar(self) -> list[ReservaSesionResponse]:
        return [ReservaSesionResponse(**r.to_response())
                for r in self.repo.obtener_todos()]

    def obtener(self, id: int) -> ReservaSesionResponse:
        r = self.repo.obtener_por_id(id)
        if not r:
            raise ValueError(f"Reserva con id {id} no encontrada")
        return ReservaSesionResponse(**r.to_response())
