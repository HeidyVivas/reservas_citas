from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from datetime import datetime

# Modelo para representar los servicios que ofrece la empresa.
class Servicio(models.Model):
    """Modelo de Servicios disponibles"""
    # Nombre único del servicio 
    nombre = models.CharField(max_length=100, unique=True)
    # Descripción del servicio, opcional
    descripcion = models.TextField(blank=True, null=True)
    # Duración del servicio en minutos
    duracion = models.IntegerField(help_text="Duración en minutos")
    # Precio del servicio
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    # Estado del servicio, por defecto activo
    activo = models.BooleanField(default=True)

    class Meta:
        # Ordenar por nombre del servicio en la base de datos
        ordering = ['nombre']
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'

    def __str__(self): # sirve para que el objeto tenga un nombre legible.
        return f"{self.nombre} ({self.duracion}min - ${self.precio})"


# Modelo para manejar las citas o reservas de los servicios.
class Cita(models.Model):
    """Modelo de Citas - Reservas de servicios"""

    # Definición de los posibles estados de la cita
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    )

    # Campos principales de la cita
    fecha = models.DateField(help_text="Fecha de la cita")
    hora = models.TimeField(help_text="Hora de la cita")
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='pendiente',
        help_text="Estado actual de la cita"
    )
    notas = models.TextField(blank=True, null=True, help_text="Notas adicionales")

    # Relaciones de la cita con otros modelos
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Relacionado con el modelo de Usuario
        on_delete=models.CASCADE, # si se borra el padre, también se borran los hijos.
        related_name='citas_como_cliente',
        help_text="Cliente que solicita la cita"
    )
    servicio = models.ForeignKey( # conecta un registro con otro.
        Servicio,  # Relacionado con el modelo de Servicio
        on_delete=models.CASCADE,
        related_name='citas',
        help_text="Servicio a reservar"
    )
    empleado = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Relacionado con el modelo de Usuario
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='citas_asignadas',
        help_text="Empleado asignado (opcional)"
    )

    # Campos de auditoría (fecha de creación y última actualización)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        # Ordenar las citas por fecha y hora (más reciente primero)
        ordering = ['-fecha', '-hora']
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'
        # Asegurarse de que no haya citas duplicadas para el mismo servicio en el mismo horario
        unique_together = [['fecha', 'hora', 'servicio']] #evitar que se repitan combinaciones específicas de campos en la base de datos.
        indexes = [
            models.Index(fields=['estado', '-fecha']),  # Índice para facilitar las búsquedas por estado y fecha
            models.Index(fields=['cliente', '-fecha']),  # Índice para facilitar las búsquedas por cliente y fecha
        ]

    def __str__(self): # sirve para que el objeto tenga un nombre legible.
        return f"Cita {self.id} - {self.cliente.get_full_name()} - {self.servicio.nombre} ({self.fecha} {self.hora})"

    def clean(self): #validar datos antes de que se guarden en la base de datos.
        """Validaciones del modelo"""
        # No permitir citas con fecha y hora en el pasado
        from django.utils import timezone
        if self.fecha and self.hora:
            cita_datetime = datetime.combine(self.fecha, self.hora)
            if cita_datetime < datetime.now():
                raise ValidationError("No se pueden crear citas en el pasado.") #sirve para detener la ejecución y lanzar un erro
    
    def save(self, *args, **kwargs):#Sobrescribe el guardado para correr validaciones antes de guardar
        # Ejecutar validaciones antes de guardar
        self.full_clean()
        super().save(*args, **kwargs)
