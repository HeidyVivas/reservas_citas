from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile  

# Serializador para el modelo User de Django
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']  # Campos visibles


# Serializador para el perfil extendido
class ProfileSerializer(serializers.ModelSerializer):
    # Anidar información del usuario dentro del perfil (solo lectura)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'nombre', 'telefono', 'rol']  # Campos del perfil


# Serializador para registrar nuevos usuarios junto con su perfil
class RegisterSerializer(serializers.ModelSerializer):
    # Campos adicionales que no están directamente en User
    password = serializers.CharField(write_only=True, required=True)  # Solo escritura
    email = serializers.EmailField(required=True)
    nombre = serializers.CharField(write_only=True, required=False, allow_blank=True)
    telefono = serializers.CharField(write_only=True, required=False, allow_blank=True)
    rol = serializers.ChoiceField(choices=Profile.ROLE_CHOICES, write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'nombre', 'telefono', 'rol']

    def create(self, validated_data):
        """
        Crear un nuevo usuario y su perfil asociado.
        Campos opcionales: nombre, telefono, rol (por defecto 'cliente')
        """
        nombre = validated_data.pop('nombre', '')
        telefono = validated_data.pop('telefono', '')
        rol = validated_data.pop('rol', 'cliente')

        # Crear usuario en Django
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        # Crear perfil asociado al usuario
        try:
            Profile.objects.create(user=user, nombre=nombre, telefono=telefono, rol=rol)
        except Exception:
            # Si ocurre algún error al crear el perfil, se ignora (aunque no es lo ideal)
            pass

        return user
