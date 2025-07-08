"""Defines balance view."""

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from ....models.balance import Balance
from ..serializers.balance import BalanceSerializer


class BalanceViewSet(viewsets.ModelViewSet[Balance]):
    """Balance viewset."""

    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer

    def retrieve(
        self,
        request: Request,
        pk: int | None = None,
        **kwargs: object,
    ) -> Response:
        """Render the user balance."""
        balance = get_object_or_404(self.queryset, pk=pk)
        serializer = BalanceSerializer(balance)
        return Response(serializer.data)
