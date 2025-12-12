from django.http import JsonResponse
from django.db import connection
from django.db.utils import OperationalError
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def health_check(request):
    """
    Health Check Endpoint
    Valida: servidor, base de datos, configuración
    Retorna 200 OK si todo funciona
    """
    try:
        # Verificar conexión a base de datos
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        db_status = "healthy"
        db_connected = True
    except OperationalError as e:
        logger.error(f"Database connection error: {e}")
        db_status = "unhealthy"
        db_connected = False

    response_data = {
        "status": "healthy" if db_connected else "degraded",
        "service": "API Reservas Citas",
        "version": "1.0.0",
        "database": db_status,
        "components": {
            "server": "healthy",
            "database": db_status,
        }
    }

    http_status = status.HTTP_200_OK if db_connected else status.HTTP_503_SERVICE_UNAVAILABLE
    return JsonResponse(response_data, status=http_status)


class HealthAPIView(APIView):
    """
    Health Check API View
    GET /api/health/status/
    Retorna estado detallado del sistema
    """
    permission_classes = []

    def get(self, request):
        """Obtener estado del sistema"""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            db_healthy = True
        except OperationalError:
            db_healthy = False

        data = {
            "status": "ok" if db_healthy else "error",
            "timestamp": timezone.now().isoformat(),
            "service": "API Reservas Citas",
            "version": "1.0.0",
            "database": "connected" if db_healthy else "disconnected",
        }

        return Response(data, status=status.HTTP_200_OK if db_healthy else status.HTTP_503_SERVICE_UNAVAILABLE)

