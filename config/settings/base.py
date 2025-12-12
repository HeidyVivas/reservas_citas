"""
Configuración base de Django para el proyecto reservas_citas.

Este archivo contiene todas las configuraciones comunes que se comparten
entre los entornos de desarrollo y producción.
"""

import os
from pathlib import Path
import environ

# ============================================================================
# INICIALIZACIÓN DE ENVIRON
# ============================================================================
# Inicializar django-environ para leer variables de entorno
env = environ.Env()

# Construir rutas dentro del proyecto usando pathlib
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Leer archivo .env si existe
environ.Env.read_env(BASE_DIR / '.env')

# ============================================================================
# CONFIGURACIÓN DE SEGURIDAD
# ============================================================================
# SECRET_KEY debe estar en variables de entorno en producción
SECRET_KEY = env('SECRET_KEY', default='django-insecure-change-this-in-production-12345')

# ============================================================================
# APLICACIONES INSTALADAS
# ============================================================================
INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_yasg',
    'corsheaders',
    'django_filters',
    
    # Apps locales
    'apps.users',
    'apps.citas',
    'apps.core',
]

# ============================================================================
# MIDDLEWARE
# ============================================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise para archivos estáticos
    'corsheaders.middleware.CorsMiddleware',  # CORS debe ir antes de CommonMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ============================================================================
# CONFIGURACIÓN DE URLs Y WSGI
# ============================================================================
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# ============================================================================
# TEMPLATES
# ============================================================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ============================================================================
# BASE DE DATOS (se sobrescribe en prod.py y dev.py)
# ============================================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ============================================================================
# VALIDACIÓN DE CONTRASEÑAS
# ============================================================================
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ============================================================================
# MODELO DE USUARIO PERSONALIZADO
# ============================================================================
AUTH_USER_MODEL = 'users.Profile'

# ============================================================================
# INTERNACIONALIZACIÓN
# ============================================================================
LANGUAGE_CODE = 'es-co'  # Español de Colombia
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# ============================================================================
# ARCHIVOS ESTÁTICOS
# ============================================================================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []

# WhiteNoise - Configuración para servir archivos estáticos
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ============================================================================
# ARCHIVOS MEDIA (uploads de usuarios)
# ============================================================================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ============================================================================
# REST FRAMEWORK
# ============================================================================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}

# ============================================================================
# SIMPLE JWT (Autenticación con tokens)
# ============================================================================
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# ============================================================================
# SWAGGER/OpenAPI
# ============================================================================
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'USE_SESSION_AUTH': False,
    'JSON_EDITOR': True,
}

# ============================================================================
# CORS (Cross-Origin Resource Sharing)
# ============================================================================
CORS_ALLOW_ALL_ORIGINS = env.bool('CORS_ALLOW_ALL_ORIGINS', default=False)
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[])

# ============================================================================
# DEFAULT PRIMARY KEY FIELD TYPE
# ============================================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
