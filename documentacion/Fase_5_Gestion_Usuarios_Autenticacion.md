# Fase 5: Gestión de Usuarios y Autenticación

## Objetivos
Implementar el sistema completo de gestión de usuarios, autenticación y reputación en frontend y backend.

## Tareas
1. Completar endpoints de backend para registro, login y gestión de usuarios.
2. Implementar hashing de contraseñas con bcrypt en backend.
3. Crear middleware de autenticación JWT en backend.
4. Desarrollar páginas de frontend para registro y login.
5. Implementar gestión de estado de usuario autenticado con Zustand.
6. Crear páginas de perfil de usuario y edición.
7. Implementar sistema de reseñas y cálculo de reputación.
8. Configurar rutas protegidas en frontend.
9. Agregar funcionalidad de historial de compras para compradores.
10. Implementar sistema de "likes" para marcar vendedores favoritos.
11. Mostrar contador de likes en perfiles de vendedores.

## Tecnologías
- JWT
- bcrypt (passlib)
- Zustand
- React Query

## Criterios de Aceptación
- Usuarios pueden registrarse y autenticarse.
- Perfiles de usuario editables.
- Sistema de reseñas funcional.
- Rutas protegidas funcionando.
- Estado de autenticación persistente.
## Estado de Cumplimiento

La fase 5 de Gestión de Usuarios y Autenticación ha sido completada exitosamente. A continuación, se detallan los cambios técnicos realizados:

- **Endpoints backend completados**: Se han implementado los endpoints para historial de compras y likes, permitiendo la gestión completa de estas funcionalidades.
- **Páginas frontend funcionales**: Las páginas del frontend están operativas con llamadas API integradas para todas las funcionalidades requeridas.
- **Gestión de estado con Zustand**: Se utiliza Zustand para manejar el estado de autenticación y datos del usuario de manera eficiente.
- **Perfil/edición integrado**: El perfil de usuario y su edición están completamente integrados en el frontend.
- **Sistema reseñas/reputación**: Implementado con cálculo de promedio de reseñas para determinar la reputación de los usuarios.
- **Rutas protegidas**: Configuradas para asegurar el acceso solo a usuarios autenticados en las secciones correspondientes.
- **Historial de compras**: Funcionalidad completa para que los compradores puedan revisar su historial de transacciones.
- **Likes con contador**: Sistema de "likes" implementado para marcar vendedores favoritos, con contador visible en los perfiles.
- **Autenticación JWT y hashing bcrypt**: La autenticación JWT está implementada en el backend, junto con el hashing de contraseñas utilizando bcrypt para mayor seguridad.