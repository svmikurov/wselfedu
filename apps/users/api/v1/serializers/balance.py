"""Defines general base serializers."""

from typing import Any

from django.core.validators import MinValueValidator
from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Valid balance',
            value={'balance': 113},
            description='Example of balance',
        )
    ]
)
class BalanceSerializer(serializers.Serializer[dict[str, Any]]):
    """Balance serializer."""

    balance = serializers.DecimalField(
        max_digits=5,
        decimal_places=0,
        help_text='Current user balance',
        validators=[MinValueValidator(0)],
    )
