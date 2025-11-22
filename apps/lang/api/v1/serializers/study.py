"""Word study serializers."""

from rest_framework import serializers

from apps.core.api.v1.serializers import IdNameSerializer
from apps.lang import models, types
from apps.lang.models.word import AbstractWordModel

# Presentation parameters
# -----------------------


class WordStudyParamsChoicesSerializer(
    serializers.Serializer[types.ParamsChoicesT],
):
    """Serializer for Word study params choices."""

    categories = IdNameSerializer(many=True)
    marks = IdNameSerializer(many=True)
    sources = IdNameSerializer(many=True)
    periods = IdNameSerializer(many=True)


class WordStudyInitialChoicesSerializer(
    serializers.Serializer[types.InitialChoicesT],
):
    """Serializer for Word study params initial choices."""

    category = IdNameSerializer(allow_null=True)
    mark = IdNameSerializer(allow_null=True)
    word_source = IdNameSerializer(allow_null=True)
    order = serializers.ChoiceField(
        choices=models.Params.TranslateChoices.choices, allow_null=True
    )
    start_period = IdNameSerializer(allow_null=True)
    end_period = IdNameSerializer(allow_null=True)


class PresentationSettingsSerializer(
    serializers.Serializer[types.ParamsChoicesT],
):
    """Serializer for Presentation settings."""

    word_count = serializers.IntegerField(allow_null=True)
    question_timeout = serializers.FloatField(allow_null=True)
    answer_timeout = serializers.FloatField(allow_null=True)


class UpdateParametersSerializer(
    WordStudyInitialChoicesSerializer,
    PresentationSettingsSerializer,
):
    """Serializer for update Presentation Parameters."""


class WordStudyPresentationParamsSerializer(
    WordStudyParamsChoicesSerializer,
    WordStudyInitialChoicesSerializer,
    PresentationSettingsSerializer,
):
    """Word study Presentation params serializer."""


# Presentation
# ------------


class WordStudyInfoSerializer(serializers.Serializer[types.InfoT]):
    """Serializer for Word study case info."""

    progress = serializers.IntegerField()


class WordStudyCaseSerializer(serializers.Serializer[types.PresentationCaseT]):
    """Serializer for Word study case."""

    case_uuid = serializers.UUIDField()
    definition = serializers.CharField(
        max_length=AbstractWordModel.WORD_LENGTH,
    )
    explanation = serializers.CharField(
        max_length=AbstractWordModel.WORD_LENGTH,
    )
    info = WordStudyInfoSerializer()


# Progress
# --------


class WordStudyProgressSerializer(serializers.Serializer[types.WordProgressT]):
    """Serializer for Word study progress."""

    case_uuid = serializers.UUIDField(
        required=True,
    )
    progress_type = serializers.ChoiceField(
        required=True,
        choices=['known', 'unknown'],
    )
