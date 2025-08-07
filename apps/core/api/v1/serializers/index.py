"""Defines Core app index serializer."""

from apps.users.api.v1.serializers.balance import BalanceSerializer


class IndexSerializer(
    BalanceSerializer,
):
    """Core app index serializer."""
