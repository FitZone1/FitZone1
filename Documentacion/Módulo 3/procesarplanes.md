## [HU-11] Gestionar planes de suscripción

### 📖 Historia de usuario

**Como** Administrador del gimnasio
**Quiero** Crear, consultar, actualizar y eliminar los planes de membresía disponibles en la plataforma
**Para** Mantener actualizado el catálogo de planes que los clientes pueden adquirir al momento de pagar su mensualidad

## 🔁 Flujo esperado

- El administrador accede a la sección de gestión de planes.
- Puede listar todos los planes activos e inactivos del sistema.
- Puede crear un nuevo plan con nombre, monto y duración en días.
- Puede consultar el detalle de un plan específico por su ID.
- Puede actualizar los datos de un plan existente.
- Puede eliminar (dar de baja) un plan cuando ya no esté disponible.
- Los planes activos son visibles para los clientes al momento de realizar el pago de mensualidad.

> **Nota:** La suscripción de un cliente a un plan se gestiona en el flujo de **Pago de Mensualidad** (`POST /api/pagos`), no en este módulo.

## Criterios de aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone `GET /api/pagos/planes` para listar todos los planes (activos e inactivos).
- [ ] Se expone `GET /api/pagos/planes/{idPlan}` para obtener el detalle de un plan por ID.
- [ ] Se expone `POST /api/pagos/planes` para crear un nuevo plan.
- [ ] Se expone `PUT /api/pagos/planes/{idPlan}` para actualizar un plan existente.
- [ ] Se expone `DELETE /api/pagos/planes/{idPlan}` para eliminar (dar de baja) un plan.
- [ ] No se puede eliminar un plan que tenga suscripciones activas asociadas.
- [ ] El `monto` debe ser mayor a 0 y la `duracionDias` debe ser mayor a 0.

### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura al listar planes:

```json
{
  "success": true,
  "message": "Planes obtenidos correctamente",
  "data": [
    {
      "idPlan": 1,
      "nombre": "Plan Básico",
      "monto": 55000,
      "duracionDias": 30,
      "activo": true
    },
    {
      "idPlan": 2,
      "nombre": "Plan Mensual Premium",
      "monto": 85000,
      "duracionDias": 30,
      "activo": true
    }
  ]
}
```

- [ ] Se responde con la siguiente estructura al obtener un plan por ID:

```json
{
  "success": true,
  "message": "Plan obtenido correctamente",
  "data": {
    "idPlan": 1,
    "nombre": "Plan Básico",
    "monto": 55000,
    "duracionDias": 30,
    "activo": true
  }
}
```

- [ ] Se responde con la siguiente estructura al crear un plan:

```json
{
  "success": true,
  "message": "Plan creado correctamente",
  "data": {
    "idPlan": 3,
    "nombre": "Plan Trimestral",
    "monto": 200000,
    "duracionDias": 90,
    "activo": true
  }
}
```

- [ ] Se responde con la siguiente estructura al actualizar un plan:

```json
{
  "success": true,
  "message": "Plan actualizado correctamente",
  "data": {
    "idPlan": 1,
    "nombre": "Plan Básico Actualizado",
    "monto": 60000,
    "duracionDias": 30,
    "activo": true
  }
}
```

- [ ] Se responde con la siguiente estructura al eliminar un plan:

```json
{
  "success": true,
  "message": "Plan eliminado correctamente",
  "data": {
    "idPlan": 1,
    "activo": false
  }
}
```

- [ ] Si el plan no existe, el backend retorna:

```json
{
  "success": false,
  "statusCode": 404,
  "message": "Plan no encontrado",
  "error": {
    "error_code": "PAY_PLAN_NOT_FOUND",
    "details": "No existe un plan con el ID proporcionado",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

- [ ] Si se intenta eliminar un plan con suscripciones activas, el backend retorna:

```json
{
  "success": false,
  "statusCode": 409,
  "message": "Plan con suscripciones activas",
  "error": {
    "error_code": "PAY_PLAN_HAS_ACTIVE_SUBSCRIPTIONS",
    "details": "No se puede eliminar un plan que tiene suscripciones activas asociadas",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

- [ ] Si no hay planes registrados, el backend retorna:

```json
{
  "success": false,
  "statusCode": 404,
  "message": "Sin planes disponibles",
  "error": {
    "error_code": "PAY_NO_PLANS_FOUND",
    "details": "No hay planes de suscripción registrados en el sistema",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

## 🔧 Notas Técnicas

- **Ruta base:** `/api/pagos/planes`
- `GET    /api/pagos/planes`           → Listar todos los planes
- `GET    /api/pagos/planes/{idPlan}`  → Obtener plan por ID
- `POST   /api/pagos/planes`           → Crear plan
- `PUT    /api/pagos/planes/{idPlan}`  → Actualizar plan
- `DELETE /api/pagos/planes/{idPlan}`  → Eliminar plan (baja lógica)

## 🧪 Requisitos de prueba

### Casos de prueba funcional

### ✅ Caso 1: Listar planes correctamente

- **Precondición:** Existen planes registrados en el sistema.
- **Acción:** `GET /api/pagos/planes`
- **Resultado esperado:**
  - HTTP 200 OK
  - Lista de planes con idPlan, nombre, monto, duracionDias y activo

### ✅ Caso 2: Crear plan exitosamente

- **Precondición:** El administrador está autenticado.
- **Acción:** `POST /api/pagos/planes` con nombre, monto y duracionDias válidos.
- **Resultado esperado:**
  - HTTP 201 Created
  - Plan creado con `idPlan` generado y `activo: true`

### ✅ Caso 3: Actualizar plan exitosamente

- **Precondición:** El plan existe.
- **Acción:** `PUT /api/pagos/planes/1` con nuevos datos.
- **Resultado esperado:**
  - HTTP 200 OK
  - Plan actualizado correctamente

### ✅ Caso 4: Eliminar plan sin suscripciones activas

- **Precondición:** El plan existe y no tiene suscripciones activas.
- **Acción:** `DELETE /api/pagos/planes/1`
- **Resultado esperado:**
  - HTTP 200 OK
  - Plan dado de baja con `activo: false`

### ❌ Caso 5: Eliminar plan con suscripciones activas

- **Precondición:** El plan tiene suscripciones activas de clientes.
- **Acción:** `DELETE /api/pagos/planes/1`
- **Resultado esperado:**
  - HTTP 409 Conflict
  - `error_code`: `PAY_PLAN_HAS_ACTIVE_SUBSCRIPTIONS`

### ❌ Caso 6: Sin planes registrados

- **Precondición:** No hay planes en el sistema.
- **Acción:** `GET /api/pagos/planes`
- **Resultado esperado:**
  - HTTP 404 Not Found
  - `error_code`: `PAY_NO_PLANS_FOUND`

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] Los cuatro endpoints CRUD funcionan correctamente.
- [ ] No se elimina un plan con suscripciones activas.
- [ ] La baja de planes es lógica (campo `activo: false`), no física.
- [ ] La respuesta JSON cumple con el contrato definido en todos los casos.

### 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas unitarias para cada operación CRUD.
- [ ] Se cubrieron los casos de error y respuestas sin datos.
- [ ] Las pruebas funcionales están documentadas y pasadas.

### 📄 Documentación Técnica

- [ ] Endpoints documentados en Swagger / OpenAPI.
- [ ] Se describen campos de entrada y salida con ejemplos.

### 🔐 Manejo de Errores

- [ ] Se devuelve código HTTP 400 para datos inválidos (monto ≤ 0, duración ≤ 0).
- [ ] Se devuelve código HTTP 401/403 para acceso no autorizado.
- [ ] Se devuelve código HTTP 404 cuando el plan no existe.
- [ ] Se devuelve código HTTP 409 cuando se intenta eliminar un plan con suscripciones activas.
- [ ] Se devuelve código HTTP 500/503 ante fallos internos.
- [ ] El campo `message` incluye texto descriptivo y amigable.