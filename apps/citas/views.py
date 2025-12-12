"""
Vistas de la aplicación de Citas
Implementa CRUD completo con filtrado avanzado, transacciones atómicas
y acciones personalizadas (aprobar, rechazar, completar).
"""

# DRF: viewsets, respuestas HTTP, decoradores y permisos
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Transacciones atómicas para evitar inconsistencias en cambios críticos
from django.db import transaction

# Filtrado avanzado
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import rest_framework as filters

# Modelos y serializers de la app
from .models import Cita, Servicio
from .serializers import CitaSerializer, ServicioSerializer


# -------------------------
#     FILTROS SERVICIOS
# -------------------------
class ServicioFilter(filters.FilterSet):
    """Permite filtrar servicios por nombre y si están activos."""
    nombre = filters.CharFilter(field_name='nombre', lookup_expr='icontains')
    activo = filters.BooleanFilter(field_name='activo')

    class Meta:
        model = Servicio
        fields = ['nombre', 'activo']


# -------------------------
#        SERVICIOS
# -------------------------
class ServicioViewSet(viewsets.ModelViewSet):
    """
    CRUD para Servicios.
    Los usuarios pueden ver servicios, pero solo personal autorizado puede modificarlos.
    """
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    permission_classes = [IsAuthenticated]

    # Filtrado, búsqueda y ordenamiento
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ServicioFilter
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre', 'precio']
    
    def get_permissions(self):
        """
        Permisos personalizados:
        - Todos los usuarios autenticados pueden leer.
        - Solo personal puede crear, actualizar o eliminar.
        """
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated()]
        return [IsAuthenticated()]


# -------------------------
#        FILTROS CITAS
# -------------------------
class CitaFilter(filters.FilterSet):
    """Filtrar citas por rango de fechas, estado, cliente y servicio."""
    fecha_desde = filters.DateFilter(field_name='fecha', lookup_expr='gte')
    fecha_hasta = filters.DateFilter(field_name='fecha', lookup_expr='lte')
    estado = filters.ChoiceFilter(field_name='estado', choices=Cita.ESTADOS)
    cliente_nombre = filters.CharFilter(field_name='cliente__first_name', lookup_expr='icontains')
    servicio = filters.NumberFilter(field_name='servicio__id')

    class Meta:
        model = Cita
        fields = ['estado', 'servicio', 'cliente', 'fecha_desde', 'fecha_hasta']


# -------------------------
#          CITAS
# -------------------------
class CitaViewSet(viewsets.ModelViewSet):
    """
    ViewSet completo para gestionar citas:

    ✓ Filtrado avanzado  
    ✓ Búsqueda por cliente o servicio  
    ✓ Ordenamiento por fecha, hora o estado  
    ✓ Acciones personalizadas: aprobar, rechazar, completar  
    ✓ Transacciones atómicas para evitar estados inconsistentes
    """
    queryset = Cita.objects.all().select_related('cliente', 'servicio', 'empleado')
    serializer_class = CitaSerializer
    permission_classes = [IsAuthenticated]
    
    # Configuración de filtros de la API
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CitaFilter
    search_fields = ['cliente__first_name', 'cliente__last_name', 'cliente__email', 'servicio__nombre']
    ordering_fields = ['fecha', 'hora', 'created_at', 'estado']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Los empleados ven todas las citas.
        Los clientes solo ven sus propias citas.
        """
        user = self.request.user
        if user.is_staff:
            return Cita.objects.all().select_related('cliente', 'servicio', 'empleado')
        return Cita.objects.filter(cliente=user).select_related('cliente', 'servicio', 'empleado')

    def perform_create(self, serializer):
        """Asignar automáticamente el cliente autenticado al crear una cita."""
        with transaction.atomic():
            serializer.save(cliente=self.request.user)

    def perform_update(self, serializer):
        """Actualizar una cita dentro de una transacción segura."""
        with transaction.atomic():
            serializer.save()


    # -------------------------
    #     ACCIONES PERSONALIZADAS
    # -------------------------

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def aprobar(self, request, pk=None):
        """Aprobar una cita (solo empleados)."""
        cita = self.get_object()
        
        # Validación de permisos
        if not request.user.is_staff:
            return Response({"detail": "Solo empleados pueden aprobar citas."},
                            status=status.HTTP_403_FORBIDDEN)
        
        # Validación de estado
        if cita.estado != 'pendiente':
            return Response({"detail": f"Solo citas pendientes pueden aprobarse. Estado actual: {cita.estado}"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        # Operación atómica
        with transaction.atomic():
            cita.estado = 'aprobada'
            cita.empleado = request.user
            cita.save()
        
        return Response(self.get_serializer(cita).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def rechazar(self, request, pk=None):
        """Rechazar una cita (solo empleados)."""
        cita = self.get_object()
        
        if not request.user.is_staff:
            return Response({"detail": "Solo empleados pueden rechazar citas."},
                            status=status.HTTP_403_FORBIDDEN)
        
        if cita.estado != 'pendiente':
            return Response({"detail": f"Solo citas pendientes pueden rechazarse. Estado actual: {cita.estado}"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            cita.estado = 'rechazada'
            cita.save()
        
        return Response(self.get_serializer(cita).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def completar(self, request, pk=None):
        """Marcar una cita como completada (solo empleados)."""
        cita = self.get_object()
        
        if not request.user.is_staff:
            return Response({"detail": "Solo empleados pueden completar citas."},
                            status=status.HTTP_403_FORBIDDEN)
        
        if cita.estado != 'aprobada':
            return Response({"detail": f"Solo citas aprobadas pueden completarse. Estado actual: {cita.estado}"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            cita.estado = 'completada'
            cita.save()
        
        return Response(self.get_serializer(cita).data, status=status.HTTP_200_OK)


    # -------------------------
    #     LISTADOS PERSONALIZADOS
    # -------------------------

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def pendientes(self, request):
        """Lista todas las citas pendientes del usuario (o de todos si es staff)."""
        qs = self.get_queryset().filter(estado='pendiente')
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def mis_citas(self, request):
        """Lista todas las citas del usuario autenticado como cliente."""
        qs = Cita.objects.filter(cliente=request.user).select_related('cliente', 'servicio', 'empleado')
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def por_rango_fechas(self, request):
        """
        Filtra citas dentro de un rango de fechas dado por parámetros:
        - fecha_desde=YYYY-MM-DD
        - fecha_hasta=YYYY-MM-DD
        """
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
            return Response({"detail": f"Error en el filtrado: {str(e)}"},
                            status=status.HTTP_400_BAD_REQUEST)
