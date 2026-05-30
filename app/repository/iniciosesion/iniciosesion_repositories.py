from app.domain.iniciosesion.iniciosesion_domain import Sesion
from typing import Optional


class SesionRepository:

    def __init__(self):
        # Almacén en memoria: { token: Sesion }
        self._sesiones_activas: dict[str, Sesion] = {}

    def guardar(self, sesion: Sesion) -> Sesion:
        """Registra una sesión activa indexada por token."""
        self._sesiones_activas[sesion.token] = sesion
        return sesion

    def obtener_por_token(self, token: str) -> Optional[Sesion]:
        """Devuelve la sesión asociada al token, o None si no existe."""
        return self._sesiones_activas.get(token)

    def obtener_por_usuario(self, id_usuario: int) -> Optional[Sesion]:
        """Devuelve la sesión activa de un usuario."""
        return next(
            (s for s in self._sesiones_activas.values()
             if s.id_usuario == id_usuario),
            None,
        )

    def eliminar(self, token: str) -> bool:
        """Invalida la sesión asociada al token."""
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
