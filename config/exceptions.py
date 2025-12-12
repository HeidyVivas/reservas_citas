"""
Exception Handler Global para la API
Maneja errores de forma profesional y consistente
"""
from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Handler personalizado para excepciones de Django REST Framework
    Retorna respuestas consistentes con estructura standard
    """
    response = exception_handler(exc, context)

    if response is None:
        # Capturar errores no controlados
        logger.error(f"Error no controlado: {exc}", exc_info=True)
        return Response(
            {
                "status": "error",
                "code": 500,
                "message": "Error interno del servidor",
                "detail": "Ha ocurrido un error inesperado. Por favor intenta de nuevo.",
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # Estructurar respuesta de error
    status_code = response.status_code
    
    # Mapear códigos de estado a mensajes claros
    error_mapping = {
        status.HTTP_400_BAD_REQUEST: "Datos inválidos",
        status.HTTP_401_UNAUTHORIZED: "Autenticación requerida",
        status.HTTP_403_FORBIDDEN: "No tienes permiso para esta acción",
        status.HTTP_404_NOT_FOUND: "Recurso no encontrado",
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Error interno del servidor",
    }

    # Construir respuesta personalizada
    data = {
        "status": "error" if status_code >= 400 else "success",
        "code": status_code,
        "message": error_mapping.get(status_code, "Error desconocido"),
        "detail": response.data if isinstance(response.data, dict) else str(response.data),
    }

    response.data = data
    return response
