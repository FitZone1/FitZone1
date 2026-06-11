# ─────────────────────────────────────────────────────────────
# CAPA SERVICE — lógica de negocio
# ─────────────────────────────────────────────────────────────

from app.domain.Entrenador.AsignarRutina_domain import (
    AsignarRutinaCreate,
    AsignarRutinaResponse,
    AsignarRutinaData,
)
from app.repository.Entrenador.AsignarRutina_repository import AsignarRutinaRepository
from app.repository.Entrenador.CargarRutina_repository import RutinaRepository


class AsignarRutinaService:

    def __init__(self, asignar_repo: AsignarRutinaRepository,
                 rutina_repo: RutinaRepository):
        self.asignar_repo = asignar_repo
        self.rutina_repo  = rutina_repo

    def asignar_rutina(self, id_entrenador_token: int,
                       datos: AsignarRutinaCreate) -> AsignarRutinaResponse:
        """
        Asigna una rutina a un día de la semana.

        Reglas de negocio:
          1. La rutina debe existir                         → RUT_NOT_FOUND (404)
          2. La rutina debe pertenecer al entrenador        → RUT_UNAUTHORIZED_EDIT (403)
          3. Si el día ya tiene rutina asignada, se reemplaza (reasignación permitida)

        Lanza:
          - ValueError("RUT_NOT_FOUND")          → rutina inexistente
          - PermissionError("RUT_UNAUTHORIZED_EDIT") → rutina de otro entrenador
        """

        # Regla 1: la rutina debe existir
        rutina = self.rutina_repo.obtener_por_id(datos.idRutina)
        if not rutina:
            raise ValueError("RUT_NOT_FOUND")

        # Regla 2: la rutina debe pertenecer al entrenador autenticado
        if rutina["idEntrenador"] != id_entrenador_token:
            raise PermissionError("RUT_UNAUTHORIZED_EDIT")

        # Regla 3: guardar (o reemplazar) la asignación para ese día
        registro = self.asignar_repo.guardar_asignacion(
            id_entrenador = id_entrenador_token,
            id_rutina     = rutina["idRutina"],
            nombre        = rutina["nombre"],
            dia_semana    = datos.diaSemana,
        )

        return AsignarRutinaResponse(
            data=AsignarRutinaData(
                idRutina  = registro["idRutina"],
                nombre    = registro["nombre"],
                diaSemana = registro["diaSemana"],
            )
        )