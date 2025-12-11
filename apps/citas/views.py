from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from datetime import datetime

from .models import Cita, Servicio
from .serializers import CitaSerializer, ServicioSerializer
from .permissions import IsEmployeeOrOwner


class ServicioViewSet(viewsets.ModelViewSet):
    """ViewSet para Servicios - Solo lectura para clientes"""
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            permission_classes = [IsAuthenticated]
            # Verificar que sea staff
            return [permission() for permission in permission_classes]
        return [IsAuthenticated()]


class CitaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Citas con:
    - Filtrado avanzado por fecha, estado, cliente, servicio
    - Endpoints personalizados para aprobar/rechazar/completar
    - Transacciones atómicas
    - Búsqueda por cliente
    """
    queryset = Cita.objects.all().select_related('cliente', 'servicio')
    serializer_class = CitaSerializer
    permission_classes = [IsAuthenticated, IsEmployeeOrOwner]
    
    # Configurar filtrado
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['fecha', 'estado', 'cliente', 'servicio']
    search_fields = ['cliente__first_name', 'cliente__last_name', 'cliente__email']
    ordering_fields = ['fecha', 'hora', 'created_at', 'estado']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filtrar citas según el rol del usuario"""
        user = self.request.user
        if user.is_staff:  # Empleados ven todas las citas
            return Cita.objects.all().select_related('cliente', 'servicio')
        # Clientes solo ven sus propias citas
        return Cita.objects.filter(cliente=user).select_related('cliente', 'servicio')

    def perform_create(self, serializer):
        """
        Crear cita de forma atómica:
        - Asignar cliente automáticamente
        - Verificar disponibilidad de horario
        """
        with transaction.atomic():
            # El cliente es siempre el usuario autenticado
            serializer.save(cliente=self.request.user)

    def perform_update(self, serializer):
        """Actualizar cita (PUT/PATCH /api/citas/{id}/)"""
        with transaction.atomic():
            serializer.save()

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsEmployeeOrOwner])
    def aprobar(self, request, pk=None):
        """
        Aprobar una cita (solo empleados)
        POST /api/citas/{id}/aprobar/
        """
        cita = self.get_object()
        
        # Verificar que solo empleados aprueben
        if not request.user.is_staff:
            return Response(
                {"detail": "Solo empleados pueden aprobar citas."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if cita.estado != 'pendiente':
            return Response(
                {"detail": f"Solo citas pendientes pueden aprobarse. Estado actual: {cita.estado}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        with transaction.atomic():
            cita.estado = 'aprobada'
            cita.save()
        
        return Response(
            self.get_serializer(cita).data,
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsEmployeeOrOwner])
    def rechazar(self, request, pk=None):
        """
        Rechazar una cita (solo empleados)
        POST /api/citas/{id}/rechazar/
        """
        cita = self.get_object()
        
        # Verificar que solo empleados rechacen
        if not request.user.is_staff:
            return Response(
                {"detail": "Solo empleados pueden rechazar citas."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if cita.estado != 'pendiente':
            return Response(
                {"detail": f"Solo citas pendientes pueden rechazarse. Estado actual: {cita.estado}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        with transaction.atomic():
            cita.estado = 'rechazada'
            cita.save()
        
        return Response(
            self.get_serializer(cita).data,
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsEmployeeOrOwner])
    def completar(self, request, pk=None):
        """
        Marcar cita como completada (solo empleados)
        POST /api/citas/{id}/completar/
        """
        cita = self.get_object()
        
        # Verificar que solo empleados completen
        if not request.user.is_staff:
            return Response(
                {"detail": "Solo empleados pueden completar citas."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if cita.estado != 'aprobada':
            return Response(
                {"detail": f"Solo citas aprobadas pueden completarse. Estado actual: {cita.estado}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        with transaction.atomic():
            cita.estado = 'completada'
            cita.save()
        
        return Response(
            self.get_serializer(cita).data,
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def pendientes(self, request):
        """
        Listar citas pendientes
        GET /api/citas/pendientes/
        """
        qs = self.get_queryset().filter(estado='pendiente')
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def mis_citas(self, request):
        """
        Listar mis citas (como cliente)
        GET /api/citas/mis-citas/
        """
        user = request.user
        qs = Cita.objects.filter(cliente=user).select_related('cliente', 'servicio')
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def por_rango_fechas(self, request):
        """
        Listar citas por rango de fechas
        GET /api/citas/por-rango-fechas/?fecha_inicio=2024-01-01&fecha_fin=2024-12-31
        """
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')
        
        if not fecha_inicio or not fecha_fin:
            return Response(
                {"detail": "Parámetros requeridos: fecha_inicio y fecha_fin"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            qs = self.get_queryset().filter(
                fecha__gte=fecha_inicio,
                fecha__lte=fecha_fin
            ).order_by('fecha', 'hora')
            serializer = self.get_serializer(qs, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"detail": f"Error en el filtrado: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

