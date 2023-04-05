from rest_framework import permissions


class IsAuthenticatedAndIsAdminOrReadOnly(permissions.BasePermission):
    """
    Global permission to check if request is a safe method
    if not, check if there is an user authenticated
    and if the authenticated use is admin.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated and request.user.is_admin:
            return True
        else:
            return False
