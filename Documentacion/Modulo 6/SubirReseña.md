## [HU-19] Subir reseña al entrenador

### 📖 Historia de usuario

**Como** Cliente del gimnasio
**Quiero** Dejar mi opinión y calificación sobre el entrenador después de completar una sesión confirmada
**Para** Ayudar a otros clientes a elegir al entrenador más adecuado para sus objetivos y contribuir a la mejora del servicio

## 🔁 Flujo esperado

- El cliente accede a la sesión completada en su historial.
- El cliente escribe su comentario y asigna una calificación del 1 al 5.
- El sistema consume el endpoint `POST /api/resenas` con idCliente, idEntrenador, idReserva, calificacion y comentario.
- El backend valida que el cliente haya completado y confirmado una sesión con ese entrenador.
- La reseña se registra y el promedio de calificación del entrenador se recalcula automáticamente.

## Criterios de aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `POST /api/resenas` que recibe idCliente, idEntrenador, idReserva, calificacion y comentario.
- [ ] Solo se puede dejar reseña si el cliente tiene una sesión en estado COMPLETADA con ese entrenador.
- [ ] La calificación debe ser un valor entero entre 1 y 5.
- [ ] El promedio de calificación del entrenador se recalcula automáticamente tras cada reseña registrada.

### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON:

```json
{
  "success": true,
  "message": "Reseña registrada correctamente",
  "data": {
    "idResena": 56,
    "calificacion": 5,
    "calificacionPromedio": 4.8
  }
}
```

- [ ] Si el cliente no completó una sesión con ese entrenador, el backend retorna:

```json
{
  "success": false,
  "statusCode": 403,
  "message": "Reseña no permitida",
  "error": {
    "error_code": "SES_REVIEW_NOT_ALLOWED",
    "details": "Solo puedes dejar una reseña si completaste y confirmaste la sesión",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

## 🔧 Notas Técnicas

- **Método HTTP:** `POST`
- **Ruta:** `/api/resenas`

## 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "message": "Reseña registrada correctamente",
  "data": {
    "idResena": 56,
    "calificacion": 5,
    "calificacionPromedio": 4.8
  }
}
```

- [ ] Si la sesión no fue completada ni confirmada, el backend retorna:

```json
{
  "success": false,
  "statusCode": 403,
  "message": "Reseña no permitida",
  "error": {
    "error_code": "SES_REVIEW_NOT_ALLOWED",
    "details": "Solo puedes dejar una reseña si completaste y confirmaste la sesión",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

## 🧪 Requisitos de prueba

### Casos de prueba funcional

### ✅ Caso 1: Reseña exitosa tras sesión completada

- **Precondición:** El cliente tiene una sesión en estado COMPLETADA con el entrenador indicado.
- **Acción:** `POST /api/resenas` con idCliente, idEntrenador, idReserva, calificacion=5 y comentario válido.
- **Resultado esperado:**
  - HTTP 201 Created
  - Campo `success: true`
  - `idResena` generado correctamente
  - `calificacionPromedio` del entrenador recalculado automáticamente

### ✅ Caso 2: Reseña sin comentario opcional

- **Precondición:** El cliente tiene sesión completada y envía solo la calificación sin comentario.
- **Acción:** `POST /api/resenas` con calificacion=4 y sin campo comentario.
- **Resultado esperado:**
  - HTTP 201 Created
  - Campo `success: true`
  - Reseña registrada correctamente solo con calificación

### ❌ Caso 3: Cliente sin sesión completada con el entrenador

- **Precondición:** El cliente no tiene sesiones en estado COMPLETADA con el entrenador indicado.
- **Acción:** `POST /api/resenas` con idEntrenador de un entrenador con quien no se completó sesión.
- **Resultado esperado:**
  - HTTP 403 Forbidden
  - Campo `success: false`
  - `error_code`: `SES_REVIEW_NOT_ALLOWED`
  - Mensaje: `"Reseña no permitida"`

### ❌ Caso 4: Calificación fuera del rango válido

- **Precondición:** El cliente envía una calificación fuera del rango permitido.
- **Acción:** `POST /api/resenas` con calificacion=6.
- **Resultado esperado:**
  - HTTP 400 Bad Request
  - Campo `success: false`
  - Mensaje descriptivo indicando que la calificación debe estar entre 1 y 5

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] Solo se aceptan reseñas de clientes con sesión en estado COMPLETADA.
- [ ] El promedio de calificación del entrenador se recalcula automáticamente tras cada reseña.
- [ ] La calificación se valida en el rango 1 a 5.
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