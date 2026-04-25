## [HU-01] Registro como cliente

### 📖 Historia de usuario

**Como** Cliente nuevo del gimnasio
**Quiero** Registrarme en FitZone con mis datos básicos 
**Para** poder acceder a la plataforma, buscar entrenadores y reservar sesiones de entrenamiento

## 🔁Flujo esperado

- El cliente completa el formulario de resgistro con nombre, correo electronico, teléfono y contraseña.
- El sistema consume el endpoint `POST /api/v1/auth/registro` con rol=CLIENTE.
- El backend valida que el correo no este registrado previamente.
- Se envía un correo de verfificación y el registro queda en estado PENDIENTE.
- El cliente verifica su correo y el estado cambia a ACTIVO.

## Criterios de aceptación

### 1.🔍 Estructura y lógica del servicio

- [ ] se expone un endpoint `POST /api/v1/auth/registro` que recibe nombre, correo, teléfono y contraseña.
- [ ] El sistema asigna automaticamente el rol CLIENTE al nuevo usuario.
- [ ] Se verifica que el correo electronico no este ya registrado.
 
### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON:

```json
{
  "success": true,
  "message": "Registro exitoso. Verifique su correo electrónico.",
  "data": {
    "idUsuario": 42,
    "nombre": "Juan Pérez",
    "rol": "CLIENTE",
    "estado": "PENDIENTE"
  }
}
```

- [ ] Si no se encuentra el usuario, se responde con un código 404 y el siguiente mensaje JSON:

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
        "rol": "CLIENTE"
      }
```

- [ ] Si el correo ya esta registrado, el backend retorna:
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

 - **Precondición**: El correo no exite en la base de datos.
 - **Accion**: `POST /api/v1/auth/registro` con datos complejos y válidos.
 - **Resultado Esperado**:
    - HTTP 201 Created
    - Campo success: true
    - Se retorna el idUsuario asignado 
    - Estado del usuario: PENDIENTE

### ❌ Caso 2: Correo ya registrado

 - **Precondición**: El correo ya existe en la base de datos.
 - **Accion**: `POST /api/v1/auth/registro` con el mismo correo electrónico.
 - **Resultado Esperado**:
    - HTTP 409 Conflict
    - Campo success: false
    - Message: El correo electrónico ya está registrado

### ❌ Caso 3: Campos obligatorios vacíos

 - **Precondición**: El body de la solicitud no contiene los campos requeridos.
 - **Accion**: `POST /api/v1/auth/registro` sin campos obligatorios.
 - **Resultado Esperado**:
    - HTTP 400 Bad Request
    - Mensajes descriptivo indicando el campo faltante.

## ✅ Definición de Hecho

## 📦 Alcance Funcional
 
 - [ ] El edpoint asigna correctamente el rol de cliente al nuevo usuario.
 - [ ] El corrreo duplicado retorna error 409 con mensaje claro.
 - [ ] El estado PENDIENTE se actualiza a ACTIVO al confirmar el correo.
 - [ ] La respuesta JSON cumple con el contrato definido.

## 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas unitarias para cada funcionalidad principal.
- [ ] Se Cubrieron los casos de error y respuestas sin datos.
- [ ] Las pruebas funcionales están documentadas y pasadas.

## 📄 Documentación Técnica

- [ ] Endpoint documentado en Swagger / OpenAPI.
- [ ] Se describen campos de entrada y salida con ejemplos.

## 🔐 Manejo de Errores

- [ ] Se devuelve código HTTP 400 para parámetros inválidos.
- [ ] Se devuelve código HTTP 401/403 para acceso no autorizado.
- [ ] Se devuelve código HTTP 500/503 ante fallos internos.
- [ ] El campo `mensaje` incluye texto descriptivo y amigable.

