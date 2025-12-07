"""Study app base serializers."""

from rest_framework import serializers

from apps.lang import types


class ProgressPhaseSerializer(serializers.Serializer[types.ProgressPhase]):
    """Item study progress phase serializer."""

    is_study = serializers.BooleanField()
    is_repeat = serializers.BooleanField()
    is_examine = serializers.BooleanField()
    is_know = serializers.BooleanField()
