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

## 🔧 Notas Técnicas

- **Método HTTP:** `POST`
- **Ruta:** `/api/rutinas/asignar`

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

## 🧪 Requisitos de prueba

### Casos de prueba funcional

### ✅ Caso 1: Asignación exitosa de rutina

- **Precondición:** La rutina existe y pertenece al entrenador autenticado.
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

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] La rutina se asigna correctamente al día de la semana indicado.
- [ ] Solo se asignan rutinas que pertenecen al entrenador autenticado.
- [ ] La rutina asignada es visible de inmediato para los clientes con sesión ese día.
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