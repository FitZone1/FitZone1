from app.domain.cliente_domain import RegistroClienteCreate, RegistroClienteResponse
from app.respository.cliente_repositories import ClienteRepository


class ClienteService:

    def __init__(self, repo: ClienteRepository):
        self.repo = repo

    def listar(self) -> list[RegistroClienteResponse]:
        return [RegistroClienteResponse(**c.to_response())
                for c in self.repo.obtener_todos()]

    def obtener(self, id: int) -> RegistroClienteResponse:
        c = self.repo.obtener_por_id(id)
        if not c:
            raise ValueError(f"Cliente con id {id} no encontrado")
        return RegistroClienteResponse(**c.to_response())

    def registrar(self, datos: RegistroClienteCreate, contrasena_hash: str) -> RegistroClienteResponse:
        # Regla de negocio: el correo no puede estar ya registrado
        if self.repo.correo_existe(datos.correo):
            raise ValueError("El correo ya está registrado")
        c = self.repo.crear(
            nombre     = datos.nombre,
            correo     = datos.correo,
            telefono   = datos.telefono,
            contrasena = contrasena_hash,
        )
        return RegistroClienteResponse(**c.to_response())

    def cambiar_estado(self, id: int, estado: str) -> RegistroClienteResponse:
        # Regla de negocio: solo se permiten estados válidos
        estados_validos = {"ACTIVO", "INACTIVO", "PENDIENTE"}
        if estado.upper() not in estados_validos:
            raise ValueError(f"Estado '{estado}' no válido. Use: ACTIVO, INACTIVO o PENDIENTE")
        c = self.repo.obtener_por_id(id)
        if not c:
            raise ValueError(f"Cliente con id {id} no encontrado")
        self.repo.actualizar_estado(id, estado.upper())
        c.estado = estado.upper()
        return RegistroClienteResponse(**c.to_response())

    def eliminar(self, id: int) -> dict:
        ok = self.repo.eliminar(id)
        if not ok:
            raise ValueError(f"Cliente {id} no existe")
        return {"mensaje": f"Cliente {id} eliminado correctamente"}

    def por_estado(self, estado: str) -> list[RegistroClienteResponse]:
        clientes = self.repo.obtener_por_estado(estado)
        if not clientes:
            raise ValueError(f"No hay clientes con estado '{estado}'")
        return [RegistroClienteResponse(**c.to_response()) for c in clientes]