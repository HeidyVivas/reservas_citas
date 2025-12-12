from rest_framework.permissions import BasePermission

class IsAuthenticatedAndOwner(BasePermission):
    """
    Permiso personalizado:
    - Solo permite el acceso a usuarios autenticados
    """
    
    def has_permission(self, request, view):
        # Retorna True si el usuario está autenticado, False si no
        return request.user and request.user.is_authenticated
