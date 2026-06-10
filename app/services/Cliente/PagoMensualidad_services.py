from app.domain.Cliente.PagoMensualidad_domain import (
    PagoMensualidadCreate,
    PagoMensualidadResponse,
    MetodoPagoResponse,
    MetodoPago,
    METODOS_CON_TARJETA,
)
from app.repository.Cliente.PagoMensualidad_repository import PagoMensualidadRepository
from app.repository.Cliente.procesarplanes_repository import ProcesarPlanesRepository
from datetime import datetime
import random


class PagoMensualidadService:

    def __init__(self, repo: PagoMensualidadRepository,
                 planes_repo: ProcesarPlanesRepository):
        self.repo        = repo
        self.planes_repo = planes_repo

    # ── GET /api/pagos/metodos ────────────────────────────────
    def listar_metodos(self) -> list[MetodoPagoResponse]:
        return [MetodoPagoResponse(**m) for m in MetodoPago.listar()]

    # ── POST /api/pagos ───────────────────────────────────────
    def procesar_pago(self, datos: PagoMensualidadCreate,
                      pasarela_pago) -> PagoMensualidadResponse:

        # Regla de negocio: el plan debe existir y estar activo
        plan = self.planes_repo.obtener_plan_por_id(datos.idPlan)
        if not plan:
            raise ValueError("PAY_PLAN_NOT_FOUND")

        fecha   = datetime.now().isoformat()
        id_pago = f"PAY-{random.randint(100000, 999999)}"
        monto   = plan.monto

        # Regla de negocio: llamar a la pasarela solo si el método la requiere.
        # Para EFECTIVO no se invoca pasarela con tarjeta; se aprueba directamente.
        if datos.metodoPago in METODOS_CON_TARJETA:
            estado = pasarela_pago(datos.numeroTarjeta, monto)
        else:
            # EFECTIVO: aprobación directa (el cajero confirma el pago presencial)
            estado = "APROBADO"

        # Regla de negocio: solo se registra si la pasarela devuelve APROBADO
        if estado != "APROBADO":
            raise PermissionError("PAY_PAYMENT_DECLINED")

        pago = self.repo.crear(
            id_pago        = id_pago,
            id_cliente     = datos.idCliente,
            id_plan        = datos.idPlan,
            monto          = monto,
            estado         = estado,
            fecha          = fecha,
            metodo_pago    = datos.metodoPago,
            numero_tarjeta = datos.numeroTarjeta,
        )
        return PagoMensualidadResponse(**pago.to_response())

    def obtener(self, id_pago: str) -> PagoMensualidadResponse:
        pago = self.repo.obtener_por_id(id_pago)
        if not pago:
            raise ValueError(f"Pago {id_pago} no encontrado")
        return PagoMensualidadResponse(**pago.to_response())

    def listar_por_cliente(self, id_cliente: int) -> list[PagoMensualidadResponse]:
        pagos = self.repo.obtener_por_cliente(id_cliente)
        if not pagos:
            raise ValueError(f"No hay pagos registrados para el cliente {id_cliente}")
        return [PagoMensualidadResponse(**p.to_response()) for p in pagos]