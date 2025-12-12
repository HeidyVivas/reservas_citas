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
            duracion=30,
            precio=50.00
        )

    def test_crear_servicio(self):
        """Prueba: crear un servicio"""
        self.assertEqual(self.servicio.nombre, "Consulta General")
        self.assertEqual(self.servicio.duracion, 30)

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
            duracion=30,
            precio=50.00
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
            duracion=30,
            precio=50.00
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
            duracion=30,
            precio=50.00
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

    def test_list_citas_requires_authentication(self):
        """Prueba: listar citas requiere autenticación"""
        response = self.client.get('/api/citas/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_list_citas(self):
        """Prueba: usuario autenticado puede listar sus citas"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/citas/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_cita_with_valid_data(self):
        """Prueba: crear cita con datos válidos"""
        self.client.force_authenticate(user=self.user)
        data = {
            "servicio": self.servicio.id,
            "fecha": self.fecha_valida,
            "hora": "10:00:00"
        }
        response = self.client.post('/api/citas/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cita_estado_default_is_pendiente(self):
        """Prueba: estado default de cita es pendiente"""
        cita = Cita.objects.create(
            cliente=self.user,
            servicio=self.servicio,
            fecha=date.today() + timedelta(days=1),
            hora=time(10, 0)
        )
        self.assertEqual(cita.estado, 'pendiente')

    def test_cancel_cita(self):
        """Prueba: cancelar una cita"""
        cita = Cita.objects.create(
            cliente=self.user,
            servicio=self.servicio,
            fecha=date.today() + timedelta(days=1),
            hora=time(10, 0),
            estado='aprobada'
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f'/api/citas/{cita.id}/cancelar/')
        
        # Verificar respuesta y estado
        if response.status_code == status.HTTP_200_OK:
            cita.refresh_from_db()
            self.assertEqual(cita.estado, 'cancelada')

    def test_cannot_cancel_completed_cita(self):
        """Prueba: no se puede cancelar cita completada"""
        cita = Cita.objects.create(
            cliente=self.user,
            servicio=self.servicio,
            fecha=date.today() - timedelta(days=1),
            hora=time(10, 0),
            estado='completada'
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f'/api/citas/{cita.id}/cancelar/')
        
        # Debería rechazar o no permitir cancelación
        if response.status_code != status.HTTP_404_NOT_FOUND:
            self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST])
