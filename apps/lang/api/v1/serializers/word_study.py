"""Word study serializers."""

from rest_framework import serializers

from apps.lang.types import WordParamsType, WordType


# TODO: Check fields max length
class WordStudyParamsSerializer(serializers.Serializer[WordParamsType]):
    """Word study params serializer."""

    category = serializers.CharField(
        max_length=200, required=False, allow_null=True, allow_blank=True
    )
    marks = serializers.CharField(
        max_length=200, required=False, allow_null=True, allow_blank=True
    )


# TODO: Check fields max length
class WordStudyPresentationsSerializer(serializers.Serializer[WordType]):
    """Word study presentation case serializer."""

    definition = serializers.CharField(max_length=200)
    explanation = serializers.CharField(max_length=200)
