from django.db import models
from django.conf import settings

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    duracion_min = models.PositiveIntegerField(default=30)

    def __str__(self):
        return self.nombre

class Cita(models.Model):
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['servicio','fecha','hora'], name='unique_cita_slot')
        ]
        ordering = ['-fecha','-hora']

    def __str__(self):
        return f"{self.servicio} - {self.fecha} {self.hora} ({self.cliente})"
