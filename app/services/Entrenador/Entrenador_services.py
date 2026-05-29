from domain.Entrenador.Entrenador_domain import RegistroEntrenadorCreate, RegistroEntrenadorResponse
from repository.Entrenador.Entrenador_repository import EntrenadorRepository


class EntrenadorService:

    def __init__(self, repo: EntrenadorRepository):
        # Inyección dee dependencia: recibe el repositorio desde afuera
        self.repo = repo

    def listar(self) -> list[RegistroEntrenadorResponse]:
        return [RegistroEntrenadorResponse(**e.to_response())
                for e in self.repo.obtener_todos()]

    def listar_activos(self) -> list[RegistroEntrenadorResponse]:
        # Regla de negocio: solo entrenadores ACTIVOS son visibles para los clientes
        entrenadores = self.repo.obtener_activos()
        if not entrenadores:
            raise ValueError("No hay entrenadores activos disponibles")
        return [RegistroEntrenadorResponse(**e.to_response()) for e in entrenadores]

    def obtener(self, id: int) -> RegistroEntrenadorResponse:
        e = self.repo.obtener_por_id(id)
        if not e:
            raise ValueError(f"Entrenador con id {id} no encontrado")
        return RegistroEntrenadorResponse(**e.to_response())

    def registrar(self, datos: RegistroEntrenadorCreate, contrasena: str) -> RegistroEntrenadorResponse:
        # Regla de negocio: el correo no puede estar ya registrado
        if self.repo.correo_existe(datos.correo):
            raise ValueError("El correo ya está registrado")

        e = self.repo.crear(
            nombre          = datos.nombre,
            correo          = datos.correo,
            contrasena = contrasena,
            especialidad    = datos.especialidad,
            gimnasio_id     = datos.gimnasioId,
        )
        return RegistroEntrenadorResponse(**e.to_response())

    def actualizar(self, id: int, datos: RegistroEntrenadorCreate) -> RegistroEntrenadorResponse:
        e = self.repo.actualizar(
            id           = id,
            nombre       = datos.nombre,
            especialidad = datos.especialidad,
            gimnasio_id  = datos.gimnasioId,
        )
        if not e:
            raise ValueError(f"Entrenador {id} no existe")
        return RegistroEntrenadorResponse(**e.to_response())

    def eliminar(self, id: int) -> dict:
        ok = self.repo.eliminar(id)
        if not ok:
            raise ValueError(f"Entrenador {id} no existe")
        return {"mensaje": f"Entrenador {id} eliminado correctamente"}

    def por_gimnasio(self, gimnasio_id: int) -> list[RegistroEntrenadorResponse]:
        entrenadores = self.repo.obtener_por_gimnasio(gimnasio_id)
        if not entrenadores:
            raise ValueError(f"No hay entrenadores registrados en el gimnasio {gimnasio_id}")
        return [RegistroEntrenadorResponse(**e.to_response()) for e in entrenadores]