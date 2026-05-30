from app.domain.ControlPermisos.ControlPermisos_domain import ValidarAutorizacionCreate, ValidarAutorizacionResponse, ControlPermisos
from app.repository.ControlPermisos.ControlPermisos_repository import ControlPermisosRepository


class ControlPermisosService:

    def __init__(self, repo: ControlPermisosRepository):
        self.repo = repo

    def validar_autorizacion(
        self,
        datos: ValidarAutorizacionCreate,
        decodificar_token,
    ) -> ValidarAutorizacionResponse:

        # Regla de negocio: el token debe ser válido
        payload = decodificar_token(datos.token)
        if not payload:
            raise PermissionError("TOKEN_INVALIDO")

        id_usuario = payload.get("id_usuario")
        rol        = payload.get("rol")

        # Regla de negocio: el usuario debe tener perfil de permisos
        perfil = self.repo.obtener_por_usuario(id_usuario)
        if not perfil:
            raise PermissionError("TOKEN_INVALIDO")

        # Regla de negocio: verificar permiso para recurso + acción
        if not perfil.tiene_permiso(datos.recurso, datos.accion):
            raise PermissionError("AUTH_UNAUTHORIZED")

        return ValidarAutorizacionResponse(**perfil.to_response())

    def asignar_rol(self, id_usuario: int, rol: str) -> dict:
        roles_validos = {"CLIENTE", "ENTRENADOR"}
        if rol.upper() not in roles_validos:
            raise ValueError(f"Rol '{rol}' no válido. Roles permitidos: {roles_validos}")

        if self.repo.usuario_registrado(id_usuario):
            self.repo.actualizar_rol(id_usuario, rol)
        else:
            self.repo.crear(id_usuario, rol)

        return {"mensaje": f"Rol '{rol}' asignado correctamente al usuario {id_usuario}"}

    def revocar_acceso(self, id_usuario: int) -> dict:
        ok = self.repo.eliminar(id_usuario)
        if not ok:
            raise ValueError(f"No existe perfil de permisos para el usuario {id_usuario}")
        return {"mensaje": f"Acceso revocado para el usuario {id_usuario}"}

    def listar_por_rol(self, rol: str) -> list[ValidarAutorizacionResponse]:
        perfiles = self.repo.obtener_por_rol(rol)
        if not perfiles:
            raise ValueError(f"No hay usuarios con el rol '{rol}'")
        return [ValidarAutorizacionResponse(**p.to_response()) for p in perfiles]