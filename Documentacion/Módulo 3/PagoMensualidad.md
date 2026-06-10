## [HU-9] Aplicar pago de mensualidad

### 📖 Historia de usuario

**Como** Cliente del gimnasio
**Quiero** Pagar mi mensualidad de forma virtual y segura desde la plataforma FitZone
**Para** Mantener mi suscripción activa sin necesidad de ir presencialmente al gimnasio y poder seguir reservando sesiones con entrenadores

## 🔁 Flujo esperado

- El cliente accede a la sección de pagos y consulta los métodos de pago disponibles.
- El cliente selecciona su plan activo y el método de pago.
- Si el método de pago es TARJETA o PSE, el cliente ingresa el número de tarjeta de 16 dígitos.
- Si el método de pago es EFECTIVO, no se requiere número de tarjeta.
- El sistema consume el endpoint `POST /api/pagos` con idCliente, idPlan, metodoPago y opcionalmente numeroTarjeta.
- El backend valida el monto según el plan seleccionado y procesa el pago.
- Si el pago es aprobado, la suscripción se renueva automáticamente.
- Se genera automáticamente una factura electrónica asociada al pago.

## Criterios de aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `GET /api/pagos/metodos` que retorna la lista de métodos de pago habilitados.
- [ ] Se expone un endpoint `POST /api/pagos` que recibe idCliente, idPlan, metodoPago y opcionalmente numeroTarjeta.
- [ ] El campo `numeroTarjeta` es obligatorio únicamente cuando el método de pago es `TARJETA` o `PSE`.
- [ ] Cuando el método de pago es `EFECTIVO`, el campo `numeroTarjeta` no se requiere ni se valida.
- [ ] El monto cobrado debe coincidir exactamente con el precio del plan seleccionado.
- [ ] El pago solo se considera exitoso si la pasarela externa devuelve estado APROBADO.
- [ ] El pago se procesa mediante HTTPS para garantizar la seguridad de los datos.

### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON al consultar métodos de pago:

```json
{
  "success": true,
  "message": "Métodos de pago obtenidos correctamente",
  "data": [
    { "codigo": "TARJETA", "nombre": "Tarjeta de crédito/débito", "requiereTarjeta": true },
    { "codigo": "PSE",     "nombre": "PSE - Débito bancario",      "requiereTarjeta": true },
    { "codigo": "EFECTIVO","nombre": "Pago en efectivo",           "requiereTarjeta": false }
  ]
}
```

- [ ] Se responde con la siguiente estructura en JSON al registrar un pago exitoso:

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

- [ ] Si se envía `numeroTarjeta` cuando el método es EFECTIVO, el backend lo ignora (no retorna error).
- [ ] Si el método requiere tarjeta y no se envía `numeroTarjeta`, el backend retorna:

```json
{
  "success": false,
  "statusCode": 400,
  "message": "Número de tarjeta requerido",
  "error": {
    "error_code": "PAY_CARD_NUMBER_REQUIRED",
    "details": "El método de pago seleccionado requiere número de tarjeta",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

## 🔧 Notas Técnicas

- **Método HTTP `GET`:** `/api/pagos/metodos`
- **Método HTTP `POST`:** `/api/pagos`
- El campo `numeroTarjeta` es opcional en el schema; la validación de su obligatoriedad se realiza en la capa de servicio según el `metodoPago` recibido.

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

## 🧪 Requisitos de prueba

### Casos de prueba funcional

### ✅ Caso 1: Consulta de métodos de pago

- **Precondición:** El sistema tiene métodos de pago habilitados.
- **Acción:** `GET /api/pagos/metodos` con token de cliente válido.
- **Resultado esperado:**
  - HTTP 200 OK
  - Campo `success: true`
  - Lista de métodos con código, nombre y flag `requiereTarjeta`

### ✅ Caso 2: Pago exitoso con tarjeta

- **Precondición:** El cliente tiene un plan activo y la pasarela de pagos está disponible.
- **Acción:** `POST /api/pagos` con metodoPago `TARJETA` y numeroTarjeta de 16 dígitos.
- **Resultado esperado:**
  - HTTP 201 Created
  - Campo `success: true`
  - Estado del pago: `APROBADO`
  - `idPago` generado correctamente
  - Suscripción renovada automáticamente

### ✅ Caso 3: Pago exitoso en efectivo (sin tarjeta)

- **Precondición:** El cliente tiene un plan activo y selecciona método EFECTIVO.
- **Acción:** `POST /api/pagos` con metodoPago `EFECTIVO`, sin campo `numeroTarjeta`.
- **Resultado esperado:**
  - HTTP 201 Created
  - Campo `success: true`
  - Estado del pago: `APROBADO`
  - No se valida ni exige número de tarjeta

### ❌ Caso 4: Pago con tarjeta sin enviar numeroTarjeta

- **Precondición:** El cliente selecciona método TARJETA pero omite el número.
- **Acción:** `POST /api/pagos` con metodoPago `TARJETA` sin `numeroTarjeta`.
- **Resultado esperado:**
  - HTTP 400 Bad Request
  - `error_code`: `PAY_CARD_NUMBER_REQUIRED`
  - Mensaje: `"Número de tarjeta requerido"`

### ❌ Caso 5: Plan no encontrado

- **Precondición:** El idPlan enviado no existe en el sistema.
- **Acción:** `POST /api/pagos` con idPlan inexistente.
- **Resultado esperado:**
  - HTTP 404 Not Found
  - `error_code`: `PAY_PLAN_NOT_FOUND`
  - Mensaje descriptivo indicando que el plan no existe

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] El endpoint `GET /api/pagos/metodos` lista todos los métodos con el flag `requiereTarjeta`.
- [ ] El campo `numeroTarjeta` solo se valida cuando el método es TARJETA o PSE.
- [ ] El monto cobrado coincide exactamente con el precio del plan seleccionado.
- [ ] El pago solo se aprueba si la pasarela confirma estado APROBADO.
- [ ] La suscripción se renueva automáticamente tras pago exitoso.
- [ ] La respuesta JSON cumple con el contrato definido.

### 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas unitarias para cada funcionalidad principal.
- [ ] Se cubrieron los casos de error y respuestas sin datos.
- [ ] Las pruebas funcionales están documentadas y pasadas.

### 📄 Documentación Técnica

- [ ] Endpoints documentados en Swagger / OpenAPI.
- [ ] Se describen campos de entrada y salida con ejemplos.

### 🔐 Manejo de Errores

- [ ] Se devuelve código HTTP 400 para parámetros inválidos o tarjeta faltante.
- [ ] Se devuelve código HTTP 401/403 para acceso no autorizado.
- [ ] Se devuelve código HTTP 402 para pagos rechazados por la pasarela.
- [ ] Se devuelve código HTTP 500/503 ante fallos internos.
- [ ] El campo `message` incluye texto descriptivo y amigable.