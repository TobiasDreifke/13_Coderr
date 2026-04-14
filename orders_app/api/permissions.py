from rest_framework import permissions


class IsBusinessUserForOrder(permissions.BasePermission):
    """Allow access only to authenticated business users tied to the order."""

    def has_permission(self, request, view):
        """Check whether the requester is an authenticated business user."""
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, 'profile')
            and request.user.profile.type == 'business'
        )

    def has_object_permission(self, request, view, obj):
        """Allow object access only for the business user assigned to the order."""
        return self.has_permission(request, view) and obj.business_user == request.user


class IsCustomerUser(permissions.BasePermission):
    """Allow access only to authenticated users with a customer profile."""

    def has_permission(self, request, view):
        """Check whether the requester is an authenticated customer user."""
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, 'profile')
            and request.user.profile.type == 'customer'
        )
