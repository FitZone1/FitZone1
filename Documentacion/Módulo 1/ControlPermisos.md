# [HU-04] Control de permisos por rol

## 📖 Historia de usuario

**Como** Sistema de autorización de BlessedFit  
**Quiero** Controlar qué acciones puede realizar cada usuario según su rol (`CLIENTE` o `ENTRENADOR`)  
**Para** Garantizar que ningún usuario acceda a funciones que no le corresponden y mantener la seguridad de la plataforma

---

## 🔁 Flujo esperado

- El usuario realiza una solicitud a un endpoint protegido incluyendo su token JWT.
- El sistema consume el endpoint `POST /api/auth/validar-autorizacion` con el token, recurso y acción.
- El backend decodifica el token y extrae el `id_usuario` y `rol`.
- Se verifica que el usuario tenga un perfil de permisos registrado en el sistema.
- Se valida si el rol tiene permiso para ejecutar la acción sobre el recurso solicitado.
- Si tiene permiso, se retorna HTTP 200 con `autorizado: true`.
- Si no tiene permiso, se retorna HTTP 403 con mensaje `"Acceso denegado"`.
- Si el token es inválido o el usuario no tiene perfil registrado, se retorna HTTP 401.

---

## 🗺️ Mapa de permisos por rol

| Recurso | CLIENTE | ENTRENADOR |
|---|---|---|
| `rutinas` | `VER` | `CREAR`, `VER`, `EDITAR`, `ELIMINAR` |
| `pagos` | `CREAR`, `VER` | ❌ sin acceso |
| `planes` | `SUSCRIBIR`, `VER` | ❌ sin acceso |
| `reservas` | `CREAR`, `VER`, `CANCELAR` | `VER` |
| `perfil` | `VER`, `EDITAR` | `VER`, `EDITAR` |
| `clientes` | ❌ sin acceso | `VER` |
| `horarios` | ❌ sin acceso | `CREAR`, `VER`, `EDITAR` |

> **Nota:** El campo `accion` se normaliza automáticamente a mayúsculas y `recurso` a minúsculas antes de validar.

---

## ✅ Criterios de aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `POST /api/auth/validar-autorizacion` que recibe `token`, `recurso` y `accion`.
- [ ] El backend decodifica el token para extraer `id_usuario` y `rol`.
- [ ] El token inválido (no decodificable) retorna HTTP 401.
- [ ] El usuario sin perfil de permisos registrado retorna HTTP 401.
- [ ] El backend valida el rol contra el mapa de permisos para el recurso y acción solicitados.
- [ ] Los clientes **NO** pueden `CREAR`, `EDITAR` ni `ELIMINAR` rutinas.
- [ ] Los entrenadores **NO** pueden acceder a `pagos` ni `planes`.
- [ ] Se expone `POST /api/auth/roles` para asignar o actualizar el rol de un usuario.
- [ ] Se expone `DELETE /api/auth/roles/{id_usuario}` para revocar todos los permisos de un usuario.
- [ ] Se expone `GET /api/auth/roles/{rol}` para listar usuarios por rol.

### 2. 📋 Estructura de la información

Respuesta exitosa de `POST /api/auth/validar-autorizacion`:

```json
{
  "idUsuario": 42,
  "autorizado": true
}
```

Respuesta de error por permiso denegado (HTTP 403):

```json
{
  "detail": "Acceso denegado"
}
```

Respuesta de error por token inválido o usuario sin perfil (HTTP 401):

```json
{
  "detail": "El token no es válido o ha expirado"
}
```

Respuesta de error por parámetros inválidos (HTTP 422):

```json
{
  "detail": [
    {
      "loc": ["body", "accion"],
      "msg": "ensure this value has at least 2 characters",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

Respuesta de `POST /api/auth/roles` exitoso:

```json
{
  "mensaje": "Rol 'CLIENTE' asignado correctamente al usuario 42"
}
```

Respuesta de `DELETE /api/auth/roles/{id_usuario}` exitoso:

```json
{
  "mensaje": "Acceso revocado para el usuario 42"
}
```

---

## 🔧 Notas Técnicas

| Endpoint | Método | Descripción |
|---|---|---|
| `/api/auth/validar-autorizacion` | `POST` | Valida si el token tiene permiso para recurso + acción |
| `/api/auth/roles` | `POST` | Asigna o actualiza el rol de un usuario |
| `/api/auth/roles/{id_usuario}` | `DELETE` | Revoca todos los permisos de un usuario |
| `/api/auth/roles/{rol}` | `GET` | Lista todos los usuarios con un rol específico |

**Campos de entrada para `/api/auth/validar-autorizacion`:**

| Campo | Tipo | Regla |
|---|---|---|
| `token` | string | JWT generado en el login |
| `recurso` | string (min 2 chars) | Se normaliza a minúsculas automáticamente |
| `accion` | string (min 2 chars) | Se normaliza a mayúsculas automáticamente |

---

## 🧪 Casos de prueba funcional

---

### ✅ Caso 1: Entrenador crea una rutina — acceso autorizado

- **Precondición:** Usuario con rol `ENTRENADOR` tiene perfil registrado y token válido.
- **Acción:** `POST /api/auth/validar-autorizacion` con token de ENTRENADOR, `recurso: "rutinas"`, `accion: "CREAR"`.
- **Resultado esperado:**
  - HTTP 200 OK
  - `autorizado: true`
  - `idUsuario` presente en la respuesta

---

### ✅ Caso 2: Cliente ve sus rutinas — acceso autorizado

- **Precondición:** Usuario con rol `CLIENTE` tiene perfil registrado y token válido.
- **Acción:** `POST /api/auth/validar-autorizacion` con token de CLIENTE, `recurso: "rutinas"`, `accion: "VER"`.
- **Resultado esperado:**
  - HTTP 200 OK
  - `autorizado: true`

---

### ❌ Caso 3: Cliente intenta crear una rutina — acceso denegado

- **Precondición:** Usuario con rol `CLIENTE` tiene perfil registrado y token válido.
- **Acción:** `POST /api/auth/validar-autorizacion` con token de CLIENTE, `recurso: "rutinas"`, `accion: "CREAR"`.
- **Resultado esperado:**
  - HTTP 403 Forbidden
  - Mensaje: `"Acceso denegado"`

---

### ❌ Caso 4: Entrenador intenta realizar un pago — acceso denegado

- **Precondición:** Usuario con rol `ENTRENADOR` tiene perfil registrado y token válido.
- **Acción:** `POST /api/auth/validar-autorizacion` con token de ENTRENADOR, `recurso: "pagos"`, `accion: "CREAR"`.
- **Resultado esperado:**
  - HTTP 403 Forbidden
  - Mensaje: `"Acceso denegado"`

---

### ❌ Caso 5: Entrenador intenta suscribirse a un plan — acceso denegado

- **Precondición:** Usuario con rol `ENTRENADOR` tiene perfil registrado y token válido.
- **Acción:** `POST /api/auth/validar-autorizacion` con token de ENTRENADOR, `recurso: "planes"`, `accion: "SUSCRIBIR"`.
- **Resultado esperado:**
  - HTTP 403 Forbidden
  - Mensaje: `"Acceso denegado"`

---

### ❌ Caso 6: Cliente intenta ver la lista de clientes — acceso denegado

- **Precondición:** Usuario con rol `CLIENTE` tiene perfil registrado y token válido.
- **Acción:** `POST /api/auth/validar-autorizacion` con token de CLIENTE, `recurso: "clientes"`, `accion: "VER"`.
- **Resultado esperado:**
  - HTTP 403 Forbidden
  - Mensaje: `"Acceso denegado"`

---

### ❌ Caso 7: Token inválido (no decodificable)

- **Precondición:** El token enviado no cumple el formato esperado.
- **Acción:** `POST /api/auth/validar-autorizacion` con token malformado (ej: `"tokenbasura"`).
- **Resultado esperado:**
  - HTTP 401 Unauthorized
  - Mensaje: `"El token no es válido o ha expirado"`

---

### ❌ Caso 8: Usuario sin perfil de permisos registrado

- **Precondición:** El token es decodificable pero el `id_usuario` no tiene perfil en el repositorio de permisos.
- **Acción:** `POST /api/auth/validar-autorizacion` con token de un usuario no registrado en el sistema de permisos.
- **Resultado esperado:**
  - HTTP 401 Unauthorized
  - Mensaje: `"El token no es válido o ha expirado"`

> ⚠️ **Regla de negocio:** El sistema trata igual un token malformado y un usuario sin perfil registrado — ambos retornan HTTP 401 con el mismo mensaje, para no revelar información sobre qué existe en el sistema.

---

### ✅ Caso 9: Asignación de rol exitosa

- **Precondición:** Se quiere asignar o actualizar el rol de un usuario.
- **Acción:** `POST /api/auth/roles?id_usuario=42&rol=CLIENTE`
- **Resultado esperado:**
  - HTTP 200 OK
  - Mensaje: `"Rol 'CLIENTE' asignado correctamente al usuario 42"`

---

### ❌ Caso 10: Asignación de rol inválido

- **Precondición:** El rol enviado no es `CLIENTE` ni `ENTRENADOR`.
- **Acción:** `POST /api/auth/roles?id_usuario=42&rol=ADMIN`
- **Resultado esperado:**
  - HTTP 400 Bad Request
  - Mensaje descriptivo indicando que el rol no es válido

---

### ✅ Caso 11: Revocación de acceso exitosa

- **Precondición:** El usuario tiene perfil de permisos registrado.
- **Acción:** `DELETE /api/auth/roles/42`
- **Resultado esperado:**
  - HTTP 200 OK
  - Mensaje: `"Acceso revocado para el usuario 42"`

---

### ❌ Caso 12: Revocación de usuario inexistente

- **Precondición:** El `id_usuario` no tiene perfil en el repositorio.
- **Acción:** `DELETE /api/auth/roles/999`
- **Resultado esperado:**
  - HTTP 404 Not Found
  - Mensaje descriptivo indicando que no existe perfil para ese usuario

---

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] El endpoint valida correctamente el rol contra el recurso y la acción usando el mapa de permisos.
- [ ] Los clientes reciben HTTP 403 al intentar `CREAR`, `EDITAR` o `ELIMINAR` rutinas.
- [ ] Los entrenadores reciben HTTP 403 al intentar acceder a `pagos` o `planes`.
- [ ] Los tokens inválidos y los usuarios sin perfil retornan HTTP 401 con el mismo mensaje genérico.
- [ ] La asignación de roles valida que el rol sea `CLIENTE` o `ENTRENADOR`.
- [ ] La revocación de acceso retorna HTTP 404 si el usuario no existe.
- [ ] La respuesta JSON cumple con el contrato definido (sin wrapper `success/data`).

### 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas unitarias para cada funcionalidad principal.
- [ ] Se cubrieron los casos de error y respuestas sin datos.
- [ ] Las pruebas funcionales están documentadas y pasadas (Casos 1 al 12).

### 📄 Documentación Técnica

- [ ] Los cuatro endpoints documentados en Swagger / OpenAPI.
- [ ] Se documenta el mapa de permisos por rol con todos los recursos y acciones.
- [ ] Se describen campos de entrada y salida con ejemplos.

### 🔐 Manejo de Errores

- [ ] Se devuelve HTTP 422 para parámetros con formato inválido (campos vacíos o muy cortos).
- [ ] Se devuelve HTTP 401 para token inválido o usuario sin perfil registrado.
- [ ] Se devuelve HTTP 403 para acceso denegado por rol insuficiente.
- [ ] Se devuelve HTTP 400 para rol no válido en asignación.
- [ ] Se devuelve HTTP 404 para revocación de usuario inexistente.
- [ ] Se devuelve HTTP 500/503 ante fallos internos.
- [ ] El campo `detail` incluye texto descriptivo y amigable.
