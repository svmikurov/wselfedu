"""DRF general."""

from django.db.models import Model
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView


class IsOwner(permissions.BasePermission):
    """Permission class fo object owner."""

    def has_object_permission(
        self,
        request: Request,
        view: APIView,
        obj: Model,
    ) -> bool:
        """Has current user the permission to the model instance."""
        return obj.user == request.user
