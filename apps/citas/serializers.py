from rest_framework import serializers
from .models import Cita, Servicio
from datetime import date, datetime, time, timedelta

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = ['id', 'nombre', 'duracion_min']

class CitaSerializer(serializers.ModelSerializer):
    servicio_nombre = serializers.CharField(source='servicio.nombre', read_only=True)
    cliente_nombre = serializers.CharField(source='cliente.get_full_name', read_only=True)
    
    class Meta:
        model = Cita
        fields = ['id', 'cliente', 'cliente_nombre', 'servicio', 'servicio_nombre', 'fecha', 'hora', 'created_at']
        read_only_fields = ['id', 'cliente', 'cliente_nombre', 'created_at']

    def validate_fecha(self, value):
        """Validar que la fecha no esté en el pasado"""
        if value < date.today():
            raise serializers.ValidationError("La fecha no puede estar en el pasado.")
        return value

    def validate_hora(self, value):
        """Validar que la hora esté en formato correcto"""
        if not isinstance(value, time):
            raise serializers.ValidationError("La hora debe estar en formato HH:MM:SS")
        return value

    def validate(self, data):
        """Validaciones a nivel de objeto"""
        servicio = data.get('servicio')
        fecha = data.get('fecha')
        hora = data.get('hora')

        # Validar que el servicio existe
        if not servicio:
            raise serializers.ValidationError({"servicio": "El servicio es requerido."})

        # Verificar que no existe cita duplicada en el mismo horario
        if Cita.objects.filter(servicio=servicio, fecha=fecha, hora=hora).exists():
            raise serializers.ValidationError(
                "Ese horario ya está reservado para este servicio. Por favor elige otro."
            )

        # Validar que el horario esté dentro del horario laboral (8 AM - 6 PM)
        hora_inicio = time(8, 0)   # 8 AM
        hora_fin = time(18, 0)     # 6 PM
        
        if not (hora_inicio <= hora <= hora_fin):
            raise serializers.ValidationError(
                {"hora": f"El horario debe estar entre las 8:00 AM y 6:00 PM."}
            )

        return data

