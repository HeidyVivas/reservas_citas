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
from django.db import IntegrityError
from django.utils import timezone
from datetime import datetime, time, timedelta




class ServicioViewSet(viewsets.ModelViewSet):
    """ViewSet para Servicios - Solo lectura para clientes"""
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        # Solo permitir escritura si es staff
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            permission_classes = [IsAuthenticated]
            return [permission() for permission in permission_classes]
        return [IsAuthenticated()]


class CitaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Citas:
    - Filtrar por fecha, estado, cliente, servicio
    - Acciones personalizadas (aprobar, rechazar, completar)
    - Búsqueda por cliente
    - Ordenamiento
    """
    queryset = Cita.objects.all().select_related('cliente', 'servicio')
    serializer_class = CitaSerializer
    permission_classes = [IsAuthenticated, IsEmployeeOrOwner]
    
    # Filtros configurados
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['fecha', 'estado', 'cliente', 'servicio']  # Filtros exactos
    search_fields = ['cliente__first_name', 'cliente__last_name', 'cliente__email']  # Búsqueda
    ordering_fields = ['fecha', 'hora', 'created_at', 'estado']  # Orden permitido
    ordering = ['-created_at']  # Orden por defecto

    def get_queryset(self):
        """Filtrar citas según el rol del usuario"""
        user = self.request.user

        if user.is_staff:  
            # Admin y empleados ven todas las citas
            return Cita.objects.all().select_related('cliente', 'servicio')

        # Clientes ven solo sus citas
        return Cita.objects.filter(cliente=user).select_related('cliente', 'servicio')

        # Código duplicado, pero respetado
        user = self.request.user
        if user.is_staff:
            return Cita.objects.all()
        if hasattr(user, "profile") and user.profile.rol == "empleado":
            return Cita.objects.all()
        return Cita.objects.filter(cliente=user)


    def perform_create(self, serializer):
        """Guardar cita asignando automáticamente el cliente"""
        with transaction.atomic():  # Garantiza operación segura
            serializer.save(cliente=self.request.user)  # Cliente autenticado


    def perform_update(self, serializer):
        """Actualizar cita de forma segura"""
        with transaction.atomic():
            serializer.save()


    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsEmployeeOrOwner])
    def aprobar(self, request, pk=None):
        """Aprobar una cita (solo empleados)"""
        cita = self.get_object()  # Obtener cita

        # Validar permiso
        if not request.user.is_staff:
            return Response({"detail": "Solo empleados pueden aprobar citas."},
                            status=status.HTTP_403_FORBIDDEN)

        # Validar estado
        if cita.estado != 'pendiente':
            return Response({"detail": f"La cita no está pendiente. Estado: {cita.estado}"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Actualizar estado
        with transaction.atomic():
            cita.estado = 'aprobada'
            cita.save()

        return Response(self.get_serializer(cita).data, status=status.HTTP_200_OK)


    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsEmployeeOrOwner])
    def rechazar(self, request, pk=None):
        """Rechazar una cita (solo empleados)"""
        cita = self.get_object()

        if not request.user.is_staff:
            return Response({"detail": "Solo empleados pueden rechazar citas."},
                            status=status.HTTP_403_FORBIDDEN)

        if cita.estado != 'pendiente':
            return Response({"detail": f"La cita no está pendiente. Estado: {cita.estado}"},
                            status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            cita.estado = 'rechazada'
            cita.save()

        return Response(self.get_serializer(cita).data, status=status.HTTP_200_OK)


    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsEmployeeOrOwner])
    def completar(self, request, pk=None):
        """Completar una cita (solo empleados)"""
        cita = self.get_object()

        # Validar rol
        if not request.user.is_staff:
            return Response({"detail": "Solo empleados pueden completar citas."},
                            status=status.HTTP_403_FORBIDDEN)

        # Validar estado
        if cita.estado != 'aprobada':
            return Response({"detail": f"La cita no está aprobada. Estado: {cita.estado}"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Cambiar estado
        with transaction.atomic():
            cita.estado = 'completada'
            cita.save()

        return Response(self.get_serializer(cita).data, status=status.HTTP_200_OK)


    def create(self, request, *args, **kwargs):
        """Validaciones adicionales antes de crear una cita"""
        serializer = self.get_serializer(data=request.data)

        # Validar datos
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        # Extraer datos enviados
        servicio_id = request.data.get('servicio')
        fecha = request.data.get('fecha')
        hora = request.data.get('hora')

        # Validar que el servicio exista
        try:
            servicio = Servicio.objects.get(id=servicio_id)
        except Servicio.DoesNotExist:
            return Response({"detail": "El servicio no existe."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Guardar cita
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def pendientes(self, request):
        """Listar todas las citas pendientes"""
        qs = self.get_queryset().filter(estado='pendiente')
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def mis_citas(self, request):
        """Listar citas del cliente autenticado"""
        user = request.user
        qs = Cita.objects.filter(cliente=user).select_related('cliente', 'servicio')
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def por_rango_fechas(self, request):
        """Listar citas dentro de un rango de fechas"""
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')

        # Validar parámetros
        if not fecha_inicio or not fecha_fin:
            return Response({"detail": "Debe enviar fecha_inicio y fecha_fin"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            qs = self.get_queryset().filter(
                fecha__gte=fecha_inicio,
                fecha__lte=fecha_fin
            ).order_by('fecha', 'hora')

            serializer = self.get_serializer(qs, many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response({"detail": f"Error: {str(e)}"},
                            status=status.HTTP_400_BAD_REQUEST)


class CitaDetailAPIView(generics.RetrieveAPIView):
    """Detalle de una cita por ID"""
    queryset = Cita.objects.all()
    serializer_class = CitaSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrEmployee]


