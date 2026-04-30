## [HU-14] Cargar rutina de ejercicios

### 📖 Historia de usuario

**Como** Entrenador del gimnasio
**Quiero** Subir mis rutinas de ejercicios a la plataforma una sola vez
**Para** Poder asignarlas a todos mis clientes sin repetir el proceso para cada uno y optimizar mi tiempo de preparación

## 🔁 Flujo esperado

- El entrenador accede a la sección de gestión de rutinas en su panel.
- El entrenador completa el formulario con nombre de la rutina y lista de ejercicios con series y repeticiones.
- El sistema consume el endpoint `POST /api/rutinas` con idEntrenador, nombre y ejercicios.
- El backend valida que la rutina tenga al menos un ejercicio registrado.
- La rutina queda guardada y disponible para asignarse a los clientes del entrenador.

## Criterios de aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `POST /api/rutinas` que recibe idEntrenador, nombre y lista de ejercicios.
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

## 🔧 Notas Técnicas

- **Método HTTP:** `POST`
- **Ruta:** `/api/rutinas`

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

- [ ] Si la rutina no contiene ejercicios, el backend retorna:

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

## 🧪 Requisitos de prueba

### Casos de prueba funcional

### ✅ Caso 1: Carga exitosa de rutina

- **Precondición:** El entrenador está autenticado y la rutina tiene al menos un ejercicio.
- **Acción:** `POST /api/rutinas` con idEntrenador, nombre y lista de ejercicios válidos.
- **Resultado esperado:**
  - HTTP 201 Created
  - Campo `success: true`
  - `idRutina` generado correctamente
  - `totalEjercicios` refleja el número de ejercicios cargados
  - Rutina asociada al entrenador creador

### ❌ Caso 2: Rutina sin ejercicios

- **Precondición:** El body de la solicitud contiene una lista de ejercicios vacía.
- **Acción:** `POST /api/rutinas` con lista de ejercicios vacía.
- **Resultado esperado:**
  - HTTP 400 Bad Request
  - Campo `success: false`
  - `error_code`: `RUT_EMPTY_EXERCISES`
  - Mensaje: `"Rutina sin ejercicios"`

### ❌ Caso 3: Cliente intenta cargar una rutina

- **Precondición:** Usuario autenticado con rol CLIENTE.
- **Acción:** `POST /api/rutinas` con token de cliente.
- **Resultado esperado:**
  - HTTP 403 Forbidden
  - Campo `success: false`
  - `error_code`: `AUTH_UNAUTHORIZED`
  - Mensaje: `"Acceso denegado"`

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] La rutina se crea correctamente con los ejercicios definidos.
- [ ] La propiedad de la rutina queda vinculada al entrenador creador.
- [ ] Los clientes no pueden crear rutinas y reciben HTTP 403.
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