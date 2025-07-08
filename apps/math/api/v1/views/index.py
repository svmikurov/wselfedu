"""Defines math app index view."""

from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response


class MathIndexViewSet(viewsets.ViewSet):
    """Math app index view."""

    def list(self, request: Request) -> Response:
        """Render data."""
        data = {
            'message': 'Hello',
            'balance': '333',
        }
        return Response(data)
