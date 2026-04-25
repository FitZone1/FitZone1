## [HU-03]	Inicio de sesión

## 📖 Historia de Usuario

**Como** usuario registrado (cliente o entrenador),
**Quiero** iniciar sesión con mi correo y contraseña,
**Para** recibir un token de acceso JWT y poder utilizar todas las funciones de la plataforma según mi rol.

## 🔁 Flujo Esperado

- El usuario ingresa su correo y contraseña en el formulario de login.
- El sistema consume el endpoint POST /api/v1/auth/login.
- El backend valida las credenciales contra la base de datos.
- Si son válidas, se genera y retorna un token JWT con el rol del usuario.
 El token se usa en las solicitudes subsiguientes para autenticación.

## ✅ Criterios de Aceptación

###  1. Lógica de autenticación
- [ ] Se expone un endpoint `POST /api/v1/auth/login` que recibe correo y contraseña.
- [ ] El backend valida las credenciales y genera un token JWT.
- [ ] El token incluye el rol del usuario (CLIENTE o ENTRENADOR).

### 2. Manejo de errores


