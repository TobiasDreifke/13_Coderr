from rest_framework import permissions


class IsBusinessUser(permissions.BasePermission):
    """
    Erlaubt nur Benutzern mit Business-Profil den Zugriff
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, 'profile')
            and request.user.profile.type == 'business'
        )


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Erlaubt Schreibzugriff nur dem Ersteller des Objekts
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user
