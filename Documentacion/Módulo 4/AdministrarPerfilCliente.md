## [HU-12] Administrar perfil del cliente

### 📖 Historia de usuario

**Como** Cliente del gimnasio
**Quiero** Ver y mantener actualizado mi perfil con mis datos personales y objetivos de entrenamiento
**Para** Que el entrenador conozca mi información antes de cada sesión y pueda personalizar mejor el entrenamiento

## 🔁 Flujo esperado

- El cliente accede a la sección "Mi perfil" en la plataforma.
- El sistema consume el endpoint `GET /api/perfiles/{idUsuario}` para ver los datos actuales.
- El cliente puede actualizar su nombre y teléfono con `PUT /api/perfiles/cliente/{idUsuario}`.
- El cliente puede registrar sus objetivos de entrenamiento con `POST /api/perfiles/{idUsuario}/objetivos`.
- El backend valida que el cliente exista y actualiza la información.
- Los cambios quedan guardados y visibles para el entrenador asignado.

## Criterios de aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `GET /api/perfiles/{idUsuario}` para ver el perfil del cliente.
- [ ] Se expone un endpoint `PUT /api/perfiles/cliente/{idUsuario}` que recibe nombre y teléfono.
- [ ] Se expone un endpoint `POST /api/perfiles/{idUsuario}/objetivos` para registrar objetivos, pesoMeta y plazoMeses.
- [ ] Solo el cliente autenticado puede modificar su propio perfil.

### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON al ver el perfil:

```json
{
  "success": true,
  "message": "Perfil obtenido correctamente",
  "data": {
    "idUsuario": 1,
    "nombre": "Juan Pérez",
    "correo": "juan@fitzone.com",
    "telefono": "3001234567",
    "objetivos": "",
    "pesoActual": 0.0
  }
}
```

- [ ] Se responde con la siguiente estructura en JSON al actualizar el perfil:

```json
{
  "success": true,
  "message": "Perfil actualizado correctamente",
  "data": {
    "idUsuario": 1,
    "nombre": "Juan Pérez",
    "correo": "juan@fitzone.com",
    "telefono": "3001234567",
    "objetivos": "Bajar de peso y ganar masa muscular",
    "pesoActual": 68.5
  }
}
```

- [ ] Se responde con la siguiente estructura en JSON al registrar objetivos:

```json
{
  "success": true,
  "message": "Objetivos registrados correctamente",
  "data": {
    "idUsuario": 1,
    "objetivos": "Bajar de peso y ganar masa muscular",
    "pesoMeta": 65.0,
    "plazoMeses": 6
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

- **Método HTTP:** `GET` para ver perfil / `PUT` para actualizar perfil / `POST` para objetivos
- **Ruta ver perfil:** `/api/perfiles/{idUsuario}`
- **Ruta actualizar perfil:** `/api/perfiles/cliente/{idUsuario}`
- **Ruta objetivos:** `/api/perfiles/{idUsuario}/objetivos`

## 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "message": "Perfil obtenido correctamente",
  "data": {
    "idUsuario": 1,
    "nombre": "Juan Pérez",
    "correo": "juan@fitzone.com",
    "telefono": "3001234567",
    "objetivos": "",
    "pesoActual": 0.0
  }
}
```

## 🧪 Requisitos de prueba

### Casos de prueba funcional

### ✅ Caso 1: Ver perfil del cliente

- **Precondición:** Existe el cliente con idUsuario=1 (incluido en el seed inicial).
- **Acción:** `GET /api/perfiles/1`
- **Resultado esperado:**
  - HTTP 200 OK
  - Campo `success: true`
  - Datos del perfil: `idUsuario`, `nombre`, `correo`, `telefono`

### ✅ Caso 2: Actualización exitosa del perfil

- **Precondición:** Existe el cliente con idUsuario=1 (incluido en el seed inicial).
- **Acción:** `PUT /api/perfiles/cliente/1` con nombre y teléfono válidos.
- **Resultado esperado:**
  - HTTP 200 OK
  - Campo `success: true`
  - Datos actualizados reflejados en la respuesta

### ✅ Caso 3: Registro exitoso de objetivos

- **Precondición:** Existe el cliente con idUsuario=1 (incluido en el seed inicial).
- **Acción:** `POST /api/perfiles/1/objetivos` con objetivos, pesoMeta y plazoMeses válidos.
- **Resultado esperado:**
  - HTTP 201 Created
  - Campo `success: true`
  - Objetivos registrados correctamente con pesoMeta y plazoMeses

### ❌ Caso 4: Cliente no encontrado

- **Precondición:** No existe ningún cliente con idUsuario=999.
- **Acción:** `GET /api/perfiles/999`
- **Resultado esperado:**
  - HTTP 404 Not Found
  - `error_code`: `PROF_CLIENT_NOT_FOUND`
  - `message`: `"Cliente no encontrado"`

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] El perfil del cliente se obtiene correctamente con nombre, correo y teléfono.
- [ ] Los datos del perfil se actualizan correctamente y son visibles para el entrenador.
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
- [ ] Se devuelve código HTTP 404 cuando el cliente no existe.
- [ ] Se devuelve código HTTP 500/503 ante fallos internos.
- [ ] El campo `message` incluye texto descriptivo y amigable.