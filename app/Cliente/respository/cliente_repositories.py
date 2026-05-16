from typing import Optional, List
from domain.cliente_domain import Cliente, ClienteCreate


class ClienteRepository:
    """Simulamos una base de datos con un dict."""

    def __init__(self):
        # "Base de datos" en memoria
        self._db: dict[int, Cliente] = {}
        self._next_id: int = 1

    def get_all(self) -> List[Cliente]:
        # Devuelve todos los clientes
        return list(self._db.values())

    def get_by_id(self, cliente_id: int) -> Optional[Cliente]:
        # Busca por ID. None si no existe
        return self._db.get(cliente_id)

    def create(self, data: ClienteCreate) -> Cliente:
        # Asigna ID, guarda y retorna el cliente
        cliente = Cliente(
            id=self._next_id,
            **data.model_dump()
        )
        self._db[self._next_id] = cliente
        self._next_id += 1
        return cliente

    def delete(self, cliente_id: int) -> bool:
        # True si existía y se borró
        if cliente_id in self._db:
            del self._db[cliente_id]
            return True
        return False