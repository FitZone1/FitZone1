# ─────────────────────────────────────────────────────────────
# CAPA REPOSITORIO — única responsabilidad: guardar y recuperar
# Solo manipula datos. Sin lógica de negocio aquí.
# ─────────────────────────────────────────────────────────────

from app.domain.iniciosesion import Sesion
from typing import Optional


class SesionRepository:

    def __init__(self):
        # Almacén en memoria: tokens activos { token: Sesion }
        self._sesiones_activas: dict[str, Sesion] = {}

    # ── Operaciones sobre sesiones ────────────────────────────

    def guardar(self, sesion: Sesion) -> Sesion:
        """Registra una sesión activa indexada por token."""
        self._sesiones_activas[sesion.token] = sesion
        return sesion

    def obtener_por_token(self, token: str) -> Optional[Sesion]:
        """Devuelve la sesión asociada al token, o None si no existe."""
        return self._sesiones_activas.get(token)

    def obtener_por_usuario(self, id_usuario: int) -> Optional[Sesion]:
        """Devuelve la sesión activa de un usuario, o None si no tiene."""
        return next(
            (s for s in self._sesiones_activas.values()
             if s.id_usuario == id_usuario),
            None,
        )

    def eliminar(self, token: str) -> bool:
        """Invalida (cierra) la sesión asociada al token."""
        if token not in self._sesiones_activas:
            return False
        del self._sesiones_activas[token]
        return True

    def token_existe(self, token: str) -> bool:
        return token in self._sesiones_activas

    def obtener_todas(self) -> list[Sesion]:
        return list(self._sesiones_activas.values())


# Instancia única compartida (Singleton simple)
sesion_repository = SesionRepository()