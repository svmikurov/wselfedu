"""Defines Core app index viewset."""

from __future__ import annotations

from django.contrib.auth.models import AnonymousUser
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from typing_extensions import TYPE_CHECKING

from apps.core.presenters.index import get_index_data
from apps.core.types import BalanceDataType, IndexDataType

from ..serializers.index import IndexSerializer

if TYPE_CHECKING:
    from apps.users.models import CustomUser


class IndexViewSet(viewsets.ViewSet):
    """ViewSet for providing core application information.

    Provides endpoints for retrieving general information about the
    application, including user-specific data when authenticated.
    """

    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary='Get core information',
        description='Returns general application information '
        'and user-specific data if authenticated',
        responses={
            200: OpenApiResponse(
                response=IndexSerializer,
                description='Success response with core application data.\n'
                'Includes balance information for authenticated users if '
                'available.',
            ),
        },
        tags=['Core'],
    )
    @action(detail=False)
    def index(self, request: Request) -> Response:
        """Retrieve core application information.

        Returns:
            Response: Serialized core application data including:
                - General application information
                - User balance (if authenticated and balance exists)

        """
        data: IndexDataType = {
            'status': 'success',
            'data': self._get_index_data(request.user),
        }
        serializer = IndexSerializer(data)
        return Response(serializer.data)

    @staticmethod
    def _get_index_data(
        user: CustomUser | AnonymousUser,
    ) -> BalanceDataType:
        """Prepare data for the index response.

        Args:
            user: The authenticated user or anonymous user

        Returns:
            Dictionary containing all necessary data for the
            index response.

        """
        return get_index_data(user)
