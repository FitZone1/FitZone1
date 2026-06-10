# ─────────────────────────────────────────────────────────────
# CAPA SERVICE — lógica de negocio
# ─────────────────────────────────────────────────────────────

from datetime import datetime

from app.domain.Pagos.ProcesarFactura_domain          import FacturaCreate, FacturaResponse, FacturaData
from app.repository.Pagos.ProcesarFactura_repository  import ProcesarFacturaRepository


class ProcesarFacturaService:

    def __init__(self, repo: ProcesarFacturaRepository):
        self.repo = repo

    def generar_factura(self, datos: FacturaCreate) -> FacturaResponse:
        """
        Genera o retorna la factura de un pago aprobado.

        Lanza ValueError:
          - "PAY_PAYMENT_NOT_FOUND" → pago no existe, no APROBADO, o idCliente incorrecto
        """
        pago = self.repo.obtener_pago(datos.idPago)

        # Regla: mismo 404 para todos los casos — no revelar info de otros clientes
        if (
            not pago
            or pago["estado"] != "APROBADO"
            or pago["idCliente"] != datos.idCliente
        ):
            raise ValueError("PAY_PAYMENT_NOT_FOUND")

        # Regla: si ya existe factura para este pago, retornarla sin duplicar
        factura_existente = self.repo.obtener_factura_por_pago(datos.idPago)
        if factura_existente:
            return self._to_response(factura_existente)

        # Crear nueva factura
        fecha   = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        factura = self.repo.guardar_factura(pago, fecha)
        return self._to_response(factura)

    def obtener_factura(self, id_factura: str) -> FacturaResponse:
        """
        Consulta una factura por su ID.

        Lanza ValueError:
          - "PAY_INVOICE_NOT_FOUND" → factura no existe
        """
        factura = self.repo.obtener_factura_por_id(id_factura)
        if not factura:
            raise ValueError("PAY_INVOICE_NOT_FOUND")

        return self._to_response(factura, message="Factura obtenida correctamente")

    # ── Privado ───────────────────────────────────────────────

    @staticmethod
    def _to_response(factura: dict, message: str = "Factura generada correctamente") -> FacturaResponse:
        return FacturaResponse(
            message = message,
            data    = FacturaData(**factura),
        )