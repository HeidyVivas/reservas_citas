import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from apps.users.models import Profile


@pytest.mark.unit
class UserCreationTests(TestCase):
    """Tests para creación y validación de usuarios"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_with_valid_data(self):
        """Crear usuario con datos válidos"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.id is not None

    def test_user_profile_created_automatically(self):
        """Profile debe crearse automáticamente con signal post_save"""
        user = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        
        # Verificar que Profile existe
        assert hasattr(user, 'profile')
        assert user.profile.rol == 'cliente'  # default

    def test_user_email_unique(self):
        """Email debe ser único"""
        User.objects.create_user(
            username='user1',
            email='duplicate@example.com',
            password='pass123'
        )
        
        with pytest.raises(Exception):  # IntegrityError or similar
            User.objects.create_user(
                username='user2',
                email='duplicate@example.com',
                password='pass123'
            )


@pytest.mark.unit
class UserProfileTests(TestCase):
    """Tests para modelo Profile"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='profiletest',
            password='pass123'
        )

    def test_profile_has_valid_roles(self):
        """Profile debe tener uno de los roles válidos"""
        valid_roles = ['cliente', 'empleado', 'admin']
        self.user.profile.rol = 'empleado'
        self.user.profile.save()
        
        assert self.user.profile.rol in valid_roles

    def test_profile_string_representation(self):
        """Profile __str__ debe mostrar usuario y rol"""
        self.user.profile.rol = 'admin'
        self.user.profile.save()
        
        expected = f"{self.user.username} - admin"
        assert str(self.user.profile) == expected


@pytest.mark.unit
class UserPermissionTests(TestCase):
    """Tests para permisos basados en rol"""

    def setUp(self):
        self.client = APIClient()
        self.cliente = User.objects.create_user(
            username='cliente1',
            password='pass123'
        )
        self.cliente.profile.rol = 'cliente'
        self.cliente.profile.save()
        
        self.empleado = User.objects.create_user(
            username='empleado1',
            password='pass123'
        )
        self.empleado.profile.rol = 'empleado'
        self.empleado.profile.save()

    def test_cliente_role_assigned_correctly(self):
        """Cliente debe tener rol cliente"""
        assert self.cliente.profile.rol == 'cliente'

    def test_empleado_role_assigned_correctly(self):
        """Empleado debe tener rol empleado"""
        assert self.empleado.profile.rol == 'empleado'

    def test_unauthenticated_user_cannot_access_protected_endpoints(self):
        """Usuario no autenticado no puede acceder a endpoints protegidos"""
        # Sin token, intenta acceder a endpoint protegido
        response = self.client.get('/api/citas/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

