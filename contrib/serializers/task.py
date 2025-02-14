"""Task serializers."""

from rest_framework import serializers


class TaskSerializer(serializers.Serializer):
    """Task serializer."""

    question = serializers.CharField(max_length=255)
    solution = serializers.CharField(max_length=255)


class AnswerSerializer(serializers.Serializer):
    """Answer serializer."""

    answer = serializers.CharField(max_length=255)
