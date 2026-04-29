## [HU-20] Confirmación de sesión

### 📖 Historia de usuario

**Como** Cliente o entrenador del gimnasio
**Quiero** Confirmar que una sesión de entrenamiento se realizó correctamente
**Para** Actualizar el estado de la reserva a COMPLETADA en el sistema y habilitar la opción de dejar una reseña del entrenamiento

## 🔁 Flujo esperado

- Una vez finalizada la sesión, el cliente o entrenador accede a la reserva en su panel.
- El sistema consume el endpoint `PATCH /api/sesiones/87/confirmar` con idReserva, idUsuario y rol.
- El backend valida que la reserva esté en estado CONFIRMADA y que el cliente tenga suscripción activa.
- El estado de la reserva pasa de CONFIRMADA a COMPLETADA.
- Se habilita la opción de dejar reseña para el cliente.

## Criterios de aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `PATCH /api/sesiones/{idReserva}/confirmar` que recibe idReserva, idUsuario y rol.
- [ ] Solo se puede confirmar una sesión si la reserva está en estado CONFIRMADA.
- [ ] El cliente debe tener plan de suscripción activo y mensualidad al día para confirmar.
- [ ] Una sesión ya confirmada o cancelada no puede confirmarse nuevamente.

### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON:

```json
{
  "success": true,
  "message": "Sesión confirmada correctamente",
  "data": {
    "idReserva": 87,
    "estado": "COMPLETADA",
    "fecha": "2026-03-20T15:00:00"
  }
}
```

- [ ] Si la sesión ya fue confirmada o cancelada, el backend retorna:

```json
{
  "success": false,
  "statusCode": 400,
  "message": "Sesión no confirmable",
  "error": {
    "error_code": "SES_ALREADY_CONFIRMED",
    "details": "La sesión ya fue confirmada anteriormente o fue cancelada",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

## 🔧 Notas Técnicas

- **Método HTTP:** `PATCH`
- **Ruta:** `/api/sesiones/{idReserva}/confirmar`

## 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "message": "Sesión confirmada correctamente",
  "data": {
    "idReserva": 87,
    "estado": "COMPLETADA",
    "fecha": "2026-03-20T15:00:00"
  }
}
```

- [ ] Si la sesión ya fue confirmada o cancelada previamente, el backend retorna:

```json
{
  "success": false,
  "statusCode": 400,
  "message": "Sesión no confirmable",
  "error": {
    "error_code": "SES_ALREADY_CONFIRMED",
    "details": "La sesión ya fue confirmada anteriormente o fue cancelada",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

## 🧪 Requisitos de prueba

### Casos de prueba funcional

### ✅ Caso 1: Confirmación exitosa de sesión

- **Precondición:** La reserva está en estado CONFIRMADA y el cliente tiene suscripción activa y mensualidad al día.
- **Acción:** `PATCH /api/sesiones/87/confirmar` con idReserva, idUsuario y rol válidos.
- **Resultado esperado:**
  - HTTP 200 OK
  - Campo `success: true`
  - Estado de la reserva actualizado a `COMPLETADA`
  - Opción de reseña habilitada para el cliente
  - Sesión registrada en el historial del entrenador

### ✅ Caso 2: Confirmación realizada por el entrenador

- **Precondición:** La reserva está en estado CONFIRMADA y el entrenador la confirma desde su panel.
- **Acción:** `PATCH /api/sesiones/87/confirmar` con rol=ENTRENADOR y token válido.
- **Resultado esperado:**
  - HTTP 200 OK
  - Campo `success: true`
  - Estado actualizado a `COMPLETADA`
  - Sesión registrada en el historial del entrenador

### ❌ Caso 3: Sesión ya confirmada anteriormente

- **Precondición:** La reserva ya tiene estado COMPLETADA.
- **Acción:** `PATCH /api/sesiones/87/confirmar` sobre una sesión ya completada.
- **Resultado esperado:**
  - HTTP 400 Bad Request
  - Campo `success: false`
  - `error_code`: `SES_ALREADY_CONFIRMED`
  - Mensaje: `"Sesión no confirmable"`

### ❌ Caso 4: Sesión cancelada no confirmable

- **Precondición:** La reserva tiene estado CANCELADA.
- **Acción:** `PATCH /api/sesiones/87/confirmar` sobre una sesión cancelada.
- **Resultado esperado:**
  - HTTP 400 Bad Request
  - Campo `success: false`
  - `error_code`: `SES_ALREADY_CONFIRMED`
  - Mensaje: `"Sesión no confirmable"`

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] El estado de la reserva pasa correctamente a COMPLETADA tras la confirmación.
- [ ] La mensualidad activa del cliente es validada antes de confirmar.
- [ ] La opción de reseña se habilita únicamente tras sesión completada.
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