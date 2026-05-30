## [HU-11] Procesar planes de suscripción

### 📖 Historia de usuario

**Como** Cliente del gimnasio
**Quiero** Consultar, seleccionar y suscribirme a un plan de membresía disponible en la plataforma
**Para** Acceder al nivel de servicio que mejor se ajuste a mis necesidades y presupuesto

## 🔁 Flujo esperado

- El cliente accede a la sección de planes en la plataforma.
- El sistema consume el endpoint `GET /api/pagos/planes` para listar los planes disponibles.
- El cliente selecciona un plan y confirma la suscripción.
- El sistema consume el endpoint `POST /api/pagos/planes/suscribir` con idCliente e idPlan.
- El backend valida que el plan exista y esté activo en el sistema.
- La suscripción queda activa con su fecha de vigencia y el cliente puede comenzar a reservar sesiones.

## Criterios de aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `GET /api/pagos/planes` que retorna todos los planes activos con nombre, monto y duración.
- [ ] Se expone un endpoint `POST /api/pagos/planes/suscribir` que recibe idCliente e idPlan.
- [ ] Solo puede haber un plan activo por cliente a la vez.
- [ ] El plan seleccionado debe existir y estar activo en el sistema.

### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON al consultar planes:

```json
{
  "success": true,
  "message": "Planes obtenidos correctamente",
  "data": [
    {
      "idPlan": 1,
      "nombre": "Plan Básico",
      "monto": 55000,
      "duracionDias": 30
    },
    {
      "idPlan": 2,
      "nombre": "Plan Mensual Premium",
      "monto": 85000,
      "duracionDias": 30
    }
  ]
}
```

- [ ] Se responde con la siguiente estructura en JSON al suscribirse a un plan:

```json
{
  "success": true,
  "message": "Suscripción activada correctamente",
  "data": {
    "idSuscripcion": 99,
    "idCliente": 42,
    "plan": "Plan Mensual Premium",
    "monto": 85000,
    "vigencia": "2026-04-18"
  }
}
```

- [ ] Si el plan seleccionado no existe o fue dado de baja, el backend retorna:

```json
{
  "success": false,
  "statusCode": 404,
  "message": "Plan no disponible",
  "error": {
    "error_code": "PAY_PLAN_NOT_FOUND",
    "details": "El plan seleccionado no existe o fue dado de baja",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

## 🔧 Notas Técnicas

- **Método HTTP:** `GET` para consultar planes / `POST` para suscribirse
- **Ruta consulta:** `/api/pagos/planes`
- **Ruta suscripción:** `/api/pagos/planes/suscribir`

## 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "message": "Suscripción activada correctamente",
  "data": {
    "idSuscripcion": 99,
    "idCliente": 42,
    "plan": "Plan Mensual Premium",
    "monto": 85000,
    "vigencia": "2026-04-18"
  }
}
```

- [ ] Si no hay planes activos en el sistema, el backend retorna:

```json
{
  "success": false,
  "statusCode": 404,
  "message": "Sin planes disponibles",
  "error": {
    "error_code": "PAY_NO_PLANS_FOUND",
    "details": "No hay planes de suscripción activos en el sistema",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

## 🧪 Requisitos de prueba

### Casos de prueba funcional

### ✅ Caso 1: Consulta exitosa de planes disponibles

- **Precondición:** Existen planes activos registrados en el sistema.
- **Acción:** `GET /api/pagos/planes` con token de cliente válido.
- **Resultado esperado:**
  - HTTP 200 OK
  - Campo `success: true`
  - Lista de planes con nombre, monto y duración
  - Al menos un plan retornado en la respuesta

### ✅ Caso 2: Suscripción exitosa a un plan

- **Precondición:** El plan existe y está activo en el sistema.
- **Acción:** `POST /api/pagos/planes/suscribir` con idCliente e idPlan válidos.
- **Resultado esperado:**
  - HTTP 201 Created
  - Campo `success: true`
  - `idSuscripcion` generado correctamente
  - Campo `vigencia` con la fecha de vencimiento del plan

### ❌ Caso 3: Plan no disponible

- **Precondición:** El idPlan enviado no existe o fue dado de baja.
- **Acción:** `POST /api/pagos/planes/suscribir` con idPlan inexistente.
- **Resultado esperado:**
  - HTTP 404 Not Found
  - Campo `success: false`
  - `error_code`: `PAY_PLAN_NOT_FOUND`
  - Mensaje: `"Plan no disponible"`

### ❌ Caso 4: Sin planes activos en el sistema

- **Precondición:** No hay planes de suscripción activos registrados.
- **Acción:** `GET /api/pagos/planes` con token válido.
- **Resultado esperado:**
  - HTTP 404 Not Found
  - Campo `success: false`
  - `error_code`: `PAY_NO_PLANS_FOUND`
  - Mensaje: `"Sin planes disponibles"`

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] Los planes se listan correctamente con nombre, monto y duración.
- [ ] La suscripción se activa correctamente con fecha de vigencia calculada.
- [ ] Solo existe un plan activo por cliente a la vez.
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