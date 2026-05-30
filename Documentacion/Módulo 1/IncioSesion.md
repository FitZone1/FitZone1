## [HU-03] Inicio de sesión

### 📖 Historia de usuario

**Como** Cliente o entrenador del gimnasio
**Quiero** Iniciar sesión en FitZone con mi correo electrónico y contraseña
**Para** Recibir mi token de acceso JWT y poder utilizar todas las funciones de la plataforma según mi rol

## 🔁 Flujo esperado

- El usuario ingresa su correo electrónico y contraseña en el formulario de login.
- El sistema consume el endpoint `POST /api/auth/login` con correo y contraseña.
- El backend valida las credenciales contra la base de datos.
- Si son válidas, se genera y retorna un token JWT con el rol del usuario.
- El token se usa en las solicitudes subsiguientes para autenticación y autorización.

## Criterios de aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `POST /api/auth/login` que recibe correo y contraseña.
- [ ] El backend valida las credenciales y genera un token JWT con el rol del usuario.
- [ ] El token incluye el rol del usuario (CLIENTE o ENTRENADOR).
- [ ] Las credenciales incorrectas retornan HTTP 401 con mensaje descriptivo.

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
- **Resultado esperado:**
  - HTTP 200 OK
  - Campo `success: true`
  - Token JWT presente en la respuesta
  - Campo `rol` con valor `CLIENTE`

### ✅ Caso 2: Inicio de sesión exitoso como entrenador

- **Precondición:** El entrenador existe en la base de datos con estado ACTIVO.
- **Acción:** `POST /api/auth/login` con correo y contraseña válidos de un entrenador.
- **Resultado esperado:**
  - HTTP 200 OK
  - Campo `success: true`
  - Token JWT presente en la respuesta
  - Campo `rol` con valor `ENTRENADOR`

### ❌ Caso 3: Contraseña incorrecta

- **Precondición:** El usuario existe pero la contraseña enviada es incorrecta.
- **Acción:** `POST /api/auth/login` con correo válido y contraseña errónea.
- **Resultado esperado:**
  - HTTP 401 Unauthorized
  - Campo `success: false`
  - `error_code`: `AUTH_INVALID_CREDENTIALS`
  - Mensaje: `"Credenciales incorrectas"`

### ❌ Caso 4: Correo no registrado

- **Precondición:** El correo enviado no existe en la base de datos.
- **Acción:** `POST /api/auth/login` con correo no registrado.
- **Resultado esperado:**
  - HTTP 401 Unauthorized
  - Campo `success: false`
  - `error_code`: `AUTH_INVALID_CREDENTIALS`
  - Mensaje: `"Credenciales incorrectas"`

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] El token JWT se genera correctamente con el rol del usuario incluido.
- [ ] Las credenciales incorrectas retornan HTTP 401 con mensaje claro.
- [ ] La sesión es diferenciada correctamente por rol entre CLIENTE y ENTRENADOR.
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