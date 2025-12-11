from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile  

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'nombre', 'telefono', 'rol']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)
    nombre = serializers.CharField(write_only=True, required=False, allow_blank=True)
    telefono = serializers.CharField(write_only=True, required=False, allow_blank=True)
    rol = serializers.ChoiceField(choices=Profile.ROLE_CHOICES, write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'nombre', 'telefono', 'rol']

    def create(self, validated_data):
        nombre = validated_data.pop('nombre', '')
        telefono = validated_data.pop('telefono', '')
        rol = validated_data.pop('rol', 'cliente')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        try:
            Profile.objects.create(user=user, nombre=nombre, telefono=telefono, rol=rol)
        except Exception:

            pass
        return user
