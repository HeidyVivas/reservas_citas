from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView, CustomTokenRefreshView, ProfileView, UserListView
from rest_framework_simplejwt.views import TokenVerifyView

urlpatterns = [
    # Registrar un nuevo usuario
    path('auth/register/', RegisterView.as_view(), name='auth-register'),

    # Login: obtener tokens JWT
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Refrescar token JWT
    path('auth/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),

    # Verificar token JWT
    path('auth/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Obtener o actualizar perfil del usuario actual
    path('auth/profile/', ProfileView.as_view(), name='auth-profile'),

    # Listar todos los usuarios (solo admin)
    path('users/', UserListView.as_view(), name='users-list'),
]
