from app.domain.iniciosesion.iniciosesion_domain import InicioSesionCreate, InicioSesionResponse, Sesion
from app.repository.iniciosesion.iniciosesion_repositories import SesionRepository
from app.repository.Cliente.cliente_repositories import ClienteRepository
from app.repository.Entrenador.Entrenador_repository import EntrenadorRepository


class SesionService:

    def __init__(
        self,
        sesion_repo:     SesionRepository,
        cliente_repo:    ClienteRepository,
        entrenador_repo: EntrenadorRepository,
    ):
        self.sesion_repo     = sesion_repo
        self.cliente_repo    = cliente_repo
        self.entrenador_repo = entrenador_repo

    def iniciar_sesion(
        self,
        datos: InicioSesionCreate,
        verificar_contrasena,
        generar_token,
    ) -> InicioSesionResponse:

        # Buscar primero como cliente, luego como entrenador
        usuario = self.cliente_repo.obtener_por_correo(datos.correo)
        rol = "CLIENTE"

        if not usuario:
            usuario = self.entrenador_repo.obtener_por_correo(datos.correo)
            rol = "ENTRENADOR"

        # Regla de negocio: el correo debe estar registrado
        if not usuario:
            raise ValueError("Credenciales incorrectas")

        # Regla de negocio: la contraseña debe ser correcta
        if not verificar_contrasena(usuario.contrasena, datos.contrasena):
            raise ValueError("Credenciales incorrectas")

        # Regla de negocio: solo usuarios ACTIVOS pueden iniciar sesión
        if usuario.estado != "ACTIVO":
            raise ValueError("Credenciales incorrectas")

        token = generar_token(usuario.id, rol)

        sesion = Sesion(
            id_usuario = usuario.id,
            nombre     = usuario.nombre,
            rol        = rol,
            token      = token,
        )

        self.sesion_repo.guardar(sesion)
        return InicioSesionResponse(**sesion.to_response())

    def cerrar_sesion(self, token: str) -> dict:
        ok = self.sesion_repo.eliminar(token)
        if not ok:
            raise ValueError("Token inválido o sesión ya cerrada")
        return {"mensaje": "Sesión cerrada correctamente"}

    def obtener_sesion(self, token: str) -> InicioSesionResponse:
        sesion = self.sesion_repo.obtener_por_token(token)
        if not sesion:
            raise ValueError("Token inválido o expirado")
        return InicioSesionResponse(**sesion.to_response())
