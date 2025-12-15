from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .serializers import UserSerializer, RegisterSerializer, ProfileSerializer
from .models import Profile

# =========================
# Registrar nuevo usuario
# =========================
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]  # Cualquiera puede registrarse

# =========================
# Login JWT personalizado
# =========================
class CustomTokenObtainPairView(TokenObtainPairView):
    pass

# =========================
# Refrescar token JWT
# =========================
class CustomTokenRefreshView(TokenRefreshView):
    pass

# =========================
# Obtener perfil del usuario actual
# =========================
class ProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados
    serializer_class = ProfileSerializer

    def get_object(self):
        """Devuelve el profile del usuario o crea uno temporal si no existe"""
        try:
            return self.request.user.profile
        except Profile.DoesNotExist:
            user = self.request.user
            return Profile(user=user, nombre='', telefono='', rol='cliente')

# =========================
# Listar todos los usuarios (solo admin)
# =========================
class UserListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]  # Solo admin puede ver
    serializer_class = UserSerializer
    queryset = User.objects.all()
