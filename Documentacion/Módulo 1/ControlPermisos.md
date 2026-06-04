## [HU-04] Control de permisos por rol

### 📖 Historia de usuario

**Como** Sistema de autorización de FitZone
**Quiero** Controlar qué acciones puede realizar cada usuario según su rol (CLIENTE o ENTRENADOR)
**Para** Garantizar que ningún usuario acceda a funciones que no le corresponden y mantener la seguridad de la plataforma

## 🔁 Flujo esperado

- El usuario realiza una solicitud a un endpoint protegido incluyendo su token JWT.
- El sistema consume el endpoint `POST /api/auth/validar-autorizacion` con el token, recurso y acción.
- El backend extrae el rol del token y valida si tiene permiso para ejecutar la acción solicitada.
- Si tiene permiso, se retorna `autorizado: true` y se continúa con la operación.
- Si no tiene permiso, se retorna HTTP 403 con el código `AUTH_UNAUTHORIZED`.

## Tabla de permisos por rol

| Rol        | Recurso   | Acciones permitidas                     |
|------------|-----------|------------------------------------------|
| CLIENTE    | rutinas   | VER                                      |
| CLIENTE    | pagos     | CREAR, VER                               |
| CLIENTE    | planes    | SUSCRIBIR, VER                           |
| CLIENTE    | reservas  | CREAR, VER, CANCELAR                     |
| CLIENTE    | perfil    | VER, EDITAR                              |
| ENTRENADOR | rutinas   | CREAR, VER, EDITAR, ELIMINAR             |
| ENTRENADOR | reservas  | VER                                      |
| ENTRENADOR | perfil    | VER, EDITAR                              |
| ENTRENADOR | clientes  | VER                                      |
| ENTRENADOR | horarios  | CREAR, VER, EDITAR                       |

> **Reglas clave:**
> - Los clientes **NO** pueden CREAR, EDITAR ni ELIMINAR rutinas.
> - Los entrenadores **NO** pueden realizar pagos ni suscribirse a planes.

## Criterios de aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `POST /api/auth/validar-autorizacion` que recibe token, recurso y acción.
- [ ] El backend extrae el rol del token y lo valida contra el mapa de permisos.
- [ ] Los clientes NO pueden CREAR, EDITAR ni ELIMINAR rutinas.
- [ ] Los entrenadores NO pueden realizar pagos ni suscribirse a planes.
- [ ] Un recurso o acción no reconocidos retorna HTTP 403.

### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura cuando el acceso es autorizado:

```json
{
  "success": true,
  "message": "Acceso autorizado correctamente",
  "data": {
    "idUsuario": 42,
    "autorizado": true
  }
}
```

- [ ] Si el rol no tiene permisos para la acción solicitada:

```json
{
  "success": false,
  "statusCode": 403,
  "message": "Acceso denegado",
  "error": {
    "error_code": "AUTH_UNAUTHORIZED",
    "details": "El token no tiene permisos para acceder a este recurso",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

- [ ] Si el token es inválido o está expirado:

```json
{
  "success": false,
  "statusCode": 401,
  "message": "Credenciales incorrectas",
  "error": {
    "error_code": "AUTH_INVALID_CREDENTIALS",
    "details": "El correo o la contraseña no son válidos",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

## 🔧 Notas Técnicas

- **Método HTTP:** `POST`
- **Ruta:** `/api/auth/validar-autorizacion`
- El token sigue el formato `jwt_{idUsuario}_{ROL}_token`. El backend lo decodifica extrayendo `id_usuario` y `rol`.
- El campo `recurso` se normaliza a minúsculas; el campo `accion` a mayúsculas antes de validar.

## 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "message": "Acceso autorizado correctamente",
  "data": {
    "idUsuario": 42,
    "autorizado": true
  }
}
```

## 🧪 Requisitos de prueba

### Casos de prueba funcional

### ✅ Caso 1: Entrenador crea una rutina — autorizado

- **Precondición:** Token válido de un ENTRENADOR (ej. `jwt_10_ENTRENADOR_token`).
- **Acción:** `POST /api/auth/validar-autorizacion`
```json
{ "token": "jwt_10_ENTRENADOR_token", "recurso": "rutinas", "accion": "CREAR" }
```
- **Resultado esperado:**
  - HTTP 200 OK
  - `success: true`
  - `autorizado: true`

### ✅ Caso 2: Entrenador edita una rutina — autorizado

- **Precondición:** Token válido de un ENTRENADOR.
- **Acción:** `POST /api/auth/validar-autorizacion`
```json
{ "token": "jwt_10_ENTRENADOR_token", "recurso": "rutinas", "accion": "EDITAR" }
```
- **Resultado esperado:**
  - HTTP 200 OK
  - `autorizado: true`

### ✅ Caso 3: Entrenador elimina una rutina — autorizado

- **Precondición:** Token válido de un ENTRENADOR.
- **Acción:** `POST /api/auth/validar-autorizacion`
```json
{ "token": "jwt_10_ENTRENADOR_token", "recurso": "rutinas", "accion": "ELIMINAR" }
```
- **Resultado esperado:**
  - HTTP 200 OK
  - `autorizado: true`

### ✅ Caso 4: Cliente ve una rutina — autorizado

- **Precondición:** Token válido de un CLIENTE (ej. `jwt_1_CLIENTE_token`).
- **Acción:** `POST /api/auth/validar-autorizacion`
```json
{ "token": "jwt_1_CLIENTE_token", "recurso": "rutinas", "accion": "VER" }
```
- **Resultado esperado:**
  - HTTP 200 OK
  - `autorizado: true`

### ✅ Caso 5: Cliente crea un pago — autorizado

- **Precondición:** Token válido de un CLIENTE.
- **Acción:** `POST /api/auth/validar-autorizacion`
```json
{ "token": "jwt_1_CLIENTE_token", "recurso": "pagos", "accion": "CREAR" }
```
- **Resultado esperado:**
  - HTTP 200 OK
  - `autorizado: true`

### ✅ Caso 6: Cliente se suscribe a un plan — autorizado

- **Precondición:** Token válido de un CLIENTE.
- **Acción:** `POST /api/auth/validar-autorizacion`
```json
{ "token": "jwt_1_CLIENTE_token", "recurso": "planes", "accion": "SUSCRIBIR" }
```
- **Resultado esperado:**
  - HTTP 200 OK
  - `autorizado: true`

### ❌ Caso 7: Cliente intenta crear una rutina — denegado

- **Precondición:** Token válido de un CLIENTE.
- **Acción:** `POST /api/auth/validar-autorizacion`
```json
{ "token": "jwt_1_CLIENTE_token", "recurso": "rutinas", "accion": "CREAR" }
```
- **Resultado esperado:**
  - HTTP 403 Forbidden
  - `success: false`
  - `error_code`: `AUTH_UNAUTHORIZED`
  - Mensaje: `"Acceso denegado"`

### ❌ Caso 8: Cliente intenta editar una rutina — denegado

- **Precondición:** Token válido de un CLIENTE.
- **Acción:** `POST /api/auth/validar-autorizacion`
```json
{ "token": "jwt_1_CLIENTE_token", "recurso": "rutinas", "accion": "EDITAR" }
```
- **Resultado esperado:**
  - HTTP 403 Forbidden
  - `error_code`: `AUTH_UNAUTHORIZED`

### ❌ Caso 9: Entrenador intenta crear un pago — denegado

- **Precondición:** Token válido de un ENTRENADOR.
- **Acción:** `POST /api/auth/validar-autorizacion`
```json
{ "token": "jwt_10_ENTRENADOR_token", "recurso": "pagos", "accion": "CREAR" }
```
- **Resultado esperado:**
  - HTTP 403 Forbidden
  - `error_code`: `AUTH_UNAUTHORIZED`
  - Mensaje: `"Acceso denegado"`

### ❌ Caso 10: Entrenador intenta suscribirse a un plan — denegado

- **Precondición:** Token válido de un ENTRENADOR.
- **Acción:** `POST /api/auth/validar-autorizacion`
```json
{ "token": "jwt_10_ENTRENADOR_token", "recurso": "planes", "accion": "SUSCRIBIR" }
```
- **Resultado esperado:**
  - HTTP 403 Forbidden
  - `error_code`: `AUTH_UNAUTHORIZED`

### ❌ Caso 11: Token inválido o expirado

- **Precondición:** El token JWT no tiene el formato esperado o ha caducado.
- **Acción:** `POST /api/auth/validar-autorizacion` con token inválido.
```json
{ "token": "token_invalido_xyz", "recurso": "rutinas", "accion": "VER" }
```
- **Resultado esperado:**
  - HTTP 401 Unauthorized
  - `error_code`: `AUTH_INVALID_CREDENTIALS`
  - Mensaje descriptivo indicando que el token no es válido

### ✅ Caso 12: Asignar rol a un usuario

- **Precondición:** El usuario existe en el sistema.
- **Acción:** `POST /api/auth/roles?id_usuario=5&rol=CLIENTE`
- **Resultado esperado:**
  - HTTP 200 OK
  - Perfil de permisos creado con el rol asignado

### ❌ Caso 13: Revocar acceso de usuario inexistente

- **Precondición:** El usuario con ese ID no tiene permisos registrados.
- **Acción:** `DELETE /api/auth/roles/{id_usuario}` con ID no existente.
- **Resultado esperado:**
  - HTTP 404 Not Found

### ✅ Caso 14: Listar usuarios por rol

- **Precondición:** Existen usuarios con el rol indicado.
- **Acción:** `GET /api/auth/roles/CLIENTE`
- **Resultado esperado:**
  - HTTP 200 OK
  - Lista de usuarios con rol CLIENTE

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] El endpoint valida correctamente el rol contra el recurso y la acción solicitada usando el mapa de permisos.
- [ ] Los clientes reciben HTTP 403 al intentar CREAR, EDITAR o ELIMINAR rutinas.
- [ ] Los entrenadores reciben HTTP 403 al intentar acceder a pagos o planes.
- [ ] Los tokens inválidos o con formato incorrecto retornan HTTP 401.
- [ ] La respuesta JSON cumple con el contrato definido.

### 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas unitarias para cada funcionalidad principal.
- [ ] Se cubrieron los casos de error y respuestas sin datos.
- [ ] Las pruebas funcionales están documentadas y pasadas.

### 📄 Documentación Técnica

- [ ] Endpoint documentado en Swagger / OpenAPI.
- [ ] Se describen campos de entrada y salida con ejemplos.
- [ ] La tabla de permisos por rol está documentada.

### 🔐 Manejo de Errores

- [ ] Se devuelve código HTTP 400 para parámetros inválidos.
- [ ] Se devuelve código HTTP 401 para token inválido o expirado.
- [ ] Se devuelve código HTTP 403 para acceso no autorizado por rol.
- [ ] Se devuelve código HTTP 500/503 ante fallos internos.
- [ ] El campo `message` incluye texto descriptivo y amigable.
