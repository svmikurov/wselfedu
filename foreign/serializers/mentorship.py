"""Foreign word mentorship serializers."""

from rest_framework import serializers


class ItemTestingAnswerSerializer(serializers.Serializer):
    """Foreign word testing exercise answer serializer."""

    answer = serializers.ListSerializer(
        allow_empty=False,
        child=serializers.IntegerField(),
    )
