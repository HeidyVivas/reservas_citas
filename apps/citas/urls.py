from django.urls import path
from .views import CitaCreateAPIView, CitaDetailAPIView

urlpatterns = [
    path('', CitaCreateAPIView.as_view(), name="cita-list-create"),
    path('<int:pk>/', CitaDetailAPIView.as_view(), name="cita-detail"),
]
