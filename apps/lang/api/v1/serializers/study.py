"""Word study serializers."""

from rest_framework import serializers

from apps.lang.models.word import WORD_LENGTH
from apps.lang.types import (
    IdNameType,
    WordCaseParamsType,
    WordParamsType,
    WordType,
)


class IdNameSerializer(serializers.Serializer[IdNameType]):
    """Serializer for objects with id and name fields."""

    id = serializers.IntegerField()
    name = serializers.CharField()


class WordStudyParamsSerializer(serializers.Serializer[WordCaseParamsType]):
    """Serializer for Word study params."""

    category = IdNameSerializer(required=False, allow_null=True)
    label = IdNameSerializer(required=False, allow_null=True)  # type: ignore[assignment]
    word_count = serializers.IntegerField(required=False, allow_null=True)


class WordStudyCaseSerializer(serializers.Serializer[WordType]):
    """Serializer for Word study case."""

    definition = serializers.CharField(max_length=WORD_LENGTH)
    explanation = serializers.CharField(max_length=WORD_LENGTH)


class WordStudyParamsSelectSerializer(serializers.Serializer[WordParamsType]):
    """Serializer for Word study params select."""

    categories = IdNameSerializer(many=True)
    labels = IdNameSerializer(many=True)
    default = WordStudyParamsSerializer()
