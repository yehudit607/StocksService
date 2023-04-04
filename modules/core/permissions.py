from rest_framework.permissions import BasePermission

from StocksAPIProject.settings import ENV, DEV


class IsAuthenticatedOrDev(BasePermission):
    """
    Allows access only to authenticated users or dev users.
    """

    def has_permission(self, request, view):
        return bool((request.user and request.user.is_authenticated) or ENV == DEV)