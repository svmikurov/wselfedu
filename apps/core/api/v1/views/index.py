"""Defines Core app index viewset."""

from __future__ import annotations

from typing import Any

from django.contrib.auth.models import AnonymousUser
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from typing_extensions import TYPE_CHECKING

from apps.core.presenters.index import get_index_data

from ..serializers.index import IndexSerializer

if TYPE_CHECKING:
    from apps.users.models import CustomUser


class IndexViewSet(viewsets.ViewSet):
    """Core app index viewset."""

    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary='Get core information',
        description='Returns core information',
        responses={
            200: OpenApiResponse(
                response=IndexSerializer,
                description='Success response with user data',
            ),
        },
        tags=['Core'],
    )
    @action(detail=False)
    def index(self, request: Request) -> Response:
        """Core app index viewset."""
        serializer = IndexSerializer(self._get_index_data(request.user))
        return Response(serializer.data)

    @staticmethod
    def _get_index_data(
        user: CustomUser | AnonymousUser,
    ) -> dict[str, Any]:
        """Get response data."""
        return get_index_data(user)
