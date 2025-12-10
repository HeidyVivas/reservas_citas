# config/settings/prod.py
from .base import *
import dj_database_url

DEBUG = env.bool("DEBUG", default=False)

# PostgreSQL via env DATABASE_URL o variables individuales
DATABASES = {
    "default": dj_database_url.parse(env('DATABASE_URL', default='postgres://user:pass@localhost:5432/dbname'))
}

# Seguridad HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Hosts
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

