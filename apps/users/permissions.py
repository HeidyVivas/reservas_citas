from rest_framework.permissions import BasePermission

class IsEmployee(BasePermission):
    """Permite acceso solo a empleados o admin."""
    def has_permission(self, request, view):
        user = request.user

        if user.is_staff:
            return True
        
        # Si el usuario tiene perfil y es empleado
        return hasattr(user, "profile") and user.profile.rol == "empleado"


class IsOwner(BasePermission):
    """Solo el dueño del objeto puede verlo."""
    def has_object_permission(self, request, view, obj):
        return obj.cliente == request.user


class IsOwnerOrEmployee(BasePermission):
    """Empleado o admin ven todo. Cliente solo lo suyo."""
    def has_object_permission(self, request, view, obj):
        user = request.user

        # Admin ve todo
        if user.is_staff:
            return True

        # Empleado ve todo
        if hasattr(user, "profile") and user.profile.rol == "empleado":
            return True

        # Cliente solo lo suyo
        return obj.cliente == user
