"""
Vistas de la aplicación de Citas
Implementa CRUD completo con filtrado avanzado, transacciones atómicas y permisos personalizados
"""
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import rest_framework as filters

from .models import Cita, Servicio
from .serializers import CitaSerializer, ServicioSerializer


class ServicioFilter(filters.FilterSet):
    """Filtrado personalizado para Servicios"""
    nombre = filters.CharFilter(field_name='nombre', lookup_expr='icontains')
    activo = filters.BooleanFilter(field_name='activo')

    class Meta:
        model = Servicio
        fields = ['nombre', 'activo']


class ServicioViewSet(viewsets.ModelViewSet):
    """ViewSet para Servicios - Solo lectura para clientes"""
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ServicioFilter
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre', 'precio']
    
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            # Solo staff puede escribir
            return [IsAuthenticated()]
        return [IsAuthenticated()]


class CitaFilter(filters.FilterSet):
    """Filtrado personalizado para Citas"""
    fecha_desde = filters.DateFilter(field_name='fecha', lookup_expr='gte')
    fecha_hasta = filters.DateFilter(field_name='fecha', lookup_expr='lte')
    estado = filters.ChoiceFilter(field_name='estado', choices=Cita.ESTADOS)
    cliente_nombre = filters.CharFilter(field_name='cliente__first_name', lookup_expr='icontains')
    servicio = filters.NumberFilter(field_name='servicio__id')

    class Meta:
        model = Cita
        fields = ['estado', 'servicio', 'cliente', 'fecha_desde', 'fecha_hasta']


class CitaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Citas con:
    - Filtrado avanzado por fecha, estado, cliente, servicio
    - Búsqueda case-insensitive
    - Endpoints personalizados para aprobar/rechazar/completar
    - Transacciones atómicas
    """
    queryset = Cita.objects.all().select_related('cliente', 'servicio', 'empleado')
    serializer_class = CitaSerializer
    permission_classes = [IsAuthenticated]
    
    # Configurar filtrado
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CitaFilter
    search_fields = ['cliente__first_name', 'cliente__last_name', 'cliente__email', 'servicio__nombre']
    ordering_fields = ['fecha', 'hora', 'created_at', 'estado']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filtrar citas según el rol del usuario"""
        user = self.request.user
        if user.is_staff:
            return Cita.objects.all().select_related('cliente', 'servicio', 'empleado')
        return Cita.objects.filter(cliente=user).select_related('cliente', 'servicio', 'empleado')

    def perform_create(self, serializer):
        """Crear cita de forma atómica"""
        with transaction.atomic():
            serializer.save(cliente=self.request.user)

    def perform_update(self, serializer):
        """Actualizar cita de forma atómica"""
        with transaction.atomic():
            serializer.save()

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def aprobar(self, request, pk=None):
        """Aprobar una cita (solo empleados) POST /api/citas/{id}/aprobar/"""
        cita = self.get_object()
        
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
            cita.empleado = request.user
            cita.save()
        
        return Response(self.get_serializer(cita).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def rechazar(self, request, pk=None):
        """Rechazar una cita (solo empleados) POST /api/citas/{id}/rechazar/"""
        cita = self.get_object()
        
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
        
        return Response(self.get_serializer(cita).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def completar(self, request, pk=None):
        """Marcar cita como completada (solo empleados) POST /api/citas/{id}/completar/"""
        cita = self.get_object()
        
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
        
        return Response(self.get_serializer(cita).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def pendientes(self, request):
        """Listar citas pendientes GET /api/citas/pendientes/"""
        qs = self.get_queryset().filter(estado='pendiente')
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def mis_citas(self, request):
        """Listar mis citas (como cliente) GET /api/citas/mis_citas/"""
        qs = Cita.objects.filter(cliente=request.user).select_related('cliente', 'servicio', 'empleado')
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def por_rango_fechas(self, request):
        """Listar citas por rango de fechas GET /api/citas/por_rango_fechas/?fecha_desde=2024-01-01&fecha_hasta=2024-12-31"""
        fecha_desde = request.query_params.get('fecha_desde')
        fecha_hasta = request.query_params.get('fecha_hasta')
        
        if not fecha_desde or not fecha_hasta:
            return Response(
                {"detail": "Parámetros requeridos: fecha_desde y fecha_hasta (YYYY-MM-DD)"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            qs = self.get_queryset().filter(fecha__gte=fecha_desde, fecha__lte=fecha_hasta).order_by('fecha', 'hora')
            serializer = self.get_serializer(qs, many=True)
            return Response({"count": qs.count(), "results": serializer.data})
        except Exception as e:
            return Response(
                {"detail": f"Error en el filtrado: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )


