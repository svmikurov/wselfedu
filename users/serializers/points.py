"""User points serializer."""

from rest_framework import serializers


class PointsSerializer(serializers.Serializer):
    """User points serializer."""

    points = serializers.CharField(max_length=255)
