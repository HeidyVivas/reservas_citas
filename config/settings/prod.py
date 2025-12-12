
"""
Configuración de Django para el entorno de PRODUCCIÓN.

Este archivo contiene todas las configuraciones de seguridad y optimización
necesarias para ejecutar la aplicación en un servidor de producción.
"""

from .base import *
import environ
import dj_database_url  # pyright: ignore[reportMissingImports]

# ============================================================================
# INICIALIZACIÓN DE ENVIRON
# ============================================================================
# Inicializar django-environ para leer variables de entorno
env = environ.Env()

# Leer archivo .env si existe (opcional en producción)
environ.Env.read_env(BASE_DIR / '.env')

# ============================================================================
# DEBUG - SEGURIDAD CRÍTICA
# ============================================================================
# OBLIGATORIO: DEBUG debe ser False en producción para evitar exponer
# información sensible en los mensajes de error
DEBUG = False

# ============================================================================
# BASE DE DATOS
# ============================================================================
# PostgreSQL vía variable de entorno DATABASE_URL
# Si DATABASE_URL no está configurada, usamos SQLite como fallback
if 'DATABASE_URL' in os.environ:
    # Parsear la URL de la base de datos (formato: postgres://user:pass@host:port/db)
    DATABASES = {
        "default": dj_database_url.parse(env('DATABASE_URL'))
    }
else:
    # Fallback a SQLite si DATABASE_URL no está definida
    # ADVERTENCIA: SQLite no es recomendado para producción con múltiples usuarios
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ============================================================================
# SEGURIDAD HTTPS
# ============================================================================
# Forzar redirección de HTTP a HTTPS
# Desactivar solo durante desarrollo local o si el servidor maneja SSL externamente
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=True)

# Las cookies de sesión solo se envían por HTTPS
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', default=True)

# Las cookies CSRF solo se envían por HTTPS
CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', default=True)

# Activar protección XSS del navegador
SECURE_BROWSER_XSS_FILTER = True

# Content Security Policy - Previene ataques XSS
SECURE_CONTENT_SECURITY_POLICY = {
    "default-src": ("'self'",),
}

# ============================================================================
# HSTS (HTTP Strict Transport Security)
# ============================================================================
# Indica a los navegadores que solo deben acceder al sitio vía HTTPS
# durante el tiempo especificado (1 año = 31536000 segundos)
SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', default=31536000)

# Aplicar HSTS también a todos los subdominios
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# Permitir que el dominio sea incluido en la lista de precarga HSTS
SECURE_HSTS_PRELOAD = True

# ============================================================================
# HOSTS PERMITIDOS
# ============================================================================
# Lista de dominios/IPs permitidos para servir la aplicación
# Ejemplo: ALLOWED_HOSTS=miapp.com,www.miapp.com,192.168.1.1
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

# Validación crítica: ALLOWED_HOSTS debe estar configurado en producción
if not ALLOWED_HOSTS:
    raise ValueError(
        "ALLOWED_HOSTS debe estar configurado en producción. "
        "Define la variable de entorno ALLOWED_HOSTS con los dominios permitidos."
    )

# ============================================================================
# CORS (Cross-Origin Resource Sharing)
# ============================================================================
# Orígenes permitidos para solicitudes cross-origin
# Ejemplo: CORS_ALLOWED_ORIGINS=https://frontend.com,https://app.com
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[])

# ============================================================================
# LOGGING
# ============================================================================
# Configuración de logs para producción
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# ============================================================================
# ARCHIVOS ESTÁTICOS
# ============================================================================
# URL base para archivos estáticos (CSS, JavaScript, imágenes)
STATIC_URL = '/static/'

# Directorio donde se recopilarán todos los archivos estáticos
# Ejecutar: python manage.py collectstatic
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise: No fallar si el manifiesto no es estricto
WHITENOISE_MANIFEST_STRICT = False

# ============================================================================
# ARCHIVOS MEDIA (uploads de usuarios)
# ============================================================================
# URL base para archivos subidos por usuarios
MEDIA_URL = '/media/'

# Directorio donde se guardan los archivos subidos
MEDIA_ROOT = BASE_DIR / 'media'
