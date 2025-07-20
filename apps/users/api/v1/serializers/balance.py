"""Defines balance serializer."""

from rest_framework import serializers

from apps.users.models import Balance


class BalanceSerializer(serializers.ModelSerializer[Balance]):
    """Balance serializer."""

    class Meta:
        """Serializer configuration."""

        model = Balance
        fields = ['points']
