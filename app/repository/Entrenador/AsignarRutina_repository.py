# ─────────────────────────────────────────────────────────────
# CAPA REPOSITORY — acceso a datos
# Solo se comunica con la fuente de datos.
# Aquí NO hay lógica de negocio.
# ─────────────────────────────────────────────────────────────

from typing import Optional


# ── Simulación de BD en memoria ───────────────────────────────
# Estructura: { (idEntrenador, diaSemana): { idRutina, nombre, diaSemana } }
_asignaciones_db: dict = {}


class AsignarRutinaRepository:

    def obtener_asignacion(self, id_entrenador: int, dia_semana: str) -> Optional[dict]:
        """Retorna la asignación existente para ese entrenador y día, o None."""
        return _asignaciones_db.get((id_entrenador, dia_semana))

    def guardar_asignacion(self, id_entrenador: int, id_rutina: int,
                           nombre: str, dia_semana: str) -> dict:
        """
        Guarda o reemplaza la asignación de rutina para el día indicado.
        Si ya existía una rutina para ese día, la sobreescribe (reasignación).
        """
        registro = {
            "idRutina":  id_rutina,
            "nombre":    nombre,
            "diaSemana": dia_semana,
        }
        _asignaciones_db[(id_entrenador, dia_semana)] = registro
        return registro

    def listar_por_entrenador(self, id_entrenador: int) -> list[dict]:
        """Retorna todas las asignaciones del entrenador."""
        return [
            v for (eid, _), v in _asignaciones_db.items()
            if eid == id_entrenador
        ]

    def listar_por_dia(self, dia_semana: str) -> list[dict]:
        """Retorna todas las rutinas asignadas a un día (visible para clientes)."""
        return [
            v for (_, dia), v in _asignaciones_db.items()
            if dia == dia_semana
        ]


# Instancia compartida (singleton)
asignar_rutina_repository = AsignarRutinaRepository()