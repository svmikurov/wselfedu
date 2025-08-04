"""Defines index view for Math API app."""

from typing import Any

from django.contrib.auth.models import AnonymousUser
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from apps.math.presenters.index import get_index_data
from apps.users.models import CustomUser

from ..serializers.index import MathIndexSerializer


class IndexViewSet(viewsets.ViewSet):
    """Math app viewset."""

    @extend_schema(
        summary='Get Math app general information',
        description='Returns Math app general information '
        'and user-specific data if authenticated',
        responses={
            200: OpenApiResponse(
                response=MathIndexSerializer,
                description='Success response with core application data.\n'
                'Includes balance information for authenticated users if '
                'available.',
            ),
        },
        tags=['Math'],
    )
    @action(detail=False)
    def index(self, request: Request) -> Response:
        """Render the Math app general info."""
        data = self._get_response_data(request.user)
        serializer = MathIndexSerializer(data)
        return Response(serializer.data)

    @staticmethod
    def _get_response_data(
        user: CustomUser | AnonymousUser,
    ) -> dict[str, Any]:
        """Get prepare data to response."""
        return get_index_data(user)
