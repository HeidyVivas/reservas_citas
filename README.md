#  API de Reservas de Citas – Backend Profesional (Django REST Framework)

**INSTITUCIÓN:** SENA - Centro de Biotecnología  
**PROGRAMA:** Análisis y Desarrollo de Software (ADSO)  
**GRUPO:** Heidy Vivas, Saira Aragón, Laura Fonseca, Juan José Bocanegra  
**INSTRUCTOR:** Esteban Hernández  
**FICHA:** 3203082

---

##  Descripción del Proyecto

API REST profesional y escalable para gestionar reservas de citas mediante Django REST Framework. Incluye:

✅ **Autenticación JWT** con SimpleJWT  
✅ **CRUD completo** para citas y servicios  
✅ **Filtrado avanzado** (fecha, estado, cliente, servicio)  
✅ **Búsqueda case-insensitive**  
✅ **Permisos granulares** (cliente, empleado, admin)  
✅ **Transacciones atómicas** para operaciones críticas  
✅ **Health Check endpoint**  
✅ **Documentación automática** con Swagger/OpenAPI  
✅ **Pruebas unitarias** (mínimo 50% cobertura)  
✅ **Manejo profesional de errores**  
✅ **Configuración dev/prod** separada  
✅ **Deployment ready** con Gunicorn  

---

##  Inicio Rápido

### 1. Requisitos Previos
- Python 3.10+
- PostgreSQL (recomendado) o SQLite (desarrollo)
- Git

### 2. Clonar el Repositorio
```bash
git clone https://github.com/HeidyVivas/reservas_citas.git
cd reservas_citas
```

### 3. Crear Entorno Virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 5. Configurar Variables de Entorno
```bash
cp .env.example .env
```

Edita `.env` y configura:
```ini
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=sqlite:///db.sqlite3
# O para PostgreSQL:
# DATABASE_URL=postgres://user:password@localhost:5432/reservas_db
```

### 6. Ejecutar Migraciones
```bash
python manage.py migrate
```

### 7. Crear Superusuario
```bash
python manage.py createsuperuser
```

### 8. Iniciar el Servidor
```bash
python manage.py runserver
```

Accede a: **http://127.0.0.1:8000/docs/**

---

##  Estructura del Proyecto

```
reservas_citas/
├── config/
│   ├── settings/
│   │   ├── base.py          # Configuración global
│   │   ├── dev.py           # Desarrollo
│   │   └── prod.py          # Producción
│   ├── urls.py              # Rutas globales
│   ├── wsgi.py              # WSGI para producción
│   └── exceptions.py        # Exception handler global
├── apps/
│   ├── core/                # Health check
│   ├── citas/               # CRUD de citas
│   │   ├── models.py        # Modelos (Cita, Servicio)
│   │   ├── serializers.py   # Serializadores
│   │   ├── views.py         # ViewSets y lógica
│   │   ├── urls.py          # Rutas
│   │   ├── permissions.py   # Permisos personalizados
│   │   └── tests.py         # Pruebas unitarias
│   └── users/               # Autenticación y usuarios
│       ├── models.py        # Modelo de usuario extendido
│       ├── views.py         # Autenticación JWT
│       ├── serializers.py   # Serializadores
│       ├── permissions.py   # Permisos
│       └── urls.py          # Rutas
├── manage.py                # Django CLI
├── requirements.txt         # Dependencias
├── .env.example            # Plantilla de variables
├── Procfile                # Configuración Heroku/Render
└── README.md               # Este archivo
```

---

##  Autenticación JWT

### Obtener Token
```bash
POST /api/auth/login/
Content-Type: application/json

{
  "username": "user@example.com",
  "password": "password123"
}

Respuesta:
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Usar Token en Requests
```bash
Authorization: Bearer <access_token>
```

### Refrescar Token
```bash
POST /api/auth/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

##  Endpoints Principales

### Health Check
```
GET /api/health/
```
Retorna estado del servidor y conexión a BD.

### Servicios
```
GET    /api/servicios/              # Listar servicios
POST   /api/servicios/              # Crear (staff)
GET    /api/servicios/<id>/         # Detalle
PUT    /api/servicios/<id>/         # Actualizar (staff)
DELETE /api/servicios/<id>/         # Eliminar (staff)
```

### Citas - CRUD
```
GET    /api/citas/                  # Listar con filtros
POST   /api/citas/                  # Crear cita
GET    /api/citas/<id>/             # Detalle
PUT    /api/citas/<id>/             # Actualizar
PATCH  /api/citas/<id>/             # Actualizar parcial
DELETE /api/citas/<id>/             # Eliminar
```

### Citas - Acciones Personalizadas
```
POST   /api/citas/<id>/aprobar/     # Aprobar (staff)
POST   /api/citas/<id>/rechazar/    # Rechazar (staff)
POST   /api/citas/<id>/completar/   # Completar (staff)
POST   /api/citas/<id>/cancelar/    # Cancelar

GET    /api/citas/pendientes/       # Solo pendientes
GET    /api/citas/mis_citas/        # Mis citas (cliente)
GET    /api/citas/por_rango_fechas/?fecha_desde=2024-01-01&fecha_hasta=2024-12-31
```

### Autenticación
```
POST   /api/auth/register/          # Registro
POST   /api/auth/login/             # Login
POST   /api/auth/refresh/           # Refrescar token
POST   /api/auth/verify/            # Verificar token
GET    /api/auth/profile/           # Mi perfil
```

---

##  Filtrado Avanzado

### Filtros Disponibles
```bash
# Por rango de fechas
GET /api/citas/?fecha_desde=2024-01-01&fecha_hasta=2024-12-31

# Por estado
GET /api/citas/?estado=pendiente

# Por cliente
GET /api/citas/?cliente=1

# Por servicio
GET /api/citas/?servicio=1

# Búsqueda
GET /api/citas/?search=juan

# Ordenamiento
GET /api/citas/?ordering=-fecha

# Combinado
GET /api/citas/?fecha_desde=2024-01-01&estado=aprobada&search=juan&ordering=-hora
```

---

##  Pruebas

### Ejecutar Pruebas
```bash
python manage.py test apps.citas.tests
```

### Con Cobertura
```bash
coverage run --source='.' manage.py test apps.citas.tests
coverage report
```

### Pruebas Implementadas
- ✅ Modelos (Servicio, Cita)
- ✅ Serializadores (validación)
- ✅ APIs (CRUD, filtros)
- ✅ Permisos (autenticación)
- ✅ Transacciones atómicas
- ✅ Health check

---

##  Seguridad

### Variables Críticas
- `SECRET_KEY` - Cambia en producción
- `DEBUG=False` en producción
- `ALLOWED_HOSTS` - Configura correctamente
- `CORS_ALLOWED_ORIGINS` - Whitelist de orígenes

### Headers de Seguridad
```python
SECURE_SSL_REDIRECT = True          # HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000      # 1 año
```

---

##  Deployment

### Preparar para Producción
```bash
# Instalar Gunicorn
pip install gunicorn

# Recolectar archivos estáticos
python manage.py collectstatic --noinput

# Probar localmente
gunicorn config.wsgi
```

### Deploying en Render.com
1. Sube el repositorio a GitHub
2. Conecta Render.com
3. Configurar variables de entorno:
   - `DEBUG=False`
   - `ALLOWED_HOSTS=tu-app.render.com`
   - `DATABASE_URL=postgres://...`
   - `SECRET_KEY=...`
4. Render automáticamente ejecutará migraciones
5. Tu API está lista en: `https://tu-app.render.com`

### Deploying en Railway.app
1. Conecta GitHub
2. Railway detecta Django automáticamente
3. Configura PostgreSQL
4. Deploy instantáneo

---

##  Configuración Avanzada

### Cambiar de SQLite a PostgreSQL
```ini
# .env
DATABASE_URL=postgres://user:password@localhost:5432/reservas_db
```

### Habilitar CORS para Frontend
```python
# config/settings/base.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://tudominio.com",
]
```

### Configurar Email
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

---

##  Métricas del Proyecto

| Métrica | Descripción | Estado |
|---------|-------------|--------|
| **Endpoints** | 20+ endpoints funcionales | ✅ |
| **Filtros Avanzados** | Rango fechas, estado, búsqueda | ✅ |
| **Cobertura de Pruebas** | Mínimo 50% | ✅ |
| **Transacciones Atómicas** | Operaciones críticas | ✅ |
| **Autenticación JWT** | SimpleJWT integrado | ✅ |
| **Permisos Granulares** | Cliente/Empleado/Admin | ✅ |
| **Health Check** | Monitoreo BD y servidor | ✅ |
| **Documentación Swagger** | OpenAPI integrado | ✅ |
| **DEBUG en Producción** | False obligatorio | ✅ |
| **Deployment** | Gunicorn + Render/Railway | ✅ |

---

##  Troubleshooting

### Error: "No module named 'cors_headers'"
```bash
pip install django-cors-headers
```

### Error: "DATABASE CONNECTION ERROR"
```bash
# Verificar que PostgreSQL esté corriendo
psql -U postgres

# O usar SQLite
DATABASE_URL=sqlite:///db.sqlite3
```

### Error: "DEBUG must be False in production"
```python
# Verifica .env en producción
DEBUG=False
```

### Swagger no funciona
```python
# Asegúrate que drf-yasg está instalado
pip install drf-yasg
```

---

##  Contacto y Soporte

- **GitHub:** [HeidyVivas/reservas_citas](https://github.com/HeidyVivas/reservas_citas)
- **Email Equipo:** [contacto@ejemplo.com]
- **Instructor:** Esteban Hernández

---

## 📄 Licencia

Este proyecto es parte del programa ADSO del SENA. Todos los derechos reservados.

---

**Última actualización:** 11 de Diciembre de 2025


#### Autenticación JWT (SimpleJWT)
Endpoints implementados:
- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/refresh/`
- `POST /api/auth/verify/`
- `GET /api/auth/profile/`

#### Parte READ del CRUD de citas
- `GET /api/citas/`
- `GET /api/citas/<id>/`

**Reglas:**
- Los clientes solo pueden ver sus propias citas
- Empleados y admin pueden ver todas las citas

#### Permisos personalizados
- `IsOwner`
- `IsEmployee`
- `IsOwnerOrEmployee`

Aplicados para proteger información sensible y mantener la integridad del sistema.

---

### Saira Aragón — Lógica + UPDATE + Filtros

#### Modelos principales
- **Servicio:** nombre, duración, precio
- **Cita:** fecha, hora, estado, cliente y servicio

#### Parte UPDATE del CRUD
- `PUT/PATCH /api/citas/<id>/`
- `POST /api/citas/<id>/aprobar/`
- `POST /api/citas/<id>/rechazar/`

**Estados de una cita:** `pendiente` → `aprobada` → `completada`

#### Filtros avanzados con django-filter
- Filtrar por rangos de fecha
- Filtrar por estado
- Buscar por nombre de cliente
- Filtrar por servicio

#### Transacciones atómicas
- Uso de `transaction.atomic()` para evitar inconsistencias al crear o modificar citas críticas

---

### Juan José Bocanegra — Pruebas + DELETE + Deployment

#### Parte DELETE del CRUD
Endpoints:
- `DELETE /api/citas/<id>/`
- `POST /api/citas/<id>/cancelar/`

**Reglas de borrado:**
- Solo dueño o admin puede eliminar una cita
- Las citas completadas no se pueden eliminar

#### Pruebas automatizadas
Pruebas implementadas:
- Unitarias e integración
- Autenticación JWT
- Permisos
- CRUD completo
- Filtros
- Cobertura mayor al 50%

#### Deployment en la nube
**Tecnologías:**
- Gunicorn / Uvicorn
- Railway, Render o Koyeb
- PostgreSQL en la nube

**Verificación en producción:**
- `/api/health/`
- JWT funcionando
- CRUD operativo
- Swagger accesible

---

## Arquitectura del Sistema

```
reservas_citas/
│
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── prod.py
│   └── urls.py
│
├── apps/
│   ├── users/
│   ├── citas/
│   └── core/
│
├── .env.example
├── requirements.txt
└── manage.py
```

---

##  Requisitos

- Python 3.10+
- Django 5
- Django REST Framework
- SimpleJWT
- PostgreSQL (producción)
- Entorno virtual

---

##  Instalación y Uso

### 1. Clonar el repositorio

```bash
git clone https://github.com/HeidyVivas/reservas_citas.git
cd reservas_citas
```

### 2. Crear entorno virtual

```bash
python -m venv .venv
source .venv/Scripts/activate  # En Windows
# source .venv/bin/activate    # En Linux/Mac
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Variables de entorno

Crear archivo `.env` basado en `.env.example`

### 5. Aplicar migraciones

```bash
python manage.py migrate
```

### 6. Ejecutar servidor

```bash
python manage.py runserver
```

---

##  Ejemplos de Uso

### Login

```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "laura",
  "password": "12345678"
}
```

### Perfil del usuario autenticado

```http
GET /api/auth/profile/
Authorization: Bearer <token>
```

### Listar citas

```http
GET /api/citas/
Authorization: Bearer <token>
```

---

##  Temas Aplicados

- Django REST Framework
- Autenticación JWT
- Permisos personalizados
- CRUD completo
- Filtros avanzados
- Transacciones atómicas
- Swagger
- Pruebas unitarias
- PostgreSQL
- Deployment en la nube

---

##  Contribuidores

- **Heidy Vivas** - Arquitectura, CREATE, Swagger
- **Laura Fonseca** - Autenticación, READ, Permisos
- **Saira Aragón** - Lógica, UPDATE, Filtros
- **Juan José Bocanegra** - Pruebas, DELETE, Deployment
