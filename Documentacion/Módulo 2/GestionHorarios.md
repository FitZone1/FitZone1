## [HU-08] Gestionar horarios disponibles

### 📖 Historia de usuario

**Como** Entrenador del gimnasio
**Quiero** Publicar y gestionar mis horarios de disponibilidad semanal
**Para** Que los clientes solo puedan reservar sesiones en los momentos en que realmente estoy disponible y evitar conflictos de agenda

## 🔁 Flujo esperado

- El entrenador accede a la sección de gestión de horarios en su panel.
- El entrenador define los días disponibles, hora de inicio y hora de fin.
- El sistema consume el endpoint `POST /api/horarios/disponibilidad` con idEntrenador, diasDisponibles, horaInicio y horaFin.
- El backend valida que el rango horario sea válido y no haya conflictos.
- La disponibilidad queda publicada y visible para los clientes de inmediato.

## Criterios de aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `POST /api/horarios/disponibilidad` que recibe idEntrenador, diasDisponibles, horaInicio y horaFin.
- [ ] La hora de inicio no puede ser mayor a la hora de fin.
- [ ] Los cambios en disponibilidad se reflejan de inmediato para los clientes.
- [ ] No se puede bloquear un horario que ya tiene una reserva confirmada.

### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON:

```json
{
  "success": true,
  "message": "Disponibilidad publicada correctamente",
  "data": {
    "idEntrenador": 10,
    "diasDisponibles": ["LUNES", "MIERCOLES", "VIERNES"],
    "horaInicio": "07:00",
    "horaFin": "17:00"
  }
}
```

- [ ] Si el rango horario es inválido, el backend retorna:

```json
{
  "success": false,
  "statusCode": 400,
  "message": "Rango horario inválido",
  "error": {
    "error_code": "HOR_INVALID_TIME_RANGE",
    "details": "La hora de inicio no puede ser mayor a la hora de fin",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

## 🔧 Notas Técnicas

- **Método HTTP:** `POST`
- **Ruta:** `/api/horarios/disponibilidad`

## 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "message": "Disponibilidad publicada correctamente",
  "data": {
    "idEntrenador": 10,
    "diasDisponibles": ["LUNES", "MIERCOLES", "VIERNES"],
    "horaInicio": "07:00",
    "horaFin": "17:00"
  }
}
```

- [ ] Si se intenta bloquear un horario con reserva activa, el backend retorna:

```json
{
  "success": false,
  "statusCode": 409,
  "message": "Horario con reserva activa",
  "error": {
    "error_code": "HOR_ACTIVE_BOOKING_EXISTS",
    "details": "No se puede bloquear un horario que ya tiene una reserva confirmada",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

## 🧪 Requisitos de prueba

### Casos de prueba funcional

### ✅ Caso 1: Publicación exitosa de disponibilidad

- **Precondición:** El entrenador está autenticado y el rango horario es válido.
- **Acción:** `POST /api/horarios/disponibilidad` con diasDisponibles, horaInicio y horaFin válidos.
- **Resultado esperado:**
  - HTTP 201 Created
  - Campo `success: true`
  - Disponibilidad visible para los clientes de inmediato
  - Días y horarios reflejados correctamente en la respuesta

### ❌ Caso 2: Rango horario inválido

- **Precondición:** El entrenador envía una hora de inicio mayor a la hora de fin.
- **Acción:** `POST /api/horarios/disponibilidad` con horaInicio `"18:00"` y horaFin `"07:00"`.
- **Resultado esperado:**
  - HTTP 400 Bad Request
  - Campo `success: false`
  - `error_code`: `HOR_INVALID_TIME_RANGE`
  - Mensaje: `"Rango horario inválido"`

### ❌ Caso 3: Bloqueo de horario con reserva activa

- **Precondición:** El horario que se intenta bloquear ya tiene una reserva confirmada.
- **Acción:** `POST /api/horarios/bloquear` con fecha y hora de una reserva activa.
- **Resultado esperado:**
  - HTTP 409 Conflict
  - Campo `success: false`
  - `error_code`: `HOR_ACTIVE_BOOKING_EXISTS`
  - Mensaje: `"Horario con reserva activa"`

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] La disponibilidad se publica correctamente con los días y horarios definidos.
- [ ] El rango horario inválido retorna error 400 con mensaje claro.
- [ ] Los cambios en disponibilidad se reflejan de inmediato para los clientes.
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