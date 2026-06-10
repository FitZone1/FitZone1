## [HU-06] Reservar sesión de entrenamiento

### 📖 Historia de usuario

**Como** Cliente del gimnasio
**Quiero** Reservar una sesión de entrenamiento con un entrenador disponible, consultar mis reservas activas y conocer la disponibilidad real del entrenador
**Para** Asegurar mi espacio con el entrenador elegido, planificar mi rutina semanal y evitar intentar reservar en horarios ya llenos

## 🔁 Flujo esperado

- El cliente consulta la capacidad del entrenador para el día deseado — el endpoint le informa la capacidad máxima, reservas actuales y lugares disponibles.
- El cliente selecciona un horario disponible del entrenador.
- El sistema consume el endpoint `POST /api/reservas` con idCliente, idEntrenador, fecha e idZona.
- El backend valida que el horario esté disponible y no haya conflictos.
- Se crea la reserva con estado CONFIRMADA y se retorna el idReserva generado.
- El cliente puede listar sus reservas por idCliente o consultar una reserva específica por ID.

## Criterios de aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone `POST /api/reservas` que recibe idCliente, idEntrenador, fecha e idZona.
- [ ] Se expone `GET /api/reservas?idCliente={id}` para listar todas las reservas de un cliente.
- [ ] Se expone `GET /api/reservas/{idReserva}` para obtener el detalle de una reserva por ID.
- [ ] Se expone `GET /api/reservas/capacidad?idEntrenador={id}&fecha={fecha}` para consultar la ocupación del entrenador en una fecha dada, incluyendo la capacidad máxima configurada en el sistema.
- [ ] Un cliente no puede tener dos reservas activas en el mismo horario exacto.
- [ ] El entrenador no puede tener dos sesiones en el mismo horario exacto.
- [ ] El entrenador tiene una capacidad máxima de reservas por día definida en el sistema y expuesta en el endpoint de capacidad.

### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura al crear una reserva:

```json
{
  "success": true,
  "message": "Reserva creada correctamente",
  "data": {
    "idReserva": 87,
    "estado": "CONFIRMADA",
    "fecha": "2026-03-20T15:00:00",
    "idEntrenador": 10,
    "idCliente": 42
  }
}
```

- [ ] Se responde con la siguiente estructura al listar reservas del cliente:

```json
{
  "success": true,
  "message": "Reservas obtenidas correctamente",
  "data": [
    {
      "idReserva": 87,
      "estado": "CONFIRMADA",
      "fecha": "2026-03-20T15:00:00",
      "idEntrenador": 10,
      "idCliente": 42
    }
  ]
}
```

- [ ] Se responde con la siguiente estructura al obtener una reserva por ID:

```json
{
  "success": true,
  "message": "Reserva obtenida correctamente",
  "data": {
    "idReserva": 87,
    "estado": "CONFIRMADA",
    "fecha": "2026-03-20T15:00:00",
    "idEntrenador": 10,
    "idCliente": 42
  }
}
```

- [ ] Se responde con la siguiente estructura al consultar capacidad del entrenador:

```json
{
  "success": true,
  "message": "Capacidad consultada correctamente",
  "data": {
    "idEntrenador": 10,
    "fecha": "2026-03-20",
    "capacidadMaxima": 8,
    "reservasActuales": 5,
    "lugaresDisponibles": 3
  }
}
```

- [ ] Si el horario ya está ocupado, el backend retorna:

```json
{
  "success": false,
  "statusCode": 409,
  "message": "Horario no disponible",
  "error": {
    "error_code": "RES_SCHEDULE_CONFLICT",
    "details": "El entrenador ya tiene una sesión asignada en ese horario",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

- [ ] Si el entrenador alcanzó la capacidad máxima, el backend retorna:

```json
{
  "success": false,
  "statusCode": 409,
  "message": "Capacidad máxima alcanzada",
  "error": {
    "error_code": "RES_MAX_CAPACITY_REACHED",
    "details": "El entrenador ya alcanzó el máximo de clientes para ese día",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

- [ ] Si no se encuentran reservas para el cliente, el backend retorna:

```json
{
  "success": false,
  "statusCode": 404,
  "message": "Sin reservas",
  "error": {
    "error_code": "RES_NOT_FOUND",
    "details": "No se encontraron reservas para el cliente especificado",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

- [ ] Si la reserva buscada por ID no existe, el backend retorna:

```json
{
  "success": false,
  "statusCode": 404,
  "message": "Reserva no encontrada",
  "error": {
    "error_code": "RES_ID_NOT_FOUND",
    "details": "No existe una reserva con el ID proporcionado",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

## 🔧 Notas Técnicas

- `POST   /api/reservas`                                           → Crear reserva
- `GET    /api/reservas?idCliente={id}`                            → Listar reservas por cliente
- `GET    /api/reservas/{idReserva}`                               → Obtener reserva por ID
- `GET    /api/reservas/capacidad?idEntrenador={id}&fecha={fecha}` → Consultar capacidad del entrenador

## 🧪 Requisitos de prueba

### Casos de prueba funcional

### ✅ Caso 1: Reserva exitosa

- **Precondición:** El horario está disponible para el entrenador y el cliente no tiene otra reserva en ese mismo horario.
- **Acción:** `POST /api/reservas` con idCliente=99, idEntrenador=1, fecha="2026-06-10T09:00:00", idZona=1.
- **Resultado esperado:**
  - HTTP 201 Created
  - Campo `success: true`
  - Estado de la reserva: `CONFIRMADA`
  - `idReserva` generado automáticamente

### ✅ Caso 3: Obtener reserva por ID

- **Precondición:** Existe la reserva con idReserva=1 (incluida en el seed inicial).
- **Acción:** `GET /api/reservas/1`
- **Resultado esperado:**
  - HTTP 200 OK
  - Detalle completo de la reserva


### ❌ Caso 6: Horario no disponible para el entrenador

- **Precondición:** Ejecutar primero el Caso 1 para que el entrenador tenga una reserva confirmada el 2026-06-10T09:00:00.
- **Acción:** `POST /api/reservas` con idCliente=100, idEntrenador=1, fecha="2026-06-10T09:00:00", idZona=2.
- **Resultado esperado:**
  - HTTP 409 Conflict
  - `error_code`: `RES_SCHEDULE_CONFLICT`
  - `message`: `"Horario no disponible"`

### ❌ Caso 7: Conflicto de horario para el cliente

- **Precondición:** El cliente con idCliente=42 tiene una reserva confirmada el 2026-03-20T15:00:00 (seed inicial).
- **Acción:** `POST /api/reservas` con idCliente=42, idEntrenador=2, fecha="2026-03-20T15:00:00", idZona=1.
- **Resultado esperado:**
  - HTTP 409 Conflict
  - `error_code`: `RES_SCHEDULE_CONFLICT`
  - `message`: `"Horario no disponible"`

### ❌ Caso 10: Reserva no encontrada por ID

- **Precondición:** No existe ninguna reserva con idReserva=9999.
- **Acción:** `GET /api/reservas/9999`
- **Resultado esperado:**
  - HTTP 404 Not Found
  - `error_code`: `RES_ID_NOT_FOUND`
  - `message`: `"Reserva no encontrada"`

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] La reserva solo se crea si el horario está disponible y no se superó la capacidad máxima.
- [ ] No se permiten reservas solapadas para el mismo cliente o entrenador en el mismo horario exacto.
- [ ] El estado de la reserva se crea correctamente como CONFIRMADA.
- [ ] El listado de reservas filtra correctamente por idCliente.
- [ ] La consulta de capacidad expone la capacidadMaxima, reservasActuales y lugaresDisponibles en tiempo real.
- [ ] La respuesta JSON cumple con el contrato definido en todos los endpoints.

### 🧪 Pruebas Completadas

- [ ] Se ejecutaron los 10 casos de prueba definidos (5 exitosos, 5 de error).
- [ ] Se cubrieron todos los endpoints expuestos.
- [ ] Las pruebas funcionales están documentadas y pasadas.

### 📄 Documentación Técnica

- [ ] Endpoints documentados en Swagger / OpenAPI.
- [ ] Se describen campos de entrada y salida con ejemplos.

### 🔐 Manejo de Errores

- [ ] Se devuelve código HTTP 400 para parámetros inválidos.
- [ ] Se devuelve código HTTP 404 cuando no existe la reserva o no hay reservas para el cliente.
- [ ] Se devuelve código HTTP 409 para conflictos de horario o capacidad máxima.
- [ ] El campo `message` incluye texto descriptivo y amigable en todos los errores.