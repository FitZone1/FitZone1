# ─────────────────────────────────────────────────────────────
# PUNTO DE ENTRADA — crea la app FastAPI y registra los routers
# ─────────────────────────────────────────────────────────────

from fastapi import FastAPI
from app.api.Cliente.cliente_api import router as cliente_router
from app.api.Entrenador.Entrenador_api import router as entrenador_router
from app.api.iniciosesion.iniciosesion_api import router as iniciosesion_router
from app.api.Entrenador.EntrenadoresDisponibles_api import router as entrenadores_disponibles_router
from app.api.Cliente.ReservaSesion_api import router as reserva_sesion_router
from app.api.Cliente.CancelarReserva_api import router as cancelar_reserva_router
from app.api.Entrenador.GestionHorarios_api import router as gestion_horarios_router
from app.api.ControlPermisos.ControlPermisos_api import router as control_permisos_router
from app.api.Cliente.PagoMensualidad_api import router as pagos_mesualidad_router
from app.api.Cliente.PagoMensualidad_api import router as pagar_mensualidad_router
from app.api.ControlPermisos.ControlPermisos_api import router as control_permisos_router
from app.api.ControlPermisos.ControlPermisos_api import router as control_permisos_router   
from app.api.Cliente.PagoMensualidad_api import router as pago_mensualidad_router
from app.api.Cliente.procesarplanes_api import router as procesar_planes_router



# Crear la aplicación con metadata para la documentación
app = FastAPI(
    title="FitZone API",
    description="API REST con arquitectura de capas — FastAPI",
    version="1.0.0",
)

# Registrar los routers
app.include_router(cliente_router)
app.include_router(entrenador_router)
app.include_router(iniciosesion_router)
app.include_router(entrenadores_disponibles_router)
app.include_router(reserva_sesion_router)
app.include_router(cancelar_reserva_router)
app.include_router(gestion_horarios_router)
app.include_router(control_permisos_router)
app.include_router(pagos_mesualidad_router)
app.include_router(pagar_mensualidad_router)
app.include_router(pago_mensualidad_router)
app.include_router(procesar_planes_router)

# Ruta raíz — bienvenida
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