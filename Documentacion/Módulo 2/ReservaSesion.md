## [HU-06] Reservar sesión de entrenamiento

### 📖 Historia de usuario

**Como** Cliente del gimnasio
**Quiero** Reservar una sesión de entrenamiento con un entrenador disponible, consultar mis reservas activas y conocer la disponibilidad real del entrenador
**Para** Asegurar mi espacio con el entrenador elegido, planificar mi rutina semanal y evitar intentar reservar en horarios ya llenos

## 🔁 Flujo esperado

- El cliente consulta la capacidad máxima de reservas del entrenador elegido para el día deseado.
- El cliente selecciona un horario disponible del entrenador.
- El sistema consume el endpoint `POST /api/reservas` con idCliente, idEntrenador, fecha e idZona.
- El backend valida que el horario esté disponible y no haya conflictos.
- Se crea la reserva con estado CONFIRMADA y se retorna el idReserva generado.
- El cliente puede listar todas sus reservas activas o consultar una reserva específica por ID.

## Criterios de aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone `POST /api/reservas` que recibe idCliente, idEntrenador, fecha e idZona.
- [ ] Se expone `GET /api/reservas?idCliente={id}` para listar todas las reservas de un cliente.
- [ ] Se expone `GET /api/reservas/{idReserva}` para obtener el detalle de una reserva por ID.
- [ ] Se expone `GET /api/reservas/capacidad?idEntrenador={id}&fecha={fecha}` para consultar la ocupación del entrenador en una fecha dada.
- [ ] Solo se puede reservar en horarios dentro del rango de disponibilidad declarado por el entrenador.
- [ ] Un cliente no puede tener dos reservas activas en el mismo horario.
- [ ] El cliente debe tener suscripción activa y mensualidad al día para reservar.
- [ ] El entrenador tiene una capacidad máxima de reservas por día configurada en el sistema.

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
    },
    {
      "idReserva": 90,
      "estado": "CONFIRMADA",
      "fecha": "2026-03-22T10:00:00",
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

## 📤 Ejemplo de Respuesta JSON

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

## 🧪 Requisitos de prueba

### Casos de prueba funcional

### ✅ Caso 1: Reserva exitosa

- **Precondición:** El horario está disponible y el cliente tiene suscripción activa.
- **Acción:** `POST /api/reservas` con idCliente, idEntrenador, fecha e idZona válidos.
- **Resultado esperado:**
  - HTTP 201 Created
  - Campo `success: true`
  - Estado de la reserva: `CONFIRMADA`
  - `idReserva` generado correctamente

### ✅ Caso 2: Listar reservas del cliente

- **Precondición:** El cliente tiene reservas activas registradas.
- **Acción:** `GET /api/reservas?idCliente=42`
- **Resultado esperado:**
  - HTTP 200 OK
  - Lista de reservas con idReserva, estado, fecha, idEntrenador e idCliente

### ✅ Caso 3: Obtener reserva por ID

- **Precondición:** La reserva existe.
- **Acción:** `GET /api/reservas/87`
- **Resultado esperado:**
  - HTTP 200 OK
  - Detalle completo de la reserva

### ✅ Caso 4: Consultar capacidad del entrenador

- **Precondición:** El entrenador existe y tiene reservas para esa fecha.
- **Acción:** `GET /api/reservas/capacidad?idEntrenador=10&fecha=2026-03-20`
- **Resultado esperado:**
  - HTTP 200 OK
  - Campo `capacidadMaxima`, `reservasActuales` y `lugaresDisponibles`

### ❌ Caso 5: Horario no disponible

- **Precondición:** El entrenador ya tiene una sesión en ese horario.
- **Acción:** `POST /api/reservas` con el mismo horario ya ocupado.
- **Resultado esperado:**
  - HTTP 409 Conflict
  - `error_code`: `RES_SCHEDULE_CONFLICT`

### ❌ Caso 6: Capacidad máxima alcanzada

- **Precondición:** El entrenador ya tiene el máximo de clientes para ese día.
- **Acción:** `POST /api/reservas` con fecha en día completo del entrenador.
- **Resultado esperado:**
  - HTTP 409 Conflict
  - `error_code`: `RES_MAX_CAPACITY_REACHED`

### ❌ Caso 7: Sin reservas para el cliente

- **Precondición:** El cliente no tiene reservas registradas.
- **Acción:** `GET /api/reservas?idCliente=42`
- **Resultado esperado:**
  - HTTP 404 Not Found
  - `error_code`: `RES_NOT_FOUND`

### ❌ Caso 8: Reserva no encontrada por ID

- **Precondición:** El idReserva no existe.
- **Acción:** `GET /api/reservas/999`
- **Resultado esperado:**
  - HTTP 404 Not Found
  - `error_code`: `RES_ID_NOT_FOUND`

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] La reserva solo se crea si el horario está disponible y no se superó la capacidad máxima.
- [ ] No se permiten reservas solapadas para el mismo cliente o entrenador.
- [ ] El estado de la reserva se crea correctamente como CONFIRMADA.
- [ ] El listado de reservas filtra correctamente por cliente.
- [ ] La consulta de capacidad refleja en tiempo real las reservas del entrenador.
- [ ] La respuesta JSON cumple con el contrato definido.

### 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas unitarias para cada funcionalidad principal.
- [ ] Se cubrieron los casos de error y respuestas sin datos.
- [ ] Las pruebas funcionales están documentadas y pasadas.

### 📄 Documentación Técnica

- [ ] Endpoints documentados en Swagger / OpenAPI.
- [ ] Se describen campos de entrada y salida con ejemplos.

### 🔐 Manejo de Errores

- [ ] Se devuelve código HTTP 400 para parámetros inválidos.
- [ ] Se devuelve código HTTP 401/403 para acceso no autorizado.
- [ ] Se devuelve código HTTP 404 cuando no existe la reserva o no hay reservas.
- [ ] Se devuelve código HTTP 409 para conflictos de horario o capacidad máxima.
- [ ] Se devuelve código HTTP 500/503 ante fallos internos.
- [ ] El campo `message` incluye texto descriptivo y amigable.