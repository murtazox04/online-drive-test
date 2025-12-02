from rest_framework import permissions

from apps.users.models import User


class IsDriver(permissions.BasePermission):
    """
    Permission to only allow drivers to access the view.
    """

    message = "Only drivers can perform this action"

    def has_permission(self, request, view) -> bool:
        return (
            request.user
            and request.user.is_authenticated
            and request.user.user_type == User.UserType.DRIVER
        )
