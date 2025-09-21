# Fase 3: Desarrollo de API Backend

## Objetivos
Desarrollar la API RESTful en FastAPI para el backend de L2 Adena Marketplace, incluyendo autenticación, modelos y endpoints básicos.

## Tareas
1. Configurar proyecto FastAPI con dependencias (FastAPI, Uvicorn, Pydantic, python-jose, passlib, SQLAlchemy, Alembic).
2. Implementar modelos de base de datos con SQLAlchemy.
3. Configurar autenticación JWT con python-jose y passlib.
4. Crear endpoints CRUD para usuarios, perfiles, reseñas, anuncios y mensajes.
5. Implementar validación de datos con Pydantic.
6. Configurar CORS y middlewares de seguridad.
7. Generar documentación Swagger UI.

## Tecnologías
- FastAPI
- SQLAlchemy
- JWT (python-jose)
- Pydantic

## Criterios de Aceptación
- API FastAPI ejecutándose en puerto local.
- Endpoints de autenticación funcionales (registro, login, logout).
- Endpoints CRUD básicos para entidades principales.
- Documentación Swagger accesible.
- Pruebas básicas de endpoints.