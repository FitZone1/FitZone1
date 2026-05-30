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

## Criterios de aceptación  

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `POST /api/auth/validar-autorizacion` que recibe token, recurso y acción.
- [ ] El backend valida el rol del token contra los permisos requeridos para el recurso.
- [ ] Los clientes NO pueden crear ni modificar rutinas.
- [ ] Los entrenadores NO pueden realizar pagos ni suscribirse a planes.

### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON cuando el acceso es autorizado:

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

- [ ] Si el rol no tiene permisos para la acción solicitada, el backend retorna:

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

## 🔧 Notas Técnicas

- **Método HTTP:** `POST`
- **Ruta:** `/api/auth/validar-autorizacion`

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

- [ ] Si el token es inválido o está expirado, el backend retorna:

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

## 🧪 Requisitos de prueba

### Casos de prueba funcional

### ✅ Caso 1: Acceso autorizado correctamente

- **Precondición:** El usuario está autenticado con token válido y tiene permisos para el recurso.
- **Acción:** `POST /api/auth/validar-autorizacion` con token de ENTRENADOR, recurso `rutinas` y acción `CREAR`.
- **Resultado esperado:**
  - HTTP 200 OK
  - Campo `success: true`
  - Campo `autorizado: true`

### ❌ Caso 2: Cliente intenta crear una rutina

- **Precondición:** Usuario autenticado con rol CLIENTE.
- **Acción:** `POST /api/auth/validar-autorizacion` con token de CLIENTE, recurso `rutinas` y acción `CREAR`.
- **Resultado esperado:**
  - HTTP 403 Forbidden
  - Campo `success: false`
  - `error_code`: `AUTH_UNAUTHORIZED`
  - Mensaje: `"Acceso denegado"`

### ❌ Caso 3: Token inválido o expirado

- **Precondición:** El token JWT no es válido o ha caducado.
- **Acción:** `POST /api/auth/validar-autorizacion` con token inválido.
- **Resultado esperado:**
  - HTTP 401 Unauthorized
  - `error_code`: `AUTH_INVALID_CREDENTIALS`
  - Mensaje descriptivo indicando que el token no es válido

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] El endpoint valida correctamente el rol contra el recurso y la acción solicitada.
- [ ] Los clientes reciben HTTP 403 al intentar acceder a recursos de entrenador.
- [ ] Los tokens inválidos o expirados retornan HTTP 401 con mensaje claro.
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