from django.urls import path
from .views import CitaCreateAPIView

urlpatterns = [
    path('citas/', CitaCreateAPIView.as_view(), name='cita-list-create'),
]
