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
    word_source = IdNameSerializer(required=False, allow_null=True)
    order = IdNameSerializer(required=False, allow_null=True)
    start_period = IdNameSerializer(required=False, allow_null=True)
    end_period = IdNameSerializer(required=False, allow_null=True)

    word_count = serializers.IntegerField(required=False, allow_null=True)
    question_timeout = serializers.IntegerField(
        required=False, allow_null=True
    )
    answer_timeout = serializers.IntegerField(required=False, allow_null=True)


class WordStudySelectSerializer(serializers.Serializer[types.WordParamsType]):
    """Serializer for Word study params select."""

    categories = IdNameSerializer(many=True)
    labels = IdNameSerializer(many=True)
    default_params = WordStudyParamsSerializer()


class WordStudyInfoSerializer(serializers.Serializer[types.Info]):
    """Serializer for Word study case info."""

    progress = serializers.IntegerField()


class WordStudyCaseSerializer(serializers.Serializer[types.PresentationCase]):
    """Serializer for Word study case."""

    case_uuid = serializers.UUIDField()
    definition = serializers.CharField(
        max_length=AbstractWordModel.WORD_LENGTH,
    )
    explanation = serializers.CharField(
        max_length=AbstractWordModel.WORD_LENGTH,
    )
    info = WordStudyInfoSerializer()


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
