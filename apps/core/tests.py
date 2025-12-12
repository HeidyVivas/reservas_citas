import pytest
from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status


@pytest.mark.unit
class HealthCheckTests(TestCase):
    """Tests para endpoints de health check"""

    def setUp(self):
        self.client = APIClient()

    def test_health_check_endpoint_exists(self):
        """Verificar que GET /api/health/ devuelve 200"""
        response = self.client.get('/api/health/')
        assert response.status_code == status.HTTP_200_OK

    def test_health_check_response_format(self):
        """Verificar que la respuesta tiene estructura esperada"""
        response = self.client.get('/api/health/')
        data = response.json()
        
        assert 'status' in data
        assert 'timestamp' in data
        assert 'version' in data

    def test_health_status_api_endpoint(self):
        """Verificar que GET /api/health/status/ devuelve 200"""
        response = self.client.get('/api/health/status/')
        assert response.status_code == status.HTTP_200_OK

    def test_health_status_response_includes_database(self):
        """Verificar que response incluye estado de database"""
        response = self.client.get('/api/health/status/')
        data = response.json()
        
        assert 'status' in data
        assert 'database' in data


@pytest.mark.unit
class SwaggerDocsTests(TestCase):
    """Tests para endpoints de documentación Swagger"""

    def setUp(self):
        self.client = Client()

    def test_swagger_ui_loads(self):
        """Verificar que /docs/ carga sin errores"""
        response = self.client.get('/docs/')
        assert response.status_code == status.HTTP_200_OK

    def test_redoc_loads(self):
        """Verificar que /redoc/ carga sin errores"""
        response = self.client.get('/redoc/')
        assert response.status_code == status.HTTP_200_OK

    def test_openapi_json_available(self):
        """Verificar que /openapi.json/ devuelve JSON válido"""
        response = self.client.get('/openapi.json/')
        assert response.status_code == status.HTTP_200_OK
        assert response['Content-Type'] == 'application/json'
