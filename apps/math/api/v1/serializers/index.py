"""Defines Math app serializer."""

from rest_framework import serializers

from apps.core.serializers.base import BalanceSerializer


class IndexSerializer(
    BalanceSerializer,
):
    """Math app index serializer."""

    exercises = serializers.ListField()
