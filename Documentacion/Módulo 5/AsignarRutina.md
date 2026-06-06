## [HU-15] Asignar rutina a clientes

### 📖 Historia de usuario

**Como** Entrenador del gimnasio
**Quiero** Asignar las rutinas cargadas a un día de la semana para todos mis clientes
**Para** Que cada cliente sepa exactamente qué ejercicios realizará en su sesión antes de llegar al gimnasio

## 🔁 Flujo esperado

- El entrenador accede a la sección de asignación de rutinas en su panel.
- El entrenador selecciona una rutina cargada y el día de la semana en que se aplicará.
- El sistema consume el endpoint `POST /api/rutinas/asignar` con idRutina, idEntrenador y diaSemana.
- El backend valida que la rutina exista y pertenezca al entrenador autenticado.
- La rutina queda asignada al día indicado y visible para todos los clientes con sesión ese día.

## Criterios de aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `POST /api/rutinas/asignar` que recibe idRutina, idEntrenador y diaSemana.
- [ ] Solo se pueden asignar rutinas que pertenezcan al entrenador autenticado.
- [ ] La rutina asignada es visible para todos los clientes con sesión en ese día de la semana.
- [ ] Se puede reasignar una rutina diferente a un día ya asignado.
- [ ] El campo `diaSemana` solo acepta valores del conjunto: LUNES, MARTES, MIÉRCOLES, JUEVES, VIERNES, SÁBADO, DOMINGO.

### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON:

```json
{
  "success": true,
  "message": "Rutina asignada correctamente",
  "data": {
    "idRutina": 24,
    "nombre": "Rutina Full Body Semana 1",
    "diaSemana": "LUNES"
  }
}
```

- [ ] Si la rutina no existe, el backend retorna:

```json
{
  "success": false,
  "statusCode": 404,
  "message": "Rutina no encontrada",
  "error": {
    "error_code": "RUT_NOT_FOUND",
    "details": "No existe una rutina con el ID proporcionado",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

- [ ] Si la rutina no pertenece al entrenador autenticado, el backend retorna:

```json
{
  "success": false,
  "statusCode": 403,
  "message": "Sin permisos",
  "error": {
    "error_code": "RUT_UNAUTHORIZED_EDIT",
    "details": "Solo el entrenador que creó la rutina puede modificar sus ejercicios",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

## 🔧 Notas Técnicas

- **Método HTTP:** `POST`
- **Ruta:** `/api/rutinas/asignar`
- El campo `diaSemana` debe enviarse en mayúsculas y en español.

## 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "message": "Rutina asignada correctamente",
  "data": {
    "idRutina": 24,
    "nombre": "Rutina Full Body Semana 1",
    "diaSemana": "LUNES"
  }
}
```

## 🧪 Requisitos de prueba

### Casos de prueba funcional

### ✅ Caso 1: Asignación exitosa de rutina a un día libre

- **Precondición:** La rutina existe, pertenece al entrenador autenticado y el día no tiene rutina asignada.
- **Acción:** `POST /api/rutinas/asignar` con idRutina, idEntrenador y diaSemana válidos.
- **Resultado esperado:**
  - HTTP 201 Created
  - Campo `success: true`
  - `diaSemana` reflejado correctamente en la respuesta
  - Rutina visible para los clientes con sesión ese día

### ✅ Caso 2: Reasignación de rutina a un día ya asignado

- **Precondición:** El día ya tiene una rutina asignada y el entrenador quiere cambiarla.
- **Acción:** `POST /api/rutinas/asignar` con nuevo idRutina para el mismo diaSemana.
- **Resultado esperado:**
  - HTTP 200 OK
  - Campo `success: true`
  - La nueva rutina reemplaza a la anterior para ese día

### ❌ Caso 3: Rutina no encontrada

- **Precondición:** El idRutina enviado no existe en la base de datos.
- **Acción:** `POST /api/rutinas/asignar` con idRutina inexistente.
- **Resultado esperado:**
  - HTTP 404 Not Found
  - Campo `success: false`
  - `error_code`: `RUT_NOT_FOUND`
  - Mensaje: `"Rutina no encontrada"`

### ❌ Caso 4: Entrenador intenta asignar rutina de otro entrenador

- **Precondición:** La rutina pertenece a otro entrenador diferente al autenticado.
- **Acción:** `POST /api/rutinas/asignar` con idRutina de otro entrenador.
- **Resultado esperado:**
  - HTTP 403 Forbidden
  - Campo `success: false`
  - `error_code`: `RUT_UNAUTHORIZED_EDIT`
  - Mensaje: `"Sin permisos"`

### ❌ Caso 5: Cliente intenta asignar una rutina

- **Precondición:** Usuario autenticado con rol CLIENTE.
- **Acción:** `POST /api/rutinas/asignar` con token de cliente y body válido.
- **Resultado esperado:**
  - HTTP 403 Forbidden
  - Campo `success: false`
  - `error_code`: `AUTH_UNAUTHORIZED`
  - Mensaje: `"Acceso denegado"`

### ❌ Caso 6: Solicitud sin token de autenticación

- **Precondición:** No se envía header de autenticación.
- **Acción:** `POST /api/rutinas/asignar` sin header `Authorization`.
- **Resultado esperado:**
  - HTTP 401 Unauthorized
  - Campo `success: false`
  - `error_code`: `AUTH_MISSING_TOKEN`
  - Mensaje: `"Token de autenticación requerido"`

### ❌ Caso 7: Valor de `diaSemana` inválido

- **Precondición:** El entrenador está autenticado y la rutina existe.
- **Acción:** `POST /api/rutinas/asignar` con `diaSemana: "FUNDAY"` u otro valor no permitido.
- **Resultado esperado:**
  - HTTP 422 Unprocessable Entity
  - Mensaje de validación indicando los valores aceptados para `diaSemana`

### ❌ Caso 8: `idRutina` o `idEntrenador` con valor cero o negativo

- **Precondición:** El entrenador está autenticado.
- **Acción:** `POST /api/rutinas/asignar` con `idRutina: 0` o `idEntrenador: -1`.
- **Resultado esperado:**
  - HTTP 422 Unprocessable Entity
  - Mensaje de validación indicando que los IDs deben ser mayores a `0`

### ❌ Caso 9: Campo `diaSemana` ausente en el body

- **Precondición:** El entrenador está autenticado y la rutina existe.
- **Acción:** `POST /api/rutinas/asignar` sin el campo `diaSemana`.
- **Resultado esperado:**
  - HTTP 422 Unprocessable Entity
  - Mensaje de validación indicando que `diaSemana` es un campo requerido

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] La rutina se asigna correctamente al día de la semana indicado.
- [ ] Solo se asignan rutinas que pertenecen al entrenador autenticado.
- [ ] La rutina asignada es visible de inmediato para los clientes con sesión ese día.
- [ ] Los clientes no pueden asignar rutinas y reciben HTTP 403.
- [ ] Las solicitudes sin token reciben HTTP 401.
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
- [ ] Se devuelve código HTTP 401 para solicitudes sin token.
- [ ] Se devuelve código HTTP 403 para acceso no autorizado.
- [ ] Se devuelve código HTTP 404 para rutina no encontrada.
- [ ] Se devuelve código HTTP 422 para datos de entrada con formato inválido.
- [ ] Se devuelve código HTTP 500/503 ante fallos internos.
- [ ] El campo `mensaje` incluye texto descriptivo y amigable.