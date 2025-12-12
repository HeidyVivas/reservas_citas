# 👤 Persona 4 — Pruebas + Deployment + DevOps
## Checklist de Tareas y Estado

---

## ✔ PRUEBAS UNITARIAS E INTEGRACIÓN

### Configurar pytest o unittest
- ❌ **NO COMPLETADO**
- **Comentario**: Se recomienda usar `pytest` para el proyecto Django. Necesita:
  - Instalar `pytest` y `pytest-django` en `requirements.txt`
  - Crear archivo `pytest.ini` con configuración básica
  - Crear archivos de test en `tests/` o `tests.py` por app

### Pruebas unitarias - Usuarios
- ❌ **NO COMPLETADO**
- **Comentario**: Crear tests en `apps/users/tests.py`:
  - Crear usuario con email válido
  - Validar permiso de rol (cliente, empleado, admin)
  - Cambiar rol de usuario
  - Verificar that `Profile` se crea automáticamente con `post_save` signal

### Pruebas unitarias - Login
- ❌ **NO COMPLETADO**
- **Comentario**: Crear tests en `apps/users/tests.py`:
  - Login con credenciales correctas → obtener JWT token
  - Login con credenciales incorrectas → error 401
  - Refresh token válido → nuevo access token
  - Token expirado → rechazar request

### Pruebas unitarias - Permisos
- ❌ **NO COMPLETADO**
- **Comentario**: Crear tests en `apps/citas/tests.py` y `apps/users/tests.py`:
  - Usuario cliente NO puede ver todas las citas (solo las suyas)
  - Usuario empleado puede ver/editar citas asignadas
  - Usuario admin puede ver/editar todas las citas
  - Usuario NO autenticado → rechazar acceso a endpoints protegidos

### Pruebas unitarias - Creación de citas
- ❌ **NO COMPLETADO**
- **Comentario**: Crear tests en `apps/citas/tests.py`:
  - Crear cita con datos válidos → status 201
  - Crear cita sin datos requeridos → status 400
  - Crear cita con fecha en el pasado → rechazar
  - Crear cita sin disponibilidad → rechazar
  - Validar que se asigna usuario actual automáticamente

### Pruebas unitarios - Endpoints personalizados
- ❌ **NO COMPLETADO**
- **Comentario**: Crear tests en `apps/core/tests.py`:
  - GET `/api/health/` → status 200, respuesta JSON válida
  - GET `/api/health/status/` → status 200, información de DB
  - Testear que endpoints de swagger están disponibles

### Pruebas de integración - Reserva de cita
- ❌ **NO COMPLETADO**
- **Comentario**: Crear tests en `apps/citas/tests.py`:
  - Usuario cliente crea cita → estado "pendiente"
  - Empleado aprueba cita → estado "aprobada"
  - Verificar historial de cambios de estado
  - Enviar notificación (si existe) al cliente

### Pruebas de integración - Cancelación
- ❌ **NO COMPLETADO**
- **Comentario**: Crear tests en `apps/citas/tests.py`:
  - Usuario puede cancelar su propia cita
  - Usuario NO puede cancelar cita de otro (sin ser admin)
  - Cita completada NO puede cancelarse
  - Cancelación libera la disponibilidad

### Cobertura de tests
- ❌ **NO COMPLETADO - Meta: 50% mínimo**
- **Comentario**: Usar `pytest-cov` para medir cobertura
  ```bash
  pytest --cov=apps --cov-report=html
  ```
  - Generar reporte HTML
  - Incluir en CI/CD si existe

---

## ✔ PREPARACIÓN DE DESPLIEGUE

### Gunicorn/Uvicorn
- ✅ **COMPLETADO**
- **Detalles implementados**:
  - `gunicorn==23.0.0` agregado en `requirements.txt`
  - `Procfile` configurado: `web: gunicorn config.wsgi:application --log-file -`
  - `build.sh` ejecuta: `pip install -r requirements.txt`
  - Render inicia automáticamente con Gunicorn

### Configurar WSGI o ASGI
- ✅ **COMPLETADO (WSGI)**
- **Detalles implementados**:
  - `config/wsgi.py` existe y está configurado correctamente
  - Django carga `settings` en función del entorno (dev/prod)
  - En Render usa `config.settings.prod` automáticamente
  - **Nota**: ASGI no es necesario a menos que uses WebSockets

### Configurar ambiente productivo en Render/Railway
- ✅ **COMPLETADO**
- **Detalles implementados**:
  - `runtime.txt` → `python-3.12.0`
  - `build.sh` → instalación de dependencias y migraciones
  - `Procfile` → comando de inicio con Gunicorn
  - `render.yaml` → configuración declarativa (alternativa)
  - `config/settings/prod.py` → seguridad (SSL, HSTS, etc.)
  - Variables de entorno en Render:
    - `SECRET_KEY` ✅
    - `DEBUG=False` ✅
    - `ALLOWED_HOSTS` ✅
    - `DJANGO_SETTINGS_MODULE=config.settings.prod` ✅

### Conexión a PostgreSQL en la nube
- ⚠️ **EN PROGRESO - Error de acceso actual**
- **Estado actual**:
  - `dj-database-url==3.0.1` instalado en `requirements.txt`
  - `psycopg2-binary==2.9.11` instalado en `requirements.txt`
  - `config/settings/prod.py` lee `DATABASE_URL` de variable de entorno
  - **Problema actual**: Error 1045 (acceso denegado MySQL) - usuario/contraseña incorrecta
  - **Solución pendiente**:
    1. Verificar tipo de BD (MySQL vs PostgreSQL) en `DATABASE_URL`
    2. Si MySQL: agregar `PyMySQL` y configurar `config/__init__.py`
    3. Si PostgreSQL: confirmar credenciales de acceso
    4. Hacer redeploy después de corregir credenciales

---

## ✔ VALIDACIÓN EN PRODUCCIÓN

### /health/ en producción
- ⚠️ **PENDIENTE DE VALIDACIÓN** (bloqueado por error de BD)
- **Implementado**:
  - `apps/core/views.py` → `health_check()` disponible
  - `apps/core/views.py` → `HealthAPIView` disponible
  - Rutas en `apps/core/urls.py` → `/api/health/` y `/api/health/status/`
- **Próximos pasos**: Validar acceso una vez se resuelva error de BD

### JWT en producción
- ⚠️ **PENDIENTE DE VALIDACIÓN** (bloqueado por error de BD)
- **Implementado**:
  - `djangorestframework_simplejwt==5.5.1` en `requirements.txt`
  - Configurado en `config/settings/base.py`:
    - `DEFAULT_AUTHENTICATION_CLASSES` incluye `JWTAuthentication`
    - `SIMPLE_JWT` configurado con `ACCESS_TOKEN_LIFETIME=1 hora`, `REFRESH_TOKEN_LIFETIME=7 días`
  - Endpoints de usuarios (login/refresh) listos en `apps/users/urls.py`
- **Próximos pasos**: Testear login y obtener token una vez BD esté operativa

### CRUD de citas operativo
- ⚠️ **PENDIENTE DE VALIDACIÓN** (bloqueado por error de BD)
- **Implementado**:
  - Modelos en `apps/citas/models.py` → `Cita`, `Servicio`
  - Serializers en `apps/citas/serializers.py`
  - Viewsets/Views en `apps/citas/views.py`
  - Rutas en `apps/citas/urls.py`
  - Permisos en `apps/citas/permissions.py`
- **Próximos pasos**: Validar GET, POST, PUT, DELETE una vez BD esté operativa

### Swagger accesible en producción
- ⚠️ **PENDIENTE DE VALIDACIÓN** (bloqueado por error de BD)
- **Implementado**:
  - `drf-yasg==1.21.11` en `requirements.txt`
  - Configurado en `config/urls.py`:
    - `GET /docs/` → Swagger UI
    - `GET /redoc/` → ReDoc
    - `GET /openapi.json/` → OpenAPI JSON
  - `SWAGGER_SETTINGS` en `config/settings/base.py`
- **Próximos pasos**: Acceder a `https://tu-app.onrender.com/docs/` una vez BD esté operativa

---

## ✔ DOCUMENTACIÓN

### Documentar despliegue en README
- ✅ **COMPLETADO**
- **Detalles documentados en `README.md`**:
  - Instalación local (venv, pip install)
  - Configuración de `.env`
  - Migraciones locales
  - Ejecución del servidor de desarrollo
  - **Despliegue en Render**:
    - Pasos exactos para crear Web Service
    - Configuración de variables de entorno
    - Creación de PostgreSQL
    - Verificación de endpoints
  - Stack tecnológico completo
  - Instrucciones de contribución
  - Licencia y créditos

---

## 📋 RESUMEN DE ESTADO ACTUAL

| Categoría | Estado | Observación |
|-----------|--------|-------------|
| **Pruebas** | ❌ No iniciado | Se recomienda comenzar con pytest |
| **Deployment** | ✅ Configurado | Gunicorn, WSGI, build scripts listos |
| **Ambiente Prod** | ✅ Configurado | Variables, settings/prod.py, seguridad OK |
| **BD en la nube** | ⚠️ En progreso | Error de credenciales MySQL - pendiente resolver |
| **Validación de endpoints** | ⚠️ Bloqueado | Depende de resolver error de BD |
| **Documentación** | ✅ Completa | README.md con instrucciones completas |

---

## 🎯 PRÓXIMOS PASOS INMEDIATOS

1. **Resolver error de acceso a BD en Render**:
   - Verificar `DATABASE_URL` en variables de entorno
   - Confirmar tipo de BD (MySQL vs PostgreSQL)
   - Actualizar credenciales si es necesario
   - Hacer redeploy

2. **Una vez BD esté operativa**:
   - Validar `/health/` → debe devolver estado 200
   - Validar `/admin/` → login funcional
   - Validar `/docs/` → Swagger cargue sin errores
   - Validar JWT → obtener token en login

3. **Iniciar suite de pruebas**:
   - Configurar pytest
   - Escribir pruebas unitarias
   - Escribir pruebas de integración
   - Lograr 50%+ coverage

---

**Última actualización**: 12 de diciembre de 2025
**Responsable**: Persona 4 (DevOps/Testing)
**Estado general**: 70% completado (deployment casi listo, falta: tests + validación en producción)
