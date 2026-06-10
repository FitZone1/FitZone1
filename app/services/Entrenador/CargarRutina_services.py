# ─────────────────────────────────────────────────────────────
# CAPA SERVICE — lógica de negocio
# ─────────────────────────────────────────────────────────────

from app.domain.Entrenador.CargarRutina_domain import RutinaCreate, RutinaResponse, RutinaData
from app.repository.Entrenador.CargarRutina_repository import RutinaRepository


class RutinaService:

    def __init__(self, rutina_repo: RutinaRepository):
        self.rutina_repo = rutina_repo

    def cargar_rutina(self, id_entrenador: int, datos: RutinaCreate) -> RutinaResponse:
        """
        Crea una nueva rutina para el entrenador autenticado.
        id_entrenador viene del token de sesión, no del body.

        Lanza:
          - ValueError("RUT_EMPTY_EXERCISES")  → lista de ejercicios vacía
          - ValueError("RUT_DUPLICATE_NAME")   → nombre ya existe para ese entrenador
        """

        # Regla de negocio: la rutina debe tener al menos un ejercicio
        if not datos.ejercicios:
            raise ValueError("RUT_EMPTY_EXERCISES")

        # Regla de negocio: nombre único por entrenador
        if self.rutina_repo.existe_nombre(id_entrenador, datos.nombre):
            raise ValueError("RUT_DUPLICATE_NAME")

        registro = self.rutina_repo.guardar(
            id_entrenador=id_entrenador,
            nombre=datos.nombre,
            ejercicios=datos.ejercicios,
        )

        return RutinaResponse(
            data=RutinaData(
                idRutina        = registro["idRutina"],
                nombre          = registro["nombre"],
                totalEjercicios = len(registro["ejercicios"]),
            )
        )

    def obtener_rutina(self, id_rutina: int, id_entrenador: int) -> dict:
        rutina = self.rutina_repo.obtener_por_id(id_rutina)

        if not rutina:
            raise ValueError("RUT_NOT_FOUND")

        if rutina["idEntrenador"] != id_entrenador:
            raise PermissionError("AUTH_UNAUTHORIZED")

        return rutina

    def listar_rutinas(self, id_entrenador: int) -> list[dict]:
        return self.rutina_repo.listar_por_entrenador(id_entrenador)