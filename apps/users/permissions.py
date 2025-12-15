from rest_framework.permissions import BasePermission

# Permiso que permite acceso solo a empleados o admin
class IsEmployee(BasePermission):
    """Permite acceso solo a usuarios con rol empleado o staff/admin."""

    def has_permission(self, request, view):
        user = request.user

        # Los usuarios staff (administradores) pueden acceder siempre
        if user.is_staff:
            return True

        # Usuarios con perfil tipo 'empleado' pueden acceder
        return hasattr(user, "profile") and user.profile.rol == "empleado"


# Permiso que permite acceso solo al dueño del objeto
class IsOwner(BasePermission):
    """Solo el dueño del objeto (cliente) puede acceder."""

    def has_object_permission(self, request, view, obj):
        # Compara si el usuario actual es el cliente asociado al objeto
        return obj.cliente == request.user


# Permiso combinado: empleado/admin ve todo, cliente solo lo suyo
class IsOwnerOrEmployee(BasePermission):
    """
    Control de acceso:
    - Admin o empleado: puede ver cualquier objeto
    - Cliente: solo puede ver sus propios objetos
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Admin ve todo
        if user.is_staff:
            return True

        # Empleado ve todo
        if hasattr(user, "profile") and user.profile.rol == "empleado":
            return True

        # Cliente solo ve sus propios objetos
        return obj.cliente == user
