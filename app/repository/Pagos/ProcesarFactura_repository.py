from app.domain.Cliente.procesarfactura_domain import Pago, Factura
from datetime import datetime, timezone
from typing import Optional


class ProcesarFacturaRepository:

    def __init__(self):
        self._pagos: list[Pago] = []
        self._facturas: list[Factura] = []
        self._siguiente_factura_num: int = 1
        self._seed()

    def _seed(self):
        """Pagos de ejemplo para que los casos de prueba funcionen autónomamente."""
        self._pagos = [
            Pago("PAY-987654", 42, 85000, "APROBADO",  "Plan Mensual Premium", "Carlos Pérez"),
            Pago("PAY-111111", 10, 55000, "APROBADO",  "Plan Básico",          "Ana López"),
            Pago("PAY-222222", 15, 85000, "RECHAZADO", "Plan Mensual Premium", "Luis García"),
            Pago("PAY-333333", 20, 85000, "PENDIENTE", "Plan Mensual Premium", "María Torres"),
        ]
        self._siguiente_factura_num = 1

    # ── Pagos ─────────────────────────────────────────────────

    def obtener_pago(self, id_pago: str, id_cliente: int) -> Optional[Pago]:
        return next(
            (p for p in self._pagos
             if p.id_pago == id_pago and p.id_cliente == id_cliente),
            None
        )

    # ── Facturas ──────────────────────────────────────────────

    def obtener_factura(self, id_factura: str) -> Optional[Factura]:
        return next(
            (f for f in self._facturas if f.id_factura == id_factura),
            None
        )

    def factura_ya_existe(self, id_pago: str) -> Optional[Factura]:
        """Evita generar una factura duplicada para el mismo pago."""
        return next(
            (f for f in self._facturas if f.id_pago == id_pago),
            None
        )

    def crear_factura(self, pago: Pago) -> Factura:
        id_factura = f"FAC-{self._siguiente_factura_num:06d}"
        fecha      = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
        nueva = Factura(
            id_factura     = id_factura,
            id_pago        = pago.id_pago,
            monto          = pago.monto,
            fecha          = fecha,
            url_descarga   = f"/facturas/{id_factura}.pdf",
            plan           = pago.plan,
            nombre_cliente = pago.nombre_cliente,
        )
        self._facturas.append(nueva)
        self._siguiente_factura_num += 1
        return nueva


# Instancia única compartida (Singleton simple)
procesar_factura_repository = ProcesarFacturaRepository()