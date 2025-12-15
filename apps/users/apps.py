from django.apps import AppConfig

# Configuración de la aplicación Users
class UsersConfig(AppConfig):
    # Define el tipo de campo automático por defecto para los IDs de los modelos
    default_auto_field = "django.db.models.BigAutoField"

    # Nombre de la aplicación dentro del proyecto Django
    name = "apps.users"
       
