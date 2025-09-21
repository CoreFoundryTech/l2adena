# Fase 7: Sistema de Chat

## Objetivos
Implementar el sistema de mensajería interna en tiempo real para coordinación entre compradores y vendedores, con visibilidad para administradores.

## Tareas
1. Configurar WebSockets en FastAPI para salas de chat por transacción.
2. Implementar endpoints para crear salas de chat al contactar vendedores.
3. Desarrollar lógica de envío y recepción de mensajes en tiempo real.
4. Persistir mensajes en base de datos.
5. Crear componentes de chat en frontend con React.
6. Implementar interfaz de chat (lista de conversaciones, mensajes).
7. Agregar funcionalidad para que administradores puedan ver todos los chats.
8. Configurar notificaciones en tiempo real.

## Tecnologías
- WebSockets (FastAPI nativo)
- React (componentes de chat)
- SQLAlchemy (persistencia de mensajes)

## Criterios de Aceptación
- Usuarios pueden iniciar chats desde anuncios.
- Mensajes enviados y recibidos en tiempo real.
- Historial de mensajes persistido.
- Administradores pueden acceder a todos los chats.
- Interfaz de chat responsiva y usable.