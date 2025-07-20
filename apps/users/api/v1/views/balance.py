"""Defines user balance view."""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.users.api.v1.serializers.balance import BalanceSerializer
from apps.users.models import Balance


class BalanceViewSet(viewsets.ViewSet):
    """User balance viewset."""

    serializer_class = BalanceSerializer
    queryset = Balance.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request: Request) -> Response:
        """Render the user balance."""
        balance, _ = self.queryset.get_or_create(user=request.user)
        serializer = self.serializer_class(balance)
        return Response(serializer.data)
