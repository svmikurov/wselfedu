"""Defines Math app index serializer."""

from rest_framework import serializers

from apps.core.serializers.base import BalanceSerializer


class MathIndexSerializer(
    BalanceSerializer,
):
    """Math app index serializer."""

    exercises = serializers.ListField()
