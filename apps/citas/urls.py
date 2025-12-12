from rest_framework.routers import DefaultRouter
from .views import CitaViewSet, ServicioViewSet

# El router crear automáticamente todas las URLs
# necesarias para los ViewSets (listar, crear, actualizar, borrar, etc.)
router = DefaultRouter()

# Registrar el ViewSet de Citas. Esto genera rutas como:
# /citas/  (GET, POST)
# /citas/<id>/  (GET, PUT, PATCH, DELETE)
router.register(r'citas', CitaViewSet, basename='cita')

# Registrar el ViewSet de Servicios. Genera rutas similares:
# /servicios/
# /servicios/<id>/
router.register(r'servicios', ServicioViewSet, basename='servicio')

# urlpatterns queda con todas las rutas generadas por el router
urlpatterns = router.urls
