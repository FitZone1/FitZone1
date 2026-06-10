## [HU-16] Consultar rutinas del día

### 📖 Historia de usuario

**Como** Cliente o entrenador del gimnasio
**Quiero** Consultar la rutina asignada para el día de hoy
**Para** Conocer los ejercicios que se realizarán en la sesión y llegar preparado sin depender de que el entrenador los explique desde cero

## 🔁 Flujo esperado

- El cliente o entrenador accede a la sección de rutinas en la plataforma.
- El sistema consume el endpoint `GET /api/rutinas/hoy?idEntrenador=10` con el token del usuario autenticado.
- El backend consulta la rutina asignada para el día actual según el entrenador indicado.
- Se retorna la rutina con el detalle completo de ejercicios, series y repeticiones.

## Criterios de aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `GET /api/rutinas/hoy` que acepta el parámetro `?idEntrenador=`.
- [ ] Se retorna la rutina asignada al día actual de la semana para el entrenador indicado.
- [ ] Cada ejercicio incluye nombre, series y repeticiones.
- [ ] Si no hay rutina asignada para el día actual, se retorna error descriptivo.
- [ ] El parámetro `idEntrenador` es obligatorio; su ausencia debe retornar error de validación.

### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON:

```json
{
  "success": true,
  "message": "Rutina del día obtenida correctamente",
  "data": {
    "idRutina": 24,
    "nombre": "Rutina Full Body Semana 1",
    "diaSemana": "LUNES",
    "ejercicios": [
      { "nombre": "Sentadilla", "series": 4, "repeticiones": 12 },
      { "nombre": "Press banca", "series": 3, "repeticiones": 10 }
    ]
  }
}
```

- [ ] Si no hay rutina asignada para el día de hoy, el backend retorna:

```json
{
  "success": false,
  "statusCode": 404,
  "message": "Sin rutina asignada",
  "error": {
    "error_code": "RUT_NO_DAILY_ROUTINE",
    "details": "No hay rutina asignada para el día de hoy",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

## 🔧 Notas Técnicas

- **Método HTTP:** `GET`
- **Ruta:** `/api/rutinas/hoy?idEntrenador=10`
- El día actual se determina en el backend según la fecha del servidor al momento de la consulta.

## 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "message": "Rutina del día obtenida correctamente",
  "data": {
    "idRutina": 24,
    "nombre": "Rutina Full Body Semana 1",
    "diaSemana": "LUNES",
    "ejercicios": [
      { "nombre": "Sentadilla", "series": 4, "repeticiones": 12 },
      { "nombre": "Press banca", "series": 3, "repeticiones": 10 }
    ]
  }
}
```

## 🧪 Requisitos de prueba

### Casos de prueba funcional

### ✅ Caso 1: Consulta exitosa de rutina del día

- **Precondición:** El entrenador tiene una rutina asignada para el día actual de la semana.
- **Acción:** `GET /api/rutinas/hoy?idEntrenador=10` con token válido.
- **Resultado esperado:**
  - HTTP 200 OK
  - Campo `success: true`
  - Rutina retornada con nombre, `diaSemana` y lista de ejercicios completa
  - Cada ejercicio incluye nombre, series y repeticiones

### ✅ Caso 2: Consulta de rutina por entrenador específico sin mezclar rutinas de otros

- **Precondición:** Existen varios entrenadores con rutinas asignadas para el día actual.
- **Acción:** `GET /api/rutinas/hoy?idEntrenador=10` con token de cliente válido.
- **Resultado esperado:**
  - HTTP 200 OK
  - Solo se retorna la rutina del entrenador con idEntrenador=10
  - No se incluyen rutinas de otros entrenadores en la respuesta

### ❌ Caso 3: Sin rutina asignada para el día actual

- **Precondición:** El entrenador no tiene rutina asignada para el día de hoy.
- **Acción:** `GET /api/rutinas/hoy?idEntrenador=10` en un día sin rutina asignada.
- **Resultado esperado:**
  - HTTP 404 Not Found
  - Campo `success: false`
  - `error_code`: `RUT_NO_DAILY_ROUTINE`
  - Mensaje: `"Sin rutina asignada"`

### ❌ Caso 4: Entrenador no encontrado

- **Precondición:** El idEntrenador enviado no existe en la base de datos.
- **Acción:** `GET /api/rutinas/hoy?idEntrenador=999`
- **Resultado esperado:**
  - HTTP 404 Not Found
  - Campo `success: false`
  - `error_code`: `TRAINER_NOT_FOUND`
  - Mensaje descriptivo indicando que el entrenador no existe

### ❌ Caso 5: Parámetro `idEntrenador` ausente en la solicitud

- **Precondición:** El usuario está autenticado.
- **Acción:** `GET /api/rutinas/hoy` sin el parámetro `idEntrenador`.
- **Resultado esperado:**
  - HTTP 422 Unprocessable Entity
  - Mensaje de validación indicando que `idEntrenador` es un parámetro requerido

### ❌ Caso 6: `idEntrenador` con valor cero, negativo o no numérico

- **Precondición:** El usuario está autenticado.
- **Acción:** `GET /api/rutinas/hoy?idEntrenador=0` o `GET /api/rutinas/hoy?idEntrenador=abc`.
- **Resultado esperado:**
  - HTTP 422 Unprocessable Entity
  - Mensaje de validación indicando que `idEntrenador` debe ser un entero mayor a `0`

### ❌ Caso 7: Solicitud sin token de autenticación

- **Precondición:** No se envía header de autenticación.
- **Acción:** `GET /api/rutinas/hoy?idEntrenador=10` sin header `Authorization`.
- **Resultado esperado:**
  - HTTP 401 Unauthorized
  - Campo `success: false`
  - `error_code`: `AUTH_MISSING_TOKEN`
  - Mensaje: `"Token de autenticación requerido"`

### ✅ Caso 8: Cliente consulta rutina del día exitosamente

- **Precondición:** Usuario autenticado con rol CLIENTE y el entrenador tiene rutina asignada para hoy.
- **Acción:** `GET /api/rutinas/hoy?idEntrenador=10` con token de cliente válido.
- **Resultado esperado:**
  - HTTP 200 OK
  - Campo `success: true`
  - Rutina retornada con lista completa de ejercicios

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] La rutina del día se retorna correctamente con el detalle de ejercicios.
- [ ] Solo se muestra la rutina del entrenador indicado en el parámetro.
- [ ] El error 404 se retorna correctamente cuando no hay rutina asignada para el día.
- [ ] El error 404 se retorna correctamente cuando el entrenador no existe.
- [ ] Las solicitudes sin token reciben HTTP 401.
- [ ] La respuesta JSON cumple con el contrato definido.

### 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas unitarias para cada funcionalidad principal.
- [ ] Se cubrieron los casos de error y respuestas sin datos.
- [ ] Las pruebas funcionales están documentadas y pasadas.

### 📄 Documentación Técnica

- [ ] Endpoint documentado en Swagger / OpenAPI.
- [ ] Se describen campos de entrada y salida con ejemplos.

### 🔐 Manejo de Errores

- [ ] Se devuelve código HTTP 401 para solicitudes sin token.
- [ ] Se devuelve código HTTP 404 para rutina o entrenador no encontrado.
- [ ] Se devuelve código HTTP 422 para parámetros ausentes o con formato inválido.
- [ ] Se devuelve código HTTP 500/503 ante fallos internos.
- [ ] El campo `mensaje` incluye texto descriptivo y amigable.