from app.domain.Cliente.AdministrarPerfilCliente_domain import (
    PerfilClienteUpdate, ObjetivosCreate,
    PerfilClienteResponse, ObjetivosResponse
)
from app.repository.Cliente.AdministrarPerfilCliente_repository import AdministrarPerfilClienteRepository


class AdministrarPerfilClienteService:

    def __init__(self, repo: AdministrarPerfilClienteRepository):
        self.repo = repo

    def ver_perfil(self, id_cliente: int) -> PerfilClienteResponse:
        perfil = self.repo.obtener_por_id(id_cliente)
        if not perfil:
            raise ValueError("PROF_CLIENT_NOT_FOUND")
        return PerfilClienteResponse(**perfil.to_response())

    def actualizar_perfil(self, id_cliente: int, datos: PerfilClienteUpdate) -> PerfilClienteResponse:
        perfil = self.repo.actualizar(
            id_cliente  = id_cliente,
            nombre      = datos.nombre,
            telefono    = datos.telefono,
            objetivos   = datos.objetivos,
            peso_actual = datos.pesoActual,
        )
        if not perfil:
            raise ValueError("PROF_CLIENT_NOT_FOUND")
        return PerfilClienteResponse(**perfil.to_response())

    def registrar_objetivos(self, id_cliente: int, datos: ObjetivosCreate) -> ObjetivosResponse:
        perfil = self.repo.registrar_objetivos(
            id_cliente  = id_cliente,
            objetivos   = datos.objetivos,
            peso_meta   = datos.pesoMeta,
            plazo_meses = datos.plazoMeses,
        )
        if not perfil:
            raise ValueError("PROF_CLIENT_NOT_FOUND")
        return ObjetivosResponse(**perfil.to_objetivos_response())
