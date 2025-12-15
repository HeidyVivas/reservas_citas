from .base import *
from decouple import config
import dj_database_url

# ====================
# GENERAL
# ====================
DEBUG = False

# ====================
# DATABASE (Render + PostgreSQL sin SSL + schema public)
# ====================
DATABASES = {
    "default": dj_database_url.parse(
        config("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=False,   # 🔑 filess.io NO soporta SSL
    )
}



# ====================
# ALLOWED HOSTS
# ====================
ALLOWED_HOSTS = config(
    "DJANGO_ALLOWED_HOSTS",
    cast=lambda v: [s.strip() for s in v.split(",")],
    default=[]
)

# ====================
# SECURITY (Render-safe)
# ====================
SECURE_SSL_REDIRECT = False  # Render maneja HTTPS por proxy

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# HSTS (seguro en Render)
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# ====================
# STATIC FILES
# ====================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

WHITENOISE_MANIFEST_STRICT = False

# ====================
# MEDIA FILES
# ====================
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ====================
# LOGGING
# ====================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
