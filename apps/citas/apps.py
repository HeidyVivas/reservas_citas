from django.apps import AppConfig

# Configuración de la aplicación citas.
class CitasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # ID automático tipo BigInteger
    name = 'apps.citas'  # Ruta de la app dentro del proyecto
