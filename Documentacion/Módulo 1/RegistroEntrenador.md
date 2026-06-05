## [HU-02] Registro como entrenador

## 📖 Historia de Usuario

**Como** entrenador del gimnasio
**Quiero** registrarme en la plataforma con mis datos personales y profesionales
**Para** que los clientes del gimnasio puedan encontrarme, ver mi perfil y reservar sesiones de entrenamiento conmigo.

## 🔁 Flujo Esperado

- El entrenador completa el formulario de registro con nombre, correo, contraseña, especialidad y gimnasioId.
- El sistema consume el endpoint `POST /api/v1/entrenadores`.
- El backend valida que el correo no esté duplicado y crea el perfil.
- El perfil queda en estado ACTIVO y visible en el listado de entrenadores.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

 - [ ] Se expone un endpoint `POST /api/v1/entrenadores` con los datos del entrenador.
 - [ ] El sistema asigna automáticamente el rol ENTRENADOR.
 - [ ] Se registra la especialidad del entrenador.
 - [ ] El entrenador queda en estado ACTIVO inmediatamente tras el registro.
 - [ ] Se expone un endpoint `GET /api/v1/entrenadores` que retorna todos los entrenadores registrados.
 - [ ] Se expone un endpoint `GET /api/v1/entrenadores/activos` que retorna solo entrenadores con estado ACTIVO.
 - [ ] Se expone un endpoint `GET /api/v1/entrenadores/{id}` que retorna un entrenador por su ID.
 - [ ] Se expone un endpoint `PUT /api/v1/entrenadores/{id}` que actualiza todos los datos del entrenador.
 - [ ] Se expone un endpoint `DELETE /api/v1/entrenadores/{id}` que elimina un entrenador por su ID.
 - [ ] Se expone un endpoint `PATCH /api/v1/entrenadores/{id}/estado` que cambia el estado del entrenador.
 - [ ] Se expone un endpoint `GET /api/v1/entrenadores/gimnasio/{gimnasio_id}` que filtra entrenadores por gimnasio.

### 2. 📆 Validaciones
- [ ] Se responde con la siguiente estructura en JSON:
```json
 "request": {
      "nombre": "Carlos Villamizar",
      "correo": "carlos@fitzone.com",
      "contrasena": "Ent123*",
      "especialidad": "Musculación",
      "gimnasioId": 1
    },
```

## 🔧 Notas Técnicas

### 🚀 Endpoint – Registro de entrenador

**Método HTTP:** POST
**Ruta:** `/api/v1/entrenadores`

## 📤 Ejemplo de Respuesta JSON
```json
"response_exitoso": {
      "success": true,
      "message": "Entrenador registrado correctamente",
      "data": {
        "idUsuario": 10,
        "nombre": "Carlos Villamizar",
        "correo": "carlos@fitzone.com",
        "rol": "ENTRENADOR",
        "especialidad": "Musculación",
        "gimnasioId": 1,
        "estado": "ACTIVO"
      }
    },
```

- [ ] Si el correo ya está registrado, el backend retorna:
```json
    "response_error": {
      "success": false,
      "statusCode": 409,
      "message": "El correo ya está registrado",
      "error": {
        "error_code": "AUTH_EMAIL_ALREADY_EXISTS",
        "details": "Ya existe una cuenta asociada a ese correo electrónico",
        "timestamp": "2026-03-18T10:30:00"
      }
    } 
```

## 🧪 Requisitos de Pruebas

## 🔍 Casos de Prueba Funcional

### ✅ Caso 1: Registro exitoso de entrenador

**Precondición:** El correo no existe en la base de datos.
**Acción:** `POST /api/v1/entrenadores` con datos válidos y especialidad.
**Resultado Esperado:**
    - HTTP 201 Created
    - Campo success: true
    - Campo correo presente en la respuesta
    - Rol asignado: ENTRENADOR
    - Estado: ACTIVO
    - Especialidad registrada correctamente

### ✅ Caso 2: Listar todos los entrenadores

**Precondición:** Existen entrenadores registrados en la base de datos.
**Acción:** `GET /api/v1/entrenadores`
**Resultado Esperado:**
    - HTTP 200 OK
    - Lista de entrenadores, cada uno con idUsuario, nombre, correo, rol, especialidad, gimnasioId y estado.

### ✅ Caso 3: Listar entrenadores activos

**Precondición:** Existen entrenadores con estado ACTIVO.
**Acción:** `GET /api/v1/entrenadores/activos`
**Resultado Esperado:**
    - HTTP 200 OK
    - Solo entrenadores cuyo estado es ACTIVO, con todos sus campos.

### ❌ Caso 4: Listar activos sin resultados

**Precondición:** No existen entrenadores con estado ACTIVO.
**Acción:** `GET /api/v1/entrenadores/activos`
**Resultado Esperado:**
    - HTTP 404 Not Found
    - Mensaje descriptivo indicando que no hay entrenadores activos.

### ✅ Caso 5: Obtener entrenador por ID

**Precondición:** El entrenador con el ID indicado existe.
**Acción:** `GET /api/v1/entrenadores/{id}` con un ID válido.
**Resultado Esperado:**
    - HTTP 200 OK
    - Objeto con todos los campos: idUsuario, nombre, correo, rol, especialidad, gimnasioId y estado.

### ❌ Caso 6: Obtener entrenador con ID inexistente

**Precondición:** No existe entrenador con ese ID.
**Acción:** `GET /api/v1/entrenadores/{id}` con ID no registrado.
**Resultado Esperado:**
    - HTTP 404 Not Found
    - Mensaje descriptivo indicando que el entrenador no existe.

### ✅ Caso 7: Actualizar entrenador completo

**Precondición:** El entrenador con el ID indicado existe.
**Acción:** `PUT /api/v1/entrenadores/{id}` con todos los campos actualizados (nombre, correo, contrasena, especialidad, gimnasioId).
**Resultado Esperado:**
    - HTTP 200 OK
    - Todos los campos actualizados reflejados en la respuesta incluyendo correo, estado y gimnasioId.

### ❌ Caso 8: Actualizar entrenador inexistente

**Precondición:** No existe entrenador con ese ID.
**Acción:** `PUT /api/v1/entrenadores/{id}` con ID no registrado.
**Resultado Esperado:**
    - HTTP 404 Not Found
    - Mensaje descriptivo indicando que el entrenador no existe.

### ✅ Caso 9: Cambiar estado del entrenador

**Precondición:** El entrenador existe y su estado actual es conocido (consultable vía GET /api/v1/entrenadores/{id}).
**Acción:** `PATCH /api/v1/entrenadores/{id}/estado` con el nuevo estado (ACTIVO o INACTIVO).
**Resultado Esperado:**
    - HTTP 200 OK
    - Campo estado refleja el nuevo valor en la respuesta.

### ❌ Caso 10: Cambiar estado con valor inválido

**Precondición:** El entrenador existe.
**Acción:** `PATCH /api/v1/entrenadores/{id}/estado` con un valor diferente a ACTIVO o INACTIVO.
**Resultado Esperado:**
    - HTTP 400 Bad Request
    - Mensaje descriptivo sobre los valores permitidos.

### ✅ Caso 11: Eliminar entrenador existente

**Precondición:** El entrenador con el ID indicado existe.
**Acción:** `DELETE /api/v1/entrenadores/{id}` con un ID válido.
**Resultado Esperado:**
    - HTTP 200 OK
    - Mensaje confirmando la eliminación.

### ❌ Caso 12: Eliminar entrenador inexistente

**Precondición:** No existe entrenador con ese ID.
**Acción:** `DELETE /api/v1/entrenadores/{id}` con ID no registrado.
**Resultado Esperado:**
    - HTTP 404 Not Found
    - Mensaje descriptivo indicando que el entrenador no existe.

### ✅ Caso 13: Filtrar entrenadores por gimnasio

**Precondición:** Existen entrenadores asociados al gimnasio indicado.
**Acción:** `GET /api/v1/entrenadores/gimnasio/{gimnasio_id}` con un ID de gimnasio válido.
**Resultado Esperado:**
    - HTTP 200 OK
    - Lista de entrenadores que pertenecen a ese gimnasio, con todos sus campos.

### ❌ Caso 14: Correo duplicado

**Precondición:** El correo ya está en uso.
**Acción:** `POST /api/v1/entrenadores` con correo existente.
**Resultado Esperado:**
    - HTTP 409 Conflict
    - error_code: AUTH_EMAIL_ALREADY_EXISTS
    - Mensaje: "El correo electrónico ya está registrado."

## ✅ Definición de Hecho

## 📦 Alcance Funcional

 - [ ] El endpoint asigna correctamente el rol ENTRENADOR.
 - [ ] La respuesta en todos los endpoints incluye correo, estado y gimnasioId.
 - [ ] El entrenador queda ACTIVO al registrarse.
 - [ ] La actualización modifica todos los campos (nombre, correo, contrasena, especialidad, gimnasioId).
 - [ ] El cambio de estado muestra el estado resultante en la respuesta.
 - [ ] El perfil es visible en el listado al estar activo.
 - [ ] La eliminación confirma la operación o retorna 404 si no existe.
 - [ ] El filtrado por gimnasio retorna solo los entrenadores de ese gimnasio.

## 🧪 Pruebas Completadas

 - [ ] Se ejecutaron pruebas unitarias para la funcionalidad principal.
 - [ ] Se cubrieron los casos de error y respuesta sin datos.
 - [ ] Las pruebas funcionales están documentadas y pasadas.

## 📄 Documentación Técnica

 - [ ] Endpoint documentado en Swagger / OpenAPI.
 - [ ] Se describen campos de entrada y salida con ejemplos.

## 🔐 Manejo de Errores

 - [ ] Se devuelve código HTTP 400 para parámetros inválidos.
 - [ ] Se devuelve código HTTP 404 cuando el entrenador no existe.
 - [ ] Se devuelve código HTTP 409 para correo duplicado.
 - [ ] Se devuelve código HTTP 500/503 ante fallos internos.
 - [ ] El campo mensaje incluye texto descriptivo y amigable.
