from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView, CustomTokenRefreshView, ProfileView, UserListView
from rest_framework_simplejwt.views import TokenVerifyView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/profile/', ProfileView.as_view(), name='auth-profile'),
    path('users/', UserListView.as_view(), name='users-list'),  # admin only
]
