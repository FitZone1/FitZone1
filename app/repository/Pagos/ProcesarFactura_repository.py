# ─────────────────────────────────────────────────────────────
# CAPA REPOSITORY — acceso a datos
# Sin lógica de negocio.
# ─────────────────────────────────────────────────────────────

from typing import Optional
from app.repository.Cliente.PagoMensualidad_repository import pago_mensualidad_repository


# ── Facturas en memoria ───────────────────────────────────────

_facturas_db:    dict = {}  # { idFactura: dict }
_factura_x_pago: dict = {}  # { idPago: idFactura } — evita duplicados
_sequence_id:    int  = 0


def _next_id() -> str:
    global _sequence_id
    _sequence_id += 1
    return f"FAC-{_sequence_id:06d}"


# ── Repositorio unificado ─────────────────────────────────────

class ProcesarFacturaRepository:

    # ── Pagos — lee directo del repositorio de PagoMensualidad ──

    def obtener_pago(self, id_pago: str) -> Optional[dict]:
        """
        Busca el pago en el repositorio real de PagoMensualidad.
        Retorna un dict con los campos que necesita el service, o None.
        """
        pago = pago_mensualidad_repository.obtener_por_id(id_pago)
        if not pago:
            return None
        return {
            "idPago":        pago.id_pago,
            "idCliente":     pago.id_cliente,
            "estado":        pago.estado,
            "monto":         pago.monto,
            "plan":          f"Plan {pago.id_plan}",
            "nombreCliente": f"Cliente {pago.id_cliente}",
        }

    # ── Facturas ──────────────────────────────────────────────

    def obtener_factura_por_pago(self, id_pago: str) -> Optional[dict]:
        """Retorna la factura ya generada para ese pago, o None."""
        id_factura = _factura_x_pago.get(id_pago)
        if not id_factura:
            return None
        return _facturas_db.get(id_factura)

    def obtener_factura_por_id(self, id_factura: str) -> Optional[dict]:
        return _facturas_db.get(id_factura)

    def guardar_factura(self, pago: dict, fecha: str) -> dict:
        """Crea y persiste una nueva factura a partir del pago."""
        id_factura = _next_id()
        factura = {
            "idFactura":     id_factura,
            "idPago":        pago["idPago"],
            "monto":         pago["monto"],
            "fecha":         fecha,
            "plan":          pago["plan"],
            "nombreCliente": pago["nombreCliente"],
        }
        _facturas_db[id_factura]        = factura
        _factura_x_pago[pago["idPago"]] = id_factura
        return factura


# Singleton
procesar_factura_repository = ProcesarFacturaRepository()