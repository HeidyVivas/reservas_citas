from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .serializers import UserSerializer, RegisterSerializer, ProfileSerializer
from .models import Profile

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class CustomTokenObtainPairView(TokenObtainPairView):
    pass

class CustomTokenRefreshView(TokenRefreshView):
    pass

class ProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        try:
            return self.request.user.profile
        except Profile.DoesNotExist:
            user = self.request.user
            return Profile(user=user, nombre='', telefono='', rol='cliente')

class UserListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()
