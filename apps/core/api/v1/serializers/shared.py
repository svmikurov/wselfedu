"""Shared serializers."""

from rest_framework import serializers

from apps.lang import types


class IdNameSerializer(serializers.Serializer[types.IdNameType]):
    """Serializer for objects with id and name fields."""

    id = serializers.IntegerField()
    name = serializers.CharField()
