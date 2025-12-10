# config/settings/dev.py
from .base import *

DEBUG = True

# DB local SQLite
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# CORS durante dev (ajusta según necesites)
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[
    "http://localhost:3000",
    "http://localhost:8000",
])
CORS_ALLOW_CREDENTIALS = True