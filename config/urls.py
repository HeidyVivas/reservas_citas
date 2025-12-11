from django.contrib import admin
from django.urls import path, include, re_path

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

schema_view = get_schema_view(
    openapi.Info(
        title="API Reservas Citas",
        default_version='v1',
        description="Documentación oficial de la API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [

    # Panel administrador
    path("admin/", admin.site.urls),

    # Auth JWT (login y refresh)
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Health check (core)
    path("api/", include("apps.core.urls")),

    # Citas (create, list, detail)
    path("api/citas/", include("apps.citas.urls")),

    # Usuarios (register, profile, users-list)
    path("api/auth/", include("apps.users.urls")),

    # Swagger UI
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="swagger-ui"
    ),

    # Redoc
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc"
    ),

    # OpenAPI JSON
    re_path(
        r"^openapi\.json$",
        schema_view.without_ui(cache_timeout=0),
        name="openapi-json"
    ),
]
