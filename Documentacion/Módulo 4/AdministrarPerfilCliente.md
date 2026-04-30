## [HU-12] Administrar perfil del cliente

### 📖 Historia de usuario

**Como** Cliente del gimnasio
**Quiero** Crear y mantener actualizado mi perfil con mis datos personales, objetivos de entrenamiento y foto
**Para** Que el entrenador conozca mi información antes de cada sesión y pueda personalizar mejor el entrenamiento

## 🔁 Flujo esperado

- El cliente accede a la sección "Mi perfil" en la plataforma.
- El sistema consume el endpoint `PUT /api/perfiles/cliente/42` con los datos actualizados.
- El backend valida que el cliente exista y actualiza la información.
- Los cambios quedan guardados y visibles para el entrenador asignado.

## Criterios de aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `PUT /api/perfiles/cliente/{idCliente}` que recibe nombre, teléfono, objetivos y pesoActual.
- [ ] Se expone un endpoint `PATCH /api/perfiles/42/foto` para actualizar la foto de perfil.
- [ ] Se expone un endpoint `POST /api/perfiles/42/objetivos` para registrar objetivos y peso meta.
- [ ] Solo el cliente autenticado puede modificar su propio perfil.

### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON al actualizar el perfil:

```json
{
  "success": true,
  "message": "Perfil actualizado correctamente",
  "data": {
    "idCliente": 15,
    "nombre": "Angela Shilel",
    "objetivos": "Bajar de peso y ganar masa muscular",
    "pesoActual": 68.5
  }
}
```

- [ ] Si el cliente no existe, el backend retorna:

```json
{
  "success": false,
  "statusCode": 404,
  "message": "Cliente no encontrado",
  "error": {
    "error_code": "PROF_CLIENT_NOT_FOUND",
    "details": "No existe un cliente con el ID proporcionado",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

## 🔧 Notas Técnicas

- **Método HTTP:** `PUT` para actualizar perfil / `PATCH` para foto / `POST` para objetivos
- **Ruta perfil:** `/api/perfiles/cliente/{idCliente}`
- **Ruta foto:** `/api/perfiles/42/foto`
- **Ruta objetivos:** `/api/perfiles/42/objetivos`

## 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "message": "Perfil actualizado correctamente",
  "data": {
    "idCliente": 15,
    "nombre": "Angela Shilel",
    "objetivos": "Bajar de peso y ganar masa muscular",
    "pesoActual": 68.5
  }
}
```

- [ ] Si el formato de la foto no es permitido, el backend retorna:

```json
{
  "success": false,
  "statusCode": 400,
  "message": "Formato no permitido",
  "error": {
    "error_code": "PROF_INVALID_IMAGE_FORMAT",
    "details": "Solo se permiten imágenes en formato JPG o PNG",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

## 🧪 Requisitos de prueba

### Casos de prueba funcional

### ✅ Caso 1: Actualización exitosa del perfil

- **Precondición:** El cliente está autenticado y tiene perfil registrado.
- **Acción:** `PUT /api/perfiles/cliente/42` con nombre, teléfono, objetivos y pesoActual válidos.
- **Resultado esperado:**
  - HTTP 200 OK
  - Campo `success: true`
  - Datos actualizados reflejados en la respuesta
  - Información visible para el entrenador asignado

### ✅ Caso 2: Registro exitoso de objetivos

- **Precondición:** El cliente está autenticado y envía objetivos con plazo válido.
- **Acción:** `POST /api/perfiles/42/objetivos` con objetivos, pesoMeta y plazoMeses válidos.
- **Resultado esperado:**
  - HTTP 201 Created
  - Campo `success: true`
  - Objetivos registrados correctamente con pesoMeta y plazoMeses

### ❌ Caso 3: Cliente no encontrado

- **Precondición:** El idCliente enviado no existe en la base de datos.
- **Acción:** `PUT /api/perfiles/cliente/999` con id inexistente.
- **Resultado esperado:**
  - HTTP 404 Not Found
  - Campo `success: false`
  - `error_code`: `PROF_CLIENT_NOT_FOUND`
  - Mensaje: `"Cliente no encontrado"`

### ❌ Caso 4: Formato de foto no permitido

- **Precondición:** El cliente intenta subir una imagen en formato no permitido.
- **Acción:** `PATCH /api/perfiles/42/foto` con imagen en formato GIF.
- **Resultado esperado:**
  - HTTP 400 Bad Request
  - Campo `success: false`
  - `error_code`: `PROF_INVALID_IMAGE_FORMAT`
  - Mensaje: `"Formato no permitido"`

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] Los datos del perfil se actualizan correctamente y son visibles para el entrenador.
- [ ] La foto de perfil se valida por formato antes de guardar.
- [ ] Los objetivos se registran correctamente con pesoMeta y plazoMeses.
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