"""Defines Index serializer."""

from typing import Any

from rest_framework import serializers


class IndexSerializer(serializers.Serializer[dict[str, Any]]):
    """Core app index serializer."""

    balance = serializers.DecimalField(
        max_digits=11,
        decimal_places=2,
        help_text='Current user balance',
    )
