# Fase 2: Diseño y Configuración de Base de Datos

## Objetivos
Diseñar y configurar la base de datos PostgreSQL para el proyecto L2 Adena Marketplace, incluyendo esquemas, migraciones y configuración inicial.

## Tareas
1. Instalar y configurar PostgreSQL localmente y en Dokploy.
2. Diseñar esquemas de base de datos basados en el documento técnico:
   - Tabla User (id, email, password_hash, username, is_verified, created_at)
   - Tabla Profile (user_id, description, server_list)
   - Tabla Review (id, listing_id, reviewer_id, reviewee_id, rating, comment, created_at)
   - Tabla Listing (id, seller_id, server_name, chronicle, type BUY/SELL, quantity, price, description, status ACTIVE/CLOSED, is_featured, featured_expires_at)
   - Tabla Message (id, room_id, sender_id, content, created_at)
   - Tabla PurchaseHistory (id, buyer_id, listing_id, transaction_date, status)
   - Tabla SellerLike (id, buyer_id, seller_id, created_at)
   - Tabla Server (id, name, chronicle, region, is_active)
   3. Configurar SQLAlchemy con modo asíncrono.
4. Crear migraciones iniciales con Alembic.
5. Establecer conexiones de base de datos seguras.

## Tecnologías
- PostgreSQL
- SQLAlchemy 2.0 (modo asíncrono)
- Alembic

## Criterios de Aceptación
- Base de datos PostgreSQL configurada y accesible.
- Esquemas de tablas creados y migrados.
- Conexiones de base de datos funcionales en el backend.
- Scripts de inicialización de datos de prueba.
## Estado de Cumplimiento

La fase está completada. Detalles técnicos de los cambios realizados:

- Backend reestructurado a Python/FastAPI.
- Modelos SQLAlchemy creados para todas las tablas (User, Profile, Review, Listing, Message, PurchaseHistory, SellerLike).
- Alembic configurado con migración inicial.
- Conexiones PostgreSQL usando variables de entorno.
- Script de inicialización de datos de prueba.
- PostgreSQL configurado en Dokploy.
- La BD está migrada exitosamente con las tablas User, Profile, Review, Listing, Message, PurchaseHistory, SellerLike creadas en PostgreSQL de Dokploy.
- Las migraciones se aplicaron correctamente.