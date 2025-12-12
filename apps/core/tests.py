import pytest
from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

# ---- TESTS PARA HEALTH CHECK ----
@pytest.mark.unit
class HealthCheckTests(TestCase):
    """Pruebas unitarias para los endpoints de verificación del sistema (health check)."""

    def setUp(self):
        # APIClient permite simular peticiones a endpoints DRF
        self.client = APIClient()

    def test_health_check_endpoint_exists(self):
        """Comprueba que el endpoint /api/health/ existe y responde 200 OK."""
        response = self.client.get('/api/health/')
        assert response.status_code == status.HTTP_200_OK

    def test_health_check_response_format(self):
        """
        Valida que la respuesta del health check contenga los campos esperados:
        - status: estado del servicio
        - timestamp: fecha/hora del chequeo
        - version: versión del API
        """
        response = self.client.get('/api/health/')
        data = response.json()
        
        assert 'status' in data
        assert 'timestamp' in data
        assert 'version' in data

    def test_health_status_api_endpoint(self):
        """Comprueba que el endpoint /api/health/status/ responde correctamente."""
        response = self.client.get('/api/health/status/')
        assert response.status_code == status.HTTP_200_OK

    def test_health_status_response_includes_database(self):
        """
        Verifica que el health status incluye información del estado de la base de datos.
        Clave esperada: 'database'
        """
        response = self.client.get('/api/health/status/')
        data = response.json()
        
        assert 'status' in data
        assert 'database' in data


# ---- TESTS PARA DOCUMENTACIÓN SWAGGER ----
@pytest.mark.unit
class SwaggerDocsTests(TestCase):
    """Pruebas para validar la disponibilidad de la documentación Swagger y Redoc."""

    def setUp(self):
        # Client usado para endpoints normales (no DRF)
        self.client = Client()

    def test_swagger_ui_loads(self):
        """Verifica que la interfaz Swagger UI /docs/ carga correctamente."""
        response = self.client.get('/docs/')
        assert response.status_code == status.HTTP_200_OK

    def test_redoc_loads(self):
        """Verifica que la documentación Redoc /redoc/ carga correctamente."""
        response = self.client.get('/redoc/')
        assert response.status_code == status.HTTP_200_OK

    def test_openapi_json_available(self):
        """Comprueba que el archivo JSON del esquema /openapi.json/ está disponible y es válido."""
        response = self.client.get('/openapi.json/')
        assert response.status_code == status.HTTP_200_OK
        assert response['Content-Type'] == 'application/json'
