from app.domain.Cliente.ReservaSesion_domain import Reserva
from typing import Optional


class ReservaSesionRepository:

    def __init__(self):
        self._datos: list[Reserva] = []
        self._siguiente_id: int = 1
        self._seed()

    def _seed(self):
        iniciales = [
            Reserva(1, 42, 10, "2026-03-20T15:00:00", 1, "CONFIRMADA"),
            Reserva(2, 43, 11, "2026-03-21T10:00:00", 2, "COMPLETADA"),
        ]
        self._datos = iniciales
        self._siguiente_id = 3

    def obtener_todos(self) -> list[Reserva]:
        return self._datos.copy()

    def obtener_por_id(self, id: int) -> Optional[Reserva]:
        return next((r for r in self._datos if r.id == id), None)

    def obtener_por_cliente(self, id_cliente: int) -> list[Reserva]:
        return [r for r in self._datos if r.id_cliente == id_cliente]

    def obtener_por_entrenador(self, id_entrenador: int) -> list[Reserva]:
        return [r for r in self._datos if r.id_entrenador == id_entrenador]

    def existe_conflicto(self, id_entrenador: int, fecha: str) -> bool:
        return any(r for r in self._datos
                   if r.id_entrenador == id_entrenador
                   and r.fecha == fecha
                   and r.estado == "CONFIRMADA")

    def cliente_tiene_conflicto(self, id_cliente: int, fecha: str) -> bool:
        return any(r for r in self._datos
                   if r.id_cliente == id_cliente
                   and r.fecha == fecha
                   and r.estado == "CONFIRMADA")

    def contar_reservas_dia(self, id_entrenador: int, fecha: str) -> int:
        dia = fecha[:10]
        return len([r for r in self._datos
                    if r.id_entrenador == id_entrenador
                    and r.fecha[:10] == dia
                    and r.estado == "CONFIRMADA"])

    def crear(self, id_cliente: int, id_entrenador: int,
              fecha: str, id_zona: int) -> Reserva:
        nueva = Reserva(
            id            = self._siguiente_id,
            id_cliente    = id_cliente,
            id_entrenador = id_entrenador,
            fecha         = fecha,
            id_zona       = id_zona,
            estado        = "CONFIRMADA",
        )
        self._datos.append(nueva)
        self._siguiente_id += 1
        return nueva

    def actualizar_estado(self, id: int, estado: str) -> Optional[Reserva]:
        reserva = self.obtener_por_id(id)
        if not reserva:
            return None
        reserva.estado = estado
        return reserva


# Instancia única compartida (Singleton simple)
reserva_sesion_repository = ReservaSesionRepository()
