from django.db import models
from django.contrib.auth.models import User

# Modelo de perfil extendido para el usuario
class Profile(models.Model):
    # Opciones de rol que puede tener un usuario
    ROLE_CHOICES = (
        ('cliente', 'Cliente'),   # Usuario normal / cliente
        ('empleado', 'Empleado'), # Usuario que atiende citas
        ('admin', 'Admin'),       # Administrador del sistema
    )

    # Relación uno a uno con el modelo User de Django
    # Si se elimina el User, se elimina también el Profile
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'  # Permite acceder al profile desde user.profile
    )

    # Campos adicionales del perfil
    nombre = models.CharField(max_length=150, blank=True)  # Nombre completo opcional
    telefono = models.CharField(max_length=30, blank=True)  # Teléfono opcional
    rol = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,   # Selección de rol
        default='cliente'       # Valor por defecto
    )

    def __str__(self):
        # Representación en texto del perfil: username y rol
        return f"{self.user.username} - {self.rol}"
