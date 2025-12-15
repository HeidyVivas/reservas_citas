from django.test import TestCase
from django.urls import reverse
from app.models import Estudiante  # Importa el modelo Estudiante

class EstudianteDeleteTest(TestCase):
    """Pruebas para la eliminación de Estudiantes"""

    def setUp(self):
        """Crear un estudiante de prueba antes de cada test"""
        self.estudiante = Estudiante.objects.create(
            nombre="Juan",
            apellido="Bocanegra",
            documento="123456"
        )

    def test_cancel_delete(self):
        """Simular que el usuario cancela la eliminación"""
        # Hacer GET a la URL de cancelar eliminar
        response = self.client.get(reverse('cancelar_eliminar'))
        
        # Verificar que se redirige correctamente (código 302)
        self.assertEqual(response.status_code, 302)
