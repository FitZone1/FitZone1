## [HU-07] Cancelar reserva

### 📖 Historia de usuario

**Como** Cliente del gimnasio
**Quiero** Cancelar una reserva de entrenamiento que tengo activa
**Para** Liberar el horario del entrenador y reorganizar mi agenda de entrenamiento de forma flexible

## 🔁 Flujo esperado

- El cliente accede a la sección de mis reservas en la plataforma.
- El cliente selecciona la reserva que desea cancelar.
- El sistema consume el endpoint `DELETE /api/reservas/87` con el motivo de cancelación.
- El backend valida que la reserva no esté ya completada.
- El estado de la reserva se actualiza a CANCELADA y el horario del entrenador queda libre.

## Criterios de aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `DELETE /api/reservas/{idReserva}` que recibe idReserva y motivo.
- [ ] Solo se pueden cancelar reservas en estado CONFIRMADA.
- [ ] Una reserva en estado COMPLETADA no puede cancelarse.
- [ ] Al cancelar, el horario del entrenador queda disponible nuevamente.

### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON:

```json
{
  "success": true,
  "message": "Reserva cancelada correctamente",
  "data": {
    "idReserva": 87,
    "estado": "CANCELADA"
  }
}
```

- [ ] Si la reserva ya fue completada y no puede cancelarse, el backend retorna:

```json
{
  "success": false,
  "statusCode": 400,
  "message": "No se puede cancelar",
  "error": {
    "error_code": "RES_ALREADY_COMPLETED",
    "details": "La reserva ya fue completada y no puede cancelarse",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

## 🔧 Notas Técnicas

- **Método HTTP:** `DELETE`
- **Ruta:** `/api/reservas/{idReserva}`

## 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "message": "Reserva cancelada correctamente",
  "data": {
    "idReserva": 87,
    "estado": "CANCELADA"
  }
}
```

- [ ] Si la reserva ya fue completada, el backend retorna:

```json
{
  "success": false,
  "statusCode": 400,
  "message": "No se puede cancelar",
  "error": {
    "error_code": "RES_ALREADY_COMPLETED",
    "details": "La reserva ya fue completada y no puede cancelarse",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

## 🧪 Requisitos de prueba

### Casos de prueba funcional

### ✅ Caso 1: Cancelación exitosa de reserva

- **Precondición:** La reserva existe y está en estado CONFIRMADA.
- **Acción:** `DELETE /api/reservas/87` con motivo de cancelación válido.
- **Resultado esperado:**
  - HTTP 200 OK
  - Campo `success: true`
  - Estado actualizado a `CANCELADA`
  - Horario del entrenador liberado

### ❌ Caso 2: Reserva ya completada

- **Precondición:** La reserva ya tiene estado COMPLETADA.
- **Acción:** `DELETE /api/reservas/87` sobre una reserva completada.
- **Resultado esperado:**
  - HTTP 400 Bad Request
  - Campo `success: false`
  - `error_code`: `RES_ALREADY_COMPLETED`
  - Mensaje: `"No se puede cancelar"`

### ❌ Caso 3: Reserva no encontrada

- **Precondición:** El idReserva enviado no existe en la base de datos.
- **Acción:** `DELETE /api/reservas/999` con id inexistente.
- **Resultado esperado:**
  - HTTP 404 Not Found
  - Campo `success: false`
  - Mensaje descriptivo indicando que la reserva no existe

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] Solo se cancelan reservas en estado CONFIRMADA.
- [ ] El horario del entrenador se libera correctamente tras la cancelación.
- [ ] Las reservas en estado COMPLETADA retornan error 400 con mensaje claro.
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