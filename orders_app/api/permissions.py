from rest_framework import permissions


class IsBusinessUserForOrder (permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, 'profile')
            and request.user.profile.type == 'business'
        )

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view) and obj.business_user == request.user


class IsCustomerUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, 'profile')
            and request.user.profile.type == 'customer'
        )
