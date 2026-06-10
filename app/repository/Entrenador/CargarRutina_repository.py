# ─────────────────────────────────────────────────────────────
# CAPA REPOSITORY — acceso a datos
# Solo se comunica con la fuente de datos.
# Aquí NO hay lógica de negocio.
# ─────────────────────────────────────────────────────────────

from typing import List, Optional
from app.domain.Entrenador.CargarRutina_domain import EjercicioCreate


# ── Simulación de BD en memoria ───────────────────────────────
# En producción reemplazar por SQLAlchemy / asyncpg / etc.

_rutinas_db: dict = {}
_sequence_id: int = 0


def _next_id() -> int:
    global _sequence_id
    _sequence_id += 1
    return _sequence_id


# ── Repositorio ───────────────────────────────────────────────

class RutinaRepository:

    def guardar(
        self,
        id_entrenador: int,
        nombre:        str,
        ejercicios:    List[EjercicioCreate],
    ) -> dict:
        """Persiste la rutina y retorna el registro con su ID generado."""
        id_rutina = _next_id()
        registro = {
            "idRutina":      id_rutina,
            "idEntrenador":  id_entrenador,
            "nombre":        nombre,
            "ejercicios":    [e.model_dump() for e in ejercicios],
        }
        _rutinas_db[id_rutina] = registro
        return registro

    def obtener_por_id(self, id_rutina: int) -> Optional[dict]:
        """Retorna la rutina o None si no existe."""
        return _rutinas_db.get(id_rutina)

    def listar_por_entrenador(self, id_entrenador: int) -> List[dict]:
        """Retorna todas las rutinas de un entrenador."""
        return [r for r in _rutinas_db.values() if r["idEntrenador"] == id_entrenador]

    def existe_nombre(self, id_entrenador: int, nombre: str) -> bool:
        """Verifica si el entrenador ya tiene una rutina con ese nombre."""
        return any(
            r["idEntrenador"] == id_entrenador and r["nombre"] == nombre
            for r in _rutinas_db.values()
        )


# Instancia compartida (singleton)
rutina_repository = RutinaRepository()