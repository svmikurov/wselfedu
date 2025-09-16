"""Custom permissions."""

from django.db.models import Model
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView


class IsOwnerOnly(permissions.BasePermission):
    """Permission to only allow owners of an object to access it."""

    def has_object_permission(
        self,
        request: Request,
        view: APIView,
        obj: Model,
    ) -> bool:
        """Check has user permission to access a specific object."""
        if not hasattr(obj, 'user'):
            return False
        return bool(request.user == obj.user)

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Check has user permission to access the view."""
        return bool(request.user and request.user.is_authenticated)
