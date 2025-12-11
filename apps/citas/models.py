from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from datetime import datetime


class Servicio(models.Model):
    """Modelo de Servicios disponibles"""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    duracion = models.IntegerField(help_text="Duración en minutos")
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'

    def __str__(self):
        return f"{self.nombre} ({self.duracion}min - ${self.precio})"


class Cita(models.Model):
    """Modelo de Citas - Reservas de servicios"""
    
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    )

    # Campos principales
    fecha = models.DateField(help_text="Fecha de la cita")
    hora = models.TimeField(help_text="Hora de la cita")
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='pendiente',
        help_text="Estado actual de la cita"
    )
    notas = models.TextField(blank=True, null=True, help_text="Notas adicionales")

    # Relaciones
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='citas_como_cliente',
        help_text="Cliente que solicita la cita"
    )

    servicio = models.ForeignKey(
        Servicio,
        on_delete=models.CASCADE,
        related_name='citas',
        help_text="Servicio a reservar"
    )

    empleado = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='citas_asignadas',
        help_text="Empleado asignado (opcional)"
    )

    # Timestamps
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-fecha', '-hora']
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'
        # Evitar citas duplicadas en el mismo horario
        unique_together = [['fecha', 'hora', 'servicio']]
        indexes = [
            models.Index(fields=['estado', '-fecha']),
            models.Index(fields=['cliente', '-fecha']),
        ]

    def __str__(self):
        return f"Cita {self.id} - {self.cliente.get_full_name()} - {self.servicio.nombre} ({self.fecha} {self.hora})"

    def clean(self):
        """Validaciones del modelo"""
        # No permitir citas en el pasado
        from django.utils import timezone
        if self.fecha and self.hora:
            cita_datetime = datetime.combine(self.fecha, self.hora)
            if cita_datetime < datetime.now():
                raise ValidationError("No se pueden crear citas en el pasado.")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


