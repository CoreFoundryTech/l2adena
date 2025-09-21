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