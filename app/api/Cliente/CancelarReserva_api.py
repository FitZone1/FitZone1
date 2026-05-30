from fastapi import APIRouter, HTTPException, status
from app.domain.Cliente.CancelarReserva_domain import CancelarReservaCreate, CancelarReservaResponse
from app.repository.Cliente.CancelarReserva_repository import cancelar_reserva_repository
from app.services.Cliente.CancelarReserva_services import CancelarReservaService

router = APIRouter(
    prefix="/api/reservas",
    tags=["Cancelar Reserva"],
)

service = CancelarReservaService(repo=cancelar_reserva_repository)


# ── DELETE /api/reservas/{idReserva} ──────────────────────────
@router.delete("/{idReserva}", response_model=CancelarReservaResponse)
def cancelar_reserva(idReserva: int, datos: CancelarReservaCreate):
    """Cancela una reserva existente. Solo aplica a reservas en estado CONFIRMADA."""
    try:
        return service.cancelar(idReserva, datos)
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
