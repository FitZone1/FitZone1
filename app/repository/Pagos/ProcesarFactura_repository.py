# ─────────────────────────────────────────────────────────────
# CAPA REPOSITORY — acceso a datos
# Sin lógica de negocio.
# ─────────────────────────────────────────────────────────────

from typing import Optional


# ── Simulación de pagos existentes en BD ─────────────────────

_pagos_db: dict = {
    "PAY-987654": {
        "idPago":        "PAY-987654",
        "idCliente":     42,
        "estado":        "APROBADO",
        "monto":         85000,
        "plan":          "Plan Mensual Premium",
        "nombreCliente": "Angela Torres",
    },
    "PAY-222222": {
        "idPago":        "PAY-222222",
        "idCliente":     42,
        "estado":        "RECHAZADO",
        "monto":         50000,
        "plan":          "Plan Básico",
        "nombreCliente": "Angela Torres",
    },
    "PAY-333333": {
        "idPago":        "PAY-333333",
        "idCliente":     15,
        "estado":        "PENDIENTE",
        "monto":         60000,
        "plan":          "Plan Semestral",
        "nombreCliente": "Carlos Ruiz",
    },
}

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

    # ── Pagos ─────────────────────────────────────────────────

    def obtener_pago(self, id_pago: str) -> Optional[dict]:
        return _pagos_db.get(id_pago)

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
            "urlDescarga":   f"/facturas/{id_factura}.pdf",
        }
        _facturas_db[id_factura]        = factura
        _factura_x_pago[pago["idPago"]] = id_factura
        return factura


# Singleton — nombre que espera el __init__.py
procesar_factura_repository = ProcesarFacturaRepository()