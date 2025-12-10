from django.test import TestCase
from django.urls import reverse
from app.models import Estudiante # pyright: ignore[reportMissingImports]

class EstudianteDeleteTest(TestCase):

    def setUp(self):
        self.estudiante = Estudiante.objects.create(
            nombre="Juan",
            apellido="Bocanegra",
            documento="123456"
        )

    def test_cancel_delete(self):
        # Simular que el usuario hace click en cancelar y vuelve
        response = self.client.get(reverse('cancelar_eliminar'))
        self.assertEqual(response.status_code, 302)  # redirección
