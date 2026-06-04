## [HU-01] Registro como cliente

### 📖 Historia de usuario

**Como** Cliente nuevo del gimnasio
**Quiero** Registrarme en FitZone con mis datos básicos
**Para** poder acceder a la plataforma, buscar entrenadores y reservar sesiones de entrenamiento

## 🔁 Flujo esperado

- El cliente completa el formulario de registro con nombre, correo electrónico, teléfono y contraseña.
- El sistema consume el endpoint `POST /api/v1/auth/registro` con rol=CLIENTE.
- El backend valida que el correo no esté registrado previamente.
- El cliente queda registrado con estado ACTIVO de inmediato.

## Criterios de aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `POST /api/v1/auth/registro` que recibe nombre, correo, teléfono y contraseña.
- [ ] El sistema asigna automáticamente el rol CLIENTE al nuevo usuario.
- [ ] Se verifica que el correo electrónico no esté ya registrado.
- [ ] El cliente queda en estado ACTIVO inmediatamente tras el registro.
- [ ] Se expone un endpoint `GET /api/v1/auth/clientes` que retorna todos los clientes registrados.
- [ ] Se expone un endpoint `GET /api/v1/auth/clientes/{id}` que retorna un cliente por su ID.
- [ ] Se expone un endpoint `DELETE /api/v1/auth/clientes/{id}` que elimina un cliente por su ID.
- [ ] Se expone un endpoint `PATCH /api/v1/auth/clientes/{id}/estado` que cambia el estado del cliente.
- [ ] Se expone un endpoint `GET /api/v1/auth/clientes/estado/{estado}` que filtra clientes por estado.

### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON cuando el registro es exitoso:

```json
{
  "success": true,
  "message": "Usuario registrado correctamente",
  "data": {
    "idUsuario": 42,
    "nombre": "Juan Pérez",
    "correo": "juan@fitzone.com",
    "rol": "CLIENTE",
    "estado": "ACTIVO"
  }
}
```

- [ ] Si el correo ya está registrado, se responde con código 409 y el siguiente JSON:

```json
{
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

## 🔧 Notas Técnicas

- **Método HTTP:** POST
- **Ruta:** /api/v1/auth/registro

## 📤 Ejemplo de Respuesta JSON

```json
"response_exitoso": {
  "success": true,
  "message": "Usuario registrado correctamente",
  "data": {
    "idUsuario": 42,
    "nombre": "Juan Pérez",
    "correo": "juan@fitzone.com",
    "rol": "CLIENTE",
    "estado": "ACTIVO"
  }
```

- [ ] Si el correo ya está registrado, el backend retorna:
```json
  },
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

## 🧪 Requisitos de prueba

## Casos de prueba funcional

### ✅ Caso 1: Registro exitoso con datos válidos

 - **Precondición**: El correo no existe en la base de datos.
 - **Accion**: `POST /api/v1/auth/registro` con datos completos y válidos.
 - **Resultado Esperado**:
    - HTTP 201 Created
    - Campo success: true
    - Se retorna el idUsuario asignado
    - Campo correo presente en la respuesta
    - Estado del usuario: ACTIVO

### ❌ Caso 2: Correo ya registrado

 - **Precondición**: El correo ya existe en la base de datos.
 - **Accion**: `POST /api/v1/auth/registro` con el mismo correo electrónico.
 - **Resultado Esperado**:
    - HTTP 409 Conflict
    - Campo success: false
    - error_code: AUTH_EMAIL_ALREADY_EXISTS
    - Message: El correo electrónico ya está registrado

### ❌ Caso 3: Campos obligatorios vacíos

 - **Precondición**: El body de la solicitud no contiene los campos requeridos.
 - **Accion**: `POST /api/v1/auth/registro` sin campos obligatorios.
 - **Resultado Esperado**:
    - HTTP 400 Bad Request
    - Mensaje descriptivo indicando el campo faltante.

### ❌ Caso 4: Contraseña sin mayúscula o sin número

 - **Precondición**: La contraseña enviada no cumple las reglas de seguridad.
 - **Accion**: `POST /api/v1/auth/registro` con contraseña como "sinseguridad".
 - **Resultado Esperado**:
    - HTTP 400 Bad Request
    - Mensaje: "La contraseña debe contener al menos una letra mayúscula" o "La contraseña debe contener al menos un número".

### ❌ Caso 5: Teléfono con caracteres no numéricos

 - **Precondición**: El campo teléfono contiene letras o caracteres especiales.
 - **Accion**: `POST /api/v1/auth/registro` con "telefono": "abc-xyz".
 - **Resultado Esperado**:
    - HTTP 400 Bad Request
    - Mensaje: "El teléfono solo puede contener dígitos".

### ✅ Caso 6: Listar todos los clientes

 - **Precondición**: Existen clientes registrados en la base de datos.
 - **Accion**: `GET /api/v1/auth/clientes`
 - **Resultado Esperado**:
    - HTTP 200 OK
    - Lista de clientes, cada uno con idUsuario, nombre, correo, rol y estado.

### ✅ Caso 7: Obtener cliente por ID

 - **Precondición**: El cliente con el ID indicado existe.
 - **Accion**: `GET /api/v1/auth/clientes/{id}` con un ID válido.
 - **Resultado Esperado**:
    - HTTP 200 OK
    - Objeto con todos los campos del cliente incluyendo correo y estado.

### ❌ Caso 8: Obtener cliente con ID inexistente

 - **Precondición**: No existe cliente con ese ID.
 - **Accion**: `GET /api/v1/auth/clientes/{id}` con ID no registrado.
 - **Resultado Esperado**:
    - HTTP 404 Not Found
    - Mensaje descriptivo indicando que el cliente no existe.

### ✅ Caso 9: Cambiar estado del cliente

 - **Precondición**: El cliente existe y su estado actual es conocido.
 - **Accion**: `PATCH /api/v1/auth/clientes/{id}/estado` con un estado válido (ACTIVO, INACTIVO o PENDIENTE).
 - **Resultado Esperado**:
    - HTTP 200 OK
    - Campo estado refleja el nuevo valor en la respuesta.

### ❌ Caso 10: Cambiar estado con valor inválido

 - **Precondición**: El cliente existe.
 - **Accion**: `PATCH /api/v1/auth/clientes/{id}/estado` con un valor diferente a ACTIVO, INACTIVO o PENDIENTE.
 - **Resultado Esperado**:
    - HTTP 400 Bad Request
    - Mensaje descriptivo sobre los valores permitidos.

### ✅ Caso 11: Eliminar cliente existente

 - **Precondición**: El cliente con el ID indicado existe.
 - **Accion**: `DELETE /api/v1/auth/clientes/{id}` con un ID válido.
 - **Resultado Esperado**:
    - HTTP 200 OK
    - Mensaje confirmando la eliminación.

### ❌ Caso 12: Eliminar cliente inexistente

 - **Precondición**: No existe cliente con ese ID.
 - **Accion**: `DELETE /api/v1/auth/clientes/{id}` con ID no registrado.
 - **Resultado Esperado**:
    - HTTP 404 Not Found
    - Mensaje descriptivo indicando que el cliente no existe.

### ✅ Caso 13: Filtrar clientes por estado

 - **Precondición**: Existen clientes con el estado indicado.
 - **Accion**: `GET /api/v1/auth/clientes/estado/{estado}` con un estado válido (ACTIVO, INACTIVO o PENDIENTE).
 - **Resultado Esperado**:
    - HTTP 200 OK
    - Lista de clientes que tienen exactamente ese estado.

### ❌ Caso 14: Filtrar por estado sin resultados

 - **Precondición**: No existen clientes con el estado indicado.
 - **Accion**: `GET /api/v1/auth/clientes/estado/{estado}` con un estado que no tiene registros.
 - **Resultado Esperado**:
    - HTTP 404 Not Found
    - Mensaje descriptivo indicando que no se encontraron clientes con ese estado.

## ✅ Definición de Hecho

## 📦 Alcance Funcional

 - [ ] El endpoint asigna correctamente el rol CLIENTE al nuevo usuario.
 - [ ] El cliente queda en estado ACTIVO inmediatamente al registrarse.
 - [ ] La respuesta JSON incluye el correo del cliente en todos los endpoints.
 - [ ] El correo duplicado retorna error 409 con mensaje claro.
 - [ ] El listado retorna todos los clientes con correo y estado.
 - [ ] La obtención por ID retorna todos los campos o 404 si no existe.
 - [ ] El cambio de estado refleja el nuevo valor en la respuesta.
 - [ ] La eliminación confirma la operación o retorna 404 si no existe.
 - [ ] El filtrado por estado retorna solo los clientes que coinciden.
 - [ ] La respuesta JSON cumple con el contrato definido.

## 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas unitarias para cada funcionalidad principal.
- [ ] Se cubrieron los casos de error y respuestas sin datos.
- [ ] Las pruebas funcionales están documentadas y pasadas.

## 📄 Documentación Técnica

- [ ] Endpoint documentado en Swagger / OpenAPI.
- [ ] Se describen campos de entrada y salida con ejemplos.

## 🔐 Manejo de Errores

- [ ] Se devuelve código HTTP 400 para parámetros inválidos.
- [ ] Se devuelve código HTTP 404 cuando el cliente no existe.
- [ ] Se devuelve código HTTP 409 para correo duplicado.
- [ ] Se devuelve código HTTP 500/503 ante fallos internos.
- [ ] El campo `mensaje` incluye texto descriptivo y amigable.
