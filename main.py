# ─────────────────────────────────────────────────────────────
# PUNTO DE ENTRADA — crea la app FastAPI y registra los routers
# ─────────────────────────────────────────────────────────────

from fastapi import FastAPI
from app.api.Cliente.cliente_api import router as cliente_router
from app.api.Entrenador.Entrenador_api import router as entrenador_router
from app.api.iniciosesion.iniciosesion_api import router as iniciosesion_router
from app.api.ControlPermisos.ControlPermisos_api import router as control_permisos_router

# Crear la aplicación con metadata para la documentación
app = FastAPI(
    title="FitZone API",
    description="API REST con arquitectura de capas — FastAPI",
    version="1.0.0",
)

# Registrar el router de cliente
app.include_router(cliente_router)
app.include_router(entrenador_router)
app.include_router(iniciosesion_router)
app.include_router(control_permisos_router)


## Ruta raíz — bienvenida
@app.get("/", tags=["Root"])
def root():
    return {
        "mensaje": "API FitZone corriendo correctamente 🚀",
        "docs":    "http://127.0.0.1:8000/docs",
        "version": "1.0.0",
    }


# ── Para correr directamente con: python main.py ─────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)