"""Word study serializers."""

from rest_framework import serializers

from apps.lang import types
from apps.lang.models.word import AbstractWordModel

from . import base

# Word study parameters
# ---------------------


class WordParametersSerializer(
    base.TranslationMetaSerializer,
    base.TranslationSettingsSerializer,
):
    """Word parameters serializer."""


class StudyParametersSerializer(
    base.TranslationMetaSerializer,
    base.TranslationSettingsSerializer,
    base.PresentationSettingsSerializer,
):
    """Word study parameters serializer."""


class SetParametersSerializer(
    base.OptionsSerializer,
    base.TranslationMetaSerializer,
    base.TranslationSettingsSerializer,
    base.PresentationSettingsSerializer,
):
    """Set Word study parameters serializer."""


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
