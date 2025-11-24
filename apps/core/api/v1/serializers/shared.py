"""Shared serializers."""

from rest_framework import serializers

from apps.lang import types


class IdNameSerializer(serializers.Serializer[types.IdName]):
    """Serializer for objects with id and name fields."""

    id = serializers.IntegerField()
    name = serializers.CharField()


class CodeNameSerializer(serializers.Serializer[types.CodeName]):
    """Serializer for objects with code and name fields."""

    code = serializers.CharField()
    name = serializers.CharField()
