API de Reservas de Citas – Backend Profesional (Django REST Framework)

INSTITUCIÓN: Servicio Nacional de Aprendizaje – SENA / Centro de Biotecnología
PROGRAMA: Análisis y Desarrollo de Software
APRENDICES: Juan José Bocanegra, Heidy Vivas, Saira Aragón, Laura Fonseca
INSTRUCTOR: Esteban Hernández
FICHA: 3203082

¿Qué hace el sistema?

Esta API permite gestionar reservas de citas mediante un backend modular y seguro construido con Django REST Framework.
Incluye autenticación JWT, manejo de roles, permisos personalizados, filtros avanzados, pruebas automatizadas y una arquitectura profesional lista para producción.

Distribución del Trabajo por Persona
👤 Heidy Vivas — Arquitectura + CREATE + Swagger
Arquitectura y configuración del sistema

Organización profesional del proyecto en config/settings/ con archivos base.py, dev.py y prod.py.

Configuración de variables de entorno con .env y .env.example.

Ajustes de seguridad: CORS, CSRF, uso de DEBUG deshabilitado en producción.

Configuración de bases de datos locales y PostgreSQL en la nube.

Health Check

Implementación del endpoint /api/health/ para verificar el estado del servidor y la conexión a la base de datos.

Parte CREATE del CRUD de citas

Implementación del endpoint POST /api/citas/.

Validaciones de fecha, hora, servicio y disponibilidad.

Manejo profesional de errores.

Documentación con Swagger

Implementación de documentación automática con drf-yasg.

Inclusión de autenticación JWT dentro de la documentación.

👤 Laura Fonseca — Autenticación + READ + Permisos
App de usuarios

Creación de la app users.

Implementación del modelo Profile con teléfono y rol (cliente, empleado, admin).

Relación OneToOne entre usuario y perfil.

Serializers

UserSerializer y ProfileSerializer.

Autenticación JWT (SimpleJWT)

Endpoints implementados:

POST /api/auth/register/

POST /api/auth/login/

POST /api/auth/refresh/

POST /api/auth/verify/

GET /api/auth/profile/

Parte READ del CRUD de citas

GET /api/citas/

GET /api/citas/<id>/

Reglas:

Los clientes solo pueden ver sus propias citas.

Empleados y admin pueden ver todas las citas.

Permisos personalizados

IsOwner

IsEmployee

IsOwnerOrEmployee

Aplicados para proteger información sensible y mantener la integridad del sistema.

👤 Saira Aragón — Lógica + UPDATE + Filtros
Modelos principales

Servicio: nombre, duración, precio

Cita: fecha, hora, estado, cliente y servicio

Parte UPDATE del CRUD

PUT/PATCH /api/citas/<id>/

POST /api/citas/<id>/aprobar/

POST /api/citas/<id>/rechazar/

Estados de una cita:
pendiente → aprobada → completada

Filtros avanzados con django-filter

Filtrar por rangos de fecha

Filtrar por estado

Buscar por nombre de cliente

Filtrar por servicio

Transacciones atómicas

Uso de transaction.atomic() para evitar inconsistencias al crear o modificar citas críticas.

👤 Juan José Bocanegra — Pruebas + DELETE + Deployment
Parte DELETE del CRUD

Endpoints:

DELETE /api/citas/<id>/

POST /api/citas/<id>/cancelar/

Reglas de borrado:

Solo dueño o admin puede eliminar una cita.

Las citas completadas no se pueden eliminar.

Pruebas automatizadas

Pruebas implementadas:

Unitarias e integración

Autenticación JWT

Permisos

CRUD completo

Filtros

Cobertura mayor al 50%

Deployment en la nube

Tecnologías:

Gunicorn / Uvicorn

Railway, Render o Koyeb

PostgreSQL en la nube

Verificación en producción:

/api/health/

JWT funcionando

CRUD operativo

Swagger accesible

Arquitectura del Sistema

reservas_citas/
│── config/
│ ├── settings/
│ │ ├── base.py
│ │ ├── dev.py
│ │ ├── prod.py
│ ├── urls.py
│
│── apps/
│ ├── users/
│ ├── citas/
│ ├── core/
│
│── .env.example
│── requirements.txt
│── manage.py

Requisitos

Python 3.10+

Django 5

Django REST Framework

SimpleJWT

PostgreSQL (producción)

Entorno virtual

Instalación y Uso

Clonar el repositorio
git clone https://github.com/HeidyVivas/reservas_citas.git

cd reservas_citas

Crear entorno virtual
python -m venv .venv
source .venv/Scripts/activate

Instalar dependencias
pip install -r requirements.txt

Variables de entorno
Crear archivo .env basado en .env.example.

Aplicar migraciones
python manage.py migrate

Ejecutar servidor
python manage.py runserver

Ejemplos de Uso
Login

POST /api/auth/login/
{
"username": "laura",
"password": "12345678"
}

Perfil del usuario autenticado

GET /api/auth/profile/
Authorization: Bearer <access_token>

Listar citas

GET /api/citas/
Authorization: Bearer <access_token>

Temas Aplicados

Django REST Framework

Autenticación JWT

Permisos personalizados

CRUD completo

Filtros avanzados

Transacciones atómicas

Swagger

Pruebas unitarias

PostgreSQL

Deployment en la nube
