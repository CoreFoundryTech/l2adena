# Fase 10: Despliegue y Pruebas

## Objetivos
Desplegar la aplicación completa en producción usando Dokploy y realizar pruebas exhaustivas.

## Tareas Completadas
1. ✅ Crear Dockerfiles para backend (Python/FastAPI) y frontend (Next.js).
2. ✅ Configurar docker-compose.yml para servicios (backend, frontend, BD).
3. ✅ Configurar SSL automático usando Dokploy (automático para dominios).
4. ✅ Implementar pruebas E2E básicas con Playwright.
5. ✅ Configurar logging básico en backend.
6. ✅ Optimizar rendimiento (compresión GZip en backend).
7. ✅ Realizar pruebas de carga básicas con Artillery.
8. ✅ Documentar proceso de despliegue.

## Docker y Despliegue
### Dockerfiles
- **Backend**: Dockerfile en `backend/` basado en python:3.9-slim, instala dependencias y ejecuta uvicorn en puerto 5001.
- **Frontend**: Dockerfile multi-stage en `frontend/`, construye con Node.js y sirve con Next.js en puerto 3000.

### Docker Compose
Archivo `docker-compose.yml` en raíz configura:
- Servicio `db`: PostgreSQL 13 con volúmenes persistentes.
- Servicio `backend`: Construye desde `backend/`, expone puerto 5001, depende de `db`.
- Servicio `frontend`: Construye desde `frontend/`, expone puerto 3000, depende de `backend`.

Para ejecutar localmente: `docker-compose up --build`

### SSL
Dokploy proporciona SSL automático para dominios personalizados. No se requiere configuración adicional.

## Pruebas
### E2E con Playwright
- Instalado en `frontend/`.
- Configuración en `frontend/playwright.config.ts`.
- Pruebas básicas en `frontend/tests/home.spec.ts`.
- Ejecutar: `cd frontend && pnpm test:e2e`

### Pruebas de Carga con Artillery
- Configuración en `load-test.yml`: 5 RPS durante 10 segundos al endpoint raíz.
- Resultados: 50 requests, 100% éxito, tiempo respuesta promedio 1.2ms.
- Ejecutar: `artillery run load-test.yml`

## Logging y Rendimiento
### Logging
- Backend: Logging básico configurado con `logging.basicConfig(level=logging.INFO)`.
- Logs en consola para endpoints accedidos.

### Optimización de Rendimiento
- Compresión GZip en backend para respuestas >1000 bytes.
- Next.js incluye compresión automática en producción.

## Tecnologías
- Dokploy
- Pruebas E2E (Playwright o Cypress)
- Monitoreo (opcional)

## Criterios de Aceptación
- Aplicación completamente funcional en producción.
- HTTPS configurado.
- Todas las funcionalidades probadas y funcionando.
- Rendimiento optimizado.
- Documentación de despliegue completa.