## [HU-17] Actualizar ejercicios de una rutina

### 📖 Historia de usuario

**Como** Entrenador del gimnasio
**Quiero** Modificar los ejercicios de una rutina existente que yo mismo he creado
**Para** Adaptar el contenido del entrenamiento a las necesidades del gimnasio manteniendo los cambios uniformes para todos los clientes asignados a esa rutina

## 🔁 Flujo esperado

- El entrenador accede a la sección de rutinas en su panel y selecciona la rutina que desea modificar.
- El entrenador edita, agrega o elimina ejercicios de la rutina.
- El sistema consume el endpoint `PUT /api/rutinas/24/ejercicios` con idRutina y la lista de ejercicios actualizada.
- El backend valida que el entrenador autenticado sea el creador original de la rutina.
- Los cambios se aplican y son visibles de inmediato para todos los clientes asignados a esa rutina.

## Criterios de aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `PUT /api/rutinas/{idRutina}/ejercicios` que recibe idRutina y lista de ejercicios actualizada.
- [ ] Solo el entrenador que creó la rutina puede modificar sus ejercicios.
- [ ] La rutina debe mantener al menos un ejercicio después de cualquier modificación.
- [ ] Cada ejercicio debe incluir nombre, series y repeticiones con valores mayores a cero.
- [ ] Los cambios aplican de inmediato para todos los clientes asignados a esa rutina.

### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON:

```json
{
  "success": true,
  "message": "Ejercicios actualizados correctamente",
  "data": {
    "idRutina": 24,
    "nombre": "Rutina Full Body Semana 1",
    "totalEjercicios": 3
  }
}
```

- [ ] Si el entrenador no tiene permisos para modificar la rutina, el backend retorna:

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

- [ ] Si la lista de ejercicios enviada está vacía, el backend retorna:

```json
{
  "success": false,
  "statusCode": 400,
  "message": "Rutina sin ejercicios",
  "error": {
    "error_code": "RUT_EMPTY_EXERCISES",
    "details": "La rutina debe tener al menos un ejercicio registrado",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

## 🔧 Notas Técnicas

- **Método HTTP:** `PUT`
- **Ruta:** `/api/rutinas/{idRutina}/ejercicios`
- La lista de ejercicios reemplaza completamente la lista anterior de la rutina.

## 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "message": "Ejercicios actualizados correctamente",
  "data": {
    "idRutina": 24,
    "nombre": "Rutina Full Body Semana 1",
    "totalEjercicios": 3
  }
}
```

## 🧪 Requisitos de prueba

### Casos de prueba funcional

### ✅ Caso 1: Actualización exitosa de ejercicios

- **Precondición:** El entrenador autenticado es el creador de la rutina y envía al menos un ejercicio válido.
- **Acción:** `PUT /api/rutinas/24/ejercicios` con lista de ejercicios actualizada.
- **Resultado esperado:**
  - HTTP 200 OK
  - Campo `success: true`
  - `totalEjercicios` refleja el número actualizado de ejercicios
  - Cambios visibles de inmediato para todos los clientes asignados

### ✅ Caso 2: Agregar un nuevo ejercicio a la rutina

- **Precondición:** El entrenador autenticado es el creador de la rutina.
- **Acción:** `PUT /api/rutinas/24/ejercicios` con la lista anterior más un ejercicio nuevo.
- **Resultado esperado:**
  - HTTP 200 OK
  - Campo `success: true`
  - `totalEjercicios` incrementado en uno respecto al total anterior

### ✅ Caso 3: Reducir la rutina al mínimo de un ejercicio

- **Precondición:** El entrenador autenticado es el creador de la rutina y la rutina tiene más de un ejercicio.
- **Acción:** `PUT /api/rutinas/24/ejercicios` enviando una lista con exactamente 1 ejercicio válido.
- **Resultado esperado:**
  - HTTP 200 OK
  - Campo `success: true`
  - `totalEjercicios: 1`

### ❌ Caso 4: Otro entrenador intenta modificar la rutina

- **Precondición:** El entrenador autenticado NO es el creador de la rutina.
- **Acción:** `PUT /api/rutinas/24/ejercicios` con token de otro entrenador.
- **Resultado esperado:**
  - HTTP 403 Forbidden
  - Campo `success: false`
  - `error_code`: `RUT_UNAUTHORIZED_EDIT`
  - Mensaje: `"Sin permisos"`

### ❌ Caso 5: Rutina no encontrada

- **Precondición:** El idRutina enviado no existe en la base de datos.
- **Acción:** `PUT /api/rutinas/999/ejercicios` con id inexistente.
- **Resultado esperado:**
  - HTTP 404 Not Found
  - Campo `success: false`
  - `error_code`: `RUT_NOT_FOUND`
  - Mensaje descriptivo indicando que la rutina no existe

### ❌ Caso 6: Lista de ejercicios vacía

- **Precondición:** El entrenador autenticado es el creador de la rutina.
- **Acción:** `PUT /api/rutinas/24/ejercicios` con `ejercicios: []`.
- **Resultado esperado:**
  - HTTP 400 Bad Request
  - Campo `success: false`
  - `error_code`: `RUT_EMPTY_EXERCISES`
  - Mensaje: `"Rutina sin ejercicios"`

### ❌ Caso 7: Ejercicio con `series` o `repeticiones` igual a cero o negativo

- **Precondición:** El entrenador autenticado es el creador de la rutina.
- **Acción:** `PUT /api/rutinas/24/ejercicios` con un ejercicio donde `series: 0` o `repeticiones: -2`.
- **Resultado esperado:**
  - HTTP 422 Unprocessable Entity
  - Mensaje de validación indicando que `series` y `repeticiones` deben ser mayores a `0`

### ❌ Caso 8: Solicitud sin token de autenticación

- **Precondición:** No se envía header de autenticación.
- **Acción:** `PUT /api/rutinas/24/ejercicios` sin header `Authorization`.
- **Resultado esperado:**
  - HTTP 401 Unauthorized
  - Campo `success: false`
  - `error_code`: `AUTH_MISSING_TOKEN`
  - Mensaje: `"Token de autenticación requerido"`

### ❌ Caso 9: `idRutina` en la URL no es un entero válido

- **Precondición:** El entrenador está autenticado.
- **Acción:** `PUT /api/rutinas/abc/ejercicios` con un id no numérico en la URL.
- **Resultado esperado:**
  - HTTP 422 Unprocessable Entity
  - Mensaje de validación indicando que `idRutina` debe ser un entero válido

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] Solo el entrenador creador puede modificar los ejercicios de la rutina.
- [ ] Los cambios se aplican de inmediato para todos los clientes asignados.
- [ ] La rutina siempre mantiene al menos un ejercicio tras la modificación.
- [ ] Los clientes no pueden modificar rutinas y reciben HTTP 403.
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

- [ ] Se devuelve código HTTP 400 para lista de ejercicios vacía.
- [ ] Se devuelve código HTTP 401 para solicitudes sin token.
- [ ] Se devuelve código HTTP 403 para acceso no autorizado.
- [ ] Se devuelve código HTTP 404 para rutina no encontrada.
- [ ] Se devuelve código HTTP 422 para datos de entrada con formato inválido.
- [ ] Se devuelve código HTTP 500/503 ante fallos internos.
- [ ] El campo `mensaje` incluye texto descriptivo y amigable.