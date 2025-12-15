"""
URL configuration for reservas_citas project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuración de Swagger/OpenAPI
schema_view = get_schema_view(
   openapi.Info(
      title="API de Reservas de Citas",
      default_version='v1',
      description="API REST para gestión de citas y servicios",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@reservas.local"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include([
        path('auth/', include('apps.users.urls')),
        path('citas/', include('apps.citas.urls')),
        path('health/', include('apps.core.urls')),
    ])),
    
    # Documentación Swagger
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='docs'),
]
