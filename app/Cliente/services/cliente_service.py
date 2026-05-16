from typing import List
from fastapi import HTTPException, status

from domain.cliente_domain import Cliente, ClienteCreate
from repositories.cliente_repositories import ClienteRepository


class ProductService:

    def __init__(self, repo: ProductRepository):
        # Recibe el repositorio por inyección de dependencias
        self.repo = repo

    def get_all_products(self) -> List[Product]:
        return self.repo.get_all()

    def get_product(self, product_id: int) -> Product:
        product = self.repo.get_by_id(product_id)

        # ⬇ Regla de negocio: si no existe, lanza error 404
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto {product_id} no encontrado"
            )
        return product

    def create_product(self, data: ProductCreate) -> Product:
        # ⬇ Regla de negocio: precio no puede ser negativo
        if data.price < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El precio no puede ser negativo"
            )
        return self.repo.create(data)

    def delete_product(self, product_id: int) -> dict:
        deleted = self.repo.delete(product_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto {product_id} no encontrado"
            )
        return {"message": "Producto eliminado correctamente"}