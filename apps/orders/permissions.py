from rest_framework import permissions

from apps.users.models import User


class IsClient(permissions.BasePermission):
    """
    Permission to only allow clients to access the view.
    """

    message = "Only clients can perform this action"

    def has_permission(self, request, view) -> bool:
        return (
            request.user
            and request.user.is_authenticated
            and request.user.user_type == User.UserType.CLIENT
        )
