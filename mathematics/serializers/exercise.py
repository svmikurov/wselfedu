"""Mathematics exercises serializers."""

from rest_framework import serializers


class MultiplicationSerializer(serializers.Serializer):
    """Multiplication exercise serializer."""

    question = serializers.CharField(max_length=255)
    answer = serializers.CharField(max_length=255)
