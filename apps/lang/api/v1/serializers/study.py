"""Word study serializers."""

from rest_framework import serializers

from apps.core.api.v1.serializers import IdNameSerializer
from apps.lang import types
from apps.lang.models.word import AbstractWordModel


class WordStudyParamsSerializer(
    serializers.Serializer[types.WordCaseParamsType]
):
    """Serializer for Word study params."""

    category = IdNameSerializer(required=False, allow_null=True)
    label = IdNameSerializer(required=False, allow_null=True)  # type: ignore[assignment]
    word_count = serializers.IntegerField(required=False, allow_null=True)


class WordStudySelectSerializer(serializers.Serializer[types.WordParamsType]):
    """Serializer for Word study params select."""

    categories = IdNameSerializer(many=True)
    labels = IdNameSerializer(many=True)
    default_params = WordStudyParamsSerializer()


class WordStudyCaseSerializer(serializers.Serializer[types.WordCaseType]):
    """Serializer for Word study case."""

    case_uuid = serializers.UUIDField()
    definition = serializers.CharField(
        max_length=AbstractWordModel.WORD_LENGTH,
    )
    explanation = serializers.CharField(
        max_length=AbstractWordModel.WORD_LENGTH,
    )


class WordStudyProgressSerializer(
    serializers.Serializer[types.WordProgressType]
):
    """Serializer for Word study progress."""

    case_uuid = serializers.UUIDField(
        required=True,
    )
    progress_type = serializers.ChoiceField(
        required=True,
        choices=['known', 'unknown'],
    )
