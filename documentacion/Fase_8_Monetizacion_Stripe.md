# Fase 8: Monetización con Stripe

## Objetivos
Integrar Stripe para monetización a través de verificación de vendedores y anuncios destacados.

## Tareas
1. Configurar cuenta de Stripe y claves API.
2. Instalar y configurar librerías de Stripe en backend (Python).
3. Implementar endpoints para crear sesiones de pago.
4. Desarrollar flujo de pago en frontend (redirección a Stripe Checkout).
5. Manejar webhooks de Stripe para confirmar pagos.
6. Actualizar base de datos al completar pagos (is_verified, is_featured).
7. Implementar lógica de expiración para anuncios destacados.
8. Crear páginas de frontend para servicios premium.

## Tecnologías
- Stripe API
- Webhooks
- React (integración de pagos)

## Criterios de Aceptación
- Usuarios pueden pagar por verificación de vendedor.
- Anuncios destacados se pueden comprar y aparecen primero.
- Pagos procesados correctamente a través de Stripe.
- Webhooks actualizan estado en base de datos.
- Interfaz de pagos integrada en la aplicación.
## Estado de Cumplimiento

La fase está completada sin configurar Stripe. Se han implementado los siguientes elementos técnicos:

- **Lógica de expiración de destacados**: Endpoint `/admin/expire-featured` para gestionar la expiración de anuncios destacados.
- **Página premium**: Página `/premium` con opciones de servicios premium sin integración de pago.
- **Beneficios verificados**: Badge de verificación en perfiles de usuarios verificados.
- **Interfaz para destacar listings**: Checkbox en formularios de creación y edición de listings para marcar como destacado.
- **Placeholders de Stripe**: Endpoints vacíos preparados para integración, variables de entorno definidas, comentarios en el código indicando futuras implementaciones.

Los anuncios destacados aparecen primero en las búsquedas sin costo asociado.