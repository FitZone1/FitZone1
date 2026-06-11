from app.domain.Cliente.AdministrarPerfilCliente_domain import (
    PerfilClienteUpdate, ObjetivosCreate,
    PerfilClienteResponse, ObjetivosResponse
)
from app.repository.Cliente.cliente_repositories import ClienteRepository


class AdministrarPerfilClienteService:

    def __init__(self, repo: ClienteRepository):
        self.repo = repo

    def ver_perfil(self, id_usuario: int) -> PerfilClienteResponse:
        cliente = self.repo.obtener_por_id(id_usuario)
        if not cliente:
            raise ValueError("PROF_CLIENT_NOT_FOUND")
        return PerfilClienteResponse(
            idUsuario  = cliente.id,
            nombre     = cliente.nombre,
            correo     = cliente.correo,
            telefono   = cliente.telefono,
            objetivos  = "",
            pesoActual = 0.0,
        )

    def actualizar_perfil(self, id_usuario: int, datos: PerfilClienteUpdate) -> PerfilClienteResponse:
        cliente = self.repo.obtener_por_id(id_usuario)
        if not cliente:
            raise ValueError("PROF_CLIENT_NOT_FOUND")
        cliente.nombre   = datos.nombre
        cliente.telefono = datos.telefono
        return PerfilClienteResponse(
            idUsuario  = cliente.id,
            nombre     = cliente.nombre,
            correo     = cliente.correo,
            telefono   = cliente.telefono,
            objetivos  = datos.objetivos,
            pesoActual = datos.pesoActual,
        )

    def registrar_objetivos(self, id_usuario: int, datos: ObjetivosCreate) -> ObjetivosResponse:
        cliente = self.repo.obtener_por_id(id_usuario)
        if not cliente:
            raise ValueError("PROF_CLIENT_NOT_FOUND")
        return ObjetivosResponse(
            idUsuario  = cliente.id,
            objetivos  = datos.objetivos,
            pesoMeta   = datos.pesoMeta,
            plazoMeses = datos.plazoMeses,
        )