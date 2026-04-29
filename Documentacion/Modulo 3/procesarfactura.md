## [HU-11] Procesar factura electrónica

### 📖 Historia de usuario

**Como** Cliente del gimnasio
**Quiero** Recibir y descargar mi factura electrónica después de cada pago realizado
**Para** Tener un comprobante legal de mis transacciones con el gimnasio y consultarlo en cualquier momento

## 🔁 Flujo esperado

- El sistema genera la factura electrónica automáticamente tras cada pago exitoso.
- El cliente accede a la sección de facturas en su panel.
- El sistema consume el endpoint `POST /api/pagos/facturas` con idPago e idCliente.
- El backend valida que exista un pago aprobado con el ID proporcionado.
- Se genera la factura y se retorna la URL de descarga en formato PDF.

## Criterios de aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint `POST /api/pagos/facturas` que recibe idPago e idCliente.
- [ ] La factura se genera únicamente si el pago asociado tiene estado APROBADO.
- [ ] Se expone un endpoint `GET /api/pagos/facturas/{idFactura}` para descargar la factura.
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

- [ ] Si el pago no existe o no está aprobado, el backend retorna:

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

- **Método HTTP:** `POST`
- **Ruta:** `/api/pagos/facturas`

## 📤 Ejemplo de Respuesta JSON

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

- [ ] Si la factura no se encuentra al intentar descargarla, el backend retorna:

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

- **Precondición:** Existe un pago con estado APROBADO asociado al idPago enviado.
- **Acción:** `POST /api/pagos/facturas` con idPago e idCliente válidos.
- **Resultado esperado:**
  - HTTP 201 Created
  - Campo `success: true`
  - `idFactura` generado correctamente
  - `urlDescarga` disponible en la respuesta

### ✅ Caso 2: Descarga exitosa de factura

- **Precondición:** La factura existe y tiene URL de descarga válida.
- **Acción:** `GET /api/pagos/facturas/FAC-001234`
- **Resultado esperado:**
  - HTTP 200 OK
  - Campo `success: true`
  - `urlDescarga` funcional y accesible

### ❌ Caso 3: Pago no encontrado o no aprobado

- **Precondición:** El idPago enviado no existe o su estado no es APROBADO.
- **Acción:** `POST /api/pagos/facturas` con idPago inexistente o rechazado.
- **Resultado esperado:**
  - HTTP 404 Not Found
  - Campo `success: false`
  - `error_code`: `PAY_PAYMENT_NOT_FOUND`
  - Mensaje: `"Pago no encontrado"`

### ❌ Caso 4: Factura no encontrada al descargar

- **Precondición:** El idFactura enviado no existe en el sistema.
- **Acción:** `GET /api/pagos/facturas/FAC-999999`
- **Resultado esperado:**
  - HTTP 404 Not Found
  - Campo `success: false`
  - `error_code`: `PAY_INVOICE_NOT_FOUND`
  - Mensaje: `"Factura no encontrada"`

## ✅ Definición de Hecho

### 📦 Alcance Funcional

- [ ] La factura se genera automáticamente tras cada pago exitoso.
- [ ] La URL de descarga es funcional y retorna el PDF correctamente.
- [ ] Solo se generan facturas para pagos con estado APROBADO.
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