from rest_framework import serializers
from .models import Cita, Servicio


class ServicioSerializer(serializers.ModelSerializer):
    """Serializa los datos de un servicio para enviarlos en las respuestas."""
    
    class Meta:
        model = Servicio
        fields = ['id', 'nombre', 'duracion', 'precio'] # Campos que se muestran
        read_only_fields = ['id']  # El ID no se modifica, solo se lee


class CitaSerializer(serializers.ModelSerializer):
    """
    Serializa las citas. Incluye:
    - Datos normales de la cita
    - Información extra del servicio (servicio_detalle)
    - Nombre completo del cliente (cliente_nombre)
    """
    
    # Muestra los datos del servicio como un objeto anidado (solo lectura)
    servicio_detalle = ServicioSerializer(source='servicio', read_only=True)

    # Muestra el nombre completo del cliente sin necesidad de enviarlo desde el frontend
    cliente_nombre = serializers.CharField( #sirve para guardar texto corto.
        source='cliente.get_full_name',
        read_only=True
    )
    
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
        
        # Campos que no deberían ser modificados por el usuario
        read_only_fields = [
            'estado',
            'cliente',
            'cliente_nombre',
            'created_at'
        ]
