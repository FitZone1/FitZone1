from typing import List
from fastapi import APIRouter, status

from domain.cliente_domain import Cliente, ClienteCreate
from services.cliente_service import ClienteService
from respository.cliente_repositories import ClienteRepository


# Instancias (en producción usarías DI de FastAPI)
repo = ClienteRepository()
service = ClienteService(repo)

# Router: agrupa endpoints bajo un prefijo
router = APIRouter(prefix="/cliente", tags=["cliente"])


@router.get("/", response_model=List[Cliente])
def list_cliente():
    """Devuelve todos los clientes."""
    return service.get_all_cliente()


@router.get("/{cliente_id}", response_model=Cliente)
def get_cliente(cliente_id: int):
    """Devuelve un producto por su ID."""
    return service.get_product(cliente_id)


@router.post(
    "/",
    response_model=Cliente,
    status_code=status.HTTP_201_CREATED
)
def create_cliente(data: ClienteCreate):
    """Crea un nuevo cliente."""
    return service.create_cliente(data)


@router.delete(
    "/{cliente_id}",
    status_code=status.HTTP_200_OK
)
def delete_cliente(cliente_id: int):
    """Elimina un cliente por su ID."""
    return service.delete_product(cliente_id)