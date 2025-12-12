from django.db import models
from django.conf import settings

class Profile(models.Model):
    ROLE_CHOICES = (
        ('cliente', 'Cliente'),
        ('empleado', 'Empleado'),
        ('admin', 'Admin'),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    nombre = models.CharField(max_length=150, blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    rol = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='cliente'
    )

    def __str__(self):
        return f"{self.user.username} - {self.rol}"
