"""
Pruebas unitarias para la aplicación de Citas
Cobertura mínima: 50%
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import date, time, timedelta
from .models import Cita, Servicio
from .serializers import CitaSerializer


class ServicioModelTest(TestCase):
    """Pruebas para el modelo Servicio"""

    def setUp(self):
        """Crear datos de prueba"""
        self.servicio = Servicio.objects.create(
            nombre="Consulta General",
            duracion_min=30
        )

    def test_crear_servicio(self):
        """Prueba: crear un servicio"""
        self.assertEqual(self.servicio.nombre, "Consulta General")
        self.assertEqual(self.servicio.duracion_min, 30)

    def test_string_representation(self):
        """Prueba: representación en texto del servicio"""
        self.assertEqual(str(self.servicio), "Consulta General")


class CitaModelTest(TestCase):
    """Pruebas para el modelo Cita"""

    def setUp(self):
        """Crear datos de prueba"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.servicio = Servicio.objects.create(
            nombre="Consulta General",
            duracion_min=30
        )
        self.cita = Cita.objects.create(
            cliente=self.user,
            servicio=self.servicio,
            fecha=date.today() + timedelta(days=1),
            hora=time(10, 0)
        )

    def test_crear_cita(self):
        """Prueba: crear una cita"""
        self.assertEqual(self.cita.cliente, self.user)
        self.assertEqual(self.cita.servicio, self.servicio)

    def test_cita_string_representation(self):
        """Prueba: representación en texto de la cita"""
        expected = f"{self.servicio} - {self.cita.fecha} {self.cita.hora} ({self.user})"
        self.assertEqual(str(self.cita), expected)

    def test_constraint_unique_cita_slot(self):
        """Prueba: no permite crear dos citas en el mismo horario"""
        from django.db import IntegrityError
        
        with self.assertRaises(IntegrityError):
            Cita.objects.create(
                cliente=self.user,
                servicio=self.servicio,
                fecha=self.cita.fecha,
                hora=self.cita.hora
            )


class CitaSerializerTest(TestCase):
    """Pruebas para el serializador de Citas"""

    def setUp(self):
        """Crear datos de prueba"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.servicio = Servicio.objects.create(
            nombre="Consulta General",
            duracion_min=30
        )

    def test_serializer_valido(self):
        """Prueba: serializer con datos válidos"""
        data = {
            "servicio": self.servicio.id,
            "fecha": (date.today() + timedelta(days=1)).isoformat(),
            "hora": "10:00:00"
        }
        serializer = CitaSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_serializer_fecha_pasada(self):
        """Prueba: rechaza fechas en el pasado"""
        data = {
            "servicio": self.servicio.id,
            "fecha": (date.today() - timedelta(days=1)).isoformat(),
            "hora": "10:00:00"
        }
        serializer = CitaSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("fecha", serializer.errors)


class CitaAPITest(APITestCase):
    """Pruebas para los endpoints de la API de Citas"""

    def setUp(self):
        """Crear datos de prueba"""
        self.client = APIClient()
        
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        
        self.servicio = Servicio.objects.create(
            nombre="Consulta General",
            duracion_min=30
        )
        
        self.fecha_valida = (date.today() + timedelta(days=1)).isoformat()

    def test_crear_cita_y_prevenir_duplicado(self):
        """Prueba: crear cita y prevenir duplicado"""
        cita = Cita.objects.create(
            cliente=self.user, 
            servicio=self.servicio, 
            fecha=date.today() + timedelta(days=1), 
            hora=time(10,0)
        )
        
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Cita.objects.create(
                cliente=self.user, 
                servicio=self.servicio, 
                fecha=date.today() + timedelta(days=1), 
                hora=time(10,0)
            )

