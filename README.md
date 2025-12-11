# API de Reservas de Citas – Backend Profesional (Django REST Framework)

---

**INSTITUCIÓN:** Servicio Nacional de Aprendizaje – SENA / Centro de Biotecnología  
**PROGRAMA:** Análisis y Desarrollo de Software  
**APRENDICES:** Juan José Bocanegra, Heidy Vivas, Saira Aragón, Laura Fonseca  
**INSTRUCTOR:** Esteban Hernández  
**FICHA:** 3203082  

---

#  ¿Qué hace el sistema?

Esta API permite realizar reservas de citas, gestionar usuarios con roles, controlar permisos según el tipo de usuario, aplicar filtros avanzados, autenticación JWT, pruebas automatizadas y despliegue en producción.  
Es un backend modular, robusto, seguro y con arquitectura profesional.

---

#  Distribución del Trabajo por Persona

---

## 👤 Heidy Vivas — Arquitectura + CREATE + Swagger

### Arquitectura
- Estructura profesional en `config/settings/`
- Variables de entorno (`.env`, `.env.example`)
- Configuración de CORS, CSRF, seguridad
- `DEBUG=False` en producción
- Conexión a BD local y en la nube

### Health Check
- Endpoint `/api/health/`
- Validación de conexión a BD

### CREATE – Citas
- `POST /api/citas/`
- Validación fecha, hora, cliente, servicio
- Validación de horario disponible

### Swagger / OpenAPI
- Configuración con `drf-yasg`
- Documentación automática de la API
- Seguridad JWT incluida

---

## 👤 Laura Fonseca — Autenticación + READ + Permisos (Laura Fonseca)

### App `users/`
- Creación de la app `users`
- Modelo `Profile` con:
  - teléfono  
  - rol (`cliente`, `empleado`, `admin`)  
  - OneToOne con usuario  

### Serializers
- `UserSerializer`
- `ProfileSerializer`

### Autenticación JWT (SimpleJWT)
Endpoints implementados:
- `POST /api/auth/register/`  
- `POST /api/auth/login/`  
- `POST /api/auth/refresh/`  
- `POST /api/auth/verify/`  
- `GET /api/auth/profile/`  

### READ – Citas
Endpoints:
- `GET /api/citas/`
- `GET /api/citas/<id>/`

Reglas:
- Clientes → solo sus citas  
- Empleados/Admin → todas las citas  

### Permisos Personalizados
- `IsOwner`
- `IsEmployee`
- `IsOwnerOrEmployee`

Aplicados a:
- Lectura de citas
- Endpoints protegidos

### Documentación (esta sección)
- Explicación de JWT
- Ejemplos de tokens y permisos
- Ejemplos de endpoints protegidos

---

## 👤 Saira Aragón — Lógica + UPDATE + Filtros

### Modelos
- `Servicio` → nombre, duración, precio
- `Cita` → fecha, hora, cliente, servicio, estado

### UPDATE – Citas
Endpoints:
- `PUT/PATCH /api/citas/<id>/`
- `POST /api/citas/<id>/aprobar/`
- `POST /api/citas/<id>/rechazar/`

Estados:
- pendiente → aprobada → completada

### Filtros Avanzados (django-filter)
- `?fecha__gte=`
- `?fecha__lte=`
- `?estado=`
- `?cliente__nombre__icontains=`
- `?servicio=`

### Transacciones Atómicas
```python
@transaction.atomic
def crear_cita_con_bloqueo(...):
    ...

## 👤 Juan Jose Bocanegra — Pruebas + DELETE + Deployment

###  DELETE – Citas

### Endpoints:
- `DELETE /api/citas/<id>/`
- `POST /api/citas/<id>/cancelar/`

### Reglas:
- Solo el **dueño** o un **admin** puede eliminar una cita.
- **No** se pueden eliminar citas que ya estén **completadas**.

---

###  Pruebas Automatizadas

Incluye pruebas:

- Unitarias e integración  
- Pruebas de autenticación JWT  
- Pruebas de permisos personalizados  
- Pruebas de filtros avanzados  
- Pruebas de CRUD completo  
- Cobertura mínima requerida: **> 50%**

---

###  Deployment

Tecnologías utilizadas:

- **Gunicorn / Uvicorn**
- Deploy en **Railway**, **Render** o **Koyeb**
- Base de datos **PostgreSQL** en la nube

### Verificación en Producción:
- `/api/health/`
- Autenticación JWT funcionando
- CRUD operativo
- Swagger accesible en producción

---

#  Arquitectura del Sistema

reservas_citas/
│── config/
│ ├── settings/
│ │ ├── base.py
│ │ ├── dev.py
│ │ ├── prod.py
│ ├── urls.py
│── apps/
│ ├── users/
│ ├── citas/
│ ├── core/
│── .env.example
│── requirements.txt
│── manage.py

---

#  Requisitos

- Python 3.10+
- Django 5
- Django REST Framework (DRF)
- SimpleJWT
- PostgreSQL (producción)
- Entorno virtual (`venv`)

---

#  Instalación y Uso

### 1. Clonar el repositorio
git clone https://github.com/HeidyVivas/reservas_citas.git

cd reservas_citas
### 2. Crear entorno virtual
python -m venv .venv
source .venv/Scripts/activate

shell
Copiar código

### 3. Instalar dependencias
pip install -r requirements.txt

markdown
Copiar código

### 4. Variables de entorno
Crear archivo `.env` basándose en `.env.example`.

### 5. Aplicar migraciones
python manage.py migrate

shell
Copiar código

### 6. Ejecutar servidor
python manage.py runserver

yaml
Copiar código

---

#  Ejemplos de Uso

###  Login
POST /api/auth/login/
{
"username": "laura",
"password": "12345678"
}

graphql
Copiar código

###  Perfil del Usuario Autenticado
GET /api/auth/profile/
Authorization: Bearer <access_token>

shell
Copiar código

### Listar Citas
GET /api/citas/
Authorization: Bearer <access_token>

yaml
Copiar código

---

#  Temas Aplicados

- Django REST Framework  
- JWT Authentication  
- Permisos personalizados  
- CRUD completo  
- Filtros avanzados  
- Transacciones atómicas  
- Swagger & Redoc  
- Pruebas unitarias  
- PostgreSQL  
- Deployment en la nube  

---

# 📌 Estado del Proyecto

### ✔ COMPLETADO  
Este backend cumple todos los requisitos técnicos, funcionales, de arquitectura, pruebas y despliegue solicitados por el instructor.
