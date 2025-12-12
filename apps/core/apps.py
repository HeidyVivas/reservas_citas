from django.apps import AppConfig

# AppConfig permite configurar la aplicación dentro del proyecto Django.
class CoreConfig(AppConfig):
    # Define el tipo de campo automático por defecto para IDs (BigAutoField -> entero grande)
    default_auto_field = 'django.db.models.BigAutoField'

    # Nombre de la aplicación registrada dentro del proyecto
    name = 'apps.core'
