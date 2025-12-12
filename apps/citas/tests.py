"""
Pruebas unitarias para la aplicación de Citas
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
        """Crear datos de prueba para el servicio"""
        self.servicio = Servicio.objects.create(
            nombre="Consulta General",  # Nombre del servicio
            duracion_min=30  # Duración del servicio en minutos
        )

    def test_crear_servicio(self):
        """Verifica que un servicio se cree correctamente"""
        self.assertEqual(self.servicio.nombre, "Consulta General")
        self.assertEqual(self.servicio.duracion_min, 30)

    def test_string_representation(self):
        """Prueba: representación en texto del servicio"""
        # Verifica que la representación del servicio sea correcta
        self.assertEqual(str(self.servicio), "Consulta General")


class CitaModelTest(TestCase):
    """Pruebas para el modelo Cita"""

    def setUp(self):
        """Crear datos de prueba para usuario y cita"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.servicio = Servicio.objects.create(
            nombre="Consulta General",
            duracion_min=30
        )
        self.cita = Cita.objects.create( #representa la instancia actual del objeto.
            cliente=self.user,  # Asocia la cita al usuario
            servicio=self.servicio,  # Asocia la cita al servicio
            fecha=date.today() + timedelta(days=1),  # La cita es para el día siguiente
            hora=time(10, 0)  # Hora de la cita
        )

    def test_crear_cita(self):
        """Verifica que la cita se cree correctamente"""
        self.assertEqual(self.cita.cliente, self.user)
        self.assertEqual(self.cita.servicio, self.servicio)

    def test_cita_string_representation(self):
        """Verifica la representación en texto de la cita"""
        # y sea algo como: 'Consulta General - 2023-12-15 10:00:00 '
        expected = f"{self.servicio} - {self.cita.fecha} {self.cita.hora} ({self.user})"
        self.assertEqual(str(self.cita), expected)

    def test_constraint_unique_cita_slot(self):
        """Prueba que no se permita crear dos citas en el mismo horario"""
        from django.db import IntegrityError #un campo único duplicado
        
        with self.assertRaises(IntegrityError):
            # Intentamos crear una segunda cita con el mismo servicio en la misma fecha y hora
            Cita.objects.create(
                cliente=self.user,
                servicio=self.servicio,
                fecha=self.cita.fecha,
                hora=self.cita.hora
            )


class CitaSerializerTest(TestCase):
    """Pruebas para el serializador de Citas"""

    def setUp(self):
        """Crear datos de prueba para el usuario y servicio"""
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
        """Verifica que el serializer acepte datos válidos"""
        data = {
            "servicio": self.servicio.id,
            "fecha": (date.today() + timedelta(days=1)).isoformat(),
            "hora": "10:00:00"
        }
        serializer = CitaSerializer(data=data)
        # El serializer debe ser válido
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_serializer_fecha_pasada(self):
        """Verifica que el serializer rechace fechas pasadas"""
        data = {
            "servicio": self.servicio.id,
            "fecha": (date.today() - timedelta(days=1)).isoformat(),
            "hora": "10:00:00"
        }
        serializer = CitaSerializer(data=data)
        # El serializer debe ser inválido porque la fecha es pasada
        self.assertFalse(serializer.is_valid())
        self.assertIn("fecha", serializer.errors)


class CitaAPITest(APITestCase):
    """Pruebas para los endpoints de la API de Citas"""

    def setUp(self):
        """Crear cliente API, usuario y servicio para las pruebas"""
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
        """Verifica que se pueda crear una cita y que no permita duplicados"""
        cita = Cita.objects.create(
            cliente=self.user, 
            servicio=self.servicio, 
            fecha=date.today() + timedelta(days=1), 
            hora=time(10,0)
        )
        
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            # Intentamos crear una cita con el mismo servicio en la misma fecha y hora
            Cita.objects.create(
                cliente=self.user, 
                servicio=self.servicio, 
                fecha=date.today() + timedelta(days=1), 
                hora=time(10,0)
            )
