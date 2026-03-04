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


class IsOwner(permissions.BasePermission):
    """Nur der Ersteller darf bearbeiten/löschen"""
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
