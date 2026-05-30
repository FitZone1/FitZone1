from app.domain.Entrenador.Entrenador_domain import RegistroEntrenadorCreate, RegistroEntrenadorResponse
from app.repository.Entrenador.Entrenador_repository import EntrenadorRepository


class EntrenadorService:

    def __init__(self, repo: EntrenadorRepository):
        self.repo = repo

    def listar(self) -> list[RegistroEntrenadorResponse]:
        return [RegistroEntrenadorResponse(**e.to_response())
                for e in self.repo.obtener_todos()]

    def listar_activos(self) -> list[RegistroEntrenadorResponse]:
        entrenadores = self.repo.obtener_activos()
        if not entrenadores:
            raise ValueError("No hay entrenadores activos disponibles")
        return [RegistroEntrenadorResponse(**e.to_response()) for e in entrenadores]

    def obtener(self, id: int) -> RegistroEntrenadorResponse:
        e = self.repo.obtener_por_id(id)
        if not e:
            raise ValueError(f"Entrenador con id {id} no encontrado")
        return RegistroEntrenadorResponse(**e.to_response())

    def registrar(self, datos: RegistroEntrenadorCreate, contrasena_hash: str) -> RegistroEntrenadorResponse:
        if self.repo.correo_existe(datos.correo):
            raise ValueError("El correo ya está registrado")
        e = self.repo.crear(
            nombre       = datos.nombre,
            correo       = datos.correo,
            contrasena   = contrasena_hash,
            especialidad = datos.especialidad,
            gimnasio_id  = datos.gimnasioId,
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

    def cambiar_estado(self, id: int, estado: str) -> RegistroEntrenadorResponse:
        estados_validos = {"ACTIVO", "INACTIVO"}
        if estado.upper() not in estados_validos:
            raise ValueError(f"Estado '{estado}' no válido. Use: ACTIVO o INACTIVO")
        e = self.repo.obtener_por_id(id)
        if not e:
            raise ValueError(f"Entrenador con id {id} no encontrado")
        self.repo.actualizar_estado(id, estado.upper())
        e.estado = estado.upper()
        return RegistroEntrenadorResponse(**e.to_response())

    def eliminar(self, id: int) -> dict:
        ok = self.repo.eliminar(id)
        if not ok:
            raise ValueError(f"Entrenador {id} no existe")
        return {"mensaje": f"Entrenador {id} eliminado correctamente"}

    def por_gimnasio(self, gimnasio_id: int) -> list[RegistroEntrenadorResponse]:
        entrenadores = self.repo.obtener_por_gimnasio(gimnasio_id)
        if not entrenadores:
            raise ValueError(f"No hay entrenadores en el gimnasio {gimnasio_id}")
        return [RegistroEntrenadorResponse(**e.to_response()) for e in entrenadores]