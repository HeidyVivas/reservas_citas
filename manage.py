#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Función principal para ejecutar comandos administrativos de Django"""
    # Configura la variable de entorno con los settings por defecto
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')

    try:
        # Importa la función que ejecuta comandos de Django (runserver, migrate, etc.)
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Mensaje de error si Django no está instalado o no se activó el virtualenv
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Ejecuta el comando que se pase por la terminal
    execute_from_command_line(sys.argv)

# Punto de entrada del script
if __name__ == '__main__':
    main()
