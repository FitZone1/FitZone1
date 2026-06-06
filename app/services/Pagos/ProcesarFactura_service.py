from app.domain.Cliente.procesarfactura_domain import (
    FacturaCreate, FacturaResponse,
)
from app.repository.Pagos.ProcesarFactura_repository import ProcesarFacturaRepository


class ProcesarFacturaService:

    def __init__(self, repo: ProcesarFacturaRepository):
        self.repo = repo

    def generar_factura(self, datos: FacturaCreate) -> FacturaResponse:
        # Validar que el pago exista y pertenezca al cliente
        pago = self.repo.obtener_pago(datos.idPago, datos.idCliente)
        if not pago:
            raise ValueError("PAY_PAYMENT_NOT_FOUND")

        # REGLA DE NEGOCIO: solo pagos APROBADOS generan factura
        if not pago.esta_aprobado():
            raise ValueError("PAY_PAYMENT_NOT_FOUND")

        # REGLA DE NEGOCIO: no generar factura duplicada para el mismo pago
        existente = self.repo.factura_ya_existe(datos.idPago)
        if existente:
            return FacturaResponse(**existente.to_response())

        factura = self.repo.crear_factura(pago)
        return FacturaResponse(**factura.to_response())

    def obtener_factura(self, id_factura: str) -> FacturaResponse:
        factura = self.repo.obtener_factura(id_factura)
        if not factura:
            raise ValueError("PAY_INVOICE_NOT_FOUND")
        return FacturaResponse(**factura.to_response())