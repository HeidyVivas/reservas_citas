from django.contrib import admin
from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

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

    path("admin/", admin.site.urls),

    # health check
    path("", include("apps.core.urls")),

    # swagger
    path("docs/", schema_view.with_ui('swagger', cache_timeout=0)),

    # openapi json
    path("openapi.json/", schema_view.without_ui()),
]
