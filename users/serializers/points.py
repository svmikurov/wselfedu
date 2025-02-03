"""User points serializer."""

from rest_framework import serializers


class PointsSerializer(serializers.Serializer):
    """User points serializer."""

    point_balance = serializers.CharField(max_length=255)
