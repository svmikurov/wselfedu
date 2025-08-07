"""Defines Math app index serializer."""

from rest_framework import serializers

from apps.users.api.v1.serializers.balance import BalanceSerializer


class MathIndexSerializer(
    BalanceSerializer,
):
    """Math app index serializer."""

    exercises = serializers.ListField()
