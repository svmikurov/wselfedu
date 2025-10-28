"""Word study serializers."""

from rest_framework import serializers

from apps.lang.types import IdNameType, WordParamsType, WordType

# Nested serializer
# -----------------


class IdNameSerializer(serializers.Serializer[IdNameType]):
    """Serializer for objects with id and name fields."""

    id = serializers.IntegerField()
    name = serializers.CharField()


# /presentation/
# --------------


# TODO: Check fields max length
class WordStudyPresentationsSerializer(serializers.Serializer[WordType]):
    """Word study presentation case serializer."""

    definition = serializers.CharField(max_length=200)
    explanation = serializers.CharField(max_length=200)


# /params/
# --------


class WordStudyParamsSerializer(serializers.Serializer[WordParamsType]):
    """Serializer for word study parameters."""

    user_id = serializers.IntegerField()
    categories = IdNameSerializer(many=True)
    labels = IdNameSerializer(many=True)
