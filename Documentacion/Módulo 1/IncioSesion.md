# [HU-03] Inicio de sesión

## 📖 Historia de usuario

**Como** Cliente o entrenador del gimnasio  
**Quiero** Iniciar sesión en BlessedFit con mi correo electrónico y contraseña  
**Para** Recibir mi token de acceso JWT y poder utilizar todas las funciones de la plataforma según mi rol

---

## 🔁 Flujo esperado

- El usuario ingresa su correo electrónico y contraseña en el formulario de login.
- El sistema consume el endpoint `POST /api/auth/login` con correo y contraseña.
- El backend busca al usuario primero como **CLIENTE** y luego como **ENTRENADOR**.
- Se verifica que el usuario tenga estado **ACTIVO** antes de continuar.
- Si las credenciales son válidas, se genera y retorna un token JWT con el rol del usuario.
- El token se usa en las solicitudes subsiguientes para autenticación y autorización.
- El usuario puede cerrar sesión mediante `POST /api/auth/logout`, invalidando el token.
- Se puede consultar la sesión activa mediante `GET /api/auth/sesion`.

---

## ✅ Criterios de aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `POST /api/auth/login` que recibe correo y contraseña.
- [ ] El backend valida formato del correo (debe cumplir patrón `email@dominio.ext`).
- [ ] El backend busca al usuario primero como CLIENTE y luego como ENTRENADOR.
- [ ] Solo se permite el inicio de sesión si el usuario tiene estado **ACTIVO**.
- [ ] El backend valida las credenciales y genera un token JWT con el rol del usuario.
- [ ] El token incluye el rol del usuario (`CLIENTE` o `ENTRENADOR`).
- [ ] Las credenciales incorrectas retornan HTTP 401 con mensaje descriptivo.
- [ ] Un usuario con estado distinto a ACTIVO recibe HTTP 401 con mensaje `"Credenciales incorrectas"`.
- [ ] Se expone un endpoint `POST /api/auth/logout` que invalida el token activo.
- [ ] Se expone un endpoint `GET /api/auth/sesion` que retorna los datos de la sesión activa.

### 2. 📋 Estructura de la información

Respuesta exitosa de `POST /api/auth/login`:

```json
{
  "idUsuario": 42,
  "nombre": "Juan Pérez",
  "rol": "CLIENTE",
  "token": "jwt_42_CLIENTE_token"
}
```

Respuesta de error (credenciales incorrectas, usuario no encontrado, o usuario INACTIVO):

```json
{
  "detail": "Credenciales incorrectas"
}
```

> **Nota:** El backend unifica el mensaje `"Credenciales incorrectas"` para los casos de correo no registrado, contraseña incorrecta y usuario INACTIVO. Esto es intencional para no revelar cuál campo falló.

Respuesta de error por formato de correo inválido (HTTP 422):

```json
{
  "detail": [
    {
      "loc": ["body", "correo"],
      "msg": "El correo electrónico no tiene un formato válido",
      "type": "value_error"
    }
  ]
}
```

Respuesta de `POST /api/auth/logout` exitoso:

```json
{
  "mensaje": "Sesión cerrada correctamente"
}
```

Respuesta de `GET /api/auth/sesion` con token válido:

```json
{
  "idUsuario": 42,
  "nombre": "Juan Pérez",
  "rol": "CLIENTE",
  "token": "jwt_42_CLIENTE_token"
}
```

---

## 🔧 Notas Técnicas

| Endpoint | Método | Descripción |
|---|---|---|
| `/api/auth/login` | `POST` | Autentica al usuario y retorna token JWT con rol |
| `/api/auth/logout` | `POST` | Invalida el token activo del usuario |
| `/api/auth/sesion` | `GET` | Retorna los datos de la sesión activa por token |

---

## 🧪 Casos de prueba funcional

---

### ✅ Caso 1: Inicio de sesión exitoso como cliente

- **Precondición:** El usuario existe en la base de datos con estado `ACTIVO` y rol `CLIENTE`.
- **Acción:** `POST /api/auth/login` con correo y contraseña válidos de un cliente.
- **Resultado esperado:**
  - HTTP 200 OK
  - Token JWT presente en la respuesta
  - Campo `rol` con valor `CLIENTE`
  - La sesión queda registrada internamente en el repositorio

---

### ✅ Caso 2: Inicio de sesión exitoso como entrenador

- **Precondición:** El entrenador existe en la base de datos con estado `ACTIVO` y rol `ENTRENADOR`.
- **Acción:** `POST /api/auth/login` con correo y contraseña válidos de un entrenador.
- **Resultado esperado:**
  - HTTP 200 OK
  - Token JWT presente en la respuesta
  - Campo `rol` con valor `ENTRENADOR`

---

### ❌ Caso 3: Contraseña incorrecta

- **Precondición:** El usuario existe con estado `ACTIVO`, pero la contraseña enviada es incorrecta.
- **Acción:** `POST /api/auth/login` con correo válido y contraseña errónea.
- **Resultado esperado:**
  - HTTP 401 Unauthorized
  - Mensaje: `"Credenciales incorrectas"`

---

### ❌ Caso 4: Correo no registrado

- **Precondición:** El correo enviado no existe ni en la tabla de clientes ni en la de entrenadores.
- **Acción:** `POST /api/auth/login` con correo no registrado.
- **Resultado esperado:**
  - HTTP 401 Unauthorized
  - Mensaje: `"Credenciales incorrectas"`

---

### ❌ Caso 5: Usuario con estado INACTIVO

- **Precondición:** El usuario existe en la base de datos pero su campo `estado` es distinto de `ACTIVO` (por ejemplo: `INACTIVO`, `SUSPENDIDO`).
- **Acción:** `POST /api/auth/login` con correo y contraseña correctos del usuario inactivo.
- **Resultado esperado:**
  - HTTP 401 Unauthorized
  - Mensaje: `"Credenciales incorrectas"`
  - **No se genera token** ni se registra sesión

> ⚠️ **Regla de negocio crítica:** El sistema verifica el estado del usuario **después** de validar las credenciales. Aunque el correo y la contraseña sean correctos, un usuario inactivo no puede iniciar sesión.

---

### ❌ Caso 6: Correo con formato inválido

- **Precondición:** El correo enviado no cumple el formato `email@dominio.ext`.
- **Acción:** `POST /api/auth/login` con correo malformado (ej: `"usuariosindominio"`, `"@dominio.com"`).
- **Resultado esperado:**
  - HTTP 422 Unprocessable Entity
  - Mensaje de validación: `"El correo electrónico no tiene un formato válido"`

---

### ✅ Caso 7: Cierre de sesión exitoso

- **Precondición:** El usuario tiene una sesión activa con token válido.
- **Acción:** `POST /api/auth/logout` con el token activo.
- **Resultado esperado:**
  - HTTP 200 OK
  - Mensaje: `"Sesión cerrada correctamente"`
  - El token queda invalidado; una consulta posterior con ese token debe retornar HTTP 401

---

### ❌ Caso 8: Cierre de sesión con token inválido o ya cerrado

- **Precondición:** El token no existe en el repositorio de sesiones (nunca fue generado o ya fue cerrado).
- **Acción:** `POST /api/auth/logout` con token inválido o expirado.
- **Resultado esperado:**
  - HTTP 401 Unauthorized
  - Mensaje: `"Token inválido o sesión ya cerrada"`

---

### ✅ Caso 9: Consulta de sesión activa

- **Precondición:** El usuario tiene una sesión activa con token válido.
- **Acción:** `GET /api/auth/sesion?token=<token_valido>`
- **Resultado esperado:**
  - HTTP 200 OK
  - Retorna `idUsuario`, `nombre`, `rol` y `token` de la sesión

---

### ❌ Caso 10: Consulta de sesión con token inválido

- **Precondición:** El token no existe o ya fue cerrado.
- **Acción:** `GET /api/auth/sesion?token=<token_invalido>`
- **Resultado esperado:**
  - HTTP 401 Unauthorized
  - Mensaje: `"Token inválido o expirado"`

---

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] El token JWT se genera correctamente con el rol del usuario incluido.
- [ ] Solo usuarios con estado `ACTIVO` pueden iniciar sesión.
- [ ] Las credenciales incorrectas, el usuario no encontrado y el usuario INACTIVO retornan HTTP 401 con el mismo mensaje genérico.
- [ ] El correo con formato inválido retorna HTTP 422 con mensaje de validación.
- [ ] La sesión es diferenciada correctamente por rol entre `CLIENTE` y `ENTRENADOR`.
- [ ] El endpoint de logout invalida el token correctamente.
- [ ] El endpoint de consulta de sesión retorna los datos asociados al token.
- [ ] La respuesta JSON cumple con el contrato definido.

### 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas unitarias para cada funcionalidad principal.
- [ ] Se cubrieron los casos de error y respuestas sin datos.
- [ ] Las pruebas funcionales están documentadas y pasadas (Casos 1 al 10).

### 📄 Documentación Técnica

- [ ] Los tres endpoints documentados en Swagger / OpenAPI.
- [ ] Se describen campos de entrada y salida con ejemplos.

### 🔐 Manejo de Errores

- [ ] Se devuelve código HTTP 422 para parámetros con formato inválido.
- [ ] Se devuelve código HTTP 401 para credenciales incorrectas, usuario inactivo y token inválido.
- [ ] Se devuelve código HTTP 500/503 ante fallos internos.
- [ ] El campo `detail` incluye texto descriptivo y amigable.
