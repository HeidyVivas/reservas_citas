from rest_framework.permissions import BasePermission

class IsAuthenticatedAndOwner(BasePermission):
    """
    Permite solo a usuarios autenticados
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
