## [HU-02] Registro como entrenador

## 📖 Historia de Usuario

**Como** entrenador del gimnasio
**Quiero** registrarme en la plataforma con mis datos personales y profesionales
**Para** que los clientes del gimnasio puedan encontrarme, ver mi perfil y reservar sesiones de entrenamiento conmigo.

## 🔁 Flujo Esperado

- El entrenador completa el formulario de registro con nombre, correo, contraseña y especialidades.
- El sistema consume el endpoint `POST /api/v1/auth/registro` con rol=ENTRENADOR.
- El backend valida los datos y crea el perfil del entrenador.
- El perfil queda visible en el listado de entrenadores una vez completado y activo.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

 - [ ] Se expone un endpoint `POST /api/v1/entrenadores` con los datos del entrenador.
 - [ ] El sistema asigna automáticamente el rol ENTRENADOR.
 - [ ] Se registran las especialidades del entrenador.

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
        "rol": "ENTRENADOR"
      }
    },
```

- [ ] Si el correo ya esta registrado, el backend retorna:
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
**Acción:** `POST /api/v1/entrenadores` con datos válidos y especialidades.
**Resultado Esperado:**
    - HTTP 201 Created
    - Campo success: true
    - Rol asignado: ENTRENADOR
    - Especialidades registradas correctamente

### ❌ Caso 2: Correo duplicado

**Precondición:** El correo ya está en uso.
**Acción:** `POST /api/v1/entrenadores` con correo existente.
**Resultado Esperado:**
    - HTTP 409 Conflict
    - Mensaje: "El correo electrónico ya está registrado."

## ✅ Definición de Hecho

## 📦 Alcance Funcional

 - [ ] El endpoint asigna correctamente el rol ENTRENADOR.
 - [ ] Las especialidades se guardan asociadas al perfil del entrenador.
 - [ ] El perfil es visible en el listado al estar activo.

## 🧪 Pruebas Completadas

 - [ ] Se ejecutaron pruebas unitarias para la funcionalidad principal.
 - [ ] Se cubrieron los casos de error y respuesta sin datos.
 - [ ] Las pruebas funcionales están documentadas y pasadas.

## 📄 Documentación Técnica

 - [ ] Endpoint documentado en Swagger / OpenAPI.
 - [ ] Se describen campos de entrada y salida con ejemplos.

## 🔐 Manejo de Errores

 - [ ] Se devuelve código HTTP 400 para parámetros inválidos.
 - [ ] Se devuelve código HTTP 401/403 para acceso no autorizado.
 - [ ] Se devuelve código HTTP 500/503 ante fallos internos.
 - [ ] El campo mensaje incluye texto descriptivo y amigable.