## [HU-14] Cargar rutina de ejercicios

### 📖 Historia de usuario

**Como** Entrenador del gimnasio
**Quiero** Subir mis rutinas de ejercicios a la plataforma una sola vez
**Para** Poder asignarlas a todos mis clientes sin repetir el proceso para cada uno y optimizar mi tiempo de preparación

## 🔁 Flujo esperado

- El entrenador accede a la sección de gestión de rutinas en su panel.
- El entrenador completa el formulario con nombre de la rutina y lista de ejercicios con series y repeticiones.
- El sistema consume el endpoint `POST /api/rutinas` con idEntrenador, nombre y ejercicios.
- El backend valida que la rutina tenga al menos un ejercicio registrado y que el solicitante sea un entrenador autenticado.
- La rutina queda guardada y disponible para asignarse a los clientes del entrenador.

## Criterios de aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `POST /api/rutinas` que recibe idEntrenador, nombre y lista de ejercicios.
- [ ] Cada ejercicio debe incluir nombre, series y repeticiones con valores mayores a cero.
- [ ] La rutina debe tener al menos un ejercicio con nombre, series y repeticiones.
- [ ] Solo el entrenador autenticado puede cargar rutinas.
- [ ] La rutina queda asociada al entrenador que la creó.

### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON:

```json
{
  "success": true,
  "message": "Rutina cargada exitosamente",
  "data": {
    "idRutina": 24,
    "nombre": "Rutina Full Body Semana 1",
    "totalEjercicios": 2
  }
}
```

- [ ] Si la rutina no tiene ejercicios registrados, el backend retorna:

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

- [ ] Si el usuario no tiene rol de entrenador, el backend retorna:

```json
{
  "success": false,
  "statusCode": 403,
  "message": "Acceso denegado",
  "error": {
    "error_code": "AUTH_UNAUTHORIZED",
    "details": "Solo los entrenadores pueden crear rutinas",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

## 🔧 Notas Técnicas

- **Método HTTP:** `POST`
- **Ruta:** `/api/rutinas`
- `totalEjercicios` en la respuesta debe reflejar exactamente el número de elementos enviados en la lista `ejercicios`.

## 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "message": "Rutina cargada exitosamente",
  "data": {
    "idRutina": 24,
    "nombre": "Rutina Full Body Semana 1",
    "totalEjercicios": 2
  }
}
```

## 🧪 Requisitos de prueba

### Casos de prueba funcional

### ✅ Caso 1: Carga exitosa de rutina con múltiples ejercicios

- **Precondición:** El entrenador está autenticado y la rutina tiene al menos un ejercicio.
- **Acción:** `POST /api/rutinas` con idEntrenador, nombre y lista de 2 ejercicios válidos.
- **Resultado esperado:**
  - HTTP 201 Created
  - Campo `success: true`
  - `idRutina` generado correctamente
  - `totalEjercicios` refleja el número exacto de ejercicios cargados
  - Rutina asociada al entrenador creador

### ✅ Caso 2: Carga exitosa con un único ejercicio (límite mínimo)

- **Precondición:** El entrenador está autenticado y envía exactamente 1 ejercicio válido.
- **Acción:** `POST /api/rutinas` con lista de ejercicios de un solo elemento.
- **Resultado esperado:**
  - HTTP 201 Created
  - Campo `success: true`
  - `totalEjercicios: 1`
  - Rutina guardada y asociada al entrenador

### ❌ Caso 3: Rutina con lista de ejercicios vacía

- **Precondición:** El body de la solicitud contiene una lista de ejercicios vacía.
- **Acción:** `POST /api/rutinas` con `ejercicios: []`.
- **Resultado esperado:**
  - HTTP 400 Bad Request
  - Campo `success: false`
  - `error_code`: `RUT_EMPTY_EXERCISES`
  - Mensaje: `"Rutina sin ejercicios"`

### ❌ Caso 4: Rutina sin el campo `ejercicios` en el body

- **Precondición:** El body de la solicitud no incluye el campo `ejercicios`.
- **Acción:** `POST /api/rutinas` omitiendo el campo `ejercicios`.
- **Resultado esperado:**
  - HTTP 422 Unprocessable Entity
  - Mensaje de validación indicando que `ejercicios` es un campo requerido

### ❌ Caso 5: Ejercicio con `series` o `repeticiones` igual a cero o negativo

- **Precondición:** El entrenador está autenticado.
- **Acción:** `POST /api/rutinas` con un ejercicio donde `series: 0` o `repeticiones: -1`.
- **Resultado esperado:**
  - HTTP 422 Unprocessable Entity
  - Mensaje de validación indicando que `series` y `repeticiones` deben ser mayores a `0`

### ❌ Caso 6: Cliente intenta cargar una rutina

- **Precondición:** Usuario autenticado con rol CLIENTE.
- **Acción:** `POST /api/rutinas` con token de cliente y body válido.
- **Resultado esperado:**
  - HTTP 403 Forbidden
  - Campo `success: false`
  - `error_code`: `AUTH_UNAUTHORIZED`
  - Mensaje: `"Acceso denegado"`

### ❌ Caso 7: Solicitud sin token de autenticación

- **Precondición:** No se envía header de autenticación.
- **Acción:** `POST /api/rutinas` sin header `Authorization`.
- **Resultado esperado:**
  - HTTP 401 Unauthorized
  - Campo `success: false`
  - `error_code`: `AUTH_MISSING_TOKEN`
  - Mensaje: `"Token de autenticación requerido"`

### ❌ Caso 8: Nombre de la rutina vacío o menor al mínimo requerido

- **Precondición:** El entrenador está autenticado.
- **Acción:** `POST /api/rutinas` con `nombre: ""` o `nombre: "A"`.
- **Resultado esperado:**
  - HTTP 422 Unprocessable Entity
  - Mensaje de validación indicando longitud mínima requerida para `nombre`

### ❌ Caso 9: `idEntrenador` con valor cero o negativo

- **Precondición:** El entrenador está autenticado.
- **Acción:** `POST /api/rutinas` con `idEntrenador: 0` o `idEntrenador: -3`.
- **Resultado esperado:**
  - HTTP 422 Unprocessable Entity
  - Mensaje de validación indicando que `idEntrenador` debe ser mayor a `0`

### ✅ Caso 10: Nombre de rutina con espacios al inicio y al final

- **Precondición:** El entrenador está autenticado y envía ejercicios válidos.
- **Acción:** `POST /api/rutinas` con `nombre: "  Rutina Full Body  "`.
- **Resultado esperado:**
  - HTTP 201 Created
  - Campo `success: true`
  - `nombre` en la respuesta retorna `"Rutina Full Body"` sin espacios extremos

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] La rutina se crea correctamente con los ejercicios definidos.
- [ ] La propiedad de la rutina queda vinculada al entrenador creador.
- [ ] Los clientes no pueden crear rutinas y reciben HTTP 403.
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
- [ ] Se devuelve código HTTP 422 para datos de entrada con formato inválido.
- [ ] Se devuelve código HTTP 500/503 ante fallos internos.
- [ ] El campo `mensaje` incluye texto descriptivo y amigable.