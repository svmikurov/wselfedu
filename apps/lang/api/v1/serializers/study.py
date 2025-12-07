"""Word study serializers."""

from rest_framework import serializers

from apps.lang import types
from apps.lang.models.word import AbstractWordModel
from apps.study.api.v1 import serializers as study

from . import base

# Word study parameters
# ---------------------


class WordParametersSerializer(
    base.TranslationMetaSerializer,
    base.TranslationSettingsSerializer,
    study.ProgressPhaseSerializer,
):
    """Word parameters serializer."""


class StudyParametersSerializer(
    base.TranslationMetaSerializer,
    base.TranslationSettingsSerializer,
    base.PresentationSettingsSerializer,
    study.ProgressPhaseSerializer,
):
    """Word study parameters serializer."""


class SetParametersSerializer(
    base.OptionsSerializer,
    base.TranslationMetaSerializer,
    base.TranslationSettingsSerializer,
    base.PresentationSettingsSerializer,
    study.ProgressPhaseSerializer,
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


class WordStudyProgressSerializer(serializers.Serializer[types.ProgressCase]):
    """Serializer for Word study progress."""

    case_uuid = serializers.UUIDField(required=True)
    is_known = serializers.BooleanField(required=True)
