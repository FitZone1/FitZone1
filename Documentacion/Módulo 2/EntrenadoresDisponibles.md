## [HU-05] Ver entrenadores disponibles

### 📖 Historia de usuario

**Como** Cliente del gimnasio
**Quiero** Ver en tiempo real la lista de entrenadores disponibles en mi gimnasio, con su especialidad y calificación
**Para** Elegir al entrenador más adecuado para mis objetivos antes de reservar una sesión

## 🔁 Flujo esperado

- El cliente accede a la sección de entrenadores en la plataforma.
- El sistema consume el endpoint `GET /api/reservas/entrenadores?especialidad=Musculación&disponible=true` con el token del cliente.
- El backend consulta los entrenadores con disponibilidad activa y retorna la lista con nombre, especialidad y calificación.
- El cliente puede filtrar por especialidad o buscar por nombre.

## Criterios de aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `GET /api/reservas/entrenadores` que acepta parámetros de filtro `?especialidad=` y `?disponible=`.
- [ ] Solo se retornan entrenadores con `disponible: true`.
- [ ] La calificación promedio se calcula en base a las reseñas válidas registradas.

### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON:

```json
{
  "success": true,
  "message": "Entrenadores encontrados correctamente",
  "data": [
    {
      "idEntrenador": 10,
      "nombre": "Carlos Villamizar",
      "especialidad": "Musculación",
      "calificacion": 4.8,
      "disponible": true
    }
  ]
}
```

- [ ] Si no se encuentran entrenadores con los filtros seleccionados, el backend retorna:

```json
{
  "success": false,
  "statusCode": 404,
  "message": "Sin resultados",
  "error": {
    "error_code": "RES_TRAINERS_NOT_FOUND",
    "details": "No se encontraron entrenadores con los filtros seleccionados",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

## 🔧 Notas Técnicas

- **Método HTTP:** `GET`
- **Ruta:** `/api/reservas/entrenadores?especialidad=Musculación&disponible=true`

## 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "message": "Entrenadores encontrados correctamente",
  "data": [
    {
      "idEntrenador": 10,
      "nombre": "Carlos Villamizar",
      "especialidad": "Musculación",
      "calificacion": 4.8,
      "disponible": true
    }
  ]
}
```

- [ ] Si no hay entrenadores disponibles, el backend retorna:

```json
{
  "success": false,
  "statusCode": 404,
  "message": "Sin resultados",
  "error": {
    "error_code": "RES_TRAINERS_NOT_FOUND",
    "details": "No se encontraron entrenadores con los filtros seleccionados",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

## 🧪 Requisitos de prueba

### Casos de prueba funcional

### ✅ Caso 1: Consulta exitosa de entrenadores disponibles

- **Precondición:** Existen entrenadores con disponibilidad activa registrada.
- **Acción:** `GET /api/reservas/entrenadores?disponible=true` con token de cliente válido.
- **Resultado esperado:**
  - HTTP 200 OK
  - Campo `success: true`
  - Lista de entrenadores con nombre, especialidad y calificación
  - Solo aparecen entrenadores con `disponible: true`

### ✅ Caso 2: Filtro por especialidad

- **Precondición:** Existen entrenadores registrados con distintas especialidades.
- **Acción:** `GET /api/reservas/entrenadores?especialidad=Musculación&disponible=true`
- **Resultado esperado:**
  - HTTP 200 OK
  - Solo se retornan entrenadores cuya especialidad es `"Musculación"`

### ❌ Caso 3: Sin entrenadores disponibles con los filtros aplicados

- **Precondición:** Ningún entrenador coincide con los filtros enviados.
- **Acción:** `GET /api/reservas/entrenadores?especialidad=Yoga&disponible=true`
- **Resultado esperado:**
  - HTTP 404 Not Found
  - Campo `success: false`
  - `error_code`: `RES_TRAINERS_NOT_FOUND`
  - Mensaje: `"Sin resultados"`

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] La lista solo incluye entrenadores con disponibilidad activa.
- [ ] El filtro por especialidad funciona correctamente.
- [ ] La calificación promedio se refleja correctamente en cada entrenador.
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