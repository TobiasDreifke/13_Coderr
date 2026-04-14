from rest_framework import permissions


class IsBusinessUser(permissions.BasePermission):
    """Allow access only to authenticated users with a business profile."""

    def has_permission(self, request, view):
        """Check whether the requester is an authenticated business user."""
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, 'profile')
            and request.user.profile.type == 'business'
        )


class IsOwner(permissions.BasePermission):
    """Allow modifications only for the user who owns the offer."""

    def has_object_permission(self, request, view, obj):
        """Check whether the current user owns the target object."""
        return obj.user == request.user
