from typing import List
from fastapi import HTTPException, status

from domain.cliente_domain import Cliente, ClienteCreate
from respository.cliente_repositories import ClienteRepository


class ClienteService:

    def __init__(self, repo: ClienteRepository):
        # Recibe el repositorio por inyección de dependencias
        self.repo = repo

    def get_all_clientes(self) -> List[Cliente]:
        return self.repo.get_all()

    def get_cliente(self, cliente_id: int) -> Cliente:
        cliente = self.repo.get_by_id(cliente_id)

        # ⬇ Regla de negocio: si no existe, lanza error 404
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente {cliente_id} no encontrado"
            )
        return cliente

    def create_Cliente(self, data: ClienteCreate) -> Cliente:
        # ⬇ Regla de negocio: cliente no puede tener el correo vacio
        if data.correo < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El cliente no puede tener un correo electrónico vacío"
            )
        return self.repo.create(data)

    def delete_cliente(self, cliente_id: int) -> dict:
        deleted = self.repo.delete(cliente_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente {cliente_id} no encontrado"
            )
        return {"message": "Cliente eliminado correctamente"}