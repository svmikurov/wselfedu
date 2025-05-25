"""Defines the User app REST API views."""

from typing import Type

from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from .serializers import UserSerializer, UserUpdateSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """User view set."""

    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()

    def get_serializer_class(self) -> Type[Serializer]:
        """Return the class to use for the serializer."""
        if self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer

    @action(detail=False, methods=['get'])
    def me(self, request: Request) -> Response:
        """Render the user data."""
        serializer = self.get_serializer()
        return Response(serializer.data)
