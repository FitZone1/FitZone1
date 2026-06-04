## [HU-03] Inicio de sesión

### 📖 Historia de usuario

**Como** Cliente o entrenador del gimnasio
**Quiero** Iniciar sesión en FitZone con mi correo electrónico y contraseña
**Para** Recibir mi token de acceso JWT y poder utilizar todas las funciones de la plataforma según mi rol

## 🔁 Flujo esperado

- El usuario ingresa su correo electrónico y contraseña en el formulario de login.
- El sistema consume el endpoint `POST /api/auth/login` con correo y contraseña.
- El backend busca el correo primero entre los clientes y luego entre los entrenadores.
- Si las credenciales son válidas y el usuario tiene estado ACTIVO, se genera y retorna un token JWT con el rol del usuario.
- Si el usuario existe pero su estado no es ACTIVO, se rechaza el acceso con HTTP 401.
- El token se usa en las solicitudes subsiguientes para autenticación y autorización.

## Criterios de aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `POST /api/auth/login` que recibe correo y contraseña.
- [ ] El backend busca el correo primero en clientes y luego en entrenadores.
- [ ] El backend valida las credenciales y genera un token JWT con el rol del usuario.
- [ ] El token incluye el rol del usuario (CLIENTE o ENTRENADOR).
- [ ] Solo los usuarios con estado ACTIVO pueden iniciar sesión.
- [ ] Las credenciales incorrectas o usuario inactivo retornan HTTP 401 con mensaje descriptivo.
- [ ] Se expone un endpoint `POST /api/auth/logout` que invalida el token activo del usuario.
- [ ] Se expone un endpoint `GET /api/auth/sesion` que retorna los datos de la sesión activa por correo.

### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON:

```json
{
  "success": true,
  "message": "Inicio de sesión exitoso",
  "data": {
    "idUsuario": 42,
    "nombre": "Juan Pérez",
    "rol": "CLIENTE",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

- [ ] Si las credenciales son incorrectas, el backend retorna:

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

- [ ] Si el usuario existe pero no tiene estado ACTIVO, el backend retorna:

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
- **Ruta:** `/api/auth/login`

## 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "message": "Inicio de sesión exitoso",
  "data": {
    "idUsuario": 42,
    "nombre": "Juan Pérez",
    "rol": "CLIENTE",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

- [ ] Si el token es inválido o la sesión expiró, el backend retorna:

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

### ✅ Caso 1: Inicio de sesión exitoso como cliente

- **Precondición:** El usuario existe en la base de datos con estado ACTIVO.
- **Acción:** `POST /api/auth/login` con correo y contraseña válidos de un cliente.
- **Body de ejemplo:**
```json
{ "correo": "juan@fitzone.com", "contrasena": "pass_1" }
```
- **Resultado esperado:**
  - HTTP 200 OK
  - Campo `success: true`
  - Token JWT presente en la respuesta
  - Campo `rol` con valor `CLIENTE`

### ✅ Caso 2: Inicio de sesión exitoso como entrenador

- **Precondición:** El entrenador existe en la base de datos con estado ACTIVO.
- **Acción:** `POST /api/auth/login` con correo y contraseña válidos de un entrenador.
- **Body de ejemplo:**
```json
{ "correo": "carlos@fitzone.com", "contrasena": "pass_1" }
```
- **Resultado esperado:**
  - HTTP 200 OK
  - Campo `success: true`
  - Token JWT presente en la respuesta
  - Campo `rol` con valor `ENTRENADOR`

### ❌ Caso 3: Contraseña incorrecta

- **Precondición:** El usuario existe pero la contraseña enviada es incorrecta.
- **Acción:** `POST /api/auth/login` con correo válido y contraseña errónea.
- **Body de ejemplo:**
```json
{ "correo": "juan@fitzone.com", "contrasena": "incorrecta" }
```
- **Resultado esperado:**
  - HTTP 401 Unauthorized
  - Campo `success: false`
  - `error_code`: `AUTH_INVALID_CREDENTIALS`
  - Mensaje: `"Credenciales incorrectas"`

### ❌ Caso 4: Correo no registrado

- **Precondición:** El correo enviado no existe ni en clientes ni en entrenadores.
- **Acción:** `POST /api/auth/login` con correo no registrado.
- **Body de ejemplo:**
```json
{ "correo": "noexiste@fitzone.com", "contrasena": "cualquiera" }
```
- **Resultado esperado:**
  - HTTP 401 Unauthorized
  - Campo `success: false`
  - `error_code`: `AUTH_INVALID_CREDENTIALS`
  - Mensaje: `"Credenciales incorrectas"`

### ❌ Caso 5: Cliente con estado INACTIVO intenta iniciar sesión

- **Precondición:** El cliente existe en la base de datos pero su estado es INACTIVO.
- **Acción:** `POST /api/auth/login` con correo y contraseña correctos del cliente inactivo.
- **Resultado esperado:**
  - HTTP 401 Unauthorized
  - Campo `success: false`
  - `error_code`: `AUTH_INVALID_CREDENTIALS`
  - Mensaje: `"Credenciales incorrectas"`

### ✅ Caso 6: Cerrar sesión correctamente

- **Precondición:** El usuario tiene una sesión activa con token válido.
- **Acción:** `POST /api/auth/logout` con el token de la sesión activa.
- **Resultado esperado:**
  - HTTP 200 OK
  - Mensaje confirmando que la sesión fue cerrada.
  - El token queda invalidado y no puede usarse nuevamente.

### ❌ Caso 7: Cerrar sesión con token inexistente

- **Precondición:** El token enviado no corresponde a ninguna sesión activa.
- **Acción:** `POST /api/auth/logout` con token no registrado.
- **Resultado esperado:**
  - HTTP 401 Unauthorized
  - Mensaje descriptivo indicando que el token no es válido.

### ✅ Caso 8: Obtener sesión activa por correo

- **Precondición:** El usuario tiene una sesión activa.
- **Acción:** `GET /api/auth/sesion?token=jwt_{idUsuario}_{ROL}_token`
- **Resultado esperado:**
  - HTTP 200 OK
  - Datos de la sesión: idUsuario, nombre, rol y token.

### ❌ Caso 9: Obtener sesión con token inválido

- **Precondición:** El token enviado no corresponde a ninguna sesión activa.
- **Acción:** `GET /api/auth/sesion?token=token_invalido`
- **Resultado esperado:**
  - HTTP 401 Unauthorized
  - Mensaje descriptivo indicando que el token no es válido o la sesión expiró.

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] El token JWT se genera correctamente con el rol del usuario incluido.
- [ ] Las credenciales incorrectas retornan HTTP 401 con mensaje claro.
- [ ] Los usuarios con estado diferente de ACTIVO no pueden iniciar sesión.
- [ ] La sesión es diferenciada correctamente por rol entre CLIENTE y ENTRENADOR.
- [ ] El logout invalida el token correctamente.
- [ ] La consulta de sesión activa retorna los datos correctos o 401 si el token no existe.
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
- [ ] Se devuelve código HTTP 401 para credenciales incorrectas o usuario inactivo.
- [ ] Se devuelve código HTTP 500/503 ante fallos internos.
- [ ] El campo `mensaje` incluye texto descriptivo y amigable.
