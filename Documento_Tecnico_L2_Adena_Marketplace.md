# Documento Técnico: L2 Adena Marketplace

## Versión en Español

Versión 1.11.

Resumen Ejecutivo

Este documento describe la arquitectura técnica y las tecnologías propuestas para la creación de "L2 Adena Marketplace", una plataforma web destinada a facilitar el comercio seguro de bienes virtuales (adena) para el juego Lineage 2.

El proyecto se basa en un modelo de monetización híbrido que prioriza la confianza del usuario y minimiza el riesgo legal para la plataforma. En lugar de procesar directamente las transacciones de RMT (Real Money Trading), la plataforma generará ingresos a través de servicios premium para vendedores, como la verificación de perfiles y la promoción de anuncios, creando un ecosistema basado en la reputación.

2. Arquitectura del Sistema

Se propone una arquitectura de tres capas (Three-Tier Architecture), un enfoque robusto y escalable para aplicaciones web modernas.

Frontend (Cliente): Una aplicación web renderizada en el servidor (SSR) y en el cliente (CSR) construida con Next.js. Será responsable de toda la interfaz de usuario y la interacción.

Backend (Servidor): Una API RESTful desarrollada en Python que manejará toda la lógica de negocio, la autenticación de usuarios y la comunicación con la base de datos.

Base de Datos (Persistencia): Un sistema de base de datos relacional para almacenar de forma segura y estructurada todos los datos de la aplicación.

Despliegue: Todo el sistema (Frontend, Backend, Base de Datos) será gestionado y desplegado a través de la plataforma de auto-hosting Dokploy.

3. Pila Tecnológica (Tech Stack)

La selección de tecnologías busca un equilibrio entre rendimiento, escalabilidad y una rápida velocidad de desarrollo, con un enfoque en el ecosistema de Python y Next.js.

3.1. Frontend (Aplicación Web)

Framework: Next.js (App Router)

Razón: Un framework de React líder para producción. Ofrece renderizado en el servidor (SSR) y generación de sitios estáticos (SSG) para un rendimiento y SEO óptimos, junto con una excelente experiencia de desarrollo.

Gestor de Paquetes: pnpm

Razón: Eficiente en el uso del espacio en disco y rápido en la instalación de dependencias, ideal para mantener un monorepo o un proyecto limpio.

UI y Estilos: Tailwind CSS + shadcn/ui

Razón: Tailwind CSS permite construir diseños modernos y responsivos rápidamente. shadcn/ui ofrece componentes accesibles y personalizables construidos sobre Tailwind para una implementación rápida y consistente.

Internacionalización (i18n): La plataforma será multiidioma, soportando inglés, español, portugués y ruso. Se utilizará next-i18next para gestionar las traducciones y cambiar el idioma dinámicamente.

Gestión de Estado: Zustand

Razón: Una solución de gestión de estado simple y potente, ideal para manejar el estado global de la aplicación (como la información del usuario autenticado) con un mínimo de código.

Comunicación con API: Fetch API con React Query (TanStack Query)

Razón: React Query simplifica drásticamente la obtención, el almacenamiento en caché y la actualización de datos del servidor, mejorando la experiencia del usuario y la resiliencia de la aplicación.

Despliegue: Dokploy

Razón: Permite auto-hospedar la aplicación Next.js de manera sencilla en tu propio servidor (VPS), ofreciendo control total sobre la infraestructura, certificados SSL automáticos y despliegues basados en Git.

3.2. Backend (API del Servidor)

Lenguaje: Python 3.11+

Razón: Un lenguaje versátil con un ecosistema maduro para el desarrollo web, la ciencia de datos y más. Su sintaxis clara facilita el mantenimiento.

Framework: FastAPI

Razón: Un framework web de Python moderno y de alto rendimiento para construir APIs. Incluye validación de datos automática (con Pydantic) y genera documentación interactiva (Swagger UI) de forma nativa.

Autenticación: JSON Web Tokens (JWT) con la librería python-jose.

Razón: Estándar para crear tokens de acceso seguros. Se utilizará passlib con bcrypt para el hasheo de contraseñas de forma segura.

Comunicación en Tiempo Real (Chat): WebSockets

Razón: FastAPI tiene soporte nativo para WebSockets, lo que permite una comunicación bidireccional eficiente para el sistema de mensajería interna sin necesidad de librerías externas complejas.

ORM (Object-Relational Mapping): SQLAlchemy 2.0 (con modo asíncrono)

Razón: El ORM más potente y flexible del ecosistema Python. Su nuevo soporte asíncrono se integra perfectamente con FastAPI. Se usará Alembic para gestionar las migraciones de la base de datos.

Despliegue: Dokploy

Razón: Dokploy facilita el despliegue de aplicaciones Python (usando Dockerfiles o buildpacks) junto con la base de datos, centralizando toda la gestión de la infraestructura en una única interfaz.

3.3. Base de Datos

Sistema Gestor: PostgreSQL

Razón: Es una base de datos relacional de código abierto, potente y confiable, con excelente soporte en el ecosistema de Python y SQLAlchemy. Dokploy facilita su despliegue y gestión.

3.4. Servicios de Terceros

Pasarela de Pagos: Stripe

Razón: Líder del mercado para procesar pagos en línea. Ofrece APIs y librerías para Python muy completas para gestionar los pagos de servicios premium.

Control de Versiones: Git y GitHub

Razón: Estándar de la industria para el control de versiones. Se integrará con Dokploy para despliegues automáticos en cada git push.

4. Implementación de Características Clave

4.1. Gestión de Usuarios y Reputación

DB Schema: Tabla User (id, email, password_hash, username, is_verified, created_at). Tabla Profile (user_id, description, server_list).

Reputación: Tabla Review (id, listing_id, reviewer_id, reviewee_id, rating, comment, created_at). Se calculará un promedio de rating que se mostrará en el perfil del usuario.

4.2. Sistema de Anuncios (Listings)

DB Schema: Tabla Listing (id, seller_id, server_name, chronicle, typeBUY/SELL, quantity, price, description, statusACTIVE/CLOSED, is_featured, featured_expires_at).

Lógica: Implementar endpoints CRUD en FastAPI. La lógica de búsqueda debe ser eficiente y permitir filtros. Los anuncios is_featured deben aparecer primero.

4.3. Mensajería Interna

Tecnología: Usar el soporte nativo de WebSockets de FastAPI para crear "salas" de chat por cada transacción.

DB Schema: Tabla Message (id, room_id, sender_id, content, created_at).

Flujo: Cuando un comprador contacta a un vendedor, se crea una conexión WebSocket a una sala única. Los mensajes se emiten en tiempo real y se persisten en la base de datos. Los administradores pueden ver todos los chats para fines de moderación.

4.4. Monetización (Integración con Stripe)

Verificación de Vendedor y Anuncios Destacados:

El frontend solicita al backend la creación de una sesión de pago.

El backend (Python) se comunica con la API de Stripe y devuelve una URL de Stripe Checkout.

El usuario es redirigido a Stripe para completar el pago.

El backend recibe la confirmación a través de un webhook de Stripe y actualiza la base de datos (is_verified = true o is_featured = true).

5. Consideraciones de Seguridad

Contraseñas: Todas las contraseñas de usuario deben ser hasheadas con bcrypt (vía passlib) antes de almacenarse.

Validación de Datos: FastAPI y Pydantic se encargarán de validar y sanear automáticamente los datos de entrada de la API para prevenir ataques de inyección.

Comunicaciones: Forzar el uso de HTTPS en todo el sitio, gestionado automáticamente por Dokploy.

Protección de Rutas: Las rutas de la API que requieren autenticación deben estar protegidas con dependencias de FastAPI que verifiquen la validez del JWT en cada solicitud.

