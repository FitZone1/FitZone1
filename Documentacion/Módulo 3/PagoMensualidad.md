## [HU-9] Aplicar pago de mensualidad

### 📖 Historia de usuario

**Como** Cliente del gimnasio
**Quiero** Pagar mi mensualidad de forma virtual y segura desde la plataforma FitZone
**Para** Mantener mi suscripción activa sin necesidad de ir presencialmente al gimnasio y poder seguir reservando sesiones con entrenadores

## 🔁 Flujo esperado

- El cliente accede a la sección de pagos y selecciona su plan activo.
- El cliente ingresa su método de pago y los datos de la tarjeta.
- El sistema consume el endpoint `POST /api/pagos` con idCliente, idPlan, metodoPago y numeroTarjeta.
- El backend valida el monto según el plan seleccionado y envía la solicitud a la pasarela de pago.
- Si la pasarela aprueba, el pago se registra como APROBADO y la suscripción se renueva.
- Se genera automáticamente una factura electrónica asociada al pago.

## Criterios de aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `POST /api/pagos` que recibe idCliente, idPlan, metodoPago y numeroTarjeta.
- [ ] El monto cobrado debe coincidir exactamente con el precio del plan seleccionado.
- [ ] El pago solo se considera exitoso si la pasarela externa devuelve estado APROBADO.
- [ ] El pago se procesa mediante HTTPS para garantizar la seguridad de los datos.

### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON:

```json
{
  "success": true,
  "message": "Pago iniciado correctamente",
  "data": {
    "idPago": "PAY-987654",
    "monto": 85000,
    "estado": "APROBADO",
    "fecha": "2026-03-18T10:30:00"
  }
}
```

- [ ] Si la pasarela de pagos rechaza la transacción, el backend retorna:

```json
{
  "success": false,
  "statusCode": 402,
  "message": "Pago rechazado",
  "error": {
    "error_code": "PAY_PAYMENT_DECLINED",
    "details": "La pasarela de pagos rechazó la transacción por fondos insuficientes",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

## 🔧 Notas Técnicas

- **Método HTTP:** `POST`
- **Ruta:** `/api/pagos`

## 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "message": "Pago iniciado correctamente",
  "data": {
    "idPago": "PAY-987654",
    "monto": 85000,
    "estado": "APROBADO",
    "fecha": "2026-03-18T10:30:00"
  }
}
```

- [ ] Si la pasarela no está disponible, el backend retorna:

```json
{
  "success": false,
  "statusCode": 402,
  "message": "Pago rechazado",
  "error": {
    "error_code": "PAY_PAYMENT_DECLINED",
    "details": "La pasarela de pagos rechazó la transacción por fondos insuficientes",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

## 🧪 Requisitos de prueba

### Casos de prueba funcional

### ✅ Caso 1: Pago exitoso

- **Precondición:** El cliente tiene un plan activo y la pasarela de pagos está disponible.
- **Acción:** `POST /api/pagos` con idCliente, idPlan, metodoPago y numeroTarjeta válidos.
- **Resultado esperado:**
  - HTTP 201 Created
  - Campo `success: true`
  - Estado del pago: `APROBADO`
  - `idPago` generado correctamente
  - Suscripción renovada automáticamente

### ❌ Caso 2: Pago rechazado por la pasarela

- **Precondición:** La pasarela de pagos devuelve estado rechazado por fondos insuficientes.
- **Acción:** `POST /api/pagos` con datos válidos pero sin fondos suficientes.
- **Resultado esperado:**
  - HTTP 402 Payment Required
  - Campo `success: false`
  - `error_code`: `PAY_PAYMENT_DECLINED`
  - Mensaje: `"Pago rechazado"`
  - Suscripción no se renueva

### ❌ Caso 3: Plan no encontrado

- **Precondición:** El idPlan enviado no existe en el sistema.
- **Acción:** `POST /api/pagos` con idPlan inexistente.
- **Resultado esperado:**
  - HTTP 404 Not Found
  - Campo `success: false`
  - `error_code`: `PAY_PLAN_NOT_FOUND`
  - Mensaje descriptivo indicando que el plan no existe

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] El monto cobrado coincide exactamente con el precio del plan seleccionado.
- [ ] El pago solo se aprueba si la pasarela confirma estado APROBADO.
- [ ] La suscripción se renueva automáticamente tras pago exitoso.
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