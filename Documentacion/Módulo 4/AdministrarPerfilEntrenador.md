## [HU-13] Administrar perfil del entrenador

### 📖 Historia de usuario

**Como** Entrenador del gimnasio
**Quiero** Crear y mantener actualizado mi perfil con mis datos personales, especialidad y años de experiencia
**Para** Que los clientes puedan conocer mi información profesional antes de reservar una sesión conmigo y tomar una decisión informada

## 🔁 Flujo esperado

- El entrenador accede a la sección "Mi perfil" en su panel.
- El sistema consume el endpoint `PUT /api/perfiles/entrenador/10` con los datos actualizados.
- El backend valida que el entrenador exista y actualiza la información.
- Los cambios quedan visibles de inmediato en el listado de entrenadores disponibles para los clientes.

## Criterios de aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `PUT /api/perfiles/entrenador/{idEntrenador}` que recibe nombre, especialidad, teléfono y experienciaAnios.
- [ ] Se expone un endpoint `PATCH /api/perfiles/42/datos` para actualizar correo, teléfono o contraseña.
- [ ] Solo el entrenador autenticado puede modificar su propio perfil.
- [ ] Los cambios en el perfil son visibles de inmediato en el listado de entrenadores disponibles.

### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON al actualizar el perfil:

```json
{
  "success": true,
  "message": "Perfil de entrenador actualizado correctamente",
  "data": {
    "idEntrenador": 10,
    "nombre": "Carlos Villamizar",
    "especialidad": "Musculación",
    "experienciaAnios": 5
  }
}
```

- [ ] Si el entrenador no existe, el backend retorna:

```json
{
  "success": false,
  "statusCode": 404,
  "message": "Entrenador no encontrado",
  "error": {
    "error_code": "PROF_TRAINER_NOT_FOUND",
    "details": "No existe un entrenador con el ID proporcionado",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

## 🔧 Notas Técnicas

- **Método HTTP:** `PUT` para actualizar perfil / `PATCH` para datos de acceso
- **Ruta perfil:** `/api/perfiles/entrenador/{idEntrenador}`
- **Ruta datos:** `/api/perfiles/42/datos`

## 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "message": "Perfil de entrenador actualizado correctamente",
  "data": {
    "idEntrenador": 10,
    "nombre": "Carlos Villamizar",
    "especialidad": "Musculación",
    "experienciaAnios": 5
  }
}
```

- [ ] Si el correo ingresado ya está en uso por otra cuenta, el backend retorna:

```json
{
  "success": false,
  "statusCode": 400,
  "message": "Datos inválidos",
  "error": {
    "error_code": "PROF_INVALID_DATA",
    "details": "El correo ingresado ya está en uso por otra cuenta",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

## 🧪 Requisitos de prueba

### Casos de prueba funcional

### ✅ Caso 1: Actualización exitosa del perfil del entrenador

- **Precondición:** El entrenador está autenticado con token válido.
- **Acción:** `PUT /api/perfiles/entrenador/10` con nombre, especialidad, teléfono y experienciaAnios válidos.
- **Resultado esperado:**
  - HTTP 200 OK
  - Campo `success: true`
  - Datos actualizados reflejados en la respuesta
  - Cambios visibles de inmediato en el listado de entrenadores

### ✅ Caso 2: Actualización exitosa de datos de acceso

- **Precondición:** El entrenador está autenticado y el nuevo correo no está en uso.
- **Acción:** `PATCH /api/perfiles/42/datos` con correo, teléfono y contraseña nuevos.
- **Resultado esperado:**
  - HTTP 200 OK
  - Campo `success: true`
  - Correo y teléfono actualizados correctamente en la respuesta

### ❌ Caso 3: Entrenador no encontrado

- **Precondición:** El idEntrenador enviado no existe en la base de datos.
- **Acción:** `PUT /api/perfiles/entrenador/999` con id inexistente.
- **Resultado esperado:**
  - HTTP 404 Not Found
  - Campo `success: false`
  - `error_code`: `PROF_TRAINER_NOT_FOUND`
  - Mensaje: `"Entrenador no encontrado"`

### ❌ Caso 4: Correo ya en uso por otra cuenta

- **Precondición:** El correo que intenta registrar el entrenador ya está asociado a otra cuenta.
- **Acción:** `PATCH /api/perfiles/42/datos` con correo existente en otra cuenta.
- **Resultado esperado:**
  - HTTP 400 Bad Request
  - Campo `success: false`
  - `error_code`: `PROF_INVALID_DATA`
  - Mensaje: `"Datos inválidos"`

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] El perfil del entrenador se actualiza correctamente con los datos enviados.
- [ ] Los cambios son visibles de inmediato en el listado de entrenadores disponibles.
- [ ] El correo duplicado retorna error 400 con mensaje claro.
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