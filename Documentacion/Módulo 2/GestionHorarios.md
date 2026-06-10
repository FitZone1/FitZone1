## [HU-08] Gestionar horarios disponibles

### 📖 Historia de usuario

**Como** Entrenador del gimnasio
**Quiero** Publicar, gestionar y cancelar mis horarios de disponibilidad semanal
**Para** Que los clientes solo puedan reservar sesiones en los momentos en que realmente estoy disponible, y poder retirar bloques de disponibilidad cuando sea necesario

## 🔁 Flujo esperado

- El entrenador accede a la sección de gestión de horarios en su panel.
- El entrenador define los días disponibles, hora de inicio y hora de fin.
- El sistema consume el endpoint `POST /api/horarios/disponibilidad` con idEntrenador, diasDisponibles, horaInicio y horaFin.
- El backend valida que el rango horario sea válido y no haya conflictos.
- La disponibilidad queda publicada y visible para los clientes de inmediato.
- Si el entrenador necesita retirar un bloque de disponibilidad, consume el endpoint `DELETE /api/horarios/disponibilidad/{idHorario}`.
- El backend valida que el horario no tenga reservas confirmadas antes de cancelarlo.

## Criterios de aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone `POST /api/horarios/disponibilidad` que recibe idEntrenador, diasDisponibles, horaInicio y horaFin.
- [ ] Se expone `DELETE /api/horarios/disponibilidad/{idHorario}` para cancelar un bloque de disponibilidad.
- [ ] La hora de inicio no puede ser mayor a la hora de fin.
- [ ] Los cambios en disponibilidad se reflejan de inmediato para los clientes.
- [ ] No se puede bloquear un horario que ya tiene una reserva confirmada.
- [ ] No se puede cancelar un horario de disponibilidad que tenga reservas confirmadas asociadas.

### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura al publicar disponibilidad:

```json
{
  "success": true,
  "message": "Disponibilidad publicada correctamente",
  "data": {
    "idHorario": 15,
    "idEntrenador": 10,
    "diasDisponibles": ["LUNES", "MIERCOLES", "VIERNES"],
    "horaInicio": "07:00",
    "horaFin": "17:00"
  }
}
```

- [ ] Se responde con la siguiente estructura al cancelar un horario disponible:

```json
{
  "success": true,
  "message": "Horario de disponibilidad cancelado correctamente",
  "data": {
    "idHorario": 15,
    "idEntrenador": 10,
    "estado": "CANCELADO"
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

- [ ] Si se intenta bloquear o cancelar un horario con reserva activa, el backend retorna:

```json
{
  "success": false,
  "statusCode": 409,
  "message": "Horario con reserva activa",
  "error": {
    "error_code": "HOR_ACTIVE_BOOKING_EXISTS",
    "details": "No se puede modificar un horario que ya tiene una reserva confirmada",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

- [ ] Si el horario no se encuentra al intentar cancelarlo, el backend retorna:

```json
{
  "success": false,
  "statusCode": 404,
  "message": "Horario no encontrado",
  "error": {
    "error_code": "HOR_NOT_FOUND",
    "details": "No existe un horario de disponibilidad con el ID proporcionado",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

## 🔧 Notas Técnicas

- `POST   /api/horarios/disponibilidad`              → Publicar disponibilidad
- `DELETE /api/horarios/disponibilidad/{idHorario}`  → Cancelar un bloque de disponibilidad

> La respuesta del `POST` incluye el campo `idHorario` generado, que el entrenador usará posteriormente para cancelar ese bloque con el `DELETE`.

## 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "message": "Disponibilidad publicada correctamente",
  "data": {
    "idHorario": 15,
    "idEntrenador": 10,
    "diasDisponibles": ["LUNES", "MIERCOLES", "VIERNES"],
    "horaInicio": "07:00",
    "horaFin": "17:00"
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
  - `idHorario` generado correctamente
  - Disponibilidad visible para los clientes de inmediato
  - Días y horarios reflejados correctamente en la respuesta


### ❌ Caso 2: Rango horario inválido

- **Precondición:** El entrenador envía una hora de inicio mayor a la hora de fin.
- **Acción:** `POST /api/horarios/disponibilidad` con horaInicio `"18:00"` y horaFin `"07:00"`.
- **Resultado esperado:**
  - HTTP 400 Bad Request
  - `error_code`: `HOR_INVALID_TIME_RANGE`
  - Mensaje: `"Rango horario inválido"`

### ✅ Caso 3: Obtener horario de un entrenador

- **Precondición:** Existe un horario registrado para el entrenador con idEntrenador=10 (incluido en el seed inicial).
- **Acción:** `GET /api/horarios/10`
- **Resultado esperado:**
  - HTTP 200 OK
  - Campo `success: true`
  - Detalle completo del horario con `diasDisponibles`, `horaInicio` y `horaFin`

### ❌ Caso 4: Entrenador sin horario registrado

- **Precondición:** No existe ningún horario para el entrenador con idEntrenador=999.
- **Acción:** `GET /api/horarios/999`
- **Resultado esperado:**
  - HTTP 404 Not Found
  - `error_code`: `HOR_NOT_FOUND`
  - `message`: `"Horario no encontrado"`


## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] La disponibilidad se publica correctamente con días y horarios definidos, retornando el `idHorario`.
- [ ] Un horario puede cancelarse siempre que no tenga reservas confirmadas.
- [ ] El rango horario inválido retorna error 400 con mensaje claro.
- [ ] Los cambios en disponibilidad se reflejan de inmediato para los clientes.
- [ ] La respuesta JSON cumple con el contrato definido en todos los casos.

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
- [ ] Se devuelve código HTTP 404 cuando el horario no existe.
- [ ] Se devuelve código HTTP 409 cuando hay reservas activas vinculadas al horario.
- [ ] Se devuelve código HTTP 500/503 ante fallos internos.
- [ ] El campo `message` incluye texto descriptivo y amigable.