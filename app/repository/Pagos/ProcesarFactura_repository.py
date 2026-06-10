from app.domain.Pagos.ProcesarFactura_domain import Factura
from datetime import datetime, timezone
from typing import Optional


class ProcesarFacturaRepository:

    def __init__(self):
        self._facturas: list[Factura] = []
        self._siguiente_factura_num: int = 1

    # ── Pagos — delega al repositorio real de pagos ───────────
    def obtener_pago(self, id_pago: str, id_cliente: int):
        """
        Busca el pago en el repositorio de PagoMensualidad (fuente de verdad).
        Retorna el pago solo si pertenece al cliente indicado.
        """
        from app.repository.Cliente.PagoMensualidad_repository import pago_mensualidad_repository
        pago = pago_mensualidad_repository.obtener_por_id(id_pago)
        if pago and pago.id_cliente == id_cliente:
            return pago
        return None

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

    def crear_factura(self, pago) -> Factura:
        id_factura = f"FAC-{self._siguiente_factura_num:06d}"
        fecha      = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
        nueva = Factura(
            id_factura     = id_factura,
            id_pago        = pago.id_pago,
            monto          = pago.monto,
            fecha          = fecha,
            url_descarga   = f"/facturas/{id_factura}.pdf",
            plan           = str(pago.id_plan),  # PagoMensualidad guarda id_plan (int)
            nombre_cliente = f"Cliente {pago.id_cliente}",
        )
        self._facturas.append(nueva)
        self._siguiente_factura_num += 1
        return nueva


# Instancia única compartida (Singleton simple)
procesar_factura_repository = ProcesarFacturaRepository()