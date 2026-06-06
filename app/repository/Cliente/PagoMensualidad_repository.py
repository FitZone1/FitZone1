from app.domain.Cliente.PagoMensualidad_domain import Pago
from typing import Optional


class PagoMensualidadRepository:

    def __init__(self):
        self._datos: list[Pago] = []
        self._seed()

    def _seed(self):
        iniciales = [
            Pago("PAY-000001", 42, 1, 55000, "APROBADO",  "2026-02-18T10:00:00", "EFECTIVO",  None),
            Pago("PAY-000002", 43, 2, 85000, "RECHAZADO", "2026-02-20T11:00:00", "TARJETA",   "4111111111111111"),
            Pago("PAY-000003", 10, 2, 85000, "APROBADO",  "2026-03-01T09:00:00", "PSE",       "4222222222222222"),
        ]
        self._datos = iniciales

    def obtener_todos(self) -> list[Pago]:
        return self._datos.copy()

    def obtener_por_id(self, id_pago: str) -> Optional[Pago]:
        return next((p for p in self._datos if p.id_pago == id_pago), None)

    def obtener_por_cliente(self, id_cliente: int) -> list[Pago]:
        return [p for p in self._datos if p.id_cliente == id_cliente]

    def crear(self, id_pago: str, id_cliente: int, id_plan: int,
              monto: float, estado: str, fecha: str,
              metodo_pago: str, numero_tarjeta: Optional[str] = None) -> Pago:
        nuevo = Pago(
            id_pago        = id_pago,
            id_cliente     = id_cliente,
            id_plan        = id_plan,
            monto          = monto,
            estado         = estado,
            fecha          = fecha,
            metodo_pago    = metodo_pago,
            numero_tarjeta = numero_tarjeta,
        )
        self._datos.append(nuevo)
        return nuevo

    def actualizar_estado(self, id_pago: str, estado: str) -> Optional[Pago]:
        pago = self.obtener_por_id(id_pago)
        if not pago:
            return None
        pago.estado = estado
        return pago


# Instancia única compartida (Singleton simple)
pago_mensualidad_repository = PagoMensualidadRepository()