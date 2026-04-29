## [HU-20] Ver reseñas y calificaciones del entrenador

### 📖 Historia de usuario

**Como** Cliente del gimnasio
**Quiero** Ver las reseñas y la calificación promedio de cada entrenador antes de reservar una sesión
**Para** Tomar una decisión informada sobre qué entrenador contratar basándome en la experiencia real de otros clientes del gimnasio

## 🔁 Flujo esperado

- El cliente accede al perfil de un entrenador o al listado general de entrenadores.
- El sistema consume el endpoint `GET /api/resenas?idEntrenador=10` con el token del cliente.
- El backend consulta todas las reseñas válidas asociadas al entrenador indicado.
- Se retorna la calificación promedio, el total de reseñas y la lista de comentarios de clientes reales.

## Criterios de aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `GET /api/resenas` que acepta el parámetro `?idEntrenador=`.
- [ ] Solo se muestran reseñas de clientes que hayan completado sesiones reales con ese entrenador.
- [ ] La calificación promedio se calcula en base a todas las reseñas válidas registradas.
- [ ] Las reseñas se retornan ordenadas por fecha descendente.

### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON:

```json
{
  "success": true,
  "message": "Reseñas obtenidas correctamente",
  "data": {
    "idEntrenador": 10,
    "calificacionPromedio": 4.8,
    "totalResenas": 24,
    "resenas": [
      {
        "idResena": 56,
        "idCliente": 42,
        "calificacion": 5,
        "comentario": "Excelente entrenador, muy puntual y profesional",
        "fecha": "2026-03-20T17:00:00"
      }
    ]
  }
}
```

- [ ] Si el entrenador no tiene reseñas registradas, el backend retorna:

```json
{
  "success": false,
  "statusCode": 404,
  "message": "Sin reseñas",
  "error": {
    "error_code": "SES_NO_REVIEWS_FOUND",
    "details": "Este entrenador aún no tiene reseñas registradas",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

## 🔧 Notas Técnicas

- **Método HTTP:** `GET`
- **Ruta:** `/api/resenas?idEntrenador=10`

## 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "message": "Reseñas obtenidas correctamente",
  "data": {
    "idEntrenador": 10,
    "calificacionPromedio": 4.8,
    "totalResenas": 24,
    "resenas": [
      {
        "idResena": 56,
        "idCliente": 42,
        "calificacion": 5,
        "comentario": "Excelente entrenador, muy puntual y profesional",
        "fecha": "2026-03-20T17:00:00"
      }
    ]
  }
}
```

- [ ] Si el entrenador aún no tiene reseñas, el backend retorna:

```json
{
  "success": false,
  "statusCode": 404,
  "message": "Sin reseñas",
  "error": {
    "error_code": "SES_NO_REVIEWS_FOUND",
    "details": "Este entrenador aún no tiene reseñas registradas",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

## 🧪 Requisitos de prueba

### Casos de prueba funcional

### ✅ Caso 1: Consulta exitosa de reseñas

- **Precondición:** El entrenador tiene reseñas válidas registradas por clientes con sesiones completadas.
- **Acción:** `GET /api/resenas?idEntrenador=10` con token de cliente válido.
- **Resultado esperado:**
  - HTTP 200 OK
  - Campo `success: true`
  - `calificacionPromedio` calculado correctamente
  - Lista de reseñas con calificación, comentario y fecha
  - `totalResenas` refleja el número correcto de reseñas

### ✅ Caso 2: Consulta de calificación promedio actualizada

- **Precondición:** El entrenador acaba de recibir una nueva reseña.
- **Acción:** `GET /api/resenas?idEntrenador=10` inmediatamente después de registrar la reseña.
- **Resultado esperado:**
  - HTTP 200 OK
  - `calificacionPromedio` ya refleja el nuevo valor recalculado
  - `totalResenas` incrementado en uno

### ❌ Caso 3: Entrenador sin reseñas registradas

- **Precondición:** El entrenador no tiene reseñas aún.
- **Acción:** `GET /api/resenas?idEntrenador=10` con entrenador sin reseñas.
- **Resultado esperado:**
  - HTTP 404 Not Found
  - Campo `success: false`
  - `error_code`: `SES_NO_REVIEWS_FOUND`
  - Mensaje: `"Sin reseñas"`

### ❌ Caso 4: Entrenador no encontrado

- **Precondición:** El idEntrenador enviado no existe en la base de datos.
- **Acción:** `GET /api/resenas?idEntrenador=999`
- **Resultado esperado:**
  - HTTP 404 Not Found
  - Campo `success: false`
  - Mensaje descriptivo indicando que el entrenador no existe

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] El promedio de calificación se calcula correctamente con las reseñas válidas.
- [ ] Solo se muestran reseñas de sesiones reales completadas.
- [ ] Las reseñas se retornan ordenadas por fecha descendente.
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