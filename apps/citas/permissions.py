from rest_framework.permissions import BasePermission


class IsEmployeeOrOwner(BasePermission):
    """
    Permite que:
    - Los empleados (is_staff) accedan a cualquier cita
    - Los clientes solo accedan a sus propias citas
    """
    
    def has_permission(self, request, view):
        # Primero verificar que el usuario esté autenticado
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Los empleados (staff) pueden hacer cualquier cosa
        if request.user.is_staff:
            return True
        
        # Los clientes solo pueden acceder a sus propias citas
        return obj.cliente == request.user
