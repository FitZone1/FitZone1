from app.domain.Entrenador.GestionHorarios_domain import HorarioDisponible
from typing import Optional


class GestionHorariosRepository:

    def __init__(self):
        self._datos: list[HorarioDisponible] = []
        self._siguiente_id: int = 1
        self._seed()

    def _seed(self):
        iniciales = [
            HorarioDisponible(1, 10, ["LUNES", "MIERCOLES", "VIERNES"], "07:00", "17:00"),
            HorarioDisponible(2, 11, ["MARTES", "JUEVES"],              "08:00", "16:00"),
        ]
        self._datos = iniciales
        self._siguiente_id = 3

    def obtener_todos(self) -> list[HorarioDisponible]:
        return self._datos.copy()

    def obtener_por_entrenador(self, id_entrenador: int) -> Optional[HorarioDisponible]:
        return next((h for h in self._datos if h.id_entrenador == id_entrenador), None)

    def obtener_por_id(self, id: int) -> Optional[HorarioDisponible]:
        return next((h for h in self._datos if h.id == id), None)

    def crear(self, id_entrenador: int, dias_disponibles: list,
              hora_inicio: str, hora_fin: str) -> HorarioDisponible:
        nuevo = HorarioDisponible(
            id               = self._siguiente_id,
            id_entrenador    = id_entrenador,
            dias_disponibles = dias_disponibles,
            hora_inicio      = hora_inicio,
            hora_fin         = hora_fin,
        )
        self._datos.append(nuevo)
        self._siguiente_id += 1
        return nuevo

    def actualizar(self, id_entrenador: int, dias_disponibles: list,
                   hora_inicio: str, hora_fin: str) -> Optional[HorarioDisponible]:
        horario = self.obtener_por_entrenador(id_entrenador)
        if not horario:
            return None
        horario.dias_disponibles = dias_disponibles
        horario.hora_inicio      = hora_inicio
        horario.hora_fin         = hora_fin
        return horario

    def eliminar(self, id: int) -> bool:
        horario = self.obtener_por_id(id)
        if not horario:
            return False
        self._datos.remove(horario)
        return True


# Instancia única compartida (Singleton simple)
gestion_horarios_repository = GestionHorariosRepository()
