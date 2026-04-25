## Reserva de sesion de entrenamiento

 **Como** Cliente
 **Quiero** reservar una sesion de entrenamiento con un entrenador disponible con un horario que me convenga
 **para** asegurar mi espacio con el entrenador elegido y planificar mi rutina de entrenamiento semanal.

 ## Flujo esperado

- El cliente selecciona un entrenador disponible en la plataforma.
- El cliente elige un horario disponible del entrenador.
- El sistema consume POST /api/v1/reservas con idEntrenador, idCliente y fechaHora.
- El backend valida que el horario esté disponible y no haya solapamientos.
- Se crea la reserva con estado CONFIRMADA y se actualiza la disponibilidad del entrenador.

## Criterios de Aceptación

### 1. Validaciones de negocio

- [] Solo se puede reservar en horarios dentro del rango declarado por el entrenador.

- [] El cliente debe tener suscripción activa y mensualidad al día para reservar.

### 2.Estado de la reserva

- [] La reserva se crea con estado CONFIRMADA.

- [] El sistema retorna idReserva, estado y fechaHora confirmada.

-[]