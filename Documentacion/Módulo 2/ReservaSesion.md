## [HU-06] Reservar sesión de entrenamiento

### 📖 Historia de usuario

**Como** Cliente del gimnasio
**Quiero** Reservar una sesión de entrenamiento con un entrenador disponible en el horario que me convenga
**Para** Asegurar mi espacio con el entrenador elegido y planificar mi rutina de entrenamiento semanal

## 🔁 Flujo esperado

- El cliente selecciona un entrenador disponible en la plataforma.
- El cliente elige un horario disponible del entrenador.
- El sistema consume el endpoint `POST /api/reservas` con idCliente, idEntrenador, fecha e idZona.
- El backend valida que el horario esté disponible y no haya conflictos.
- Se crea la reserva con estado CONFIRMADA y se retorna el idReserva generado.

## Criterios de aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `POST /api/reservas` que recibe idCliente, idEntrenador, fecha e idZona.
- [ ] Solo se puede reservar en horarios dentro del rango de disponibilidad declarado por el entrenador.
- [ ] Un cliente no puede tener dos reservas activas en el mismo horario.
- [ ] El cliente debe tener suscripción activa y mensualidad al día para reservar.

### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON:

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

## 🔧 Notas Técnicas

- **Método HTTP:** `POST`
- **Ruta:** `/api/reservas`

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

- [ ] Si el entrenador alcanzó el máximo de clientes para ese día, el backend retorna:

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

### ❌ Caso 2: Horario no disponible

- **Precondición:** El entrenador ya tiene una sesión asignada en ese horario.
- **Acción:** `POST /api/reservas` con el mismo horario ya ocupado.
- **Resultado esperado:**
  - HTTP 409 Conflict
  - Campo `success: false`
  - `error_code`: `RES_SCHEDULE_CONFLICT`
  - Mensaje: `"Horario no disponible"`

### ❌ Caso 3: Capacidad máxima del entrenador alcanzada

- **Precondición:** El entrenador ya tiene el máximo de clientes asignados para ese día.
- **Acción:** `POST /api/reservas` con fecha en día completo del entrenador.
- **Resultado esperado:**
  - HTTP 409 Conflict
  - Campo `success: false`
  - `error_code`: `RES_MAX_CAPACITY_REACHED`
  - Mensaje: `"Capacidad máxima alcanzada"`

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] La reserva solo se crea si el horario está disponible.
- [ ] No se permiten reservas solapadas para el mismo cliente o entrenador.
- [ ] El estado de la reserva se crea correctamente como CONFIRMADA.
- [ ] La respuesta JSON cumple con el contrato definido.

### 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas unitarias para cada funcionalidad principal.
- [ ] Se cubrieron los casos de error y respuestas sin datos.
- [ ] Las pruebas funcionales están documentadas y pasadas.

### 📄 Documentación Técnica

- [ ] Endpoint documentado en Swagger / OpenAPI.
- [ ] Se describen campos de entrada y salida con ejemplos.

### 🔐 Manejo de Errores

- [ ] Se devuelve código HTTP 400 para parámetros inválidos.
- [ ] Se devuelve código HTTP 401/403 para acceso no autorizado.
- [ ] Se devuelve código HTTP 500/503 ante fallos internos.
- [ ] El campo `mensaje` incluye texto descriptivo y amigable.