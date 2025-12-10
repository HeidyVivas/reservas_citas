from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Servicio, Cita
from datetime import date, time

User = get_user_model()

class CitaTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='pass')
        self.servicio = Servicio.objects.create(nombre='Corte', duracion_min=30)

    def test_crear_cita_y_prevenir_duplicado(self):
        Cita.objects.create(cliente=self.user, servicio=self.servicio, fecha=date.today(), hora=time(10,0))
        with self.assertRaises(Exception):
            # intenta crear la misma cita — la constraint debe fallar
            Cita.objects.create(cliente=self.user, servicio=self.servicio, fecha=date.today(), hora=time(10,0))
