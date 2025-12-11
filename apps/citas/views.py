from rest_framework import generics, permissions, serializers, status
from rest_framework.response import Response
from django.db import IntegrityError
from django.utils import timezone
from datetime import datetime, time, timedelta

from .models import Cita, Servicio
from .serializers import CitaSerializer
from apps.users.permissions import IsOwnerOrEmployee
from rest_framework.permissions import IsAuthenticated


class CitaCreateAPIView(generics.ListCreateAPIView):
    """
    API para listar y crear citas.
    
    POST /api/citas/ - Crear nueva cita
    GET /api/citas/ - Listar todas las citas
    """
    queryset = Cita.objects.all()
    serializer_class = CitaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Retorna las citas del usuario autenticado, empleados y admin ven todo."""
        user = self.request.user

        # admin ve todo
        if user.is_staff:
            return Cita.objects.all()

        # empleado ve todo
        if hasattr(user, "profile") and user.profile.rol == "empleado":
            return Cita.objects.all()

        # cliente ve solo sus citas
        return Cita.objects.filter(cliente=user)

    def perform_create(self, serializer):
        """
        Crear una nueva cita validando:
        - Disponibilidad de horario
        - No duplicados en el mismo horario
        - Datos válidos
        """
        try:
            serializer.save(cliente=self.request.user)
        except IntegrityError:
            raise serializers.ValidationError({
                "detail": "Ese horario ya está reservado para este servicio. Por favor elige otro."
            })

    def create(self, request, *args, **kwargs):
        """Override para agregar validaciones adicionales antes de guardar"""
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        servicio_id = request.data.get('servicio')
        fecha = request.data.get('fecha')
        hora = request.data.get('hora')

        # Validar servicio
        try:
            servicio = Servicio.objects.get(id=servicio_id)
        except Servicio.DoesNotExist:
            return Response(
                {"servicio": "El servicio no existe."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validar hora
        try:
            hora_obj = datetime.strptime(hora, "%H:%M:%S").time()
            hora_inicio = time(8, 0)  # 8 AM
            hora_fin = time(18, 0)    # 6 PM
            
            if not (hora_inicio <= hora_obj <= hora_fin):
                return Response(
                    {"hora": f"El horario debe estar entre {hora_inicio} y {hora_fin}."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ValueError:
            return Response(
                {"hora": "Formato de hora inválido. Usa HH:MM:SS."},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class CitaDetailAPIView(generics.RetrieveAPIView):
    """
    GET /api/citas/<id>/ - Ver detalle de cita (cliente dueño, empleado o admin)
    """
    queryset = Cita.objects.all()
    serializer_class = CitaSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrEmployee]
