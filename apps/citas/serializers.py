from rest_framework import serializers
from .models import Cita, Servicio


class ServicioSerializer(serializers.ModelSerializer):
    """Serializador para Servicios"""
    class Meta:
        model = Servicio
        fields = ['id', 'nombre', 'duracion', 'precio']
        read_only_fields = ['id']


class CitaSerializer(serializers.ModelSerializer):
    """Serializador para Citas con información anidada de servicio y cliente"""
    servicio_detalle = ServicioSerializer(source='servicio', read_only=True)
    cliente_nombre = serializers.CharField(source='cliente.get_full_name', read_only=True)
    
    class Meta:
        model = Cita
        fields = [
            'id',
            'fecha',
            'hora',
            'estado',
            'cliente',
            'cliente_nombre',
            'servicio',
            'servicio_detalle',
            'created_at'
        ]
        read_only_fields = ['estado', 'cliente', 'cliente_nombre', 'created_at']


