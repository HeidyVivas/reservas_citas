from rest_framework.routers import DefaultRouter
from .views import CitaViewSet, ServicioViewSet

router = DefaultRouter()
router.register(r'citas', CitaViewSet, basename='cita')
router.register(r'servicios', ServicioViewSet, basename='servicio')

urlpatterns = router.urls
