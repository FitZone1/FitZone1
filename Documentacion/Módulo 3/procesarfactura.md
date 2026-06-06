## [HU-10] Procesar factura electrónica

### 📖 Historia de usuario

**Como** Cliente del gimnasio
**Quiero** Recibir y descargar mi factura electrónica después de cada pago realizado
**Para** Tener un comprobante legal de mis transacciones con el gimnasio y consultarlo en cualquier momento

## 🔁 Flujo esperado

- El sistema genera la factura electrónica automáticamente tras cada pago exitoso.
- El cliente accede a la sección de facturas en su panel.
- El sistema consume el endpoint `POST /api/pagos/facturas` con idPago e idCliente.
- El backend valida que exista un pago aprobado con el ID proporcionado y que pertenezca al cliente.
- Se genera la factura y se retorna la URL de descarga en formato PDF.
- Si el cliente intenta generar la factura de un pago ya facturado, se retorna la factura existente sin crear una nueva.

## Criterios de aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `POST /api/pagos/facturas` que recibe idPago e idCliente.
- [ ] La factura se genera únicamente si el pago asociado tiene estado APROBADO.
- [ ] Si el pago tiene estado RECHAZADO o PENDIENTE, se retorna error 404 igual que si no existiera.
- [ ] Si el idCliente no coincide con el dueño del pago, se retorna error 404.
- [ ] Si ya existe una factura para el pago, se retorna la factura existente sin crear duplicados.
- [ ] Se expone un endpoint `GET /api/pagos/facturas/{idFactura}` para consultar y descargar la factura.
- [ ] La factura incluye fecha, monto, plan, nombre del cliente y número de factura.

### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON:

```json
{
  "success": true,
  "message": "Factura generada correctamente",
  "data": {
    "idFactura": "FAC-001234",
    "idPago": "PAY-987654",
    "monto": 85000,
    "fecha": "2026-03-18T10:30:00",
    "urlDescarga": "/facturas/FAC-001234.pdf"
  }
}
```

- [ ] Si el pago no existe, no está aprobado o no pertenece al cliente, el backend retorna:

```json
{
  "success": false,
  "statusCode": 404,
  "message": "Pago no encontrado",
  "error": {
    "error_code": "PAY_PAYMENT_NOT_FOUND",
    "details": "No existe un pago aprobado con el ID proporcionado",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

## 🔧 Notas Técnicas

- **Método HTTP:** `POST` para generar factura / `GET` para consultar factura
- **Ruta generación:** `/api/pagos/facturas`
- **Ruta consulta:** `/api/pagos/facturas/{idFactura}`
- Los IDs de factura siguen el formato `FAC-XXXXXX` (6 dígitos).
- Los IDs de pago siguen el formato `PAY-XXXXXX` (6 dígitos).

## 📤 Ejemplo de Respuesta JSON

```json
{
  "success": true,
  "message": "Factura generada correctamente",
  "data": {
    "idFactura": "FAC-000001",
    "idPago": "PAY-987654",
    "monto": 85000,
    "fecha": "2026-03-18T10:30:00",
    "urlDescarga": "/facturas/FAC-000001.pdf"
  }
}
```

- [ ] Si la factura no se encuentra al intentar consultarla, el backend retorna:

```json
{
  "success": false,
  "statusCode": 404,
  "message": "Factura no encontrada",
  "error": {
    "error_code": "PAY_INVOICE_NOT_FOUND",
    "details": "No existe una factura con el ID proporcionado",
    "timestamp": "2026-03-18T10:30:00"
  }
}
```

## 🧪 Requisitos de prueba

### Casos de prueba funcional

### ✅ Caso 1: Generación exitosa de factura

- **Precondición:** Existe un pago con estado APROBADO asociado al idPago enviado y pertenece al idCliente enviado.
- **Acción:** `POST /api/pagos/facturas` con `idPago: "PAY-987654"` e `idCliente: 42`.
- **Resultado esperado:**
  - HTTP 201 Created
  - Campo `success: true`
  - `idFactura` generado con formato `FAC-XXXXXX`
  - `urlDescarga` disponible con formato `/facturas/FAC-XXXXXX.pdf`

### ✅ Caso 2: Descarga exitosa de factura

- **Precondición:** La factura existe en el sistema.
- **Acción:** `GET /api/pagos/facturas/FAC-000001`
- **Resultado esperado:**
  - HTTP 200 OK
  - Campo `success: true`
  - `urlDescarga` presente en la respuesta

### ✅ Caso 3: Factura duplicada — retorna la existente

- **Precondición:** Ya existe una factura generada para el pago `PAY-987654`.
- **Acción:** `POST /api/pagos/facturas` con el mismo `idPago: "PAY-987654"` e `idCliente: 42`.
- **Resultado esperado:**
  - HTTP 201 Created
  - Campo `success: true`
  - Se retorna la misma factura ya existente (mismo `idFactura`)
  - No se crea un registro duplicado en el sistema

### ❌ Caso 4: Pago no encontrado

- **Precondición:** El idPago enviado no existe en el sistema.
- **Acción:** `POST /api/pagos/facturas` con `idPago: "PAY-999999"` e `idCliente: 42`.
- **Resultado esperado:**
  - HTTP 404 Not Found
  - Campo `success: false`
  - `error_code`: `PAY_PAYMENT_NOT_FOUND`
  - Mensaje: `"Pago no encontrado"`

### ❌ Caso 5: Pago no aprobado (estado RECHAZADO o PENDIENTE)

- **Precondición:** El idPago existe pero su estado no es APROBADO.
- **Acción:** `POST /api/pagos/facturas` con `idPago: "PAY-222222"` (RECHAZADO) o `idPago: "PAY-333333"` (PENDIENTE).
- **Resultado esperado:**
  - HTTP 404 Not Found
  - Campo `success: false`
  - `error_code`: `PAY_PAYMENT_NOT_FOUND`
  - Mensaje: `"Pago no encontrado"`

### ❌ Caso 6: idCliente no coincide con el pago

- **Precondición:** El idPago existe y está aprobado, pero pertenece a otro cliente.
- **Acción:** `POST /api/pagos/facturas` con `idPago: "PAY-987654"` e `idCliente: 99` (cliente incorrecto).
- **Resultado esperado:**
  - HTTP 404 Not Found
  - Campo `success: false`
  - `error_code`: `PAY_PAYMENT_NOT_FOUND`
  - Mensaje: `"Pago no encontrado"`

### ❌ Caso 7: Factura no encontrada al consultar

- **Precondición:** El idFactura enviado no existe en el sistema.
- **Acción:** `GET /api/pagos/facturas/FAC-999999`
- **Resultado esperado:**
  - HTTP 404 Not Found
  - Campo `success: false`
  - `error_code`: `PAY_INVOICE_NOT_FOUND`
  - Mensaje: `"Factura no encontrada"`

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] La factura se genera únicamente para pagos con estado APROBADO.
- [ ] No se generan facturas duplicadas para el mismo pago.
- [ ] Solo el cliente dueño del pago puede generar su factura.
- [ ] La URL de descarga sigue el formato `/facturas/FAC-XXXXXX.pdf`.
- [ ] La respuesta JSON cumple con el contrato definido en todos los casos.

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