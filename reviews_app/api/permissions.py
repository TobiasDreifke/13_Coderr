from rest_framework import permissions


class IsCustomerUser(permissions.BasePermission):
    """Nur Customer dürfen Reviews erstellen"""
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, 'profile')
            and request.user.profile.type == 'customer'
        )


class IsReviewOwner(permissions.BasePermission):
    """Nur der Ersteller darf die Review bearbeiten/löschen"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.reviewer == request.user