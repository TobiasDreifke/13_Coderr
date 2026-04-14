from rest_framework import permissions


class IsCustomerUser(permissions.BasePermission):
    """Allow only authenticated customers to create reviews."""

    def has_permission(self, request, view):
        """Check whether the requester is an authenticated customer user."""
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, 'profile')
            and request.user.profile.type == 'customer'
        )


class IsReviewOwner(permissions.BasePermission):
    """Allow review edits or deletes only for the review owner."""

    def has_object_permission(self, request, view, obj):
        """Allow safe reads for all and writes only for the review owner."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.reviewer == request.user
