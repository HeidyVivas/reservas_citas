
from rest_framework.routers import DefaultRouter
from .views import CitaViewSet, ServicioViewSet

router = DefaultRouter()
router.register(r'citas', CitaViewSet, basename='cita')
router.register(r'servicios', ServicioViewSet, basename='servicio')

urlpatterns = router.urls

from django.urls import path
from .views import CitaCreateAPIView, CitaDetailAPIView

urlpatterns = [
    path('', CitaCreateAPIView.as_view(), name="cita-list-create"),
    path('<int:pk>/', CitaDetailAPIView.as_view(), name="cita-detail"),
]

